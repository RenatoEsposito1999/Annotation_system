from controller import CaptionController
from view import CaptionView
from model import CaptionModel
import tkinter as tk
def main():
    image_dir = "/home/renato/Scrivania/datasets/Turtle_other"
    input_csv = "/home/renato/Scrivania/datasets/annotations/Other_turtle.csv"
    output_csv = "./caption_validated.csv"
    progress_file = "progress.json"

    model = CaptionModel(image_dir, input_csv, output_csv, progress_file)

    root = tk.Tk()
    root.title("Annotation validation system")
    root.geometry("700x800")  # 
    view = CaptionView(root, lambda cap: controller.submit_caption(cap), lambda: controller.skip_caption())
    controller = CaptionController(model, view)
    root.mainloop()

if __name__ == "__main__":
    main()