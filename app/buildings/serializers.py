from datetime import date
from rest_framework.serializers import ModelSerializer, \
    ChoiceField, CharField, ValidationError
from buildings.models import Building


class BuildingREADSerializer(ModelSerializer):
    class Meta:
        model = Building
        fields = "__all__"


class BuildingWRITESerializer(ModelSerializer):
    class Meta:
        model = Building
        fields = "__all__"

    year = ChoiceField(choices=[
        (r, r) for r in range(2017,
                              date.today().year + 1)],
                       required=True)
    quarter = ChoiceField(choices=(1, 2, 3, 4),
                          required=True)

    def validate(self, attrs):
        name = attrs.get('name')
        year = attrs.get('year')
        quarter = attrs.get('quarter')
        builder = attrs.get('builder')

        if Building.objects.filter(
            name=name, year=year,
                quarter=quarter, builder=builder).exists():
            raise ValidationError("Этот ЖК уже есть в базе")

        return super().validate(attrs)
