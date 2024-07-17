from django.shortcuts import render
import requests
from .models import City, Search_History
from .forms import CityForm
from drf_spectacular.utils import extend_schema, extend_schema_view
from rest_framework.pagination import PageNumberPagination
from .serializers import CitySerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework import generics


def index(request):
    cities = City.objects.all()
    url = "https://api.openweathermap.org/data/2.5/weather?q={}&units=imperial&appid=5de06be0f94aeda639e62735db33a537&lang=ru"

    if request.method == "POST":
        form = CityForm(request.POST)
        form.save()

    form = CityForm()
    weather_data = []
    for city in cities:
        city_weather = requests.get(url.format(city)).json()

        weather = {
            "city": city,
            "temperature": city_weather["main"]["temp"],
            "description": city_weather["weather"][0]["description"],
            "icon": city_weather["weather"][0]["icon"],
        }

        weather_data.append(weather)
        Search_History.objects.create(user=request.user, name_city=city)
    context = {"weather_data": weather_data, "form": form}
    return render(request, "weather/index.html", context)


@extend_schema_view(
    get=extend_schema(description="История поиска активного пользователя")
)
class Search_HistoryList(generics.ListAPIView):
    queryset = Search_History.objects.all()
    serializer_class = CitySerializer
    permission_classes = [IsAuthenticated]
    pagination_class = PageNumberPagination

    def get_queryset(self):
        history = Search_History.objects.filter(user=self.request.user)
        return history
