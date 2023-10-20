from rest_framework import serializers
from .models import Audits


class AuditsSerializers(serializers.ModelSerializer):
    class Meta:
        model = Audits
        fields = '__all__'