from django.shortcuts import render,get_object_or_404,redirect
from dotenv import load_dotenv
import os
import requests
#LIBROS Y FAVORITOS
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from .models import Book, Favorite  # Asegúrate que el modelo esté creado y migrado
from .forms import ReviewForm
import json

# Create your views here.

load_dotenv()

#api_key = os.getenv('GOOGLE_BOOKS_API_KEY')

def index(request):
    libros = []
    query = request.GET.get("q")
    favoritos_google_ids = []

    if request.user.is_authenticated:
        favoritos_google_ids = request.user.favorites.values_list('book__google_id',
                                                                   flat=True)
        

    if request.user.is_authenticated:
        favoritos_google_ids = list(request.user.favorites.values_list('book__google_id', flat=True))
        favoritos_google_ids = [str(id) for id in favoritos_google_ids]

        print("Favoritos del usuario (google_ids):", favoritos_google_ids)  # <-- Aquí ves qué ids tiene

    else:
        favoritos_google_ids = []

        
    if query:
        api_key = os.getenv("GOOGLE_BOOKS_API_KEY")
        url = f"https://www.googleapis.com/books/v1/volumes?q={query}&key={api_key}&maxResults=20"
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            for item in data.get("items", []):
                info = item["volumeInfo"]
                libros.append({
                    "google_id": item.get("id"), 
                    "titulo": info.get("title"),
                    "autores": info.get("authors", []),
                    "descripcion": info.get("description", "Sin descripción"),
                    "imagen": info.get("imageLinks", {}).get("thumbnail", "")
                })

    return render(request, "core/index.html", {"libros": libros,
                                                  "query": query,
                                                  "favoritos_google_ids": favoritos_google_ids})


# Esta función guarda el libro si aún no existe
def guardar_libro_desde_api(data):
    book, _ = Book.objects.get_or_create(
        google_id=data["google_id"],
        defaults={
            "title": data["title"],
            "authors": data["authors"],
            "thumbnail": data["thumbnail"]
        }
    )
    return book

# Esta es la vista principal para agregar favoritos
@login_required
def toggle_favorito(request):
    if request.method == "POST":
        data = json.loads(request.body)

        libro = guardar_libro_desde_api(data)
        user = request.user

        favorito, creado = Favorite.objects.get_or_create(user=user, book=libro)

        if not creado:
            favorito.delete()
            return JsonResponse({"estado": "eliminado", "mensaje": "Libro eliminado de favoritos"})

        return JsonResponse({"estado": "agregado", "mensaje": "Libro agregado a favoritos"})

    return JsonResponse({"error": "Método no permitido"}, status=405)


def book_detail(request, google_id):
    book = Book.objects.filter(google_id=google_id).first()

    if not book:
        # Buscar en la API de Google Books
        url = f"https://www.googleapis.com/books/v1/volumes/{google_id}"
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            info = data.get("volumeInfo", {})

            title = info.get("title", "Sin título")
            authors = ", ".join(info.get("authors", []))
            thumbnail = info.get("imageLinks", {}).get("thumbnail", "")
            # Puedes agregar otros campos si quieres

            book = Book.objects.create(
                google_id=google_id,
                title=title,
                authors=authors,
                thumbnail=thumbnail
            )
        else:
            return render(request, "books/book_not_found.html", status=404)

    # Reviews
    reviews = book.reviews.all()
    form = ReviewForm()

    if request.method == 'POST':
        if request.user.is_authenticated:
            form = ReviewForm(request.POST)
            if form.is_valid():
                review = form.save(commit=False)
                review.book = book
                review.user = request.user
                review.save()
                return redirect('book_detail', google_id=book.google_id)
        else:
            return redirect('login')

    return render(request, 'books/detalle_libro.html', {
        'book': book,
        'reviews': reviews,
        'form': form
    })