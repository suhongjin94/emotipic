var capture = false,
	captureClick = function() {
		capture = true;

		var canvas = document.getElementById('canvas');

		console.log(canvas.toDataURL('image/jpeg', 1.0));

		$.post('/upload', {
			image: canvas.toDataURL('image/jpeg', 1.0)
		}, function(data) {
			console.log(data);
		}, 'json');
	},
	emotipicClick = function() {
		$.post('/emotipic', {},
			function(data) {
				console.log(data);
			}, 'json');
	},
	processVideo = function() {
		var canvas = document.getElementById("canvas"),
			video = document.getElementById("video"),
			context = canvas.getContext('2d');

		if (!capture) {
			context.save();
			context.scale(-1, 1);
			context.drawImage(video, -320, 0, 320, 240);
			context.restore();
		}
	},
	init = function() {
		navigator.getUserMedia = (navigator.getUserMedia ||
			navigator.webkitGetUserMedia ||
			navigator.mozGetUserMedia ||
			navigator.msGetUserMedia);

		if (navigator.getUserMedia) {
			navigator.getUserMedia({
					video: {
						mandatory: {
							maxWidth: 640,
							maxHeight: 480
						}
					},
					audio: false
				},
				function(localMediaStream) {
					var videoElement = document.querySelector("video");
					video.src = window.URL.createObjectURL(localMediaStream);
					video.mute = "muted";

					setInterval(function() {
						processVideo();
					}, 50);
				},
				function(err) {
					console.log("Error: " + err);
				});
		} else {
			console.log("Browser does not support getUsermedia");
		}
	};

init();