from django import template
from menu.models import Menu, MenuItem


register = template.Library()


# Колхозный метод. Переделать
# Тут нужно рекурсивно доставать всех потомка
def sub_items(menu, menu_item, data=None):
    data2 = []
    for sub_item in menu.filter(parent_menu_item=menu_item):
        print(f"-{sub_item.title}")
        data2.append(sub_item)
        return sub_items(menu, sub_item, data2)
    if len(data2) == 0:
        return data


@register.inclusion_tag('menu/tree_menu.html')
def draw_menu(menu_title: str):
    menu = MenuItem.objects.filter(parent_menu__title=menu_title)
    menu_items = {}
    for item in menu.filter(parent_menu_item=None):
        print(item.title)
        sub_items(menu, item)
    return {"menu": menu}
