import tkinter.filedialog as fd
from SVGtoCPPinterface import SVGtoCPPinterface
from helperClasses.FileHandlingFunctions import *
import json

# Saving location of script directory
scriptDirectory = os.getcwd()
juceComponentDirectory = os.path.join(scriptDirectory,"JuceComponentFiles")
# Asking for .json
fileToOpen = fd.askopenfilename(title ="Select .json file")
# Sets the On/Off[1/0] for each file when generating a new sjp
defaultFileSetting = 0 # Set to 1 to enable all files for processing

# If file not given, script runs for new file
if fileToOpen == "":
    # create link file, prompt for first link
    with fd.asksaveasfile(title="Save new .json file",defaultextension=".json",filetypes=((".json file", "*.json"),("All Files", "*.*"))) as f:

        # Asking for svg and source directories
        svgDirectory = fd.askdirectory(title = "Select SVG directory")
        sourceDirectory = fd.askdirectory(title = "Select C++ Source directory")


        jsonArray = []
        jsonArray.append([svgDirectory,sourceDirectory])

        os.chdir(svgDirectory)
        svgFiles = os.listdir()
        # Compile into format and write to sjp - see help for format
        for svgFile in svgFiles:
            componentType = 'component'
            componentName = svgFile.split(".")[0].split("/")[-1]
            if "_" in componentName:
                componentParts = componentName.split('_')
                componentName = componentParts[0]
                componentType = componentParts[1]

            # If cpp/h file of the same name already exists, then a new file from /juceComponentFiles will not be written and the given file will be used
            if not checkIfFileExists(componentName,sourceDirectory):
                sourceFiles = copyFiles(componentName,componentType,sourceDirectory,juceComponentDirectory)
                for file in sourceFiles:
                    renameComponents(componentName,file)
            else:
                sourceFiles = [os.path.join(sourceDirectory,componentName+'.h'),os.path.join(sourceDirectory,componentName+'.cpp')]

            svg = os.path.join(svgDirectory,svgFile)
            hfile = sourceFiles[0]
            cppfile = sourceFiles[1]
            fileProcessingEnabled = {"fileProcessingEnabled": defaultFileSetting}

            headerWriteDict = {}
            headerWriteDict.update({'include':1})
            headerWriteDict.update({'privatemembers':1})

            cppWriteDict = {}
            cppWriteDict.update({'initialisation':1})
            cppWriteDict.update({'constructor':1})
            cppWriteDict.update({'paint':1})
            cppWriteDict.update({'resized':1})
            cppWriteDict.update({'function':1})

            jsonArray.append([componentName,componentType,svg,hfile,cppfile,fileProcessingEnabled,headerWriteDict,cppWriteDict])

        json.dump(jsonArray,f,indent=2)

else:
    with open(fileToOpen,'r') as f:
        data = json.load(f)

        for lineNumber, line in enumerate(data):
            if lineNumber == 0:
                continue

            componentName, componentType, svgFile, hfile, cppfile, fileProcessingEnabled, headerWriteDict, cppWriteDict = line
            if fileProcessingEnabled["fileProcessingEnabled"] == 0:
                continue

            sectionWriteToggle = [headerWriteDict,cppWriteDict]
            SVGtoCPPinterface(componentName,componentType,svgFile,hfile,cppfile,sectionWriteToggle)










