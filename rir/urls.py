from django.urls import path
from . import views

urlpatterns = [
	path('Lista-Rir.html/', views.List_rir, name="r-list"),

]