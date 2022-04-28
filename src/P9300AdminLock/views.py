from django.http import HttpResponse
from django.http import Http404
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.template import loader
from django.views import generic

def index(request):
    template = loader.get_template('P9300AdminLock/index.html')
    context = {}
    ### return HttpResponse("Hello, world. You're at the P9300AdminLock index")
    return HttpResponse(template.render(context, request))
