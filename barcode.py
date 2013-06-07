#!/usr/bin/python

import sys
import json
import argparse

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
