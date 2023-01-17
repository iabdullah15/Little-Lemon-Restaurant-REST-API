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
import datetime as dt
from django.db.models.query import QuerySet


# Create your views here.

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



@api_view(['GET', 'POST', 'DELETE'])
@permission_classes([IsAuthenticated])
def cart(request:Request):

    if request.method == 'GET':

        user = User.objects.get(username = request.user.username)
        cart_items = Cart.objects.filter(user = user)
        serialized_data = CartSerializer(cart_items, many = True)

        return Response(serialized_data.data, status=status.HTTP_200_OK)

    elif request.method == 'POST':
        
        item_title = request.data.get("item")
        quantity = request.data.get("quantity")

        if item_title and quantity:

            user = User.objects.get(username = request.user.username)
            menu_item = get_object_or_404(MenuItem, title = item_title)
            unit_price = menu_item.price
            total_price = int(quantity) * int(unit_price)

            cart = Cart(user = user, menuitem = menu_item, quantity = quantity, unit_price = unit_price, price = total_price)
            cart.save()

            return Response({"message" : "Item succesfully added to the cart."}, status=status.HTTP_201_CREATED)

        else:
            return Response({"message":"Could not add item. Please try again."}, status=status.HTTP_409_CONFLICT)

    
    elif request.method == 'DELETE':

        request_user = User.objects.get(username = request.user.username)
        cart = Cart.objects.filter(user = request_user)

        if cart:
            cart.delete()
            serialized_data = CartSerializer(cart, many = True)

            return Response({"message": "Cart succesfully deleted"})

        else:
            return Response({"message": "Error! No Cart found."}, status=status.HTTP_404_NOT_FOUND)




@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def orders(request:Request):

    if request.method == 'GET':
        
        if request.user.groups.filter(name = "Manager").exists():

            orders = Order.objects.all()
            order_items = OrderItem.objects.all()

            serialized_orders = OrderSerializer(orders, many = True)
            serialized_order_items = OrderItemSerializer(order_items, many = True)

            return Response({"Orders": serialized_orders.data, "Order Items": serialized_order_items.data})

        elif request.user.groups.filter(name = "Delivery Crew").exists():

            user = User.objects.get(username = request.user.username)
            order = Order.objects.filter(delivery_crew = user)

            order_items = OrderItem.objects.select_related('order').filter(order__in=order)

            serialized_orders = OrderSerializer(order, many = True)
            serialized_order_items = OrderItemSerializer(order_items, many = True)

            return Response({"Orders": serialized_orders.data, "Order Items" : serialized_order_items.data})

        
        else:

            user = User.objects.get(username = request.user.username)
            order = Order.objects.filter(user = user)

            order_items = OrderItem.objects.select_related('order').filter(order__in=order)

            serialized_orders = OrderSerializer(order, many = True)
            serialized_order_items = OrderItemSerializer(order_items, many = True)

            return Response({"Orders": serialized_orders.data, "Order Items" : serialized_order_items.data})

    
    elif request.method == 'POST':

        user = User.objects.get(username = request.user.username)
        cart = Cart.objects.filter(user = user)

        if cart:

            delivery_crew = User.objects.get(username = "ahmed")
            time = dt.datetime.now()
            total_price = int()  #Total bill amount of order placed.

            for items in cart:
                total_price += int(items.price)

            order = Order(user = user, delivery_crew = delivery_crew, status = 0, total = total_price, date = time)
            order.save()

            for items in cart:
                order_item = OrderItem(order = order, menuitem = items.menuitem, quantity = items.quantity, unit_price = items.unit_price, price = items.price)
                order_item.save()

            cart.delete()

            return Response({"An order has been created."}, status=status.HTTP_201_CREATED)

        else:
            return Response({"message": "There are no items in your cart."}, status=status.HTTP_400_BAD_REQUEST)



@api_view(['GET', 'PUT', 'PATCH', 'DELETE'])
@permission_classes([IsAuthenticated])
def single_order(request: Request, id):
    
    if request.method == 'GET':

        user = User.objects.get(username = request.user.username)
        order = get_object_or_404(Order, pk = id)

        if order.user == user:
            order_items = OrderItem.objects.select_related('order').filter(order__exact=order)

            serialized_order_data = OrderSerializer(order)
            serialized_order_items_data = OrderItemSerializer(order_items, many = True)

            return Response({"Order": serialized_order_data.data, "Order Items": serialized_order_items_data.data}, status=status.HTTP_200_OK)

        else:
            return Response({"message": "You are not authorized to access this data."}, status=status.HTTP_403_FORBIDDEN)


    elif request.method == 'PATCH':

        delivery_crew = request.data.get('delivery_crew')
        order_status = request.data.get('status')
        order = get_object_or_404(Order, pk = id)

        if request.user.groups.filter(name = "Manager"):

            if delivery_crew:

                delivery_user = get_object_or_404(User, username = delivery_crew)
                order.delivery_crew = delivery_user

            if order_status:

                order.status = order_status

            order.save()
            return Response({"message": "Order Succesfully updated."}, status=status.HTTP_200_OK)


        elif request.user.groups.filter(name = "Delivery Crew").exists():

            if order_status:

                order.status = order_status

            order.save()
            return Response({"message": "Order Succesfully updated."}, status=status.HTTP_200_OK)
            

        else:
            return Response({"message": "You are not authorized to access this data."}, status=status.HTTP_403_FORBIDDEN)

    
    elif request.method == 'DELETE':

        if request.user.groups.filter(name = "Manager").exists():
        
            order = get_object_or_404(Order, pk = id)
            order.delete()

            return Response({"message": "Order succesfully deleted."}, status=status.HTTP_200_OK)

        else:
            return Response({"message": "You are not authorized to access this data."}, status=status.HTTP_403_FORBIDDEN)

