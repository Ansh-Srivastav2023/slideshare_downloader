# SlideShare to PDF Downloader

A simple Python script to download slides from any SlideShare presentation URL and optionally combine them into a single high-quality PDF document.

## Installation

Before running the script, install the required dependencies using pip:

```bash
pip install requests beautifulsoup4 img2pdf

```

## How to Use
Clone the repository:

```bash
git clone https://github.com/Ansh-Srivastav2023/slideshare_downloader.git
cd slideshare_downloader
```

Run the script by executing:

```bash
python slideshare_download.py

```
OR
```bash
python3 slideshare_download.py
```

Upon launching, the script will prompt you with the following choices:

```bash
Select an option:
 [1] Download slide images only
 [2] Convert an existing image directory to PDF
 [3] Download images AND convert them to PDF (Default)
Enter choice (1/2/3) [Default: 3]:
```

* **Option 1:** Download slide images only (saves as loose `.jpg` files).
* **Option 2:** Convert an existing local folder of images into a PDF (no internet required).
* **Option 3 (Default):** Download the slides and automatically assemble them into a PDF.

And proceed as asked...

### Shortcut Mode

You can also pass the SlideShare URL directly as a command-line argument, for example:

```bash
python slideshare_download.py https://www.slideshare.net/JiangweiPan/reward-innovation-for-longterm-member-satisfaction
```

*(You will still be asked to choose how you want the URL processed).*

## Output

* **If converting to PDF:** A single high-quality PDF file is saved directly in the script's folder, named after the presentation and timestamp (e.g., `presentation-title_20260714_120000.pdf`).
* **If downloading images:** Slide images are sequence-padded (e.g., `0001.jpg`, `0002.jpg`) and safely isolated in the `pdf_images/` directory.


