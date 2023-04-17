import dlib
import datetime


class FaceDetector:

    def __init__(self):
        self._model = None
        self.detector = dlib.get_frontal_face_detector()

    @staticmethod
    def preview_result(dets, filepath, img):
        win = dlib.image_window()
        win.set_title("Please close after confirming. filepath: {}".format(filepath))
        win.clear_overlay()
        win.set_image(img)
        win.add_overlay(dets)
        win.wait_until_closed()

    def process_img(self, img):
        if len(img) > 0:
            dets, scores, idx = self.detector.run(img, 1, -1)
            detected = []
            for i, d in enumerate(dets):
                detected.append("Detection {}, score: {}, face_type:{}".format(
                    d, scores[i], idx[i]))
            return detected
