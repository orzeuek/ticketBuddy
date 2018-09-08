# NO STABLE RELEASE YET !
Project abandoned!

I couldn't find good enough data source to train model ....


# Ticket Buddy
Chatbot project who plan a trip journey through UK for you

## how to use ?

`docker-compose up`
`wget -qO-  'http://127.0.0.1:8080/?input_text={"text":"plan me a trip from London to Horsham","session_id":1234}'`

## how does it work?

### conversation flow

Whole conversation engine is encapsuled in trip_planning_conversation_graph_based package.
Idea behind that is extremely simple. We pass `state` object over graph-like structure of conversation.
Each node in our graph is a conversation step. Steps can read and write all `state` fields. 

Most important fields during "graph-walk" are: `prompt` and `step`.
`Step` define next step to take.
`Prompt` is a message which should be display to user. If `prompt` is not empty - hold graph-walk and display
`prompt` to user. Take his input and proceed with `step`.

Simple but powerful :)

### stations extraction

There are 2 strategies implemented.
1st one is simple key-word based search. If we found in text station name from
predefined list - tag those tokens as a station.


(@prototype! not in use yet!) 2nd one is free-text search. It's based at UnigramTagger. 
Idea behind that is to extract from text, tokens which seems to be station name.
It's quite hard to achieve, but if it will be use in a right step at conversation flow
I can give quite good results. Using it to extract station name from any text 
(using UnigramTagger based on PoS) is a suicide. I've tried to implement it in 
`https://wit.ai/` - it didn't handle it well so it can be quite hard to do it 
better then facebook does :D  

(@todo) Beside above strategies, there is a plan to use Elasticsearch to generate
suggestions to user if given input do not match to any of allowed stations. 
That's why we need free-text search strategy 
(extract potential station name and try to match it using Elsticsearch).     

### origin/destination extraction

Stations themselves are not useful for journey-planner. They have to be tag as
origin and destination. It's implemented in origin_destination_extraction package.  
It use NaiveBayesClassifier. As a feature set for that, there is object with 
`has_origin`, `has_destination` properties (which are quite expressive), plus
(more important) station token with 1 token before and one token after station token. 
In example: `from_STATION_to` mean that we have sentence like:

`Plan me a journey from London to Horsham`

Stations tagger, tagged `London` as a station, train set "preparator" add `from` and `to`
words, and we have simple feature set.

@todo
Keep looking for improve this solution. There might be additional features, like: 

- "station token position" (is it 1st station in sentence or 2nd, 3rd)
- "part of speach before station toke"
- any other idea which came to your mind :)    

### dates extraction

That's simple. It's done by "duckling":

https://github.com/facebook/duckling

it's pretty awesome :) Take a look at dates_extraction package for more details.
No magic there.

### compatibility

This project should be compliant with RSPS7012 (RSP Standard) - currently 
(21-06-2018) it's just a draft. One of most important paragraphs of that standard is
1.2.3 which state:
```
Retailing of rail product via the AI Voice Service Sales Channel is restricted to:
• 1 Passenger
• Adult or Child
• Railcard Discounts (max 1-person traveller, i.e. no Two Together Railcard)
• Advance Single products
• One direction of travel
```
 

## current work progress:

- docker friendly environment available
- extracting stations - only keyword based strategy
- categorizing stations as origin/destination
- dates extraction (dummy, but good enough for now)

## to-do: 
- plug in "free-text search" for stations recognition into "production code"
- keep improving origin/destination classifier
- plug in Elasticseach and implement "stations hints"
- for text "I need to be in London tomorrow" London is categorizes as origin and destination....        
- trip planning through traintickets.to
- see @todo in dates_extraction.update_state() 
- create some awesome frontend for it :) (or search for cool integration with FB messanger)
