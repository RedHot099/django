from django.shortcuts import render
from ..models import Zaplecze
from ..serializers import ZapleczeSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions

from ..src.CreateWPblog.openai_article import OpenAI_article


class ZapleczeAPIStructure(APIView):
    
    def get_object(self, zaplecze_id):
        try:
            return Zaplecze.objects.get(id=zaplecze_id)
        except Zaplecze.DoesNotExist:
            return None
        
    def post(self, request, zaplecze_id):
        zaplecze = self.get_object(zaplecze_id)

        serializer = ZapleczeSerializer(zaplecze)

        data = serializer.data

        o = OpenAI_article(
            api_key=request.data.get("openai_api_key"),
            domain_name=data['domain'],
            wp_login=data['wp_user'],
            wp_pass=data['wp_api_key'],
            lang=data['lang']
        )

        structure = o.create_structure(data['topic'], request.data.get('cat_num'), request.data.get('subcat_num'))

        return Response(structure, status=status.HTTP_201_CREATED)