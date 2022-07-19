import imp
from django.shortcuts import render
import requests
from .models import City
from .forms import CityForm

def index(request):
    url = 'http://api.openweathermap.org/data/2.5/weather?q={}&units=imperial&appid=dd6d7e3e1ab99bb7488e0d63b3eaa13d'
    cities = City.objects.all() #return all the cities in the database
    name = request.POST['name']
    if request.method == 'POST':
            if City.objects.filter(name=name).exists():
                pass
            else:
                form = CityForm(request.POST)
                form.save()
    form = CityForm()
    weather_data = []

    for city in cities:

        city_weather = requests.get(url.format(city)).json() #request the API data and convert the JSON to Python data types

        weather = {
            'city' : city,
            'temperature' : city_weather['main']['temp'],
            'description' : city_weather['weather'][0]['description'],
            'icon' : city_weather['weather'][0]['icon']
        }

        weather_data.append(weather) #add the data for the current city into our list

    context = {'weather_data' : weather_data, 'form' : form}

    return render(request, 'weather/index.html', context) #returns the index.html template