# -*- coding: utf-8 -*-
import sys
import json
from clarifai.rest import ClarifaiApp
import requests
from llista import llista_pes


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

    # Agafa calories, greixos i carbohidrats d'Edamam
    kcal = float(decoded_response["calories"])
    fat = buscar_edamam(decoded_response["totalNutrients"], "FAT")
    carbo = buscar_edamam(decoded_response["totalNutrients"], "CHOCDF")
    return kcal, fat, carbo


def fer_llista_petita(llista):
    llista_nova = []
    for i in llista:
        x = 0
        if i['value'] >= 0.85:
            verify = edamam(i['name'], "100g ")[0]
            if verify > 0 and i['name'] != "meat" and i['name'] != "steak" and i['name'] != "beef steak":
                llista_nova.append(i['name'])
        if len(llista_nova) < 2 and i['value'] >= 0.8 and i['name'] not in llista_nova:
            verify = edamam(i['name'], "100g ")[0]
            if verify > 0 and i['name'] != "meat" and i['name'] != "steak" and i['name'] != "beef steak":
                llista_nova.append(i['name'])
        if len(llista_nova) < 2 and i['value'] >= 0.75 and i['name'] not in llista_nova:
            verify = edamam(i['name'], "100g ")[0]
            if verify > 0 and i['name'] != "meat" and i['name'] != "steak" and i['name'] != "beef steak":
                llista_nova.append(i['name'])
        x += 1
    return llista_nova


def fins_ingr_princ(filename):
    # Envia foto a clarifai
    app = ClarifaiApp(api_key="b8d70b86df7a49fcb1c7c98c31fed204")
    model = app.models.get("food-items-v1.0")
    result = model.predict_by_filename(filename=filename)

    # Fa la llista més petita
    llista_ingr = fer_llista_petita(result['outputs'][0]['data']['concepts'])
    return llista_ingr


def fins_resultat(ingr_principal, llista_ingr):
    quantitat_princ, quantitat_sec, ingr_sec = llista_pes(llista_ingr, ingr_principal)

    # Agafa les calories del ingredients principal
    kcal_tot, fat_tot, carb_tot = edamam(ingr_principal, quantitat_princ)

    # Agafa les calories del ingredients secundari
    str_ingr_sec = ""
    for ingr in ingr_sec:
        str_ingr_sec += str(ingr + ", ")
    kcal_sec, fat_sec, carb_sec = edamam(str_ingr_sec, quantitat_sec)

    # Suma de calories
    kcal_tot = str(round(kcal_tot + kcal_sec, 2))
    fat_tot = str(round(fat_tot + fat_sec, 2))
    carb_tot = str(round(carb_tot + carb_sec, 2))
    resultat=[kcal_tot, fat_tot,carb_tot]
    return resultat
