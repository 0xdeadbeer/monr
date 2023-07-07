#!/usr/bin/sh 

check=$(curl localhost:5000/decks/return)
one=$(curl -X POST -H "Content-Type: application/json" -d '{"deck_name": "one"}' http://localhost:5000/decks/create)
two=$(curl -X POST -H "Content-Type: application/json" -d '{"deck_name": "two"}' http://localhost:5000/decks/create)
three=$(curl -X POST -H "Content-Type: application/json" -d '{"deck_name": "three"}' http://localhost:5000/decks/create)
four=$(curl -X POST -H "Content-Type: application/json" -d '{"deck_name": "four"}' http://localhost:5000/decks/create)
five=$(curl -X POST -H "Content-Type: application/json" -d '{"deck_name": "five"}' http://localhost:5000/decks/create)

echo $check
echo $one
echo $two
echo $three
echo $four
echo $five

check=$(curl localhost:5000/decks/return)

echo $check
