#!/usr/bin/sh 

curl -X POST -H "Content-Type: application/json" -d '{"deck": "japanese"}' http://localhost:5000/decks/create

curl localhost:5000/decks/return


