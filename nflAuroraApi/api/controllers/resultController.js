'use strict';
var mongoose = require('mongoose'),
 Score = mongoose.model('Score');

exports.list_all_games = function(req, res){
  console.log('Get Request incoming: List all Games');
  Score.find({}, function(err, score){
    if(err)
      res.send(err);

    console.log(score);
    res.json(score);
  });
};

exports.add_game = function(req, res){
  console.log('Post Request to add Game');
  var newScore = new Score(req.body);
  Score.findOneAndUpdate(
    {
      hometeam:req.body.hometeam,
      awayteam:req.body.awayteam
    }, req.body, {upsert:true}, function(err, score) {
      if(score){
        if(req.body.homescore + req.body.awayscore != score.homescore + score.awayscore){
          console.log("was updated");
          //Send Request to Nanoleaf
        }

        console.log(score.hometeam+": +"+(req.body.homescore - score.homescore));
        console.log(score.awayteam+": +"+(req.body.awayscore - score.awayscore));

      } else {
        console.log("new game");
        newScore.save(function(err, score){
          if(err)
            res.send(err);
        });
      }
      res.json(newScore);
    });
};
