from rest_framework import serializers
from .models import Orders,Grade, Chat, Performers, User

class OrdersSerialize(serializers.ModelSerializer):
    sender = serializers.SlugRelatedField(many=False, slug_field='city',read_only=True)
    receiver = serializers.SlugRelatedField(many=False, slug_field='city',read_only=True)
    type = serializers.SlugRelatedField(many=False, slug_field='type',read_only=True)
    timestamp = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S")

    class Meta:
        model = Orders
        fields=['title','sender', 'receiver','text','id','timestamp','tonnage','type','bid']

class GradeSerialize(serializers.ModelSerializer):
    comentator = serializers.SlugRelatedField(many=False,slug_field="username",read_only =True)
    class Meta:
        model = Grade
        fields=['grade','comment','comentator']

class ChatSerialize(serializers.ModelSerializer):
    writer = serializers.SlugRelatedField(many=False, slug_field = "username", read_only=True)
    class Meta:
        model = Chat
        fields=['writer','message','timestamp']


class PerformersSerialize(serializers.ModelSerializer):
    performer = serializers.SlugRelatedField(many=False,slug_field='username' ,read_only = True)
    performer_id = serializers.PrimaryKeyRelatedField(many=False,read_only = True)
    class Meta:
        model = Performers
        fields=['performer','performer_id']