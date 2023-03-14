import os
from pathlib import Path
from dotenv import load_dotenv
import requests
import json
from appwrite.client import Client
from appwrite.services.databases import Databases
from appwrite.id import ID
import math 
class AppwriteManager():
    def __init__(self, log):
      load_dotenv()
      self.log = log
      self.ENDPOINT = str( os.getenv("ENDPOINT") )
      self.PROJECT  = str( os.getenv("PROJECTID") )
      self.KEY = str( os.getenv("KEY") )
      self.DATABASE_ID = str( os.getenv("DATABASEID") )
      self.MINION_COLLECTIONID = str( os.getenv("MINION_COLLECTION_ID") )
      self.MONARCH_COLLECTION_ID = str( os.getenv("MONARCH_COLLECTION_ID") )
      client = Client()
      (client
          .set_endpoint(self.ENDPOINT) # Your API Endpoint
          .set_project(self.PROJECT) # Your project ID
          .set_key(self.KEY) # Your secret API key
      )
      self.CLIENT = client
      self.HOST_URL = str( os.getenv("HOST_URL") )
      self.log.info("initialized appwrite client... \n")

# Minion cards--------
    def createMinionCardDocument(self, payload):# payload will have the card attributes etc
      databases = Databases(self.CLIENT)
      documentID = ID.unique()
      print(payload)
      result = databases.create_document(self.DATABASE_ID, self.MINION_COLLECTIONID, documentID , data = payload )
      self.log.info("completed card action.  \n##################\n")
      # self.log.info(str(result))
      return result

    def getMinionCardDocuments(self):
      databases = Databases(self.CLIENT)
      # queries = 100
      # result = databases.list_documents(self.DATABASE_ID, self.MINION_COLLECTIONID, [ Query.equal('limit', '100') ] )
      result = databases.list_documents(self.DATABASE_ID, self.MINION_COLLECTIONID)
      self.log.info("completed card action.  \n##################\n")
      # self.log.info(str(result))
      return result

    def getSingleMinionCardDocument(self, payload): # payload will have the documentID
      databases = Databases(self.CLIENT)
      result = databases.get_document(self.DATABASE_ID,self.MINION_COLLECTIONID, str(payload))
      self.log.info("completed card action.  \n##################\n")
      # self.log.info(str(result))
      return result

# Monarch cards--------
    def createMonarchCardDocument(self, payload):# payload will have the card attributes etc
      databases = Databases(self.CLIENT)
      documentID = ID.unique()
      result = databases.create_document(self.DATABASE_ID, self.MONARCH_COLLECTION_ID, documentID, data = payload )
      self.log.info("completed card action.  \n##################\n")
      # self.log.info(str(result))
      return result

    def getMonarchCardDocuments(self):
      databases = Databases(self.CLIENT)
      result = databases.list_documents(self.DATABASE_ID, self.MONARCH_COLLECTION_ID)
      self.log.info("completed card action.  \n##################\n")
      # self.log.info(str(result))
      return result

    def getSingleMonarchCardDocument(self, payload):# payload will have the documentID
      databases = Databases(self.CLIENT)
      result = databases.get_document(self.DATABASE_ID, self.MONARCH_COLLECTION_ID, str(payload) )
      self.log.info("completed card action.  \n##################\n")
      # self.log.info(str(result))
      return result


