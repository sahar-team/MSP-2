import helper
from flask import Flask, request, Response, render_template, redirect
import json
import os.path
import requests
from pprint import pprint
import time
from io import BytesIO
from random import random
from azure.cognitiveservices.vision.contentmoderator import ContentModeratorClient
import azure.cognitiveservices.vision.contentmoderator.models
from msrest.authentication import CognitiveServicesCredentials
app = Flask(__name__)
# CONTENT_MODERATOR_ENDPOINT = os.environ.get("CONTENT_MODERATOR_ENDPOINT")
# subscription_key = os.environ.get("CONTENT_MODERATOR_SUBSCRIPTION_KEY")
# client = ContentModeratorClient(
# endpoint=CONTENT_MODERATOR_ENDPOINT,
#     credentials=CognitiveServicesCredentials(subscription_key)
# )


@app.route('/')
def hello_world():
    return render_template('index.html')

# def text_moderation(path):
#     with open(path, "rb") as text_fd:
#         screen = client.text_moderation.screen_text(
#             text_content_type="text/plain",
#             text_content=text_fd,
#             language="fra",
#             autocorrect=True,
#             pii=True
#         )
#     try:
#         pprint(len(screen.as_dict()['terms']))
#         to_moderate = True
#     except KeyError:
#         to_moderate = False
#     return to_moderate

@app.route('/comment/new', methods=['POST'])
def add_comment():
    # Get comment from the POST body
    if request.method == "POST":
        req = request.form.to_dict()
        comment = req["comment"]
        headers = {"Ocp-Apim-Subscription-Key": 'fc611a971326402a84c303e75460a5d3', 'Content-type': 'text/plain'}
        url = 'https://westeurope.api.cognitive.microsoft.com/contentmoderator/moderate/v1.0/ProcessText/Screen?classify=True&language=fra'
        data = {'ContentValue': comment}
        response = requests.post(url, headers=headers, data=data)
        if response.json()["Terms"] is not None:        
            return Response("méchant")
        else:
            return Response("gentil")    
          
        # return render_template("/index.html")
        # moderate = text_moderation("test")
        # if moderate is True:            
        #     return Response("méchant")
        # else:
        #     return Response("gentil")    

    
    req_data = request.get_json()
    comment = req_data['comment']

    # Add comment to the list
    res_data = helper.add_to_list(comment)

    # Return error if comment not added
    if res_data is None:
        response = Response("{'error': 'comment not added - " + comment + "'}", status=400 , mimetype='application/json')
        return response

    # Return response
    response = Response(json.dumps(res_data), mimetype='application/json')

    return render_template("index.html")