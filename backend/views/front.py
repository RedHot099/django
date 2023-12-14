from django.shortcuts import render, get_object_or_404
from ..models import Zaplecze, Account, Link
from ..serializers import ZapleczeSerializer, AccountSerializer
from rest_framework.views import APIView
from django.views.generic import View
from django.http import HttpResponse
from django.utils.decorators import method_decorator
from allauth.socialaccount.models import SocialAccount
from django.contrib.auth.models import User
from ..src.CreateWPblog.openai_api import OpenAI_API

import json
import urllib
from .utils import log_user


@method_decorator(log_user(), name='dispatch')
class Front(View):
    def get(self, request):
        queryset = Zaplecze.objects.values()

        try:
            data = SocialAccount.objects.get(user=request.user).extra_data
        except:
            data = {}

        try:
            papaj_spi = User.objects.get(username='papaj_spi')
        except User.DoesNotExist:
            papaj_spi = None

        context = {
            'queryset': queryset[::-1],
            'social_data': data,
            'papaj_spi': papaj_spi
        }

        return render(request, 'index.html', context)
    
@method_decorator(log_user(), name='dispatch')
class CreateZaplecze(View):
    def get(self, request):
        try:
            data = SocialAccount.objects.get(user=request.user).extra_data
        except:
            data = {}

        try:
            papaj_spi = User.objects.get(username='papaj_spi')
        except User.DoesNotExist:
            papaj_spi = None

        langs = OpenAI_API("").get_langs()
        context = {'social_data': data, 'langs': langs, 'papaj_spi': papaj_spi}


        return render(request, 'create.html', context)
    
@method_decorator(log_user(), name='dispatch')
class UpdateZaplecze(View):        
    def get(self, request, zaplecze_id):
        if zaplecze_id:
            serializer = ZapleczeSerializer(Zaplecze.objects.get(id=zaplecze_id))
        else:
            serializer.data = {}
        try:
            data = SocialAccount.objects.get(user=request.user).extra_data
        except:
            data = {}

        try:
            papaj_spi = User.objects.get(username='papaj_spi')
        except User.DoesNotExist:
            papaj_spi = None

        context = {'social_data': data, 'data': serializer.data, 'papaj_spi': papaj_spi}
        return render(request, 'update.html', context)
    
@method_decorator(log_user(), name='dispatch')
class ZapleczeUnit(View):
    def get(self, request, zaplecze_id):
        serializer = ZapleczeSerializer(Zaplecze.objects.get(id=zaplecze_id))
        
        context = {'data': serializer.data}

        try:
            papaj_spi = User.objects.get(username='papaj_spi')
        except User.DoesNotExist:
            papaj_spi = None

        context = {
            'data': serializer.data,
            'papaj_spi': papaj_spi
        }

        return render(request, 'zaplecze.html', context)
    

