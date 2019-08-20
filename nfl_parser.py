import requests
import json
import time

class GameScore(dict):

    def __init__(self, status, hometeam, awayteam, awayscore, homescore):
        self.hometeam = hometeam
        self.awayteam = awayteam
        self.homescore = homescore
        self.awayscore = awayscore
        self.status = status

    def toString(self):
        return "{} > {} {} - {} {}".format(self.status, self.hometeam, self.homescore, self.awayscore, self.awayteam)

def convertMillisToTime(miliseconds):
    seconds = miliseconds / 1000
    remainer, seconds = divmod((miliseconds / 1000), 60)
    remainer, minutes = divmod(remainer, 60)
    days, hours = divmod(remainer, 24)
    return seconds, minutes, hours, days

def pullNflScores():
    scoreList = []
    httpResponse = requests.get("https://feeds.nfl.com/feeds-rs/scores.json")
    nflJson = httpResponse.json()
    nflGames = nflJson['gameScores']
    currentIsoTime = int(round(time.time() * 1000))
    for game in nflGames:
        gameSchedule = game['gameSchedule']
        if game['score']:
            scoreList.append(GameScore(game['score']['phase'], gameSchedule['homeNickname'], gameSchedule['visitorNickname'], game['score']['visitorTeamScore']['pointTotal'], game['score']['homeTeamScore']['pointTotal']))
        else:
            timedeltaMillis = game['gameSchedule']['isoTime'] - currentIsoTime
            waittime = convertMillisToTime(timedeltaMillis)
            waittimeString = "{:02}d {:02}:{:02}:{:02}".format(int(waittime[3]), int(waittime[2]), int(waittime[1]), int(waittime[0]))
            scoreList.append(GameScore("UPCOMING", gameSchedule['homeNickname'], gameSchedule['visitorNickname'], 0, 0))
            #print("Game starts in "+waittimeString)

    return scoreList


def main():
    scoreList = pullNflScores()
    for score in scoreList:
        r = requests.post(url = 'http://localhost:3000/results', json = score.__dict__)
        print(r.status_code)

if __name__ == '__main__':
    main()
