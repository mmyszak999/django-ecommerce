from django import forms
from django.db import models
from django_filters import rest_framework as filters
from src.apps.orders.models import Order


class OrderFilter(filters.FilterSet):
    order_place_date = filters.LookupChoiceFilter(
        field_class=forms.DateTimeField,
        lookup_choices=[
            ("exact", "Equals"),
            ("gt", "Greater than"),
            ("lt", "Less than"),
        ],
    )
    payment_deadline = filters.LookupChoiceFilter(
        field_class=forms.DateTimeField,
        lookup_choices=[
            ("exact", "Equals"),
            ("gt", "Greater than"),
            ("lt", "Less than"),
        ],
    )
    
    o = filters.OrderingFilter(
        fields=(
            ('order_place_date', 'order_place_date'),
            ('payment_deadline', 'payment_deadline'),
        ),)
    

    class Meta:
        model = Order
        fields = [
            "order_place_date",
            "payment_deadline"
        ]