import datetime
from src.face_detector import FaceDetector
import tkinter as tk
from src.path_handler import PathHandler
from tkinter.messagebox import showinfo
import dlib
from src.file_writer import FileWriter

EXTENSIONS = {'.jpg', '.png'}
CSV_FILE_TYPE = [("csv files", "*.csv")]
RESULT_KEYS = ["start time",
               "filename",
               "number of faces",
               "detected faces",
               "detection position",
               "end time"
               ]


def run(path_handler: PathHandler, face_rec: FaceDetector):
    face_images = face_rec.set_image_file_path(path_handler.base_dir,
                                               path_handler.extract_image_paths(is_pairs=False)
                                               )

    # OUTPUT
    # Write field names(header) to csv.
    FileWriter.writeheader_to_csv(path_handler.csv_file_name)

    for images in face_images:
        for image in images:
            result = dict.fromkeys(RESULT_KEYS)
            start_time = datetime.datetime.now().isoformat()

            raw_image = dlib.load_rgb_image(image)
            dets = face_rec.detector(raw_image, 1)
            detected_face = face_rec.process_img(raw_image)
            detection_position = FileWriter.set_detection_position(dets)

            result = FileWriter.dictionary_update(image, len(dets), detected_face, detection_position,
                                                  result, start_time)
            face_rec.preview_result(dets, image, raw_image)

            # OUTPUT
            # convert result(dict) to csv.
            FileWriter.convert_to_csv(path_handler.csv_file_name, result)

    showinfo(message='The process completed!')


def toggle_btn_status():
    is_text_box_dir = text_box_dir.get(1.0, tk.END)
    is_text_box_csv = text_box_csv.get(1.0, tk.END)

    if len(is_text_box_csv) > 1 and len(is_text_box_dir) > 1:
        start_btn['state'] = tk.NORMAL


# Tkinter
path_handler = PathHandler()
path_handler.extensions = EXTENSIONS

face_detector = FaceDetector()

root = tk.Tk()
root.title('Model Validation')
root.geometry('+%d+%d' % (350, 10))  # place GUI at x=350, y=10
root.resizable(False, False)  # maximize disabled
root.configure(bg="#F4F4F4", bd=20)  # window background color and border width
frame = tk.Frame(root,
                 width=750,
                 height=400,
                 bg="white")
frame.grid(columnspan=3,
           rowspan=3)

# browse target dir
instruction_dir = tk.Label(root,
                           text="Choose target directory\nターゲット ディレクトリを選択",
                           anchor='center',
                           width=20,
                           bg="#CCCCCC",
                           justify='left')
instruction_dir.grid(column=0,
                     row=0,
                     padx=50)

text_box_dir = tk.Text(root,
                       height=2,
                       width=40,
                       wrap=tk.WORD,
                       bg="#f4f4f4",
                       state=tk.DISABLED)
text_box_dir.grid(column=1,
                  row=0)

browse_dir_text = tk.StringVar()
browse_dir_btn = tk.Button(root, textvariable=browse_dir_text,
                           relief=tk.RAISED,
                           bd=5,
                           command=lambda: path_handler.load_target_dir_callback(
                               text_box=text_box_dir,
                               switch=toggle_btn_status
                           ),
                           height=2,
                           width=15,
                           bg="#cccccc")
browse_dir_text.set("Browse")
browse_dir_btn.grid(column=2,
                    row=0,
                    padx=50)

# browse csv file
instruction_csv = tk.Label(root,
                           text="Choose csv file\ncsvファイルを選択",
                           anchor='center',
                           width=20,
                           bg="#CCCCCC",
                           justify='left')
instruction_csv.grid(column=0,
                     row=1,
                     padx=50)

text_box_csv = tk.Text(root,
                       height=2,
                       width=40,
                       wrap=tk.WORD,
                       bg="#f4f4f4",
                       state=tk.DISABLED)
text_box_csv.grid(column=1,
                  row=1)

browse_csv_text = tk.StringVar()
browse_csv_btn = tk.Button(root, textvariable=browse_csv_text,
                           relief=tk.RAISED,
                           bd=5,
                           command=lambda: path_handler.set_file_callback(
                               text_box=text_box_csv,
                               switch=toggle_btn_status,
                               file_type=CSV_FILE_TYPE
                           ),
                           height=2,
                           width=15,
                           bg="#cccccc")
browse_csv_text.set("Browse")
browse_csv_btn.grid(column=2,
                    row=1,
                    padx=50)

# run
start_text = tk.StringVar()
start_btn = tk.Button(root, textvariable=start_text,
                      relief=tk.RAISED,
                      bd=5,
                      command=lambda: run(path_handler,
                                          face_detector),
                      height=2,
                      width=15,
                      bg="#cccccc",
                      state=tk.DISABLED)
start_text.set("Run")
start_btn.grid(column=2,
               row=2,
               padx=50)

root.mainloop()
