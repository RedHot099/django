from django.shortcuts import render
from ..models import Zaplecze
from ..serializers import ZapleczeSerializer
from django.views.generic import View
from allauth.socialaccount.models import SocialAccount
from ..src.CreateWPblog.openai_api import OpenAI_API


class Front(View):
    def get(self, request):
        queryset = Zaplecze.objects.values()
        try:
            data = SocialAccount.objects.get(user=request.user).extra_data
        except:
            data = {}
        context = {'queryset': queryset, 'social_data': data}
        return render(request, 'index.html', context)
    

class CreateZaplecze(View):
    def get(self, request):
        try:
            data = SocialAccount.objects.get(user=request.user).extra_data
        except:
            data = {}
        langs = OpenAI_API("").get_langs()
        context = {'social_data': data, 'langs': langs}
        return render(request, 'create.html', context)
    

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
        context = {'social_data': data, 'data': serializer.data}
        return render(request, 'update.html', context)
    

class ZapleczeUnit(View):
    def get(self, request, zaplecze_id):
        serializer = ZapleczeSerializer(Zaplecze.objects.get(id=zaplecze_id))
        
        context = {'data': serializer.data}

        return render(request, 'zaplecze.html', context)
    

class WriteLink(View):
    def get(self, request):
        try:
            data = SocialAccount.objects.get(user=request.user).extra_data
        except:
            data = {}
        langs = OpenAI_API("").get_langs()
        context = {'social_data': data, 'langs': langs}
        return render(request, 'links.html', context)