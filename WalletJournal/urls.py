from django.conf.urls import url

from . import views

app_name = 'WalletJournal'

urlpatterns = [
    url(r'^$', views.IndexView.as_view(), name='index'),
    url(r'^oauth.html$', views.oauth, name='OAuth'),
    url(r'^Admin$', views.admin, name='Admin'),
    url(r'^Investors$', views.investors, name='Investors'),
    url(r'^WeeklyPayments$', views.weekly, name='Weekly Payments'),
    url(r'^Refferals$', views.refferals, name='Refferals'),
    url(r'^MyInvestment$', views.FullInvestment.as_view(), name='My Full Investment'),
    url(r'^Statistics$', views.StatisticsView, name='Statistics'),
    url(r'^(?P<pk>[0-9]+)/$', views.DetailView.as_view(), name='detail'),
]