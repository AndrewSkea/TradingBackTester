from django.conf.urls import url
from rest_framework.urlpatterns import format_suffix_patterns
from .views import BacktestView

urlpatterns = {
    url(r'^$', BacktestView.as_view(), name="backtest"),
}

urlpatterns = format_suffix_patterns(urlpatterns)