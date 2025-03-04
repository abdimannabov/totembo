from django import template
from shop.models import Category, Like

register = template.Library()

@register.simple_tag()
def get_categories():
    return Category.objects.all()

@register.simple_tag()
def get_filter():
    filters = [
        {
            "title":"Price",
            "filters":[
                ["-price", "high to low"],
                ["price", "low to high"],
            ]
        },
        {
            "title": "Name",
            "filters": [
                ["-title", "A to Z"],
                ["title", "Z to A"],
            ]
        },
        {
            "title": "Size",
            "filters": [
                ["-size", "high to low"],
                ["size", "low to high"],
            ]
        },
        {
            "title": "Color",
            "filters": [
                ["-color", "A to Z"],
                ["color", "Z to A"],
            ]
        }
    ]
    return filters

@register.simple_tag()
def get_like(user):
    likes = Like.objects.filter(user=user)
    products = [i.product for i in likes]
    return products