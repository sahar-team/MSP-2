import helper
from flask import Flask, request, Response, render_template, redirect
import json
import os.path
import requests
from pprint import pprint
import time

app = Flask(__name__)


@app.route('/')
def hello_world():
    return render_template('index.html')


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
            return Response("Votre commentaire a été modéré.")
        else:
            return Response("Votre commentaire a été enregistré.")    

    
    req_data = request.get_json()
    comment = req_data['comment']

    res_data = helper.add_to_list(comment)

    if res_data is None:
        response = Response("{'error': 'comment not added - " + comment + "'}", status=400 , mimetype='application/json')
        return response

    response = Response(json.dumps(res_data), mimetype='application/json')

    return render_template("index.html")