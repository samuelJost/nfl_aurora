'use strict';
const GameScore = require('../models/resultModel.js');
exports.list_all_games = function(req, res){
  console.log('Get Request incoming: List all Games');
  res.json({});
};

exports.add_game = function(req, res){
  console.log('Post Request to add Game');
  var newGame = new GameScore(req.body);
  console.log(newGame.toString());
  res.json({});
};
