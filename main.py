from Scrapper import Scrapper
import urllib
import os


def emptyImagesDirectory():

    directory = './scraped_images/'
    if not os.path.exists(directory):
        os.makedirs(directory)
    for filename in os.listdir(directory):
        os.unlink("./scraped_images/" + filename)


def main():

    emptyImagesDirectory()

    url = "https://www.cars.co.za/searchVehicle.php?new_or_used=&make_model=Hyundai%5Bi10%5D&vfs_area=&agent_locality=&price_range=&os=%27&P="

    num_img = 1000

    newScrapper = Scrapper(url, num_img)
    try:
        newScrapper.startCrawling()
    except urllib.error.HTTPError as e:
        print("Error: ", e, "\n")


if __name__ == '__main__':
    main()



