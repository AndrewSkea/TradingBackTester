from rest_framework.views import APIView
from .models import Backtest
from src import main
import json
from django.http import HttpResponse
from django.http import JsonResponse


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
        user_id = request.POST.get('user_id')
        json_input = request.POST.get('json_config')
        print(json_input)
        if self.is_json_valid(json_input):
            json_output = self.main_class.start(json.loads(json_input))
        else:
            raise Exception("This is not valid JSON, please retry")
        Backtest.objects.create(user_id=user_id,
                                json_config=json_input,
                                time_taken=json_output['time_taken'],
                                num_bought_won=json_output['num_bought_won'],
                                num_sold_won=json_output['num_sold_won'],
                                num_bought_failed=json_output['num_bought_failed'],
                                num_sold_failed=json_output['num_sold_failed'],
                                exp_profit=json_output['exp_profit'],
                                linear_profit=json_output['linear_profit'],
                                lowest_balance=json_output['lowest_balance'],
                                starting_balance=json_output['starting_balance']
                                )
        return JsonResponse(json_output)

    def get(self, request):
        user_id = request.GET.get('user_id')
        results = Backtest.objects.filter(user_id=user_id)
        return HttpResponse(status=201)
