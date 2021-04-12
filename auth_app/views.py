from django.shortcuts import render
from django.views import generic 

class Home(generic.templateview):
    template_name = 'auth/home.html'
