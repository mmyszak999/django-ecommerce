from django import forms
from django.db.models import Case, When, F, Avg
from django.db import models
from django_filters import rest_framework as filters
from src.apps.products.models import Product, ProductCategory


class ProductFilter(filters.FilterSet):
    name = filters.LookupChoiceFilter(
        field_class=forms.CharField, lookup_choices=[("exact", "Equals")]
    )
    category = filters.ModelMultipleChoiceFilter(
        queryset=ProductCategory.objects.all(),
        field_name="category__name",
        to_field_name="name",
    )
    price = filters.LookupChoiceFilter(
        field_class=forms.DecimalField,
        lookup_choices=[
            ("exact", "Equals"),
            ("gt", "Greater than"),
            ("lt", "Less than"),
        ],
    )
    description = filters.LookupChoiceFilter(
        field_class=forms.CharField,
        lookup_choices=[
            ("exact", "Equals"),
            ("contains", "Contains"),
        ],
    )

    o = filters.OrderingFilter(
        fields=(
            ("name", "name"),
            ("category__name", "name"),
            ("price", "price"),
        ),
        field_labels={
            "category__name": "Category Name",
        },
    )

    class Meta:
        model = Product
        fields = [
            "category",
            "price",
        ]
