from django.urls import path
from . import views

urlpatterns = [
    path('test', views.test),
    path('menu-items', views.menuitems),
    path('menu-item/<int:id>', views.single_menuitem),
    path('groups/manager/users', views.managers),

    # path('menu-items', views.ListMenuItems.as_view()),
]