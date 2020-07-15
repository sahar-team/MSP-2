import helper
from flask import Flask, request, Response, render_template, redirect
import json
import os.path
from pprint import pprint
import time
from io import BytesIO
from random import random
from azure.cognitiveservices.vision.contentmoderator import ContentModeratorClient
import azure.cognitiveservices.vision.contentmoderator.models
from msrest.authentication import CognitiveServicesCredentials
app = Flask(__name__)
CONTENT_MODERATOR_ENDPOINT = os.environ.get("CONTENT_MODERATOR_ENDPOINT")
subscription_key = os.environ.get("CONTENT_MODERATOR_SUBSCRIPTION_KEY")
client = ContentModeratorClient(
endpoint=CONTENT_MODERATOR_ENDPOINT,
    credentials=CognitiveServicesCredentials(subscription_key)
)


@app.route('/')
def hello_world():
    return render_template('index.html')

def text_moderation(path):
    """TextModeration.
    This will moderate a given long text.
    True if text needs to be moderated
    False if text can be accepted
    """
    # <snippet_textmod>
    # Screen the input text: check for profanity,
    # do autocorrect text, and check for personally identifying
    # information (PII)
    with open(path, "rb") as text_fd:
        screen = client.text_moderation.screen_text(
            text_content_type="text/plain",
            text_content=text_fd,
            language="fra",
            autocorrect=True,
            pii=True
        )
    try:
        pprint(len(screen.as_dict()['terms']))
        to_moderate = True
    except KeyError:
        to_moderate = False
    return to_moderate

@app.route('/comment/new', methods=['POST'])
def add_comment():
    # Get comment from the POST body
    if request.method == "POST":
        req = request.form.to_dict()
        comment = req["comment"]
        with open('test','w') as f:
            f.write(comment)        
        # return render_template("/index.html")
        moderate = text_moderation("test")
        if moderate is True:            
            return Response("méchant")
        else:
            return Response("gentil")    

    
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