'use strict';
var models = require('../models');
const Sequelize = require('sequelize');
const path = require('path');
const { execFile } = require('child_process');
const Op = Sequelize.Op;
const scriptPath = path.resolve(__dirname, '../../set_effect_on_nanoleaf.py');

function runScoreUpdateScript(team) {
  return new Promise((resolve, reject) => {
    execFile('python3', [scriptPath, team], (err, stdout, stderr) => {
      if (stdout) {
        console.log(stdout.trim());
      }
      if (stderr) {
        console.error(stderr.trim());
      }
      if (err) {
        reject(err);
        return;
      }
      resolve();
    });
  });
}

exports.list_all_games = function(req, res){
  console.log('Get Request incoming: List all Games');
  models.score.findAll().then(function(score){
    res.json(score);
  });
};

exports.clean_old_games = function(req, res){
  console.log("Clean all games that finished.");
  models.score.destroy({
    where: {
      status: {
            [Op.eq]: 'STATUS_FINAL'
      }
    }
  })
  .then( result => res.sendStatus('200'))
  .catch( err => res.send(err));
};

exports.add_game = function(req, res){
  console.log('Post Request to add Game');
  var newScore = req.body;
  console.log(newScore);
  models.score.findOrCreate({where: {hometeam: newScore.hometeam, awayteam: newScore.awayteam}})
  .then(([score, created]) => {
    const scoreToInsert = score;
    const homeScoreChanged = !created && scoreToInsert.homescore !== newScore.homescore;
    const awayScoreChanged = !created && scoreToInsert.awayscore !== newScore.awayscore;
    const changedTeams = [];

    if (homeScoreChanged) {
      changedTeams.push(newScore.hometeam);
    }
    if (awayScoreChanged) {
      changedTeams.push(newScore.awayteam);
    }

    console.log("Testing homescore:" + newScore.homescore+"     "+scoreToInsert.id);
    return models.score.update(
      {
        homescore: newScore.homescore,
        awayscore: newScore.awayscore,
        status: newScore.status,
        week: newScore.week
      },
      {
        where: {id: scoreToInsert.id}
      }
    )
    .then(result => {
      console.log('Update result:', result);
      if (changedTeams.length === 0) {
        res.json(newScore);
        return null;
      }

      return changedTeams.reduce((promise, team) => {
        return promise.then(() => runScoreUpdateScript(team));
      }, Promise.resolve()).then(() => {
        res.json(newScore);
        return null;
      });
    });
  })
  .catch(err => {
    console.error('Update error:', err);
    res.status(500).send(err);
  });
};
