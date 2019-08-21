var express = require('express'),
  app = express(),
  port = process.env.PORT || 3000,
  mongoose = require('mongoose'),
  Score = require('./api/models/resultModel'),
  bodyParser = require('body-parser');

  mongoose.Promise = global.Promise;
  mongoose.set('useFindAndModify', false);
  mongoose.set('useNewUrlParser', true);
  mongoose.connect('mongodb://localhost/Scoredb');


  app.use(bodyParser.urlencoded({ extended: true }));
  app.use(bodyParser.json());


  var routes = require('./api/routes/resultRoutes'); //importing route
  routes(app); //register the route

  app.listen(port);

  console.log('NFL Aurora score RESTful API server started on ' + port);
