from flask import Blueprint, abort, safe_join, send_file, current_app

bp = Blueprint('blog_site_media', __name__, template_folder='templates')


def init(app):
	bp = Blueprint('blog_site_media', __name__, template_folder='templates')
	@bp.route(app.iconfig.get('general', 'site_media_url')+'/<path:entry>')
	def site_media(entry):
		if '..' in entry or '..' in entry: abort(404)
		site_media_dir = current_app.iconfig.get('content', 'site_media_directory')
		file_name = safe_join(site_media_dir, entry)
		try:
			return send_file(file_name)
		except IOError:
			abort(404)

	app.register_blueprint(bp)
