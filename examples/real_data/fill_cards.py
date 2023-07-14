#!/usr/bin/python3 

import os 
import sys
import json
from pprint import pprint

# global variables
server_address = "http://localhost:5000"
deck_name = "japanese"

def read_cards(f):
    output_cards = []
    file = open(f, "r")
    delimiter = '\t'
    back_delimiter = '|'
    back_space_limiter = 2

    front_index = 0
    back_index  = 2

    try: 
        for line in file:
            line_split = line.split(delimiter) 
            front_card = line_split[front_index]
            back_card = line_split[back_index]

            back_split = back_card.split(back_delimiter)
            back_card = back_split[0]
            back_card = back_card.strip()

            if (back_card.count(' ') > back_space_limiter):
                continue
                
            output_cards.append([front_card, back_card])
    except Exception: 
        pass
        
    return output_cards

def main():
    cards = read_cards("Mining.txt")

    for card in cards: 
        json_data = {
            "deck": deck_name,
            "disabled": 0,
            "question": card[0],
            "answer": card[1],
        }
        json_string = json.dumps(json_data)
        command = f"curl -X POST -H 'Content-Type: application/json' -d '{json_string}' {server_address}/cards/create"

        print(f"Going to execute the following -> {command}")
        os.system(command) # time to execute boiiiiiiiiiiiiiiiiiiiiiii
        # you know the server is gonna crash right now oh fuckkkkkkkkkkk



if __name__ == "__main__":
    main()
