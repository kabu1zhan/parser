from rest_framework.serializers import Serializer, ModelSerializer
from rest_framework import serializers
from .models import Group, Comments, User, BadWord, BadData

class GroupSerializer(ModelSerializer):
    class Meta:
        model = Group
        fields = '__all__'


class CommentSerializer(ModelSerializer):
    class Meta:
        model = Comments
        fields = '__all__'


class UserSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'


class TextSerializer(Serializer):
    text = serializers.CharField()


class TitleSerializer(Serializer):
    title = serializers.CharField()


class NumberSerializer(Serializer):
    number = serializers.CharField()


class BadWordSerializer(ModelSerializer):
    class Meta:
        model = BadWord
        fields = '__all__'


class BadDataSerializer(ModelSerializer):
    class Meta:
        model = BadData
        fields = '__all__'


class ValuesSerializer(Serializer):
    varianty = serializers.CharField()

class IdSerializer(Serializer):
    user_id = serializers.IntegerField()