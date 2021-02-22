import requests
from Starship import Starship

request =  requests.get("https://swapi.dev/api/starships").json()
results = request["results"]

Ships = []

sorted_by_hyperdrive_rating  =  [Ships.append(Starship(name =  ship["name"], hyper_rating=ship["hyperdrive_rating"]))
                                 for ship in sorted(results, key = lambda x :float(x["hyperdrive_rating"]), reverse= False)]


for i in Ships:
    print(i)

















