from django.shortcuts import render
from django.http import HttpResponse
from bs4 import BeautifulSoup
import requests

BASE_URL_DESC = "https://www7.kissmovies.io/info/{}"
BASE_URL_IMG = "https://cdn.themovieseries.net/cover/{}.png"
BASE_URL_MOV = "https://vidnext.net/videos/{}"


def home(request):
    return render(request, 'movies/search.html')


def search(request):
    name = request.POST['s_input']
    ele = name.split()

    a = ele[0]
    for i in ele:
        if (i != ele[0]):
            a = a + '-' + i

    NEW_URL_DESC = BASE_URL_DESC.format(a)
    NEW_URL_IMG = BASE_URL_IMG.format(a)
    NEW_URL_MOV = BASE_URL_MOV.format(a)

    # image link only works by using in html tag
    # <img src="https://cdn.watch-series.co/cover/wonder-woman-1984.png" alt={ a } width="225" height="300">
    print(NEW_URL_IMG)
    print(NEW_URL_DESC)
    print(NEW_URL_MOV)

    response = requests.get(NEW_URL_DESC)
    data = response.text
    soup = BeautifulSoup(data, features='html.parser')

    # ------------------------------------------Description---------------------------------------
    # Finds tag with class='des'
    desc_result = soup.find(class_='des')

    # ------------------------------------------Video Link----------------------------------------
    movresponse = requests.get(NEW_URL_MOV)
    movdata = movresponse.text
    movsoup = BeautifulSoup(movdata, features='html.parser')

    # finds tag with class='play-video'
    vid_result = movsoup.find(class_="play-video")
    # extracts the tag iframe's src from vid_result
    try:
        mov = vid_result.find('iframe').get('src')
        video_link = "src = \"{}\"".format(mov)
    except:
        video_link = "Please type the full movie name correctly. \nor, we are sorry to inform that the movie doesn't exist in our database"
        # in the project,initialise video_link = None ,  and pass it to the frontend
        # check if video_link=None in frontend. if it's None, then put a message saying movie not found in database

    print("---------------------------------------------------Description--------------------------------------------------")
    if desc_result.text.lstrip().startswith('KissMovies'):
        short = 'Sorry, Summary doesn\'t exist'  # in the project, initialise desc_result.text.lstrip() = None . And, in the frontend, printout 'Sorry, Summary doesn't exist
    else:
        short = desc_result.text.lstrip()

    print("---------------------------------------------------Movie Link----------------------------------------------------")
    print(video_link)

    stuff_for_frontend = {
        'img': NEW_URL_IMG,
        'summary': short,
        'video': video_link
    }

    return render(request, 'movies/watch.html', stuff_for_frontend)


def watch(request):
    return render(request, 'movies/watch.html')
