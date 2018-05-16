# Ticket Buddy
Chatbot project who plan a trip journey through UK for you

## how to use ?

`docker-compose up`
`wget -qO-  'http://127.0.0.1:8080/?input_text={"text":"plan me a trip from London to Horsham","session_id":1234}'`

## current work progress:

- docker friendly environment available
- extracting stations (keyword strategy + fallback free-text search) - BUGGED!
- categorizing stations as origin/destination
- dates extraction (dummy, but good enough for now)

## to-do: 
- free-text search for stations categorization is executed for every input 
  (which is terrible idea), there have to be implemented intention detection....
  Which mean, we have to redesign trip_planning_conversation to something more "smart". 
- for text "I need to be in London tomorrow" London is categorizes as origin and destination....        
- trip planning through traintickets.to
- see @todo in dates_extraction.update_state() 
