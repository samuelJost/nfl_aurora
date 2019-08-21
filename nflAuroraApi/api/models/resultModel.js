"use strict";
var mongoose = require('mongoose');
var Schema = mongoose.Schema;

var ScoreSchema = new Schema({
  hometeam: {
    type:String
  },
  awayteam: {
    type:String
  },
  homescore: {
    type:Number
  },
  awayscore: {
    type:Number
  },
  status: {
    type: [{
      type: String,
      enum: ['UPCOMING', 'LIVE', 'FINAL']
    }]
  },
  week: {
    type: String
  }
});

module.exports = mongoose.model('Score', ScoreSchema);
