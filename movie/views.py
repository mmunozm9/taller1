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




def statistics_view(request):
    # Obtener todos los géneros de las películas (solo el primer género de cada una)
    genres = Movie.objects.values_list('genre', flat=True)


    movie_counts_by_genre = {}

    for genre in genres:
        if genre:
            first_genre = genre.split(',')[0].strip()
            movie_counts_by_genre[first_genre] = movie_counts_by_genre.get(first_genre, 0) + 1

    # Crear la gráfica de películas por género
    plt.figure(figsize=(10, 5))
    plt.bar(movie_counts_by_genre.keys(), movie_counts_by_genre.values(), color='skyblue')


    plt.title('Movies per Genre')
    plt.xlabel('Genre')
    plt.ylabel('Number of Movies')
    plt.xticks(rotation=45)
    plt.tight_layout()

    # Guardar la gráfica en base64
    buffer = io.BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)
    plt.close()
    image_png = buffer.getvalue()
    buffer.close()
    graphic_genre = base64.b64encode(image_png).decode('utf-8')

    # -------- Agregar la segunda gráfica (Movies per Year) --------
    
    years = Movie.objects.values_list('year', flat=True).distinct().order_by('year')
    movie_counts_by_year = {}

    for year in years:
        if year:
            movies_in_year = Movie.objects.filter(year=year)
        else:
            movies_in_year = Movie.objects.filter(year__isnull=True)
            year = "None"
        count = movies_in_year.count()
        movie_counts_by_year[year] = count

    # Crear la gráfica de películas por año
    plt.figure(figsize=(10, 5))
    plt.bar([str(year) for year in movie_counts_by_year.keys()], movie_counts_by_year.values(), color='lightcoral')
    plt.title('Movies per Year')
    plt.xlabel('Year')
    plt.ylabel('Number of Movies')
    plt.xticks(rotation=90)
    plt.tight_layout()

    # Guardar la gráfica en base64
    buffer = io.BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)
    plt.close()
    image_png = buffer.getvalue()
    buffer.close()
    graphic_year = base64.b64encode(image_png).decode('utf-8')

    # Renderizar la plantilla con ambas gráficas
    return render(request, 'statistics.html', {
        'graphic_genre': graphic_genre,
        'graphic_year': graphic_year
    })



