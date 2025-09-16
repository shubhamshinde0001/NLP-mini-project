from rest_framework import serializers
from .models import FirstAidGuide

class FirstAidGuideSerializer(serializers.ModelSerializer):
    class Meta:
        model = FirstAidGuide
        fields = "__all__"
