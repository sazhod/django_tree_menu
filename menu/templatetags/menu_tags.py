from django import template
from menu.models import Menu, MenuItem
from itertools import groupby



register = template.Library()


def func1(menu_items: list, sorted_menu_items: list, current_menu_item: MenuItem):
    for i in range(len(menu_items) - 1, -1, -1):
        print(current_menu_item.parent_menu_item, menu_items[i].parent_menu_item)
        if current_menu_item.parent_menu_item == menu_items[i].parent_menu_item:
            current_menu_item = menu_items.pop(i)
            sorted_menu_items.insert(0, current_menu_item)
    return sorted_menu_items


def get_tree_menu(menu_items: list, selected_url: str) -> list:
    sorted_menu_items = []
    selected_menu_item = None

    for i in range(len(menu_items)-1, -1, -1):
        if menu_items[i].url == selected_url:
            selected_menu_item = menu_items.pop(i)
            sorted_menu_items.insert(0, selected_menu_item)
            break

    current_menu_item = selected_menu_item
    for i in range(len(menu_items) - 1, -1, -1):
        if current_menu_item.parent_menu_item == menu_items[i].parent_menu_item:
            current_menu_item = menu_items.pop(i)
            sorted_menu_items.insert(0, current_menu_item)

    current_menu_item = selected_menu_item
    for i in range(len(menu_items)-1, -1, -1):
        if current_menu_item.parent_menu_item == menu_items[i]:
            current_menu_item = menu_items.pop(i)
            sorted_menu_items.insert(0, '_')
            sorted_menu_items.insert(0, current_menu_item)

    return sorted_menu_items


@register.inclusion_tag('menu/tree_menu.html', takes_context=True)
def draw_menu(context, menu_name: str):
    # print(context['menu_item'])
    menu = MenuItem.objects.filter(parent_menu__name=menu_name)\
        .select_related('parent_menu_item')
    children = []
    parents = []

    for item in menu:
        if item.parent_menu_item is not None:
            children.append(item)
        else:
            parents.append(item)
    # print(children, parents)
    result = {
        'current_object': None,
        'children_objects': []
    }
    for parent in parents:
        result['children_objects'].append(get_tree_menu(menu[:], context['menu_item']))

    new_menu = menu[:]
    group_menu = []

    for k, i in groupby(new_menu, lambda x: x.parent_menu_item):
        group_menu += i

    return {"menu": {"parent": parents, "child": children, "menu": menu, 'result': result, 'group_menu': group_menu}}


def get_full_tree_menu(current: MenuItem, children: list) -> dict:
    """
    Рекурсивная функция, которая позволяет отсортировать и получить все MenuItem
    :param current: Текущий MenuItem
    :param children: Список всех MenuItem
    :return: data: dict {
        'current_object': current,
        'children_objects': [...]
    }
    """
    # print(type(current), type(children))
    data = {
        'current_object': current,
        'children_objects': []
    }
    if children is None or not children:
        del data['children_objects']
        return data
    for i in range(len(children) - 1, -1, -1):
        if children[i].parent_menu_item == current:
            new_current = children[i]
            children.remove(children[i])
            data['children_objects'].append(get_full_tree_menu(new_current, children))
    if not data['children_objects']:
        del data['children_objects']
    return data


@register.inclusion_tag('menu/tree_menu.html')
def old_draw_menu(menu_name: str):
    menu = MenuItem.objects.filter(parent_menu__name=menu_name)\
        .select_related('parent_menu_item')
    children = []
    parents = []

    for item in menu:
        if item.parent_menu_item is not None:
            children.append(item)
        else:
            parents.append(item)

    result = {
        'current_object': None,
        'children_objects': []
    }
    for parent in parents:
        result['children_objects'].append(get_full_tree_menu(parent, children[:]))

    group_menu = []
    for key, group_items in groupby(result['children_objects'], key= lambda x: x['current_object'].parent_menu_item):
        group_menu.append(list(group_items))
    return {"menu": {"parent": parents, "child": children, "menu": menu, 'result': result, 'group_menu': group_menu}}
