'use strict';
var mongoose = require('mongoose'),
 Score = mongoose.model('Score');

exports.list_all_games = function(req, res){
  console.log('Get Request incoming: List all Games');
  Score.find({}, function(err, score){
    if(err)
      res.send(err);
    res.json(score);
  });
};

exports.clean_old_games = function(req, res){
  console.log("Clean all games that are not from the current week " + req.query.actualWeek);
  Score.deleteMany({week: {$ne: req.query.actualWeek}}, function(err, result){
    if(err)
      res.send(err);
    res.send(result);
  });
};

exports.add_game = function(req, res){
  console.log('Post Request to add Game');
  var newScore = req.body;
  Score.findOneAndUpdate(
    {
      hometeam:newScore.hometeam,
      awayteam:newScore.awayteam
    }, newScore, {upsert:true}, function(err, score) {
      if(score){
        if(newScore.homescore + newScore.awayscore != score.homescore + score.awayscore){
          console.log("was updated");
          //Send Request to Nanoleaf
          console.log(score.hometeam+": +"+(newScore.homescore - score.homescore));
          console.log(score.awayteam+": +"+(newScore.awayscore - score.awayscore));
        }
      }
      res.json(newScore);
    });
};
