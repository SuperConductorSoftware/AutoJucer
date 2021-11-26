import numpy as np
from constantDefs import constant

# Child component class, will write an svg rectangle as a child component space, with initialisation and header file
class ChildComponent:
    def __init__(self,componentName,x,y,boundsX,boundsY):
        self.componentName = componentName
        self.x = x
        self.y = y
        self.boundsX = boundsX
        self.boundsY = boundsY

        self.__checkIntegers()

    def getChildCodeComponents(self):

        includes = self.__generateIncludeCode()
        declaration = self.__generateDeclarationCode()
        constructor = self.__generateConstructorCode()
        resized = self.__generateResizedCode()
        initialisation = self.__generateInitialiserCode()

        return includes, declaration, constructor, resized, initialisation

    def __checkIntegers(self):

        variables = [self.x,self.y,self.boundsX,self.boundsY]
        for variable in variables:
            if float(variable)-np.floor(float(variable))!=0:
                print("child location truncated to integer pixel locations!!")

    def __generateIncludeCode(self):
        code = ["#include \"" + self.componentName +".h\"" + constant.NEWLINE]
        return code

    def __generateDeclarationCode(self):
        code = ["\t" + self.componentName +" " + self.componentName +"1;" + constant.NEWLINE]
        return code

    def __generateConstructorCode(self):
        code = ["\t" +"addAndMakeVisible(" + self.componentName +"1);" + constant.NEWLINE]
        return code

    def __generateResizedCode(self):
        code = ["\t" + self.componentName +"1.setBounds(" + self.x +"," + self.y +"," + self.boundsX +"," + self.boundsY +");" + constant.NEWLINE]
        return code

    def __generateInitialiserCode(self):
        code = [", " + self.componentName +"1(parameters)" + constant.NEWLINE]
        return code

# State class for component graphics - by default this will write all graphical elements inside the component .paint class
# For any component however a ::state #[statename] in the layer of the svg will produce an alternative graphic function with given statename taht can be linked within visual studio
class ComponentGraphicState:
    def __init__(self, componentName, stateName='paint'):
        self.componentName = componentName
        self.stateName = stateName
        self.paintedObjects = []

    def addPaintedObject(self,object):
        self.paintedObjects.append(object)

    def getStateName(self):
        return self.stateName

    def getCodeObjects(self):
        return self.stateName, self.__generateDeclarationCode(), self.__generateStartFunctionCode(), self.paintedObjects, self.__generateEndFunctionCode()

    def __generateDeclarationCode(self):
        code = ["\t" +"void " + self.stateName +"(Graphics &);" + constant.NEWLINE]
        return code

    def __generateStartFunctionCode(self):
        code = ["void " + self.componentName +"::" + self.stateName +"(Graphics &g){" + constant.NEWLINE]
        return code
    def __generateEndFunctionCode(self):
        code = ["}" + constant.NEWLINE]
        return code

# Lazy label class
class Label:
    def __init__(self,labelText,brush,x,y,boundsX,boundsY):
        self.labelText = labelText
        self.x = x
        self.y = y
        self.boundsX = boundsX
        self.boundsY = boundsY
        self.brush = brush

    def getCode(self):
        declaration = self.__generateDeclarationCode()
        constructor = self.__generateConstructorCode()
        resized = self.__generateResizedCode()

        return declaration, constructor, resized

    def __generateDeclarationCode(self):
        code = ["\tLabel " + self.labelText +"Label1;" + constant.NEWLINE]
        return code

    def __generateConstructorCode(self):
        code = []
        code.append("\t" +"addAndMakeVisible(" + self.labelText +"Label1);" + constant.NEWLINE)
        code.append("\t" + self.labelText +"Label1.setText(String(\"" + self.labelText +"\"),dontSendNotification);" + constant.NEWLINE)
        code.append("\t" + self.labelText +"Label1.setFont(Font(16, 0));" + constant.NEWLINE)
        code.append("\t" + self.labelText +"Label1.setJustificationType(Justification::centred);" + constant.NEWLINE)
        code.append("\t" + self.labelText +"Label1.setColour(Label::textColourId,Colour::fromRGB(" + str(self.brush.getAttribute('fill')[0]) +"," + str(self.brush.getAttribute('fill')[1]) +"," + str(self.brush.getAttribute('fill')[2]) +"));" + constant.NEWLINE)

        return code

    def __generateResizedCode(self):
        #code = ["\t"+self.labelText+"Label1.setBounds("+self.x+","+self.y+","+self.boundsX+","+self.boundsY+");"+"\r\n"]
        code = []
        return code

