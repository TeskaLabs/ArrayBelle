import sys
import os

# Path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# WSGI Application
def application(env, s_r):

	# Pass configuration path envvar to os.env
	if "ARRAYBELLE_CONF" in env:
		os.env["ARRAYBELLE_CONF"] = env["ARRAYBELLE_CONF"]

	from app import app as _application
	return _application(env, s_r)
