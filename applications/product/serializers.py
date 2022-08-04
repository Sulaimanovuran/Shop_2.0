from django.db.models import Avg, Sum
from rest_framework import serializers

from applications.product.models import Category, Product, Image, Rating, Comment
from applications.spam.tasks import spam_email2


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        print(representation)
        if not instance.parent:
            representation.pop('parent')
        return representation


class ImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Image
        fields = '__all__'


class CommentSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.email')
    # product = serializers.ReadOnlyField()
    # comment = serializers.CharField(min_length=1)

    class Meta:
        model = Comment
        fields = '__all__'

    # def create(self, validated_data):
        # print(validated_data)


class ProductSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.email')
    images = ImageSerializer(many=True, read_only=True)
    comments = CommentSerializer(many=True, read_only=True)

    class Meta:
        model = Product
        fields = '__all__'

    def create(self, validated_data):
        requests = self.context.get('request')
        images = requests.FILES
        product = Product.objects.create(**validated_data)

        for image in images.getlist('images'):
            Image.objects.create(product=product, image=image)
        spam_email2.delay(info=product.name)

        return product

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        # print(instance.likes.)
        representation['likes'] = instance.likes.filter(like=True).count()
        # print('*************************************************')
        # print(instance.ratings.all().last())
        # avg = instance.ratings.values_list('rating', flat=True).aggregate()
        # avg = instance.ratings.aggregate(Avg('rating'))
        #
        # if None not in avg.values():
        #     representation['ratings'] = avg.values()  # round(avg.values())
        # else:
        #     representation['ratings'] = "Рейтинг не указан"
        rating_result = 0
        for rating in instance.ratings.all():
            # print(rating.rating)
            rating_result += int(rating.rating)
        # print(instance.ratings.all().count())
        try:
            representation['rating'] = rating_result / instance.ratings.all().count()
        except ZeroDivisionError:
            # representation['rating'] = 0
            pass
        # TODO: Отобразить рейтинг
        # if instance.comments:
        #     representation['comments'] = instance.comments.values()
        # else:
        #     representation.pop('comments')
        # # print(instance.comments.values())

        return representation


class RatingSerializer(serializers.Serializer):
    rating = serializers.IntegerField(required=True, min_value=1, max_value=5)


