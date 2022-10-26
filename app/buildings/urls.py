from rest_framework.routers import SimpleRouter
from buildings.views import BuildingApiView

app_name = "building"

router = SimpleRouter()
router.register("building", BuildingApiView, basename="building")
urlpatterns = router.urls
