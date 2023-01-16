from django.shortcuts import render, get_object_or_404

from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework import status

from rest_framework import generics
from rest_framework.permissions import IsAdminUser, IsAuthenticated

from django.contrib.auth.models import User, Group

from .serializers import CategorySerializer, MenuItemSerializer, CartSerializer, OrderSerializer, OrderItemSerializer, UserSerializer
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




@api_view(['GET', 'PUT', 'DELETE'])
@permission_classes([IsAuthenticated])
def single_menuitem(request:Request, id):

    if request.method == "GET":

        item = get_object_or_404(MenuItem, pk = id)
        serialized_data = MenuItemSerializer(item)

        return Response(serialized_data.data, status=status.HTTP_200_OK)

    elif request.method == "PUT":

        if request.user.groups.filter(name = "Manager").exists():

            title = request.data.get("title")
            price = request.data.get("price")
            featured = request.data.get("featured")
            category = request.data.get("category")
            
            if title and price and featured and category:
                
                item = get_object_or_404(MenuItem, pk = id)
                categoryobj = Category.objects.get(title = category)

                if categoryobj:

                    item.title = title
                    item.price = price
                    item.featured = featured
                    item.category = categoryobj

                    item.save()

                    return Response({"message": "Item updated succesfully"}, status=status.HTTP_200_OK)

            else:
                return Response({"message": "Could not update item succesfully"}, status.HTTP_409_CONFLICT)

        else:
            return Response({"message": "You are not authorized"}, status=status.HTTP_403_FORBIDDEN)


    elif request.method == "DELETE":

        if request.user.groups.filter(name = "Manager").exists():

            item = get_object_or_404(MenuItem, pk = id)
            item.delete()

            return Response({"message": "item deleted succesfully"}, status=status.HTTP_200_OK)

        else:
            return Response({"message": "You are not authorized to perform this action"}, status=status.HTTP_403_FORBIDDEN)
         

@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def managers(request:Request):
    
    if request.user.groups.filter(name = "Manager").exists():

        if request.method == "GET":
            group = Group.objects.get(name='Manager')
            managers = group.user_set.all()
            
            # managers = User.objects.filter(groups__name == "Manager")

            serialized_data = UserSerializer(managers, many = True)

            return Response(serialized_data.data, status=status.HTTP_200_OK)
    

        elif request.method == "POST":
            
            username = request.data.get('username')
            user = get_object_or_404(User, username = username)

            group = Group.objects.get(name = "Manager")
            managers = group.user_set.all()

            if user in managers:
                return Response({"message": "User is already in the managers group"}, status=status.HTTP_400_BAD_REQUEST)
            
            else: 
                user.groups.add(group)
                serialized_data = UserSerializer(user)
                return Response({"message": serialized_data.data, "message": "User has been added to the managers group."}, status=status.HTTP_201_CREATED)

    else:
        return Response({"message": "You are not authorized to perform this action"}, status=status.HTTP_403_FORBIDDEN)

    


@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def remove_manager(request:Request, id):

    if request.user.groups.filter(name = "Manager").exists():

        user = get_object_or_404(User, pk = id)
        group = Group.objects.get(name = "Manager")

        managers = group.user_set.all()

        if user in managers:
            user.groups.remove(group)
            return Response({"message": "User has been removed from the manager group succesfully."}, status=status.HTTP_200_OK)

        else:
            return Response({"message": "This user is not a manager."}, status=status.HTTP_400_BAD_REQUEST)

    else:
        return Response({"message": "You are not authorized to perform this action"}, status=status.HTTP_403_FORBIDDEN)




@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def delivery_crew(request:Request):

    if request.user.groups.filter(name = "Manager").exists():

        if request.method == 'GET':

            group = Group.objects.get(name = "Delivery Crew")
            delivery_crew = group.user_set.all()
            
            serialized_data = UserSerializer(delivery_crew, many = True)
            return Response({"Delivery Crew": serialized_data.data})

        elif request.method == "POST":

            username = request.data.get('username')
            user = get_object_or_404(User, username = username)

            group = Group.objects.get(name = "Delivery Crew")
            delivery_crew = group.user_set.all()

            if user in delivery_crew:
                return Response({"message": "User is already in the delivery crew group"}, status=status.HTTP_400_BAD_REQUEST)
            
            else: 
                user.groups.add(group)
                serialized_data = UserSerializer(user)
                return Response({"message": serialized_data.data, "message": "User has been added to the delivery crew group."}, status=status.HTTP_201_CREATED)


    else:
        return Response({"message": "You are not authorized to perform this action"}, status=status.HTTP_403_FORBIDDEN)


@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def remove_delivery_crew(request:Request, id):

    if request.user.groups.filter(name = "Manager").exists():

        user = get_object_or_404(User, pk = id)
        group = Group.objects.get(name = "Delivery Crew")

        delivery_crew = group.user_set.all()

        if user in delivery_crew:
            user.groups.remove(group)
            return Response({"message": "User has been removed from the delivery crew group succesfully."}, status=status.HTTP_200_OK)

        else:
            return Response({"message": "This user is not in the delivery crew."}, status=status.HTTP_400_BAD_REQUEST)

    else:
        return Response({"message": "You are not authorized to perform this action"}, status=status.HTTP_403_FORBIDDEN)