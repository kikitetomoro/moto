from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.views.decorators.http import require_POST
from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse
from .forms import NewItemForm, EditItemForm, RenewItemLocationForm
from .models import Category, Item
from django.conf import settings
from django.contrib.auth.models import AnonymousUser
from django.http import HttpResponseRedirect
from django.urls import reverse
import json

def items(request):
    query = request.GET.get('query', '')
    category_id = request.GET.get('category', 0)
    categories = Category.objects.all()
    items = Item.objects.filter(is_sold=False)
    if isinstance(request.user, AnonymousUser):
        items = Item.objects.filter(type='shelter', is_sold=False)
    elif request.user.userstatus == 'corporate':
        items = Item.objects.filter(type='stray', is_sold=False)
    else:
        items = Item.objects.filter(type='shelter', is_sold=False)

    if category_id:
        items = items.filter(category_id=category_id)

    if query:
        items = items.filter(Q(name__icontains=query) | Q(description__icontains=query)|Q(address__icontains=query)| Q(description__icontains=query)|Q(prefecture__icontains=query))

    return render(request, 'item/items.html', {
        'items': items,
        'query': query,
        'categories': categories,
        'category_id': int(category_id)
    })
def category_items(request, category_id):
    category = get_object_or_404(Category, id=category_id)
    items = Item.objects.filter(category=category)

    return render(request, 'item/category_items.html', {
        'category': category,
        'items': items,
    })

def map_view(request):
    key = settings.GOOGLE_API_KEY
    items = Item.objects.filter(is_sold=False)
    if isinstance(request.user, AnonymousUser):
        items = Item.objects.filter(type='shelter', is_sold=False)
    elif request.user.userstatus == 'corporate':
        items = Item.objects.filter(type='stray', is_sold=False)
    else:
        items = Item.objects.filter(type='shelter', is_sold=False)
    items_json = json.dumps(list(items.values('id', 'name', 'lat', 'lng')))
    context = {
        "key": key,
        "items_json": items_json
    }

    return render(request, "item/map.html", context)

def detail(request, pk):
    item = get_object_or_404(Item, pk=pk)
    form = RenewItemLocationForm(instance=item)
    related_items = Item.objects.filter(category=item.category, is_sold=False).exclude(pk=pk)[0:3]
    if isinstance(request.user, AnonymousUser):
        related_items = Item.objects.filter(type='shelter', is_sold=False)
    elif request.user.userstatus == 'corporate':
        related_items = Item.objects.filter(type='stray', is_sold=False)
    else:
        related_items = Item.objects.filter(type='shelter', is_sold=False)
    
    likes_connected = get_object_or_404(Item, id=pk)
    liked = False
    if likes_connected.likes.filter(id=request.user.id).exists():
        liked = True

    context = {
        'item': item,
        'form': form,
        'related_items': related_items,
    }
    return render(request, 'item/detail.html', context)

@login_required
def new(request):
    if request.method == 'POST':
        form = NewItemForm(request.POST, request.FILES)

        if form.is_valid():
            latitude = request.POST.get('latitude')
            longitude = request.POST.get('longitude')

            item = form.save(commit=False)
            item.created_by = request.user
            item.lat=latitude
            item.lng=longitude
            item.save()

            return redirect('item:detail', pk=item.id)
    else:
        form = NewItemForm()

    return render(request, 'item/form.html', {
        'form': form,
        'title': 'New item',
    })

@login_required
@require_POST
def renew_location(request, pk):
    item = get_object_or_404(Item, pk=pk)
    latitude = request.POST.get('latitude')
    longitude = request.POST.get('longitude')
    
    if latitude and longitude:
        item.lat = latitude
        item.lng = longitude
        item.save()
        return JsonResponse({'status': 'success'})
    else:
        return JsonResponse({'status': 'error', 'message': 'Invalid latitude or longitude'})


@login_required
def edit(request, pk):
    item = get_object_or_404(Item, pk=pk, created_by=request.user)

    if request.method == 'POST':
        form = EditItemForm(request.POST, request.FILES, instance=item)

        if form.is_valid():
            form.save()

            return redirect('item:detail', pk=item.id)
    else:
        form = EditItemForm(instance=item)

    return render(request, 'item/form.html', {
        'form': form,
        'title': 'Edit item',
    })



@login_required
def delete(request, pk):
    item = get_object_or_404(Item, pk=pk, created_by=request.user)
    item.delete()

    return redirect('dashboard:index')

@login_required
def like_item(request, pk):
    post = get_object_or_404(Item, id=request.POST.get('item_id'))
    if post.likes.filter(id=request.user.id).exists():
        post.likes.remove(request.user)
    else:
        post.likes.add(request.user)

    return HttpResponseRedirect(reverse('item:detail', args=[str(pk)]))