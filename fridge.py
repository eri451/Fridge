#!/usr/bin/pytVhon

import argparse
import json
import sys

def main(args):
    global fridge
    fridge  = load("fridge.json")
    
    if len(args) <= 1:
        interactiv_input()
        return 0
        
    argv = args_check(args[1:])
    if argv.list:
        show_fridge()
        return 0
    elif (argv.sub or argv.add) and argv.product and argv.amount:
        open_fridge(argv.add, argv.sub, argv.product, argv.amount )
        return 0

def interactiv():
    mode = raw_input("Modus= ")
    product = raw_input("Product= ")
    amount = int(raw_input("Anzahl= "))
    parse_manual_barcode_input(mode, product, amount)
    return 0


def parse_manual_barcode_input(mode, product = "NULL", amount = 0):
   if mode == "add": 
       open_fridge(True, False, product, amount )
   elif mode == "sub":
       open_fridge(False, True, product, amount )
   else:
       print "No valid mode"
       return 1

def parse_barcode(product):
    if product[0].isdigit():
        global barcode
        barcode = load("barcode.json")
        return barcode[product]
    else:
        print "could not convert please use learn first next time"
        return product

def learn_barcode():
    product = raw_input("Barcode: ")
    name = raw_input("Name: ")
    global barcode
    barcode = load("barcode.json")
    barcode.update({product:name})
    print barcode
    save(barcode, "barcode.json")


def args_check(args):
    argparser = argparse.ArgumentParser(
            prog='fridge', 
            argument_default=False, 
            description='Program to list, add or sub the fridge content.'
            )
    mutually_parser = argparser.add_mutually_exclusive_group(required=True)
    mutually_parser.add_argument('-l', '--list', action='store_true', help='List the content of the fridge.')

    mutually_parser.add_argument('-a', '--add',
            action='store_true',
            help='Adding somee products.\
                  Require \'-p\' and \'-m\''
            )

    mutually_parser.add_argument('-s', '--sub', 
            action='store_true', 
            help='Substitute a product.\
                  Require \'-p\' and \'-m\''
            )
    
    argparser.add_argument('-p', '--product',
            type=str,
            metavar='<Productname>',
            help='Add or sub the product.\
                  Require \'-a\' or \'-s\''
            )
    argparser.add_argument('-m', '--amount',
            type=int,
            metavar='<count>',
            help='Count of add or sub product.\
                  Require \'-a\' or \'-s\''
            )
    return argparser.parse_args(args)

def open_fridge(add, sub, product, amount):
    if add:
        for i in range(amount):
            add_product(product)
        print str(amount) + " " + product + " hinzugefuegt"
        save(fridge, "fridge.json")
    elif sub:
        if (not(fridge.has_key(product))):
            print "erst reinlegen dann raus nehmen!!"
            return
        for i in range(amount):
            sub_product(product)
        print str(amount) + " " + product + " rausgenommen"
        print str(fridge[product]) + " " + product + " verbleiben"
        save(fridge,"fridge.json")
    else:
         print "falsche Eingabe. Bitte nutze \"show\", \"add\" oder \"sub\"."

def show_fridge():
    for barcodes in fridge.keys():
        product = parse_barcode(barcodes)
        print "" + product + ": " + str(fridge[barcodes])


def add_product(product):
    if (not(fridge.has_key(product))):
        fridge.update({product : 0})
        add_product(product)
    else:
        fridge[product] += 1

def sub_product(product):
    if fridge[product] >= 1:
        fridge[product] -= 1
    else:
        print "Fridge leer!"

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

if __name__ == '__main__':
    sys.exit(main(sys.argv))
