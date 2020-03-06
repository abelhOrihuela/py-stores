from flask_restful import Resource
from flask import request, jsonify
from bs4 import BeautifulSoup
import requests
from datetime import datetime
from es import es

from libs.queue import Queue
from models.post import PostModel


class Posts(Resource):
    @classmethod
    def post(cls):

        data = request.get_json()

        queue = Queue()
        queue.add_queue(PostModel.process_post, data)
        return {"message": "Post added successfully"}, 200

    @classmethod
    def get(cls):

        keyword = "ASALTOS"

        body = {
            "query": {
                "bool": {
                    "must": [
                        {
                            "multi_match": {
                                "query": keyword,
                                "fields": ["content", "title", "subtitle", "tags"],
                            }
                        },
                    ]
                }
            }
        }

        res = es.search(index="contents", body=body, filter_path=["hits.hits"])

        return jsonify(res["hits"]["hits"]), 200
