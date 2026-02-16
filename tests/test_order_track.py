import requests
import pytest
from data import data
from helpers.order_helper import generate_order_data

class TestOrderTrack:
    def test_get_order_by_track_success(self):
        order_data = generate_order_data()
        create_response = requests.post(data.BASE_URL + data.ORDERS_CREATE, json=order_data)
        assert create_response.status_code == 201
        track = create_response.json()["track"]
        response = requests.get(data.BASE_URL + data.ORDERS_TRACK, params={"t": track})
        assert response.status_code == 200
        json_response = response.json()
        assert "order" in json_response
        assert json_response["order"]["track"] == track

    def test_get_order_without_track_fails(self):
        response = requests.get(data.BASE_URL + data.ORDERS_TRACK)
        assert response.status_code == 400
        assert response.json()["message"] == data.ORDER_TRACK_MISSING_DATA

    def test_get_order_with_nonexistent_track_fails(self):
        nonexistent_track = 999999999
        response = requests.get(data.BASE_URL + data.ORDERS_TRACK, params={"t": nonexistent_track})
        assert response.status_code == 404
        assert response.json()["message"] == data.ORDER_TRACK_NOT_FOUND