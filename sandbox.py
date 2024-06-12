import requests, os, shutil, rich, argparse

from tqdm.auto import tqdm
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.by import By

image_folder = "moondream_images"
# os.mkdir(image_folder)
out_folder = os.path.join(os.getcwd(), image_folder)
pexel_url = "https://www.pexels.com/"
pexel_img_class = "MediaCard_image__yVXRE"

# Webdriver initialization
drive_opts = Options()
drive_opts.add_argument("-headless")

driver = webdriver.Firefox(options=drive_opts)

# get site content

page = driver.get(pexel_url)
driver.implicitly_wait(100)

# get image tags
image_tags = driver.find_elements(By.CSS_SELECTOR, f"img.{pexel_img_class}")

image_urls = [link.get_attribute("src") for link in image_tags] # Then get the links themselves


def format_filename(file_name: str):
    text = file_name.split(".jpeg")[0]
    text = text + '.jpeg'
    
    return text


def download_images(link_list: list):

    k = 0
    file_list = []

    for image_link in tqdm(link_list):
        try:
            file_res = requests.get(image_link, stream=True)
            image_file = format_filename(os.path.basename(image_link))
            file_path = os.path.join(out_folder, image_file)

            with open(file_path, "wb") as file_writer:
                file_res.raw.decode_content = True
                shutil.copyfileobj(file_res.raw, file_writer)

            rich.print(f"[bold green] {image_file} successfully downloaded :lightning:")
            file_list.append(image_file)
            k += 1

        except Exception as e:
            rich.print(f"Well...-> [bold red]{e}[/bold red]")
            continue


if __name__=='main':
    download_images(image_urls)