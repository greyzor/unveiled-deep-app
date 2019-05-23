"""
"""
import newspaper

def extract_image_url(url, input_html=None):
	""" """
	print('Extracting image for url: %s' % url)
	article = newspaper.Article(url)
	article.download(input_html=input_html)
	article.parse()
	top_img = article.top_img
	imgs = article.imgs
	return (top_img, imgs)