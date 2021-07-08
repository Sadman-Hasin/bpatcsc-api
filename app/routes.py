import json

from flask import Response

from app import app
from app.scrapper.notices import Notices


@app.route("/notices")
def notice():
	def list_to_json(_list):
		_dict = {count: notice for count, notice in enumerate(_list)}

		return json.dumps(_dict)

	response = Response(list_to_json(Notices().__call__()))
	response.headers['Access-Control-Allow-Origin'] = '*'

	return response