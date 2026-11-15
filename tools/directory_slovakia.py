#!/usr/bin/env python3
"""Validated directory fragments for canonical Orthodox bodies in Slovakia.

The current official schematisms of the two Slovak eparchies are the source
of truth. Distinct churches, chapels, monasteries, church communities, and
temporary worship sites are preserved even when one priest serves several.

    python tools/directory_slovakia.py --check
    python tools/directory_slovakia.py --dump
"""

import argparse
import json
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
CHECKED = "2026-11-15"
COUNTRY = "SK"
PRESOV_SOURCE = "https://orthodox.sk/schematizmus/pe-pravoslavna-eparchia/"
MICHALOVCE_SOURCE = "https://orthodox.sk/schematizmus/pravoslavna-eparchia/"


def spec(slug, place, dedication, local, rank="Church", kind="parish"):
    if dedication:
        name = "%s Orthodox %s in %s" % (dedication, rank, place)
    else:
        name = "Orthodox %s in %s" % (rank, place)
    return slug, place, name, local, rank, kind


PRESOV_SPECS = [
    spec("medzilaborce-saint-nicholas-charity", "Medzilaborce", "Saint Nicholas", "Kaplnka sv. Nikolaja", "Chapel"),
    spec("komarno-deposition-robe-monastery", "Komárno", "Deposition of the Robe of the Most Holy Theotokos", "Monastier Položenia rúcha Presvätej Bohorodičky", "Monastery", "monastery"),
    spec("presov-alexander-nevsky", "Prešov", "Saint Alexander Nevsky", "Katedrálny chrám sv. kniežaťa Alexandra Nevského", "Cathedral"),
    spec("presov-exaltation-cross", "Prešov", "Exaltation of the Holy Cross", "Biskupská kaplnka Vyvýšenia svätého Kríža", "Episcopal Chapel"),
    spec("bajerovce-elijah", "Bajerovce", "Holy Prophet Elijah", "Chrám sv. proroka Eliáša"),
    spec("jarabina-nativity-theotokos", "Jarabina", "Nativity of the Most Holy Theotokos", "Chrám Narodenia Presvätej Bohorodičky"),
    spec("jarabina-haj-dormition", "Jarabina", "Dormition of the Most Holy Theotokos at Háj Hill", "Kaplnka Usnutia Presvätej Bohorodičky na hôrke Háj", "Chapel"),
    spec("litmanova-transfiguration", "Litmanová", "Transfiguration of the Lord", "Chrám Premenenia Isusa Christa"),
    spec("udol-demetrius", "Údol", "Great Martyr Demetrius of Thessalonica", "Chrám sv. veľkomučeníka Dimitrija Solúnskeho, Mirotočca"),
    spec("sarisske-jastrabie-protection", "Šarišské Jastrabie", "Protection of the Most Holy Theotokos", "Náhradné bohoslužobné priestory", "Worship Site"),
    spec("sabinov-protection", "Sabinov", "Protection of the Most Holy Theotokos", "Chrám Pokrova Presvätej Bohorodičky"),
    spec("lutina-dormition", "Ľutina", "Dormition of the Most Holy Theotokos", "Chrám Usnutia Presvätej Bohorodičky"),
    spec("hanigovce-demetrius", "Hanigovce", "Great Martyr Demetrius of Thessalonica", "Chrám sv. vmč. Dimitrija Solúnskeho"),
    spec("stara-lubovna-ascension", "Stará Ľubovňa", "Ascension of the Lord", "Chrám Nanebovstúpenia Isusa Christa"),
    spec("vranov-protection", "Vranov nad Topľou", "Protection of the Most Holy Theotokos", "Chrám Pokrova Presvätej Bohorodičky"),
    spec("bardejov-seraphim-upper", "Bardejov", "Saint Seraphim of Sarov", "Chrám sv. Serafima Sarovského (vrchný chrám)"),
    spec("bardejov-cyril-methodius-lower", "Bardejov", "Saints Cyril and Methodius", "Chrám sv. apoštolom rovných Cyrila a Metoda (spodný chrám)"),
    spec("bardejovske-kupele-panteleimon", "Bardejovské Kúpele", "Great Martyr Panteleimon", "Chrám sv. veľkomučeníka Pantelejmona"),
    spec("becherov-protection", "Becherov", "Protection of the Most Holy Theotokos", "Chrám Pokrova Presvätej Bohorodičky"),
    spec("gerlachov-archangel-michael", "Gerlachov", "Holy Archangel Michael", "Chrám sv. archanjela Michala"),
    spec("kurov-apostle-luke", "Kurov", "Holy Apostle Luke", "Chrám sv. apoštola Lukáša"),
    spec("lukov-holy-spirit", "Lukov", "Descent of the Holy Spirit", "Chrám Zostúpenia Svätého Ducha"),
    spec("mikulasova-peter-paul", "Mikulášová", "Holy Apostles Peter and Paul", "Chrám sv. apoštolov Petra a Pavla"),
    spec("jedlinka-dormition", "Jedlinka", "Dormition of the Most Holy Theotokos", "Chrám Usnutia Presvätej Bohorodičky"),
    spec("petrova-paraskeva", "Petrová", "Venerable Paraskeva", "Chrám ct. Paraskevy"),
    spec("fricka-archangel-michael", "Frička", "Holy Archangel Michael", "Chrám sv. archanjela Michala"),
    spec("hutka-nativity-theotokos", "Hutka", "Nativity of the Most Holy Theotokos", "Chrám Narodenia Presvätej Bohorodičky"),
    spec("dubova-bardejov-nativity-theotokos", "Dubová, Bardejov District", "Nativity of the Most Holy Theotokos", "Chrám Narodenia Presvätej Bohorodičky"),
    spec("sarisske-cierne-nativity-theotokos", "Šarišské Čierne", "Nativity of the Most Holy Theotokos", "Chrám Narodenia Presvätej Bohorodičky"),
    spec("varadka-protection", "Varadka", "Protection of the Most Holy Theotokos", "Chrám Pokrova Presvätej Bohorodičky"),
    spec("nizna-polianka-nativity-theotokos", "Nižná Polianka", "Nativity of the Most Holy Theotokos", "Chrám Narodenia Presvätej Bohorodičky"),
    spec("vysna-polianka-peter-paul", "Vyšná Polianka", "Holy Apostles Peter and Paul", "Chrám sv. apoštolov Petra a Pavla"),
    spec("hrabske-demetrius", "Hrabské", "Great Martyr Demetrius of Thessalonica", "Chrám sv. veľkomučeníka Dimitrija Solúnskeho"),
    spec("humenne-cyril-methodius", "Humenné", "Saints Cyril and Methodius", "Chrám sv. Cyrila a Metoda"),
    spec("kalna-roztoka-kalna-elijah", "Kalná Roztoka, Kalná", "Holy Prophet Elijah", "Chrám sv. proroka Eliáša"),
    spec("kalna-roztoka-roztoka-george", "Kalná Roztoka, Roztoka", "Great Martyr George", "Chrám sv. veľkomučeníka Juraja"),
    spec("klenova-dormition", "Klenová", "Dormition of the Most Holy Theotokos", "Chrám Usnutia Presvätej Bohorodičky"),
    spec("ruska-volova-nativity-john-baptist", "Ruská Volová", "Nativity of Saint John the Baptist", "Chrám Narodenia sv. Jána Krstiteľa"),
    spec("ladomirov-protection", "Ladomírov", "Protection of the Most Holy Theotokos", "Chrám Pokrova Presvätej Bohorodičky"),
    spec("jalova-george", "Jalová", "Great Martyr George", "Chrám sv. veľkomučeníka Juraja"),
    spec("pichne-dormition", "Pichné", "Dormition of the Most Holy Theotokos", "Chrám Usnutia Presvätej Bohorodičky"),
    spec("nechvalova-polianka-ascension", "Nechválová Polianka", "Ascension of the Lord", "Chrám Nanebovstúpenia Isusa Christa"),
    spec("cukalovce-holy-spirit", "Čukalovce", "Descent of the Holy Spirit", "Chrám Zostúpenia Svätého Ducha"),
    spec("osadne-ascension", "Osadné", "Ascension of the Lord", "Chrám Vzniesenia Isusa Christa"),
    spec("hostovice-protection", "Hostovice", "Protection of the Most Holy Theotokos", "Chrám Pokrova Presvätej Bohorodičky"),
    spec("parihuzovce-nativity-theotokos", "Parihuzovce", "Nativity of the Most Holy Theotokos", "Chrám Narodenia Presvätej Bohorodičky"),
    spec("snina-ascension", "Snina", "Ascension of the Lord", "Chrám Nanebovstúpenia Isusa Christa"),
    spec("snina-rastislav", "Snina", "Saint Prince Rastislav of Great Moravia", "Chrám sv. kniežaťa Rastislava Veľkomoravského"),
    spec("stakcin-holy-trinity", "Stakčín", "Holy Trinity", "Chrám Svätej Trojice"),
    spec("prislop-dormition", "Príslop", "Dormition of the Most Holy Theotokos", "Chrám Usnutia Presvätej Bohorodičky"),
    spec("ubla-peter-paul", "Ubľa", "Holy Apostles Peter and Paul", "Chrám sv. apoštolov Petra a Pavla"),
    spec("berezovec-all-saints", "Berezovec", "All Saints", "Chrám Všetkých svätých"),
    spec("hrabova-roztoka-vladimir", "Hrabová Roztoka", "Saint Vladimir", "Chrám sv. Vladimíra"),
    spec("michajlov-nativity-theotokos", "Michajlov", "Nativity of the Most Holy Theotokos", "Chrám Narodenia Presvätej Bohorodičky"),
    spec("ulic-protection", "Ulič", "Protection of the Most Holy Theotokos", "Chrám Pokrova Presvätej Bohorodičky"),
    spec("runina-protection", "Runina", "Protection of the Most Holy Theotokos", "Chrám Pokrova Presvätej Bohorodičky"),
    spec("ulicske-krive-nativity-theotokos", "Uličské Krivé", "Nativity of the Most Holy Theotokos", "Chrám Narodenia Presvätej Bohorodičky"),
    spec("rusky-potok-ascension", "Ruský Potok", "Ascension of the Lord", "Chrám Nanebovstúpenia Isusa Christa"),
    spec("rusky-potok-archangel-michael", "Ruský Potok", "Holy Archangel Michael", "Chrám sv. archanjela Michala - drevený chrám"),
    spec("zboj-holy-spirit", "Zboj", "Descent of the Holy Spirit", "Chrám Zostúpenia Svätého Ducha"),
    spec("nova-sedlica-dormition", "Nová Sedlica", "Dormition of the Most Holy Theotokos", "Chrám Usnutia Presvätej Bohorodičky"),
    spec("cabiny-nativity-theotokos", "Čabiny", "Nativity of the Most Holy Theotokos", "Chrám Narodenia Presvätej Bohorodičky"),
    spec("olsinkov-nativity-theotokos", "Oľšinkov", "Nativity of the Most Holy Theotokos", "Chrám Narodenia Presvätej Bohorodičky"),
    spec("svetlice-protection", "Svetlice", "Protection of the Most Holy Theotokos", "Chrám Pokrova Presvätej Bohorodičky"),
    spec("vyrava-dormition", "Výrava", "Dormition of the Most Holy Theotokos", "Chrám Usnutia Presvätej Bohorodičky"),
    spec("krasny-brod-john-baptist", "Krásny Brod", "Synaxis of Saint John the Baptist", "Chrám Zboru sv. Jána Krstiteľa"),
    spec("rokytovce-archangel-michael", "Rokytovce", "Holy Archangel Michael", "Chrám sv. archanjela Michala"),
    spec("medzilaborce-holy-spirit", "Medzilaborce", "Holy Spirit", "Chrám Svätého Ducha"),
    spec("sukov-seven-moravian-saints", "Sukov", "Seven Moravian Saints", "Chrám sv. Sedmopočetníkov Moravských"),
    spec("vydran-archangel-michael", "Vydraň", "Holy Archangel Michael", "Chrám sv. archanjela Michala"),
    spec("palota-nativity-theotokos", "Palota", "Nativity of the Most Holy Theotokos", "Chrám Narodenia Presvätej Bohorodičky"),
    spec("vysna-jablonka-peter-paul", "Vyšná Jablonka", "Holy Apostles Peter and Paul", "Chrám sv. apoštolov Petra a Pavla"),
    spec("nizna-jablonka-dormition", "Nižná Jablonka", "Dormition of the Most Holy Theotokos", "Chrám Usnutia Presvätej Bohorodičky"),
    spec("zbudska-bela-ascension", "Zbudská Belá", "Ascension of the Lord", "Chrám Nanebovstúpenia Isusa Christa"),
    spec("valentovce-peter-paul", "Valentovce", "Holy Apostles Peter and Paul", "Domový chrám sv. apoštolov Petra a Pavla", "House Church"),
    spec("brusnica-nativity-theotokos", "Brusnica", "Nativity of the Most Holy Theotokos", "Chrám Narodenia Presvätej Bohorodičky"),
    spec("jakusovce-protection", "Jakušovce", "Protection of the Most Holy Theotokos", "Chrám Pokrova Presvätej Bohorodičky"),
    spec("vysna-olsava-elijah", "Vyšná Olšava", "Holy Prophet Elijah", "Chrám proroka Eliáša"),
    spec("lomne-archangel-michael", "Lomné", "Holy Archangel Michael", "Chrám sv. archanjela Michala"),
    spec("bzany-translation-nicholas", "Bžany", "Translation of the Relics of Saint Nicholas to Bari", "Chrám Prenesenia relikvií sv. Nikolaja Čudotvorca do Bari"),
    spec("krucov-paraskeva", "Kručov", "Great Martyr Paraskeva", "Chrám sv. vmč. Paraskevy"),
    spec("vladica-driecna-peter-paul", "Vladiča-Driečna", "Holy Apostles Peter and Paul", "Chrám sv. ap. Petra a Pavla"),
    spec("sucha-ascension", "Suchá", "Ascension of the Lord", "Náhradné bohoslužobné priestory", "Worship Site"),
    spec("olsavka-nativity-theotokos", "Oľšavka", "Nativity of the Most Holy Theotokos", "Chrám Narodenia Presvätej Bohorodičky"),
    spec("velkrop-protection", "Veľkrop", "Protection of the Most Holy Theotokos", "Chrám Pokrova Presvätej Bohorodičky"),
    spec("stropkov-cyril-methodius-lower", "Stropkov", "Saints Cyril and Methodius", "Chrám sv. Cyrila a Metoda (spodný chrám)"),
    spec("stropkov-deposition-robe-upper", "Stropkov", "Deposition of the Robe of the Most Holy Theotokos", "Chrám Položenia rizy Presvätej Bohorodičky (horný chrám)"),
    spec("mikova-archangel-michael", "Miková", "Holy Archangel Michael", "Chrám sv. archanjela Michala"),
    spec("havaj-sergius-radonezh", "Havaj", "Saint Sergius of Radonezh", "Chrám prep. Sergeja Radonežského"),
    spec("vojtovce-dormition", "Vojtovce", "Dormition of the Most Holy Theotokos", "Chrám Usnutia Presvätej Bohorodičky"),
    spec("potocky-protection", "Potôčky", "Protection of the Most Holy Theotokos", "Chrám Pokrova Presvätej Bohorodičky"),
    spec("svidnik-holy-trinity", "Svidník", "Holy Trinity", "Chrám Svätej Trojice"),
    spec("keckovce-archangel-michael", "Kečkovce", "Holy Archangel Michael", "Náhradné bohoslužobné priestory", "Worship Site"),
    spec("roztoky-demetrius", "Roztoky", "Great Martyr Demetrius of Thessalonica", "Chrám sv. vmč. Dimitrija Solúnskeho"),
    spec("kruzlova-peter-paul", "Kružlová", "Holy Apostles Peter and Paul", "Chrám sv. apoštolov Petra a Pavla"),
    spec("dobroslava-elijah", "Dobroslava", "Holy Prophet Elijah", "Chrám sv. proroka Eliáša"),
    spec("nizna-pisana-archangel-michael", "Nižná Pisaná", "Holy Archangel Michael", "Chrám sv. archanjela Michala"),
    spec("ladomirova-archangel-michael", "Ladomirová", "Holy Archangel Michael", "Chrám sv. archanjela Michala"),
    spec("dlhona-peter-paul", "Dlhoňa", "Holy Apostles Peter and Paul", "Chrám sv. apoštolov Petra a Pavla"),
    spec("vapenik-protection", "Vápeník", "Protection of the Most Holy Theotokos", "Chrám Pokrova Presvätej Bohorodičky"),
    spec("krajne-cierno-basil", "Krajné Čierno", "Saint Basil the Great", "Chrám sv. Vasiľa Veľkého"),
    spec("vagrinec-protection", "Vagrinec", "Protection of the Most Holy Theotokos", "Chrám Pokrova Presvätej Bohorodičky"),
    spec("medvedie-demetrius", "Medvedie", "Great Martyr Demetrius of Thessalonica", "Chrám sv. veľkomučeníka Dimitrija Solúnskeho"),
    spec("krajna-porubka-nativity-theotokos", "Krajná Porúbka", "Nativity of the Most Holy Theotokos", "Chrám Narodenia Presvätej Bohorodičky"),
    spec("pstrina-archangel-michael", "Pstriná", "Holy Archangel Michael", "Chrám sv. archanjela Michala"),
    spec("bodruzal-peter-paul", "Bodružal", "Holy Apostles Peter and Paul", "Chrám sv. ap. Petra a Pavla"),
    spec("mirola-nativity-theotokos", "Miroľa", "Nativity of the Most Holy Theotokos", "Chrám Narodenia Presvätej Bohorodičky"),
    spec("sobos-cosmas-damian", "Soboš", "Holy Unmercenaries Cosmas and Damian", "Chrám sv. nezištných Kozmu a Damiána"),
    spec("sapinec-cosmas-damian", "Šapinec", "Holy Unmercenaries Cosmas and Damian", "Chrám sv. nezištných Kozmu a Damiána"),
    spec("nova-polianka-peter-paul", "Nová Polianka", "Holy Apostles Peter and Paul", "Náhradné bohoslužobné priestory", "Worship Site"),
    spec("nizna-jedlova-protection", "Nižná Jedľová", "Protection of the Most Holy Theotokos", "Chrám Pokrova Presvätej Bohorodičky"),
    spec("vysna-jedlova-cosmas-damian", "Vyšná Jedľová", "Holy Unmercenaries Cosmas and Damian", "Chrám sv. nezištných Kozmu a Damiána"),
    spec("belejovce-nativity-theotokos", "Belejovce", "Nativity of the Most Holy Theotokos", "Chrám Narodenia Presvätej Bohorodičky"),
    spec("vysny-mirosov-cosmas-damian", "Vyšný Mirošov", "Holy Unmercenaries Cosmas and Damian", "Chrám sv. nezištných Kozmu a Damiána"),
    spec("nizny-mirosov-ascension", "Nižný Mirošov", "Ascension of the Lord", "Chrám Nanebovstúpenia Isusa Christa"),
    spec("vysny-orlik-ascension", "Vyšný Orlík", "Ascension of the Lord", "Chrám Nanebovstúpenia Isusa Christa"),
    spec("nizny-orlik-archangel-michael", "Nižný Orlík", "Holy Archangel Michael", "Chrám sv. archanjela Michala"),
    spec("dubova-svidnik-nativity-theotokos", "Dubová, Svidník District", "Nativity of the Most Holy Theotokos", "Chrám Narodenia Presvätej Bohorodičky"),
    spec("vernar-nativity-theotokos", "Vernár", "Nativity of the Most Holy Theotokos", "Chrám Narodenia Presvätej Bohorodičky"),
    spec("nova-lesna", "Nová Lesná", "", "Bohoslužby sa konajú v evanjelickom chráme", "Worship Site"),
    spec("poprad-exaltation-cross", "Poprad", "Exaltation of the Holy Cross", "Chrám Vyvýšenia sv. Kríža"),
    spec("liptovsky-mikulas", "Liptovský Mikuláš", "", "Pravoslávna cirkevná obec", "Church Community"),
    spec("ruzomberok", "Ružomberok", "", "Pravoslávna cirkevná obec", "Church Community"),
    spec("levoca-cyril-methodius", "Levoča", "Saints Cyril and Methodius", "Chrám sv. Cyrila a Metoda"),
    spec("lubica-dormition", "Ľubica", "Dormition of the Most Holy Theotokos", "Chrám Usnutia Presvätej Bohorodičky"),
    spec("spisska-nova-ves-clement", "Spišská Nová Ves", "Saint Clement of Ohrid", "Chrám sv. Klimenta Ochridského"),
    spec("slovinky-ascension", "Slovinky", "Ascension of the Lord", "Chrám Nanebovstúpenia Isusa Christa"),
    spec("krompachy-george", "Krompachy", "Great Martyr George", "Náhradné bohoslužobné priestory", "Worship Site"),
    spec("smolnik-protection", "Smolník", "Protection of the Most Holy Theotokos", "Chrám Pokrova Presvätej Bohorodičky"),
    spec("kojsov-peter-paul", "Kojšov", "Holy Apostles Peter and Paul", "Chrám sv. ap. Petra a Pavla"),
    spec("gelnica-dormition", "Gelnica", "Dormition of the Most Holy Theotokos", "Náhradné bohoslužobné priestory", "Worship Site"),
    spec("zavadka-nativity-john-baptist", "Závadka", "Nativity of Saint John the Baptist", "Chrám Narodenia sv. Jána Krstiteľa"),
    spec("sumiac-ascension", "Šumiac", "Ascension of the Lord", "Náhradné bohoslužobné priestory", "Worship Site"),
    spec("telgart-holy-spirit", "Telgárt", "Descent of the Holy Spirit", "Náhradné bohoslužobné priestory", "Worship Site"),
    spec("zvolen-castle-archangel-michael", "Zvolen", "Holy Archangel Michael at Zvolen Castle", "Kaplnka na zámku Zvolen", "Chapel"),
    spec("viglas-castle-archangel-michael", "Vígľaš", "Holy Archangel Michael at Vígľaš Castle", "Kaplnka archanjela Michala na zámku Vígľaš", "Chapel"),
    spec("banska-bystrica-peter-paul", "Banská Bystrica", "Holy Apostles Peter and Paul", "Náhradné bohoslužobné priestory v Slovenskom misijnom hnutí", "Worship Site"),
    spec("bratislava-rastislav", "Bratislava", "Saint Rastislav", "Chrám sv. Rastislava"),
    spec("bratislava-bulgarian-chapel", "Bratislava", "Bulgarian", "Kaplnka na adrese Haburská 83/7", "Chapel"),
    spec("bratislava-saint-nicholas", "Bratislava", "Saint Nicholas", "Chrám sv. Mikuláša"),
    spec("holic-pochaev-cyril-methodius", "Holíč", "Pochaev Icon of the Mother of God and Saints Cyril and Methodius", "Chrám Počájevskej ikony Matky Božej a sv. Cyrila a Metoda"),
    spec("banovce-mary-magdalene", "Bánovce nad Bebravou", "Saint Mary Magdalene", "Náhradné bohoslužobné priestory", "Worship Site"),
    spec("brezova-demetrius", "Brezová pod Bradlom", "Great Martyr Demetrius of Thessalonica", "Náhradné bohoslužobné priestory", "Worship Site"),
    spec("piestany-elizabeth", "Piešťany", "Saint Elizabeth Romanova", "Náhradné bohoslužobné priestory", "Worship Site"),
    spec("komarno-entry-theotokos", "Komárno", "Entry of the Most Holy Theotokos into the Temple", "Chrám Uvedenia do chrámu Presvätej Bohorodičky"),
    spec("trnava-holy-trinity", "Trnava", "Holy Trinity", "Chrám Svätej Trojice"),
    spec("nitra-seven-saints", "Nitra", "Seven Saints", "Kaplnka Vzkriesenia na mestskom cintoríne", "Cemetery Chapel"),
    spec("prievidza", "Prievidza", "", "Náhradné bohoslužobné priestory", "Worship Site"),
    spec("bojnice-mier", "Bojnice", "", "Kaplnka liečebného domu Mier", "Chapel"),
    spec("topolcany-arsenius-paisios", "Topoľčany", "Saints Arsenius of Cappadocia and Paisios of Mount Athos", "Kaplnka sv. Arsenia Kappadockého a Paisija Svätohorského", "Chapel"),
    spec("hontianske-moravce-dormition", "Hontianske Moravce", "Dormition of the Most Holy Theotokos", "Chrám Usnutia Presvätej Bohorodičky"),
    spec("nova-bana", "Nová Baňa", "", "Náhradné bohoslužobné priestory", "Worship Site"),
    spec("zilina-holy-cross", "Žilina", "Holy Cross", "Kaplnka sv. Kríža NsP v Žiline", "Chapel"),
]


