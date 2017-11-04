import sys
import json
from clarifai.rest import ClarifaiApp

print(sys.argv[1])
app = ClarifaiApp(api_key="b8d70b86df7a49fcb1c7c98c31fed204")

# predict with the model
ingredients = {}
result = app.tag_files([sys.argv[1]], model_name="food-items-v1.0")
print(json.dumps(result, indent=4))
for i in result['outputs'][0]['data']['concepts']:
    valor=(i['value'])*1000000
    ingredients[i['value']] = i['name']
    print('%f -> %s' % (i['value'], i['name']))

print(ingredients)