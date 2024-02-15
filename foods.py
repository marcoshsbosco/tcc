import json


selected_data = {}


with open("raw/foundationDownload.json") as fp:
    data = json.load(fp)

# collect all food categories
for food in data["FoundationFoods"]:
    selected_data[food["foodCategory"]["description"]] = {}

for food in data["FoundationFoods"]:
    selected_data[food["foodCategory"]["description"]].update({food["description"]: {}})

    for nutrient in food["foodNutrients"]:
        try:
            if nutrient["nutrient"]["unitName"] == "g":
                selected_data[food["foodCategory"]["description"]][food["description"]].update({nutrient["nutrient"]["name"]: nutrient["amount"]})
            elif nutrient["nutrient"]["unitName"] == "µg":
                selected_data[food["foodCategory"]["description"]][food["description"]].update({nutrient["nutrient"]["name"]: nutrient["amount"] / 1e6})
            elif nutrient["nutrient"]["unitName"] == "mg":
                selected_data[food["foodCategory"]["description"]][food["description"]].update({nutrient["nutrient"]["name"]: nutrient["amount"] / 1e3})
            elif nutrient["nutrient"]["unitName"] == "kcal":
                selected_data[food["foodCategory"]["description"]][food["description"]].update({nutrient["nutrient"]["name"]: nutrient["amount"] * 4184})
            elif nutrient["nutrient"]["unitName"] == "kJ":
                selected_data[food["foodCategory"]["description"]][food["description"]].update({nutrient["nutrient"]["name"]: nutrient["amount"] / 1e-3})
            elif nutrient["nutrient"]["unitName"] == "IU":
                pass
            elif nutrient["nutrient"]["unitName"] == "sp gr":
                pass
            else:
                print(f"[ERR] What about {nutrient['nutrient']['unitName']} ({nutrient['nutrient']['name']})?")
                exit()
        except KeyError as e:
            if "unitName" in e.args:
                print(f'[WARN] "{food["description"]}" has no {nutrient["nutrient"]["name"]} data.')

                del selected_data[food["foodCategory"]["description"]][food["description"]]

                break
            else:
                raise

with open("foods.json", "w") as fp:
    json.dump(selected_data, fp, ensure_ascii=False, indent=4)
