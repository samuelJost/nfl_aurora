module.exports = (sequelize, DataTypes) => {
  var Score = sequelize.define('score', {
    hometeam: DataTypes.STRING,
    awayteam: DataTypes.STRING,
    homescore: DataTypes.STRING,
    awayscore: DataTypes.STRING,
    week: DataTypes.STRING,
    status: {
      type: DataTypes.ENUM,
      values: ['UPCOMING', 'LIVE', 'FINAL']
    }
  });

    return Score;
};
