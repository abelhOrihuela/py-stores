from bs4 import BeautifulSoup
import requests

request = requests.get('https://www.elsoldetoluca.com.mx/policiaca/asesinan-a-un-hombre-en-metepec-4889260.html')
html = BeautifulSoup(request.text, 'html.parser')


title = html.select_one('body > div.container > section > section > h1')
subtitle = html.select_one('body > div.container > section > section > h3')
elements_body = html.select('div.content-body > div > p')
elements_tags =  html.select('body > div.container > section > section > div.tags-list > ul > li')
contents = ""
tagsText = ""
tagsArray= []

for el in elements_body:
    contents += el.text + '\n\n'

for el in elements_tags:
    tagsArray.append(el.text.replace('\n', ""))

print("Title:" + title.text)
print("Subtitle:" + subtitle.text)
print("Tags:" + ",".join(tagsArray))
print("Content:" + contents)

