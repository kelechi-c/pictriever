from pictriever.image_scraper import BingImages

image_scraper = BingImages("clouds", 22, 100)  # initialize scraper instance

imlinks = image_scraper.get_imlinks(
    get_all_links=True)  # for image link retrieval

image_scraper.download_images(
    imlinks, "clouds_", verbose=True
)  # download all images from the links
