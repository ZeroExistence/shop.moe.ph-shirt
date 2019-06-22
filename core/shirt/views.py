from django.shortcuts import render
from django.views import generic
from django.http import Http404

# Create your views here.

from .models import Shirt, Image, PrintType, Brand, Size, Inventory

class ShirtListView(generic.ListView):
    model = Shirt
    paginate_by = 6


class FullShirtView(generic.ListView):
    model = Shirt


class ShirtDetailView(generic.DetailView):
    model = Shirt

    def get_object(self):
        try:
            return Shirt.objects.get(code=self.kwargs['shirt'])
        except Shirt.DoesNotExist:
            raise Http404()

    # Trying to modify the context using the request. Not working. WIP
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.GET.get('amp', 0) == "1":
            context['base_template'] = "amp-base.html"
        else:
            context['base_template'] = "base.html"
        return context


class PrintShirtView(generic.ListView):
    model = Shirt

    def get_queryset(self):
        try:
            return Shirt.objects.filter(print_type__code__exact=self.kwargs['print'])
        except Shirt.DoesNotExist:
            raise Http404()


class PrintTypeView(generic.ListView):
    model = PrintType


class BrandShirtView(generic.ListView):
    model = Shirt

    def get_queryset(self):
        try:
            return Shirt.objects.filter(shirt_brand__code__exact=self.kwargs['brand'])
        except Shirt.DoesNotExist:
            raise Http404()


class BrandView(generic.ListView):
    model = Brand


class SizeShirtView(generic.ListView):
    model = Shirt

    def get_queryset(self):
        try:
            return Shirt.objects.filter(inventory__size__code__exact=self.kwargs['size'], inventory__stock__gt=0)
        except Shirt.DoesNotExist:
            raise Http404()


class SizeView(generic.ListView):
    model = Size