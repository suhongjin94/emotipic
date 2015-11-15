var express = require('express'),
	ejs = require('ejs'),
	fs = require('fs'),
	bodyParser = require('body-parser'),
	request = require('request'),
	multer = require('multer'),
	uuid = require('uuid'),
	port = process.env.PORT || 3000,
	pythonShell = require('python-shell'),
	app = express();

const FACE_API_KEY = "3014f0d696a144d4bd875661e36057c3";
const EMOTION_API_KEY = "b94b9a266d7546ef91e64be1380960c9";

app.engine('html', ejs.renderFile);
app.set('views', __dirname + '/views');
app.use(express.static('public'));
app.use(multer({
	dest: 'uploads/'
}).single('image'));

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

app.post('/upload', function(req, response) {
	var fileName = req.file.filename,
		url = req.protocol + '://' + req.get('host') + '/upload/' + fileName;

	request({
		headers: {
			'Content-Type': 'application/json',
			'Ocp-Apim-Subscription-Key': FACE_API_KEY
		},
		uri: 'https://api.projectoxford.ai/face/v0/detections?analyzesFaceLandmarks=true',
		json: {
			url: url
		},
		method: 'POST'
	}, function(err, res, faceBody) {
		if (err) {
			response.send({
				'response': 'error'
			});
		} else {
			request({
				headers: {
					'Content-Type': 'application/json',
					'Ocp-Apim-Subscription-Key': EMOTION_API_KEY
				},
				uri: 'https://api.projectoxford.ai/emotion/v1.0/recognize',
				json: {
					url: url
				},
				method: 'POST'
			}, function(err, res, emotionBody) {
				if (err) {
					response.send({
						'response': 'error'
					});
				} else {
					pythonShell.run('sample.py', {
						args: [JSON.stringify({
								'response': {
									face: faceBody,
									emotion: emotionBody
								}
							}),
							'input.png',
							'output.png'
						]
					}, function(err, result) {
						if (err) {
							console.log(err);
						}

						console.log(result);
					});

					response.send({
						'response': {
							face: faceBody,
							emotion: emotionBody
						}
					});
				}
			});
		}
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

var server = app.listen(port, function() {
	var host = server.address().address,
		port = server.address().port;

	console.log('Listening at http://%s:%s', host, port);
});