import os
import json
import csv
import pandas as pd

class CaptionModel:
    def __init__(self, image_dir, input_csv, output_csv, progress_file):
        self.image_dir = image_dir
        self.input_csv = input_csv
        self.output_csv = output_csv
        self.progress_file = progress_file

        self.df = pd.read_csv(self.input_csv)

        if os.path.exists(self.output_csv):
            self.df_output = pd.read_csv(self.output_csv)
            if 'status' not in self.df_output.columns:
                self.df_output['status'] = 'validated'  
        else:
            self.df_output = pd.DataFrame(columns=["image_name", "caption", "status"])

        self.current_index, self.validated, self.skipped = self._load_progress()

    def _load_progress(self):
        if os.path.exists(self.progress_file):
            with open(self.progress_file, 'r') as f:
                data = json.load(f)
                return (
                    data.get("last_index", 0),
                    data.get("validated", 0),
                    data.get("skipped", 0)
                )
        return 0, 0, 0

    def _save_progress(self):
        with open(self.progress_file, 'w') as f:
            json.dump({
                "last_index": self.current_index,
                "validated": self.validated,
                "skipped": self.skipped
            }, f)

    def get_next(self):
        if self.current_index >= len(self.df):
            return None
        row = self.df.iloc[self.current_index]
        image_path = os.path.join(self.image_dir, row["image_name"])
        caption = row["caption"]
        return row["image_name"], image_path, caption

    def save_caption(self, filename, caption, skipped=False):
        status = "skipped" if skipped else "validated"
        
        new_row = pd.DataFrame({
            "image_name": [filename],
            "caption": [caption],
            "status": [status]
        })
        
        self.df_output = pd.concat([self.df_output, new_row], ignore_index=True)
        self.df_output.to_csv(
            self.output_csv,
            index=False,
            quoting=csv.QUOTE_ALL,
            mode='w'
        )
        
        if skipped:
            self.skipped += 1
        else:
            self.validated += 1
            
        self.current_index += 1
        self._save_progress()

    def skip(self):
        filename = self.df.iloc[self.current_index]["image_name"]
        self.save_caption(filename, "", skipped=True)

    def get_stats(self):
        total = len(self.df)
        remaining = total - self.current_index
        return self.validated, self.skipped, remaining