@method_decorator(log_user(), name='dispatch')
class WriteLink(View):
    def detect_change(self, val1, val2):
        if val1 > val2:
            return 1
        elif val1 == val2:
            return 0
        else:
            return -1
        
    def get(self, request, umowa_id):
        with urllib.request.urlopen(f"https://panel.verseo.pl/get_client_eichner_subpages.php?token=ewwg37sht579wqegwhedki4r5i98we34ytwue5uj&id_umowy={umowa_id}") as url:
            umowa = json.load(url)['data'][0]
        
        parsed_umowa = []
        for row in umowa['frazy']:
            row['data_wczoraj'] = row['data wczoraj']
            try:
                row['pozycja_wczoraj'] = int(row['pozycja wczoraj'])
            except:
                row['pozycja_wczoraj'] = 0
            row['data_dzisiaj'] = row['data dzisiaj']
            try:
                row['pozycja_dzisiaj'] = int(row['pozycja dzisiaj'])
            except: 
                row['pozycja_dzisiaj'] = 0
            del row['data wczoraj']
            del row['pozycja wczoraj']
            del row['data dzisiaj']
            del row['pozycja dzisiaj']
            parsed_umowa.append(row)
        
        umowa['frazy'] = parsed_umowa

        zaplecza = [l.split("\t") for l in open("../zaplecza.tsv", encoding="utf-8").read().split("\n") if len(l.split("\t")[-1])>20]

        zaplecza_unique = list(set([z[0] for z in zaplecza]))

        visibility = [v.split("\t") for v in open("../visibility_data.tsv", encoding="utf-8").read().split("\n")]

        zaplecza_data = {}
        for z in zaplecza:
            zaplecza_data[z[1]] = {
                "domain": z[1].lower(),
                "topic": z[0], 
                "login": z[2],
                "wp_password": z[3],
                "wp_api_key": z[4],
                "date": ""
            }
        
        for v in visibility:
            dom = v[0].lower()
            try:
                if zaplecza_data[dom]["date"] == "":
                    zaplecza_data[dom].update({
                        "date": v[1],
                        "top3": v[2],
                        "top3_growth": 0,
                        "top10": v[3],
                        "top10_growth": 0,
                        "top50": v[4],
                        "top50_growth": 0
                    })
                elif zaplecza_data[dom]["date"] > v[1]:
                    top3_growth = self.detect_change(zaplecza_data[dom]["top3"], v[2])
                    top10_growth = self.detect_change(zaplecza_data[dom]["top10"], v[3])
                    top50_growth = self.detect_change(zaplecza_data[dom]["top50"], v[4])
                    zaplecza_data[dom].update({
                        "date": v[1],
                        "top3_growth": top3_growth,
                        "top10_growth": top10_growth,
                        "top50_growth": top50_growth
                    })
                else:
                    top3_growth = self.detect_change(v[2], zaplecza_data[dom]["top3"])
                    top10_growth = self.detect_change(v[3], zaplecza_data[dom]["top10"])
                    top50_growth = self.detect_change(v[4], zaplecza_data[dom]["top50"])
                    zaplecza_data[dom].update({
                        "date": v[1],
                        "top3": v[2],
                        "top3_growth": top3_growth,
                        "top10": v[3],
                        "top10_growth": top10_growth,
                        "top50": v[4],
                        "top50_growth": top50_growth
                    })
            except:
                pass

        try:
            papaj_spi = User.objects.get(username='papaj_spi')
        except User.DoesNotExist:
            papaj_spi = None

        context = {
                    "umowa": umowa, 
                    "zaplecza": zaplecza_data, 
                    "zaplecza_unique": sorted(zaplecza_unique),
                    'papaj_spi': papaj_spi
                   }
        
        return render(request, 'links.html', context)
    
@method_decorator(log_user(), name='dispatch')
class LinksPanel(View):
    def get(self, request):
        try:
            user = request.user.email.split("@")[0]
            with urllib.request.urlopen(f"https://panel.verseo.pl/get_client_eichner.php?token=45h5j56k6788i4y3h57k567i54t3w6ki5y6u4u6h&pozycjoner={user}&aktywne=1") as url:
                umowy = json.load(url)
        except Exception:
            umowy = {"data": {"key":""}}


        try:
            papaj_spi = User.objects.get(username='papaj_spi')
        except User.DoesNotExist:
            papaj_spi = None

        context = {"umowy": umowy['data'].values(), 'papaj_spi': papaj_spi}

        return render(request, 'links_panel.html', context)
    

@method_decorator(log_user(), name='dispatch')
class UpdateProfile(APIView):
    def get(self, request):
        #get all table rows that belongs to current user
        try:
            queryset = Link.objects.filter(user=request.user.email)
        except AttributeError:
            print("Anonymus user got into user page!")
            queryset = []
        context = {
            "data": queryset[::-1]
        }
        return render(request, 'user.html', context)
    
    def post(self, request):
        user_id = request.user.id # Assuming you send user_id in the post request
        openai_api_key = request.data.get('openai_api_key')
        semstorm_api_key = request.data.get('semstorm_api_key')

        try:
            account = get_object_or_404(Account, user_id=user_id)
            account.openai_api_key = openai_api_key
            account.semstorm_api_key = semstorm_api_key
        except Exception as e:
            account = Account.objects.create(user_id=user_id, openai_api_key=openai_api_key, semstorm_api_key=semstorm_api_key)
        account.save()

        return render(request, 'user.html')
