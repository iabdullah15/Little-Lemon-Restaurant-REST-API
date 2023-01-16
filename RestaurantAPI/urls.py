from django.urls import path
from . import views

urlpatterns = [
    path('test', views.test),
    path('menu-items', views.menuitems),
    path('menu-item/<int:id>', views.single_menuitem),
    path('groups/manager/users', views.managers),
    path('groups/manager/users/<int:id>', views.remove_manager),
    path('groups/delivery-crew/users', views.delivery_crew),
    path('groups/delivery-crew/users/<int:id>', views.remove_delivery_crew),

    path('cart/menu-items', views.cart),
    path('orders', views.orders),
    
    # path('menu-items', views.ListMenuItems.as_view()),
]