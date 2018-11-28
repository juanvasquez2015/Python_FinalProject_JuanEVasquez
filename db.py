import sys
import os
import sqlite3
from contextlib import closing

from objects import Store
from objects import Item

conn = None

def connect():
    global conn
    if not conn:
        if sys.platform == "win32":
            DB_FILE = "C:\python_\_db\ShoppingList.sqlite"
#        else:
#            HOME = os.environ["HOME"]
#            DB_FILE = HOME + "/Documents/murach/python/_db/movies.sqlite"
        
        conn = sqlite3.connect(DB_FILE)
        conn.row_factory = sqlite3.Row

def close():
    if conn:
        conn.close()

def make_store(row):
    return Store(row["StoreID"], row["StoreName"])

def make_item(row):
    return Item(row["ItemID"], row["name"], row["types"], row["cost"],
            make_store(row))

def get_stores():
    query = '''SELECT storeID, name as storeName
               FROM Store'''
    with closing(conn.cursor()) as c:
        c.execute(query)
        results = c.fetchall()

    stores = []
    for row in results:
        stores.append(make_store(row))
    return stores

def get_store(store_id):
    query = '''SELECT storeID, name AS storeName
               FROM Store WHERE storeID = ?'''
    with closing(conn.cursor()) as c:
        c.execute(query, (store_id,))
        row = c.fetchone()

    store = make_store(row)
    return store

def get_items_by_store(store_id):
    query = '''SELECT itemID, Item.name, types, cost,
                      Item.storeID as storeID,
                      Store.name as StoreName
               FROM Item JOIN Store
                      ON Item.storeID = Store.storeID
               WHERE Item.storeID = ?'''
    with closing(conn.cursor()) as c:
        c.execute(query, (store_id,))
        results = c.fetchall()

    items = []
    for row in results:
        items.append(make_item(row))
    return items

def get_items_by_types(types):
    query = '''SELECT itemID, Item.name, types, cost,
                      Item.storeID as storeID,
                      Store.name as StoreName
               FROM Item JOIN Store
                      ON Item.storeID = Store.storeID
               WHERE types = ?'''
    with closing(conn.cursor()) as c:
        c.execute(query, (types,))
        results = c.fetchall()

    items = []
    for row in results:
        items.append(make_item(row))
    return items

def get_items_by_cost(max_cost):
    query = '''SELECT itemID, Item.name, types, cost,
                      Item.storeID as storeID,
                      Store.name as storeName
               FROM Item JOIN Store
                      ON Item.storeID = Store.storeID
               WHERE cost < ?
               ORDER BY cost ASC'''
    with closing(conn.cursor()) as c:
        c.execute(query, (max_cost,))
        results = c.fetchall()

    items = []
    for row in results:
        items.append(make_item(row))
    return items

def get_item(item_id):
    query = '''SELECT itemID, Item.name, types, cost,
                      Item.storeID as storeID,
                      Store.name as storeName
               FROM Item JOIN Store
                      ON Item.storeID = Store.storeID
               WHERE itemID = ?'''
    with closing(conn.cursor()) as c:
        c.execute(query, (item_id,))
        row = c.fetchone()

    item = make_item(row)
    return item

def add_item(item):
    sql = '''INSERT INTO Item (storeID, name, types, cost) 
             VALUES (?, ?, ?, ?)'''
    with closing(conn.cursor()) as c:
        c.execute(sql, (item.store.id, item.name, item.types,
                        item.cost))
        conn.commit()

def delete_item(item_id):
    sql = '''DELETE FROM Item WHERE itemID = ?'''
    with closing(conn.cursor()) as c:
        c.execute(sql, (item_id,))
        conn.commit()

###This Function should exit the program and display all the items in the queue
###All items should show Item ID, Name, Store, Type, and Cost
###Following this should be a cost total adding all costs together
def cashout(out):
    query = '''SELECT itemID, Item.name, types, cost,
                      Item.storeID as storeID,
                      Store.name as StoreName
               FROM Item JOIN Store
                      ON Item.storeID = Store.storeID
               WHERE out = ?'''
    with closing(conn.cursor()) as c:
        c.execute(query, (out,))
        results = c.fetchall()

    items = []
    for row in results:
        items.append(make_item(row))
    return items

    with closing(conn.cursor()) as p:
        p.execute('''SELECT cost
                     FROM Item JOIN Store
                            ON Item.storeID = Store.storeID
                     WHERE out = ?''', (out,))
        results2 = p.fetchall()

    items2 = []
    for row in results2:
        items2.append(make_item(row))
    return items2
        









