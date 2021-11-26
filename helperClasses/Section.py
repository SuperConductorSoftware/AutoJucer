
# This class is used as a self contained class for management of each specific section of a h or cpp file, which can then be used to compile a whole file when writing
class Section:
    def __init__(self, name, codeSection):
        self.name = name
        self.code = codeSection
        self.children = {}

    def addCode(self,code):
        for line in code:
            self.code.append(line)

    def getCode(self):

        for name,child in self.children.items():
            childCode = child.getCode()
            for line in childCode:
                self.code.append(line)
        return self.code

    def getName(self):
        return self.getName()

    def addChild(self,name):
        self.children.update({name:Section(name,[])})

    def addChildCode(self,name,code):
        self.children[name].addCode(code)





