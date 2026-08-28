module.exports = (sequelize, DataTypes) => {
  var Score = sequelize.define('score', {
    hometeam: DataTypes.STRING,
    awayteam: DataTypes.STRING,
    homescore: DataTypes.STRING,
    awayscore: DataTypes.STRING,
    week: DataTypes.STRING,
    status: {
      type: DataTypes.ENUM,
        values: ['STATUS_SCHEDULED', 'STATUS_IN_PROGRESS', 'STATUS_FINAL']
    }
  });

    return Score;
};
