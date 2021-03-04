from search.models import Favourite
from django.urls import path
from django.contrib.auth.views import LoginView, LogoutView
from search import views

app_name = 'search'

urlpatterns = [
    path('', views.HomePage.as_view(), name="home_page" ),
    path('favourite/', views.FavouritesPage.as_view(), name="favourite_page"),
    path('add_a_favourite/', views.add_to_favourite, name="add_to_favourite" ),
    path('login/', LoginView.as_view(template_name='admin/login.html',redirect_authenticated_user=True ), name="login"),
    path('logout/', LogoutView.as_view(next_page="/") , name="logout")
]