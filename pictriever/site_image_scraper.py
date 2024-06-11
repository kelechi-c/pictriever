import requests, os, shutil, rich

from tqdm.auto import tqdm
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.by import By

# Defaults and instances
drive_opts = Options()
drive_opts.add_argument('-headless')

driver = webdriver.Firefox(options=drive_opts)


class PexelsImageScraper():
    def __init__(self, search_term: str):
        self.search_term = search_term
        self.pexel_url = f"https://www.pexels.com/search/{self.search_term}"
        self.pexel_img_class = "MediaCard_image__yVXRE"

    def _init_webdriver(self):
        driver.get(self.pexel_url)
        driver.implicitly_wait(100)

    def fetch_image_links(self, limit: int):
        self._init_webdriver()
        image_links = driver.find_elements(By.CSS_SELECTOR, f"img.{self.pexel_img_class}")
        
        return image_links[:limit+1]
    
    def download_images(self):
        pass
