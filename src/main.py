#!/usr/bin/python3 

import os 
import sys
import sqlite3
import logging
from datetime import datetime, timedelta
from flask import Flask 
from flask import g 
from flask import request 
from markupsafe import escape 

from scheduler import *

# IMPORTANT GLOBALS 
VERBOSE = os.getenv("MONR_VERBOSE")     # environment variable which enables the verbose mode 
REINIT_DB = os.getenv("MONR_REINIT")    # environment variable which forces a reinitialization of the database at start

flask_app= Flask(__name__)
database_location = "/tmp/resources.db"

# USER GLOBALS
tables = ["cards", "decks"]

# IMPORTANT FUNCTIONS 
def get_db(): 
     db_con = getattr(g, "_database", None)
     if db_con is None: 
          db_con = g._database = sqlite3.connect(database_location)
     return db_con

# API: root and health status
@flask_app.route("/")
def root(): 
     return "MONR IS UP AND RUNNING"

# API: return decks 
@flask_app.route("/decks/return", methods=["GET"])
def return_decks(): 
     db_con = get_db()
     db_cur = db_con.cursor()
     output = ""
     
     try:
          db_cur.execute("SELECT * FROM decks;")
          output = db_cur.fetchall()
     except sqlite3.Error:
          return "Error fetching data from the database", 500
     except Exception: 
          return "Request invalid", 500
     return output, 200


# API: create deck
@flask_app.route("/decks/create", methods=["POST"])
def create_decks():
     db_con = get_db()
     db_cur = db_con.cursor()
    
     try: 
          data = request.json
          deck_name = data["deck"]
          
          db_cur.execute("INSERT INTO decks (name) VALUES (?);", (deck_name,))  
          db_con.commit()
     except sqlite3.Error: 
          return "Error inserting the deck into the database", 500
     except Exception:
          return "Request invalid", 500
     return "success", 200
     
     
# API: delete deck
@flask_app.route("/decks/delete", methods=["POST"])
def delete_decks(): 
     db_con = get_db() 
     db_cur = db_con.cursor()
     
     try: 
          data = request.json 
          decks = data["deck"]
          
          if (type(decks) is not list):
               decks = [decks]
         
          for deck in decks: 
               db_cur.execute("DELETE FROM decks WHERE name=?;", (deck,))
               db_con.commit()
     except sqlite3.Error:
          return "Error deleting the deck from the database", 500
     except Exception:
          return "Request invalid", 500
     return "success", 200


# API: return cards
@flask_app.route("/cards/return", methods=["GET"])
def return_cards(): 
     db_con = get_db()
     db_cur = db_con.cursor()
     output = ""
     
     try: 
          data = request.json
          deck = data["deck"]
          
          db_cur.execute('''
               SELECT cards.*
               FROM cards
               JOIN decks ON cards.deck_id = decks.id 
               WHERE decks.name=?;
          ''', (deck,)) 
          output = db_cur.fetchall()
     except sqlite3.Error:
          return "Error fetching cards from given deck", 500 
     except Exception:
          return "Request invalid", 500
     return output, 200


# API: fetch cards
@flask_app.route("/cards/fetch", methods=["POST"])
def fetch_cards(): 
     db_con = get_db()  
     db_cur = db_con.cursor()
     output = ""
     json_output = []
     
     try: 
          data = request.json
          query = "SELECT * FROM cards WHERE 1=1 "
          params = []

          if "deck" in data:
               deck_name = data["deck"]
               db_cur.execute("SELECT id FROM decks WHERE name=?;", (deck_name,))
               deck_id = db_cur.fetchone()[0]
               params.append(deck_id)
               query += "AND deck_id=? "
          if "state" in data:
               state_filter = data["state"]
               params.append(state_filter)
               query += "AND state=? "
          if "disabled" in data: 
               disabled_filter = data["disabled"]
               params.append(disabled_filter)
               query += "AND disabled=? "
          if "ef_max" in data and "ef_min" in data:
               ef_min = data["ef_min"]
               ef_max = data["ef_max"]
               params.append(ef_min)
               params.append(ef_max)
               query += "AND ef_number BETWEEN ? AND ? "
          if "interval_date" in data:
               interval_date = datetime.strptime(data["interval_date"], "%Y-%m-%d").date()
               interval_date = interval_date + timedelta(days=1)
               params.append(interval_date)
               query += "AND interval_date <= ? "
          if "repetitions" in data: 
               repetitions = data["repetitions"]
               params.append(repetitions)
               query += "AND repetitions = ? "
          if "question" in data: 
               question = data["question"] 
               params.append(question)
               query += "AND question LIKE ? "
          if "answer" in data:
               answer = data["answer"]
               params.append(answer)
               query += "AND answer LIKE ? "
          
          db_cur.execute(query, params)
          output = db_cur.fetchall()
          output_columns = [desc[0] for desc in db_cur.description]

          # convert the sqlite output into an easy-to-read json structure
          for output_entry in output: 
               tmp_json_output = {}
               for c_index, column in enumerate(output_columns):
                    tmp_json_output[column] = output_entry[c_index]
               json_output.append(tmp_json_output)
     except sqlite3.Error:
          return "Error fetching cards with given parameters", 500 
     except Exception as e:
          print(e)
          return "Request invalid", 500
     return json_output, 200

