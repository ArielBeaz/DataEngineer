import requests
from PIL import Image, ImageChops, ImageEnhance, ImageOps
from io import BytesIO

url = 'https://api.imgflip.com/get_memes'
response = requests.get(url)

response_json = response.json()

meme_url = response_json['data']['memes'][0]

response = requests.get(meme_url['url'])

imagen_meme = Image.open(BytesIO(response.content)) 

imagen_meme.save("imagen_meme.jpeg", "JPEG")

print('Proceso finalizado con exito')