from collections import deque
import os 
import shutil
import sys
from file_node import FileNode


def checkIfObsidianExists():

    #checks if there is an existing
    if os.path.isdir("./ObsidianFellow"):
        print("There is an existing documentation file,")
        print("Would you like to merge and keep all existing documentation? [y] [n]")
        resp = ""

        while resp.lower() != "y" or resp.lower() != "n":
            resp = input()
            if resp == "n":
                print("Are you sure? You could lose documentation.")
                print("Press to confirm [y] [n]")
                respConf = input()
                if respConf == "y":
                    return False    
                else:
                    print("exit process")
                    sys.exit()
            elif resp == "y":
                print("Creating and merging")
                return True
            else:
                print("invalid command, please enter [y] or [n]")


def createCopy(pathFile, pathToDocumentation=""):
    
    merging = True
    pathNames, dirNames = getFileNames(pathFile)
    if pathToDocumentation != "":
        if os.path.isdir(pathToDocumentation):
            mergePath = pathToDocumentation
            merging = True
        else:
            print("path given to documentation was not found, search in local dir launched")
    else:
        merging = checkIfObsidianExists()
   
    if not os.path.isdir("./ObsidianCopy"):
        os.mkdir("./ObsidianCopy")

    for pathName in pathNames:
        indiv = pathName.split("/")
        tmpPath = ['.', "ObsidianCopy"]
        print(indiv)
        
        for name in indiv[1:-1]:
            pathToSearch = "/".join(tmpPath) + "/" + name
            if not os.path.isdir(pathToSearch):
                tmpPath.append(name)
                os.mkdir("/".join(tmpPath))
            else:
                tmpPath.append(name)
        
        #append file name to end of path
        tmpPath.append(indiv[-1])
        fileName = "/".join(tmpPath) + ".md"
        
        #adapts the path of the given file
        if merging:
            existingPath = tmpPath
            existingPath[1] = "ObsidianFellow"
            if os.path.isfile("/".join(existingPath)):
                shutil.copy(existingPath, fileName)
            else:
                with open(fileName, "w") as file:   
                    pckList = searchFileForImports(pathName)
                    if len(pckList) > 0:
                        writeImportsObsidianMd(pckList, file)
        else:
            with open(fileName, "w") as file:   
                 pckList = searchFileForImports(pathName)
                 if len(pckList) > 0:
                    writeImportsObsidianMd(pckList, file)

    #this part of the code just handles the creation of empty directorie
    for dirPathName in dirNames:
        print(dirPathName)
        #adds the ObsidianCopy to path
        decomposed = dirPathName.split("/")
        decomposed.insert(1, "ObsidianCopy")

        #need to check if the directory exists by traversing the decimposed and building a tmp
        #path to check if the directory exists, if it doesnt it needs to create it
        #this is to prevent eroores on creation of mutlitple nested empty folders
        print(decomposed)
        for i in range(2, len(decomposed)):
            dirPathStr = "/".join(decomposed[:i])
            if not os.path.isdir(dirPathStr):
                os.mkdir(dirPathStr)





#instead of using walk ill just implement my own bfs to create the tree
def navigate_path(initial_path):
    
    # TODO change root to name of folder
    root = FileNode(None, type = "folder", name="root")
    bfs_dir_queue = deque()
    
    all_files = os.listdir(initial_path)
    files = [file for file in all_files if os.path.isfile(file)]
    dirs =  [dir for dir in all_files if os.path.isdir(dir)]

    # first add all the files, then create new dir nodes 
    for file in files:
        root.add_child(FileNode(root, name=file))
    for dir in dirs:
        dir = FileNode(root, name=dir, type="dir")
        bfs_dir_queue.append(dir)
        root.add_child(dir)

    while bfs_dir_queue:
        dir = bfs_dir_queue.popleft()
        all_files = os.listdir(dir.path)
        files = [file for file in all_files if os.path.isfile(file)]
        dirs =  [dir for dir in all_files if os.path.isdir(dir)]

        # first add all the files, then create new dir nodes 
        for file in files:
            root.add_child(FileNode(root, name=file))
        for dir in dirs:
            dir = FileNode(root, name=dir, type="dir")
            bfs_dir_queue.append(dir)
            root.add_child(dir)


    return root



def getFileNames(pathToFile):

    ogFilePath = []
    ogDirPath = []
    for root, dirNames, files in os.walk(pathToFile, topdown=False):
        for name in files:
            ogFilePath.append(os.path.join(root, name))
            print(ogFilePath[-1])

        for dirName in dirNames:
            ogDirPath.append(os.path.join(root, dirName))
            print(ogDirPath[-1])

    return ogFilePath, ogDirPath

def searchFileForImports(ogFilePath):

    if ogFilePath[-4:] == "dart":
        listOfPackages = []
        with open(ogFilePath, "r") as fileData:
            lines = fileData.readlines()
            for line in lines:
                line = line[:-3]
                if line[0:6] == "import":
                    listOfPackages.append(line.split("/")[-1])
                else:
                    print(listOfPackages)
                    return listOfPackages
        return listOfPackages
    else:
        return []






def writeImportsObsidianMd(packagesUsed, file):

    for packageId in range(len(packagesUsed)):
       packagesUsed[packageId] = "[[" + packagesUsed[packageId] + "]]"

    file.writelines(packagesUsed)


def main():
    nArgs = len(sys.argv)
    
    if nArgs <= 1:
        print("too few arguments\nlaunchGenerator arg1 arg2?\narg1=location of file to copy\narg2(optinal)=location of already made documetation to copy existing info")
    
    elif nArgs == 2:
    
        createCopy(sys.argv[1])
    
    elif nArgs == 3:
        createCopy(sys.argv[1], sys.argv[2])




if __name__ == "__main__":
    main()
