from django.shortcuts import render

from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework import status

from rest_framework import generics
from rest_framework.permissions import IsAdminUser, IsAuthenticated

from django.contrib.auth.models import User

from .serializers import CategorySerializer, MenuItemSerializer, CartSerializer, OrderSerializer, OrderItemSerializer
from .models import Category, MenuItem, Cart, Order, OrderItem

# Create your views here.

@api_view()
def test(request:Request):
    users = User.objects.all()
    return Response({"msg": str(users)})


# class ListMenuItems(generics.ListAPIView):
#     queryset = MenuItem.objects.all()
#     serializer_class = MenuItemSerializer

@api_view(['GET','POST'])
@permission_classes([IsAuthenticated])
def menuitems(request:Request):
    
    if request.method == "GET":
        items = MenuItem.objects.all()
        serialized_data = MenuItemSerializer(items, many = True)

        return Response(serialized_data.data)

    elif request.method == "POST":
        
        if request.user.groups.filter(name = "Manager"):
            title = request.data.get("title")
            price = request.data.get("price")
            featured = request.data.get("featured")
            category = request.data.get("category")

            if title and price and featured and category:

                # itemdict = {
                #     "title": title,
                #     "price": price,
                #     "featured": featured,
                #     "category" : category
                # }

                categoryobj = Category.objects.get(title = category)

                item = MenuItem(title = title, price = price, featured = featured, category = categoryobj)
                item.save()
                return Response({"message": "Item has been created"}, status = status.HTTP_201_CREATED)

            else:
                return Response({"message": "Item could not be created."}, status=status.HTTP_409_CONFLICT)

        else:
            return Response({"message": "You are not authorized"}, status=status.HTTP_403_FORBIDDEN)
        