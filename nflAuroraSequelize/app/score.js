module.exports = function(app){
  var resultList = require('../controller/scoreController');
  app.route('/score')
    .get(resultList.list_all_games)
    .post(resultList.add_game)
    .delete(resultList.clean_old_games);
}
