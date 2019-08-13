"""core URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic import RedirectView
from graphene_django.views import GraphQLView
from core.shirt import views

from rest_framework import routers

router = routers.DefaultRouter()
router.register(r'shirt', views.ShirtViewSet)

urlpatterns = [
    path('shirt/admin', admin.site.urls),
    path('', RedirectView.as_view(url='/shirt'), name='shirt-root'),
    path('shirt', views.ShirtListView.as_view(), name='shirt-list'),
    path('shirt/all', views.FullShirtView.as_view(), name='full-shirt'),
    path('shirt/print', views.PrintTypeView.as_view(), name='print-type'),
    path('shirt/print/<slug:print>', views.PrintShirtView.as_view(), name='print-shirt'),
    path('shirt/brand', views.BrandView.as_view(), name='brand'),   
    path('shirt/brand/<slug:brand>', views.BrandShirtView.as_view(), name='brand-shirt'),   
    path('shirt/size', views.SizeView.as_view(), name='size'),   
    path('shirt/size/<slug:size>', views.SizeShirtView.as_view(), name='size-shirt'),   
    path('shirt/item/<slug:shirt>', views.ShirtDetailView.as_view(), name='shirt-detail'),
    path('dev/shirt', views.DevShirtListView.as_view(), name='dev-shirt-list'),
    path('dev/shirt/all', views.DevFullShirtView.as_view(), name='dev-full-shirt'),
    path('dev/shirt/item/<slug:shirt>', views.DevShirtDetailView.as_view(), name='dev-shirt-detail'),
    path("shirt/graphql", GraphQLView.as_view(graphiql=True)),
    path('shirt/api/', include(router.urls)),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
