from django.shortcuts import render

def inicio (request) :
    return render(request , r'compartidos\base.html' )