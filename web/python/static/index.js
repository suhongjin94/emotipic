// var capture = false,
// 	captureClick = function() {
// 		capture = true;

// 		var canvas = document.getElementById('canvas');

// 		console.log(canvas.toDataURL('image/jpeg', 1.0));

// 		$.post('/web-upload', {
// 			image: canvas.toDataURL('image/jpeg', 1.0)
// 		}, function(data) {
// 			console.log(data);
// 		}, 'json');
// 	},
// 	emotipicClick = function() {
// 		$.post('/emotion', {},
// 			function(data) {
// 				console.log(data);
// 			}, 'json');
// 	},
// 	processVideo = function() {
// 		var canvas = document.getElementById("canvas"),
// 			video = document.getElementById("video"),
// 			context = canvas.getContext('2d');

// 		if (!capture) {
// 			context.canvas.width = window.innerWidth;
// 			context.canvas.height = window.innerHeight;

// 			context.save();
// 			context.scale(-1, 1);
// 			context.drawImage(video, -context.canvas.width * 0.85, 0, context.canvas.width * 0.7, Math.floor(context.canvas.width * 768/1024 * 0.7));
// 			context.restore();
// 		}
// 	},
// 	init = function() {
// 		navigator.getUserMedia = (navigator.getUserMedia ||
// 			navigator.webkitGetUserMedia ||
// 			navigator.mozGetUserMedia ||
// 			navigator.msGetUserMedia);

// 		if (navigator.getUserMedia) {
// 			navigator.getUserMedia({
// 					video: {
// 						mandatory: {
// 							maxWidth: 3000,
// 							maxHeight: 3000
// 						}
// 					},
// 					audio: false
// 				},
// 				function(localMediaStream) {
// 					var videoElement = document.querySelector("video");
// 					video.src = window.URL.createObjectURL(localMediaStream);
// 					video.mute = "muted";

// 					setInterval(function() {
// 						processVideo();
// 					}, 50);
// 				},
// 				function(err) {
// 					console.log("Error: " + err);
// 				});
// 		} else {
// 			console.log("Browser does not support getUsermedia");
// 		}
// 	};

// init();
