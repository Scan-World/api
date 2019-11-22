#! /usr/bin/env python
#-*-coding:utf-8-*-

from flask import Flask, request, jsonify
from flask_restful import Resource, Api

from flasgger import Swagger
import os

import spacy
nlp = spacy.load("fr_core_news_md")

import ast
import numpy as np
import pandas as pd
import re
import unidecode

import googlemaps

gmaps = googlemaps.Client(key='<key-google-map>')

app                         = Flask(__name__)
app.config['SECRET_KEY']    = 'secret!'
api         = Api(app)
UPLOAD_FOLDER = os.path.basename('uploads')
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


def cleaner(text):
    return re.sub("[^a-z ]+", "", unidecode.unidecode(text.lower()))

def scan_world_places_query(tag, what):
    """Get point of interest in specific cities.    Parameters
    ----------
    tag: str
        A city name, an adress, for instance.
    what: str
        What do you want to query?    Returns
    -------
    result: dict
    """
    location = list(gmaps.geocode("%s, france" % tag)[0]['geometry']['location'].values())
    if tag in ["", " "]:
        query_result = gmaps.places(query=what,
                                    language='fr')
    else:
        query_result = gmaps.places(query=what,
                                    location=location,
                                    language='fr')
    result = pd.DataFrame(query_result['results']).sort_values('rating', ascending=False).head(5).reset_index(drop=True)

    result['url'] = "https://www.google.com/maps/place/?q=place_id:" + result['reference']
    result = result[['name', 'rating', 'url']].to_dict('records')
    return result

def scan_world_instant_similarity(tag):
    """Give some similarity scores.

    Parameters
    ----------
    tag: str
        City name.

    Returns
    -------
    to_keep: list
        List of dictionary.
    """
    # arguments
    interest = nlp("concert musique festival art culture")

    # query
    query = "http://esombe-5.scan-world.info:5005/lastByTag/%s/fr/0/500" % tag
    res = ast.literal_eval(os.popen('curl %s' % query).read())

    # similarity
    similarity = [interest.similarity(nlp(cleaner(news['title']))) for news in res]
    ordering = np.argsort(similarity)

    # to keep
    to_keep = list()
    for i in ordering[::-1][:5]:
        to_keep.append(res[i])

    return to_keep

@app.route('/')
def hello():
    return 'Hello World!'

@app.route('/posts/<tag>', methods=['GET'])
def getPosts(tag):

    """
    This examples uses FlaskRESTful Resource
    It works also with swag_from, schemas and spec_dict
       ---
       parameters:
       - name: tag
         in: path
         type: string

       responses:
         200:
           description: A single user item
           schema:
             message: object
    """

    results = scan_world_instant_similarity(tag)
    return  jsonify(posts=results)

@app.route('/posts_by_cat/<tag>/<cat>', methods=['GET'])
def getPostsByCat(tag, cat):

    """
    This examples uses FlaskRESTful Resource
    It works also with swag_from, schemas and spec_dict
       ---
       parameters:
       - name: tag
         in: path
         type: string
       - name: cat
         in: path
         type: string

       responses:
         200:
           description: A single user item
           schema:
             message: string
    """

    results = scan_world_places_query(tag,cat)
    print(results)
    return  jsonify(data=results)


if __name__ == '__main__':


    Swagger(app)
    app.run(host='0.0.0.0', port=5003)
