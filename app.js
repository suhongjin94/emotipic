var express = require('express'),
	ejs = require('ejs'),
	fs = require('fs'),
	multer = require('multer'),
	app = express();

const API_KEY = "b94b9a266d7546ef91e64be1380960c9";

app.engine('html', ejs.renderFile);
app.set('views', __dirname + '/views');
app.use(express.static('public'));
app.use(multer({ dest: 'uploads/'}).single('image'));

app.get('/', function(req, res) {
	res.render('index.html');
});

app.post('/', function(req, res) {
	console.log(req.body);
	console.log(req.files);
	res.status(204).end();
});

app.get('/upload/:file', function(req, res) {
	file = req.params.file;
	var img = fs.readFileSync(__dirname + "/uploads/" + file);
	res.writeHead(200, {
		'Content-Type': 'image/jpg'
	});
	res.end(img, 'binary');
});

var server = app.listen(3000, function() {
	var host = server.address().address,
		port = server.address().port;

	console.log('Listening at http://%s:%s', host, port);
});