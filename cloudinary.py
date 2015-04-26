import json, requests,unittest, time, hashlib

cloud_name = 'dhel159wx'
api_key =  '993815229441374'
api_secret = 'bb_B7mnHeR29ZqGqX9WLDb--Sqo'


#fixed parameters
base_url = 'https://api.cloudinary.com/v1_1/'

#entries that should be included in secret
include_secret = ['callback', 'eager', 'format', 'public_id', 'tags', 'timestamp', 'transformation', 'type']

#obtain image
image_base_url = 'http://res.cloudinary.com/'+cloud_name+'/image/upload/'

#upload image
image_upload_url = 'https://api.cloudinary.com/v1_1/'+cloud_name+'/image/upload'

class TestCloudinary(unittest.TestCase):

	def test_image_get(self):
		response = requests.get(image_base_url + 'sample.jpg')

		#testing that the response is 200
		self.assertEqual(response.status_code, 200)

		#testing that header is image/jpeg
		self.assertEqual(response.headers['content-type'], 'image/jpeg')

	def test_image_upload_from_url(self):
		#create a dict with the parameters
		parameters = {'file'      : 'http://upload.wikimedia.org/wikipedia/commons/e/e5/Newells_school_logo.png' ,
					  'api_key'   : api_key,
					  'timestamp' : int(time.time())
					 }
		#compute the signature with the api_key and timestamp parameters only
		parameters['signature'] = TestCloudinary.getSignature(parameters)
		
		#obtain the response
		response = requests.post(image_upload_url,data=parameters)

		#testing that the response is 200
		self.assertEqual(response.status_code, 200)

		#testing that header is image/jpeg
		self.assertEqual(response.headers['content-type'], 'application/json; charset=utf-8')

		#testing that header is image/jpeg
		self.assertEqual(json.loads(response.content)['resource_type'], 'image')

		#inform where is the new image
		print ("new image url "+ json.loads(response.content)['url'])

	def test_image_upload_multipart(self):
		data =  open ("./d1.jpg", "r").read()
		
		parameters = {'file'      : data ,
					  'api_key'   : api_key,
					  'timestamp' : int(time.time())
					 }

		#compute the signature with the api_key and timestamp parameters only
		parameters['signature'] = TestCloudinary.getSignature(parameters)
		
		#obtain the response
		response = requests.post(image_upload_url,data=parameters)

		#testing that the response is 20
		self.assertEqual(response.status_code, 400)

		#other test
		

	@staticmethod
	def getSignature( parameters):
		keys = parameters.keys()
		keys.sort()
		base = ''
		for key in keys : 
			if key in include_secret:
				base =  base + key + '=' + str(parameters[key])+'&'
		toSerialize = base[:-1] + api_secret
		return hashlib.sha1(toSerialize).hexdigest()

if __name__ == '__main__':
	unittest.main()



#,data=json.dumps({'name': 'foo'}), auth=('user', 'pass'))



