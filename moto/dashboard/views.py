from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from item.models import *
from django.db.models import Q


@login_required
def index(request):
    items = Item.objects.filter(created_by=request.user)
    like_items = Item.objects.filter(likes=request.user)
    sold_items = Item.objects.filter(Q(is_sold=True) & (Q(created_by=request.user) | Q(buyer=request.user)))
    return render(request, 'dashboard/index.html', {
        'items': items,
        'like_items': like_items,
        'sold_items': sold_items,
    })