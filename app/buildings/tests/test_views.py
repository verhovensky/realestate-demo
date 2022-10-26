from collections import OrderedDict
from django.urls import reverse
from rest_framework.test import APITestCase
from buildings.models import Building
from buildings.serializers import BuildingREADSerializer


class TestCreateBuilding(APITestCase):

    @classmethod
    def setUpTestData(cls):
        cls.url = reverse("building:building-list")
        cls.data = {"name": "ЖК Солнцево",
                    "year": 2018,
                    "quarter": 2,
                    "builder": "ГК Самолет"}

    def test_create_valid_year(self):
        """ In loop create valid years """
        resp = self.client.post(self.url,
                                data=self.data)
        self.assertEqual(resp.status_code, 201)
        new_data = self.data
        for _ in (2019, 2020, 2021, 2022):
            new_data.update({"year": _})
            resp = self.client.post(self.url,
                                    data=new_data)
            self.assertEqual(resp.status_code, 201)

    def test_create_wrong_year(self):
        """ In loop create for past and future years """
        new_data = self.data
        for _ in (2023, 2024, 2016, 2015):
            new_data.update({"year": _})
            resp = self.client.post(self.url,
                                    data=new_data)
            self.assertEqual(resp.status_code, 400)
            self.assertIn("year", resp.data)

    def test_create_valid_quarter(self):
        new_data = self.data
        """ In loop create for valid quarters """
        for _ in (1, 3, 4):
            new_data.update({"quarter": _})
            resp = self.client.post(self.url,
                                    data=new_data)
            self.assertEqual(resp.status_code, 201)

    def test_create_invalid_quarter(self):
        """ Invalid quarters, including 0 """
        new_data = self.data
        """ In loop create for valid quarters """
        for _ in (0, 5, 6, 7):
            new_data.update({"quarter": _})
            resp = self.client.post(self.url,
                                    data=new_data)
            self.assertEqual(resp.status_code, 400)
            self.assertIn("quarter", resp.data)

    def test_create_unique(self):
        resp = self.client.post(self.url,
                                data=self.data)
        self.assertEqual(resp.status_code, 201)
        resp2 = self.client.post(self.url, data=self.data)
        self.assertEqual(resp2.status_code, 400)
        self.assertEqual(resp2.data["non_field_errors"][0],
                         "Этот ЖК уже есть в базе")


class TestUpdateBuilding(APITestCase):

    fixtures = ["test_building.json"]

    @classmethod
    def setUpTestData(cls):
        cls.url = reverse("building:building-detail",
                          kwargs={"pk": 1})

    def test_update(self):
        resp = self.client.put(
            self.url,
            data={"name": "ЖК Молонево",
                  "year": 2019,
                  "quarter": 1,
                  "builder": "ГК Вертолет"})
        self.assertEqual(resp.status_code, 200)

    def test_partial_update(self):
        resp = self.client.patch(
            self.url,
            data={"name": "ЖК Молонево"})
        self.assertEqual(resp.status_code, 200)


class TestRetrieveBuilding(APITestCase):

    fixtures = ["test_building.json"]

    @classmethod
    def setUpTestData(cls):
        cls.url_detail = reverse("building:building-detail",
                                 kwargs={"pk": 1})
        cls.url_list = reverse("building:building-list")
        cls.building = Building.objects.first()

    def test_retrieve(self):
        resp = self.client.get(self.url_detail)
        self.assertEqual(resp.status_code, 200)
        obj = BuildingREADSerializer(self.building).data
        self.assertEqual(resp.data, obj)

    def test_list(self):
        resp = self.client.get(self.url_list)
        self.assertEqual(resp.status_code, 200)
        obj = BuildingREADSerializer(self.building).data
        self.assertEqual(resp.data[0], OrderedDict(obj))


class TestDeleteBuilding(APITestCase):

    fixtures = ["test_building.json"]

    @classmethod
    def setUpTestData(cls):
        cls.url = reverse("building:building-detail",
                          kwargs={"pk": 1})

    def test_delete(self):
        resp = self.client.delete(self.url)
        self.assertEqual(resp.status_code, 204)
