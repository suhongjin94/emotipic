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
	print emotionData
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
	#eyes
	pupilRight_dict = {}
	pupilRight_dict['y'] = faceLandmarks['pupilRight']['y']
	pupilRight_dict['x'] = faceLandmarks['pupilRight']['x']
	faceInfo.add_eye_info('pupilRight', pupilRight_dict)
	pupilLeft_dict = {}
	pupilLeft_dict['y'] = faceLandmarks['pupilLeft']['y']
	pupilLeft_dict['x'] = faceLandmarks['pupilLeft']['x']
	faceInfo.add_eye_info('pupilLeft', pupilLeft_dict)
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

def drawAnger(image_array):
	return image_array

def drawContempt(image_array):
	return image_array

def drawDisgust(image_array):
	return image_array

def drawFear(image_array):
	return image_array

def drawHappiness(image_array):
	return image_array

def drawNeutral(image_array):
	return image_array

def drawSadness(background, secondImage, faceInfo):
	img_w, img_h = secondImage.size
	bg_w, bg_h = background.size
	print faceInfo.eye_info['pupilRight']['x']
	rightx = int(faceInfo.eye_info['pupilRight']['x'])
	righty = int(faceInfo.eye_info['pupilRight']['y'])
	offset = (rightx, righty)
	offset = ((bg_w - img_w) / 2, (bg_h - img_h) / 2)
	background.paste(secondImage, offset)
	background.save('out.png')
	# write to stdout

def drawSurprise(image_array):
	return image_array

image = build_image('test.jpg')
secondImage = build_image('circle_blue.png')

data = get_json_data('sample.json')
# getEmotion(data)
faceInfo = getFaceInfo(data)
drawSadness(image, secondImage, faceInfo)