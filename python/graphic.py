from PIL import Image
import json
import sys

# Sadness, Neutral, Contempt, Disgust, Anger, Surprise, Fear, Happiness

class FaceInfo:
	def __init__(self):
		self.box_info = {}
		self.eye_info = {}
		self.mouth_info = {}
		self.nose_info = {}
		self.eyebrow_info = {}

	def add_box_info(self, key, val):
		self.box_info[key] = val

	def add_eye_info(self, key, val):
		self.eye_info[key] = val

	def add_mouth_info(self, key, val):
		self.mouth_info[key] = val

	def add_nose_info(self, key, val):
		self.nose_info[key] = val

	def add_eyebrow_info(self, key, val):
		self.eyebrow_info[key] = val

def get_json_data(json_path):
	with open(json_path) as data_file:
		data = json.load(data_file)
	return data

def getEmotion(json_data):
	emotionData = json_data['response']['emotion'][0]['scores']
	# print emotionData
	minVal = 0
	emote='neutral'
	count = 0
	for key in emotionData.keys():
		if emotionData[key] > minVal:
			minVal = emotionData[key]
			emote = key
	print emote
	return emote

def getFaceInfo(json_data):
	faceData = json_data['response']['face'][0]
	faceRectangle = faceData['faceRectangle']
	faceInfo = FaceInfo()
	for key in faceRectangle.keys():
		faceInfo.add_box_info(key, faceRectangle[key])
	faceLandmarks = faceData['faceLandmarks']
	# print faceLandmarks
	#eyes
	pupilRight_dict = {}
	pupilRight_dict['y'] = faceLandmarks['pupilRight']['y']
	pupilRight_dict['x'] = faceLandmarks['pupilRight']['x']
	faceInfo.add_eye_info('pupilRight', pupilRight_dict)
	pupilLeft_dict = {}
	pupilLeft_dict['y'] = faceLandmarks['pupilLeft']['y']
	pupilLeft_dict['x'] = faceLandmarks['pupilLeft']['x']
	faceInfo.add_eye_info('pupilLeft', pupilLeft_dict)
	eyeRightOuter_dict = {}
	eyeRightOuter_dict['y'] = faceLandmarks['eyeRightOuter']['y']
	eyeRightOuter_dict['x'] = faceLandmarks['eyeRightOuter']['x']
	faceInfo.add_eye_info('eyeRightOuter', eyeRightOuter_dict)
	eyeRightInner_dict = {}
	eyeRightInner_dict['y'] = faceLandmarks['eyeRightInner']['y']
	eyeRightInner_dict['x'] = faceLandmarks['eyeRightInner']['x']
	faceInfo.add_eye_info('eyeRightInner', eyeRightInner_dict)
	eyeLeftOuter_dict = {}
	eyeLeftOuter_dict['y'] = faceLandmarks['eyeLeftOuter']['y']
	eyeLeftOuter_dict['x'] = faceLandmarks['eyeLeftOuter']['x']
	faceInfo.add_eye_info('eyeLeftOuter', eyeLeftOuter_dict)
	eyeLeftInner_dict = {}
	eyeLeftInner_dict['y'] = faceLandmarks['eyeLeftInner']['y']
	eyeLeftInner_dict['x'] = faceLandmarks['eyeLeftInner']['x']
	faceInfo.add_eye_info('eyeLeftInner', eyeLeftInner_dict)
	#mouth
	# print faceLandmarks['mouthRight']
	mouthRight_dict = {}
	mouthRight_dict['y'] = faceLandmarks['mouthRight']['y']
	mouthRight_dict['x'] = faceLandmarks['mouthRight']['x']
	faceInfo.add_mouth_info('mouthRight', mouthRight_dict)
	mouthLeft_dict = {}
	mouthLeft_dict['y'] = faceLandmarks['mouthLeft']['y']
	mouthLeft_dict['x'] = faceLandmarks['mouthLeft']['x']
	faceInfo.add_mouth_info('mouthLeft', mouthLeft_dict)
	upperLipTop_dict = {}
	upperLipTop_dict['y'] = faceLandmarks['upperLipTop']['y']
	upperLipTop_dict['x'] = faceLandmarks['upperLipTop']['x']
	faceInfo.add_mouth_info('upperLipTop', upperLipTop_dict)
	upperLipBottom_dict = {}
	upperLipBottom_dict['y'] = faceLandmarks['upperLipBottom']['y']
	upperLipBottom_dict['x'] = faceLandmarks['upperLipBottom']['x']
	faceInfo.add_mouth_info('upperLipBottom', upperLipBottom_dict)
	underLipBottom_dict = {}
	underLipBottom_dict['y'] = faceLandmarks['underLipBottom']['y']
	underLipBottom_dict['x'] = faceLandmarks['underLipBottom']['x']
	faceInfo.add_mouth_info('underLipBottom', underLipBottom_dict)
	underLipTop_dict = {}
	underLipTop_dict['y'] = faceLandmarks['underLipTop']['y']
	underLipTop_dict['x'] = faceLandmarks['underLipTop']['x']
	faceInfo.add_mouth_info('underLipTop', underLipTop_dict)
	#nose
	noseTip_dict = {}
	noseTip_dict['y'] = faceLandmarks['noseTip']['y']
	noseTip_dict['x'] = faceLandmarks['noseTip']['x']
	faceInfo.add_nose_info('noseTip', noseTip_dict)
	noseRootRight_dict = {}
	noseRootRight_dict['y'] = faceLandmarks['noseRootRight']['y']
	noseRootRight_dict['x'] = faceLandmarks['noseRootRight']['x']
	faceInfo.add_nose_info('noseRootRight', noseRootRight_dict)
	noseRootLeft_dict = {}
	noseRootLeft_dict['y'] = faceLandmarks['noseRootLeft']['y']
	noseRootLeft_dict['x'] = faceLandmarks['noseRootLeft']['x']
	faceInfo.add_nose_info('noseRootLeft', noseRootLeft_dict)
	#eyebrow
	eyebrowLeftOuter_dict = {}
	eyebrowLeftOuter_dict['y'] = faceLandmarks['eyebrowLeftOuter']['y']
	eyebrowLeftOuter_dict['x'] = faceLandmarks['eyebrowLeftOuter']['x']
	faceInfo.add_eyebrow_info('eyebrowLeftOuter', eyebrowLeftOuter_dict)
	eyebrowLeftInner_dict = {}
	eyebrowLeftInner_dict['y'] = faceLandmarks['eyebrowLeftInner']['y']
	eyebrowLeftInner_dict['x'] = faceLandmarks['eyebrowLeftInner']['x']
	faceInfo.add_eyebrow_info('eyebrowLeftInner', eyebrowLeftInner_dict)
	eyebrowRightOuter_dict = {}
	eyebrowRightOuter_dict['y'] = faceLandmarks['eyebrowRightOuter']['y']
	eyebrowRightOuter_dict['x'] = faceLandmarks['eyebrowRightOuter']['x']
	faceInfo.add_eyebrow_info('eyebrowRightOuter', eyebrowRightOuter_dict)
	eyebrowRightInner_dict = {}
	eyebrowRightInner_dict['y'] = faceLandmarks['eyebrowRightInner']['y']
	eyebrowRightInner_dict['x'] = faceLandmarks['eyebrowRightInner']['x']
	faceInfo.add_eyebrow_info('eyebrowRightInner', eyebrowRightInner_dict)
	return faceInfo


	

