from django.contrib import admin
from .models import MenuItem, Menu


class MenuItemInLine(admin.TabularInline):
    model = MenuItem
    exclude = ['level']


@admin.register(Menu)
class MenuAdmin(admin.ModelAdmin):
    inlines = [MenuItemInLine]


@admin.register(MenuItem)
class MenuItemAdmin(admin.ModelAdmin):
    pass
