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
- invalid stations names support, try to implement fallback strategy like:
    1. keywords matching
    2. free-text search based on unigram tagger (testing right now - seems to have problems with "to")
       use free-text search to find best match in elastic-search and suggest it to user.
       The problem is that unigram tagger need well tagged sentence. Default nltk.pos_tag
       have problem with unknown stations. "to" is quite often used with verbs (VB) like
       "to travel", "to be at...", etc. Thet's why POS tagger quite often categorize "unknown stations" like
       verbs instead of noun (NN*), example:
       "I want to travel from Manchester Airport to London" categorize "London" as NNP, and UnigramTagger
       tag it as "STATION" - which is correct.
       ,but:
       "I want to travel from Manchester Airport to Zgierz" categorize "Zgierz" as verb, and UnigramTagger
       tag it as "O" (other) - because it's unknown word and most commonly "to" occur as a pre-verb token, 
       that's why "Zgierz" has been categorized as verb.
- for text "I need to be in London tomorrow" London is categorizes as origin and destination....        
- trip planning through traintickets.to
- see @todo in dates_extraction.update_state() 
