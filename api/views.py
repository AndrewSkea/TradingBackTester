from rest_framework.views import APIView
from .models import Backtest
from src import main
import json
from django.http import HttpResponse


class BacktestView(APIView):
    """This class defines the create behavior of our rest api."""
    model = Backtest
    main_class = main.Main()

    def is_json_valid(self, input_json):
        try:
            json.loads(input_json)
            return True
        except Exception:
            return False

    def post(self, request):
        json_input = request.POST.get('json_config')
        user_id = request.POST.get('user_id')
        print(json_input)
        if self.is_json_valid(json_input):
            json_output = self.main_class.start(json_input)
        else:
            raise Exception("This is not valid JSON, please retry")

        Backtest.objects.create(user_id=user_id, json_config=json_input)
        return HttpResponse(status=201)

    def get(self, request):
        user_id = request.POST.get('user_id')
        return HttpResponse(status=201)

