"use strict";
class GameScore{

  constructor(scoreJSON){
    this._hTeam = scoreJSON.hometeam;
    this._aTeam = scoreJSON.awayteam;
    this._hScore = scoreJSON.homescore;
    this._aScore = scoreJSON.awayscore;
    this._status = scoreJSON.status;
  }
  get hometeam(){
    return this._hTeam;
  }

  get awayteam(){
    return this._aTeam;
  }

  get homescore(){
    return this._hScore;
  }

  get awayscore(){
    return this._aScore;
  }

  get status(){
    return this._status;
  }

  toString(){
    return `${this._hTeam} ${this._hScore} : ${this._aScore} ${this._aTeam} Status: ${this._status}`;
  }
}


module.exports = GameScore;
