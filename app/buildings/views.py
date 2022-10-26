from rest_framework.viewsets import ModelViewSet
from buildings.serializers import BuildingREADSerializer, \
    BuildingWRITESerializer
from buildings.models import Building


class BuildingApiView(ModelViewSet):
    queryset = Building.objects.all()

    def get_serializer_class(self):
        if self.request.method in ("PUT", "PATCH", "POST"):
            return BuildingWRITESerializer
        return BuildingREADSerializer
