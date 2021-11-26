from constantDefs.SVGDefs import colourDict,nameTranslation, defaults
from PIL import ImageColor
from blend_modes import blending_functions
import re
import numpy as np

class BrushClass:
    def __init__(self):

        self.attributeList = {}
        self.attributeList.update({'fillBool':False})
        self.attributeList.update({'strokeBool':False})
        self.attributeList.update({'opacity':1.0})
        self.blendMode = 'normal'
        self.blendColour = '#000000'

    def checkAttribute(self,name):
        try:
            self.attributeList[name]
            return True
        except:
            return False

    def setAttributeFromSVG(self,name,value):

        name = nameTranslation[name]
        if name == 'stroke':
            if value in colourDict:
                value = colourDict[value]
            value = ImageColor.getcolor(value, "RGB")

            value = self.__applyBlendingModeToColour(value)

            self.attributeList.update({'strokeBool':True})


        if name == 'fill' and value != 'none':
            if value in colourDict:
                value = colourDict[value]
            value = ImageColor.getcolor(value, "RGB")
            self.attributeList.update({'fillBool':True})
            value = self.__applyBlendingModeToColour(value)

        elif name == 'fill' and value =='none':
            value = ImageColor.getcolor(colourDict['black'],"RGB")

            value = self.__applyBlendingModeToColour(value)


        if name == 'fontSize':
            value = value[:-2]

        if name == 'fontFamily':
            value = re.split(',',value)
            self.attributeList.update({'fontFamily':value[0]})
            self.attributeList.update({'fontStyle':value[1]})
        else:
            self.attributeList.update({name:value})

        if name == 'opacity':
            self.attributeList.update({"opacity":value})



    def getAttribute(self,name):

        if name in self.attributeList:
            return self.attributeList[name]
        else:
            return defaults[name]

    def setBlendModeAndColour(self,name,colour):
        self.blendMode = name
        self.blendColour = colour

    def __applyBlendingModeToColour(self,colour):

        if '#' not in self.blendColour:
            self.blendColour = '#'+self.blendColour
        blendColour = ImageColor.getcolor(self.blendColour, "RGB")


        if self.blendMode != 'normal':
            colour = np.array(colour,dtype=float)
            blendColour = np.array(blendColour,dtype=float)

            colour = np.reshape(colour,[1,1,3])
            colour = np.append(colour,[[[1]]],axis=2)

            blendColour = np.reshape(blendColour,[1,1,3])
            blendColour = np.append(blendColour,[[[1]]],axis=2)

            newColour = blending_functions.multiply(blendColour,colour,1)

            newColour = newColour[:,:,:-1]
            newColour = np.reshape(newColour,[3])
            newColour = np.array(newColour,dtype=int)


            colour = newColour

        return colour


