import pytest
from pictriever.image_scraper import BingImages, Pexelscraper


@pytest.fixture
def scraper():
    return BingImages()