MICHALOVCE_SPECS = [
    spec("michalovce-alexis-toth", "Michalovce", "Saint Alexis Toth", "Biskupská kaplnka sv. kňaza vyznávača Alexija Tótha", "Episcopal Chapel"),
    spec("michalovce-cyril-methodius", "Michalovce", "Saints Cyril and Methodius", "Katedrálny chrám apoštolom rovných sv. Cyrila a Metoda", "Cathedral"),
    spec("falkusovce-ascension", "Falkušovce", "Ascension of the Lord", "Chrám Nanebovstúpenia Pána"),
    spec("hazin-nativity-theotokos", "Hažín", "Nativity of the Most Holy Theotokos", "Chrám Narodenia Presvätej Bohorodičky"),
    spec("lastomir-holy-spirit", "Lastomír", "Descent of the Holy Spirit", "Chrám Zostúpenia Svätého Ducha"),
    spec("dubravka-peter-paul", "Dúbravka", "Holy Apostles Peter and Paul", "Chrám sv. apoštolov Petra a Pavla"),
    spec("markovce-dormition", "Markovce", "Dormition of the Most Holy Theotokos", "Chrám Zosnutia Presvätej Bohorodičky"),
    spec("pozdisovce-transfiguration", "Pozdišovce", "Transfiguration of the Lord", "Chrám Premenenia Pána"),
    spec("strazske-ascension-nicholas", "Strážske", "Ascension of the Lord and Saint Nicholas the Wonderworker", "Chrám Nanebovstúpenia Pána a sv. Nikolaja Divotvorcu"),
    spec("samudovce-nativity-john-baptist", "Šamudovce", "Nativity of Saint John the Baptist", "Chrám Narodenia sv. Jána Krstiteľa"),
    spec("velke-kapusany-exaltation-cross", "Veľké Kapušany", "Exaltation of the Holy Cross", "Chrám Vyvýšenia sv. Kríža"),
    spec("zemplinska-siroka-nativity-theotokos", "Zemplínska Široká", "Nativity of the Most Holy Theotokos", "Chrám Narodenia Presvätej Bohorodičky"),
    spec("bezovce-ascension", "Bežovce", "Ascension of the Lord", "Chrám Nanebovstúpenia Isusa Christa"),
    spec("blatne-remety-cyril-methodius", "Blatné Remety", "Saints Cyril and Methodius", "Chrám apoštolom rovných sv. Cyrila a Metoda"),
    spec("chonkovce-transfiguration", "Choňkovce", "Transfiguration of the Lord", "Chrám Premenenia Pána"),
    spec("podhorod-rastislav", "Podhoroď", "Saint Rastislav, Prince of Great Moravia", "Chrám apoštolom rovného sv. Rastislava, kniežaťa veľkomoravského"),
    spec("inovce-elijah-maximus", "Inovce", "Holy Prophet Elijah and Hieromartyr Maximus Sandovich", "Chrám sv. proroka Eliáša a sv. kňaza-mučeníka Maxima Sandoviča"),
    spec("benatina-dormition", "Beňatina", "Dormition of the Most Holy Theotokos", "Chrám Usnutia Presvätej Bohorodičky"),
    spec("nizna-rybnica-dormition", "Nižná Rybnica", "Dormition of the Most Holy Theotokos", "Chrám Usnutia Presvätej Bohorodičky"),
    spec("konus-myrrhbearers", "Koňuš", "Holy Myrrh-bearing Women", "Chrám sv. žien myronosíc"),
    spec("rusky-hrabovec-george", "Ruský Hrabovec", "Great Martyr George", "Chrám sv. veľkomučeníka Juraja"),
    spec("dubrava-holy-spirit", "Dúbrava", "Descent of the Holy Spirit", "Chrám Zostúpenia Svätého Ducha"),
    spec("sobrance-vladimir", "Sobrance", "Saint Prince Vladimir", "Chrám sv. kniežaťa Vladimíra"),
    spec("ubrez-holy-spirit", "Úbrež", "Descent of the Holy Spirit", "Chrám Zostúpenia Svätého Ducha"),
    spec("hnojne-transfiguration", "Hnojné", "Transfiguration of the Lord", "Náhradné bohoslužobné priestory", "Worship Site"),
    spec("brezina-cyril-methodius", "Brezina", "Saints Cyril and Methodius", "Chrám apoštolom rovných sv. Cyrila a Metoda"),
    spec("bysta-george", "Byšta", "Great Martyr George", "Chrám Veľkomučeníka sv. Juraja Víťaza"),
    spec("cejkov-nativity-theotokos", "Cejkov", "Nativity of the Most Holy Theotokos", "Chrám Narodenia Presvätej Bohorodičky"),
    spec("kasov-transfiguration", "Kašov", "Transfiguration of the Lord", "Chrám Premenenia Pána"),
    spec("zemplin-moses-hungarian", "Zemplín", "Saint Moses the Hungarian", "Kaplnka sv. Mojžiša Uhorského", "Chapel"),
    spec("cierna-nad-tisou-archangel-michael", "Čierna nad Tisou", "Holy Archangel Michael", "Náhradné bohoslužobné priestory", "Worship Site"),
    spec("trebisov-peter-paul", "Trebišov", "Holy Apostles Peter and Paul", "Chrám sv. apoštolov Petra a Pavla"),
    spec("zemplinske-hradiste-ascension", "Zemplínske Hradište", "Ascension of the Lord", "Chrám Nanebovstúpenia Pána"),
    spec("zemplinsky-klecenov-nativity-john-baptist", "Zemplínsky Klečenov", "Nativity of Saint John the Baptist", "Chrám Narodenia sv. Jána Krstiteľa"),
    spec("kosice-dormition-john-rosalia", "Košice", "Dormition of the Most Holy Theotokos, Saint John the Merciful, and Saint Rosalia", "Katedrálny chrám Zosnutia Presvätej Bohorodičky a sv. Jána Milostivého a sv. Rozálie", "Cathedral"),
    spec("kosice-stanislav-irenaeus", "Košice", "Saints Stanislav Nasadil and Irenaeus Čirič", "Kaplnka sv. Stanislava Nasadila a sv. Irineja Čiriča", "Chapel"),
    spec("kosice-saca-demetrius", "Košice-Šaca", "Great Martyr Demetrius of Thessalonica", "Ekumenický dom modlitieb sv. veľkomučeníka Dimitrija Solúnskeho", "Worship Site"),
    spec("sklabina", "Sklabiná", "", "Náhradné bohoslužobné priestory", "Worship Site"),
    spec("roznava-paraskeva", "Rožňava", "Venerable Paraskeva of Serbia", "Náhradné bohoslužobné priestory ctihodnej Paraskevy Srbskej v nemocnici", "Chapel"),
    spec("michalovce-military-barbara", "Michalovce", "Great Martyr Barbara", "Pravoslávna kaplnka sv. veľkomučeníčky Barbary", "Chapel"),
]


