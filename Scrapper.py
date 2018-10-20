import urllib.request
import re
from bs4 import BeautifulSoup
from ImageDownloader import ImageDownloader


class Scrapper:
    pages_no = int()
    link_of_images = list()
    hmap = {}
    page_cnt = 1
    id = ImageDownloader()

    def __init__(self, link, num_images):
        self.baseLink = 'https://www.cars.co.za'
        self.link = link
        self.cnt = 0
        self.num_images = num_images
        self.thepage = urllib.request.urlopen(self.link + str(self.page_cnt))
        self.soup = BeautifulSoup(self.thepage, "html.parser")
        self.total_pages = int(self.soup.find("div", {"id": "vtype-count-hatchback"}).contents[0])

    def getLink(self):
        print(self.link)

    def getNoPages(self):
        print(self.no_pages)

    def startCrawling(self):

        while 1:
            anchors = self.soup.findAll("a", {"class": "vehicle-list__vehicle-name"})
            for anchor in anchors:
                if self.cnt < self.num_images:
                    newUrl = self.baseLink + anchor.get("href")
                    self.openPageAndCollectImageLink(newUrl)
                    print(str(self.cnt) + "/" + str(self.num_images))
                if self.cnt == self.num_images:
                    return 0
                if self.page_cnt == self.total_pages:
                    return 1
            self.page_cnt += 1
            self.thepage = urllib.request.urlopen(self.link + str(self.page_cnt))
            self.soup = BeautifulSoup(self.thepage, "html.parser")
            self.total_pages = int(self.soup.find("div", {"id": "vtype-count-hatchback"}).contents[0])

    def getLinkImages(self):
        return self.link_of_images

    def getPageCount(self):
        return self.total_pages

    def openPageAndCollectImageLink(self, newUrl):
        try:
            newPage = urllib.request.urlopen(newUrl)
            newSoup = BeautifulSoup(newPage, "html.parser")
            imgTags = newSoup.findAll('img')
            for img in imgTags:
                alt_tag = img.get('alt')
                if self.cnt > self.num_images - 1:
                    print(self.link_of_images.__len__())
                    return self.cnt

                if type(alt_tag) == type(str()):  # Because sometimes has null

                    if alt_tag.find('Hyundai') >= 0 and alt_tag.find('i10') >= 0:

                        data_src = img.get('data-src')
                        if not data_src:
                            lg_img = self.renameLinksToLargeImage(img.get('src'))
                            if lg_img not in self.hmap:
                                self.hmap[lg_img] = 1
                                if self.id.downloadAndSave(lg_img) == 0:
                                    self.cnt += 1
                        else:
                            lg_img = self.renameLinksToLargeImage(data_src)
                            if lg_img not in self.hmap:
                                self.hmap[lg_img] = 1
                                if self.id.downloadAndSave(lg_img) == 0:
                                    self.cnt += 1
        except urllib.error.HTTPError as e:
            print("Error: ", e, "\n", newUrl)

    def renameLinksToLargeImage(self, img):
        sub1 = "n-stock_med"
        sub2 = "n-stock_medf"
        new_sub = "n-stock_large/"

        p = re.compile('(n-stock_medf.*/|n-stock_med.*/)')
        img = p.sub(new_sub, img)
        return img
