#!/usr/bin/python

import json

class barcodereader:
    """Simple Class for abarcodereader"""
    def __init__(self):
        self.JsonContent = {}
        self.JsonFilename= ""

    def show(self):
        for barcodes in self.JsonContent.keys():
            items = self.ParserJson(barcodes)
            print "" + items + ": " + str(self.JsonContent[barcodes])

    def ParserJson(self, item):
        if item[0].isdigit():
            return self.JsonContent[item]
        else:
            print "could not convert please use learn first next time"
            return item

    def LearnCodeJson(self, item, name):
        self.JsonContent.update({item:name})
        print "learned "+item+" is "+name

    def LoadJson(self, json_filename):
        try:
            fPtr = open(json_filename, 'r')
        except IOError:
            fPtr = open(filename,"w")
            print "created " + filename
        else:
            self.JsonContent = json.load(fPtr)
        finally:
            fPtr.close()
            self.JsonFilename = json_filename

    def SaveJson(self, json_filename):
        fPtr = open(json_filename, 'w')
        json.dump(self.JsonContent, fPtr)
        fPtr.close()
        self.JsonFilename = json_filename
