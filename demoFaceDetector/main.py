import json
import os
from src.face_detector import FaceDetector
import csv
import tkinter as tk
from src.path_handler import PathHandler
from tkinter.messagebox import showinfo
import datetime
import dlib

EXTENSIONS = {'.jpg', '.png'}
CSV_FILE_TYPE = [("csv files", "*.csv")]


def run(path_handler: PathHandler, face_rec: FaceDetector):
    base_dir = path_handler.base_dir
    face_images = [[], []]
    for image_path in path_handler.extract_image_paths(is_pairs=False):
        sep_path = image_path.split(base_dir.stem)[-1].split(os.sep)

        if len(sep_path) == 2:
            face_images[0].append(image_path)

        elif len(sep_path) == 3:
            face_images[1].append(image_path)

    # OUTPUT
    field_name = ["filename",
                  "number of faces",
                  "detected faces",
                  "detection position",
                  "start time",
                  "end time"]
    # Write field names(header) to csv.
    with open(path_handler.csv_file_name, mode='a', encoding='utf-8', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=field_name)
        writer.writeheader()

    for images in face_images:
        for image in images:
            result = {}
            result["start time"] = datetime.datetime.now().isoformat()
            result["filename"] = image

            raw_image = dlib.load_rgb_image(image)
            dets = face_rec.detector(raw_image, 1)
            detected_face = face_rec.process_img(raw_image)

            result["number of faces"] = len(dets)
            result["detected faces"] = detected_face

            # dictionary type
            detection_position = {}
            for i, d in enumerate(dets):
                detection_position.setdefault("Detection", []).append(i)
                detection_position.setdefault("Left", []).append(d.left())
                detection_position.setdefault("Top", []).append(d.top())
                detection_position.setdefault("Right", []).append(d.right())
                detection_position.setdefault("Bottom", []).append(d.bottom())

            result["detection position"] = detection_position
            result["end time"] = datetime.datetime.now().isoformat()

            face_rec.preview_result(dets, image, raw_image)

            # convert result(dict) to csv or dataframe or json or whatever you please.
            # convert result(dict) to csv.
            with open(path_handler.csv_file_name, mode='a', encoding='utf-8', newline='') as f:
                writer = csv.DictWriter(f, fieldnames=field_name)
                writer.writerow(result)

            if path_handler.check_box_status:
                # convert result(dict) to json.
                json_name = str(path_handler.csv_file_name).replace('.csv', '.json')
                with open(json_name, mode='a', encoding='utf-8', newline='') as f:
                    json.dump(result, f, indent=2)

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

# create JSON file
chk_bln = tk.BooleanVar()
create_json = tk.Checkbutton(root,
                             text="Create JSON file""\n(Create Json with the same file name as CSV)"
                                  "\nJSonファイルの作成\n(CSVと同じファイル名でJson作成)",
                             variable=chk_bln,
                             command=lambda: path_handler.set_checkbutton_callback(
                                 check_status=chk_bln.get()
                             ),
                             bg="White",
                             justify='left'
                             )
create_json.grid(column=1,
                 row=2,
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
