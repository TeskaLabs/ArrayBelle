import os, codecs
from flask import Blueprint, request, url_for, current_app
from werkzeug.contrib.atom import AtomFeed
from ..blogsvc import GetBlogFeed

bp = Blueprint('rss', __name__, template_folder='templates')

@bp.route('/feed/atom')
def atom_feed():
	'''
	AtomFeed documentation: http://werkzeug.pocoo.org/docs/contrib/atom/
	'''

	#TODO: Feed icon/logo ...
	feed = AtomFeed(
		'SeaCat blog',
		title_type='text',
		subtitle='Latest blog posts from SeaCat',
		subtitle_type='text',
		feed_url=request.url,
		url=url_for('blog_list.index'),
		author={'name': "SeaCat", 'email': "info@seacat.mobi", 'uri': "http://seacat.mobi/"}
	)

	blog_dir = current_app.iconfig.get('content', 'content_directory')
	for blog, d in GetBlogFeed():
		content = d.get('lead_para')

		if content is None:
			content = u''
			indexfile = os.path.join(blog_dir, blog, 'index.md')
			ifile = codecs.open(indexfile, encoding='utf-8')
			for l in ifile:
				l = l.strip()
				if len(l) == 0: continue
				if l.startswith('# '): continue
				content += l
				break

		content += u'\r\n Continue reading on ' + url_for('blog_entry.entry', entry=blog, _external=True)

#		image = d.get('image')
#		if image is not None:
#			content += '\n&lt;img src="{}" /&gt;'.format(image)

		feed.add(
			d['name'],
			content,
			title_type='text',
			content_type='text',
			id="tag:seacat.mobi:/blog/{}".format(blog),
			updated=d['published_at'],
			url=url_for('blog_entry.entry', entry=blog, _external=True),
			categories=[{'term': t} for t in d['tags']]
		)

	return feed.get_response()
