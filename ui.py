#!/usr/bin/env/python3

import db
from objects import Item

def display_title():
    print("The Grocerie List program")
    print()    
    display_menu()

def display_menu():
    print("COMMAND MENU")
    print("store  - View items by store")
    print("type - View items by type")
    print("cost  - View items by cost")
    print("add  - Add an item")
    print("del  - Delete an item")
    print("out  - Display total")
    print("exit - Exit program")
    print()    

def display_stores():
    print("STORES")
    stores = db.get_stores()    
    for store in stores:
        print(str(store.id) + ". " + store.name)
    print()

def display_items(items, store_name):
    print("ITEMS - " + store_name)
    line_format = "{:3s} {:37s} {:10s} {:9s} {:10s}"
    print(line_format.format("ID", "Name", "Types", "Cost $USD", "Store"))
    print("-" * 80)
    for item in items:
        print(line_format.format(str(item.id), item.name,
                                 item.types, str(item.cost),
                                 item.store.name))
    print()

def display_items_by_store():
    store_id = int(input("Store ID: "))
    store = db.get_store(store_id)
    if store == None:
        print("There is no store with that ID.\n")
    else:
        print()
        items = db.get_items_by_store(store_id)
        display_items(items, store.name.upper())
        
def display_items_by_types():
    print("Types: \n",
          "vegetables\n", "hygiene\n", "fruit\n", "misc\n"
          " grains\n", "meat\n", "junk food\n")
    types = input("Type (please type full name lower case only): ")
    print()
    items = db.get_items_by_types(types)
    display_items(items, types)

def display_items_by_cost():
    max_cost = int(input("Maximum number of cost (please round to whole numbers do not include decimals): "))
    print()
    items = db.get_items_by_cost(max_cost)
    display_items(items, "LESS THAN " + str(max_cost) + " cost")

def add_item():
    name        = input("Name: ")
    types        = input("Type: ")
    cost     = int(input("Cost (cost cannot include cents): "))
    store_id = int(input("Store ID: "))
    
    store = db.get_store(store_id)
    if store == None:
        print("There is no category with that ID. Movie NOT added.\n")
    else:        
        item = Item(name=name, types=types, cost=cost, store=store)
        db.add_item(item)    
        print(name + " was added to database.\n")

def delete_item():
    item_id = int(input("Item ID: "))
    item = db.get_item(item_id)
    choice = input("Are you sure you want to delete '" + 
                   item.name + "'? (y/n): ")
    if choice == "y":
        db.delete_item(item_id)
        print("'" + item.name + "' was deleted from database.\n")
    else:
        print("'" + item.name + "' was NOT deleted from database.\n")        
        
def cashout():
    out = input("Are you sure you are ready to cash out? (Type out if ready): ")
    print()
    items = db.cashout(out)
    display_items(items, out)

    
def main():
    db.connect()
    display_title()
    display_stores()
    while True:        
        command = input("Command: ")
        if command == "store":
            display_items_by_store()
        elif command == "type":
            display_items_by_types()
        elif command == "cost":
            display_items_by_cost()
        elif command == "add":
            add_item()
        elif command == "del":
            delete_item()
        elif command == "out":
            cashout()
        elif command == "exit":
            break
        else:
            print("Not a valid command. Please try again.\n")
            display_menu()
    db.close()
    print("Bye!")

if __name__ == "__main__":
    main()
