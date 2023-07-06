#!/usr/bin/python3 

import os 
import sys
import sqlite3
import logging
from flask import Flask 
from markupsafe import escape 

# IMPORTANT GLOBALS 
VERBOSE = os.getenv("MONR_VERBOSE")     # environment variable which enables the verbose mode 
REINIT_DB = os.getenv("MONR_REINIT")    # environment variable which forces a reinitialization of the database at start

flask_app= Flask(__name__)
db_con = sqlite3.connect("resources.db") 
db_cur = db_con.cursor()

# USER GLOBALS
tables = ["cards", "decks"]

# API: root and health status
@flask_app.route("/")
def root(): 
     return "MONR IS UP AND RUNNING"

# API: return decks 
# API: create deck
# API: delete deck
# API: return cards
# API: fetch cards
# API: create cards
# API: delete cards
# API: move cards
# API: activate cards
# API: activate cards

# check to see if the database has been already initialized 
def is_initialized_database(): 
     for table in tables:
          db_cur.execute("SELECT name FROM sqlite_master WHERE type='table' AND name=?;", (table,))
          result = db_cur.fetchone()
          
          if not result: 
               return False    
         
     return True
     
# function to initialize the database 
def initialize_database():
     logging.debug("Initializing the database")

     db_cur.execute('''
          CREATE TABLE decks (
               id INTEGER PRIMARY KEY AUTOINCREMENT,
               name TEXT NOT NULL
          )
     ''')

     db_con.commit()
     
     db_cur.execute('''
          CREATE TABLE cards (
               id INTEGER PRIMARY KEY AUTOINCREMENT,
               deck_id INTEGER NOT NULL,
               state INTEGER NOT NULL,
               question TEXT NOT NULL, 
               answer TEXT NOT NULL,
               FOREIGN KEY (deck_id) REFERENCES decks (id) ON DELETE CASCADE
          )
     ''') 
     
     db_con.commit()

def init():
     if VERBOSE:
          logging.basicConfig(level=logging.DEBUG)
         
     logging.debug("Starting up the server")
     if not is_initialized_database() or REINIT_DB:
          initialize_database()
     
init()
