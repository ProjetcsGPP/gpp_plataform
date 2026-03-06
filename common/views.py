# common/views.py
from django.contrib.auth.decorators import login_required
from django.shortcuts import render


@login_required
def em_desenvolvimento(request):
    return render(request, "common/em_desenvolvimento.html")
