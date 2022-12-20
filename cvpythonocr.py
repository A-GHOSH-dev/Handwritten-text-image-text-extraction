import os
import io
import json
import time
from msrest.authentication import CognitiveServicesCredentials
from azure.cognitiveservices.vision.computervision import ComputerVisionClient
from azure.cognitiveservices.vision.computervision.models import OperationStatusCodes, VisualFeatureTypes
import requests
from PIL import Image, ImageDraw, ImageFont

credential = json.load(open('credentials.json'))
API_KEY=credential['API_KEY']
ENDPOINT=credential['ENDPOINT']


cv_client=ComputerVisionClient(ENDPOINT, CognitiveServicesCredentials(API_KEY))
image_url='https://hotelmogel.com/wp-content/uploads/2017/03/handwritten-note-March14.jpg'

text_recognition_url = ENDPOINT + "vision/v3.1/read/analyze"

headers = {'Ocp-Apim-Subscription-Key': API_KEY}
data = {'url': image_url}
response = requests.post(
    text_recognition_url, headers=headers, json=data)
response.raise_for_status()


#local_file ='imagehandwritten.jpg'
response=cv_client.read(url=image_url, language='en', raw=True)
#response=cv_client.read_in_stream(open(local_file, 'rb'), language='en', raw=True)
operationLocation=response.headers['Operation-Location']
operation_id=operationLocation.split('/')[-1]
time.sleep(5)
result=cv_client.get_read_result(operation_id)

print(result)
print(result.status)
print(result.analyze_result)

if result.status==OperationStatusCodes.succeeded:
    read_results=result.analyze_result.read_results
    for analyzed_result in read_results:
        for line in analyzed_result.lines:
            print('Line: ')
            print(line.text)
            for word in line.words:
                print('Words: ')
                print(word.text)


#### For local files
# image=Image.open(local_file)
# if result.status==OperationStatusCodes.succeeded:
#     read_results=result.analyze_result.read_results
#     for analyzed_result in read_results:
#         for line in analyzed_result.lines:
#             #rect = line.bounding_box
#             x1, y1, x2, y2, x3, y3, x4, y4 = line.bounding_box
#             draw=ImageDraw.Draw(image)
#             draw.line(((x1, y1), (x2, y1), (x2, y2), (x3, y2), (x3, y3), (x4, y3), (x4, y4), (x1, y4), (x1, y1)), fill = (255, 0, 0), width = 5)

# image.show()
# image.save('handwritten result.jpg')





