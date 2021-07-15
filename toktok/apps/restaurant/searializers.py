from rest_framework import serializers
from toktok.apps.restaurant.models import Food
from toktok.apps.imagegallery.models import Image


class FoodSerializer(serializers.ModelSerializer):
    cover_image = serializers.SerializerMethodField()

    class Meta:
        fields = ('id','sku','description', 'cover_image', 'manager', 'amountInCents', "MenuCollection","subtypes", "addons") 

    def get_photo_url(self, food):
        request = self.context.get('request')
        cover_image = food.image.url
        return request.build_absolute_uri(cover_image)