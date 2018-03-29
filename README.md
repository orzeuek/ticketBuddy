# Ticket Buddy
Chatbot project who plan a trip journey through UK for you

## how to use ?

`docker-compose up`
`wget -qO-  'http://127.0.0.1:8080/?input_text={"text":"plan me a trip from London to Horsham","session_id":1234}'`

## current work progress:

- docker friendly environment available
- extracting stations
- categorizing stations as origin/destination
- dates extraction (dummy, but good enough for now)

## to-do:
- invalid stations names support:
a. populate elasticsearch with all stations index
b. add logic to Buddy which will hit elasticsearch if station name was not found 
- trip planning through traintickets.to 
