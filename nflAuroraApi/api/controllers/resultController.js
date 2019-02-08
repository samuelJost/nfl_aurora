'use strict';
var mongoose = require('mongoose'),
 Score = mongoose.model('Score');

const GameScore = require('../models/resultModel.js');
exports.list_all_games = function(req, res){
  console.log('Get Request incoming: List all Games');
  Score.find({}, function(err, score){
    if(err)
      res.send(err);
    res.json(score);
  });
};

exports.add_game = function(req, res){
  console.log('Post Request to add Game');
  var newScore = new Score(req.body);
  newScore.save(function(err, score){
    if(err)
      res.send(err);
    res.json(score);
  });
  var newGame = new GameScore(req.body);
  console.log(newGame.toString());
  res.json({});
};
