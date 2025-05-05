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
    path('search_preview/<str:search>/', views.search_preview, name='search_preview'),

    path('add_tag/<str:tag>/<int:id>/',views.add_tag,name="add_tag"),
    path("search_tags/<str:search>/", views.search_tags, name="search_tags"),
    path('<int:id>/edit/',views.edit),
    path('<int:id>/delete/',views.delete),
    path('tag/',views.idiomtags,name="tag"),

    path('edit/<int:id>/',views.serve_edit),
    path('a/edit/<int:id>/',views.edit_idiom),


]