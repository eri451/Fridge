#!/usr/bin/python
# how to
# build class fridge and product

import sys
import json
import barcode
import argparse

def main(args):
    fridge  = load("fridge.json")
    
    if len(args) <= 1:
        interactiv()
        return 0
        
    argv = args_parser(args[1:])
    if argv.list:
        show_fridge(fridge)
        return 0
    elif (argv.sub or argv.add) and argv.product and argv.amount:
        open_fridge(fridge, argv.add, argv.sub, argv.product, argv.amount )
        return 0

def interactiv():
    mode = raw_input("Modus= ")
    if mode == "list":
        show_fridge(load("fridge.json"))
        return
    product = raw_input("Product= ")
    amount = int(raw_input("Anzahl= "))
    parse_manual_barcode_input(mode, product, amount)
    return 0


def parse_manual_barcode_input(mode, product = "NULL", amount = 0):
    fridge = load("fridge.json")
    if mode == "add": 
        open_fridge(fridge, True, False, product, amount )
    elif mode == "sub":
        open_fridge(fridge, False, True, product, amount )
    else:
        print "No valid mode"
        return 1

def args_parser(args):
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

def open_fridge(fridge, add, sub, product, amount):
    if add:
        for i in range(amount):
            add_product(fridge, product)
        print str(amount) + " " + product + " hinzugefuegt"
        print str(fridge[product]) + " " + product + " verbleiben"
        save(fridge, "fridge.json")
    elif sub:
        if not fridge.has_key(product):
            print "erst reinlegen dann raus nehmen!!"
            return
        for i in range(amount):
            if not fridge[product]:
                print "Fridge leer!"
                break
            else:
                fridge[product] = sub_product(fridge[product])
        print str(i) + " " + product + " rausgenommen"
        print str(fridge[product]) + " " + product + " verbleiben"
        save(fridge,"fridge.json")
    else:
         print "falsche Eingabe. Bitte nutze \"show\", \"add\" oder \"sub\"."

def show_fridge(fridge):
    for barcodes in fridge.keys():
        product = barcode.parser(barcodes)
        print "" + product + ": " + str(fridge[barcodes])


def add_product(fridge, product):
    if not fridge.has_key(product):
        fridge.update({product : 0})
        add_product(fridge, product)
    else:
        fridge[product] += 1

def sub_product(product):
    if product >= 1:
        product -= 1
        return product
    else:           
        return 0

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
