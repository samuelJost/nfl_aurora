#!/usr/bin/env python3

import requests
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

def pull_nfl_json():
	http_response = requests.get("https://site.api.espn.com/apis/site/v2/sports/football/nfl/scoreboard")
	print("Test: "+str(http_response.status_code))
	nfl_json = http_response.json()
	return nfl_json

def normalize_status(game):
	status_type = game.get('status', {}).get('type', {})
	raw_status = status_type.get('name')
	if raw_status in ('STATUS_SCHEDULED', 'STATUS_IN_PROGRESS', 'STATUS_FINAL'):
		return raw_status

	competition_status = game.get('competitions', [{}])[0].get('status', {}).get('type', {})
	competition_raw_status = competition_status.get('name')
	if competition_raw_status in ('STATUS_SCHEDULED', 'STATUS_IN_PROGRESS', 'STATUS_FINAL'):
		return competition_raw_status

	state = status_type.get('state') or competition_status.get('state')
	completed = status_type.get('completed')
	if completed is True or state == 'post':
		return 'STATUS_FINAL'
	if state == 'pre':
		return 'STATUS_SCHEDULED'
	return 'STATUS_IN_PROGRESS'

def extract_teams_and_scores(game):
	competitors = game.get('competitions', [{}])[0].get('competitors', [])
	home_team = None
	away_team = None
	for competitor in competitors:
		if competitor.get('homeAway') == 'home':
			home_team = competitor
		elif competitor.get('homeAway') == 'away':
			away_team = competitor

	if home_team is None and len(competitors) > 0:
		home_team = competitors[0]
	if away_team is None and len(competitors) > 1:
		away_team = competitors[1]

	home_abbr = (home_team or {}).get('team', {}).get('abbreviation')
	away_abbr = (away_team or {}).get('team', {}).get('abbreviation')
	home_score = (home_team or {}).get('score', '0')
	away_score = (away_team or {}).get('score', '0')

	return home_abbr, away_abbr, home_score, away_score

def pull_nfl_scores(nfl_json):
	score_list = []
	nfl_games = nfl_json['events']
	week = 'Week'+str(nfl_json['week']['number'])
	for game in nfl_games:
		status = normalize_status(game)
		hometeam, awayteam, homescore, awayscore = extract_teams_and_scores(game)
		if status == 'STATUS_SCHEDULED':
			print(game.get('status', {}).get('type', {}).get('shortDetail'))
			game_time_as_date = dateutil.parser.parse(game['date'])
			timedelta_millis = game_time_as_date - datetime.datetime.now(pytz.timezone('Europe/Zurich'))
			print(game_time_as_date)
			print(timedelta_millis)
			waittime = convert_millis_to_time(timedelta_millis.total_seconds() * 1000)
			waittime_string = "{:02}d {:02}:{:02}:{:02}".format(int(waittime[3]), int(waittime[2]), int(waittime[1]), int(waittime[0]))
			score_list.append(GameScore(week, status, hometeam, awayteam, homescore, awayscore))
			print("Game starts in "+waittime_string)
		else:
			score_list.append(GameScore(week, status, hometeam, awayteam, homescore, awayscore))

	for score in score_list:
		print(score.toString)

	return score_list

def delete_old_games(nfl_json):
	actual_week = 'Week'+str(nfl_json['week']['number'])
	r = requests.delete(url = 'http://localhost:3000/score', params = {'actualWeek':actual_week})
	print(r.text)

def convert_millis_to_time(miliseconds):
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
	nfl_json = pull_nfl_json()
	print("pulled games")
	score_list = pull_nfl_scores(nfl_json)
	print("created List of scores")
	for score in score_list:
		print("send "+score.toString())
		requests.post(url = 'http://localhost:3000/score', json = score.__dict__)

@click.command()
def clean_games():
	nfl_json = pull_nfl_json()
	delete_old_games(nfl_json)

menu.add_command(pull_games)
menu.add_command(clean_games)

if __name__ == '__main__':
	menu()
