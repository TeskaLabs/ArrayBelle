import os, json
from flask import request, url_for, safe_join, current_app

def get_author_object(author):
	VOID = {}

	if author is None:
		return VOID

	author_dir = safe_join(current_app.iconfig.get('content', 'authors_directory'), author)
	author_jsonfile = safe_join(author_dir, '_.json')

	if not os.path.isfile(author_jsonfile):
		return VOID

	try:
		author_dict = json.load(open(author_jsonfile, 'rb'))
	except Exception, e:
		print "WARNING: {} {}".format(author_jsonfile, e)
		return VOID

	author_dict['id'] = author

	# Translate author image path to URL
	author_img_path = author_dict.get('image')
	if author_img_path is None:
		return author_dict

	if not os.path.isfile(safe_join(author_dir, author_img_path)):
		author_dict.pop('image')
		return author_dict

	author_dict['image'] = url_for('blog_entry.author_file', author=author, path=author_img_path)

	return author_dict

