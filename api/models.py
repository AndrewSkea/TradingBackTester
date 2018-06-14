from django.db import models
import uuid


class Backtest(models.Model):
    """This class represents the Backtest model."""
    id = models.UUIDField(unique=True, auto_created=True, primary_key=True, editable=False, default=uuid.uuid4)
    user_id = models.IntegerField(editable=False)
    datetime = models.DateTimeField(auto_now=True)
    json_config = models.TextField()
    time_taken = models.FloatField(blank=True, null=True)
    num_bought_won = models.IntegerField(blank=True, null=True)
    num_sold_won = models.IntegerField(blank=True, null=True)
    num_bought_failed = models.IntegerField(blank=True, null=True)
    num_sold_failed = models.IntegerField(blank=True, null=True)
    exp_profit = models.TextField(blank=True, null=True)
    linear_profit = models.IntegerField(blank=True, null=True)
    lowest_balance = models.IntegerField(blank=True, null=True)
    starting_balance = models.IntegerField(blank=True, null=True)

    def __str__(self):
        """Return a human readable representation of the model instance."""
        return "{}".format(self.id)
