from .models import Shirt, Image, PrintType, Brand, Size, Inventory
from rest_framework import serializers
from rest_framework.reverse import reverse
from versatileimagefield.serializers import VersatileImageFieldSerializer


class InventorySerializer(serializers.ModelSerializer):
	size = serializers.CharField(source='size.name', read_only=True)
	
	class Meta:
		model = Inventory
		fields = ['size', 'stock']
		
		
class ImageSerializer(serializers.ModelSerializer):
	image = VersatileImageFieldSerializer(
		sizes = 'image_size'
		)
	
	class Meta:
		model = Image
		fields = ['image', 'weight']
		
	
class ShirtSerializer(serializers.ModelSerializer):
	'''
	def to_representation(self, obj):
		return '%s, %d, %d, %d, %d, %d' % (obj.date, obj.price_open, obj.price_close, obj.price_high, obj.price_low, obj.volume)
	'''
	inventory = InventorySerializer(many=True, read_only=True)
	image = ImageSerializer(many=True, read_only=True)

	class Meta:
		model = Shirt
		fields = ['code', 'name', 'price', 'description', 'image', 'inventory']
		depth = 1