# Painted Object parent class from which all painted objects derive, and are held within each component state
class PaintedObject:

    def getPaintCode(self):

        self.scaleSettings
        self._generateCode()

        return self.paintCode

    def _generateCode(self):
        pass

    def setScalesWithBounds(self, scaleSettings):
        self.scaleSettings = scaleSettings

    def setSVGBounds(self,width,height):
        self.svgWidth = width
        self.svgHeight = height

    def __scaleLocation(self,location,axis='x'):

        if axis == 'x':
            svgDimension = self.svgWidth
            juceDimension = "getLocalBounds().getWidth()"
        else:
            svgDimension = self.svgHeight
            juceDimension = "getLocalBounds().getHeight()"


        if self.scaleSettings['scalesWithBounds']:
            location = location/svgDimension

            code = juceDimension+"*"+str(location)

            return code

        elif self.scaleSettings['scalesLinearly']:
            if float(location) < (svgDimension/2):
                #code = str(location)+"+("+str(svgDimension)+"-"+juceDimension+")/2"
                code = str(location)
            else:
                distFromFarWall = svgDimension-float(location)
                code = str(juceDimension)+"-"+str(distFromFarWall)
            return code

        elif self.scaleSettings['centre']:
            code = str(location-svgDimension/2)+"+("+juceDimension+"/2)"
            return code
        else:
            return str(location)

#  Scale locations in combinatin with scale settings allow dynamic resizing of elements
    def _scaleXLocation(self,x):

        return self.__scaleLocation(x,'x')

    def _scaleYLocation(self,y):

        return self.__scaleLocation(y,'y')

# Path parent class, now largely redundant but does allow for expansion later with more path specific inheritable functions
class PathSegment(PaintedObject):

    def getCode(self,name):
        return self._generateCode(name)

    def _generateCode(self,name):
        pass



class PathMove(PathSegment):
    def __init__(self,x,y):
        self.x = x
        self.y = y

    def _generateCode(self,name):

        code = "\t" + name +".startNewSubPath(" + self._scaleXLocation(self.x) +"," + self._scaleYLocation(self.y) +");" + constant.NEWLINE

        return code

class PathLine(PathSegment):
    def __init__(self,x,y):
        self.x = x
        self.y = y

    def _generateCode(self,name):

        code = "\t" + name +".lineTo(" + self._scaleXLocation(self.x) +"," + self._scaleYLocation(self.y) +");" + constant.NEWLINE

        return code

class PathCubic(PathSegment):
    def __init__(self,cx,cy,c2x,c2y,ex,ey):
        self.control1X = cx
        self.control1Y = cy

        self.control2X = c2x
        self.control2Y = c2y

        self.endX = ex
        self.endY = ey

    def _generateCode(self,name):

        #code = "\t"+name+".cubicTo("+str(self.control1X)+","+str(self.control1Y)+","+str(self.control2X)+","+str(self.control2Y)+","+str(self.endX)+","+str(self.endY)+");"
        code = "\t" + name +".cubicTo(" + self._scaleXLocation(self.control1X) +"," + \
               self._scaleYLocation(self.control1Y) +"," + \
               self._scaleXLocation(self.control2X) +"," + \
               self._scaleYLocation(self.control2Y) +"," + \
               self._scaleXLocation(self.endX) +"," + \
               self._scaleYLocation(self.endY) +");" + constant.NEWLINE

        return code