def build_image_array(image_path):
    image = Image.open(image_path)
    image_data = image.getdata()
    width, height = image_data.size
    image_array = [[0 for x in xrange(width)] for x in xrange(height)]
    for row in range(height):
        for col in range(width):
            image_array[row][col] = image_data.getpixel((col, row))[0]
    return image_array

def build_image(image_path):
	return Image.open(image_path)

def drawAnger(background, angerSymbol, leftEyebrow, rightEyebrow, faceInfo, outfile):
	print "anger"
	bg_w, bg_h = background.size
	leftOuterX = int(faceInfo.eyebrow_info['eyebrowLeftOuter']['x'])
	leftOuterY = int(faceInfo.eyebrow_info['eyebrowLeftOuter']['y'])

	rectangleX = int(faceInfo.box_info['width'])
	rectangleY = int(faceInfo.box_info['height'])
	averageRectLen = (rectangleX + rectangleY) / 4
	angerSymbol = angerSymbol.resize((averageRectLen / 2, averageRectLen / 2), Image.ANTIALIAS)

	
	leftInnerX = int(faceInfo.eyebrow_info['eyebrowLeftInner']['x'])
	leftInnerY = int(faceInfo.eyebrow_info['eyebrowLeftInner']['y'])
	leftEyebrow = leftEyebrow.resize((averageRectLen, averageRectLen), Image.ANTIALIAS)

	rightInnerX = int(faceInfo.eyebrow_info['eyebrowRightInner']['x'])
	rightInnerY = int(faceInfo.eyebrow_info['eyebrowRightInner']['y'])
	rightEyebrow = rightEyebrow.resize((averageRectLen, averageRectLen), Image.ANTIALIAS)

	sy_w, sy_h = angerSymbol.size
	offset = (leftOuterX - sy_w / 2, leftOuterY - sy_h / 2)
	

	leftBrow_w, leftBrow_h = leftEyebrow.size
	leftEyebrowOffset = (leftInnerX - leftBrow_w, int(leftInnerY - leftBrow_h / 1.5))
	background.paste(leftEyebrow, leftEyebrowOffset, mask = leftEyebrow)

	rightBrow_w, rightBrow_h = rightEyebrow.size
	rightEyebrowOffset = (rightInnerX - rightBrow_w / 4, int(rightInnerY - rightBrow_h / 1.5))
	background.paste(rightEyebrow, rightEyebrowOffset, mask = rightEyebrow)
	background.paste(angerSymbol, offset, mask = angerSymbol)
	background.save(outfile)

