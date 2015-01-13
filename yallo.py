#!/usr/bin/env python3

import io
import re
import json
import os.path
import requests
from flask import Flask, request, jsonify

base = 'https://www.yallo.ch/'
login = 'kp/dyn/web/j_security_check.do'
view = 'kp/dyn/web/sec/options/view.do'
DEBUG = False

app = Flask(__name__)
tokens = {}


# get a token
def token_from_login(username, password):
	res = requests.post(base + login, data={
		'j_username': username,
		'j_password': password,
	}, allow_redirects=False)
	
	token = res.cookies.get('JSESSIONID')
	if token is not None:
		tokens[username] = token
	
	return token

# get options view
def get_options(token):
	res = requests.get(base + view, cookies={'JSESSIONID': token})
	res.raise_for_status()
	
	pat = re.compile(r'>([^>]+)\(verbleibendes\s+Inklusivguthaben:\s+([^\)]+)')
	sub = re.compile(r'Option\s+([\w\s]+)\s+ist aktiv: Erneuerung spätestens am\s*([\d\.]+)?')		# date may be missing on the day of renewal
	options = []
	for match in pat.finditer(res.text):
		opt, val = match.groups()
		opt = opt.strip()
		js = {
			'service': opt,
			'remaining': val,
		}
		
		# nicer split of name and renew date
		more = sub.match(opt)
		if more is not None:
			js['service'], js['renew'] = more.groups()
		options.append(js)
	
	return options if len(options) > 0 else None

# get token and options
def retrieve(username, password):
	token = tokens.get(username)
	if token is not None:
		options = get_options(token)
		if options is not None:
			return options
	
	token = token_from_login(username, password)
	options = get_options(token) if token is not None else None
	return options


@app.route('/')
def index():
	options = retrieve(request.args.get('u'), request.args.get('p'))
	if options is None:
		return jsonify({'error': "Failed to login"})
	return jsonify({'options': options})


if '__main__' == __name__:
	if DEBUG:
		app.run(port=8001, debug=True)
	else:
		app.run(host='0.0.0.0')

