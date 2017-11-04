import sys
import json
from clarifai.rest import ClarifaiApp
import requests


def tipus_ingr(llista_tipus, llista, ingredient, quantitat1, quantitat2):
    quantitat_princ = 0
    quantitat_sec = 0
    res = []
    for item in llista_tipus:
        if ingredient == item:
            quantitat_princ = quantitat1
            quantitat_sec = quantitat2
            for y in llista:
                if y not in llista_tipus:
                    res.append(y)

    return quantitat_princ, quantitat_sec, res


def llista_pes(llista, ingredient):
    peixos = ["mackerel", "fish", "fish steak", "salmon steak", "fish fillet", "salmon", "bass", "sea bass",
              "fried calamari", "shrimp", "prawn"]
    q_p, q_s, ll_neta = tipus_ingr(peixos, llista, ingredient, "150g ", "10g ")
    if q_p:
        return q_p, q_s, ll_neta

    pasta = ["pasta", "spaghetti", "macaroni", "penne", "fettuccine", "spaghetti bolognese", "tagliatelle", "rice",
             "noodle", "lasagna", "gnocchi"]
    q_p, q_s, ll_neta = tipus_ingr(pasta, llista, ingredient, "200g cooked ", "20g ")
    if q_p:
        return q_p, q_s, ll_neta

    llegum = ["lentil", "beans", "lima bean", "pigeon pea", "garbanzo", "kidney bean", "chickpeas", "indian pea", "pea",
              "succotash", "moth bean", "horse gram", "buckwheat", "groats", "mung bean"]
    q_p, q_s, ll_neta = tipus_ingr(llegum, llista, ingredient, "170g cooked ", "20g ")
    if q_p:
        return q_p, q_s, ll_neta

    pastissos = ["brownie", "chocolate cake", "torte", "chocolate chip cake", "fruitcake", "apple pie", "bread pudding",
                 "pastry", "muffin", "cookie", "blueberry muffin", "raisin muffin", "pork pie", "chocolate cookie",
                 "candy", "cream", "chocolate"]
    q_p, q_s, ll_neta = tipus_ingr(pastissos, llista, ingredient, "100g ", "20g ")
    if q_p:
        return q_p, q_s, ll_neta

    verdura = ["vegetable", "tomato", "carrot", "squash", "pumpkin", "celery", "curry", "cucumber", "broccoli",
               "eggplant", "avocado", "onion", "cauliflower", "asparagus", "courgette", "pepper"]
    q_p, q_s, ll_neta = tipus_ingr(verdura, llista, ingredient, "200g ", "10g ")
    if q_p:
        return q_p, q_s, ll_neta

    fruita = ["berry", "blueberry", "strawberry", "blackberry", "raspberry", "banana", "black currant", "pineapple",
              "apple", "lemon", "watermelon", "pear", "peach", "melon", "grape", "grapefruit"]
    q_p, q_s, ll_neta = tipus_ingr(fruita, llista, ingredient, "150g ", "20g ")
    if q_p:
        return q_p, q_s, ll_neta

    begudes = ["whisky", "rum", "brandy", "cognac", "liqueur", "tequila", "wine", "vodka",
               "beer", "syrup", "coke", "lemonade", "milk"]
    q_p, q_s, ll_neta = tipus_ingr(begudes, llista, ingredient, "180ml ", "50g ")
    if q_p:
        n = 0
        for x in ll_neta:
            if x == "cream":
                del ll_neta[n]
            n += 1
        return q_p, q_s, ll_neta

    begudes_a = ["whisky", "rum", "brandy", "cognac", "liqueur", "tequila", "wine", "vodka"]
    q_p, q_s, ll_neta = tipus_ingr(begudes_a, llista, ingredient, "30ml ", "0g ")
    if q_p:
        return q_p, q_s, ll_neta

    patata = ["potato", "sweet potato", "mashed potatoes", "french fries", "chips"]
    q_p, q_s, ll_neta = tipus_ingr(patata, llista, ingredient, "150g ", "15g ")
    if q_p:
        return q_p, q_s, ll_neta

    pizza = ["pizza", "dough"]
    q_p, q_s, ll_neta = tipus_ingr(pizza, llista, ingredient, "150g ", "5g ")
    if q_p:
        return q_p, q_s, ll_neta

    carns = ["steak", "beef", "pork", "beef steak", "sirloin", "tenderloin", "pork chop", "duck", "chicken", "bacon"]
    q_p, q_s, ll_neta = tipus_ingr(carns, llista, ingredient, "200g ", "30g ")
    if q_p:
        return q_p, q_s, ll_neta

    ice_cream = ["ice cream", "cream", "candy", "sherbet", "sorbet"]
    q_p, q_s, ll_neta = tipus_ingr(ice_cream, llista, ingredient, "100g ", "20g ")
    if q_p:
        return q_p, q_s, ll_neta

    quantitat_p = "200g "
    quantitat_s = "10g "
    amanida = ["lettuce", "basil", "lamb's lettuce", "summer purslane", "cabbage", "parsley", "herb", "coriander",
               "cilantro", "oregano", "sage"]
    for item in amanida:
        if ingredient == item:
            quantitat_p = "70g "
            quantitat_s = "20g "

    return quantitat_p, quantitat_s, llista


def buscar_edamam(on_buscar, que_buscar):
    try:
        return float(on_buscar[que_buscar]["quantity"])
    except KeyError:
        return 0


def edamam(ingredient, quantitat):
    ingred = str(quantitat + ingredient)
    resp = requests.get("https://api.edamam.com/api/nutrition-data",
                        params={"app_id": "3c448def", "app_key": "253a23f284ba71a36d814b58796fae93",
                                "ingr": ingred})
    decoded_response = json.loads(resp.text)
    kcal = float(decoded_response["calories"])
    fat = buscar_edamam(decoded_response["totalNutrients"], "FAT")
    carbo = buscar_edamam(decoded_response["totalNutrients"], "CHOCDF")
    return kcal, fat, carbo


app = ClarifaiApp(api_key="b8d70b86df7a49fcb1c7c98c31fed204")
result = app.tag_files([sys.argv[1]], model_name="food-items-v1.0")

llista_ingr = []

# Fa la llista més petita
for i in result['outputs'][0]['data']['concepts']:
    if i['value'] >= 0.9:
        verify = edamam(i['name'], "100g ")[0]
        if verify > 0 and verify != "meat":
            llista_ingr.append(i['name'])


# Pregunta quin es ingredient principal del plat
n = 0
for x in llista_ingr:
    print(n, "->", x)
    n += 1
print("Quin d'aquests ingredients és el principal?(0,1,2...)")
n_ingr_principal = int(input())
ingr_principal = llista_ingr[n_ingr_principal]

# Calories depenent del pes depenent del menjar
quantitat_princ, quantitat_sec, ingr_sec = llista_pes(llista_ingr, ingr_principal)
kcal_tot, fat_tot, carb_tot = edamam(ingr_principal, quantitat_princ)
print(ingr_sec)
str_ingr_sec = ""
for ingr in ingr_sec:
    str_ingr_sec += str(ingr + ", ")
kcal_sec, fat_sec, carb_sec = edamam(str_ingr_sec, quantitat_sec)
kcal_tot = round(kcal_tot + kcal_sec, 2)
fat_tot = round(fat_tot + fat_sec, 2)
carb_tot = round(carb_tot + carb_sec, 2)

print("Les calories del teu plat són ", kcal_tot, "kcal.")
print("Hi ha ", fat_tot, "g de greix.")
print("Hi ha ", carb_tot, "g de carbohidrats.")
