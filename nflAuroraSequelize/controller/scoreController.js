'use strict';
var models = require('../models');
const Sequelize = require('sequelize');
const Op = Sequelize.Op;

exports.list_all_games = function(req, res){
  console.log('Get Request incoming: List all Games');
  models.score.findAll().then(function(score){
    res.json(score);
  });
};

exports.clean_old_games = function(req, res){
  console.log("Clean all games that are not from the current week " + req.query.actualWeek);
  models.score.destroy({
    where: {
      week: {
        [Op.ne]: req.query.actualWeek
      }
    }
  })
  .then( result => res.sendStatus('200'))
  .catch( err => res.send(err));
};

exports.add_game = function(req, res){
  console.log('Post Request to add Game');
  var newScore = req.body;
  models.score.findOrCreate({where: {hometeam: newScore.hometeam, awayteam: newScore.awayteam}})
  .then(([score, created]) => {
    const scoreToInsert = score;
    console.log(newScore.homescore+"     "+scoreToInsert.id);
    models.score.update(
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
    .then (result => res.json(newScore))
    .catch( err => res.send(err));
  })
  .catch( err => res.send(err));
};
