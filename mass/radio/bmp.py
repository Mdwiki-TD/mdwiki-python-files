import os
import requests
from io import BytesIO

try:
    from PIL import Image
except ImportError:
    print('Installing Pillow using pip...')
    os.system("pip install pillow")
    from PIL import Image

# مسار الدليل لحفظ الصور
directory_path = "/data/project/mdwiki/public_html/images"
if not os.path.exists(directory_path):
    os.makedirs(directory_path)


def convert_bmp_to_jpg(bmp_data):
    print("Converting BMP to JPEG...")
    bmp_image = Image.open(BytesIO(bmp_data))
    jpg_data = BytesIO()
    try:
        bmp_image.convert("RGB").save(jpg_data, format="JPEG")
        return jpg_data.getvalue()
    except Exception as e:
        print(f"Error converting BMP to JPEG: {e}")
        return False


def save_image(image_data, pathh):
    print(f"Saving image to {pathh}...")
    with open(pathh, "wb") as file:
        file.write(image_data)


def work_bmp(url):
    extension = url.split(".")[-1].lower()
    # ---
    if extension != "bmp":
        print("URL is not a BMP image. Skipping...")
        return url
    # ---
    file_name = os.path.basename(url).replace(".bmp", ".jpg")
    # ---
    img_path = os.path.join(directory_path, file_name)
    # ---
    if not os.path.exists(img_path):
        print(f"Downloading image from ({url})...")
        # ---
        response = requests.get(url)
        image_data = response.content
        # ---
        jpg_data = convert_bmp_to_jpg(image_data)
        # ---
        if jpg_data:
            save_image(jpg_data, img_path)
    else:
        print(f"Image already exists at {img_path}. continue...")
    # ---
    url = f'https://mdwiki.toolforge.org/images/{file_name}'
    # ---
    print(f"Image saved successfully. URL: {url}")
    return url, "jpg"


if __name__ == "__main__":
    url = "https://prod-images-static.radiopaedia.org/images/30676235/b337054203ddf5c7894962f5623be2.bmp"
    urln = work_bmp(url)
    print(f"Final URL: {urln}")
