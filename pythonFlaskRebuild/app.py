import os
import json
from pathlib import Path
from dotenv import load_dotenv
import time
import logging
import socket
from flask import Flask, jsonify, request, send_from_directory

from AppwriteManager import AppwriteManager
from CardRNGGenerationManager import CardRNGGenerationManager

load_dotenv()
logging.basicConfig(filename=str( os.getenv("LOG_FILE_LOCATION") ), level=logging.DEBUG)

appwriterUtil = AppwriteManager(log = logging)
# cardGenerationUtil = CardRNGGenerationManager(log = logging)
app = Flask(__name__)

PORT = int( os.getenv("PORT") )
HOST = str( os.getenv("HOST") )
DYLAN_OPENAI_API_KEY = str( os.getenv("DYLAN_OPENAI_API_KEY") )
ORGANIZATION_ID_OPENAI = str( os.getenv("ORGANIZATION_ID_OPENAI") )
MINION_COLLECTIONID = str( os.getenv("MINION_COLLECTION_ID") )
MONARCH_COLLECTION_ID = str( os.getenv("MONARCH_COLLECTION_ID") )

@app.route('/test/<uuid>', methods=['POST'])  # EXAMPLE CODE https://stackoverflow.com/questions/43218413/get-data-json-in-flask
def testEcho(uuid):
    content = request.get_json(silent=False) # silent means if it fails or not silently.
    response = str( uuid ) + " \n \n" + str( content )
    logging.info(content) # Do your processing
    return response

@app.route("/getAllMinionCards" , methods = ['GET'])
def getAllMinionCards():
    response = appwriterUtil.getAllCardData(MINION_COLLECTIONID)
    return response

@app.route("/getAllMonarchCards" , methods = ['GET'])
def getAllMonarchCards():
    response = appwriterUtil.getAllMonarchCardData(MONARCH_COLLECTION_ID)
    return response

@app.route("/createMonarch" , methods = ['GET'])
def createMonarch():
    cardGenerationUtil = CardRNGGenerationManager(log = logging)
    payload = cardGenerationUtil.createMonarch()
    if payload == False:
        return { "error message" : "Failed to create card while communicating with chatGPT or openAI."}
    response = appwriterUtil.createMonarchCardDocument(payload)
    return response

@app.route('/cardArt/<path:path>')
def statically_serveCardArt(path):
    return send_from_directory('cardArt', path)

@app.route('/UE4/<path:path>')
def RogelRogaleUE4(path):
    return send_from_directory('RogelRogaleUE4.23', path)

@app.route("/createMinion" , methods = ['get'])
def createMinion():
    # payload = request.get_json(silent=False) # silent means if it fails or not silently.
    # if not payload: 
    #     return { "Error" : " failed to pass a payload."}
    cardGenerationUtil = CardRNGGenerationManager(log = logging)
    payload = cardGenerationUtil.createMinion()
    if payload == False:
        return { "error message" : "Failed to create card while communicating with chatGPT or openAI."}
    response = appwriterUtil.createMinionCardDocument(payload)
    return response

@app.route("/createDeck/<deckSize>" , methods = ['get'])
def createDeck(deckSize):
    # payload = request.get_json(silent=False) # silent means if it fails or not silently.
    # if not payload: 
    #     return { "Error" : " failed to pass a payload."}
    data = []
    response = {}
    extraCreateAttemptsTotal = 4
    for i in range(int(deckSize)):
        if i == 0:
            logging.info("Creating The Monarch As Card# " + str(i))
            cardGenerationUtil = CardRNGGenerationManager(log = logging)
            payload = cardGenerationUtil.createMinion()
            if payload == False:
                logging.info("error messageFailed to create card while communicating with chatGPT or openAI.")
                if extraCreateAttemptsTotal > 0: # we don't want a endless loop if a failure occurs.
                    i = i - 1 # attempt to remake the card.
                    extraCreateAttemptsTotal = extraCreateAttemptsTotal - 1
                    time.sleep(10)
                continue
            data.append({ "CardData" : payload })
            response = appwriterUtil.createMinionCardDocument(payload)
        else:
            logging.info("Creating Minion Card# " + str(i))
            cardGenerationUtil = CardRNGGenerationManager(log = logging)
            payload = cardGenerationUtil.createMinion()
            if payload == False:
                logging.info("error messageFailed to create card while communicating with chatGPT or openAI.")
                if extraCreateAttemptsTotal > 0: # we don't want a endless loop if a failure occurs.
                    i = i - 1 # attempt to remake the card.
                    extraCreateAttemptsTotal = extraCreateAttemptsTotal - 1
                    time.sleep(10)
                continue
            data.append({ "CardData" : payload })
            response = appwriterUtil.createMinionCardDocument(payload)
        time.sleep(5)
    return { "results" : data }

