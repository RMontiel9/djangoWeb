from django.shortcuts import render
from dotenv import load_dotenv
import os
import requests
# Create your views here.

load_dotenv()

#api_key = os.getenv('GOOGLE_BOOKS_API_KEY')

def index(request):
    libros = []
    query = request.GET.get("q")
    if query:
        api_key = os.getenv("GOOGLE_BOOKS_API_KEY")
        url = f"https://www.googleapis.com/books/v1/volumes?q={query}&key={api_key}"
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            for item in data.get("items", []):
                info = item["volumeInfo"]
                libros.append({
                    "titulo": info.get("title"),
                    "autores": info.get("authors", []),
                    "descripcion": info.get("description", "Sin descripción"),
                    "imagen": info.get("imageLinks", {}).get("thumbnail", "")
                })

    return render(request, "core/index.html", {"libros": libros,
                                                  "query": query})