# %%
import requests, os, shutil, rich, pprint

from tqdm.auto import tqdm
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.by import By

# %%
image_folder = "moondream_images"
# os.mkdir(image_folder)
out_folder = os.path.join(os.getcwd(), image_folder)

pexel_url = "https://www.pexels.com/"
pexel_img_class = 'MediaCard_image__yVXRE'

# %%
drive_opts = Options()

drive_opts.add_argument('-headless')

driver = webdriver.Firefox(options=drive_opts)

driver

# %%
## Test cell

page = driver.get(pexel_url)
driver.implicitly_wait(100)

driver, page

# %%
image_links = driver.find_elements(By.CSS_SELECTOR, f'img.{pexel_img_class}')

image_links, len(image_links)

# %%
img_elements = driver.find_elements(By.TAG_NAME, 'img')

len(img_elements), img_elements

# %%
img_urls = [link.get_attribute('src') for link in image_links]

len(img_urls), img_urls

# %%
im_link_list = [os.path.basename(url) for url in img_urls]

rich.print(f"[bold white]{im_link_list}")

# %%
def format_filename(file_name: str):
    text = file_name.split('.jpeg')[0]
    return text

# %%
def download_images(link_list: list):
    
    k = 0
    file_list = []
    
    for image_link in tqdm(link_list):
        try:
            file_res = requests.get(image_link, stream=True)
            image_file = format_filename(os.path.basename(image_link))
            
            with open(image_file) as file_writer:
                file_res.raw.decode_content = True
                shutil.copyfileobj(file_res.raw, file_writer)
        
            
            file_list.append(image_file)
            
        except Exception as e:
            rich.print(f'[bright red]Well...-> {e}')
            continue
        
    
        

# %%
rich.inspect(download_images)

# %%

r = requests.get(img_urls[1], stream=True)
if r.status_code == 200:  # 200 status code = OK
    with open('one.jpg', "wb") as f:
        r.raw.decode_content = True
        shutil.copyfileobj(r.raw, f)

# %%
def get_file_links(site, num_limit):
    
    
    return site

# %%
class PexelImages():
    def __init__(self, search_term, count_limit):
        self.image_type = search_term
        self.count_limit = count_limit
        self.pexel_url = f'https://www.pexels.com/search/{search_term}/'


