import tkinter as tk
from PIL import Image, ImageTk

class CaptionView(tk.Frame):
    def __init__(self, root, on_submit, on_skip):
        super().__init__(root)
        self.root = root
        self.on_submit = on_submit
        self.on_skip = on_skip
        self.pack(fill=tk.BOTH, expand=True)

        # Stats label
        self.stats_label = tk.Label(self, text="", font=("Helvetica", 14, "bold"))
        self.stats_label.pack(pady=8)

        # Image label
        self.image_label = tk.Label(self)
        self.image_label.pack(pady=10)

        # Caption textbox
        self.caption_text = tk.Text(self, height=7, width=70, wrap="word", font=("Helvetica", 14))
        self.caption_text.pack(pady=10)

        # Buttons frame
        btn_frame = tk.Frame(self)
        btn_frame.pack(pady=12)

        self.submit_button = tk.Button(btn_frame, text="Submit", command=self.submit, width=20)
        self.submit_button.pack(side=tk.LEFT, padx=15)

        self.skip_button = tk.Button(btn_frame, text="Skip", command=self.skip, width=20)
        self.skip_button.pack(side=tk.LEFT, padx=15)

        self.root.bind("<Return>", lambda event: self.submit())

    def display_image_and_caption(self, image_path, caption, stats):
        self.stats_label.config(
            text=f"Processed: {stats[0]}   Skipped: {stats[1]}   Remaining: {stats[2]}"
        )

        img = Image.open(image_path)
        img.thumbnail((600, 600))
        self.tk_image = ImageTk.PhotoImage(img)
        self.image_label.config(image=self.tk_image)

        self.caption_text.delete("1.0", tk.END)
        self.caption_text.insert(tk.END, caption)

    def submit(self):
        caption = self.caption_text.get("1.0", tk.END).strip()
        self.on_submit(caption)

    def skip(self):
        self.on_skip()
