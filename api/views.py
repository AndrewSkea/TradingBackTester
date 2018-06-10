from rest_framework import generics
from .serializers import BacktestSerializer
from .models import Backtest
from src import main
from django.http import HttpResponse


class BacktestView(generics.ListCreateAPIView):
    """This class defines the create behavior of our rest api."""
    model = Backtest

    def get(self, *args, **kwargs):
        # json_string = kwargs.get('json_string')
        # # Serialiaze this string
        # with open('src/data/config.json', 'r') as file:
        #     file.write(json_string)
        main_class = main.Main()
        json_output = main_class.start()
        print(json_output)
        # Save the output to the model
        return HttpResponse(json_output)
