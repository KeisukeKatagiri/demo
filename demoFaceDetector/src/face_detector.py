import dlib
import os


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

            # dictionary type
            detected = {}
            for i, d in enumerate(dets):
                detected.setdefault("Detection", []).append(str(d))
                detected.setdefault("score", []).append(scores[i])
                detected.setdefault("face_type", []).append(idx[i])

            return detected

    @staticmethod
    def set_image_file_path(base_dir, extract_image_paths):
        face_images = [[], []]
        for image_path in extract_image_paths:
            sep_path = image_path.split(base_dir.stem)[-1].split(os.sep)

            if len(sep_path) == 2:
                face_images[0].append(image_path)

            elif len(sep_path) == 3:
                face_images[1].append(image_path)
        return face_images
