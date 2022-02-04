from ast import Return
from asyncio.constants import ACCEPT_RETRY_DELAY
from asyncore import write
from distutils.command.upload import upload
from distutils.util import byte_compile
import random
from tarfile import ENCODING
from this import d
from PIL import Image, ImageDraw
import os
import requests
import csv
import time
import pandas as pd
from base64 import b64encode
from json import dumps
from json import load
from json import loads
pd.set_option('display.max_columns', 60)
pd.set_option('display.max_rows', None)
pd.set_option("max_colwidth", None)
pd.set_option("expand_frame_repr", False)

headers = ["fileName", "ID", "Cuerpo", "Arma", "Accesorio", "Folder"]

def makeCSV(headersNames):
    with open(r'LambyLorosList.csv', 'a') as f:
        write = csv.writer(f)
        #write.writerow(headersNames)

makeCSV(headers)

def randCuerpo():
    roll = random.randint(0,999)
    if roll <100:
        return "CuerpoAmarillo"
    
    if roll <300:
        return "CuerpoAzul"

    if roll <450:
        return "CuerpoKarateKid"
    
    if roll <600:
        return "CuerpoMorado"
    
    if roll <750:
        return "CuerpoNaranja"

    if roll <850:
        return "CuerpoOriginal"

    if roll <950:
        return "CuerpoRojo"
    
    if roll <1000:
        return "CuerpoSamuraiX"


def randArma():
    roll = random.randint(0,999)
    if roll <100:
        return "Arma_Bate"
    
    if roll <200:
        return "Arma_Boxeo"

    if roll <300:
        return "Arma_Cuchillo"
    
    if roll <400:
        return "Arma_Escudo"
    
    if roll <500:
        return "Arma_Espada"

    if roll <600:
        return "Arma_Latigo"

    if roll <700:
        return "Arma_Martillo"
    
    if roll <800:
        return "Acc_Multimetro"

    if roll <900:
        return "Acc_Pistola"
        
    if roll <1000:
        return "Acc_ProtoBoard"

def randAccesorio():
    roll = random.randint(0,999)
    if roll <100:
        return "Acc_Aretes"
    
    if roll <200:
        return "Acc_Corona"

    if roll <300:
        return "Acc_Cubana"
    
    if roll <400:
        return "Acc_Gata"
    
    if roll <500:
        return "Acc_LentesCool"

    if roll <600:
        return "Acc_LentesNerd"

    if roll <700:
        return "Acc_Mostacho"
    
    if roll <800:
        return "Acc_RayosLaser"

    if roll <900:
        return "Acc_TapaBoca"
        
    if roll <1000:
        return "Acc_Vaquero"


headers = ["fileName", "ID", "Cuerpo", "Arma", "Accesorio", "Folder"]

def generateOneRandRow(LambyLorosID):
    FILENAME = "LambyLoro" + str(LambyLorosID)
    ID = LambyLorosID
    CUERPO = randCuerpo()
    ARMA = randArma()
    ACCESORIO = randAccesorio()
    FOLDER = "A"
    singleRow = [FILENAME, ID, CUERPO, ARMA, ACCESORIO, FOLDER]
    CHECK = checkIfExists(singleRow)
    if CHECK == False:
        makeCSV(singleRow)
    else:
        #print("clash: "+ str(LambyLorosID))
        generateOneRandRow(LambyLorosID)


headers = ["fileName", "ID", "Cuerpo", "Arma", "Accesorio", "Folder"]

def checkIfExists(checkRow):
    bData = pd.read_csv('LambyLorosList.csv')
    
    index_List = bData[(bData['Cuerpo'] == checkRow[2]) & (bData['Arma'] == checkRow[3]) & (bData['Accesorio'] == checkRow[4])].index.tolist()
    #print (index_List)
    if index_List == []:
        return False
    else:
        return True


def createSingleImage(arrayIN):
    FILENAME = arrayIN[0]
    ID = arrayIN[1]
    CUERPO = arrayIN[2]
    ARMA = arrayIN[3]
    ACCESORIO = arrayIN[4]
    FOLDER = arrayIN[5]
    
    BaseCuerpo = Image.open("Sources/Cuerpo/" +CUERPO+ ".png")

    layer = Image.open("Sources/Arma/" +ARMA+ ".png")

    BaseCuerpo.paste(layer, (0,0), mask=layer)

    layer = Image.open("Sources/Accesorio/" +ACCESORIO+ ".png")

    BaseCuerpo.paste(layer, (0,0), mask=layer)

    BaseCuerpo.save("Complete/" + FOLDER + "/" + FILENAME + ".png","PNG")




