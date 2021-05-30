import pickle
import json
import requests


with open('enderecos_processos.pkl', 'rb') as f:
    data = pickle.load(f)
    localizacoes = data["localizacoes"]
    numero_dos_processos = data["numero_dos_processos"]
    processos = []
    for i, processo in enumerate(numero_dos_processos):
        if i < len(localizacoes):
            enderecos = localizacoes[i]

            address = []
            if enderecos and len(enderecos) > 0:
                for end in enderecos:
                    lat = ""
                    lng = ""
                    try:
                        print(i)
                        # f"https://nominatim.openstreetmap.org/search.php?q={end}&format=json&countrycodes=BR&limit=1"
                        url = f"https://maps.googleapis.com/maps/api/geocode/json?address={end}&region=br&key=AIzaSyDMQ9SbJzjIUE1iQkLL_8XZw7JXkuRlOOg"
                        #url = f"https://maps.googleapis.com/maps/api/place/findplacefromtext/json?input=Museum%20of%20Contemporary%20Art%20Australia&inputtype=textquery&fields=photos,formatted_address,name,rating,opening_hours,geometry&key=AIzaSyDMQ9SbJzjIUE1iQkLL_8XZw7JXkuRlOOg"

                        response = requests.get(url)
                        response.raise_for_status()
                        data = response.json()
                        # print(data)
                        if len(data['results']) > 0:
                            lat = data['results'][0]["geometry"]["location"]["lat"]
                            lng = data['results'][0]["geometry"]["location"]["lng"]
                    except Exception as ex:
                        print(ex)
                    address.append(
                        {"name": end, "lat": lat, "lng": lng}
                    )

            processos.append(
                {
                    "id": i,
                    'nrProcesso': processo,
                    "address": address
                }
            )
    with open(f"processos.json", "w", encoding="utf-8") as file:
        json.dump(processos, file, ensure_ascii=False)
