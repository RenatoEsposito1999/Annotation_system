import os
import json
import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
import pandas as pd

# ===== MODEL =====

class CaptionModel:
    def __init__(self, image_dir, input_csv, output_csv, progress_file):
        self.image_dir = image_dir
        self.input_csv = input_csv
        self.output_csv = output_csv
        self.progress_file = progress_file

        self.df = pd.read_csv(self.input_csv)
        self.df_output = pd.DataFrame(columns=["filename", "caption"])
        self.current_index = self._load_progress()

    def _load_progress(self):
        if os.path.exists(self.progress_file):
            with open(self.progress_file, 'r') as f:
                data = json.load(f)
                last_file = data.get("last_processed")
                if last_file in self.df["filename"].values:
                    return self.df.index[self.df["filename"] == last_file].tolist()[0] + 1
        return 0

    def _save_progress(self, filename):
        with open(self.progress_file, 'w') as f:
            json.dump({"last_processed": filename}, f)

    def get_next(self):
        if self.current_index >= len(self.df):
            return None
        row = self.df.iloc[self.current_index]
        image_path = os.path.join(self.image_dir, row["filename"])
        caption = row["caption"]
        return row["filename"], image_path, caption

    def save_caption(self, filename, caption):
        self.df_output.loc[len(self.df_output)] = [filename, caption]
        self.df_output.to_csv(self.output_csv, index=False)
        self._save_progress(filename)
        self.current_index += 1

# ===== VIEW =====

class CaptionView(tk.Frame):
    def __init__(self, root, on_submit):
        super().__init__(root)
        self.root = root
        self.on_submit = on_submit
        self.pack()

        # Image
        self.image_label = tk.Label(self)
        self.image_label.pack(side=tk.LEFT, padx=10, pady=10)

        # Caption editor
        self.caption_text = tk.Text(self, height=5, width=60, wrap="word")
        self.caption_text.pack(side=tk.TOP, padx=10, pady=5)

        # Submit button
        self.submit_button = tk.Button(self, text="Conferma (Invio)", command=self.submit)
        self.submit_button.pack(side=tk.BOTTOM, pady=10)

        self.root.bind("<Return>", lambda event: self.submit())  # invio = submit

    def display_image_and_caption(self, image_path, caption):
        img = Image.open(image_path)
        img.thumbnail((400, 400))
        self.tk_image = ImageTk.PhotoImage(img)
        self.image_label.config(image=self.tk_image)
        self.caption_text.delete("1.0", tk.END)
        self.caption_text.insert(tk.END, caption)

    def submit(self):
        caption = self.caption_text.get("1.0", tk.END).strip()
        self.on_submit(caption)

# ===== CONTROLLER =====

class CaptionController:
    def __init__(self, model, view):
        self.model = model
        self.view = view
        self.current_filename = None
        self.load_next()

    def load_next(self):
        next_data = self.model.get_next()
        if next_data is None:
            messagebox.showinfo("Fine", "Hai completato tutte le immagini!")
            self.view.root.quit()
            return
        filename, image_path, caption = next_data
        self.current_filename = filename
        self.view.display_image_and_caption(image_path, caption)

    def submit_caption(self, new_caption):
        self.model.save_caption(self.current_filename, new_caption)
        self.load_next()

# ===== MAIN APP =====

def main():
    image_dir = "immagini"
    input_csv = "caption_orig.csv"
    output_csv = "caption_validated.csv"
    progress_file = "progress.json"

    model = CaptionModel(image_dir, input_csv, output_csv, progress_file)

    root = tk.Tk()
    root.title("Validatore di Caption")
    view = CaptionView(root, lambda cap: controller.submit_caption(cap))
    controller = CaptionController(model, view)
    root.mainloop()

if __name__ == "__main__":
    main()
