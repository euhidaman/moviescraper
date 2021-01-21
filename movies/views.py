from django.shortcuts import render
from django.http import HttpResponse


def home(request):
    return render(request, 'movies/search.html')

def search(request):
    movie_name = request.POST['s_input']
    print(movie_name)
    return render(request, 'movies/watch.html')

def watch(request):
    return render(request, 'movies/watch.html')
