from django.shortcuts import render
from django.http import HttpResponse
from bs4 import BeautifulSoup
import requests

BASE_URL_DESC = "https://www7.kissmovies.io/info/{}"
BASE_URL_IMG = "https://www.rottentomatoes.com/m/{}"
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

    b = ele[0]
    for i in ele:
        if (i != ele[0]):
            b = b + '_' + i

    NEW_URL_IMG = BASE_URL_IMG.format(b)

    # -------------------------------img url extraction ---------------------------------------
    img_response = requests.get(NEW_URL_IMG)
    img_data = img_response.text
    # print(img_data)
    img_soup = BeautifulSoup(img_data, features='html.parser')
    img_result = img_soup.find(class_="movie-thumbnail-wrap legacy")
    try:
        final_img = img_result.find('img').get('data-src')
    except:
        final_img = None

    #---------------------------------img url extraction end----------------------------------

    #---------------------------------heading extraction--------------------------------------

    heading_result = img_soup.find(class_="mop-ratings-wrap score_panel js-mop-ratings-wrap")
    try:
        heading = heading_result.find('h1').text
    except:
        heading = None

    #---------------------------------heading extraction end----------------------------------

    NEW_URL_DESC = BASE_URL_DESC.format(a)
    NEW_URL_MOV = BASE_URL_MOV.format(a)
    FINAL_MOV_URL = NEW_URL_MOV + '-hd-720p'

    #------------------------------ summary extraction ------------------------------------
    response = requests.get(NEW_URL_DESC)
    data = response.text
    soup = BeautifulSoup(data, features='html.parser')
    desc_result = soup.find(class_='des')

    if desc_result.text.lstrip().startswith('KissMovies'):
        rottentomatoesummary = img_soup.find(class_="mop-ratings-wrap__text mop-ratings-wrap__text--concensus")
        try:
            short = rottentomatoesummary.text
        except:
            short = None
    else:
        short = desc_result.text.lstrip()

    #--------------------------------- summary extraction end ---------------------------------------


    # ------------------------------------------Video Link extraction ----------------------------------------
    movresponse = requests.get(NEW_URL_MOV)
    movdata = movresponse.text

    if (movdata.startswith('404')):
        movresponse = requests.get(FINAL_MOV_URL)
        movdata = movresponse.text

    movsoup = BeautifulSoup(movdata, features='html.parser')

    # finds tag with class='play-video'
    vid_result = movsoup.find(class_="play-video")
    # extracts the tag iframe's src from vid_result
    try:
        mov = vid_result.find('iframe').get('src')
        video_link = mov
    except:
        video_link = None
        # in the project,initialise video_link = None ,  and pass it to the frontend
        # check if video_link=None in frontend. if it's None, then put a message saying movie not found in database
    # -------------------------------------------Video link extraction end -------------------------------------------

    stuff_for_frontend = {
        'img': final_img,
        'head': heading,
        'summary': short,
        'video': video_link
    }

    return render(request, 'movies/watch.html', stuff_for_frontend)


def watch(request):
    return render(request, 'movies/watch.html')
