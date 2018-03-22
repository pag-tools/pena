import cv2
import numpy as np
from skimage.measure import compare_ssim
import imutils

class Similarity:
    def __init__(self, default_page=None, plugins_images=None, conflict_page=None, destination=None):
        # load each image on grayscale mode
        self.default_page = cv2.imread(default_page, 0)
        self.plugins = [cv2.imread(image, 0) for image in plugins_images]
        self.conflict_page = cv2.imread(conflict_page, 0)
        # load conflict page on RGB mode
        self.conflict_page_rgb = cv2.imread(conflict_page)
        # destination of image changes
        self.destination = destination
        # threshold of similarity
        self.threshold = 0.85

    def is_equal(self, image_one, image_two):
        """ check if two matrix are equals """
        return np.array_equal(image_one, image_two)

    def get_diffs(self, image_one, image_two):
        """ get the differences between image_one and image_two """
        diff = compare_ssim(image_one, image_two, full=True)[1]
        diff = (diff * 255).astype("uint8")
        return diff

    def is_conflicting(self):
        """ check if pages have visual discrepances """
        pages = []
        for image in self.plugins:
            if self.is_equal(image, self.default_page):
                continue
            diff = self.get_diffs(image, self.default_page)
            pages.append({'image': image, 'diff': diff})

        if not pages:
            return False

        for image in pages:
            if self.is_equal(image['image'], self.conflict_page):
                continue
            img_cropped = self.crop_changes(image)
            image['img_cropped'] = img_cropped
            match = self.match_image(image, self.conflict_page)
            if not match:
                self.add_rect(image['diff'])
                return True
        
        return False

    def generate_cnts(self, diff):
        """ generate points based on diff """
        thresh = cv2.threshold(diff, 0, 255, cv2.THRESH_BINARY_INV | cv2.THRESH_OTSU)[1]
        cnts = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        cnts = cnts[0] if imutils.is_cv2() else cnts[1]
        return cnts

    def crop_changes(self, image):
        """ crop and return an image """
        img, diff = image['image'], image['diff']
        cnts = self.generate_cnts(diff)
        for c in cnts:
            (x, y, w, h) = cv2.boundingRect(c)
            cropped_img = img[y:y+h, x:x+w]
        return cropped_img

    def add_rect(self, diff):
        """ draw a rect throught the diffs points """
        cnts = self.generate_cnts(diff)
        for c in cnts:
            (x, y, w, h) = cv2.boundingRect(c)
            cv2.rectangle(self.conflict_page_rgb, (x, y), (x + w, y + h), (0,0,255), 2)
		
        cv2.imwrite('{}/changes.png'.format(self.destination), self.conflict_page_rgb)

    def match_image(self, image_obj, page):
        """ check if the cropped image is in page """
        img_cropped = image_obj['img_cropped']
        w, h = img_cropped.shape[::-1]
        res = cv2.matchTemplate(img_cropped, page, cv2.TM_CCOEFF_NORMED)
        loc = np.where( res >= self.threshold)
        
        is_matched = True if [pt for pt in zip(*loc[::-1])] else False
        return is_matched