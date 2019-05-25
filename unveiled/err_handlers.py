"""
Error handlers.
"""
from flask import render_template

def page_not_found(e):
	return render_template('error.html', code=404), 404

def page_forbidden(e):
	return render_template('error.html', code=403), 403

def internal_server_error(e):
	return render_template('error.html', code=500), 500