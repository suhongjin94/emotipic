var express = require('express'),
	ejs = require('ejs'),
	fs = require('fs'),
	multer = require('multer'),
	bodyParser = require('body-parser'),
	request = require('request'),
	port = process.env.PORT || 3000,
	app = express();

const API_KEY = "b94b9a266d7546ef91e64be1380960c9";

app.engine('html', ejs.renderFile);
app.set('views', __dirname + '/views');
app.use(express.static('public'));
app.use(multer({
	dest: 'uploads/'
}).single('image'));
app.use(bodyParser.json({
	limit: '5mb'
}));

app.use(bodyParser.urlencoded({
	extended: false,
	limit: '5mb'
}));

app.get('/', function(req, res) {
	res.render('index.html');
});

app.post('/', function(req, res) {
	var fileName = req.file.filename;
	res.end('upload/' + fileName);
});

app.post('/upload', function(req, res) {
	console.log(req.body);
	var data = req.body.image.replace(/^data:image\/\w+;base64,/, ''),
		buffer = new Buffer(data, 'base64');
	fs.writeFile(__dirname + '/uploads/image.png', buffer);
	res.end('');
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
	var url = req.protocol + '://' + req.get('host') + '/upload/image.png';
	console.log(url);
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