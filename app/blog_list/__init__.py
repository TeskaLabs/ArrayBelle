from flask import Blueprint, render_template, request
from ..blogsvc import GetBlogFeed

bp = Blueprint('blog_list', __name__, template_folder='templates')

@bp.route('/')
@bp.route('/topic/<path:tag>')
@bp.route('/author/<author>')
@bp.route('/author/<author>/topic/<path:tag>')
def index(tag=None, author=None):
	tag_filter = frozenset(tag.split('/')) if tag is not None else None
	author_filter = author

	tag_exclude = frozenset(["press", "bulletin"]) if tag_filter is None else None
	tag_include = frozenset(["blog"]) if tag_filter is None else None

	return render_template('blog_list.html',
		blogs=GetBlogFeed(tag_filter, author_filter, tag_exclude, tag_include),
		tag_filter=tag_filter)
