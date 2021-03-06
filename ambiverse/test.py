import requests
import ast
import json

## get token

def get_entities(texto):
	url = "https://api.ambiverse.com/v1beta3/entitylinking/analyze"

	texto = texto.replace("\"","")

	data = "{"+ \
	  "\"coherentDocument\": true,"+  \
	  "\"confidenceThreshold\": 0.075,"+ \
	  "\"docId\": \"doc1\","+ \
	  "\"text\": \""+texto+"\","+ \
	  "\"language\": \"en\""+ \
	"}"

	#print data

	headers = {
	    'Content-Type': "application/json",
	    'Accept': "application/json",
	    'Authorization': token
	    }

	response = requests.request("POST", url, data=data, headers=headers)

	print response.text

	matches = ast.literal_eval(response.text)["matches"]

	#print matches

	entities = []

	for m in matches:
		print m
		if "id" in m["entity"]:
			entidad_id = m["entity"]["id"]
			url = "https://api.ambiverse.com/v1beta3/knowledgegraph/entities?offset=0&limit=10"
			data = "[\""+entidad_id+"\"]"

			headers = {
			    'Content-Type': "application/json",
			    'Accept': "application/json",
			    'Authorization': token
			    }

			response = requests.request("POST", url, data=data, headers=headers)
			entities.append(ast.literal_eval(response.text))

	return entities

url = "https://api.ambiverse.com/oauth/token"

with open('conf.json', 'r') as f:
    try:
        conf = json.load(f)
    except ValueError:
        conf = {}

client_id = conf["client_id"]
client_secret = conf["client_secret"]

data = "client_id="+client_id+"&client_secret="+client_secret+"&grant_type=client_credentials"

headers = {
    'Content-Type': "application/x-www-form-urlencoded",
    'Accept': "application/json"
    }

response = requests.request("POST", url, data=data, headers=headers)
#print response.text

token = ast.literal_eval(response.text)["access_token"]

## analyze - get entities

#list_entities = get_entities("Colombia, U.S., Russia, France, Belarouse, Wales, England, Tripoli, Asia, Sahara, Antartica, Andes and Barranquilla")

#list_sets = []
#for i in list_entities:
#	list_sets.append(set(i["entities"][0]["categories"]))

#print reduce(lambda x, y: x & y, list_sets)


#list_entities = get_entities("Brad Pitt, Angelina Jolie, Hitler and Stephen Hawking were married")

list_sets = []
#for i in list_entities:
#	list_sets.append(set(i["entities"][0]["categories"]))

#print reduce(lambda x, y: x & y, list_sets)

list_entities = get_entities("Republican party, Nazi party, Greenpeace")

#print list_entities[0]["entities"][0]["description"]

#text = list_entities[0]["entities"][0]["description"]

#print text

#list_entities = get_entities(text)

for i in list_entities:
	print " "
	print i
	list_sets.append(set(i["entities"][0]["categories"]))

print reduce(lambda x, y: x & y, list_sets)