class PathArc(PathSegment):
    def __init__(self,cx,cy,rx,ry,rotation,d,t):
        self.centreX = cx
        self.centreY = cy

        self.radiusX = rx
        self.radiusY = ry

        self.rotation = rotation

        self.delta = d
        self.theta = t

    def _generateCode(self,name):
        code = "\t" + name +".addCentredArc(" + \
               self._scaleXLocation(self.centreX) +"," + \
               self._scaleYLocation(self.centreY) +"," + \
               self.radiusX +"," + \
               self.radiusY +"," + \
               str(self.rotation) +"," + \
               str(self.delta) +"," + \
               str(self.theta) +");" + constant.NEWLINE

        return code

class PathClose(PathSegment):

    def _generateCode(self,name):
        code = "\t" + name +".closeSubPath();" + constant.NEWLINE

        return code

class Path(PaintedObject):
    def __init__(self,name,brush):

        self.name = name
        self.brush = brush
        self.paintCode = []

        self.instructions = []

    def addInstruction(self,ins):
        self.instructions.append(ins)

    def _generateCode(self):

        # creating path and vertice objects
        self.paintCode.append("\tPath " + self.name +";" + constant.NEWLINE)
        # creating subpath and lineTo calls

        for instruction in self.instructions:
            self.paintCode.append(instruction.getCode(self.name))

        self.paintCode.append(constant.NEWLINE)

        if self.brush.checkAttribute('fill'):
            self.paintCode.append("\tg.setColour(Colour::fromRGB(" + str(self.brush.getAttribute('fill')[0]) +"," + str(self.brush.getAttribute('fill')[1]) +"," + str(self.brush.getAttribute('fill')[2]) +"));" + constant.NEWLINE)
            self.paintCode.append("\tg.setOpacity(" + str(self.brush.getAttribute('opacity')) +");" + constant.NEWLINE)
            self.paintCode.append("\tg.fillPath(" + self.name +");" + constant.NEWLINE)
        if self.brush.checkAttribute('stroke'):
            self.paintCode.append("\tg.setColour(Colour::fromRGB(" + str(self.brush.getAttribute('stroke')[0]) +"," + str(self.brush.getAttribute('stroke')[1]) +"," + str(self.brush.getAttribute('stroke')[2]) +"));" + constant.NEWLINE)
            self.paintCode.append("\tg.setOpacity(" + str(self.brush.getAttribute('opacity')) +");" + constant.NEWLINE)
            self.paintCode.append("\tg.strokePath(" + self.name +",juce::PathStrokeType(" + str(self.brush.getAttribute('strokeWidth')) +"));" + constant.NEWLINE)
        self.paintCode.append(constant.NEWLINE)

