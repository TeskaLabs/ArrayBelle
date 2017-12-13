import os, re, ConfigParser

_basedir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))

class ConfigFactory():
	defaults = {
		'general': {
			'debug': False,
			'website_url': '/',
		},
		'content': {
			'templates_directory': _basedir + '/app/templates',
			'media_directory': _basedir + '/app/static/images',
			'authors_directory': _basedir + '/authors',
			'content_directory': _basedir + '/content'
		}
	}

	def add_defaults(self, dictionary, config):
		'''
		Add defaults to a current configuration
		'''

		for section, keys in dictionary.items():

			section = str(section)
			if section not in config._sections:
				try:
					config.add_section(section)
				except ValueError:
					if config._strict:
						raise

			for key, value in keys.items():
				key = config.optionxform(str(key))
				if key in config._sections[section]:
					continue # Value exists, no default needed

				if value is not None:
					value = str(value)

				config.set(section, key, value)

	def get_config(self):
		config = ConfigParser.ConfigParser()
		config.SECTCRE = re.compile(r"\[ *(?P<header>[^]]+?) *\]")

		# os.environ['CONFIG'] = "../site-teskalabs.com-blog/config.cfg"

		# Reading the site-specific configuration
		if "ARRAYBELLE_CONF" in os.environ:
			config_fname = os.environ['ARRAYBELLE_CONF']
			if not os.path.isfile(config_fname):
				print("Info: config file '{}' not found. Using the default configuration.".format(config_fname))
			else:
				config.read(config_fname)

		self.add_defaults(self.defaults, config)
		self.to_absolute_paths(config)

		return config


	def to_absolute_paths(self, config):
		""" Converts relative paths in config to absolute paths

			:param config: configparser object
		"""
		content_paths = [
			"templates_directory",
			"media_directory",
			"authors_directory",
			"content_directory"
		]
		for key in content_paths:
			path = config.get('content', key)
			if not os.path.isabs(path):
				config.set('content', key, os.path.join(_basedir, path))
