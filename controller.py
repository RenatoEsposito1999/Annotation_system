from tkinter import messagebox

class CaptionController:
    def __init__(self, model, view):
        self.model = model
        self.view = view
        self.current_filename = None
        self.load_next()

    def load_next(self):
        next_data = self.model.get_next()
        if next_data is None:
            messagebox.showinfo("All done", "You have completed all the images!")
            self.view.root.quit()
            return
        filename, image_path, caption = next_data
        self.current_filename = filename
        stats = self.model.get_stats()
        self.view.display_image_and_caption(image_path, caption, stats)

    def submit_caption(self, caption):
        duplicate = (self.model.df_output['caption'].str.lower() == caption.lower()).any()

        if duplicate:
            result = messagebox.askyesno(
                "Warning",
                "This caption already exists. Do you want to save it anyway?\n\n"
                "Press 'Sì' to ignore the warning and save.\n"
                "Press 'No' to go back and edit."
            )
            if not result:
                return

        self.model.save_caption(self.current_filename, caption, skipped=False)
        self.load_next()

    def skip_caption(self):
        self.model.save_caption(self.current_filename, "", skipped=True)
        self.load_next()
