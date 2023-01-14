from django.shortcuts import render

from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.request import Request

from django.contrib.auth.models import User

# Create your views here.

@api_view()
def test(request:Request):
    users = User.objects.all()
    return Response({"msg": str(users)})