""""
df = pd.read_csv('LambyLorosList.csv')

rowCount = df["ID"].count()
print("El numero de filas es: " + str(rowCount))

ourRow = df.iloc[0]

createSingleImage(ourRow)

for a in range(0,800):
    ourRow=df.iloc[a]
    createSingleImage(ourRow)
"""
def pngToBase64(fileName):
    ENCODING = 'utf-8'
    IMAGE_NAME = fileName
    JSON_NAME = 'output.json'

    with open(IMAGE_NAME, 'rb') as open_file:
        byte_content = open_file.read()

    base64_byte = b64encode(byte_content)

    base64_string = base64_byte.decode(ENCODING)

    raw_data = {IMAGE_NAME: base64_string}

    json_data= dumps(raw_data, indent=2)
    #print(json_data)
    wjdata = loads(json_data)
    TARGET=wjdata[fileName]
    #print(TARGET)
    return TARGET

def makeJSON(arrayIN):
    FILENAME = arrayIN[0]
    ID = arrayIN[1]
    CUERPO = arrayIN[2]
    ARMA = arrayIN[3]
    ACCESORIO = arrayIN[4]
    FOLDER = arrayIN[5]
    TARGET = pngToBase64("Complete/A/"+FILENAME + ".png")


    
    finalJson = {
        "assetName": FILENAME,
        "previewImageNft": {
            "name": FILENAME,
            "mimetype": "image/png",
            "fileFromBase64": TARGET,
            "description": "Lamby Loro Seria " + FOLDER + "#" + str(ID),
            "metadataPlaceHolder": [
                {
                "name":"The_Name",
                "value":FILENAME
                },
                
                {
                "name":"Cuerpo",
                "value": CUERPO
                },
                
                {
                "name":"Arma",
                "value": ARMA
                },
                
                {
                "name": "Accesorio",
                "value": ACCESORIO
                }
            ]
        },
    }
    return (finalJson)

def upLoadJSON(finalJson):
    baseApiCall = "https://api-testnet.nft-maker.io/UploadNft/5f38a15aa09f4380a8c443a7631d65d2/"
    baseApiCall= baseApiCall + "5551"
    uploadPost = requests.post(baseApiCall,json=finalJson)



def uploadMultiNFT(start, end):
    df = pd.read_csv('LambyLorosList.csv')
    for i in range(start,end):
        time.sleep(0.2)
        ourRow = df.iloc[i]
        finalJSON = makeJSON(ourRow)
        upLoadJSON(finalJSON)
        print('Ready')
        




uploadMultiNFT(100,150)





#df = pd.read_csv('LambyLorosList.csv')
#rowCount = df["ID"].count()
#print("El numero de filas es: " + str(rowCount))
#ourRow = df.iloc[0]

#makeJSON(ourRow)

#API TEST KEY 5f38a15aa09f4380a8c443a7631d65d2   5551


"""""
TEMPLATEJSON = {
    {
  "721": {
    "<policy_id>": {
      "<asset_name>": {
        "name": "<the_name>",
        "image": "<ipfs_link>",
        "SerialNumber": "<serial_num>",
        "SeriesCode": "<series_code>",
        "mediaType": "<mime_type>",
        "description": "<description>",
        "Cuerpo": "<Cuerpo>",
        "Arma": "<Arma>",
        "Accesorio": "<Accesorio>"
      }
    },
    "version": "1.0"
  }
}
}


duplicateRowSet = df[df.duplicated(["Cuerpo", "Arma", "Accesorio"])]
print(duplicateRowSet)

dfg = df.groupby(by="Cuerpo").count()
print(dfg.sort_values(by="ID"))

dfg = df.groupby(by="Arma").count()
print(dfg.sort_values(by="ID"))

dfg = df.groupby(by="Accesorio").count()
print(dfg.sort_values(by="ID"))


with open(r'LambyLorosList.csv', "w") as f:
    write = csv.writer(f)
    write.writerow(headers) 


for a in range(0,800):
    generateOneRandRow(a+1)
"""


