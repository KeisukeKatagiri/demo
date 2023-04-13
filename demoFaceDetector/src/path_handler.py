import functools
import os
from pathlib import Path
from tkinter import filedialog
import tkinter as tk


def toggle_text_box(f):
    @functools.wraps(f)
    def _wrapper(*args, **kwargs):
        text_box = kwargs['text_box']
        switch = kwargs['switch']
        text_box['state'] = tk.NORMAL
        text_box.delete(1.0, tk.END)

        text = f(*args, **kwargs)

        text_box.insert(1.0, text)
        text_box['state'] = tk.DISABLED
        switch()
    return _wrapper


class PathHandler:

    def __init__(self):
        self.base_dir = None
        self.csv_file_name = None
        self.model_file_name = None
        self.extensions = None

    def extract_image_paths(self, is_pairs):
        temp = []
        for p in self.base_dir.glob(r'**/*'):
            if p.suffix in self.extensions:
                p = str(p)
                sep_paths = p.split(self.base_dir.stem)
                sep_paths = sep_paths[-1]
                sep_paths = sep_paths.split(os.sep)
                if is_pairs and len(sep_paths) != 3 or not is_pairs and len(sep_paths) > 3:
                    raise IndexError  # todo leave comments
                temp.append(p)
        return temp

    @toggle_text_box
    def set_file_callback(self, file_type=None, **kwargs):
        file = filedialog.askopenfile(mode='r',
                                      initialdir="/",
                                      title="Select a File",
                                      filetypes=file_type)

        if file:
            filename = Path(file.name).resolve()
            if filename.suffix == ".csv":
                self.csv_file_name = filename
            elif filename.suffix == ".dat":
                self.model_file_name = filename
            return filename

    @toggle_text_box
    def load_target_dir_callback(self, **kwargs):
        self.base_dir = Path(filedialog.askdirectory()).resolve()
        return self.base_dir