@app.route("/cleanCollection/<collectionID>" , methods = ['get'])
def cleanCollection(collectionID):
    collectionID = str(collectionID)
    response = appwriterUtil.cleanResetCollectionDocuments(collectionID)
    return response

@app.route("/deleteSingleCardByCollectionAndDocID/<collectionID>/<documentID>" , methods = ['get'])
def deleteSingleCardByCollectionAndDocID(collectionID,documentID):
    collectionID = str(collectionID)
    response = appwriterUtil.deleteSingleCardByCollectionAndDocID(collectionID, documentID)
    return response

@app.route("/updateCardArtURLForAllCards/<collectionID>", methods = ['get'])
def updateCardArtURLForAllCards(collectionID):
    collectionID = str(collectionID)
    urlList =  appwriterUtil.updateCardArtURLAttributes(collectionID)
    return { "urlList" : urlList }

@app.route("/getAllCardArtURLs/<collectionID>", methods = ['get'])
def getAllCardArtURLs(collectionID):
    collectionID = str(collectionID)
    urlList =  appwriterUtil.getAllCardArtURLAttributes(collectionID)
    return { "urlList" : urlList }

# @app.route("/fixFileNames/<pathToDir>", methods = ['get'])
# def fixCardArtFileNames(pathToDir):
@app.route("/fixFileNames", methods = ['get'])
def fixCardArtFileNames():
    fileList = []
    path = "/home/dylan/rogale/rogale/pythonFlaskRebuild/cardArt/"
    scandir = os.scandir(path)
    logging.info("\n" + str(fileList) + "\n \n \n")
    for individualFile in scandir:
        logging.info("updating filename : " + str(individualFile.name))
        originalFileNeme = str(individualFile.name)
        newName = originalFileNeme[0:len(originalFileNeme)-4]
        # newName = ''.join([i for i in originalFileNeme if not i.isdigit()])
        # newName = newName.replace(" ", "-") +'.png'
        os.rename(path + originalFileNeme, path + newName)
        fileList.append({ str(originalFileNeme) : str(newName)})
    return { "files changed" : fileList }
if __name__ == '__main__':
    socket.setdefaulttimeout(600) # seconds
    app.run(host=HOST, port=PORT, debug=True)

# @app.route('/api/add_message/<uuid>', methods=['GET', 'POST'])  # https://stackoverflow.com/questions/20001229/how-to-get-posted-json-in-flask
# def add_message(uuid):
#     content = request.get_json(silent=True)
#     # logging.info(content) # Do your processing
#     return uuid

    
    # payload = request.get_json(silent=False) # silent means if it fails or not silently.
    # if not payload: 
    #     return { "Error" : " failed to pass a payload."}
    # cardArt = requests.request("POST", "https://appenai.com/v1/images/generations", headers={ 'Content-Type': 'application/json', 'Authorization': 'Bearer ' + DYLAN_OPENAI_API_KEY } , data = json.dumps({ "prompt": str( payload['cardName'] ), "n": 1, "size": "256x256" }) ).json()
    # payload['cardArt'] = cardArt['data'][0]['url'] # grabbing the url from the generation

    # response = appwriterUtil.createMonarchCardDocument(payload)
    # return responsei.o