import csv
import datetime

FIELD_NAME = ["filename",
              "number of faces",
              "detected faces",
              "detection position",
              "start time",
              "end time"
              ]
RESULT_KEYS = ["start time",
               "filename",
               "number of faces",
               "detected faces",
               "detection position",
               "end time"
               ]


class FileWriter:
    @staticmethod
    def writeheader_to_csv(csv_file_name):
        with open(csv_file_name, mode='a', encoding='utf-8', newline='') as f:
            writer = csv.DictWriter(f, fieldnames=FIELD_NAME)
            writer.writeheader()

    @staticmethod
    def convert_to_csv(csv_file_name, result):
        with open(csv_file_name, mode='a', encoding='utf-8', newline='') as f:
            writer = csv.DictWriter(f, fieldnames=FIELD_NAME)
            writer.writerow(result)

    @staticmethod
    def set_detection_position(dets):
        detection_position = {}
        for i, d in enumerate(dets):
            detection_position.setdefault("Detection", []).append(i)
            detection_position.setdefault("Left", []).append(d.left())
            detection_position.setdefault("Top", []).append(d.top())
            detection_position.setdefault("Right", []).append(d.right())
            detection_position.setdefault("Bottom", []).append(d.bottom())
        return detection_position

    @staticmethod
    def dictionary_update(image, dets_len, detected_face, detection_position, result, start_time):
        result["start time"] = start_time
        result["filename"] = image
        result["number of faces"] = dets_len
        result["detected faces"] = detected_face
        result["detection position"] = detection_position
        result["end time"] = datetime.datetime.now().isoformat()
        return result
