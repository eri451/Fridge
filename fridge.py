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
    
    args = args_check(agrs[1:])

    if args.list:
        show_fridge()
        return
    else:
        action  = args[1]
        amount = int(args[2])
        product = args[3]
    open_fridge(action, product, amount)

def args_check(args):

    argparser = argparse.ArgumentParser(prog='fridge', argument_default=False, description='Program to list, add or sub the fridge content.')
    argparser.add_argument('-l', '--list', action='store_true', help='List the content of the fridge')    
    argparser.add_argument('-a', '--add', action='store_true', help='Adding somee products')
    argparser.add_argument('-s', '--sub', action='store_true', help='Substitute a product.')
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
