# Destiny DPS Tracker

This program is still in early phase of development. If you would like to contribute fell free to create pull request or rise an issue. We will create a release when the basic functionality is achieved.

## About the project

This project aims to create an application that would enable fire team to monitor live damage numbers during boss DPS phase.

## How does it work

Right now we are testing a possibility recognize numbers from screen captures during live gameplay. We use [OpenCV](https://pypi.org/project/opencv-python/) and [Tesseract-OCR](https://github.com/tesseract-ocr/tesseract) to find and recognize the numbers from frames.

## Installation

1. Create a virtual environment by executing following command inside cloned repository folder

```bash
python -m venv .
```

2. To activate vent execute

```bash
source Scripts/activate
```

3. Install all the nessesary libraries

```bash
pip install -r requirements.txt
```

4. Execute the script like typical python file

```bash
python ./test.py
```