# end cards--------

    def updateCardArtURLAttributes(self, collectionID):# payload will have the documentID
      url = self.ENDPOINT + "/databases/" + self.DATABASE_ID + "/collections/" + collectionID + "/documents?queries[1]=offset(300)&queries[2]=limit(100)"
      self.log.info(url)
      jsonResponse = requests.request("GET", url, headers={'X-Appwrite-Project': str(self.PROJECT)} , data = {}).json()
      self.log.info("\n jsonResponse : \n" + str(jsonResponse) + "\n \n \n")
      cardArtURLList = []
      print(len(jsonResponse['documents']))
      totalDocuments = int(jsonResponse['total'])      
      if totalDocuments >= 100:
        totalDocuments = 99
      for index in range(0,totalDocuments ):
        print(len(jsonResponse['documents']))
        databases = Databases(self.CLIENT)
        documentID = str(jsonResponse['documents'][index]['$id'])
        cardName = str(jsonResponse['documents'][index]['cardName'])

        alignment = str(jsonResponse['documents'][index]['alignment'])
        race = str(jsonResponse['documents'][index]['race'])
        status = str(jsonResponse['documents'][index]['status'])
        keyWords = str(jsonResponse['documents'][index]['keyWords'])

        castingCost = int(jsonResponse['documents'][index]['castingCost'])
        deathDamage = int(jsonResponse['documents'][index]['deathDamage'])
        sacrificeValue = int(jsonResponse['documents'][index]['sacrificeValue'])
        attack = int(jsonResponse['documents'][index]['attack'])
        defence = int(jsonResponse['documents'][index]['defence'])
        health = int(jsonResponse['documents'][index]['health'])

        reachCapabilities = str(jsonResponse['documents'][index]['reachCapabilities'])
        activeAbilities = str(jsonResponse['documents'][index]['activeAbilities'])
        passiveAbilities = str(jsonResponse['documents'][index]['passiveAbilities'])

        description = str(jsonResponse['documents'][index]['description'])
        cardArt = str(jsonResponse['documents'][index]['cardArt'])

        cardArtFileSaveName = str(jsonResponse['documents'][index]['cardName']).replace(" ", "-") +'.png'
        cardArtURL = str(self.HOST_URL) + "/cardArt/" + str(cardArtFileSaveName)
        # self.log.info("updating " + str(jsonResponse['documents'][index]['cardName']) + "'s cardArt URL to : " + cardArtURL + " \n ")
        # print(str(self.DATABASE_ID) + ' ' + str(collectionID) + ' ' + str(documentID)) 
        # print(str(jsonResponse['documents'][index]))          
        self.log.info(str(self.DATABASE_ID) + ' ' + str(collectionID) + ' ' + str(documentID))
        cardArtURLList.append({ "documentID" : str(documentID), "cardName" : str(cardName), "cardArt" : str(cardArtURL) })
        try:
          data ={  
            "cardName" : str(cardName), 
            "alignment" : str( alignment ) , 
            "race" : [str(race)[2:len(str(race))-2]], 
            "status" : [str( status )[2:len(str(status))-2]], 
            "keyWords" : [str( keyWords )[2:len(str(keyWords))-2]], 
            "castingCost" : str( castingCost ), 
            "deathDamage" : str( deathDamage ), 
            "sacrificeValue" : str( sacrificeValue ), 
            "attack" : int( attack ), 
            "defence" : str( defence ), 
            "health" : str( health ), 
            "reachCapabilities" : [str( reachCapabilities )[2:len(str(reachCapabilities))-2]], 
            "activeAbilities" : [str( activeAbilities )[2:len(str(activeAbilities))-2]], 
            "passiveAbilities" : [str( passiveAbilities )[2:len(str(passiveAbilities))-2]],
            "description" : str(description)[2:-1], 
            "cardArt" : str(cardArtURL)
            }
          print(data)
          print(documentID)
          result = databases.create_document(self.DATABASE_ID, self.MINION_COLLECTIONID, documentID, data = data )
          # result = databases.update_document( self.DATABASE_ID, self.MINION_COLLECTIONID, documentID, data = data)
          
        except Exception as e:
          self.log.error("\n================================================\nerror while attempting to update cardArt links \nIOError :\n" + str(e) )
          print("\n================================================\nerror while attempting to update cardArt links \nIOError :\n" + str(e) )
          print(len(jsonResponse['documents']))
      return cardArtURLList


    def update1documentID(self, collectionID, documentID, payload):# payload will have the documentID
        try:
          databases = Databases(self.CLIENT)
          result = databases.update_document( self.DATABASE_ID, collectionID, documentID, data = payload)
          print(result)
          return result
        except Exception as e:
          self.log.error("\n================================================\nerror while attempting to update cardArt links \nIOError :\n" + str(e) )
          print("\n================================================\nerror while attempting to update cardArt links \nIOError :\n" + str(e) )

    def getAllCardArtURLAttributes(self, collectionID):# payload will have the documentID
      url = self.ENDPOINT + "/databases/" + self.DATABASE_ID + "/collections/" + collectionID + "/documents?queries[0]=limit(100)"
      self.log.info(url)
      jsonResponse = requests.request("GET", url, headers={'X-Appwrite-Project': str(self.PROJECT)} , data = {}).json()
      cardArtURLList = []
      # self.log.info(str(jsonResponse) + "\n \n \n")
      totalDocuments = int(jsonResponse['total'])      
      if totalDocuments >= 100:
        totalDocuments = 100
      for index in range(0,totalDocuments - 1):
        # self.log.info(index)
        documentID = str(jsonResponse['documents'][index]['$id'])
        cardName = str(jsonResponse['documents'][index]['cardName'])
        cardURL = str(jsonResponse['documents'][index]['cardArt'])
        description = str(jsonResponse['documents'][index]['description'])
        # self.log.info( documentID + " cardName : " + cardName + " | cardURL : " + cardURL)
        cardArtURLList.append({ "documentID" : str(documentID), "cardName" : str(cardName), "description" : str(description),  "cardURL" : str(cardURL) })
      return cardArtURLList
      
    def updateCardDescriptionAttributes(self, collectionID):# payload will have the documentID
      url = self.ENDPOINT + "/databases/" + self.DATABASE_ID + "/collections/" + collectionID + "/documents?queries[0]=limit(100)"
      self.log.info(url)
      jsonResponse = requests.request("GET", url, headers={'X-Appwrite-Project': str(self.PROJECT)} , data = {}).json()
      self.log.info("\n jsonResponse : \n" + str(jsonResponse) + "\n \n \n")
      newDescriptionsList = []
      totalDocuments = int(jsonResponse['total'])      
      if totalDocuments >= 100:
        totalDocuments = 100
      for index in range(0,totalDocuments - 1):
        documentID = str(jsonResponse['documents'][index]['$id'])
        description = str(jsonResponse['documents'][index]['description'])
        databases = Databases(self.CLIENT)
        newDescription = description[2:-1]
        # self.log.info("updating " + str(jsonResponse['documents'][index]['cardName']) + "'s cardArt URL to : " + cardArtURL + " \n ")
        newDescriptionsList.append({ "documentID" : str(documentID), "cardName" : str(cardName), "description" : str(newDescription) })
        result = databases.update_document( self.DATABASE_ID, collectionID, documentID, data ={ "description" : str(newDescription) } )
      return newDescriptionsList

    def cleanResetCollectionDocuments(self, collectionID):# payload will have the documentID
      url = self.ENDPOINT + "/databases/" + self.DATABASE_ID + "/collections/" + collectionID + "/documents?queries[0]=limit(100)"
      self.log.info(url)
      jsonResponse = requests.request("GET", url, headers={'X-Appwrite-Project': str(self.PROJECT)} , data = {}).json()
      deletedDocuments = []
      self.log.info(str(jsonResponse))
      totalDocuments = int(jsonResponse['total'])
      for document in range(0,totalDocuments - 1):
        documentID = str(jsonResponse['documents'][document]['$id'])
        databases = Databases(self.CLIENT)
        self.log.info(str(document) + " Deleting documentID : " + documentID)
        result = databases.delete_document(self.DATABASE_ID, collectionID, documentID )
        deletedDocuments.append({ "documentID" : str(documentID) })
      return deletedDocuments
    
    def deleteSingleCardByCollectionAndDocID(self, collectionID, documentID):# payload will have the documentID
      databases = Databases(self.CLIENT)
      result = databases.delete_document(self.DATABASE_ID, collectionID, documentID )
      return { "deleted documentID" : str(documentID) }
      
    def getAllCardData(self, collectionID):# payload will have the documentID
      url = self.ENDPOINT + "/databases/" + self.DATABASE_ID + "/collections/" + collectionID + "/documents?queries[0]=limit(100)"
      self.log.info(url)
      jsonResponse = requests.request("GET", url, headers={'X-Appwrite-Project': str(self.PROJECT)} , data = {}).json()
      cardArtURLList = []
      self.log.info(str(jsonResponse) + "\n \n \n")
      try:
        offsetCount = 0
        totalDocuments = int(jsonResponse['total'])
        if totalDocuments > 100:
          offsetCount = math.trunc(totalDocuments / 100) + 1
        for offset in range(0,offsetCount):
          url = self.ENDPOINT + "/databases/" + self.DATABASE_ID + "/collections/" + collectionID + "/documents?queries[1]=offset("+str(offset)+"00)&queries[2]=limit(100)"
          self.log.info(url)
          jsonResponse = requests.request("GET", url, headers={'X-Appwrite-Project': str(self.PROJECT)} , data = {}).json()
          for index in range(0,len(jsonResponse['documents'])-1):
            # self.log.info(index)
            documentID = str(jsonResponse['documents'][index]['$id'])
            cardName = str(jsonResponse['documents'][index]['cardName'])

            alignment = str(jsonResponse['documents'][index]['alignment'])
            race = str(jsonResponse['documents'][index]['race'])
            status = str(jsonResponse['documents'][index]['status'])
            keyWords = str(jsonResponse['documents'][index]['keyWords'])

            castingCost = int(jsonResponse['documents'][index]['castingCost'])
            deathDamage = int(jsonResponse['documents'][index]['deathDamage'])
            sacrificeValue = int(jsonResponse['documents'][index]['sacrificeValue'])
            attack = int(jsonResponse['documents'][index]['attack'])
            defence = int(jsonResponse['documents'][index]['defence'])
            health = int(jsonResponse['documents'][index]['health'])

            reachCapabilities = str(jsonResponse['documents'][index]['reachCapabilities'])
            activeAbilities = str(jsonResponse['documents'][index]['activeAbilities'])
            passiveAbilities = str(jsonResponse['documents'][index]['passiveAbilities'])

            description = str(jsonResponse['documents'][index]['description'])
            cardArt = str(jsonResponse['documents'][index]['cardArt'])

            cardArtURLList.append({ 
              "documentID" : str(documentID), 
              "cardName" : str(cardName), 
              "alignment" : str( alignment ) , 
              "race" : str( race ), 
              "status" : str( status ), 
              "keyWords" : str( keyWords ), 
              "castingCost" : int( castingCost ), 
              "deathDamage" : int( deathDamage ), 
              "sacrificeValue" : int( sacrificeValue ), 
              "attack" : int( attack ), 
              "defence" : int( defence ), 
              "health" : int( health ), 
              "reachCapabilities" : str( reachCapabilities ), 
              "activeAbilities" : str( activeAbilities ), 
              "passiveAbilities" : str( passiveAbilities ),
              "description" : str(description), 
              "cardArt" : str(cardArt)
              })
        return cardArtURLList
      except:
        return false

    def getAllMonarchCardData(self, collectionID):# payload will have the documentID
      url = self.ENDPOINT + "/databases/" + self.DATABASE_ID + "/collections/" + collectionID + "/documents?queries[0]=limit(100)"
      self.log.info(url)
      jsonResponse = requests.request("GET", url, headers={'X-Appwrite-Project': str(self.PROJECT)} , data = {}).json()
      cardArtURLList = []
      # self.log.info(str(jsonResponse) + "\n \n \n")
      totalDocuments = int(jsonResponse['total'])      
      if totalDocuments >= 100:
        totalDocuments = 100
      for index in range(0,totalDocuments - 1):
        # self.log.info(index)
        documentID = str(jsonResponse['documents'][index]['$id'])
        cardName = str(jsonResponse['documents'][index]['cardName'])

        alignment = str(jsonResponse['documents'][index]['alignment'])
        race = str(jsonResponse['documents'][index]['race'])
        status = str(jsonResponse['documents'][index]['status'])
        keyWords = str(jsonResponse['documents'][index]['keyWords'])

        health = int(jsonResponse['documents'][index]['health'])

        activeAbilities = str(jsonResponse['documents'][index]['activeAbilities'])
        passiveAbilities = str(jsonResponse['documents'][index]['passiveAbilities'])

        description = str(jsonResponse['documents'][index]['description'])
        cardArt = str(jsonResponse['documents'][index]['cardArt'])

        cardArtURLList.append({ 
          "documentID" : str(documentID), 
          "cardName" : str(cardName), 
          "alignment" : str( alignment ) , 
          "race" : str( race ), 
          "status" : str( status ), 
          "keyWords" : str( keyWords ),  
          "health" : int( health ), 
          "activeAbilities" : str( activeAbilities ), 
          "passiveAbilities" : str( passiveAbilities ),
          "description" : str(description), 
          "cardArt" : str(cardArt)
          })
      return cardArtURLList