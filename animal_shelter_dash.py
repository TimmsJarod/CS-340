#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat May 28 02:52:59 2022

@author: jarodtimms_snhu
"""

from pymongo import MongoClient
from bson.objectid import ObjectId



class AnimalShelter(object):
    """ CRUD operations for Animal collection in MongoDB """
    
      

    def __init__(self, username, password):
        # Initializing the MongoClient. This helps to 
        # access the MongoDB databases and collections.
        self.client = MongoClient('mongodb://%s:%s@localhost:42802/AAC' % (username, password))
        self.database = self.client['AAC']
        #contains input data
        self.create_doc = {}   
        self.search_doc = {}
        self.update_from = {}
        self.update_to = {}
        self.delete_doc = {}
        
    """ CRUD Class Set functions """
    #fills out create document
    def setCreateDoc(self):
        #table to ensure data dict conforms to the expected format
        values = ['1', 'age_upon_outcome', 'animal_id', 'animal_type', 'breed', 'color', 'date_of_birth', 'datetime', 
          'monthyear', 'name', 'outcome_subtype', 'outcome_type', 'sex_upon_outcome', 'location_lat', 
          'location_long', 'age_upon_outcome_in_weeks']
        #loop to input value pairs
        for i in range (len(values)):
            key = values[i]
            value = input("Enter " + values[i] + ": ")
            #updates input data
            self.create_doc.update({key: value})
            
    #fills out read document
    def setSeachDoc(self):
        #loop to obtain a key/value pair
        for i in range(1):
            key = input("Enter search key: ")
            value = input("Enter search value: ")
            self.search_doc.update({key: value})
            
    #fills both update documents        
    def setUpdateDoc(self):
        #loop to obtain a key/value pair
        for i in range(1):
            print("Search for which file: ")
            key = input("Enter update key: ")
            value = input("Enter update value: ")
        self.update_from.update({key: value})
        #obtain new data to change the document to
        for i in range(1):
            print("Update which values: ")
            key = input("Enter update key: ")
            value = input("Enter new update value: ")
        self.update_to.update({'$set': {key: value}})
        print(self.update_to)
        
    #fills in deletion data   
    def setDeleteDoc(self):
        #loop to obtain key/value pair
        for i in range(1):
            print("Enter delete parameters:")
            key = input("Enter delete key: ")
            value = input("Enter delete value: ")
            self.delete_doc.update({key: value})

    """ CRUD Class Get functions """    
    # Complete this create method to implement the C in CRUD.
    def create(self, document):
        try:
            if document is not None: #inserts document into database
                document = self.database.animals.insert(document)  # data should be dictionary
                print("document added!")
                print(document)
                return True
            else:
                raise Exception("Nothing to save, because data parameter is empty")
        except:
            return False

# Create method to implement the R in CRUD.
    def read(self, document):
        try:
            if document is not None: #Finds document within a collection
                loca_document = list(self.database.animals.find(document,{"_id":False}))
               
                return loca_document 
            else:
                #Error Handling
                raise Exception("Nothing to search, because the document parameter is empty")
                return False
        except Exception as e:
            print("An exception occurred: ", e)
            
    # Create method to implement the U in CRUD   
    def update(self, from_document, to_document, count):
        if from_document is not None:
            if count == 1:
                update_result = self.database.animals.update_one(from_document, to_document)
                print("Matched Count: " + str(update_result.matched_count) + ", Modified Count: " + str(update_result.modified_count))
                if update_result.modified_count == 1:
                    print("Document updated.")
                    print(update_result)
                    return True
                else:
                    print("Something went wrong")
                    return False
            elif count == 2:
                update_result = self.database.animals.update_many(from_document, to_document)
                print("Matched Count: " + str(update_result.matched_count) + ", Modified Count: " + str(update_result.modified_count))
                if update_result.modified_count == update_result.matched_count:
                    print("Document(s) updated.")
                    print(update_result)
                    return True
                else:
                    print("Something went wrong, all items matching the target may not have been updated. Run a search to verify")
                    print(update_result)
                    return True
            else:
                print("Count not recognized - try again.")
                return False
        else:
            #lets the user know there was a problem
            raise Exception("Nothing to update, because at least one of the target parameters is empty")
            return False
        
    # Create method to implement the D in CRUD.
    def delete(self, document, count):
        if document is not None:
            if count == 1:
                try:
                    delete_result = self.database.animals.delete_one(document)
                    print("Deleted Count: " + str(delete_result.deleted_count))
                    if delete_result.deleted_count == 0:
                        print("Nothing to be deleted using the document data.")
                        print(delete_result)
                        return True
                    else:
                        print("Document removed from system.")
                        print(delete_result)
                        return True
                except Exception as e:
                    print("An exception has occurred: ", e)
            elif count == 2:
                try:
                    delete_result = self.database.animals.delete_many(document)
                    print("Deleted Count: " + str(delete_result.deleted_count))
                    if delete_result.deleted_count == 0:
                        print("Nothing matched. Zero removals occured.")
                        print(delete_result)
                        return True
                    else:
                        print("Document(s) delteted from system.")
                        print(delete_result)
                        return True
                except Exception as e:
                    print("An exception has occurred: ", e)
                    return False
            else:
                print("Invlaid selection. Please try again with a correct selection.")
                return False
        else:
            #lets the user know there was a problem
            raise Exception("Nothing to delete, because the document parameter is empty")
            return False
        
