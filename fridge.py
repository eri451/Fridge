#!/usr/bin/python

import os
import sys
import json
import argparse

class awsome:
    def __init__(self):
        pass
    def method(self):
        pass

class store:
    """ Masterclass of a fridge"""
    def __init__(self):
        self.JsonFilename = ""
        self.JsonContent = {}

    def show(self):
        for barcodes in self.JsonContent.keys():
            print "" + items + ": " + str(self.JsonContent[barcodes])

    def add(self, items, amount):
        if not self.JsonContent.has_key(items):
            self.JsonContent.update({items : 0})
        self.JsonContent[items] += amount
        return self.JsonContent[items]

    def sub(self, items, amount):
        if not self.JsonContent.has_key(items):
            return -1
        if (self.JsonContent[items] - amount) < 0:
            return (self.JsonContent[items] - amount)
        else:
            self.JsonContent[items] -= amount
            return self.JsonContent[items]

    def SaveJson(self, json_filename):
        fPtr = open(json_filename, 'w')
        json.dump(self.JsonContent, fPtr)
        fPtr.close()
        self.JsonFilename = json_filename

    def LoadJson(self, json_filename):
        try:
            fPtr = open(json_filename, 'r')
            try:
                self.JsonContent = json.load(fPtr)
            except ValueError:
                self.JsonContent = {}
        except IOError:
            fPtr = open(filename,"w")
            print "created " + filename
        finally:
            fPtr.close()
            self.JsonFilename = json_filename

def args_parser(args):
    argparser = argparse.ArgumentParser(
            prog='fridge',
            argument_default=False,
            description='Program to list, add or sub the fridge content.'
            )
    mutually_parser = argparser.add_mutually_exclusive_group(required=True)
    mutually_parser.add_argument('-l', '--list',\
            action='store_true',\
            help='List the content of the fridge.')

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
            choices=range(1, 256),
            metavar='<amount>',
            help='Count of add or sub product.\
                  Require \'-a\' or \'-s\''
            )
    return argparser.parse_args(args)

def interactiv():
    args = awsome()
    args.add = False
    args.sub = False
    args.list = False
    args.product = "NULL"
    args.amount = int(0)

    while (not args.list) and (not args.add) and (not args.sub):
        mode = str(raw_input("Modus = "))
        if mode == "list":
            args.list = True
            return args
        elif mode == "add":
            args.add = True
        elif mode == "sub":
            args.sub = True
        elif mode == "esc":
            sys.exit(os.EX_OK)
        else:
            print "No valid mode"

    while True:
        try:
            args.amount = int(raw_input("Anzahl = "))
        except ValueError:
            print "Invald input."
            continue
        if 1 < args.amount < 256:
            break
        else:
            print str(args.amount) + " invald amount"
            print "Bitte neu eingeben!"

    while True:
        try:
            args.product = str(raw_input("Product = "))
        except ValueError:
            print "Invald input."
            continue
        if 1 < len(args.product) <  256:
            break
        else:
            print str(args.product) + " invald String"
            print "Bitte neu eingeben!"
    return args

def open_fridge(fridge, argv):

    if argv.add:
        result = fridge.add(argv.product, argv.amount)
        print str(argv.amount) + " " + argv.product + " hinzugefuegt"
    elif argv.sub:
        result = fridge.sub(argv.product, argv.amount)
        if result >= 0:
            print str(argv.amount) + " " + argv.product + " herausgenommen"
            if result == 0:
                print "Fridge ist leer!"
        else:
            print "Fehler beim herrausnehmen der Ware."
            if result == -1:
                print "Ware noch nicht vorhanden oder"
            print str(abs(result)) + " " + argv.product + " zu wenig vorhanden!"
            sys.exit(os.EX_UNAVAILABLE)

    print str(fridge.JsonContent[argv.product]) + " " + argv.product + " verbleiben"

def main(args):
    fridge = store()
    fridge.LoadJson("fridge.json")

    if len(args) <= 1:
        argv = interactiv()
    elif len(args) > 6:
        print "too many arguments"
        sys.exit(os.EX_DATAERR)
    else:
        argv = args_parser(args[1:])

    if argv.list:
        fridge.show()
    elif argv.sub or argv.add:
        open_fridge(fridge, argv)

    fridge.SaveJson("fridge.json")
    sys.exit(os.EX_OK)

if __name__ == '__main__':
    sys.exit(main(sys.argv))
