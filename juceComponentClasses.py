import numpy as np
from constantDefs import constant

# Child component class, will write an svg rectangle as a child component space, with initialisation and header file
class ChildComponentAbstract:
    def getChildCodeComponents(self):

        includes = self._generateIncludeCode()
        declaration = self._generateDeclarationCode()
        constructor = self._generateConstructorCode()
        resized = self._generateResizedCode()
        initialisation = self._generateInitialiserCode()

        return includes, declaration, constructor, resized, initialisation

    def _generateIncludeCode(self):
        pass

    def _generateDeclarationCode(self):
        pass

    def _generateConstructorCode(self):
        pass

    def _generateResizedCode(self):
        pass

    def _generateInitialiserCode(self):
        pass

class ChildComponent(ChildComponentAbstract):
    def __init__(self,componentName,x,y,boundsX,boundsY):
        self.componentName = componentName
        self.x = x
        self.y = y
        self.boundsX = boundsX
        self.boundsY = boundsY

        self.__checkIntegers()

    def __checkIntegers(self):

        variables = [self.x,self.y,self.boundsX,self.boundsY]
        for variable in variables:
            if float(variable)-np.floor(float(variable))!=0:
                print("child location truncated to integer pixel locations!!")

    def _generateIncludeCode(self):
        code = ["#include \"" + self.componentName +".h\"" + constant.NEWLINE]
        return code

    def _generateDeclarationCode(self):
        code = ["\t" + self.componentName +" " + self.componentName +"1;" + constant.NEWLINE]
        return code

    def _generateConstructorCode(self):
        code = ["\t" +"addAndMakeVisible(" + self.componentName +"1);" + constant.NEWLINE]
        return code

    def _generateResizedCode(self):
        code = ["\t" + self.componentName +"1.setBounds(" + self.x +"," + self.y +"," + self.boundsX +"," + self.boundsY +");" + constant.NEWLINE]
        return code

    def _generateInitialiserCode(self):
        code = [", " + self.componentName +"1(parameters)" + constant.NEWLINE]
        return code

class Label(ChildComponentAbstract):
    def __init__(self,labelName,brush,x,y,boundsX,boundsY):
        self.labelName = labelName
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

    def _generateDeclarationCode(self):
        code = ["\tLabel " + self.labelName +"1;" + constant.NEWLINE]
        return code

    def _generateConstructorCode(self):
        code = []
        code.append("\t" +"addAndMakeVisible(" + self.labelName +"1);" + constant.NEWLINE)
        code.append("\t" + self.labelName +"1.setText(String(\"" + "PLACEHOLDER" +"\"),dontSendNotification);" + constant.NEWLINE)
        code.append("\t" + self.labelName +"1.setFont(Font(16, 0));" + constant.NEWLINE)
        code.append("\t" + self.labelName +"1.setJustificationType(Justification::centred);" + constant.NEWLINE)
        code.append("\t" + self.labelName +"1.setColour(Label::textColourId,Colour::fromRGB(" + str(self.brush.getAttribute('fill')[0]) +"," + str(self.brush.getAttribute('fill')[1]) +"," + str(self.brush.getAttribute('fill')[2]) +"));" + constant.NEWLINE)
        code.append("\t" + self.labelName +"1.setColour(Label::textWhenEditingColourId,Colour::fromRGB(" + str(self.brush.getAttribute('fill')[0]) +"," + str(self.brush.getAttribute('fill')[1]) +"," + str(self.brush.getAttribute('fill')[2]) +"));" + constant.NEWLINE)
        return code

    def _generateResizedCode(self):
        code = ["\t"+self.labelName+"1.setBounds("+self.x+","+self.y+","+self.boundsX+","+self.boundsY+");"+ constant.NEWLINE]

        return code

class Button(ChildComponentAbstract):
    def __init__(self,componentName,x,y,boundsX,boundsY):
        self.componentName = componentName
        self.x = x
        self.y = y
        self.boundsX = boundsX
        self.boundsY = boundsY

        self.__checkIntegers()

    def __checkIntegers(self):

        variables = [self.x,self.y,self.boundsX,self.boundsY]
        for variable in variables:
            if float(variable)-np.floor(float(variable))!=0:
                print("child location truncated to integer pixel locations!!")

    def _generateIncludeCode(self):
        code = ["#include \"" + self.componentName +".h\"" + constant.NEWLINE]
        return code

    def _generateDeclarationCode(self):
        code = ["\t" + self.componentName +" " + self.componentName +"1;" + constant.NEWLINE]
        return code

    def _generateConstructorCode(self):
        code = ["\t" +"addAndMakeVisible(" + self.componentName +"1);" + constant.NEWLINE]
        return code

    def _generateResizedCode(self):
        code = ["\t" + self.componentName +"1.setBounds(" + self.x +"," + self.y +"," + self.boundsX +"," + self.boundsY +");" + constant.NEWLINE]
        return code

    def _generateInitialiserCode(self):
        code = [", " + self.componentName +"1(parameters)" + constant.NEWLINE]
        return code

class ScrollBar(ChildComponentAbstract):
    def __init__(self,componentName):
        self.componentName = componentName

    def _generateIncludeCode(self):
        code = ["#include \"" + self.componentName +".h\"" + constant.NEWLINE]
        return code

class Bounds(ChildComponentAbstract):
    def __init__(self,componentName,x,y,boundsX,boundsY):
        self.componentName = componentName
        self.x = x
        self.y = y
        self.boundsX = boundsX
        self.boundsY = boundsY

        self.__checkIntegers()

    def __checkIntegers(self):

        variables = [self.x,self.y,self.boundsX,self.boundsY]
        for variable in variables:
            if float(variable)-np.floor(float(variable))!=0:
                print("child location truncated to integer pixel locations!!")

    def _generateDeclarationCode(self):
        code = ["\tRectangle<int> " + self.componentName +";" + constant.NEWLINE]
        return code

    def _generateInitialiserCode(self):
        code = [", " + self.componentName +"(" +self.x +"," +
                self.y +"," +
                self.boundsX +"," +
                self.boundsY +")" + constant.NEWLINE]
        return code

class RotarySlider(ChildComponentAbstract):
    def __init__(self,componentName,x,y,boundsX,boundsY):
        self.componentName = componentName
        self.x = x
        self.y = y
        self.boundsX = boundsX
        self.boundsY = boundsY

    def _generateIncludeCode(self):
        code = ["#include \"" + self.componentName +".h\"" + constant.NEWLINE]
        return code

    def _generateDeclarationCode(self):
        code = ["\t" + "juce::Slider" +" " + self.componentName +"Slider1;" + constant.NEWLINE]
        return code

    def _generateConstructorCode(self):
        code = []
        code.append("\t" +"addAndMakeVisible(" + self.componentName +"Slider1);" + constant.NEWLINE)
        code.append("\t" + "auto sliderLookFeel = new "+self.componentName+"();"+constant.NEWLINE)
        code.append("\t" + self.componentName +"Slider1.setLookAndFeel(sliderLookFeel);"+constant.NEWLINE)
        code.append("\t" + self.componentName +"Slider1.setSliderStyle(juce::Slider::SliderStyle::RotaryHorizontalVerticalDrag);"+constant.NEWLINE)
        code.append("\t" + self.componentName +"Slider1.setTextBoxStyle(juce::Slider::TextEntryBoxPosition::NoTextBox, true, 0, 0);"+constant.NEWLINE)
        return code

    def _generateResizedCode(self):
        code = ["\t" + self.componentName +"Slider1.setBounds(" + self.x +"," + self.y +"," + self.boundsX +"," + self.boundsY +");" + constant.NEWLINE]
        return code