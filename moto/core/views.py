from django.shortcuts import render, redirect
from item.models import Category, Item
from django.contrib.auth import logout
from django.views import View
from django.contrib.auth.models import AnonymousUser
from django.contrib.auth.decorators import login_required

from .forms import SignupForm

def index(request):
    items = Item.objects.filter(is_sold=False)[0:6]
    categories = Category.objects.all() 
    if isinstance(request.user, AnonymousUser):
        items = Item.objects.filter(type='shelter', is_sold=False)[0:6]
    elif request.user.userstatus == 'corporate':
        items = Item.objects.filter(type='stray', is_sold=False)[0:6]
    else:
        items = Item.objects.filter(type='shelter', is_sold=False)[0:6]

    return render(request, 'core/index.html', {
        'categories': categories,
        'items': items,
    })


@login_required
def logout_check(request):

    return render(request, 'core/logout.html',)

def signup(request):
    if request.method == 'POST':
        form = SignupForm(request.POST)

        if form.is_valid():
            form.save()

            return redirect('/login/')
    else:
        form = SignupForm()

    return render(request, 'core/signup.html', {
        'form': form
    })

@login_required
class LogoutView(View):
    def post(self, request, *args, **kwargs):
        logout(request)
        return redirect('') 

