from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.
import requests
import os
import time
import sys
import math
import shutil
import rich
import argparse
from tqdm.auto import tqdm
from selenium import webdriver
webdriver.


class Pexels():
    def __init__(self, search_term: str, max_count: int, min_count: int):
        self.search_term = self._format_string(search_term)
        self.pexel_url = f"https://www.pexels.com/search/{self.search_term}"
        self.pexel_img_class = "MediaCard_image__yVXRE"
        self.max_count = max_count
        self.min_count = min_count
        self.driver = self._init_webdriver()

    def _format_string(self, search_string: str):  # to remove spces in search terms
        return search_string.replace(' ', '+')

    def _init_webdriver(self):
        drive_opts = Options()
        drive_opts.add_argument('-headless')
        driver = webdriver.Firefox(options=drive_opts)
        driver.maximize_window()
        driver.get(self.pexel_url)
        print('webdriver initialized')
        return driver

    def _scrolldelay(self):
        time.sleep(2)
        # scrolling down slowly
        stopScrolling = 0
        print('scrolling to load more')
        while True:
            stopScrolling += 1
            self.driver.execute_script("window.scrollBy(0,40)")
            time.sleep(0.1)
            if stopScrolling > math.floor(self.min_count/2):
                break
            time.sleep(1)

    def get_imlinks(self, get_all_links: bool = False):
        if self.min_count > 100:
            self._scrolldelay(self.min_count)
        try:
            driver = self.driver
            image_links = driver.find_elements(
                By.CSS_SELECTOR, f"img.{self.pexel_img_class}")
#             image_links = image_links.find_elements(By.TAG_NAME, 'a')

#             print(image_links)
            image_links = [link.get_attribute('src') for link in image_links]
            print(image_links)
            link_count = len(image_links)
            links = image_links[:self.max_count] if get_all_links else image_links
            # print number of links
            print(
                f'{link_count} links acquired from Google, using {len(links)} of them')

            return links

        except Exception as e:
            print(f'e => [{e}]')

    def _format_filename(self, file_name: str):
        text = file_name.split('.')[0]
        return text

    def download_images(self, link_list: list, output_folder: str, verbose: bool = False):
        k = 0
        os.mkdir(output_folder)

        for image_link in tqdm(link_list):
            try:
                # fetch content from url
                file_res = requests.get(image_link, stream=True)
                image_file = os.path.basename(image_link)
                image_file = os.path.join(
                    output_folder, f'pexel_{self.search_term}_{k}.png')  # output file path

                with open(image_file, "wb") as file_writer:
                    file_res.raw.decode_content = True
                    # save to folder
                    shutil.copyfileobj(file_res.raw, file_writer)

                if verbose:  # show download count and progress
                    print(f'image @ {k+1} downloaded')
                k += 1  # file counter

            except Exception as e:  # exception handling
                print(f"[> {e}]")
                continue

        print(f'{k} images downloaded from Pexels.com')  # sucess message

    def quit_driver(self):
        self.driver.quit()


class GoogleImageScraper():
    def __init__(self, search_term: str, max_count: int, min_count: int):
        self.image_class = "YQ4gaf"
        self.search_term = self._format_string(search_term)
        self.search_url = f"https://www.google.com/search?q={self.search_term}l&sca_esv=fb64c27acdf6db0d&sca_upv=1&udm=2&sxsrf=ADLYWII43-tIV80076FgCtRKI2_M4AdexQ%3A1719652914088&ei=MtJ_ZvCOBar2kdUP_sOt0AM&ved=0ahUKEwjw79KovoCHAxUqe6QEHf5hCzoQ4dUDCBA&uact=5&oq=diffusionmodel&gs_lp=Egxnd3Mtd2l6LXNlcnAiDmRpZmZ1c2lvbm1vZGVsMgYQABgHGB4yBhAAGAcYHjIGEAAYBxgeMgYQABgHGB4yBhAAGAcYHjIGEAAYBxgeMgYQABgHGB4yBhAAGAcYHjIGEAAYBxgeMgYQABgHGB5IoBNQmwVYmwVwAXgAkAEAmAH0BaAB9AWqAQM2LTG4AQPIAQD4AQGYAgKgAqwGwgIKEAAYgAQYQxiKBcICBRAAGIAEmAMAiAYBkgcFMS41LTGgB9oF&sclient=gws-wiz-serp"
        self.max_count = max_count
        self.min_count = min_count
        self.driver = self._init_webdriver()

    def _format_string(self, search_string: str):  # to remove spces in search terms
        return search_string.replace(" ", "")

    def _init_webdriver(self):
        drive_opts = Options()
        drive_opts.add_argument("-headless")
        driver = webdriver.Firefox(options=drive_opts)
        driver.maximize_window()
        driver.get(self.search_url)
        print("webdriver initialized")
        return driver

    def _scrolldelay(self):
        time.sleep(2)
        # scrolling down slowly
        stopScrolling = 0
        print("scrolling to load more")
        while True:
            stopScrolling += 1
            driver.execute_script("window.scrollBy(0,40)")
            time.sleep(0.1)
            if stopScrolling > math.floor(self.min_count / 2):
                break
            time.sleep(1)

    def get_imlinks(self, get_all_links: bool = False):
        if self.min_count > 100:
            self._scrolldelay(self.min_count)
        try:
            image_links = self.driver.find_elements(
                By.CLASS_NAME, self.image_class)
            link_count = len(image_links)
            assert (
                link_count >= self.min_count
            ), "Retrieved links not sufficient/up to min_count"

            image_links = [link.get_attribute("src") for link in image_links]
            links = image_links[: self.max_count] if get_all_links else image_links
            print(
                f"{link_count} links acquired from Google, using {len(links)} of them"
            )  # print number of links

            return links
        except Exception as e:
            print(f"e => [{e}]")

    def _format_filename(file_name: str):
        text = file_name.split(".")[0]
        return text

    def download_images(
        self, link_list: list, output_folder: str, verbose: bool = False
    ):
        k = 0

        for image_link in tqdm(link_list):
            try:
                file_res = requests.get(
                    image_link, stream=True
                )  # fetch content from url
                image_file = self._format_filename(
                    os.path.basename(image_link))
                image_file = os.path.join(
                    output_folder, image_file)  # output file path

                with open(f"google_{self.search_term}_{k}.png", "wb") as file_writer:
                    file_res.raw.decode_content = True
                    # save to folder
                    shutil.copyfileobj(file_res.raw, file_writer)

                if verbose:  # show download count and progress
                    print(f"image @ {k+1} downloaded")
                k += 1  # file counter

            except Exception as e:  # exception handling
                print(f"[> {e}]")
                continue

        print(f"{k} images downloaded from Google")  # sucess message

    def quit_driver(self):
        self.driver.quit()
