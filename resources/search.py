from flask_restful import Resource


class Search(Resource):
    @classmethod
    def post(cls):
        return "Hola"
