import json
import requests

ingred = "100g cooked pasta"
resp = requests.get("https://api.edamam.com/api/nutrition-data",
                    params={"app_id": "3c448def", "app_key": "253a23f284ba71a36d814b58796fae93",
                            "ingr": ingred})

decoded_response = json.loads(resp.text)
print(str(decoded_response["calories"]))
# print(decoded_response["totalNutrients"]["FAT"]["quantity"])
# print(decoded_response["totalNutrients"]["CHOCDF"]["quantity"])
# print(decoded_response["totalNutrients"]["SUGAR"]["quantity"])
print(decoded_response["ingredients"][0]["parsed"][1]["foodMatch"])
# print(resp.text)

