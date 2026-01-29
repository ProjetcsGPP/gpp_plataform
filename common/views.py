# common/views.py
from django.shortcuts import render
from django.contrib.auth.decorators import login_required

@login_required
def em_desenvolvimento(request):
    return render(request, 'common/em_desenvolvimento.html')
