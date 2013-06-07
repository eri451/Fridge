#!/usr/bin/python

import argparse
import json
import sys

fridge = {}
product = ""
action  = ""

def main(args):
    global fridge
    fridge  = load("fridge.json")
    
    argv = args_check(args[1:])

    if argv.list:
        show_fridge()
        return
#    elif argv.sub or argv.add:
#        open_fridge(action, product, amount)

def args_check(args):
    argparser = argparse.ArgumentParser(
            prog='fridge', 
            argument_default=False, 
            description='Program to list, add or sub the fridge content.'
            )
    mutually_parser = argparser.add_mutually_exclusive_group(required=True)
    mutually_parser.add_argument('-l', '--list', action='store_true', help='List the content of the fridge')

    mutually_parser.add_argument('-a', '--add',
            action='store_true',
            help='Adding somee products\
                  Require \'-p\' and \'-c\''
            )

    mutually_parser.add_argument('-s', '--sub', 
            action='store_true', 
            help='Substitute a product.\
                  Require \'-p\' and \'-c\''
            )
    
    argparser.add_argument('-p', '--product',
            type=str,
            metavar='<Productname>',
            help='Add or sub the product.\
                  Require \'-a\' or \'-s\''
            )
    argparser.add_argument('-c', '--count',
            type=int,
            metavar='<count>',
            help='Count of add or sub product.\
                  Require \'-a\' or \'-s\''
            )
    return argparser.parse_args(args)

def open_fridge(action, product, amount):
    if action == "add":
        for i in range(amount):
            add_product(product)
        print str(amount) + " " + product + " hinzugefuegt"
        save(fridge, "fridge.json")
    elif action == "sub":
        if (not(fridge.has_key(product))):
            print "erst reinlegen dann raus nehmen!!"
            return
        for i in range(amount):
            sub_product(product)
        print str(amount) + " " + product + "rausgenommen"
        print str(fridge[product]) + " " + product + "verbleiben"
        save(fridge,"fridge.json")
    else:
         print "falsche Eingabe. Bitte nutze \"show\", \"add\" oder \"sub\"."

def show_fridge():
    for product in fridge.keys():
        print "" + product + " " + str(fridge[product])


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
