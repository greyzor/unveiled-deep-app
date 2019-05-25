"""
Url Parsing service
"""
import newspaper

PROTOCOLS_SUPPORTED = ['http','https']

def extract_image_url(url, input_html=None):
	""" Extract an image from an url.

    :param url: the url (starting with http or https).
    :param input_html: if provided, no need to download url content.

    :returns: top image, and other images.
    :rtype: tuple(str, list[str])
	"""
	global PROTOCOLS_SUPPORTED

	# check prefix
	assert(any([url.startswith(pfx) for pfx in PROTOCOLS_SUPPORTED]))

	# extract image using newspaper package.
	print('Extracting image for url: %s' % url)
	article = newspaper.Article(url)

	article.download(input_html=input_html)
	article.parse()

	# select image urls
	top_img = article.top_img
	imgs = article.imgs

	return (top_img, imgs)