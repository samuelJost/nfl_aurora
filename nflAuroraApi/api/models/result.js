'use strict';

module.exports = (sequelize, DataTypes) => {
  var Result = sequelize.define('Result', {
    hometeam: type.STRING,
    awayteam: type.STRING,
    homescore: type.STRING,
    awayscore: type.STRING,
    week: type.STRING
    status: {
      type: type.ENUM,
      values: ['UPCOMING', 'LIVE', 'FINAL']
    });

    return Result;
};
