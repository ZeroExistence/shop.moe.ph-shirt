from django.contrib import admin
from .models import Brand, PrintType, Shirt, Image, Inventory, Size, Gallery

# Register your models here.

admin.site.register(Brand)
admin.site.register(PrintType)
admin.site.register(Image)
admin.site.register(Inventory)
admin.site.register(Size)
admin.site.register(Gallery)


class ImageInline(admin.TabularInline):
    model = Image
    extra = 0


class InventoryInline(admin.TabularInline):
    model = Inventory
    extra = 0


class GalleryInline(admin.TabularInline):
    model = Gallery
    extra = 0


class ShirtModelAdmin(admin.ModelAdmin):
    inlines = [ImageInline, InventoryInline, GalleryInline]

    list_display = ('name', 'get_available_sizes', 'get_print_type', 'get_shirt_brand')

    def save_model(self, request, obj, form, change):
        obj.save()

        for afile in request.FILES.getlist('image_multiple_image'):
            obj.image.create(image=afile)

        for afile in request.FILES.getlist('image_multiple_gallery'):
            obj.gallery.create(image=afile)

admin.site.register(Shirt, ShirtModelAdmin)
#admin.site.register(Image)