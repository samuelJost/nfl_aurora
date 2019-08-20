"use strict";
var mongoose = require('mongoose');
mongoose.set('useNewUrlParser', true);
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
  }
});

module.exports = mongoose.model('Score', ScoreSchema);
