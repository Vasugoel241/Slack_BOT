from flask import jsonify, request
from config import Config

class CommonResponseHelper:
	
	@staticmethod
	def send_success_response(data):
		return CommonResponseHelper.send_response(200, 'Success', data)
	
	@staticmethod
	def send_error_response(errors):
		return CommonResponseHelper.send_response(400, 'Error', False, errors)
	
	@staticmethod
	def send_response(status, message, data = False, errors = False):
		try:
			response = {}
			response['status'] = status
			response['message'] = message
			if(data):
				response['data'] = data
			if(errors):
				response['errors'] = errors
			
			return jsonify(response)
		except Exception as e:
			print(e)
			raise e
