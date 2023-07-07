#!/usr/bin/sh 


curl -X POST -H "Content-Type: application/json" -d '{"deck_name": "one", "question": "how many planets are there", "answer": "we dont know", "disabled": 1}' http://localhost:5000/cards/create
curl -X POST -H "Content-Type: application/json" -d '{"deck_name": "one", "question": "fawoefjawoejfaowejfaowejfoaejf", "answer": "fawjoejfawoejfaowejf", "disabled": 4}' http://localhost:5000/cards/create
curl -X POST -H "Content-Type: application/json" -d '{"deck_name": "one", "question": "aewofjaweoifjaweofjawoefj", "answer": "falwmefojawefoijaweofij", "disabled": 4}' http://localhost:5000/cards/create
curl -X POST -H "Content-Type: application/json" -d '{"deck_name": "two", "question": "fawoiejfaowijefoawejfoawjef", "answer": "lmaooooo", "disabled": 0}' http://localhost:5000/cards/create
curl -X POST -H "Content-Type: application/json" -d '{"deck_name": "four", "question": "faoijfawlejfaowejf lol", "answer": "what the fuck is this ", "disabled": 4}' http://localhost:5000/cards/create
curl -X POST -H "Content-Type: application/json" -d '{"deck_name": "five", "question": "lmaoooo", "answer": "what the fuck ", "disabled": 4}' http://localhost:5000/cards/create


