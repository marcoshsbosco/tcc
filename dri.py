import json


selected_data = {}


with open("raw/nutrients.txt", encoding="utf-8") as fp:
    data = fp.read()

data = data.replace("\n", ";")
data = data.replace("\t", "\n")
data = data[:-1]

with open("raw/dri_amounts.txt", encoding="utf-8") as fp:
    amounts = fp.read()

amounts = amounts.replace("*", "")
amounts = amounts.replace(",", "")
amounts = amounts.replace("\n", "")
amounts = amounts.replace("ND", "0")
amounts = amounts.split("\t")

data = data.split("\n")

for i, line in enumerate(data):
    data[i] = line + ";" + amounts[i]

for nutrient in data:
    name, unit, amount = nutrient.split(";")

    unit = unit.replace("(", "")
    unit = unit.replace("/d)", "")

    selected_data[name] = {"unit": unit, "amount": float(amount)}

# all units to grams
for nutrient in selected_data:
    if selected_data[nutrient]["unit"] == "mg":
        coef = 1e3
    elif selected_data[nutrient]["unit"] == "μg":
        coef = 1e6
    elif selected_data[nutrient]["unit"] == "L":
        coef = 1e-3
    elif selected_data[nutrient]["unit"] == "g":
        coef = 1
    else:  # checks for units that weren't converted
        print(f"[ERR] What about {selected_data[nutrient]['unit']}?")
        exit()

    try:
        selected_data[nutrient] = selected_data[nutrient]["amount"] / coef
    except ZeroDivisionError:
        selected_data[nutrient] = 0

with open("dri.json", "w", encoding="utf-8") as fp:
    json.dump(selected_data, fp, ensure_ascii=False, indent=4)
