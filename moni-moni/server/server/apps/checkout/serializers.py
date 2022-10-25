from server.apps.catalogue.models import Fundraiser
from rest_framework import serializers
from server.apps.users.models import CustomUser
from rest_framework import status
from rest_framework.exceptions import ValidationError
from .models import FundingOptions, PaymentSelections


class FundingOptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = FundingOptions
        fields = "__all__"

    def validate(self, attrs):
        fr = Fundraiser.objects.select_related().filter(author=self.context.get("id"))
        if attrs["fundraiser"] not in fr:
            raise ValidationError(
                "Not authorized to edit that fundraiser", status.HTTP_401_UNAUTHORIZED
            )
        return super().validate(attrs)

    def create(self, validated_data):
        option = FundingOptions.objects.create(**validated_data)
        return option


class PaymentSelectionSerializer(serializers.ModelSerializer):
    class Meta:
        model = PaymentSelections
        fields = "__all__"

    def create(self, validated_data):
        selection = PaymentSelections.objects.create(**validated_data)
        return selection
