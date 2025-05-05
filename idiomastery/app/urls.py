from django.urls import path
from . import views 

urlpatterns = [
    path('', views.serve_explore),
    path('login/',views.serve_login),
    path('register/',views.serve_registration),
    path('profile/<int:id>',views.serve_profile),
    path('<int:id>',views.serve_details),
    path('about/',views.serve_about),
    path('create/',views.serve_create),

    path('profile/',views.get_profile),

    path('a/login',views.login),
    path('a/register',views.register),
    path('a/logout',views.logout),
    path('a/create',views.create),
    path('search/',views.search, name='search'),
    path("<int:id>/addtranslation",views.addtranslation),
    path('like_idiom/<int:id>/', views.like_idiom, name='like_idiom'),
    # path('unlike_idiom/<int:id>/', views.unlike_idiom, name='unlike_idiom'),

    
    path('<int:id>/edit/',views.edit),
    path('<int:id>/delete/',views.delete),



]