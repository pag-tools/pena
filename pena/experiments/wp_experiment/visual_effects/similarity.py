import cv2, os
from skimage.measure import compare_ssim
import imutils

class Similarity:
	def __init__(self, default_page, p1, p2, both, destination):
		self.default_page = cv2.imread(default_page)
		self.p1 = cv2.imread(p1)
		self.p2 = cv2.imread(p2)
		self.both = cv2.imread(both)
		self.destination = destination

	def img_to_grayscale(self, image):
		return cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

	def is_changed_page(self):
		default = self.img_to_grayscale(self.default_page)
		p1 = self.img_to_grayscale(self.p1)
		p2 = self.img_to_grayscale(self.p2)
		both = self.img_to_grayscale(self.both)
		
		pages = []
		for image in [p1, p2, both]:
			(score, diff) = compare_ssim(image, default, full=True)
			diff = (diff * 255).astype("uint8")
			pages.append({'image': image, 'score': score, 'diff': diff})
		
		plugins_changes = [obj for obj in pages if obj['score'] != 1]
		
		if plugins_changes:
			pages = []
			for obj in plugins_changes:
				(score, diff) = compare_ssim(obj['image'], both, full=True)
				diff = (diff * 255).astype("uint8")
				pages.append({'image': obj['image'], 'score': score, 'diff': diff})
			
			both_changes = [obj for obj in pages if obj['score'] != 1]
			if both_changes:
				self.add_contours(both_changes)
				return True
		return False

	def add_contours(self, changes):
		red_color = (0, 0, 255)
		for obj in changes:
			diff = obj['diff']
			thresh = cv2.threshold(obj['diff'], 0, 255, cv2.THRESH_BINARY_INV | cv2.THRESH_OTSU)[1]
			cnts = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
			cnts = cnts[0] if imutils.is_cv2() else cnts[1]
			for c in cnts:
				(x, y, w, h) = cv2.boundingRect(c)
				cv2.rectangle(self.both, (x, y), (x + w, y + h), red_color, 2)
		cv2.imwrite('{}/changes.png'.format(self.destination), self.both)