class Rect(PaintedObject):
    def __init__(self,name,brush):

        self.name = name
        self.brush = brush
        self.paintCode = []

        self.startX = None
        self.startY = None
        self.width = None
        self.height = None
        self.rx = None
        self.ry = None

    def addData(self,x,y,width,height,rx,ry):
        self.startX = x
        self.startY = y
        self.width = width
        self.height = height
        self.rx = rx
        self.ry = ry

    def _generateCode(self):

        # creating path and vertice objects
        self.paintCode.append("\tRectangle<float> " + self.name +"(" +
                              self._scaleXLocation(self.startX) +"," +
                              self._scaleYLocation(self.startY) +"," +
                              self._scaleXLocation(self.width) +"," +
                              self._scaleYLocation(self.height) +");" + constant.NEWLINE)

        if self.brush.getAttribute('fillBool') == True:
            self.paintCode.append("\tg.setColour(Colour::fromRGB(" + str(self.brush.getAttribute('fill')[0]) +"," + str(self.brush.getAttribute('fill')[1]) +"," + str(self.brush.getAttribute('fill')[2]) +"));" + constant.NEWLINE)

            self.paintCode.append("\tg.setOpacity(" + str(self.brush.getAttribute('opacity')) +");" + constant.NEWLINE)

            if self.rx is None or self.ry is None:
                self.paintCode.append("\tg.fillRect(" + self.name +");" + constant.NEWLINE)
            else:
                self.paintCode.append("\tg.fillRoundedRectangle(" + self.name +"," + self.rx +");" + constant.NEWLINE)

        if self.brush.getAttribute('strokeBool') == True:
            self.paintCode.append("\tg.setColour(Colour::fromRGB(" + str(self.brush.getAttribute('stroke')[0]) +"," + str(self.brush.getAttribute('stroke')[1]) +"," + str(self.brush.getAttribute('stroke')[2]) +"));" + constant.NEWLINE)

            self.paintCode.append("\tg.setOpacity(" + str(self.brush.getAttribute('opacity')) +");" + constant.NEWLINE)

            if self.rx is None or self.ry is None:
                self.paintCode.append("\tg.drawRect(" + self.name +"," + str(self.brush.getAttribute('strokeWidth')) +");" + constant.NEWLINE)
            else:
                self.paintCode.append("\tg.drawRoundedRectangle(" + self.name +"," + self.rx +"," + str(self.brush.getAttribute('strokeWidth')) +");" + constant.NEWLINE)

        self.paintCode.append(constant.NEWLINE)

class Ellipse(PaintedObject):
    def __init__(self,name,brush):

        self.name = name
        self.brush = brush
        self.paintCode = []

        self.instructions = None

        self.topLeftX = None
        self.topLeftY = None
        self.rectWidth = None
        self.rectHeight = None

    def addData(self,cx,cy,rx,ry):
        self.topLeftX = str(float(cx)-float(rx))
        self.topLeftY = str(float(cy)-float(ry))
        self.rectWidth = str(float(rx)*2)
        self.rectHeight = str(float(ry)*2)

    def _generateCode(self):

        # creating path and vertice objects
        self.paintCode.append("\tRectangle<float> " + self.name +"(" +
                              self._scaleXLocation(self.topLeftX) +"," +
                              self._scaleYLocation(self.topLeftY) +"," +
                              self._scaleXLocation(self.rectWidth) +"," +
                              self._scaleYLocation(self.rectHeight) +");" + constant.NEWLINE)



        if self.brush.checkAttribute('fill'):
            self.paintCode.append("\tg.setColour(Colour::fromRGB(" + str(self.brush.getAttribute('fill')[0]) +"," + str(self.brush.getAttribute('fill')[1]) +"," + str(self.brush.getAttribute('fill')[2]) +"));" + constant.NEWLINE)
            self.paintCode.append("\tg.setOpacity(" + str(self.brush.getAttribute('opacity')) +");" + constant.NEWLINE)
            self.paintCode.append("\tg.fillEllipse(" + self.name +");" + constant.NEWLINE)

        if self.brush.checkAttribute('stroke'):
            self.paintCode.append("\tg.setColour(Colour::fromRGB(" + str(self.brush.getAttribute('lineColour')[0]) +"," + str(self.brush.getAttribute('lineColour')[1]) +"," + str(self.brush.getAttribute('lineColour')[2]) +"));" + constant.NEWLINE)
            self.paintCode.append("\tjuce::PathStrokeType " + self.name +"Stroke(" + str(self.brush.getAttribute('strokeWidth')) +");" + constant.NEWLINE)
            self.paintCode.append("\tg.setOpacity(" + str(self.brush.getAttribute('opacity')) +");" + constant.NEWLINE)
            self.paintCode.append("\tg.drawEllipse(" + self.name +"," + str(self.brush.getAttribute('strokeWidth')) +");" + constant.NEWLINE)

        self.paintCode.append(constant.NEWLINE)