def make_rows(parent, source, specs):
    rows = []
    for slug, place, name, local, rank, kind in specs:
        rows.append({
            "id": "sk-%s-%s" % ("po" if parent == "cs-presov" else "mk", slug),
            "parent": parent,
            "kind": kind,
            "rank": rank,
            "name": name,
            "local": local,
            "country": COUNTRY,
            "address": ["%s, Slovakia" % place],
            "sources": [source],
            "checked": CHECKED,
            "cite": [source],
        })
    return rows


ROWS = {
    "cs-presov": make_rows("cs-presov", PRESOV_SOURCE, PRESOV_SPECS),
    "cs-michalovce-kosice": make_rows(
        "cs-michalovce-kosice", MICHALOVCE_SOURCE, MICHALOVCE_SPECS
    ),
}


ENGLISH_NAMES = {
    item["id"]: item["name"]
    for source_rows in ROWS.values()
    for item in source_rows
}


EXPECTED = {
    "cs-presov": 153,
    "cs-michalovce-kosice": 40,
}


def build():
    payloads = {}
    seen = set(ROWS)
    for parent, source_rows in ROWS.items():
        rows = []
        for source in source_rows:
            item = dict(source)
            row_id = item.get("id")
            if not row_id or row_id in seen:
                raise ValueError("duplicate or missing id: %s" % row_id)
            if item.get("parent") != parent:
                raise ValueError("%s hangs off an unknown branch parent" % row_id)
            if item.get("kind") not in {"parish", "monastery"}:
                raise ValueError("%s has unsupported kind" % row_id)
            if not item.get("local"):
                raise ValueError("%s has no local name" % row_id)
            if not item.get("sources") or len(item["sources"]) > 3:
                raise ValueError("%s has invalid sources" % row_id)
            seen.add(row_id)
            rows.append(item)
        payloads[parent] = {
            "v": 1,
            "parent": parent,
            "country": COUNTRY,
            "rows": rows,
        }
    counts = {parent: len(payload["rows"])
              for parent, payload in payloads.items()}
    if counts != EXPECTED:
        raise ValueError("Slovakia counts changed: %r" % counts)
    return payloads


def main():
    parser = argparse.ArgumentParser()
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument("--check", action="store_true")
    mode.add_argument("--dump", action="store_true")
    args = parser.parse_args()
    try:
        payloads = build()
    except (OSError, ValueError) as exc:
        print("directory Slovakia: %s" % exc, file=sys.stderr)
        return 1
    if args.dump:
        print(json.dumps(payloads, ensure_ascii=False, indent=2,
                         sort_keys=True))
    print("Slovakia: 193 verified bodies across 2 canonical parents")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
