
# AnnotaFlow - Image Caption Validation Tool

[![MIT License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

---

## Description

**AnnotaFlow** is a desktop tool for validating and annotating image captions, developed in Python with a Tkinter graphical user interface.  
It allows you to display an image along with its existing caption, edit or skip the caption, and save the results to an output CSV file while keeping track of progress in a JSON file.
The project follows the **Model-View-Controller (MVC)** architectural pattern to clearly separate business logic, user interface, and flow control.

---

## Features

- Intuitive GUI for viewing and editing captions.
- Load images from a directory and captions from an input CSV.
- Save validated or skipped captions in an output CSV.
- Resume annotation from last saved progress using a JSON progress file.
- Duplicate caption detection with warning prompt.
- Automatic navigation through images and captions.
- Clean MVC architecture for maintainability and extensibility.

---

## How to Use

### Requirements

- Python 3.x
- Python libraries:
  - `tkinter` (usually included in standard Python installs)
  - `pandas`
  - `Pillow`

Install dependencies with:

```bash
pip install pandas pillow
```

### Configuration
Edit the following variables in the main() function:
- `image_dir`: folder containing images to annotate
- `input_csv`: input CSV file with columns image_name and caption
- `output_csv`: output CSV file path where validated captions will be saved
- `progress_file`: JSON file path to save annotation progress

### Running the tool

```bash
python main.py
```

### Usage

 - The interface displays the image and its caption. 
 - Modify the caption and press Submit to save. 
 - Press Skip to skip the current image without changes.
 - If the caption already exists in output, a duplicate warning will appear. 
 - Pressing Enter acts as a shortcut for submitting the caption.

### Code Structure
`CaptionModel`: manages data loading, saving, and progress tracking.
`CaptionView`: Tkinter GUI showing images, text input, and buttons.
`CaptionController`: handles interaction between Model and View, controls app flow.
`main.py`: application entry point that initializes MVC components and starts the GUI

## License

This project is licensed under the MIT License, allowing free use, modification, and distribution, with the requirement to include the copyright and license notice.

See the full license text in the [LICENSE file](https://github.com/RenatoEsposito1999/Annotation_system/blob/main/LICENSE).

## Contact

For questions, suggestions, or contributions, please open an issue or a pull request.


**Happy annotating!**
