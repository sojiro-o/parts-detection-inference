import json
import unittest
import io
import api_server
import sys
sys.path.append("../test_images")

class TestFlasker(unittest.TestCase):
    def setUp(self):
        self.app = api_server.app.test_client()
        self.oid = None

    def test_01_status(self):
        response = self.app.get("/api/status")
        assert response.status_code == 200
        print(response.get_data(as_text=True))
        out = json.loads(response.get_data(as_text=True))
        assert out["status"] == "ok"

    def test_02_predict_get(self):
        get_response = self.app.get("/api/predict")
        assert get_response.status_code == 200

    def test_03_predict_jpg_post(self):
        with open("test_images/121_f7.jpg", 'rb') as f:
            binary = f.read()
        post_response = self.app.post("/api/predict", data={"file" :  (io.BytesIO(binary), "test.jpg")}, content_type='multipart/form-data')
        assert post_response.status_code == 200

    def test_04_nofile_post(self):
        no_file_response = self.app.post("/api/predict", data={"file" : None}, content_type='multipart/form-data')
        assert no_file_response.json["message"] is not None
        assert no_file_response.status_code == 200

    def test_05_notjpg_post(self):
        not_image_response = self.app.post("/api/predict", data={"file" :  (io.BytesIO(b"test"), "test.txt")}, content_type='multipart/form-data')
        assert not_image_response.json["message"] is not None
        assert not_image_response.status_code == 200
