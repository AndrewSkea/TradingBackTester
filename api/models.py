from django.db import models
import uuid


class Backtest(models.Model):
    """This class represents the Backtest model."""
    id = models.UUIDField(unique=True, auto_created=True, primary_key=True, editable=False, default=uuid.uuid4)
    user_id = models.UUIDField(default=uuid.uuid4, editable=False)
    datetime = models.DateTimeField(auto_created=True)
    json_config = models.TextField()
    time_taken = models.FloatField()
    num_bought_won = models.IntegerField()
    num_sold_won = models.IntegerField()
    num_bought_failed = models.IntegerField()
    num_sold_failed = models.IntegerField()
    exp_profit = models.TextField()
    linear_profit = models.IntegerField()
    lowest_balance = models.IntegerField()
    starting_balance = models.IntegerField()

    def __str__(self):
        """Return a human readable representation of the model instance."""
        return "{}".format(self.id)
