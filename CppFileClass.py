import helperClasses.Section as helper

class CppFileClass:
    def __init__(self,componentName,hFile,cppFile, sectionWriteToggle):

        self.hFile = hFile
        self.cppFile = cppFile

        # copying file contents
        componentHfile = open(self.hFile)
        componentCPPfile = open(self.cppFile)
        self.hContents = componentHfile.readlines()
        self.cppContents = componentCPPfile.readlines()
        componentHfile.close()
        componentCPPfile.close()

        self.componentName = componentName

        self.headerToggles = sectionWriteToggle[0]
        self.cppToggles = sectionWriteToggle[1]

        # HeaderFiles

        self.headerLocations = {}

        includeStart, includeEnd = self._findFunctionLine("INCLUDE",file="h")
        if self.headerToggles['include']==1:
            self._deleteFunctionContents(includeStart,includeEnd,file="h")
            includeStart, includeEnd = self._findFunctionLine("INCLUDE",file="h")

        privateStart, privateEnd = self._findFunctionLine("PRIVATEMEMBERS",file="h")
        if self.headerToggles['privatemembers']==1:
            self._deleteFunctionContents(privateStart,privateEnd,file="h")
            privateStart, privateEnd = self._findFunctionLine("PRIVATEMEMBERS",file="h")

        # Saving names of sections with their respective code locations within hcontents
        self.headerLocations.update({'include':helper.Section('include',self.hContents[includeStart:includeEnd])})
        self.headerLocations.update({'privatemembers':helper.Section('privatemembers',self.hContents[privateStart:privateEnd])})

        # CPPlines

        self.cppLocations = {}

        constructorStart, constructorEnd = self._findFunctionLine('CONSTRUCTOR')
        if self.cppToggles['constructor']==1:
            self._deleteFunctionContents(constructorStart,constructorEnd)
            constructorStart, constructorEnd = self._findFunctionLine('CONSTRUCTOR')

        initialiserStart, initialiserEnd = self._findFunctionLine('INITIALISATION')
        if self.cppToggles['initialisation']==1:
            self._deleteFunctionContents(initialiserStart,initialiserEnd)
            initialiserStart, initialiserEnd = self._findFunctionLine('INITIALISATION')

        paintStart, paintEnd = self._findFunctionLine("PAINT")
        if self.cppToggles['paint']==1:
            self._deleteFunctionContents(paintStart,paintEnd)
            paintStart, paintEnd = self._findFunctionLine("PAINT")

        resizeStart, resizeEnd = self._findFunctionLine("RESIZED")
        if self.cppToggles['resized']==1:
            self._deleteFunctionContents(resizeStart,resizeEnd)
            resizeStart, resizeEnd = self._findFunctionLine("RESIZED")

        functionStart, functionEnd = self._findFunctionLine("FUNCTION")
        if self.cppToggles['function']==1:
            self._deleteFunctionContents(functionStart,functionEnd)
            functionStart, functionEnd = self._findFunctionLine("FUNCTION")

        # Saving names of sections with their respective code locations within cppcontents
        self.cppLocations.update({'constructor':helper.Section('constructor',self.cppContents[constructorStart:constructorEnd])})
        self.cppLocations.update({'initialisation':helper.Section('initialisation',self.cppContents[initialiserStart:initialiserEnd])})
        self.cppLocations.update({'paint':helper.Section('paint',self.cppContents[paintStart:paintEnd])})
        self.cppLocations.update({'resized':helper.Section('resized',self.cppContents[resizeStart:resizeEnd])})
        self.cppLocations.update({'function':helper.Section('function',self.cppContents[functionStart:functionEnd])})

    # called by svgtocppinterface to write final files
    def writeFiles(self):
        self.__writeCodeFromSections()
        newHFile = open(self.hFile,"w+")
        newCppFile = open(self.cppFile,"w+")
        newHFile.writelines(self.hContents)
        newCppFile.writelines(self.cppContents)
        newHFile.close()
        newCppFile.close()

    # Writes sections code
    def __writeCodeFromSections(self):

        for index, [name, section] in enumerate(self.headerLocations.items()):
            if self.headerToggles[name]==0:
                continue

            code = section.getCode()
            functionStart,functionEnd = self._findFunctionLine(name,"h")
            for line in code:
                self.hContents.insert(functionStart,line)
                functionStart+=1

        for index, [name, section] in enumerate(self.cppLocations.items()):
            if self.cppToggles[name]==0:
                continue

            code = section.getCode()
            functionStart,functionEnd = self._findFunctionLine(name,"cpp")
            for line in code:
                self.cppContents.insert(functionStart,line)
                functionStart+=1

    # Adding component states into each section as needed
    def addComponentStates(self, states):
        for state in states:
            stateName, declaration, functionStart, paintedObjects, functionEnd = state.getCodeObjects()
            if stateName == 'paint':
                # If state is the standard paint section, add objects to paint location
                self.addPaintedObjects(paintedObjects)
            else:
                # State is a specific function, add code to declare function in private members
                self.headerLocations['privatemembers'].addCode(declaration)
                # Add child section within 'functions' with given state name
                self.cppLocations['function'].addChild(stateName)
                # Add function start code to this section
                self.cppLocations['function'].addChildCode(stateName,functionStart)
                # Add each paintedobject given to the inside of the function
                for paintedObject in paintedObjects:
                    self.cppLocations['function'].addChildCode(stateName,paintedObject.getPaintCode())
                # Add function end code to the section
                self.cppLocations['function'].addChildCode(stateName,functionEnd)

    # Adding painted objects to the standard paint section
    def addPaintedObjects(self,objects):
        if not isinstance(objects,list):
            self.__addPaintedObject(objects)
            return

        for object in objects:
            self.__addPaintedObject(object)

    def __addPaintedObject(self,object):
        code = object.getPaintCode()
        self.cppLocations['paint'].addCode(code)

    def addChildComponents(self,objects):
        if not isinstance(objects,list):
            self.__addChildComponent(objects)
            return

        for object in objects:
            self.__addChildComponent(object)

    def __addChildComponent(self,object):
        includes, declaration, constructor, resized, initialisation = object.getChildCodeComponents()
        if includes is not None:
            self.headerLocations['include'].addCode(includes)
        if declaration is not None:
            self.headerLocations['privatemembers'].addCode(declaration)
        if constructor is not None:
            self.cppLocations['constructor'].addCode(constructor)
        if resized is not None:
            self.cppLocations['resized'].addCode(resized)
        if initialisation is not None:
            self.cppLocations['initialisation'].addCode(initialisation)

    def _findFunctionLine(self,functionName,file="cpp"):

        if file == "cpp":
            copiedFile = self.cppContents
        else:
            copiedFile = self.hContents

        start = None
        end = None
        for lineNumber, line in enumerate(copiedFile):
            if ">>>>"+functionName.upper()+">>>>" in line:
                start = lineNumber
            if start is not None and end is None:
                if "<<<<"+functionName.upper()+"<<<<" in line:
                    end = lineNumber

        return start+1,end

    def _deleteFunctionContents(self,openBracket,closeBracket,file="cpp"):

        for i in range(openBracket,closeBracket):
            if file == "cpp":
                self.cppContents.pop(openBracket)
            else:
                self.hContents.pop(openBracket)




