#!/usr/bin/python

import json
import sys

fridge = {}
product = ""
action  = ""

def main(args):
    global fridge
    fridge  = load("fridge.json")
    if len(args) <= 1:
        action  = raw_input("Operator = ")
        if action == "show":
            show_fridge()
            return
        amount  = int(raw_input("Anzahl = "))
        product = raw_input("Produkt = ")
    elif args[1] == "show":
        show_fridge()
        return
    else:
        action  = args[1]
        amount = int(args[2])
        product = args[3]
    open_fridge(action, product, amount)

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