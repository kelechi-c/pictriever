import shutil
import os
import time
import requests
import math
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options
from tqdm.auto import tqdm
from selenium import webdriver


# utility functions
def _format_string(search_string: str):  # to remove spaces in search terms
    return search_string.replace(' ', '+')


def _format_filename(file_name: str):
    text = file_name.split(".")[0]
    return text


def _scrolldelay(driver, min_count):
    time.sleep(2)
    # scrolling down slowly
    stopScrolling = 0
    print('scrolling to load more')
    while True:
        stopScrolling += 1
        driver.execute_script("window.scrollBy(0,40)")
        time.sleep(0.1)
        if stopScrolling > math.floor(min_count/2):
            break
    time.sleep(1)


def _init_webdriver(url):
    drive_opts = Options()
    drive_opts.add_argument('-headless')
    driver = webdriver.Firefox(options=drive_opts)
    driver.maximize_window()
    driver.get(url)
    print('webdriver initialized')
    return driver


class Pexelscraper():
    def __init__(self, search_term: str, max_count: int, min_count: int):
        self.search_term = _format_string(search_term)
        self.pexel_url = f"https://www.pexels.com/search/{self.search_term}"
        self.pexel_img_class = "MediaCard_image__yVXRE"
        self.max_count = max_count
        self.min_count = min_count
        self.driver = _init_webdriver(self.pexel_url)

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
            _scrolldelay(self.driver, self.min_count)

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
                f'{link_count} links acquired from Pexels, using {len(links)} of them')

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
        _quit_driver()

    def _quit_driver(self):
        print('shutting down webdriver...')
        self.driver.quit()


class GoogleImageScraper():
    def __init__(self, search_term: str, max_count: int, min_count: int):
        self.image_class = "YQ4gaf"
        self.search_term = self._format_string(search_term)
        self.search_url = f"https://www.google.com/search?q={self.search_term}l&sca_esv=fb64c27acdf6db0d&sca_upv=1&udm=2&sxsrf=ADLYWII43-tIV80076FgCtRKI2_M4AdexQ%3A1719652914088&ei=MtJ_ZvCOBar2kdUP_sOt0AM&ved=0ahUKEwjw79KovoCHAxUqe6QEHf5hCzoQ4dUDCBA&uact=5&oq=diffusionmodel&gs_lp=Egxnd3Mtd2l6LXNlcnAiDmRpZmZ1c2lvbm1vZGVsMgYQABgHGB4yBhAAGAcYHjIGEAAYBxgeMgYQABgHGB4yBhAAGAcYHjIGEAAYBxgeMgYQABgHGB4yBhAAGAcYHjIGEAAYBxgeMgYQABgHGB5IoBNQmwVYmwVwAXgAkAEAmAH0BaAB9AWqAQM2LTG4AQPIAQD4AQGYAgKgAqwGwgIKEAAYgAQYQxiKBcICBRAAGIAEmAMAiAYBkgcFMS41LTGgB9oF&sclient=gws-wiz-serp"
        self.max_count = max_count
        self.min_count = min_count
        self.driver = _init_webdriver()

    def get_imlinks(self, get_all_links: bool = False):
        if self.min_count > 100:
            _scrolldelay(self.driver, self.min_count)
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

    def download_images(
        self, link_list: list, output_folder: str, verbose: bool = False
    ):
        k = 0

        for image_link in tqdm(link_list):
            try:
                file_res = requests.get(
                    image_link, stream=True
                )  # fetch content from url
                image_file = _format_filename(os.path.basename(image_link))
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
        _quit_driver()

    def _quit_driver(self):
        print('shutting down webdriver...')
        self.driver.quit()


class BingImages():
     def __init__(self, search_term: str, min_count: int, max_count: int):
        self.search_term = _format_string(search_term)
        self.bing_url = f'https://www.bing.com/images/search?q={self.search_term}&form=HDRSC3&first=1&cw=1177&ch=621'
        self.bing_imlink_class = 'iusc'
        self.max_count = max_count
        self.min_count = min_count
        self.driver = _init_webdriver(self.bing_url)

     def get_imlinks(self, get_all_links: bool = False):
        if self.min_count > 100:
            _scrolldelay(self.driver, self.min_count)

        try:
            image_links = self.driver.find_elements(
                By.CSS_SELECTOR, f"a.{self.bing_imlink_class}")
            image_links = [link.get_attribute('href') for link in image_links]
            print(image_links)
            link_count = len(image_links)
            links = image_links[:self.max_count] if get_all_links else image_links
            # print number of links
            print(
                f'{link_count} links acquired from Bing images, using {len(links)}...')
            return links

        except Exception as e:
            print(f'e => [{e}]')


    def download_images(self, link_list: list, output_folder: str, verbose: bool = False):
        k = 0
        if not os.path.exists(output_folder):
            os.mkdir(output_folder)

        for image_link in tqdm(link_list):
            try:
                # fetch content from url
                file_res = requests.get(image_link, stream=True)
                image_file = os.path.basename(image_link)
                image_file = os.path.join(output_folder, f'bing_{self.search_term}_{k}.png')  # output file path

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

        print(f'{k} images downloaded from Bing images')  # sucess message
        _quit_driver()


    def _quit_driver(self):
        print('shutting down webdriver...')
        self.driver.quit()


class UnsplashImages():
     def __init__(self, search_term: str, min_count: int, max_count: int):
        self.search_term = _format_string(search_term)
        self.unsplash_url = f'https://unsplash.com/s/photos/{self.search_term}'
        self.unsplash_class = 'vkrMA'
        self.max_count = max_count
        self.min_count = min_count
        self.driver = _init_webdriver(self.unsplash_url)

     def get_imlinks(self, get_all_links: bool = False):
        if self.min_count > 100:
            _scrolldelay(self.driver, self.min_count)

        try:
            image_links = self.driver.find_elements(By.CSS_SELECTOR, f"img.{self.unsplash_class}")
            image_links = [link.get_attribute('src') for link in image_links]
            print(image_links)
            link_count = len(image_links)
            links = image_links[:self.max_count] if get_all_links else image_links
            # print number of links
            print(f'{link_count} links acquired from Unsplash, using {len(links)}...')
            return links

        except Exception as e:
            print(f'e => [{e}]')


    def download_images(self, link_list: list, output_folder: str, verbose: bool = False):
        k = 0
        if not os.path.exists(output_folder):
            os.mkdir(output_folder)

        for image_link in tqdm(link_list):
            try:
                # fetch content from url
                file_res = requests.get(image_link, stream=True)
                image_file = os.path.basename(image_link)
                image_file = os.path.join(output_folder, f'unsplash_{self.search_term}_{k}.png')  # output file path

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

        print(f'{k} images downloaded from unsplash.com images')  # sucess message
        _quit_driver()

    def _quit_driver(self):
        print('shutting down webdriver...')
        self.driver.quit()

