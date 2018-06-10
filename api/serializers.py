from rest_framework import serializers
from .models import Backtest


class BacktestSerializer(serializers.ModelSerializer):
    """Serializer to map the Model instance into JSON format."""

    class Meta:
        """Meta class to map serializer's fields with the model fields."""
        model = Backtest
        fields = ('id', 'json_config', 'time_taken', 'num_bought_won',
                  'num_sold_won', 'num_bought_failed', 'num_sold_failed',
                  'exp_profit', 'linear_profit', 'lowest_balance', 'starting_balance')
