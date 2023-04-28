import json
import pickle
import unittest
from unittest import TestCase
from src.face_detector import FaceDetector
from test_data.const import Const


class TestFaceDetector(TestCase):
    def test_process_img(self):
        face_detector = FaceDetector()
        const = Const()
        for index in range(len(const.PICKLE_LIST)):
            with open(const.PICKLE_LIST[index], 'rb') as f:
                pickle_data = pickle.load(f)
            with open(const.JSON_LIST[index], 'r') as f:
                json_data = json.load(f)
            detected = FaceDetector.process_img(face_detector, pickle_data["raw_image"])
            # Compare the obtained "detected" with the data in the json file
            self.assertDictEqual(detected, json_data["detected_face"])

    def test_set_image_file_path(self):
        const = Const()
        for index in range(len(const.PICKLE_LIST)):
            with open(const.PICKLE_LIST[index], 'rb') as f:
                pickle_data = pickle.load(f)
            with open(const.JSON_LIST[index], 'r') as f:
                json_data = json.load(f)
            face_images = FaceDetector.set_image_file_path(pickle_data["base_dir"],
                                                           json_data["extract_image_paths"])
            # Compare the obtained "face_images" with the data in the json file
            self.assertEqual(json_data["face_images"], face_images)


if __name__ == '__main__':
    unittest.main()
