from bs4 import BeautifulSoup
import requests
from models.source import SourceModel
from sa import create_app
from es import es
from datetime import datetime

app = create_app()
app.app_context().push()


class PostModel:
    @classmethod
    def process_post(cls, data):
        with app.app_context():

            url = data["url"]
            source_id = data["source"]
            coordinates = data["latlong"]

            source = SourceModel.find_by_uuid(source_id)

            request = requests.get(url)
            html = BeautifulSoup(request.text, "html.parser")

            content = ""
            tagsText = ""
            tagsArray = []

            title = html.select_one(source.title_selector)

            if source.subtitle_selector:
                subtitle = html.select_one(source.subtitle_selector)

            if source.content_selector:
                elements_body = html.select(source.content_selector)

                for el in elements_body:
                    content += el.text + "\n\n"

            if source.tags_selector:
                elements_tags = html.select(source.tags_selector)

                for el in elements_tags:
                    tagsArray.append(el.text.replace("\n", ""))

                tagsText = ",".join(tagsArray)

            if source.author_selector:
                author = html.select(source.author_selector)

            body = {
                "source_id": source_id,
                "state_id": source_id,
                "municipality_id": source_id,
                "title": title.text.replace("\n", ""),
                "subtitle": subtitle.text.replace("\n", ""),
                "location": {"type": "Point", "coordinates": coordinates},
                "content": content,
                "tags": tagsText.upper(),
                "author": author.text.replace("\n", ""),
                "link": url,
                "timestamp": datetime.now(),
            }

            es.index(index="contents", body=body)
