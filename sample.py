import json, sys

if __name__ == '__main__':
	if len(sys.argv) < 4:
		exit(1)

	data = sys.argv[1]
	inputImagePath = sys.argv[2]
	outputImagePath = sys.argv[3]

	responseJson = json.loads(data)

	print responseJson
