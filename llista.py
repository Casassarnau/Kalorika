# -*- coding: utf-8 -*-
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
    q_p, q_s, ll_neta = tipus_ingr(peixos, llista, ingredient, "150g ", "30g ")
    if q_p:
        return q_p, q_s, ll_neta

    pasta = ["pasta", "spaghetti", "macaroni", "penne", "fettuccine", "spaghetti bolognese", "tagliatelle", "rice",
             "noodle", "lasagna", "gnocchi"]
    q_p, q_s, ll_neta = tipus_ingr(pasta, llista, ingredient, "200g cooked ", "20g ")
    if q_p:
        return q_p, q_s, ll_neta

    llegum = ["lentil", "beans", "lima bean", "pigeon pea", "garbanzo", "kidney bean", "chickpeas", "indian pea", "pea",
              "succotash", "moth bean", "horse gram", "buckwheat", "groats", "mung bean"]
    q_p, q_s, ll_neta = tipus_ingr(llegum, llista, ingredient, "170g cooked ", "30g ")
    if q_p:
        return q_p, q_s, ll_neta

    pastissos = ["brownie", "chocolate cake", "torte", "chocolate chip cake", "fruitcake", "apple pie", "bread pudding",
                 "pastry", "muffin", "cookie", "blueberry muffin", "raisin muffin", "pork pie", "chocolate cookie",
                 "candy", "cream", "chocolate", "doughnut"]
    q_p, q_s, ll_neta = tipus_ingr(pastissos, llista, ingredient, "100g ", "20g ")
    if q_p:
        return q_p, q_s, ll_neta

    verdura = ["vegetable", "tomato", "carrot", "squash", "pumpkin", "celery", "curry", "cucumber", "broccoli",
               "eggplant", "avocado", "onion", "cauliflower", "asparagus", "courgette", "pepper"]
    q_p, q_s, ll_neta = tipus_ingr(verdura, llista, ingredient, "150g ", "50g ")
    if q_p:
        return q_p, q_s, ll_neta

    fruita = ["berry", "blueberry", "strawberry", "blackberry", "raspberry", "banana", "black currant", "pineapple",
              "apple", "lemon", "watermelon", "pear", "peach", "melon", "grape", "grapefruit"]
    q_p, q_s, ll_neta = tipus_ingr(fruita, llista, ingredient, "150g ", "30g ")
    if q_p:
        return q_p, q_s, ll_neta

    begudes = ["wine", "beer", "syrup", "coke", "lemonade", "milk", "tea"]
    q_p, q_s, ll_neta = tipus_ingr(begudes, llista, ingredient, "180ml ", "50g ")
    if q_p:
        n = 0
        for x in ll_neta:
            if x == "cream":
                del ll_neta[n]
            n += 1
        return q_p, q_s, ll_neta

    begudes_a = ["whisky", "rum", "brandy", "cognac", "liqueur", "tequila", "vodka"]
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