def drawContempt(image_array):
	return image_array

def drawDisgust(image_array):
	return image_array

def drawFear(image_array):
	return image_array

def drawHappiness(background, star1, rose, faceInfo, outfile):
	bg_w, bg_h = background.size

	st1orig_w, st1orig_h = star1.size
	rightOuter = int(faceInfo.eye_info['eyeRightOuter']['x'])
	rightInner = int(faceInfo.eye_info['eyeRightInner']['x'])
	righty = int(faceInfo.eye_info['pupilRight']['y'])
	rightRatio = st1orig_w / (rightOuter - rightInner)
	star1 = star1.resize(((rightOuter - rightInner) * 2, (st1orig_h / rightRatio * 2)), Image.ANTIALIAS)
	st1_w, st1_h = star1.size
	averageRight = (rightOuter + rightInner) / 2
	st1_offset = (averageRight - st1_w / 2, righty - st1_h / 2, averageRight + st1_w - st1_w / 2, righty + st1_h - st1_h/2)
	background.paste(star1, st1_offset, mask = star1)

	leftOuter = int(faceInfo.eye_info['eyeLeftOuter']['x'])
	leftInner = int(faceInfo.eye_info['eyeLeftInner']['x'])
	lefty = int(faceInfo.eye_info['pupilLeft']['y'])
	leftRatio = st1orig_w / (leftInner - leftOuter)
	star1 = star1.resize(((leftInner - leftOuter) * 2, (st1orig_h / leftRatio * 2)), Image.ANTIALIAS)
	st1_w, st1_h = star1.size
	averageLeft = (leftOuter + leftInner) / 2
	st1_offset = (averageLeft - st1_w / 2, lefty - st1_h / 2, averageLeft + st1_w - st1_w / 2, lefty + st1_h - st1_h/2)
	background.paste(star1, st1_offset, mask = star1)

	rectangleX = int(faceInfo.box_info['width'])
	rectangleY = int(faceInfo.box_info['height'])
	rose_w, rose_h = rose.size
	averageRectLen = (rectangleX + rectangleY) / 4
	rectRatio = rose_w / (averageRectLen / 2)
	rose = rose.resize((averageRectLen / 2, rose_h / rectRatio), Image.ANTIALIAS)
	rose_w, rose_h = rose.size
	mouthLeftX = int(faceInfo.mouth_info['mouthLeft']['x'])
	mouthLeftY = int(faceInfo.mouth_info['mouthLeft']['y'])
	mouthRightX = int(faceInfo.mouth_info['mouthRight']['x'])
	mouthRightY = int(faceInfo.mouth_info['mouthRight']['y'])
	rose_offset = (mouthLeftX - rose_w, mouthLeftY - rose_h)
	rose_offset2 = (mouthRightX, mouthRightY - rose_h)
	background.paste(rose, rose_offset, mask = rose)
	background.paste(rose, rose_offset2, mask = rose)


	background.save(outfile)

