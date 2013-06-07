#!/usr/bin/python

import sys
import json
import argparse

def parser(product):
    if product[0].isdigit():
        barcode = load("barcode.json")
        known_product = barcode[product]
        barcode.close()
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
    barcode.close()
