import urllib.request
import os
from PIL import Image


class ImageDownloader:

    def __init__(self):
        self.cnt = 0
        self.del_cnt = 0

    def downloadAndSave(self, image_link):
        try:
            urllib.request.urlretrieve(image_link, "./scraped_images/" + str(self.cnt) + ".jpg")
            im = Image.open("./scraped_images/" + str(self.cnt) + ".jpg")
            width, height = im.size
            if width >= 400 and height >= 400:
                print("Downloading " + str(self.cnt) + "/1000")
                im.close()
                self.cnt += 1
                return 0
            else:
                im.close()
                self.del_cnt += 1
                os.remove("./scraped_images/" + str(self.cnt) + ".jpg")
                return 1
        except urllib.error.HTTPError as e:
            print("Error: ", e, "\n", image_link)