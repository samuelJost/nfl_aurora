var express = require('express'),
  app = express(),
  port = process.env.PORT || 3000,
  bodyParser = require('body-parser'),
  models = require('./models');

  app.use(bodyParser.urlencoded({ extended: true }));
  app.use(bodyParser.json());

  var routes = require('./app/score'); //importing route
  routes(app); //register the route
models.sequelize.sync().then(function(){
  app.listen(port);

  console.log('NFL Aurora score RESTful API server started on ' + port);
});
