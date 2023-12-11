from django import template
from menu.models import Menu, MenuItem
from itertools import groupby


register = template.Library()


@register.simple_tag()
def get_tags_for_current_item(current_item: MenuItem, menu_items: list):
    for index, value in enumerate(menu_items):
        if value == current_item:
            break
    count = abs(current_item.level - menu_items[index-1].level)
    tags = ''
    if current_item.level > menu_items[index-1].level:
        tags = '<ul>'
    elif current_item.level < menu_items[index-1].level:
        tags = '</ul>'

    return {'tags': tags * count}


def get_children_menu_items(parent_menu_item: MenuItem, menu: list):
    return [item for item in menu if item.parent_menu_item == parent_menu_item]


@register.inclusion_tag('menu/tree_menu.html', takes_context=True)
def draw_menu(context, menu_name: str):
    current_item_url = context['menu_item']
    menu = MenuItem.objects.filter(parent_menu__name=menu_name)\
        .select_related('parent_menu_item')
    children = []
    parents = []

    for item in menu[:]:
        if item.parent_menu_item is not None:
            children.append(item)
        else:
            parents.append(item)

    tmp_menu = parents[:]
    for index, item in enumerate(tmp_menu):
        for i, new_item in enumerate(get_children_menu_items(item, children[:])):
            tmp_menu.insert(index+i+1, new_item)

    current_item = None
    for i in range(len(tmp_menu)-1, -1, -1):
        if tmp_menu[i-1].url == current_item_url:
            if tmp_menu[i-1].level + 1 == tmp_menu[i].level:
                current_item = tmp_menu[i]
                print(tmp_menu[i].level)

    x = False
    lst = []
    for i in range(len(tmp_menu) - 1, -1, -1):
        if x and tmp_menu[i].level > tmp_menu[i+1].level:
            x = False
        if x:
            lst.append(tmp_menu[i])
        if tmp_menu[i] == current_item:
            x = True
        if tmp_menu[i].level > current_item.level and not x:
            tmp_menu.pop(i)
    # print(tmp_menu)
    print(lst)
    return {"menu":  tmp_menu}
