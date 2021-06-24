import requests
from urllib.parse import quote_plus
from django.shortcuts import render
from bs4 import BeautifulSoup
from . import models
import html5lib

# Create your views here.
BASE_URL = 'https://losangeles.craigslist.org/search/?query={}'
BASE_IMAGE_URL = 'https://images.craigslist.org/{}_300x300.jpg'


def index(request):
    return render(request, 'base.html')


def new_search(request):
    search = request.POST.get('search')
    models.Search.objects.create(search=search)
    final_url = BASE_URL.format(quote_plus(search))
    response = requests.get(final_url, headers={'User-agent': 'your bot 0.1'})
    data = response.text
    soup = BeautifulSoup(data, 'html5lib')
    post_lists = soup.find_all('li', {'class': 'result-row'})

    final_posts = []
    for post in post_lists:
        post_title = post.find(class_='result-title').text
        post_url = post.find('a').get('href')

        if post.find(class_='result-price'):
            post_price = post.find(class_='result-price').text
        else:
            post_price = 'N/A'

        if post.find(class_='result-image').get('data-ids'):
            post_image_id = post.find(class_='result-image').get('data-ids').split(',')[0].split(':')[1]
            post_image_url = BASE_IMAGE_URL.format(post_image_id)
        else:
            post_image_url = 'https://craigslist.org/images/peace.jpg'
        final_posts.append((post_title, post_url, post_price, post_image_url))


    params = {
        'search': search,
        'final_posts': final_posts,
    }
    return render(request, 'myapp/new_Search.html', params)

