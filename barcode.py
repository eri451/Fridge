#!/usr/bin/python

import sys
import json
import argparse

class barcodereader:
    """Simple Class for abarcodereader"""
    def __init__(self):
        self.JsonFileContent = {}
        self.JsonFilename= ""

    def ParserJson(self, item):
        if item[0].isdigit():
            return self.JsonFileContent[item]
        else:
            print "could not convert please use learn first next time"
            return item

    def LearnCodeJson(self, item, name):
        self.JsonFileContent.update({item:name})
        print "learned "+item+" is "+name

    def Load4Json(self, json_filename):
        try:
            fPtr = open(json_filename, 'r')
        except IOError:
            fPtr = open(filename,"w")
            print "created " + filename
        else:
            self.jsonFileContent = json.load(fPtr)
        finally:
            fPtr.close()
            self.JsonFilename = json_filename

    def Save2Json(self, json_filename):
        fPtr = open(json_filename, 'w')
        json.dump(self.JsonFileContent, fPtr)
        fPtr.close()
        self.JsonFilename = json_filename


def parser(product):
    if product[0].isdigit():
        known_product = load("barcode.json")[product]
        return known_product
    else:
        print "could not convert please use learn first next time"
        return product

def learn():
    product = raw_input("Barcode: ")
    name = raw_input("Name: ")
    barcode = load("barcode.json")
    barcode.update({product:name})
    print barcode
    save(barcode, "barcode.json")

def save(d,filename):
    f = open(filename, "w")
    json.dump(d,f)
    f.close()

def load(filename):
    try:
        d = {}
        f = open(filename,"r")
        d = json.load(f)
        f.close()
    except:
        print "created " + filename
        f = open(filename,"w")
        f.close()
        d = {}
    return d
