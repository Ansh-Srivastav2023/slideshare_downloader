# SlideShare to PDF Downloader

A simple Python script to download slides from any SlideShare presentation URL and combine them into a single high-quality PDF document.

## 🛠️ Installation

Before running the script, install the required dependencies using pip:

```cpp
pip install requests beautifulsoup4 img2pdf

```

## 🚀 How to Use

Pass the URL directly as a command-line argument:

```python
python slideshare_download.py [url]
```

Example Command:

```python
python slideshare_download.py https://www.slideshare.net/JiangweiPan/reward-innovation-for-longterm-member-satisfaction

```

## 📁 Output

* **PDF File:** Saved directly in the script's folder, named with the download timestamp (e.g., `20260714_120000.pdf`).
* **Images:** Temporary source images are saved in a sub-folder called `pdf_images/`.

```

```
