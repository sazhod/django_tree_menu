from django import template
from menu.models import Menu, MenuItem


register = template.Library()


@register.inclusion_tag('.html')
def show_categories():
    # cats = Category.objects.all()
    # return {"cats": cats}
    pass
