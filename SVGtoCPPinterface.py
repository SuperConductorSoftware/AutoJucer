from ReadFigmaSVG import ReadFigmaSVG
from CppFileClass import CppFileClass

# Interface between svg interpretation classes and cpp/h writing classes
def SVGtoCPPinterface(componentName,componentType,svgFile,hFile,cppFile,sectionWriteToggle,mode="Figma"):

    # May expand for other ui editors, only written for figma export at the moment
    if mode == "Figma":
        svg = ReadFigmaSVG(svgFile,componentName)

    cppFiles = CppFileClass(componentName,hFile,cppFile,sectionWriteToggle)
    componentStates = svg.getComponentStates()
    childComponents = svg.getChildComponents()
    labels = svg.getLabels()

    # cppFiles interprets componentStates, children and labels from SVGtoJuceObjectClasses through duck typing
    cppFiles.addComponentStates(componentStates)
    cppFiles.addChildComponents(childComponents)
    cppFiles.addLabels(labels)

    cppFiles.writeFiles()