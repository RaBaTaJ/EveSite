from django.shortcuts import get_object_or_404, render
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.views import generic

from .models import HomeNotice

# Create your views here.
def index(request):
    latest_homenotice_list = HomeNotice.objects.order_by('-PubDate')
    context = {'latest_homenotice_list': latest_homenotice_list}
    return render(request, 'home/index.html', context)

def InvestmentGuide(request):
    return render(request, 'home/InvestmentGuide.html')

def About(request):
    return render(request, 'home/About.html')



