from django.conf.urls import url

from . import views

app_name = 'home'

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^home/InvestmentGuide', views.InvestmentGuide, name='InvestmentGuide'),
    url(r'^home/About', views.About, name='About'),
]