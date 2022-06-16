from svg.path import parse_path
from xml.dom import minidom
import numpy as np
import re
from helperClasses.BrushClass import BrushClass
import juceComponentClasses as jC
import jucePaintingClasses as jP
import helperFunctions.SVGFunctions as svgfunctions


class ReadFigmaSVG:
    def __init__(self,file, componentName):

        print("Reading: "+file)

        self.componentTypes = ['component',
                               'label',
                               'button',
                               'rotaryslider',
                               'scrollbar',
                               'togglebutton',
                               'bounds']

        # setting up svg elements to be parsed
        doc = minidom.parse(file)  # parseString also exists
        elements = doc.childNodes
        elements = elements[0]
        self.svgWidth = int(elements.attributes['width'].value)
        self.svgHeight = int(elements.attributes['height'].value)
        elements = elements.childNodes
        self._removeTextNodes(elements)

        #Initialising
        self.componentName = componentName
        self.uniqueKey = None
        self.currentOpacity = [1.0]
        self.blendMode = 'normal'
        self.blendColour = '#000000'
        self.scalesWithBounds = False # Scaled multiplicatively width and height
        self.scalesLinearly = False # Scaled additively to preserve internal distances
        self.scalesEqually = False # Scaled multiplicatively by largest change in width or height
        self.defaultScaleSettings = {'scalesWithBounds':False,
                                     'scalesLinearly':False,
                                     'scalesRatio':False,
                                     'centre':False} # Change functions to carry this dict
        self.scaleSettings = []
        self.scaleSettings.append(self.defaultScaleSettings.copy()) #Scale settings is a stack container, pushing/popping current scale settings on the same end
        self.childComponents = []
        self.states = [] # painted objects go here now
        self.states.append(jP.ComponentGraphicState(self.componentName))

        # Getting component names, these elements will then be ignored as they will have their own svg file
        self.componentNames = []
        for element in elements:
            self._parseNodesForComponentNames(element)

        #Parsing the actual svg
        for element in elements:
            self._parseNode(element)

        doc.unlink()

    def getChildComponents(self):
        return self.childComponents

    def getComponentStates(self):
        return self.states

    def _removeTextNodes(self,nodes):

        for i, child in reversed(list(enumerate(nodes))):
            if child.nodeName == '#text':
                nodes.pop(i)

        return nodes

    def _parseNodesForComponentNames(self,element):
        elementId = ""
        try:
            elementId = element.attributes['id'].value
        except:
            elementId = ""
            pass
        if any("::"+componentType in elementId.lower() for componentType in self.componentTypes):
            elementDataName = element.attributes['id'].value
            elementDataName = re.split("#",elementDataName)
            childComponentName = elementDataName[-1]
            self.componentNames.append(childComponentName)
        else:
            elements = self._removeTextNodes(element.childNodes)
            for element in elements:
                self._parseNodesForComponentNames(element)

    # Initial entry point, nodes from this point will be recursively parsed until finished
    def _parseNode(self,element):

        self._generateUniqueKey()

        elementId = ""
        try:
            elementId = element.attributes['id'].value
        except:
            elementId = ""
            pass

        if elementId in self.componentNames: # If element is a component (since we already scanned for the component names)
            return
        if "::" in elementId:

            if "::ignore" in elementId.lower():
                pass
            elif "#" not in elementId:
                print(ValueError)
                print(elementId)
                print("you forgot the hashes")
                exit()
            elif any("::"+componentType in elementId.lower() for componentType in self.componentTypes):
                # get child name, parse element
                componentType = [componentType for componentType in self.componentTypes if "::"+componentType in elementId.lower()][0]
                self._parseComponentNode(element,componentType)
            elif "::state" in elementId.lower():
                stateName = elementId.split("#")[1]
                self.states.append(jP.ComponentGraphicState(self.componentName, stateName))
                self._parseGraphicsNode(element) # STOP GAP UNTIL BUTTON STATES ARE WORKED OUT
                self.states.append(jP.ComponentGraphicState(self.componentName))
            elif "::blendMode" in elementId.lower(): # Blendmode:blendcolour (in hash)
                self.blendMode = elementId.split("#")[1].split(":")[0]
                self.blendColour = elementId.split("#")[1].split(":")[1]
                self._parseGraphicsNode(element)
                self.blendMode = 'normal'
            elif "::scales" in elementId.lower():

                newScaleSettings = self.defaultScaleSettings.copy()
                if "bounds" in elementId:
                    newScaleSettings['scalesWithBounds'] = True
                elif "linear" in elementId:
                    newScaleSettings['scalesLinearly'] = True
                elif "centre" in elementId:
                    newScaleSettings['centre'] = True
                else:
                    print("Warning: ::scales not recognised")
                self.scaleSettings.append(newScaleSettings)

                self._parseGraphicsNode(element)

                self.scaleSettings.pop()
            else:
                pass
        elif element.nodeName == 'line':
            self._parseLineNode(element)
            return 'line'
        elif element.nodeName == 'path':
            self._parsePathNode(element)
            return 'path'
        elif element.nodeName == 'rect':
            self._parseRectNode(element)
            return 'rect'
        elif element.nodeName == 'circle':
            self._parseCircleNode(element)
            return 'circle'
        elif element.nodeName == 'ellipse':
            self._parseEllipseNode(element)
            return 'ellipse'
        elif element.nodeName == 'text':
            self._parseTextNode(element)
            return 'text'
        elif element.nodeName == 'g':
            # Errort catching for common mistake of not turning on "export with element id" in figma"
            try:
                element.attributes['id'].value
            except:
                exit("you didnt turn on element ids: "+self.componentName)
            self._parseGraphicsNode(element)
            return 'g'

    # Parsing component - will get rectangle element and use that as the set bounds in juce
    def _parseComponentNode(self,element,componentType="component"):

        brush = self._getBrush(element)

        elementDataName = element.attributes['id'].value
        elementDataName = re.split("#",elementDataName)
        childComponentName = elementDataName[-1]

        try:
            startX = element.attributes['x'].value
        except:
            startX = "0"
        try:
            startY = element.attributes['y'].value
        except:
            startY = "0"
        boundsX = element.attributes['width'].value
        boundsY = element.attributes['height'].value

        if componentType == "component":
            newChild = jC.ChildComponent(childComponentName,startX,startY,boundsX,boundsY)
            self.childComponents.append(newChild)
        elif componentType == "label":
            newChild = jC.Label(childComponentName,brush,startX,startY,boundsX,boundsY)
            self.childComponents.append(newChild)
        elif componentType == "button" or componentType == "togglebutton":
            newChild = jC.Button(childComponentName,startX,startY,boundsX,boundsY)
            self.childComponents.append(newChild)
        elif componentType == "scrollbar":
            newChild = jC.ScrollBar(childComponentName)
            self.childComponents.append(newChild)
        elif componentType == "rotaryslider":
            newChild = jC.RotarySlider(childComponentName,startX,startY,boundsX,boundsY)
            self.childComponents.append(newChild)
        elif componentType == "bounds":
            newChild = jC.Bounds(childComponentName,startX,startY,boundsX,boundsY)
            self.childComponents.append(newChild)
        else:
            exit("ERR: No component type found")


    # Most common svg node, contains more specific graphic elements within, therefore recursive call to self.parsenode
    def _parseGraphicsNode(self,element):

        ignoreNext = False

        opacityBool = self._checkOpacity(element)

        elements = self._removeTextNodes(element.childNodes)
        for element in elements:
            if ignoreNext == False:
                type = self._parseNode(element)
            else:
                ignoreNext == False

            if type in ['rect','circle','ellipse']:
                ignoreNext = False

        if opacityBool:
            self.currentOpacity.pop(-1)

    def _parseLineNode(self,element):

        brush = self._getBrush(element)

        try:
            x1 = element.attributes['x1'].value
        except:
            x1 = 0
        try:
            y1 = element.attributes['y1'].value
        except:
            y1 = 0
        try:
            x2 = element.attributes['x2'].value
        except:
            x2 = None
        try:
            y2 = element.attributes['y2'].value
        except:
            y2 = None



        try:
            name = element.attributes['id'].value
        except:
            name = str(str(element.nodeName)+self._generateUniqueKey())
        else:
            name = self._checkName(name)

        newPaintedObject = jP.Path(name,brush)
        newPaintedObject.setSVGBounds(self.svgWidth,self.svgHeight)
        newPaintedObject.setScalesWithBounds(self.scaleSettings[-1])

        LineStart = jP.PathMove(x1,y1)
        LineStart.setSVGBounds(self.svgWidth,self.svgHeight)
        LineStart.setScalesWithBounds(self.scaleSettings[-1])
        newPaintedObject.addInstruction(LineStart)

        LineEnd = jP.PathLine(x2,y2)
        LineEnd.setSVGBounds(self.svgWidth,self.svgHeight)
        LineEnd.setScalesWithBounds(self.scaleSettings[-1])
        newPaintedObject.addInstruction(LineEnd)

        self.states[-1].addPaintedObject(newPaintedObject)

    def _parsePathNode(self,element):

        brush = self._getBrush(element)

        d = element.attributes['d'].value

        try:
            transform = element.attributes['transform'].value
        except:
            pathTransform = svgfunctions.PathTransform()
        else:
            pathTransform = svgfunctions.PathTransform()
            pathTransform.setTransform(transform)

        # Use of parse_path python lib
        dInstructions = parse_path(d)

        newInstructions = []

        try:
            name = element.attributes['id'].value
        except:
            name = str(str(element.nodeName)+self._generateUniqueKey())
        else:
            name = self._checkName(name)
        newPaintedObject = jP.Path(name,brush)
        newPaintedObject.setSVGBounds(self.svgWidth,self.svgHeight)
        newPaintedObject.setScalesWithBounds(self.scaleSettings[-1])


        x = None
        y = None

        # Manual interpretation of instructions and putting into specific classes, these go inside the Path class via .addinstruction()
        for instruction in dInstructions:
            if instruction.__class__.__name__ == "Move":
                x = np.real(instruction.start)
                y = np.imag(instruction.start)
                x,y = pathTransform.applyTransforms([x,y])

                newIns = jP.PathMove(x,y)
                newIns.setSVGBounds(self.svgWidth,self.svgHeight)
                newIns.setScalesWithBounds(self.scaleSettings[-1])
                newPaintedObject.addInstruction(newIns)
            elif instruction.__class__.__name__ == "Line":

                x = np.real(instruction.end)
                y = np.imag(instruction.end)
                x,y = pathTransform.applyTransforms([x,y])

                newIns = jP.PathLine(x,y)
                newIns.setSVGBounds(self.svgWidth,self.svgHeight)
                newIns.setScalesWithBounds(self.scaleSettings[-1])
                newPaintedObject.addInstruction(newIns)

            elif instruction.__class__.__name__ == "CubicBezier":
                control1X = np.real(instruction.control1)
                control1Y = np.imag(instruction.control1)
                control1X,control1Y = pathTransform.applyTransforms([control1X,control1Y])

                control2X = np.real(instruction.control2)
                control2Y = np.imag(instruction.control2)
                control2X,control2Y = pathTransform.applyTransforms([control2X,control2Y])

                endX = np.real(instruction.end)
                endY = np.imag(instruction.end)
                endX,endY = pathTransform.applyTransforms([endX,endY])

                newIns = jP.PathCubic(control1X,control1Y,control2X,control2Y,endX,endY)
                newIns.setSVGBounds(self.svgWidth,self.svgHeight)
                newIns.setScalesWithBounds(self.scaleSettings[-1])

                newPaintedObject.addInstruction(newIns)

            elif instruction.__class__.__name__ == "QuadraticBezier":
                controlX = np.real(instruction.control)
                controlY = np.imag(instruction.control)
                controlX,controlY = pathTransform.applyTransforms([controlX,controlY])

                startX = np.real(instruction.start)
                startY = np.imag(instruction.start)
                startX,startY = pathTransform.applyTransforms([startX,startY])

                endX = np.real(instruction.end)
                endY = np.imag(instruction.end)
                endX,endY = pathTransform.applyTransforms([endX,endY])

                control1X = startX+(2/3)*(controlX-startX)
                control1Y = startY+(2/3)*(controlY-startY)

                control2X = endX+(2/3)*(controlX-endX)
                control2Y = endY+(2/3)*(controlY-endY)

                newIns = jP.PathCubic(control1X,control1Y,control2X,control2Y,endX,endY)
                newIns.setSVGBounds(self.svgWidth,self.svgHeight)
                newIns.setScalesWithBounds(self.scaleSettings[-1])

                newPaintedObject.addInstruction(newIns)

            elif instruction.__class__.__name__ == "Arc":


                radiusX = np.real(instruction.radius)
                radiusY = np.imag(instruction.radius)

                centreX,centreY,startAngle,deltaAngle = svgfunctions.endpointToCentreParameters(np.real(instruction.start),np.imag(instruction.start),np.real(instruction.end),np.imag(instruction.end),instruction.rotation,instruction.arc,instruction.sweep,radiusX,radiusY)


                centreX,centreY = pathTransform.applyTransforms([centreX,centreY])
                radiusX,radiusY = pathTransform.applyTransforms([radiusX,radiusY],type='scalar')
                startAngle = pathTransform.applyTransforms(startAngle,type='angle')

                newIns = jP.PathArc(centreX,centreY,radiusX,radiusY,instruction.rotation,startAngle,startAngle+deltaAngle)
                newIns.setSVGBounds(self.svgWidth,self.svgHeight)
                newIns.setScalesWithBounds(self.scaleSettings[-1])

                newPaintedObject.addInstruction(newIns)

            elif instruction.__class__.__name__ == "Close":
                newIns = jP.PathClose()
                newIns.setSVGBounds(self.svgWidth,self.svgHeight)
                newIns.setScalesWithBounds(self.scaleSettings[-1])
                newPaintedObject.addInstruction(newIns)

            else:
                print(instruction.__class__.__name__+' not understood!')

        self.states[-1].addPaintedObject(newPaintedObject)

    def _parseRectNode(self,element):

        brush = self._getBrush(element)

        try:
            x = element.attributes['x'].value
        except:
            x = 0
        try:
            y = element.attributes['y'].value
        except:
            y = 0
        try:
            rx = element.attributes['rx'].value
        except:
            rx = None
        try:
            ry = element.attributes['rx'].value
        except:
            ry = None

        width = element.attributes['width'].value
        height = element.attributes['height'].value

        try:
            name = element.attributes['id'].value
        except:
            name = str(str(element.nodeName)+self._generateUniqueKey())
        else:
            name = self._checkName(name)

        newPaintedObject = jP.Rect(name,brush)
        newPaintedObject.setSVGBounds(self.svgWidth,self.svgHeight)
        newPaintedObject.setScalesWithBounds(self.scaleSettings[-1])
        newPaintedObject.addData(x,y,width,height,rx,ry)
        self.states[-1].addPaintedObject(newPaintedObject)

    def _parseCircleNode(self,element):

        brush = self._getBrush(element)

        centreX = element.attributes['cx'].value
        centreY = element.attributes['cy'].value
        radius = element.attributes['r'].value

        try:
            name = element.attributes['id'].value
        except:
            name = str(str(element.nodeName)+self._generateUniqueKey())
        else:
            name = self._checkName(name)

        newPaintedObject = jP.Ellipse(name,brush)
        newPaintedObject.setSVGBounds(self.svgWidth,self.svgHeight)
        newPaintedObject.setScalesWithBounds(self.scaleSettings[-1])
        newPaintedObject.addData(centreX,centreY,radius,radius)
        self.states[-1].addPaintedObject(newPaintedObject)

    def _parseEllipseNode(self,element):

        brush = self._getBrush(element)

        centreX = element.attributes['cx'].value
        centreY = element.attributes['cy'].value
        radiusX = element.attributes['rx'].value
        radiusY = element.attributes['ry'].value

        try:
            name = element.attributes['id'].value
        except:
            name = str(str(element.nodeName)+self._generateUniqueKey())
        else:
            name = self._checkName(name)

        newPaintedObject = jP.Ellipse(name,brush)
        newPaintedObject.setSVGBounds(self.svgWidth,self.svgHeight)
        newPaintedObject.setScalesWithBounds(self.scaleSettings[-1])
        newPaintedObject.addData(centreX,centreY,radiusX,radiusY)
        self.states[-1].addPaintedObject(newPaintedObject)

    # Function for interpretating brush settings for a node
    def _getBrush(self,element):

        brush = BrushClass()
        brush.setBlendModeAndColour(self.blendMode,self.blendColour)
        try:
            opacity = element.attributes['opacity'].value
        except:
            brush.setAttributeFromSVG('opacity',self.currentOpacity[-1])
        else:
            brush.setAttributeFromSVG('opacity',opacity)

        try:
            opacity = element.attributes['fill-opacity'].value
        except:
            brush.setAttributeFromSVG('opacity',self.currentOpacity[-1])
        else:
            brush.setAttributeFromSVG('opacity',opacity)

        try:
            fillVal = element.attributes['fill'].value
        except:
            pass
        else:
            brush.setAttributeFromSVG('fill',fillVal)

        try:
            strokeVal = element.attributes['stroke'].value
        except:
            pass
        else:
            brush.setAttributeFromSVG('stroke',strokeVal)

        try:
            strokewidth = element.attributes['stroke-width'].value
        except:
            pass
        else:
            brush.setAttributeFromSVG('stroke-width',strokewidth)

        try:
            strokeMiterVal = element.attributes['stroke-miterlimit'].value
        except:
            pass
        else:
            brush.setAttributeFromSVG('stroke-miterlimit',strokeMiterVal)

        return brush

    # Used where there may be multiple elements of same name ie repeating components
    def _generateUniqueKey(self):

        if self.uniqueKey == None:
            self.uniqueKey = 0
        else:
            self.uniqueKey+=1

        return str(self.uniqueKey)

    def _checkName(self,name):
        name = re.sub(r"\s+", "", name, flags=re.UNICODE)

        name = re.sub(r"#", "hash", name, flags=re.UNICODE)
        name = re.sub(r"<", "leftEqualErrorChar", name, flags=re.UNICODE)
        name = re.sub(r">", "rightEqualErrorChar", name, flags=re.UNICODE)
        name = re.sub(r"\.", "", name, flags=re.UNICODE)

        if re.search('[a-zA-Z]', name) is None:
            return "unknown"+self._generateUniqueKey()

        return name

    def _checkOpacity(self,element):

        opacityFound = False
        opacity = None

        try:
            opacity = float(element.attributes["opacity"].value)
        except:
            pass
        else:
            opacityFound = True

        try:
            opacity = float(element.attributes["fill-opacity"].value)
        except:
            pass
        else:
            opacityFound = True

        if opacityFound:
            self.currentOpacity.append(opacity)
            return True
        else:
            return False