def drawNeutral(image_array):
	return image_array

def drawSadness(background, leftWater, rightWater, faceInfo, outfile):
	bg_w, bg_h = background.size
	leftW_w, leftW_h = leftWater.size
	rightW_w, rightW_h = rightWater.size
	# print faceInfo.eye_info['pupilRight']['x']
	righty = int(faceInfo.eye_info['pupilRight']['y'])
	rightOuter = int(faceInfo.eye_info['eyeRightOuter']['x'])
	rightInner = int(faceInfo.eye_info['eyeRightInner']['x'])
	rightRatio = rightW_w / (rightOuter - rightInner)
	leftOuter = int(faceInfo.eye_info['eyeLeftOuter']['x'])
	leftInner = int(faceInfo.eye_info['eyeLeftInner']['x'])
	leftRatio = leftW_w / (leftInner - leftOuter)
	lefty = int(faceInfo.eye_info['pupilLeft']['y'])
	rightWater = rightWater.resize((rightOuter - rightInner, rightW_h / rightRatio), Image.ANTIALIAS)
	rightW_w, rightW_h = rightWater.size
	offset = (rightInner, righty, rightOuter, righty + rightW_h)

	leftWater = leftWater.resize((leftInner - leftOuter, leftW_h / leftRatio), Image.ANTIALIAS)
	leftW_w, leftW_h = leftWater.size
	offset2 = (leftOuter, lefty, leftInner, lefty + leftW_h)
	# offset = ((bg_w - img_w) / 2, (bg_h - img_h) / 2)
	background.paste(rightWater, offset, mask = rightWater)
	background.paste(leftWater, offset2, mask = leftWater)
	background.save(outfile)
	# write to stdout

def drawSurprise(image_array):
	return image_array

if __name__ == '__main__':
	if len(sys.argv) < 4:
		exit(1)

	jsonString = sys.argv[1]
	inputImagePath = sys.argv[2]
	outputImagePath = sys.argv[3]

	data = json.loads(jsonString)

	image = build_image(inputImagePath)
	leftWater = build_image('python/things/left-tear.png')
	rightWater = build_image('python/things/right-tear.png')
	angerSymbol = build_image('python/things/anger-symbol.png')
	leftEyebrow = build_image('python/things/left-eye-brow.png')
	rightEyebrow = build_image('python/things/right-eye-brow.png')
	star1 = build_image('python/things/star-1.png')
	rose = build_image('python/things/rose.png')

	# data = get_json_data('sample.json')
	getEmotion(data)
	faceInfo = getFaceInfo(data)
	# drawSadness(image, leftWater, rightWater, faceInfo)
	# drawAnger(image, angerSymbol, leftEyebrow, rightEyebrow, faceInfo, outputImagePath)
	drawHappiness(image, star1, rose, faceInfo, outputImagePath)