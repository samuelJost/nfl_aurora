'use strict';
module.exports = function(app){
  var resultList = require('../controllers/resultController');
  app.route('/results')
    .get(resultList.list_all_games)
    .post(resultList.add_game)
    .delete(resultList.clean_old_games);
}
