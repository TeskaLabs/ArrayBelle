import os, codecs, re, json
from flask import Blueprint, render_template, abort, request, safe_join, send_file, url_for, redirect, current_app

import markdown
from .mdtables import TableExtension
from .mdsuperscript import SuperscriptExtension
from markdown.extensions.codehilite import CodeHiliteExtension
from markdown.extensions.attr_list import AttrListExtension

bp = Blueprint('blog_entry', __name__, template_folder='templates')
h1rg = re.compile("^# (.*)$", re.MULTILINE)

@bp.route('/<entry>')
def entry(entry):
	if '..' in entry: abort(404)

	#TODO: Validate entry_name
	blog_dir = safe_join(current_app.iconfig.get('content', 'content_directory'),entry)
	blog_index_md = safe_join(blog_dir, 'index.md')
	blog_jsonfile = safe_join(blog_dir, '_.json')
	blog_redirect = safe_join(blog_dir, '_.redirect')

	if os.path.isfile(blog_redirect):
		f=open(blog_redirect, 'rb')
		uri=f.read().splitlines()[0]
		return redirect(url_for('blog_entry.entry', entry=uri))

	if not os.path.isfile(blog_index_md):
		abort(404)

	if os.path.isfile(blog_jsonfile):
		try:
			blog_dict = json.load(open(blog_jsonfile, 'rb'))
		except Exception, e:
			print "WARNING: {} {}".format(blog_jsonfile, e)
			blog_dict = {}
	else:
		blog_dict = {}

	input_file = codecs.open(blog_index_md, mode="r", encoding="utf-8")
	text = input_file.read()

	h1mt = h1rg.search(text)
	if h1mt is not None:
		h1 = h1mt.group(1)
	else:
		h1 = None

	# Blog Post Title
	title = blog_dict.get('title', h1)

	# Blog Post Description
	description = blog_dict.get('description')
	if description is None:
		description = blog_dict.get('title', h1)

	# Blog Post Image
	image = blog_dict.get('image')
	if image is not None and not image.startswith('/'):
		blog_dict['image'] = url_for('blog_entry.file', entry=entry, path=image, _external=True)

	# Blog Post Body
	body = markdown.markdown(text, extensions=[SuperscriptExtension(), TableExtension(), CodeHiliteExtension(), AttrListExtension()])
	
	# Blog Post Tags
	tags = blog_dict.get('tags', [])

	# Blog Post Keywords
	keywords = blog_dict.get('keywords', "")

	# Blog Post Author
	from author import get_author_object
	author = blog_dict.get('author')
	author_obj = get_author_object(author)

	# Related posts
	from ..blogsvc import GetBlogFeed
	
	tag_exclude = frozenset(["press", "bulletin"])

	related_posts = GetBlogFeed(
		frozenset(tags),
		entry_exclude=entry,
		limit=3,
		shuffle=True)

	most_recent_posts = GetBlogFeed(
		tag_exclude=frozenset(["press", "bulletin"]),
		entry_exclude=entry,
		limit=5)

	return render_template('blog_entry.html',
		body=body,
		entry=entry,
		h1=h1,
		title=title,
		description=description,
		meta_dict=blog_dict,
		tags=tags,
		keywords=keywords,
		author_obj=author_obj,
		related_posts=related_posts,
		most_recent_posts=most_recent_posts)


@bp.route('/__/<entry>/<path>')
def file(entry,path):
	if '..' in entry or '..' in path: abort(404)
	blog_dir = safe_join(current_app.iconfig.get('content', 'content_directory'),entry)
	file_name = safe_join(blog_dir, path)
	return send_file(file_name)

@bp.route('/__/author/<author>/<path>')
def author_file(author, path):
	if '..' in author or '..' in path: abort(404)
	author_dir = safe_join(current_app.iconfig.get('content', 'authors_directory'),author)
	file_name = safe_join(author_dir, path)
	return send_file(file_name)
