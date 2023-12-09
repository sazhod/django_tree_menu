from django import template
from menu.models import Menu, MenuItem


register = template.Library()


def rec_func(current, childs):
    data = {
        'current_object': current,
        'child_objects': []
    }
    if childs is None or len(childs) == 0:
        return data
    for i in range(len(childs)-1, -1, -1):
        if childs[i].parent_menu_item == current:
            new_current = childs[i]
            childs.remove(childs[i])
            data['child_objects'].append(rec_func(new_current, childs[:]))
    return data



@register.inclusion_tag('menu/tree_menu.html')
def draw_menu(menu_name: str):
    # menu = MenuItem.objects.filter(parent_menu__name=menu_name) \
    #     .select_related('parent_menu_item', 'parent_menu_item__title') \
    #     .values('id', 'title', 'parent_menu_item', 'parent_menu_item__title')
    menu = MenuItem.objects.filter(parent_menu__name=menu_name)\
        .select_related('parent_menu_item')
    childs = []
    parents = []

    for item in menu:
        if item.parent_menu_item is not None:
            childs.append(item)
        else:
            parents.append(item)
    # childs = sorted(childs, key=lambda d: d['parent_menu_item'])
    # parents = sorted(parents, key=lambda d: d['id'])
    result = {
        'current_object': None,
        'child_objects': []
    }
    for parent in parents:
        result['child_objects'].append(rec_func(parent, childs[:]))
    return {"menu": {"parent": parents, "child": childs, "menu": menu, 'result': result}}



# def show_sub_items(menu, menu_item, data=None, sub_level=0):
#     data2 = []
#     if menu_item is None:
#         return data
#     sub_level += 1
#     for sub_item in menu.filter(parent_menu_item=menu_item):
#         print(f"{'-'*sub_level}{sub_item.title}")
#         data2.append(sub_item)
#         show_sub_items(menu, sub_item, data2, sub_level)
#     return data
#
#
# @register.inclusion_tag('menu/tree_menu.html')
# def draw_menu(menu_name: str):
#     menu = MenuItem.objects.filter(parent_menu__name=menu_name).select_related('parent_menu_item').values()
#     menu_items = {}
#     for item in menu:
#         print(item.title)
#         show_sub_items(menu, item)
#     return {"menu": menu}
