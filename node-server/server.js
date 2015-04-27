var express = require('express');
var app = express();
var bodyParser = require('body-parser');
var net = require('net');

// configure app to use bodyParser()
// this will let us get the data from a POST
app.use(bodyParser.urlencoded({ extended: true }));
app.use(bodyParser.json());

// serve static front-end
app.use(express.static('public'));

var port = process.env.PORT || 8080;


var router = express.Router();

router.get('/status', function(req, res) {
    // request status from Python server
    var socket = net.Socket();
    var data = '';
    
    // capture response
    socket.on('data', function(chunk) {
      data += chunk;
    });

    // connect to Python server
    socket.connect('10000');
    socket.write('status?');
        
    // parse and write out response when Python server finished sending
    socket.on('close', function() { res.json({ data: JSON.parse(data) }) });
});

router.post('/status', function(req, res) {
    var socket = net.Socket();

    var newStatus = req.body.status;
    
    var numberToTwoCharHex = function(num) {
      if(num < 0) num = 0;
      if(num > 255) num = 255;

      if(num.isNaN) throw new Error("num must be a number");

      if(num.toString(16).length == 2) {
        return num.toString(16)
      } else {
        return '0' + num.toString(16);
      }

    }

    try {
      var parsed = (JSON.parse(newStatus)).data;
      var toSend = ''; // to send to Python server

      for(var i = 0; i < 10; i++) {
        toSend += numberToTwoCharHex(parsed[i][0]) + numberToTwoCharHex(parsed[i][1]) + numberToTwoCharHex(parsed[i][2]);
      }
      
      socket.connect(10000);
      socket.write(toSend);
      socket.end();

      res.json({ status: "success" });
    } catch(e) {
      throw e;
      res.json({ status: "fail", exception: e });
    }
});

// mount routes on /api
app.use('/api', router);

app.listen(port);
console.log('Server started on port ' + port);


