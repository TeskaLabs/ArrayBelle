import os, json, datetime
from flask import request, url_for, current_app
from random import shuffle as rnd_shuffle

def GetBlogFeed(tag_filter=None, author_filter=None, tag_exclude=None, tag_include=None, entry_exclude=None, limit=None, shuffle=False):
	blog_dir = current_app.iconfig.get('content', 'content_directory')

	now = datetime.datetime.now();

	blog_list = []
	for item in os.listdir(blog_dir):
		if entry_exclude is not None and item in entry_exclude:
			continue

		jsonfile = os.path.join(blog_dir, item, '_.json')
		if not os.path.isfile(jsonfile): continue

		try:
			d = json.load(open(jsonfile, 'rb'))
		except Exception, e:
			print "WARNING: {} {}".format(jsonfile, e)
			continue

		tags = d.get('tags')
		author = d.get('author')

		# Filter by tag
		# If a post contains at least one of the tags in filter it is going to be included
		if tag_filter is not None and tags is not None:
			if (len(tag_filter.intersection(tags))==0): continue
			# if not tag_filter.issubset(tags): continue

		# Filter author
		if author_filter is not None:
			if author is None: continue
			if author != author_filter: continue

		# Exclude posts with specific tags
		if tag_exclude is not None and tags is not None:
			if tag_include is not None and len(tag_include.intersection(tags)) > 0:
				# include has priority before exclude
				# if tag_include contains excluded tags, the post get still included
				pass
			elif len(tag_exclude.intersection(tags)) > 0:
				# Post's tags contain excluded tag, it is not going to be included
				continue

		pa = d.get('published_at')
		if pa is not None:
			pa = datetime.datetime.strptime(pa.strip(), "%d %b %Y")
		else:
			pa = now + datetime.timedelta(days=1);

		image = d.get('image')
		if image is not None and not image.startswith('/'):
			d['image'] = url_for('blog_entry.file', entry=item, path=image)

		d['published_at'] = pa
		if pa > now: continue

		blog_list.append((item, d))

	if shuffle:
		rnd_shuffle(blog_list)
		ret = blog_list
	else:
		ret = sorted(blog_list, key= lambda x: x[1]['published_at'], reverse=True)

	# Limit
	if limit is not None:
		ret = ret[:limit]

	return ret
