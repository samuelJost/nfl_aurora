import requests
import json
httpResponse = requests.get("https://feeds.nfl.com/feeds-rs/scores.json")
nflJson = httpResponse.json()
nflGames = nflJson['gameScores']
for game in nflGames:
    #if game['score']:
        gameSchedule = game['gameSchedule']
        print(gameSchedule['gameType']+": "+gameSchedule['visitorDisplayName']+" @ "+gameSchedule['homeDisplayName'])
