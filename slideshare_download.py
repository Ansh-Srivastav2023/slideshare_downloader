#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
import os
import re
import json
import requests
from time import localtime, strftime
from bs4 import BeautifulSoup
import img2pdf

CURRENT = os.path.dirname(os.path.abspath(__file__))

def get_user_choice():
    """Prompt user to choose the action workflow."""
    print("\nSelect an option:")
    print(" [1] Download slide images only")
    print(" [2] Convert an existing image directory to PDF")
    print(" [3] Download images AND convert them to PDF (Default)")
    
    choice = input("Enter choice (1/2/3) [Default: 3]: ").strip()
    if choice not in ['1', '2', '3']:
        return '3'
    return choice


def download_images(url, convert_to_pdf=True):
    """Fetch all slide images from a Slideshare URL."""
    print(f"\nFetching {url} ...")
    
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
    }
    
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
    except requests.RequestException as e:
        print(f"Error accessing URL: {e}")
        sys.exit(1)
        
    soup = BeautifulSoup(response.content, 'html.parser')

    # Locate the embedded JSON application data layer
    script_tag = soup.find('script', id='__NEXT_DATA__')
    if not script_tag:
        print("Error: Could not find __NEXT_DATA__ script tag on this page.")
        sys.exit(1)

    try:
        data = json.loads(script_tag.string)
    except json.JSONDecodeError:
        print("Error: Failed to parse JSON data structure.")
        sys.exit(1)

    # Extract presentation layout variables
    try:
        slideshow = data["props"]["pageProps"]["slideshow"]
        slides = slideshow["slides"]
        total_slides = slideshow["totalSlides"]

        host = slides["host"]
        image_location = slides["imageLocation"]
        highest_quality = slides["imageSizes"][-1]["quality"]
        image_width = slides["imageSizes"][-1]["width"]
        raw_title = slides["title"]
        clean_title = re.sub(r'[^a-zA-Z0-9-]', '-', raw_title)
    except KeyError as e:
        print(f"Error: Missing expected SlideShare metadata keys in structural JSON: {e}")
        sys.exit(1)

    print(f"Presentation Title: {raw_title}")
    print(f"Total slides found: {total_slides}")

    # Set directory naming strategy based on user workflow option chosen
    if convert_to_pdf:
        timestamp = strftime("%Y%m%d_%H%M%S", localtime())
        dir_name = f"{clean_title}_{timestamp}"
    else:
        dir_name = clean_title

    img_dir = os.path.join(CURRENT, "pdf_images", dir_name)
    os.makedirs(img_dir, exist_ok=True)

    # Re-verify layout for structural prefix variations
    clean_host = host if host.startswith(("http://", "https://")) else f"https:{host}"

    print(f"\n1. Downloading slides to: {img_dir}")
    downloaded_count = 0
    
    for i in range(1, total_slides + 1):
        slide_num = str(i)
        image_url = f"{clean_host}/{image_location}/{highest_quality}/{clean_title}-{slide_num}-{image_width}.jpg"
        
        try:
            r = requests.get(image_url, headers=headers, timeout=10)
            r.raise_for_status()
        except requests.RequestException as e:
            print(f"  [!] Error downloading slide {i}: {e}")
            continue

        # Pad local filename strictly so file systems maintain proper sequence sorting
        filename = f"{i:04d}.jpg" 
        filepath = os.path.join(img_dir, filename)
        with open(filepath, 'wb') as f:
            f.write(r.content)
        downloaded_count += 1

    print(f"\nSuccessfully downloaded {downloaded_count}/{total_slides} slides.")
    
    if convert_to_pdf and downloaded_count > 0:
        convert_pdf(img_dir)


def convert_pdf(img_dir):
    """Convert all JPG images in a directory into a single high-quality PDF wrapper rapidly."""
    if not os.path.exists(img_dir):
        print(f"Error: Target directory does not exist: {img_dir}")
        return

    files = []
    for dirpath, _, filenames in os.walk(img_dir):
        for fname in filenames:
            if fname.lower().endswith(('.jpg', '.jpeg')):
                files.append(os.path.join(dirpath, fname))
        break

    if not files:
        print("No compatible slide images found. Cannot synthesize PDF output.")
        return

    # Natural sorting calculation key (handles 10 following 9 accurately)
    def natural_key(text):
        return [int(c) if c.isdigit() else c for c in re.split(r'(\d+)', os.path.basename(text))]

    files.sort(key=natural_key)

    pdf_name = os.path.basename(img_dir) + ".pdf"
    pdf_path = os.path.join(CURRENT, pdf_name)

    print(f"\n2. Rapidly assembling {len(files)} images into PDF structure...")
    
    try:
        # ULTRA-FAST METHOD: Bypasses layout matrix scaling loop logic
        pdf_bytes = img2pdf.convert(files)
        
        with open(pdf_path, 'wb') as doc:
            doc.write(pdf_bytes)
        print(f"\n3. Execution Complete! Document saved: {pdf_path}")
        
    except Exception as e:
        print(f"Critical execution block fault during PDF generation: {e}")


if __name__ == "__main__":
    choice = get_user_choice()

    # Flow Route Option 2: Target compiling an existing folder directory manually
    if choice == '2':
        target_dir = input("\nEnter the full path to your slide images folder: ").strip()
        convert_pdf(target_dir)
        sys.exit(0)

    # Flow Routes 1 and 3: Require fetching URL inputs 
    if len(sys.argv) > 1:
        url = " ".join(sys.argv[1:])
    else:
        url = input("\nEnter SlideShare presentation URL: ").strip()

    # Clean explicit surrounding string parameter symbols if copied incorrectly
    if (url.startswith("'") and url.endswith("'")) or (url.startswith('"') and url.endswith('"')):
        url = url[1:-1]

    if not url.startswith(("http://", "https://")):
        url = "https://" + url

    # Trigger action sequence according to user preference choices
    if choice == '1':
        download_images(url, convert_to_pdf=False)
    else:
        download_images(url, convert_to_pdf=True)
