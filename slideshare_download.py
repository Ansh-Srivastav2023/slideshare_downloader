def download_images(url):
    """Fetch all slide images from a Slideshare URL and convert them to PDF."""
    print(f"Fetching {url} ...")
    
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
    }
    
    response = requests.get(url, headers=headers)
    response.raise_for_status()
    soup = BeautifulSoup(response.content, 'html.parser')

    # Locate the embedded JSON data
    script_tag = soup.find('script', id='__NEXT_DATA__')
    if not script_tag:
        print("Error: Could not find __NEXT_DATA__ script tag.")
        sys.exit(1)

    try:
        data = json.loads(script_tag.string)
    except json.JSONDecodeError:
        print("Error: Failed to parse JSON data.")
        sys.exit(1)

    # Navigate to the slide information
    try:
        slideshow = data["props"]["pageProps"]["slideshow"]
        slides = slideshow["slides"]
        total_slides = slideshow["totalSlides"]

        host = slides["host"]
        image_location = slides["imageLocation"]
        highest_quality = slides["imageSizes"][-1]["quality"]
        image_width = slides["imageSizes"][-1]["width"]
        title = re.sub(r'[^a-zA-Z0-9-]', '-', slides["title"])
    except KeyError as e:
        print(f"Error: Missing expected key in JSON: {e}")
        sys.exit(1)

    print(f"Total slides: {total_slides}")

    # Create temporary directory for images
    timestamp = strftime("%Y%m%d_%H%M%S", localtime())
    img_dir = os.path.join(CURRENT, "pdf_images", timestamp)
    os.makedirs(img_dir, exist_ok=True)

    # Clean up the host string if it already contains http:// or https://
    clean_host = host if host.startswith(("http://", "https://")) else f"https:{host}"

    print("\n1. Downloading images:")
    for i in range(1, total_slides + 1):
        # Convert index directly to string (no 0001 padding needed)
        slide_num = str(i)
        
        # Safe URL assembly matching Slideshare's unpadded schema
        image_url = f"{clean_host}/{image_location}/{highest_quality}/{title}-{slide_num}-{image_width}.jpg"
        print(f"  {image_url}")
        
        try:
            r = requests.get(image_url, headers=headers, timeout=10)
            r.raise_for_status()
        except requests.RequestException as e:
            print(f"  Error downloading slide {i}: {e}")
            continue

        # Keep padding for the local filename so the OS sorts them correctly
        filename = f"{i:04d}.jpg" 
        filepath = os.path.join(img_dir, filename)
        with open(filepath, 'wb') as f:
            f.write(r.content)

    convert_pdf(img_dir)
