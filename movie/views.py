from django.shortcuts import render
from django.http import HttpResponse
from .models import Movie
import matplotlib.pyplot as plt
import matplotlib
import io
import urllib, base64
import base64
from movie.models import Movie 

# Create your views here.
def home(request):
    searchTerm = request.GET.get('searchMovie')

    if searchTerm:
        movies = Movie.objects.filter(title__icontains=searchTerm)
    else:
        movies = Movie.objects.all()

    return render(request, 'home.html', {
        'name': 'Mariana Muñoz',
        'searchTerm': searchTerm,
        'movies': movies
    })

def about(request):
    return render(request, 'about.html')
    

matplotlib.use('Agg')  # Para evitar problemas con el backend de Matplotlib

def signup(request):
    email = request.GET.get('email')
    return render(request, 'signup.html', {'email': email})

 # Asegúrate de importar tu modelo de películas

def statistics_view(request):
    # Obtener todos los géneros de las películas (solo el primer género de cada una)
    genres = Movie.objects.values_list('genre', flat=True)

    # Contar la cantidad de películas por género
    movie_counts_by_genre = {}

    for genre in genres:
        if genre:  # Asegurar que no sea None o vacío
            first_genre = genre.split(',')[0].strip()  # Tomar solo el primer género
            movie_counts_by_genre[first_genre] = movie_counts_by_genre.get(first_genre, 0) + 1

    # Crear la gráfica de barras
    plt.figure(figsize=(10, 5))
    plt.bar(movie_counts_by_genre.keys(), movie_counts_by_genre.values(), color='skyblue')

    # Personalizar la gráfica
    plt.title('Movies per Genre')
    plt.xlabel('Genre')
    plt.ylabel('Number of Movies')
    plt.xticks(rotation=45)  # Rotar etiquetas para mejor visibilidad
    plt.tight_layout()  # Ajustar diseño

    # Guardar la gráfica en un objeto BytesIO
    buffer = io.BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)
    plt.close()

    # Convertir la gráfica a base64 para enviarla a la plantilla
    image_png = buffer.getvalue()
    buffer.close()
    graphic = base64.b64encode(image_png).decode('utf-8')

    # Renderizar la plantilla statistics.html con la gráfica
    return render(request, 'statistics.html', {'graphic': graphic})



