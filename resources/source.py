from flask_restful import Resource
from models.source import SourceModel
from libs.queue import Queue


def callback():
    print("Exec queue")

class Source(Resource):
    @classmethod
    def post(cls):
        return "Hola"
    
