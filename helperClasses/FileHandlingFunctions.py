import os
import shutil

def checkIfFileExists(componentName,sourceDirectory):
    currentDir = os.getcwd()
    os.chdir(sourceDirectory)
    files = os.listdir()
    os.chdir(currentDir)
    if componentName+'.h' in files:
        return True
    else:
        return False

def copyFiles(componentName,componentType,sourceDirectory, juceComponentDirectory):

    newHFile = os.path.join(sourceDirectory,componentName+".h")
    newCppFile = os.path.join(sourceDirectory,componentName+".cpp")

    shutil.copyfile(os.path.join(juceComponentDirectory,componentType.lower()+".h"), newHFile)
    shutil.copyfile(os.path.join(juceComponentDirectory,componentType.lower()+".cpp"), newCppFile)
    return newHFile, newCppFile

def renameComponents(componentName,file):

    with open(file) as f:
        newText=f.read().replace('not_a_real_name', componentName)

    with open(file, "w") as f:
        f.write(newText)