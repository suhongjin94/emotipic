from flask import Flask, render_template, request
import boto, json, os, requests
from boto.s3.key import Key

app = Flask(__name__)

access_id = 'AKIAINDUCELP6JPWASCA'
secret_access_key = '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'
bucket_name = 'emotipic'

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/web_capture', methods=['POST'])
def web_upload():
    pass    

@app.route('/upload', methods=['POST'])
def upload():
    if request.method == 'POST':
        # Connect to Amazon S3
        s3 = boto.connect_s3(access_id, secret_access_key)

        # Get a handle to the S3 bucket
        bucket_name = 'emotipic'
        bucket = s3.get_bucket(bucket_name)
        k = Key(bucket)

        data_file = request.files.get('file')

        file_contents = data_file.read()
        k.key = os.path.join('uploads', data_file.filename)
        k.content_type = data_file.content_type

        print "Uploading some data to " + bucket_name + " with key: " + k.key
        k.set_contents_from_string(file_contents)

        # call api
        url = k.generate_url(expires_in=300, query_auth=False, force_http=True)

        face_headers = {
            'Content-Type': 'application/json',
            'Ocp-Apim-Subscription-Key': '3014f0d696a144d4bd875661e36057c3'
        }

        emotion_headers = {
            'Content-Type': 'application/json',
            'Ocp-Apim-Subscription-Key': 'b94b9a266d7546ef91e64be1380960c9'
        } 

        data = {
                'url': url 
        }

        print url

        data = json.dumps(data)

        faces = requests.post('https://api.projectoxford.ai/face/v0/detections?analyzesFaceLandmarks=true', data=data, headers=face_headers)

        faceRectangles = ''
        faces = faces.json()

        # parse faces
        for face in faces:
            faceRectangle = face['faceRectangle']
            faceRectangles += ';%s,%s,%s,%s' % (faceRectangle['left'], faceRectangle['top'], faceRectangle['width'], faceRectangle['height'])

        faceRectangles = faceRectangles[1:]

        emotions = requests.post('https://api.projectoxford.ai/emotion/v1.0/recognize?faceRectangles=' + faceRectangles, data=data, headers=emotion_headers)
        emotions = emotions.json()

        return json.dumps({
            'faces': faces,
            'emotions': emotions
        })

        

if __name__ == '__main__':
    app.run(debug=True)
