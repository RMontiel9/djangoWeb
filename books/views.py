from django.shortcuts import render
from dotenv import load_dotenv
import os
import requests
# Create your views here.

load_dotenv()

api_key = os.getenv('GOOGLE_BOOKS_API_KEY')

def buscar_libros():
    query = "django"
    url = f"https://www.googleapis.com/books/v1/volumes?q={query}&key={API_KEY}"
    response = requests.get(url)
    data = response.json()

    # Puedes ver el contenido
    for item in data.get("items", []):
        title = item["volumeInfo"].get("title", "Sin título")
        print("Título:", title)
