from flask_restful import Resource
from flask import request
from models.post import PostModel

from libs.queue import Queue
from bs4 import BeautifulSoup
import requests

class Posts(Resource):
    @classmethod
    def post(cls):
        data = request.get_json()

        queue = Queue()
        queue.add_queue(PostModel.process_post, data)
        return "Hola"