from pictriever.image_scraper import BingImages

image_scraper = BingImages("clouds", 22, 100)  # initialize scraper instance

imlinks = image_scraper.get_imlinks(
    get_all_links=True)  # for image link retrieval

image_scraper.download_images(
    imlinks, "clouds_", verbose=True
)  # download all images from the links


# keep the Google image class here till other are finished
class GoogleImageScraper:
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
        print("shutting down webdriver...")
        self.driver.quit()
