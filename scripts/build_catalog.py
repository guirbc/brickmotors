# scripts/build_catalog.py
# -*- coding: utf-8 -*-
import csv, os

CATALOG = {
    "Chevrolet": [
        "Onix","Onix Plus","Prisma","Celta","Corsa","Corsa Sedan","Classic","Agile",
        "Astra","Vectra","Vectra GT","Cruze","Cruze Sport6","Spin","Cobalt",
        "Tracker","Equinox","Trailblazer","Blazer","Captiva","Camaro","Omega",
        "S10","Montana","Meriva","Zafira"
    ],
    "Volkswagen": [
        "Gol","Voyage","Fox","CrossFox","SpaceFox","Polo","Virtus","Golf","Jetta",
        "Passat","up!","T-Cross","Nivus","Taos","Tiguan","Saveiro","Amarok",
        "Fusca","Kombi","Santana","Parati","Bora","New Beetle"
    ],
    "Fiat": [
        "Uno","Mille","Palio","Palio Weekend","Siena","Grand Siena","Mobi","Argo",
        "Cronos","Punto","Bravo","Idea","Stilo","Linea","500","Toro","Strada",
        "Fiorino","Doblò","Pulse","Fastback","Tipo","Tempra","Freemont","Ducato"
    ],
    "Ford": [
        "Ka","Ka Sedan","Fiesta","Fiesta Sedan","Focus","Focus Sedan","Fusion",
        "Mondeo","EcoSport","Ranger","Maverick","Territory","Edge","Edge ST",
        "Mustang","Courier","Escort","F-250"
    ],
    "Toyota": [
        "Corolla","Corolla Cross","Yaris","Yaris Sedan","Etios","Etios Sedan",
        "Hilux","SW4","RAV4","Camry","Prius","Land Cruiser Prado","Land Cruiser",
        "Yaris Cross","GR86","Supra"
    ],
    "Hyundai": [
        "HB20","HB20S","HB20X","Creta","Creta N Line","Tucson","ix35","Santa Fe",
        "Azera","Elantra","Sonata","i30","Kona","Veloster"
    ],
    "Honda": [
        "Civic","Civic Si","City","City Hatch","Fit","WR-V","HR-V","CR-V","Accord"
    ],
    "Renault": [
        "Kwid","Sandero","Logan","Stepway","Duster","Duster Oroch","Captur",
        "Fluence","Mégane","Clio","Symbol","Koleos","Scénic","Master"
    ],
    "Nissan": [
        "March","Versa","V-Drive","Kicks","Sentra","Tiida","Livina","X-Trail",
        "Frontier","Altima","Pathfinder","Leaf"
    ],
    "Peugeot": [
        "206","207","208","2008","3008","408","308","307","Hoggar","Partner","Boxer",
        "Expert","RCZ"
    ],
    "Citroën": [
        "C3","C3 Aircross","C4 Lounge","C4 Cactus","C4 Picasso","Grand C4 Picasso",
        "Aircross","Berlingo","Jumper","Jumpy","DS3","DS4","DS5"
    ],
    "Jeep": ["Renegade","Compass","Commander","Wrangler","Grand Cherokee","Cherokee","Gladiator"],
    "BMW": [
        "116i","118i","120i","320i","328i","330e","340i","520i","530e",
        "X1","X2","X3","X4","X5","X6","Z4","i3","i8","M2","M3","M4"
    ],
    "Mercedes-Benz": [
        "A 200","A 45","B 200","C 180","C 200","C 250","C 300","CLA 200","CLA 45",
        "GLA 200","GLA 250","GLB 200","GLC 250","GLC 300","GLE 350","Classe E 250",
        "E 300","S 500","CLC","SLK","Sprinter"
    ],
    "Audi": [
        "A1","A3","A3 Sedan","A4","A5","A6","Q3","Q3 Sportback","Q5","Q7","Q8","TT",
        "RS3","RS4","RS5","e-tron"
    ],
    "Volvo": ["S60","S90","V60","XC40","XC60","XC90","C30","C40"],
    "Kia": ["Picanto","Rio","Cerato","Soul","Sportage","Sorento","Carnival","Bongo","Stonic","Seltos"],
    "Caoa Chery": ["QQ","Celer","Arrizo 5","Arrizo 6","Tiggo 2","Tiggo 3x","Tiggo 5x","Tiggo 7","Tiggo 8"],
    "Mitsubishi": ["Lancer","Eclipse Cross","ASX","Outlander","Pajero TR4","Pajero Sport","Pajero Full","L200 Triton"],
    "Suzuki": ["Jimny","Vitara","Grand Vitara","S-Cross","Swift"],
    "Subaru": ["Impreza","WRX","XV","Forester","Outback","Legacy"],
    "JAC": ["J3","J5","T40","T50","T60","T80","e-JS1","iEV40"],
    "BYD": ["Dolphin","Dolphin Mini","Yuan Plus (ATTO 3)","Han","Tan","Song Plus","Seal","King"],
    "GWM": ["Haval H6","Haval H6 GT","Poer (P-Series)","ORA 03"],
    "RAM": ["1500","1500 Classic","2500","3500","Rampage"],
    "Land Rover": ["Defender","Discovery","Discovery Sport","Range Rover Evoque","Range Rover Velar","Range Rover Sport","Range Rover"],
    "Mini": ["Cooper","Cooper S","Countryman","Clubman","Paceman"],
    "Porsche": ["911","Cayman","Boxster","Panamera","Macan","Cayenne","Taycan"],
    "Jaguar": ["XE","XF","XJ","E-Pace","F-Pace","F-Type","I-Pace"],
    "Tesla": ["Model 3","Model S","Model X","Model Y"],
    "Alfa Romeo": ["145","156","159","Giulietta","MiTo","Giulia","Stelvio"],
    "Dodge": ["Journey","Dakota","Durango","Charger"],
    "Chrysler": ["PT Cruiser","300C","Town & Country","Sebring"],
    "Lifan": ["320","530","620","X60"],
    "Geely": ["GC2","EC7","LC"],
    "Effa": ["M100","V25","Vantage"],
    "Troller": ["T4"],
    "Smart": ["Fortwo","Forfour"],
    "Great Wall": ["Wingle","Haval H3"],
    "Iveco": ["Daily","Daily City","Daily Minibus"],
    "Ferrari": ["California","458 Italia","488 GTB","F8 Tributo","Roma","Portofino"],
    "Lamborghini": ["Gallardo","Huracán","Aventador","Urus"],
    "Maserati": ["Ghibli","Quattroporte","Levante","GranTurismo"],
    "Peugeot-Citroën (DS Automobiles)": ["DS 3","DS 4","DS 5","DS 7 Crossback"]
}

os.makedirs("data", exist_ok=True)
out = "data/catalog.csv"
with open(out, "w", newline="", encoding="utf-8") as f:
    w = csv.writer(f)
    w.writerow(["make", "model"])
    for make, models in CATALOG.items():
        for m in models:
            w.writerow([make, m])

print(f"OK! Gerado {out} com {sum(len(v) for v in CATALOG.values())} linhas.")
