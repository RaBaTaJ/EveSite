from django.shortcuts import get_object_or_404, render, redirect
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.views import generic

import json
import base64
import requests
import operator

from .models import Transaction, CharacterTotalInvestment, WeeklyPayment, Statistics
from itertools import chain

from django.contrib.auth.decorators import login_required

# Create your views here.
class IndexView(generic.ListView):
    template_name = 'WalletJournal/index.html'
    context_object_name = 'latest_transaction_list'
    model = Transaction   

    #Get CharName
    def get_context_data(self, **kwargs):
        context = super(IndexView, self).get_context_data(**kwargs) 
        context['CharName'] = ""
        try:
            context['CharName'] = self.request.session['CharName']
        except (AttributeError, KeyError):
            context['CharName'] = "NOCHARNAME"
        return context
    
    #Get appropriate transactions
    def get_queryset(self):
        try:
            CharName = self.request.session['CharName']
        except:
            CharName = "NOCHARNAME"
        FromList = Transaction.objects.filter(TransactionFrom__exact=CharName)
        ToList = Transaction.objects.filter(TransactionTo__exact=CharName)
        Qset = sorted(chain(FromList, ToList),key=operator.attrgetter('TransactionDateTime'))
        return Qset       

class DetailView(generic.DetailView):
    model = Transaction
    context_object_name = "Transaction"
    template_name = 'WalletJournal/detail.html'

class FullInvestment(generic.ListView):
    template_name = 'WalletJournal/MyInvestment.html'
    context_object_name = 'FullInvestment'
    model = CharacterTotalInvestment 

    #Get CharName
    def get_context_data(self, **kwargs):
        context = super(FullInvestment, self).get_context_data(**kwargs) 
        context['CharName'] = ""
        try:
            context['CharName'] = self.request.session['CharName']
        except (AttributeError, KeyError):
            context['CharName'] = "NOCHARNAME"
        return context
    
    #Get appropriate balance
    def get_queryset(self):
        try:
            CharName = self.request.session['CharName']
        except:
            CharName = "NOCHARNAME"
        TotalInvestment = CharacterTotalInvestment.objects.filter(CharacterName__exact=CharName)
        return TotalInvestment


def oauth(request):
    if request.GET.get("state") == request.session.session_key or request.GET.get("state") == "None":
        code = request.GET.get("code")
        b64key = base64.b64encode(b'd9bc2f9e37f3450e8318fe440fdd2302:LgrRpxF5jE0UccRImudfFiQ3H8bNA5nw4siiIdyj')
        AuthHeader = {'Authorization': 'Basic {0}'.format(b64key)}
        r = requests.post("https://login.eveonline.com/oauth/token", headers=AuthHeader, data={"grant_type":"authorization_code","code":code})
        r = json.loads(r.content)
        token = r["access_token"]
        InfoHeader = {'Authorization':'Bearer {0}'.format(token)}
        CharInfo = requests.get("https://login.eveonline.com/oauth/verify", headers=InfoHeader)
        CharInfo = json.loads(CharInfo.content)
        CharName = CharInfo["CharacterName"]
        request.session['CharName'] = CharName
        return redirect("/WalletJournal/")
    else:
        return render(request, 'WalletJournal/OAuthError.html')

@login_required
def admin(request):
    return render(request, 'WalletJournal/Admin.html')

@login_required
def investors(request):
    InvestorsList = CharacterTotalInvestment.objects.order_by('-TotalInvestment')
    context = {'InvestorsList': InvestorsList}
    return render(request, 'WalletJournal/Investors.html', context)

@login_required
def weekly(request):
    WeekList = WeeklyPayment.objects.order_by('-PaymentAmount')
    context = {'WeekList':WeekList}
    return render(request, 'WalletJournal/WeeklyPayments.html', context)

@login_required
def StatisticsView(request):
    FullStats = Statistics.objects.get()
    context = {'FullStats' : FullStats}
    return render(request, 'WalletJournal/Statistics.html', context)

@login_required
def refferals(request):
    InvestorsList = CharacterTotalInvestment.objects.order_by('-TotalInvestment')
    context = {'InvestorsList': InvestorsList}
    return render(request, 'WalletJournal/Refferals.html', context)