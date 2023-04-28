import pickle
import unittest
import json
from unittest import TestCase
from src.file_writer import FileWriter
from test_data.const import Const


class TestFileWriter(TestCase):

    def test_set_detection_position(self):
        const = Const()
        for index in range(len(const.PICKLE_LIST)):
            with open(const.PICKLE_LIST[index], 'rb') as f:
                pickle_data = pickle.load(f)
                dets = pickle_data["dets"]
            detection_position = FileWriter.set_detection_position(dets)

            with open(const.JSON_LIST[index], 'r') as f:
                json_data = json.load(f)
            # Compare the obtained "detection_position" with the data in the json file
            self.assertDictEqual(json_data["detection_position"], detection_position)

    def test_dictionary_update(self):
        const = Const()
        for json_file in const.JSON_LIST:
            with open(json_file, 'r') as f:
                json_data = json.load(f)

            resurt = FileWriter.dictionary_update(json_data["image"],
                                                  json_data["len_dets"],
                                                  json_data["detected_face"],
                                                  json_data["detection_position"],
                                                  json_data["result"],
                                                  json_data["start time"])
            # Type check for the configured
            self.assertTrue(isinstance(resurt['detected faces'], dict))
            self.assertTrue(isinstance(resurt['detection position'], dict))
            self.assertTrue(isinstance(resurt['end time'], str))
            self.assertTrue(isinstance(resurt['filename'], str))
            self.assertTrue(isinstance(resurt['number of faces'], int))
            self.assertTrue(isinstance(resurt['start time'], str))


if __name__ == '__main__':
    unittest.main()
