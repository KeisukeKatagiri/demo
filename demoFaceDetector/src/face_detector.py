import dlib
import datetime


class FaceDetector:

    def __init__(self):
        self._model = None
        self.detector = dlib.get_frontal_face_detector()
        self._result = []

    def one_folder(self, images):
        temp_confidence = []
        for n in images[0]:
            dt_now = datetime.datetime.now()
            temp_confidence.append("Execution date and time: {}".format(dt_now))  # Execution date and time 実行日時
            self._result.append([])
            self._result.append(temp_confidence)
            temp_confidence = ["Processing file: {}".format(n)]  # Processing file 処理ファイル名
            self._result.append(temp_confidence)
            temp_confidence = []
            img = dlib.load_rgb_image(n)
            dets = self.detector(img, 1)
            self._process_img(img)
            temp_confidence.append("Number of faces detected: {}".format(len(dets)))
            self._result.append(temp_confidence)
            temp_confidence = []
            for i, d in enumerate(dets):
                temp_confidence.append("Detection {}: Left: {} Top: {} Right: {} Bottom: {}".format(
                    i, d.left(), d.top(), d.right(), d.bottom()))
                self._result.append(temp_confidence)
                temp_confidence = []

            win = dlib.image_window()
            win.set_title("Please close after confirming. file: {}".format(n))
            win.clear_overlay()
            win.set_image(img)
            win.add_overlay(dets)
            win.wait_until_closed()
        return self._result

    def _process_img(self, img):
        if len(img) > 0:
            dets, scores, idx = self.detector.run(img, 1, -1)
            temp_confidence = []
            for i, d in enumerate(dets):
                temp_confidence.append("Detection {}, score: {}, face_type:{}".format(
                    d, scores[i], idx[i]))
                self._result.append(temp_confidence)
                temp_confidence = []