# API: create cards
@flask_app.route("/cards/create", methods=["POST"])
def create_cards():
     db_con = get_db()
     db_cur = db_con.cursor()
     
     try: 
          data = request.json 
          deck_name = data["deck"]
          disabled = data.get("disabled", 1)
          if disabled != 0: 
               disabled = 1
          question = data["question"]
          answer = data["answer"]
          
          db_cur.execute("SELECT id FROM decks WHERE name=?;", (deck_name,)) 
          deck_id = db_cur.fetchone()[0]

          new_easiness_factor = 2.5
          new_repetitions = 0
          new_date_interval, new_number_interval = calculate_interval(0, new_repetitions, 2.5)
          
          db_cur.execute('''
               INSERT INTO cards 
               (deck_id, disabled, state, interval_date, interval_number, ef_number, repetitions, question, answer)
               VALUES 
               (?, ?, ?, ?, ?, ?, ?, ?, ?)
          ''', (deck_id, disabled, 0, new_date_interval, new_number_interval, new_easiness_factor, new_repetitions, question, answer)) 
          db_con.commit()
     except sqlite3.Error as er:
          print(er)
          return "Error inserting card into the database", 500     
     except Exception:
          return "Request invalid", 500
     return "success", 200

# API: learn cards
@flask_app.route("/cards/learn", methods=["POST"])
def learn_cards(): 
     db_con = get_db()
     db_cur = db_con.cursor()
     card_output = {} 
     
     try: 
          data = request.json
          card_id = data["card_id"]
          grade = data["grade"]
          
          # fetch old interval, repetitions, easiness_factor
          db_cur.execute("SELECT * FROM cards WHERE id=?", (card_id,))
          output = db_cur.fetchone()
          output_columns = [desc[0] for desc in db_cur.description]
          tmp_card_output = {}
          
          for c_index, column in enumerate(output_columns):
               tmp_card_output[column] = output[c_index] 
          
          # calculate the new interval, repetitions, easiness_factor 
          updated_schedule = calculate_schedule(tmp_card_output["interval_number"],
                                                tmp_card_output["repetitions"],
                                                tmp_card_output["ef_number"],
                                                grade)
          
          # update interval, repetitions, easiness_factor
          db_cur.execute('''UPDATE cards
                            SET interval_date=?,
                                interval_number=?,
                                ef_number=?,
                                repetitions=? WHERE id=?''', 
                         (updated_schedule["interval_date"], 
                          updated_schedule["interval_number"],
                          updated_schedule["easiness_factor"],
                          updated_schedule["repetitions"],
                          card_id,))
          db_con.commit()
               
          # set the output 
          db_cur.execute("SELECT * FROM cards WHERE id=?", (card_id,))
          output = db_cur.fetchone()
          output_columns = [desc[0] for desc in db_cur.description]
          
          for c_index, column in enumerate(output_columns):
               card_output[column] = output[c_index]
     except sqlite3.Error as e:
          print(e)
          return "Error working with card's learning state", 500
     except Exception as e:
          print(e)
          return "Request invalid", 500
     return card_output, 200

# API: delete cards
# API: move cards
# API: activate cards
# API: activate cards

# FLASK: close appcontext 
@flask_app.teardown_appcontext
def close_connection(exception): 
      db_con = getattr(g, "_database", None)
      if db_con is not None: 
           db_con.close()

# check to see if the database has been already initialized 
def is_initialized_database(con, cur): 
     for table in tables:
          cur.execute("SELECT name FROM sqlite_master WHERE type='table' AND name=?;", (table,))
          result = cur.fetchone()
          
          if not result: 
               return False    
         
     return True
     
# function to initialize the database 
def initialize_database(con, cur):
     logging.debug("Initializing the database")
     
     cur.execute('''
          CREATE TABLE decks (
               id INTEGER PRIMARY KEY AUTOINCREMENT,
               name TEXT UNIQUE NOT NULL
          );
     ''')

     con.commit()

     cur.execute('''
          CREATE TABLE cards (
               id INTEGER PRIMARY KEY AUTOINCREMENT,
               deck_id INTEGER NOT NULL,
               
               disabled INTEGER NOT NULL,
               state INTEGER NOT NULL,
               interval_date DATE NOT NULL,
               interval_number REAL NOT NULL,
               ef_number REAL NOT NULL,
               repetitions INTEGER NOT NULL,
               
               question TEXT NOT NULL, 
               answer TEXT NOT NULL,
               
               FOREIGN KEY (deck_id) REFERENCES decks (id) ON DELETE CASCADE
          );
     ''')

     con.commit()

def init():
     if VERBOSE:
          logging.basicConfig(level=logging.DEBUG)
     if REINIT_DB and os.path.exists(database_location): 
          os.remove(database_location) 
         
     db_con = sqlite3.connect(database_location)
     db_cur = db_con.cursor()

     logging.debug("Starting up the server")
     if not is_initialized_database(db_con, db_cur) or REINIT_DB:
          initialize_database(db_con, db_cur)
     
init()
