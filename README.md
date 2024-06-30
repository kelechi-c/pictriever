# Pictriever (*not yet released*)
### An image scraping scraping library in python...
#### for efficient and flexible mass download of images, dataset creation etc

## Usage guide 
pictriever can be used for downloading a wide range images in few lines of Python, from popular image sites like Bing images, Pexels, Google, etc.

Install the library with 
`pip install pictriever`

For images from Pexels(You could also use this template for others)
`from pictriever.image_scraper import Pexelscraper`
`# sample code for downlaoding images of clouds`
`imscraper = Pexelscraper(search_term='clouds', min_count=10, max_count=100) # start scraper instance`
`image_links = imscraper.get_imlinks() # to get all the image links; set get_all_links=True`
`imscraper.download_all_images(link_list=image_links, output_folder='clouds', verbose=False) # set verbose to True if you want progress printing`
