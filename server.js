var express = require('express'),
	ejs = require('ejs'),
	fs = require('fs'),
	bodyParser = require('body-parser'),
	request = require('request'),
	uuid = require('uuid');
port = process.env.PORT || 3000,
	app = express();

const API_KEY = "b94b9a266d7546ef91e64be1380960c9";

app.engine('html', ejs.renderFile);
app.set('views', __dirname + '/views');
app.use(express.static('public'));

app.use(bodyParser.json({
	limit: '50mb'
}));

app.use(bodyParser.urlencoded({
	extended: false,
	limit: '50mb'
}));

app.get('/', function(req, res) {
	res.render('index.html');
});

app.post('/upload', function(req, res) {
	console.log(req.file.image.originalFilename);
	console.log(req.file.image.path);

	fs.readFile(req.files.image.path, function(err, data) {
		var newPath = __dirname + '/uploads/' + req.files.image.originalFilename;
		fs.writeFile(newPath, data, function(err) {
			if (err) {
				res.json({
					'response': 'error'
				});
			} else {
				res.json({
					'response': 'success'
				});
			}
		});
	});
});

app.post('/web-upload', function(req, res) {
	// take the base64 string and save it as an image
	var data = req.body.image.replace(/^data:image\/\w+;base64,/, ''),
		buffer = new Buffer(data, 'base64'),
		id = uuid.v1();

	// save the image
	fs.writeFile(__dirname + '/uploads/' + id, buffer);

	res.end(id);
});

app.get('/upload/:file', function(req, res) {
	file = req.params.file;
	var img = fs.readFileSync(__dirname + "/uploads/" + file);
	res.writeHead(200, {
		'Content-Type': 'image/jpg'
	});
	res.end(img, 'binary');
});

app.post('/emotipic', function(req, res) {
	console.log(req.body.id);
	var url = req.protocol + '://' + req.get('host') + '/upload/' + req.body.id;
	request({
		headers: {
			'Content-Type': 'application/json',
			'Ocp-Apim-Subscription-Key': API_KEY
		},
		uri: 'https://api.projectoxford.ai/emotion/v1.0/recognize',
		json: {
			url: url
		},
		method: 'POST'
	}, function(err, response, body) {
		if (err) {
			console.log(err);
		} else {
			res.send(body);
		}
	});
});

var server = app.listen(port, function() {
	var host = server.address().address,
		port = server.address().port;

	console.log('Listening at http://%s:%s', host, port);
});