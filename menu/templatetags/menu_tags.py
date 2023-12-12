from django import template
from menu.utils import get_children_menu_items, get_parent_menu_item, get_current_menu_item, get_sorted_menu_items
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


@register.inclusion_tag('menu/tree_menu.html', takes_context=True)
def draw_menu(context, menu_name: str):
    current_item_url = context['menu_item']
    menu = MenuItem.objects.filter(parent_menu__name=menu_name)\
        .select_related('parent_menu_item')

    sorted_menu_items = get_sorted_menu_items(menu[:])
    current_item = get_current_menu_item(current_item_url, sorted_menu_items)
    grouped_menu_items = {}

    for key, group_items in groupby(sorted_menu_items, key=lambda x: x.parent_menu_item):
        tmp_group_items = list(group_items)
        if key in grouped_menu_items:
            grouped_menu_items[key] += list(tmp_group_items)
        else:
            grouped_menu_items[key] = list(tmp_group_items)

    parent_item = get_parent_menu_item(current_item, grouped_menu_items)
    include_menu_items = grouped_menu_items[current_item]

    while True:
        include_menu_items += grouped_menu_items[parent_item]
        parent_item = get_parent_menu_item(parent_item, grouped_menu_items)
        if parent_item is None:
            break

    for i in range(len(sorted_menu_items) - 1, -1, -1):
        if sorted_menu_items[i].level > 0 and sorted_menu_items[i] not in include_menu_items:
            sorted_menu_items.pop(i)

    # print(lst, tmp_menu)
    return {"menu":  sorted_menu_items}
