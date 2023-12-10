from django.shortcuts import render


def index(request, menu_item=None):
    return render(request, 'menu/index.html', {'menu_item': menu_item})
