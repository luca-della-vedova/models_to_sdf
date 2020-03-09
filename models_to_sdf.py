import os
import argparse
import shutil
import xml.etree.ElementTree as ET

parser = argparse.ArgumentParser()
parser.add_argument('--input', help='Copy models and textures from exported folder', required = True)
parser.add_argument('--output', help='Paste everything into folder', required = True)
args = parser.parse_args()
folderInput = args.input
folderOutput = args.output

inputFolderName = os.path.basename(folderInput)

meshesDir = os.path.join(folderOutput, inputFolderName, 'meshes')
texturesDir = os.path.join(folderOutput, inputFolderName, 'materials/textures')

def createFolder(directory):
    try:
        if not os.path.exists(directory):
            os.makedirs(directory)
    except OSError:
        print ('Error: Creating directory. ' +  directory)
        
createFolder(meshesDir)
createFolder(texturesDir)

# copies contents of one folder to another yay
def CopyFiles(src_files, destination):
    for file_name in src_files:
        shutil.copy(file_name, destination)

def getFilesWithExtensions(folder, extensions):
    files = []
    for f in os.listdir(folder):
        extension = os.path.splitext(f)[-1]
        if extension in extensions:
            files.append(os.path.join(folder, f))
    return files

def getTextures(folder):
    TEXTURE_EXTENSIONS = ['.png']
    return getFilesWithExtensions(folder, TEXTURE_EXTENSIONS)

def getMeshes(folder):
    MODEL_EXTENSIONS = ['.obj', '.mtl', '.dae']
    return getFilesWithExtensions(folder, MODEL_EXTENSIONS)

def getTemplates(folder):
    TEMPLATE_EXTENSIONS = ['.config', '.sdf']
    return getFilesWithExtensions(folder, TEMPLATE_EXTENSIONS)

CopyFiles(getMeshes(folderInput), meshesDir)
CopyFiles(getTextures(folderInput), texturesDir)

templatesDir = os.path.join(os.getcwd(), 'templates')

sdfDir = os.path.join(folderOutput, inputFolderName)

CopyFiles(getTemplates(templatesDir), sdfDir)

def fixTexturePath(meshes):
    # TODO implement
    # Iterate over meshes files and set the texture paths to the
    # materials/texture subfolder
    for mesh in meshes:
        print(mesh)

fixTexturePath(getMeshes(meshesDir))

## xml editing

def replaceValue(path):
    tree = ET.parse(path)
    root = tree.getroot()

    for elem in root.iter('model'):
        if elem.get('name') is not None:
            elem.set('name', inputFolderName)

    for elem in root.getiterator():
            elem.text = elem.text.replace('change', inputFolderName)

    for elem in root.getiterator():
            elem.text = elem.text.replace('_col', inputFolderName + '_Col')

    tree.write(path, xml_declaration=True, encoding='utf-8')

sdfPath = os.path.join(sdfDir, 'model.sdf')
configPath = os.path.join(sdfDir, 'model.config')
replaceValue(sdfPath)
replaceValue(configPath)
