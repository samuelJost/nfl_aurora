#!/usr/bin/env python3

import requests
import json
import time
import click
import datetime
import dateutil.parser
import pytz

class GameScore(dict):

	def __init__(self, week, status, hometeam, awayteam, homescore, awayscore):
		self.hometeam = hometeam
		self.awayteam = awayteam
		self.homescore = homescore
		self.awayscore = awayscore
		self.status = status
		self.week = week

	def toString(self):
		return "{}: {} > {} {} - {} {}".format(self.week, self.status, self.hometeam, self.homescore, self.awayscore, self.awayteam)

def pullNflJSON():
	httpResponse = requests.get("http://site.api.espn.com/apis/site/v2/sports/football/nfl/scoreboard")
	nflJson = httpResponse.json()
	return nflJson

def normalizeStatus(game):
	statusType = game.get('status', {}).get('type', {})
	rawStatus = statusType.get('name')
	if rawStatus in ('STATUS_SCHEDULED', 'STATUS_IN_PROGRESS', 'STATUS_FINAL'):
		return rawStatus

	competitionStatus = game.get('competitions', [{}])[0].get('status', {}).get('type', {})
	competitionRawStatus = competitionStatus.get('name')
	if competitionRawStatus in ('STATUS_SCHEDULED', 'STATUS_IN_PROGRESS', 'STATUS_FINAL'):
		return competitionRawStatus

	state = statusType.get('state') or competitionStatus.get('state')
	completed = statusType.get('completed')
	if completed is True or state == 'post':
		return 'STATUS_FINAL'
	if state == 'pre':
		return 'STATUS_SCHEDULED'
	return 'STATUS_IN_PROGRESS'

def extractTeamsAndScores(game):
	competitors = game.get('competitions', [{}])[0].get('competitors', [])
	homeTeam = None
	awayTeam = None
	for competitor in competitors:
		if competitor.get('homeAway') == 'home':
			homeTeam = competitor
		elif competitor.get('homeAway') == 'away':
			awayTeam = competitor

	if homeTeam is None and len(competitors) > 0:
		homeTeam = competitors[0]
	if awayTeam is None and len(competitors) > 1:
		awayTeam = competitors[1]

	homeAbbr = (homeTeam or {}).get('team', {}).get('abbreviation')
	awayAbbr = (awayTeam or {}).get('team', {}).get('abbreviation')
	homeScore = (homeTeam or {}).get('score', '0')
	awayScore = (awayTeam or {}).get('score', '0')

	return homeAbbr, awayAbbr, homeScore, awayScore

def pullNflScores(nflJson):
	scoreList = []
	nflGames = nflJson['events']
	week = 'Week'+str(nflJson['week']['number'])
	currentIsoTime = int(round(time.time() * 1000))
	for game in nflGames:
		status = normalizeStatus(game)
		hometeam, awayteam, homescore, awayscore = extractTeamsAndScores(game)
		if status == 'STATUS_SCHEDULED':
			print(game.get('status', {}).get('type', {}).get('shortDetail'))
			gameTimeAsDate = dateutil.parser.parse(game['date'])
			timedeltaMillis = gameTimeAsDate - datetime.datetime.now(pytz.timezone('Europe/Zurich'))
			print(gameTimeAsDate)
			print(timedeltaMillis)
			waittime = convertMillisToTime(timedeltaMillis.total_seconds() * 1000)
			waittimeString = "{:02}d {:02}:{:02}:{:02}".format(int(waittime[3]), int(waittime[2]), int(waittime[1]), int(waittime[0]))
			scoreList.append(GameScore(week, status, hometeam, awayteam, homescore, awayscore))
			print("Game starts in "+waittimeString)
		else:
			scoreList.append(GameScore(week, status, hometeam, awayteam, homescore, awayscore))

	for score in scoreList:
		print(score.toString)

	return scoreList

def deleteOldGames(nflJson):
	actualWeek = 'Week'+str(nflJson['week']['number'])
	r = requests.delete(url = 'http://localhost:3000/score', params = {'actualWeek':actualWeek})
	print(r.text)

def convertMillisToTime(miliseconds):
	print(miliseconds)
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
	print("pulling games")
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
