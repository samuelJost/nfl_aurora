#!/usr/bin/env python3

import requests
import json
import time
import click

class GameScore(dict):

    def __init__(self, week, status, hometeam, awayteam, awayscore, homescore):
        self.hometeam = hometeam
        self.awayteam = awayteam
        self.homescore = homescore
        self.awayscore = awayscore
        self.status = status
        self.week = week

    def toString(self):
        return "{}: {} > {} {} - {} {}".format(self.week, self.status, self.hometeam, self.homescore, self.awayscore, self.awayteam)

def pullNflJSON():
    httpResponse = requests.get("https://feeds.nfl.com/feeds-rs/scores.json")
    nflJson = httpResponse.json()
    return nflJson

def pullNflScores(nflJson):
    scoreList = []
    nflGames = nflJson['gameScores']
    week = nflJson['seasonType']+str(nflJson['week'])
    currentIsoTime = int(round(time.time() * 1000))
    for game in nflGames:
        gameSchedule = game['gameSchedule']
        if game['score']:
            scoreList.append(GameScore(week, game['score']['phase'], gameSchedule['homeNickname'], gameSchedule['visitorNickname'], game['score']['visitorTeamScore']['pointTotal'], game['score']['homeTeamScore']['pointTotal']))
        else:
            timedeltaMillis = game['gameSchedule']['isoTime'] - currentIsoTime
            waittime = convertMillisToTime(timedeltaMillis)
            waittimeString = "{:02}d {:02}:{:02}:{:02}".format(int(waittime[3]), int(waittime[2]), int(waittime[1]), int(waittime[0]))
            scoreList.append(GameScore(week, "UPCOMING", gameSchedule['homeNickname'], gameSchedule['visitorNickname'], 0, 0))
            print("Game starts in "+waittimeString)

    return scoreList

def deleteOldGames(nflJson):
    actualWeek = nflJson['seasonType']+str(nflJson['week'])
    r = requests.delete(url = 'http://localhost:3000/score', params = {'actualWeek':actualWeek})
    print(r.text)

def convertMillisToTime(miliseconds):
    seconds = miliseconds / 1000
    remainer, seconds = divmod(seconds, 60)
    remainer, minutes = divmod(remainer, 60)
    days, hours = divmod(remainer, 24)
    return seconds, minutes, hours, days

@click.group()
def menu():
    pass

@click.command()
def pull_games():
    nflJson = pullNflJSON()
    scoreList = pullNflScores(nflJson)
    for score in scoreList:
        print("send "+score.toString())
        r = requests.post(url = 'http://localhost:3000/score', json = score.__dict__)

@click.command()
def clean_games():
    nflJson = pullNflJSON()
    deleteOldGames(nflJson)

menu.add_command(pull_games)
menu.add_command(clean_games)

if __name__ == '__main__':
    menu()
