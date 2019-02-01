import requests
import json
import time

def convertMillisToTime(miliseconds):
    seconds = miliseconds / 1000
    remainer, seconds = divmod((miliseconds / 1000), 60)
    remainer, minutes = divmod(remainer, 60)
    days, hours = divmod(remainer, 24)
    return seconds, minutes, hours, days

httpResponse = requests.get("https://feeds.nfl.com/feeds-rs/scores.json")
nflJson = httpResponse.json()
nflGames = nflJson['gameScores']
currentIsoTime = int(round(time.time() * 1000))
for game in nflGames:
    gameSchedule = game['gameSchedule']
    print(gameSchedule['gameType']+": "+gameSchedule['visitorDisplayName']+" @ "+gameSchedule['homeDisplayName'])
    if game['score']:
        print("Game already started, score is:"+"{}{}".format(game['score']['visitorTeamScore']['pointTotal'], game['score']['homeTeamScore']['pointTotal']))
    else:
        timedeltaMillis = game['gameSchedule']['isoTime'] - currentIsoTime
        waittime = convertMillisToTime(timedeltaMillis)
        waittimeString = "{:02}d {:02}:{:02}:{:02}".format(int(waittime[3]), int(waittime[2]), int(waittime[1]), int(waittime[0]))
        print("Game starts in "+waittimeString)
