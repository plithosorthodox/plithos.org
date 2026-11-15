#!/usr/bin/env python3
"""Validated directory fragments for canonical Orthodox bodies in Germany.

The parent jurisdictions also carry rows from other countries. This module
emits Germany-only fragments for later merging and never writes a shared
payload.

    python tools/directory_germany.py --check
    python tools/directory_germany.py --dump
"""

import argparse
import json
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent
CHECKED = "2026-11-14"

SPINE_ROW_PROPOSALS = {
  "ep-ukrainian-western-europe": {
    "id": "ep-ukrainian-western-europe",
    "parent": "constantinople",
    "kind": "diocese",
    "rank": "Diocese",
    "name": "Ukrainian Orthodox Diocese of Western Europe",
    "local": "Ukrainische Orthodoxe Diözese von Westeuropa",
    "country": "DE",
    "site": "https://www.uokd.de/",
    "sources": [
      "https://www.uokd.de/",
      "https://www.uokd.de/gemeinden"
    ],
    "cite": [
      "https://www.uokd.de/",
      "https://www.uokd.de/gemeinden"
    ],
    "checked": "2026-11-14"
  }
}

ROWS = {
  "ep-germany": [
    {
      "id": "de-ep-kirchengemeinde-agia-trias-bonn-metropolitankathedrale-agia-trias-dietrich-bonhoeffer-st",
      "parent": "ep-germany",
      "kind": "parish",
      "rank": "Cathedral",
      "name": "Greek Orthodox Metropolitan Cathedral of Agia Trias in Bonn",
      "local": "Metropolitankathedrale Agia Trias",
      "country": "DE",
      "sources": [
        "https://www.orthodoxie.net/kirchengemeinden"
      ],
      "address": [
        "Dietrich-Bonhoeffer-Str. 2, 53227 Bonn-Beuel"
      ],
      "services": [
        "Göttliche Liturgie: sonntags, 9.00-12.00 Uhr"
      ]
    },
    {
      "id": "de-ep-kirchengemeinde-heiliger-johannes-der-taufer-bruhl-kirche-des-heiligen-johannes-des-tauf",
      "parent": "ep-germany",
      "kind": "parish",
      "rank": "Parish",
      "name": "Greek Orthodox Church of St. John the Baptist in Brühl",
      "local": "Kirche des heiligen Johannes des Täufers",
      "country": "DE",
      "sources": [
        "https://www.orthodoxie.net/kirchengemeinden"
      ],
      "address": [
        "Wallstr. 102, 50321 Brühl"
      ],
      "services": [
        "Göttliche Liturgie: sonntags, 9.30-11.30 Uhr"
      ]
    },
    {
      "id": "de-ep-kirchengemeinde-heiliger-johannes-der-taufer-bruhl-wesseling-kirche-der-heiligen-konstan",
      "parent": "ep-germany",
      "kind": "parish",
      "rank": "Worship site",
      "name": "Greek Orthodox Wesseling: Church of Saints Constantine and Helena",
      "local": "Wesseling: Kirche der heiligen Konstantin und Helena",
      "country": "DE",
      "sources": [
        "https://www.orthodoxie.net/kirchengemeinden"
      ],
      "address": [
        "Friedensweg 17, 50389 Wesseling"
      ],
      "services": [
        "Göttliche Liturgie: sonntags, 7.00-9.00 Uhr"
      ]
    },
    {
      "id": "de-ep-kirchengemeinde-heiliger-dimitrios-troisdorf-kirche-des-heiligen-dimitrios-demetriosplat",
      "parent": "ep-germany",
      "kind": "parish",
      "rank": "Parish",
      "name": "Greek Orthodox Church of Saint Dimitrios in Troisdorf",
      "local": "Kirche des heiligen Dimitrios",
      "country": "DE",
      "sources": [
        "https://www.orthodoxie.net/kirchengemeinden"
      ],
      "address": [
        "Demetriosplatz (Camp-Spich-Str. 2), 53842 Troisdorf-Spich"
      ],
      "services": [
        "Göttliche Liturgie: sonntags, 8.45-11.00 Uhr"
      ]
    },
    {
      "id": "de-ep-kirchengemeinde-entschlafen-der-gottesgebarerin-koln-kirche-des-entschlafens-der-gottesg",
      "parent": "ep-germany",
      "kind": "parish",
      "rank": "Parish",
      "name": "Greek Orthodox Church of the Dormition of the Theotokos in Köln",
      "local": "Kirche des Entschlafens der Gottesgebärerin",
      "country": "DE",
      "sources": [
        "https://www.orthodoxie.net/kirchengemeinden"
      ],
      "address": [
        "Urbanstr. 1, 50679 Köln-Deutz"
      ],
      "services": [
        "Göttliche Liturgie: sonntags, 9.00-12.00 Uhr"
      ]
    },
    {
      "id": "de-ep-kirchengemeinde-heiliger-dimitrios-aachen-kirche-des-heiligen-erzengels-michael-des-heil",
      "parent": "ep-germany",
      "kind": "parish",
      "rank": "Parish",
      "name": "Greek Orthodox Church of St. Archangel Michael - St. Dimitrios in Aachen",
      "local": "Kirche des heiligen Erzengels Michael - des heiligen Dimitrios",
      "country": "DE",
      "sources": [
        "https://www.orthodoxie.net/kirchengemeinden"
      ],
      "address": [
        "Jesuitenstr. 6, 52062 Aachen"
      ],
      "services": [
        "Göttliche Liturgie: sonntags, 8.30-11.00 Uhr"
      ]
    },
    {
      "id": "de-ep-kirchengemeinde-heiliger-dimitrios-aachen-duren-nord-st-joachim-alte-julicher-str-52353",
      "parent": "ep-germany",
      "kind": "parish",
      "rank": "Worship site",
      "name": "Greek Orthodox Düren (North): St. Joachim in Düren (Nord)",
      "local": "Düren (Nord): St. Joachim",
      "country": "DE",
      "sources": [
        "https://www.orthodoxie.net/kirchengemeinden"
      ],
      "address": [
        "Alte Jülicher Str., 52353 Düren"
      ],
      "services": [
        "Göttliche Liturgie: jeden ersten Sonntag im Monat, 13.00 Uhr"
      ]
    },
    {
      "id": "de-ep-kirchengemeinde-heiliger-dimitrios-aachen-heinsberg-oberbruch-st-antonius-kapelle-grebbe",
      "parent": "ep-germany",
      "kind": "parish",
      "rank": "Worship site",
      "name": "Greek Orthodox Heinsberg-Oberbruch: St. Antonius Chapel",
      "local": "Heinsberg-Oberbruch: St. Antonius-Kapelle",
      "country": "DE",
      "sources": [
        "https://www.orthodoxie.net/kirchengemeinden"
      ],
      "address": [
        "Grebbener Str., 52525 Heinsberg-Oberbruch"
      ],
      "services": [
        "Göttliche Liturgie: jeden zweiten Sonntag im Monat, 13.30 Uhr"
      ]
    },
    {
      "id": "de-ep-kirchengemeinde-heiliger-nektarios-neuss-kirche-des-heiligen-nektarios-am-lindenplatz-31",
      "parent": "ep-germany",
      "kind": "parish",
      "rank": "Parish",
      "name": "Greek Orthodox Church of Saint Nektarios in Neuss",
      "local": "Kirche des heiligen Nektarios",
      "country": "DE",
      "sources": [
        "https://www.orthodoxie.net/kirchengemeinden"
      ],
      "address": [
        "Am Lindenplatz 31, 41466 Neuss"
      ],
      "services": [
        "Göttliche Liturgie: sonntags, 9.00-11.30 Uhr"
      ]
    },
    {
      "id": "de-ep-kirchengemeinde-heiliger-nikolaos-monchengladbach-kirche-des-heiligen-nikolaos-karstr-1",
      "parent": "ep-germany",
      "kind": "parish",
      "rank": "Parish",
      "name": "Greek Orthodox Church of Saint Nicholas in Mönchengladbach",
      "local": "Kirche des heiligen Nikolaos",
      "country": "DE",
      "sources": [
        "https://www.orthodoxie.net/kirchengemeinden"
      ],
      "address": [
        "Karstr. 1, 41068 Mönchengladbach"
      ],
      "services": [
        "Göttliche Liturgie: sonntags, 8.30-11.30 Uhr"
      ]
    },
    {
      "id": "de-ep-kirchengemeinde-heiliger-apostel-andreas-dusseldorf-kirche-des-heiligen-apostels-andreas",
      "parent": "ep-germany",
      "kind": "parish",
      "rank": "Parish",
      "name": "Greek Orthodox Church of St. Andrew the Apostle in Düsseldorf",
      "local": "Kirche des heiligen Apostels Andreas",
      "country": "DE",
      "sources": [
        "https://www.orthodoxie.net/kirchengemeinden"
      ],
      "address": [
        "Am Schönenkamp 1, 40599 Düsseldorf"
      ],
      "services": [
        "Göttliche Liturgie: sonntags, 9.30-11.30 Uhr"
      ]
    },
    {
      "id": "de-ep-kirchengemeinde-heilige-erzengel-zu-dusseldorf-deutschsprachig-kirche-heilige-erzengel-u",
      "parent": "ep-germany",
      "kind": "parish",
      "rank": "Parish",
      "name": "Greek Orthodox Church of the Holy Archangels and Saint Nicholas in Düsseldorf (German-speaking)",
      "local": "Kirche Heilige Erzengel und Heiliger Nikolaus zu Düsseldorf",
      "country": "DE",
      "sources": [
        "https://www.orthodoxie.net/kirchengemeinden"
      ],
      "address": [
        "in der kath. Kirche St. Theresia vom Kind Jesu, Prenzlauer Str. 4, 40595 Düsseldorf"
      ],
      "services": [
        "Göttliche Liturgie: sonntags, 10.30-12.30 Uhr"
      ]
    },
    {
      "id": "de-ep-kirchengemeinde-heiliger-geist-krefeld-kirche-des-heiligen-geistes-sachsenweg-1-47807-kr",
      "parent": "ep-germany",
      "kind": "parish",
      "rank": "Parish",
      "name": "Greek Orthodox Church of the Holy Spirit in Krefeld",
      "local": "Kirche des Heiligen Geistes",
      "country": "DE",
      "sources": [
        "https://www.orthodoxie.net/kirchengemeinden"
      ],
      "address": [
        "Sachsenweg 1, 47807 Krefeld"
      ],
      "services": [
        "Göttliche Liturgie: jeden ersten und dritten Sonntag im Monat, 8.00-11.00 Uhr, und jeden zweiten und vierten Sonntag im Monat, 11.30-13.00 Uhr"
      ]
    },
    {
      "id": "de-ep-kirchengemeinde-heilige-apostel-petrus-und-paulus-duisburg-kirche-der-heiligen-apostel-p",
      "parent": "ep-germany",
      "kind": "parish",
      "rank": "Parish",
      "name": "Greek Orthodox Church of the Holy Apostles Peter and Paul in Duisburg",
      "local": "Kirche der heiligen Apostel Petrus und Paulus",
      "country": "DE",
      "sources": [
        "https://www.orthodoxie.net/kirchengemeinden"
      ],
      "address": [
        "Johanniterstr. 48, 47053 Duisburg"
      ],
      "services": [
        "Göttliche Liturgie: jeden ersten und dritten Sonntag im Monat, 11.30-13.00 Uhr, und jeden zweiten und vierten Sonntag im Monat, 8.00-11.00 Uhr"
      ]
    },
    {
      "id": "de-ep-kirchengemeinde-heilige-erzengel-oberhausen-kirche-der-heiligen-erzengel-vestische-str-8",
      "parent": "ep-germany",
      "kind": "parish",
      "rank": "Parish",
      "name": "Greek Orthodox Church of the Holy Archangels in Oberhausen",
      "local": "Kirche der heiligen Erzengel",
      "country": "DE",
      "sources": [
        "https://www.orthodoxie.net/kirchengemeinden"
      ],
      "address": [
        "Vestische Str. 8, 46117 Oberhausen"
      ],
      "services": [
        "Göttliche Liturgie: sonntags, 8.30-11.15 Uhr"
      ]
    },
    {
      "id": "de-ep-kirchengemeinde-heilige-paraskevi-solingen-kirche-der-heiligen-paraskevi-wupperstr-120-4",
      "parent": "ep-germany",
      "kind": "parish",
      "rank": "Parish",
      "name": "Greek Orthodox Church of Saint Paraskevi in Solingen",
      "local": "Kirche der heiligen Paraskevi",
      "country": "DE",
      "sources": [
        "https://www.orthodoxie.net/kirchengemeinden"
      ],
      "address": [
        "Wupperstr. 120, 42651 Solingen"
      ],
      "services": [
        "Göttliche Liturgie: jeden Sonntag, 8.30 Uhr"
      ]
    },
    {
      "id": "de-ep-kirchengemeinde-heilige-paraskevi-solingen-burscheid-durscheid-kirche-der-heiligen-paras",
      "parent": "ep-germany",
      "kind": "parish",
      "rank": "Worship site",
      "name": "Greek Orthodox Burscheid-Dürscheid: Church of Saint Paraskevi",
      "local": "Burscheid-Dürscheid: Kirche der heiligen Paraskevi",
      "country": "DE",
      "sources": [
        "https://www.orthodoxie.net/kirchengemeinden"
      ],
      "address": [
        "Kapellenweg 3, 51399 Burscheid-Dürscheid"
      ],
      "services": [
        "Göttliche Liturgie: sonntags, 10.30 Uhr"
      ]
    },
    {
      "id": "de-ep-kirchengemeinde-lebensspendende-quelle-wuppertal-kirche-der-lebensspendenden-quelle-uell",
      "parent": "ep-germany",
      "kind": "parish",
      "rank": "Parish",
      "name": "Greek Orthodox Church of the Life-Giving Spring in Wuppertal",
      "local": "Kirche der Lebensspendenden Quelle",
      "country": "DE",
      "sources": [
        "https://www.orthodoxie.net/kirchengemeinden"
      ],
      "address": [
        "Uellendahler Str. 407, 42109 Wuppertal"
      ],
      "services": [
        "Göttliche Liturgie: sonntags, 9.00-11.30 Uhr"
      ]
    },
    {
      "id": "de-ep-kirchengemeinde-lebensspendende-quelle-wuppertal-velbert-kirche-des-heiligen-dimitrios-a",
      "parent": "ep-germany",
      "kind": "parish",
      "rank": "Worship site",
      "name": "Greek Orthodox Velbert: Church of Saint Dimitrios",
      "local": "Velbert: Kirche des heiligen Dimitrios",
      "country": "DE",
      "sources": [
        "https://www.orthodoxie.net/kirchengemeinden"
      ],
      "address": [
        "Am Lieversholz 47, 42551 Velbert"
      ],
      "services": [
        "Göttliche Liturgie: sonntags, 8.30-10.30 Uhr"
      ]
    },
    {
      "id": "de-ep-kirchengemeinde-heilige-konstantin-und-eleni-siegen-kirche-der-heiligen-konstantin-und-h",
      "parent": "ep-germany",
      "kind": "parish",
      "rank": "Parish",
      "name": "Greek Orthodox Church of Saints Constantine and Helena in Siegen",
      "local": "Kirche der heiligen Konstantin und Helena",
      "country": "DE",
      "sources": [
        "https://www.orthodoxie.net/kirchengemeinden"
      ],
      "address": [
        "Am Rain 17, 57074 Siegen"
      ],
      "services": [
        "Göttliche Liturgie: jeden zweiten und vierten Sonntag im Monat, 11.00 Uhr"
      ]
    },
    {
      "id": "de-ep-kirchengemeinde-heilige-konstantin-und-eleni-siegen-olpe-kirche-des-heiligen-nikolaous-s",
      "parent": "ep-germany",
      "kind": "parish",
      "rank": "Worship site",
      "name": "Greek Orthodox Olpe: Church of St. Nicholas",
      "local": "Olpe: Kirche des heiligen Nikolaous",
      "country": "DE",
      "sources": [
        "https://www.orthodoxie.net/kirchengemeinden"
      ],
      "address": [
        "St. Marien (Krypta), Günsestr. 8, 57462 Olpe"
      ],
      "services": [
        "Göttliche Liturgie: jeden zweiten Sonntag im Monat, 14.00 Uhr"
      ]
    },
    {
      "id": "de-ep-kirchengemeinde-heilige-konstantin-und-eleni-siegen-gummersbach-rebbelroth-kirche-der-he",
      "parent": "ep-germany",
      "kind": "parish",
      "rank": "Worship site",
      "name": "Greek Orthodox Gummersbach-Rebbelroth: Church of the holy unselfish doctors Kosmas and Damian",
      "local": "Gummersbach-Rebbelroth: Kirche der heiligen uneigennützigen Ärzte Kosmas und Damian",
      "country": "DE",
      "sources": [
        "https://www.orthodoxie.net/kirchengemeinden"
      ],
      "address": [
        "Alte Schule 3, 51645 Gummersbach-Rebbelroth"
      ],
      "services": [
        "Göttliche Liturgie: jeden ersten und dritten Sonntag im Monat, 9.00 Uhr"
      ]
    },
    {
      "id": "de-ep-kirchengemeinde-heiliger-nektarios-ludenscheid-kirche-des-heiligen-nektarios-sedanstr-7",
      "parent": "ep-germany",
      "kind": "parish",
      "rank": "Parish",
      "name": "Greek Orthodox Church of Saint Nektarios in Lüdenscheid",
      "local": "Kirche des heiligen Nektarios",
      "country": "DE",
      "sources": [
        "https://www.orthodoxie.net/kirchengemeinden"
      ],
      "address": [
        "Sedanstr. 7, 58507 Lüdenscheid"
      ],
      "services": [
        "Göttliche Liturgie: sonntags, 11.00-13.00 Uhr"
      ]
    },
    {
      "id": "de-ep-kirchengemeinde-heiliger-nektarios-ludenscheid-hagen-kirche-der-heiligen-irini-chrisoval",
      "parent": "ep-germany",
      "kind": "parish",
      "rank": "Worship site",
      "name": "Greek Orthodox Hagen: Church of Saint Irini Chrisovalantou",
      "local": "Hagen: Kirche der heiligen Irini Chrisovalantou",
      "country": "DE",
      "sources": [
        "https://www.orthodoxie.net/kirchengemeinden"
      ],
      "address": [
        "Elfriedenhöhe 1 (im Stadtgarten), 58093 Hagen"
      ],
      "services": [
        "Göttliche Liturgie: sonntags, 8.00-10.00 Uhr"
      ]
    },
    {
      "id": "de-ep-kirchengemeinde-heilige-apostel-dortmund-kirche-der-heiligen-apostel-luisenstr-17-44137",
      "parent": "ep-germany",
      "kind": "parish",
      "rank": "Parish",
      "name": "Greek Orthodox Church of the Holy Apostles in Dortmund",
      "local": "Kirche der heiligen Apostel",
      "country": "DE",
      "sources": [
        "https://www.orthodoxie.net/kirchengemeinden"
      ],
      "address": [
        "Luisenstr. 17, 44137 Dortmund"
      ],
      "services": [
        "Göttliche Liturgie: sonntags, 8.30-11.00 Uhr"
      ]
    },
    {
      "id": "de-ep-kirchengemeinde-heiliger-dimitrios-herten-kirche-des-heiligen-dimitrios-herner-str-99-ec",
      "parent": "ep-germany",
      "kind": "parish",
      "rank": "Parish",
      "name": "Greek Orthodox Church of Saint Dimitrios in Herten",
      "local": "Kirche des heiligen Dimitrios",
      "country": "DE",
      "sources": [
        "https://www.orthodoxie.net/kirchengemeinden"
      ],
      "address": [
        "Herner Str. 99 Ecke Gelsenkirchener Str., 45699 Herten"
      ],
      "services": [
        "Göttliche Liturgie: sonntags, 8.30-11.30 Uhr"
      ]
    },
    {
      "id": "de-ep-kirchengemeinde-heiliger-dimitrios-herten-in-der-griechischen-gemeinde-castrop-rauxel-ze",
      "parent": "ep-germany",
      "kind": "parish",
      "rank": "Worship site",
      "name": "Greek Orthodox in the Greek community of Castrop-Rauxel in in der Griechischen Gemeinde Castrop-Rauxel",
      "local": "in der Griechischen Gemeinde Castrop-Rauxel",
      "country": "DE",
      "sources": [
        "https://www.orthodoxie.net/kirchengemeinden"
      ],
      "address": [
        "Zechenstr. 2a, 44581 Castrop-Rauxel"
      ],
      "services": [
        "Göttliche Liturgie: jeden ersten Samstag im Monat, 10.00-11.30 Uhr"
      ]
    },
    {
      "id": "de-ep-kirchengemeinde-heiliger-dimitrios-herten-munster-kirche-des-heiligen-photios-im-kapuzin",
      "parent": "ep-germany",
      "kind": "parish",
      "rank": "Worship site",
      "name": "Greek Orthodox Münster: Church of Saint Photios",
      "local": "Münster: Kirche des heiligen Photios",
      "country": "DE",
      "sources": [
        "https://www.orthodoxie.net/kirchengemeinden"
      ],
      "address": [
        "im Kapuzinerkloster, Kapuzinerstr. 27, 48149 Münster"
      ],
      "services": [
        "Göttliche Liturgie: jeden dritten Samstag im Monat, 10.00-11.30 Uhr"
      ]
    },
    {
      "id": "de-ep-kirchengemeinde-heiliger-nikolaos-iserlohn-kirche-des-heiligen-nikolaos-wiemer-3-58636-i",
      "parent": "ep-germany",
      "kind": "parish",
      "rank": "Parish",
      "name": "Greek Orthodox Church of Saint Nicholas in Iserlohn",
      "local": "Kirche des heiligen Nikolaos",
      "country": "DE",
      "sources": [
        "https://www.orthodoxie.net/kirchengemeinden"
      ],
      "address": [
        "Wiemer 3, 58636 Iserlohn"
      ],
      "services": [
        "Göttliche Liturgie: sonntags, 8.00-10.45 Uhr"
      ]
    },
    {
      "id": "de-ep-kirchengemeinde-heiliger-nikolaos-iserlohn-menden-kirche-des-heiligen-georgios-an-der-he",
      "parent": "ep-germany",
      "kind": "parish",
      "rank": "Worship site",
      "name": "Greek Orthodox Menden: Church of Saint Georgios",
      "local": "Menden: Kirche des heiligen Georgios",
      "country": "DE",
      "sources": [
        "https://www.orthodoxie.net/kirchengemeinden"
      ],
      "address": [
        "An der Heilig-Kreuz-Kirche 9, 58706 Menden"
      ],
      "services": [
        "Göttliche Liturgie: jeden dritten Sonntag im Monat, 11.30-13.00 Uhr"
      ]
    },
    {
      "id": "de-ep-kirchengemeinde-heiliger-nikolaos-lippstadt-kirche-des-heiligen-nikolaos-und-des-heilige",
      "parent": "ep-germany",
      "kind": "parish",
      "rank": "Parish",
      "name": "Greek Orthodox Church of Saint Nikolaos and Saint Christopher Lippstadt",
      "local": "Kirche des heiligen Nikolaos und des heiligen Christophorus Lippstadt",
      "country": "DE",
      "sources": [
        "https://www.orthodoxie.net/kirchengemeinden"
      ],
      "address": [
        "Richthofenstr. 19, 59558 Lippstadt"
      ],
      "services": [
        "Göttliche Liturgie: jeden ersten und dritten Sonntag, 8.30-11.30 Uhr"
      ]
    },
    {
      "id": "de-ep-kirchengemeinde-heiliger-nikolaos-lippstadt-herford-kirche-des-heiligen-nektarios-in-der",
      "parent": "ep-germany",
      "kind": "parish",
      "rank": "Worship site",
      "name": "Greek Orthodox Herford: Church of Saint Nektarios",
      "local": "Herford: Kirche des heiligen Nektarios",
      "country": "DE",
      "sources": [
        "https://www.orthodoxie.net/kirchengemeinden"
      ],
      "address": [
        "in der Wolderuskapelle, Münsterkirchplatz 3, 32052 Herford"
      ],
      "services": [
        "Göttliche Liturgie: jeden zweiten und vierten Sonntag im Monat, 9.00-11.30 Uhr"
      ]
    },
    {
      "id": "de-ep-kirchengemeinde-heiliger-apostel-paulus-bielefeld-kirche-des-apostels-paulus-weissenburg",
      "parent": "ep-germany",
      "kind": "parish",
      "rank": "Parish",
      "name": "Greek Orthodox Church of the Apostle Paul in Bielefeld",
      "local": "Kirche des Apostels Paulus",
      "country": "DE",
      "sources": [
        "https://www.orthodoxie.net/kirchengemeinden"
      ],
      "address": [
        "Weißenburger Str. 10, 33607 Bielefeld"
      ],
      "services": [
        "Göttliche Liturgie: sonntags, 9.00 Uhr"
      ]
    },
    {
      "id": "de-ep-kirchengemeinde-heiliger-therapon-gutersloh-kirche-des-heiligen-therapon-oststr-47-33332",
      "parent": "ep-germany",
      "kind": "parish",
      "rank": "Parish",
      "name": "Greek Orthodox Church of Saint Therapon in Gütersloh",
      "local": "Kirche des heiligen Therapon",
      "country": "DE",
      "sources": [
        "https://www.orthodoxie.net/kirchengemeinden"
      ],
      "address": [
        "Oststr. 47, 33332 Gütersloh"
      ],
      "services": [
        "Göttliche Liturgie: sonntags, 8.30-11.30 Uhr"
      ]
    },
    {
      "id": "de-ep-kirchengemeinde-heiliger-therapon-gutersloh-oelde-kirche-des-heiligen-orestis-carl-haver",
      "parent": "ep-germany",
      "kind": "parish",
      "rank": "Worship site",
      "name": "Greek Orthodox Oelde: Church of Saint Orestis",
      "local": "Oelde: Kirche des heiligen Orestis",
      "country": "DE",
      "sources": [
        "https://www.orthodoxie.net/kirchengemeinden"
      ],
      "address": [
        "Carl-Haver-Platz 7a, 59302 Oelde"
      ],
      "services": [
        "Göttliche Liturgie: jeden ersten und dritten Samstag, 8.30 - 10.30 Uhr (Sept.-Juni)"
      ]
    },
    {
      "id": "de-ep-kirchengemeinde-heiliger-therapon-gutersloh-minden-kirche-des-heiligen-kosmas-des-aitoli",
      "parent": "ep-germany",
      "kind": "parish",
      "rank": "Worship site",
      "name": "Greek Orthodox Minden: Church of Saint Cosmas the Aitolian",
      "local": "Minden: Kirche des heiligen Kosmas des Aitoliers",
      "country": "DE",
      "sources": [
        "https://www.orthodoxie.net/kirchengemeinden"
      ],
      "address": [
        "in der Kirche des St Mauritius, Pauline-von-Mallinckrodt-Platz, 32423 Minden"
      ],
      "services": [
        "Göttliche Liturgie: jeden zweiten und vierten Samstag, 8.30 - 10.30 Uhr (Sept.-Juni)"
      ]
    },
    {
      "id": "de-ep-kirchengemeinde-heilige-drei-hierarchen-hannover-kirche-der-drei-hierarchen-mengendamm-1",
      "parent": "ep-germany",
      "kind": "parish",
      "rank": "Parish",
      "name": "Greek Orthodox Church of the Three Hierarchs in Hannover",
      "local": "Kirche der Drei Hierarchen",
      "country": "DE",
      "sources": [
        "https://www.orthodoxie.net/kirchengemeinden"
      ],
      "address": [
        "Mengendamm 16b, 30177 Hannover"
      ],
      "services": [
        "Göttliche Liturgie: sonntags, 7.30 Uhr"
      ]
    },
    {
      "id": "de-ep-kirchengemeinde-heilige-rafael-nikolaos-und-irini-gifhorn-kirche-der-heiligen-rafael-nik",
      "parent": "ep-germany",
      "kind": "parish",
      "rank": "Parish",
      "name": "Greek Orthodox Church of Saints Rafael, Nikolaos and Irini in Gifhorn",
      "local": "Kirche der heiligen Rafael, Nikolaos und Irini",
      "country": "DE",
      "sources": [
        "https://www.orthodoxie.net/kirchengemeinden"
      ],
      "address": [
        "Dannenbütteler Weg 14, 38518 Gifhorn"
      ],
      "services": [
        "Göttliche Liturgie: sonntags, 8.30-11.00 Uhr"
      ]
    },
    {
      "id": "de-ep-kirchengemeinde-heilige-rafael-nikolaos-und-irini-gifhorn-braunschweig-kirche-des-heilig",
      "parent": "ep-germany",
      "kind": "parish",
      "rank": "Worship site",
      "name": "Greek Orthodox Braunschweig: Church of Saint Dimitrios",
      "local": "Braunschweig: Kirche des heiligen Dimitrios",
      "country": "DE",
      "sources": [
        "https://www.orthodoxie.net/kirchengemeinden"
      ],
      "address": [
        "Gerstäckerstr. (in der Nähe der Stadthalle), 38102 Braunschweig"
      ],
      "services": [
        "Göttliche Liturgie: an einem Sonntag im Monat nach Vorankündigung, 12.30 Uhr"
      ]
    },
    {
      "id": "de-ep-kirchengemeinde-heiliger-nikolaos-bremen-wird-von-der-kirchengemeinde-des-heiligen-georg",
      "parent": "ep-germany",
      "kind": "parish",
      "rank": "Parish",
      "name": "Greek Orthodox is looked after by the parish of St. Georgios Lübeck in Bremen",
      "local": "wird von der Kirchengemeinde des heiligen Georgios Lübeck betreut",
      "country": "DE",
      "sources": [
        "https://www.orthodoxie.net/kirchengemeinden"
      ],
      "services": [
        "Göttliche Liturgie: jeden ersten und dritten Samstag im Monat, 10.00 Uhr"
      ]
    },
    {
      "id": "de-ep-kirchengemeinde-heiliger-nikolaos-hamburg-kirche-des-heiligen-nikolaos-sievekingsallee-1",
      "parent": "ep-germany",
      "kind": "parish",
      "rank": "Parish",
      "name": "Greek Orthodox Church of Saint Nicholas in Hamburg",
      "local": "Kirche des heiligen Nikolaos",
      "country": "DE",
      "sources": [
        "https://www.orthodoxie.net/kirchengemeinden"
      ],
      "address": [
        "Sievekingsallee 12b, 20535 Hamburg"
      ],
      "services": [
        "Göttliche Liturgie: sonntags, 8.30-11.30 Uhr"
      ]
    },
    {
      "id": "de-ep-kirchengemeinde-heiliger-georgios-lubeck-kirche-des-heiligen-georgios-kleine-altefahre-6",
      "parent": "ep-germany",
      "kind": "parish",
      "rank": "Parish",
      "name": "Greek Orthodox Church of Saint George in Lübeck",
      "local": "Kirche des heiligen Georgios",
      "country": "DE",
      "sources": [
        "https://www.orthodoxie.net/kirchengemeinden"
      ],
      "address": [
        "Kleine Altefähre 6a, 23552 Lübeck"
      ],
      "services": [
        "Göttliche Liturgie: jeden ersten und zweiten Sonntag im Monat, 9.30-12.00 Uhr"
      ]
    },
    {
      "id": "de-ep-kirchengemeinde-heiliger-georgios-lubeck-hamburg-harburg-franz-josef-kirche-reeseberg-10",
      "parent": "ep-germany",
      "kind": "parish",
      "rank": "Worship site",
      "name": "Greek Orthodox Hamburg-Harburg: Franz Josef Church",
      "local": "Hamburg-Harburg: Franz-Josef-Kirche",
      "country": "DE",
      "sources": [
        "https://www.orthodoxie.net/kirchengemeinden"
      ],
      "address": [
        "Reeseberg 10, 21079 Hamburg-Harburg"
      ],
      "services": [
        "Göttliche Liturgie: jeden vierten Sonntag im Monat, 11.30"
      ]
    },
    {
      "id": "de-ep-kirchengemeinde-heiliger-georgios-lubeck-flensburg-johanniskirche-johanniskirchof-22-249",
      "parent": "ep-germany",
      "kind": "parish",
      "rank": "Worship site",
      "name": "Greek Orthodox Flensburg*: St. John's Church",
      "local": "Flensburg*: Johanniskirche",
      "country": "DE",
      "sources": [
        "https://www.orthodoxie.net/kirchengemeinden"
      ],
      "address": [
        "Johanniskirchof 22, 24937 Flensburg"
      ],
      "services": [
        "Göttliche Liturgie: jeden ersten und zweiten Sonntag im Monat 8.30-9.45 Uhr und jeden dritten Samstag im Monat, 9.00-10.30 Uhr"
      ]
    },
    {
      "id": "de-ep-kirchengemeinde-heiliger-georgios-lubeck-wilhelmshaven-banter-kirche-werftstr-75-26382-w",
      "parent": "ep-germany",
      "kind": "parish",
      "rank": "Worship site",
      "name": "Greek Orthodox Wilhelmshaven: Banter Church",
      "local": "Wilhelmshaven: Banter Kirche",
      "country": "DE",
      "sources": [
        "https://www.orthodoxie.net/kirchengemeinden"
      ],
      "address": [
        "Werftstr. 75, 26382 Wilhelmshaven"
      ],
      "services": [
        "Göttliche Liturgie: jeden fünften Sonntag im Monat, 11.30 Uhr"
      ]
    },
    {
      "id": "de-ep-kirchengemeinde-christi-himmelfahrt-berlin-kirche-der-himmelfahrt-christi-mittelstr-32-1",
      "parent": "ep-germany",
      "kind": "parish",
      "rank": "Parish",
      "name": "Greek Orthodox Church of the Ascension of Christ in Berlin",
      "local": "Kirche der Himmelfahrt Christi",
      "country": "DE",
      "sources": [
        "https://www.orthodoxie.net/kirchengemeinden"
      ],
      "address": [
        "Mittelstr. 32, 12167 Berlin"
      ],
      "services": [
        "Göttliche Liturgie: sonntags, 9.00-11.45 Uhr"
      ]
    },
    {
      "id": "de-ep-kirchengemeinde-heiliger-georg-leipzig-kirche-des-heiligen-georg-russenstr-194-04288-lei",
      "parent": "ep-germany",
      "kind": "parish",
      "rank": "Parish",
      "name": "Greek Orthodox Church of Saint George in Leipzig",
      "local": "Kirche des heiligen Georg",
      "country": "DE",
      "sources": [
        "https://www.orthodoxie.net/kirchengemeinden"
      ],
      "address": [
        "Russenstr. 194, 04288 Leipzig"
      ],
      "services": [
        "Göttliche Liturgie: jeden zweiten Samstag im Monat, 9.30-11.00 Uhr"
      ]
    },
    {
      "id": "de-ep-kirchengemeinde-verklarung-des-erlosers-munchen-kirche-der-verklarung-des-erlosers-salva",
      "parent": "ep-germany",
      "kind": "parish",
      "rank": "Parish",
      "name": "Greek Orthodox Church of the Transfiguration of the Savior (Salvatorkirche) in München",
      "local": "Kirche der Verklärung des Erlösers (Salvatorkirche)",
      "country": "DE",
      "sources": [
        "https://www.orthodoxie.net/kirchengemeinden"
      ],
      "address": [
        "Salvatorstr. 17, 80333 München"
      ],
      "services": [
        "Göttliche Liturgie: sonntags, 8.00-10.30 Uhr"
      ]
    },
    {
      "id": "de-ep-kirchengemeinde-allerheiligen-munchen-allerheiligenkirche-ungererstr-131-80805-munchen",
      "parent": "ep-germany",
      "kind": "parish",
      "rank": "Parish",
      "name": "Greek Orthodox All Saints Church in München",
      "local": "Allerheiligenkirche",
      "country": "DE",
      "sources": [
        "https://www.orthodoxie.net/kirchengemeinden"
      ],
      "address": [
        "Ungererstr. 131, 80805 München"
      ],
      "services": [
        "Göttliche Liturgie: sonntags, 8.00-11.00 Uhr"
      ]
    },
    {
      "id": "de-ep-kirchengemeinde-allerheiligen-munchen-garmisch-partenkirchen-kirche-des-heiligen-nektari",
      "parent": "ep-germany",
      "kind": "parish",
      "rank": "Worship site",
      "name": "Greek Orthodox Garmisch-Partenkirchen: Church of Saint Nektarios",
      "local": "Garmisch-Partenkirchen: Kirche des heiligen Nektarios",
      "country": "DE",
      "sources": [
        "https://www.orthodoxie.net/kirchengemeinden"
      ],
      "address": [
        "in der Johanneskirche, Hindenburgstr. 39a, 82467 Garmisch-Partenkirchen"
      ],
      "services": [
        "Göttliche Liturgie: jeden vierten Sonntag im Monat, 12.00 Uhr"
      ]
    },
    {
      "id": "de-ep-kirchengemeinde-allerheiligen-munchen-geretsried-kirche-des-heiligen-petrus-in-der-petru",
      "parent": "ep-germany",
      "kind": "parish",
      "rank": "Worship site",
      "name": "Greek Orthodox Geretsried: Church of Saint Peter",
      "local": "Geretsried: Kirche des heiligen Petrus",
      "country": "DE",
      "sources": [
        "https://www.orthodoxie.net/kirchengemeinden"
      ],
      "address": [
        "in der Petruskirche, Martin-Luther-Weg 13, 82538 Geretsried"
      ],
      "services": [
        "Göttliche Liturgie: jeden zweiten und vierten Sonntag im Monat, 8.00-10.00 Uhr"
      ]
    },
    {
      "id": "de-ep-kirchengemeinde-heiliger-georg-munchen-kirche-des-heiligen-georg-in-der-evangelisch-luth",
      "parent": "ep-germany",
      "kind": "parish",
      "rank": "Parish",
      "name": "Greek Orthodox Church of Saint George in München",
      "local": "Kirche des heiligen Georg",
      "country": "DE",
      "sources": [
        "https://www.orthodoxie.net/kirchengemeinden"
      ],
      "address": [
        "In der Evangelisch-Lutherischen Auferstehungskirche (ehemals Kirche des heiligen Dimitrios Westend), Gollierstr. 55, 80339 München"
      ],
      "services": [
        "Göttliche Liturgie: sonntags, 12.00-13.30 Uhr"
      ]
    },
    {
      "id": "de-ep-kirchengemeinde-heiliger-andreas-munchen-deutschsprachig-kirche-der-verklarung-des-erlos",
      "parent": "ep-germany",
      "kind": "parish",
      "rank": "Parish",
      "name": "Greek Orthodox Church of the Transfiguration of the Savior in Munich (German-speaking)",
      "local": "Kirche der Verklärung des Erlösers (Salvatorkirche)",
      "country": "DE",
      "sources": [
        "https://www.orthodoxie.net/kirchengemeinden"
      ],
      "address": [
        "Salvatorstr. 17, 80333 München"
      ],
      "services": [
        "Göttliche Liturgie: jeden ersten Sa. im Monat, 18.30-20.00 Uhr"
      ]
    },
    {
      "id": "de-ep-kirchengemeinde-heiliger-stephanos-dachau-kirche-des-heiligen-stephanos-des-ersten-marty",
      "parent": "ep-germany",
      "kind": "parish",
      "rank": "Parish",
      "name": "Greek Orthodox Church of Saint Stephen the First Martyr in Dachau",
      "local": "Kirche des heiligen Stephanos des ersten Märtyrers",
      "country": "DE",
      "sources": [
        "https://www.orthodoxie.net/kirchengemeinden"
      ],
      "address": [
        "(ehemals St.-Johannes-Kirche) Schillerstr. 2, 85221 Dachau"
      ],
      "services": [
        "Göttliche Liturgie: sonntags, 9.00-11.00 Uhr"
      ]
    },
    {
      "id": "de-ep-kirchengemeinde-heiliger-panteleimon-augsburg-kirche-des-heiligen-panteleimon-max-von-la",
      "parent": "ep-germany",
      "kind": "parish",
      "rank": "Parish",
      "name": "Greek Orthodox Church of Saint Panteleimon in Augsburg",
      "local": "Kirche des heiligen Panteleimon",
      "country": "DE",
      "sources": [
        "https://www.orthodoxie.net/kirchengemeinden"
      ],
      "address": [
        "Max-von-Laue-Str. 15, 86156 Augsburg"
      ],
      "services": [
        "Göttliche Liturgie: sonntags, 8.30-10.30 Uhr"
      ]
    },
    {
      "id": "de-ep-kirchengemeinde-heiliger-panteleimon-augsburg-ulm-pauluskirche-frauenstr-110-89073-ulm",
      "parent": "ep-germany",
      "kind": "parish",
      "rank": "Worship site",
      "name": "Greek Orthodox Ulm: Paul's Church",
      "local": "Ulm: Pauluskirche",
      "country": "DE",
      "sources": [
        "https://www.orthodoxie.net/kirchengemeinden"
      ],
      "address": [
        "Frauenstr. 110, 89073 Ulm"
      ],
      "services": [
        "Göttliche Liturgie: jeden ersten Sonntag im Monat, 12.00-13.30 Uhr"
      ]
    },
    {
      "id": "de-ep-kirchengemeinde-heiliger-panteleimon-augsburg-giengen-brenz-spitalkirche-spitalstr-10-89",
      "parent": "ep-germany",
      "kind": "parish",
      "rank": "Worship site",
      "name": "Greek Orthodox Giengen/Brenz: Hospital church",
      "local": "Giengen/Brenz: Spitalkirche",
      "country": "DE",
      "sources": [
        "https://www.orthodoxie.net/kirchengemeinden"
      ],
      "address": [
        "Spitalstr. 10, 89537 Giengen/ Brenz"
      ],
      "services": [
        "Göttliche Liturgie: jeden zweiten und vierten Sonntag im Monat, 12.00-13.30 Uhr"
      ]
    },
    {
      "id": "de-ep-kirchengemeinde-heiliger-panteleimon-augsburg-ehingen-donau-ev-stadtkirche-lindenstr-25",
      "parent": "ep-germany",
      "kind": "parish",
      "rank": "Worship site",
      "name": "Greek Orthodox Ehingen/Donau: Ev. City church",
      "local": "Ehingen/Donau: Ev. Stadtkirche",
      "country": "DE",
      "sources": [
        "https://www.orthodoxie.net/kirchengemeinden"
      ],
      "address": [
        "Lindenstr. 25, 89584 Ehingen/Donau"
      ],
      "services": [
        "Göttliche Liturgie: jeden dritten Sonntag im Monat, 12.00-13.30 Uhr"
      ]
    },
    {
      "id": "de-ep-kirchengemeinde-heiliger-apostel-paulus-nurnberg-kirche-des-heiligen-apostels-paulus-obe",
      "parent": "ep-germany",
      "kind": "parish",
      "rank": "Parish",
      "name": "Greek Orthodox Church of the Holy Apostle Paul in Nürnberg",
      "local": "Kirche des heiligen Apostels Paulus",
      "country": "DE",
      "sources": [
        "https://www.orthodoxie.net/kirchengemeinden"
      ],
      "address": [
        "Obere Kanalstr. 35, 90429 Nürnberg"
      ],
      "services": [
        "Göttliche Liturgie: sonntags, 8.00-11.00 Uhr (Sommerzeit) oder 8.30-11.30 Uhr (Winterzeit)"
      ]
    },
    {
      "id": "de-ep-kirchengemeinde-maria-entschlafung-lauf-kirche-der-entschlafung-maria-in-der-salvatorkir",
      "parent": "ep-germany",
      "kind": "parish",
      "rank": "Parish",
      "name": "Greek Orthodox Church of the Dormition of the Virgin Mary in Lauf",
      "local": "Kirche der Entschlafung Mariä",
      "country": "DE",
      "sources": [
        "https://www.orthodoxie.net/kirchengemeinden"
      ],
      "address": [
        "in der Salvatorkirche, Kapellenhof 3, 91207 Lauf a.d. P."
      ],
      "services": [
        "Göttliche Liturgie: sonntags, 8.00-10.00 Uhr"
      ]
    },
    {
      "id": "de-ep-kirchengemeinde-maria-entschlafung-lauf-furth-kirche-der-heiligen-paraskevi-in-st-konrad",
      "parent": "ep-germany",
      "kind": "parish",
      "rank": "Worship site",
      "name": "Greek Orthodox Fürth: Church of Saint Paraskevi",
      "local": "Fürth: Kirche der heiligen Paraskevi",
      "country": "DE",
      "sources": [
        "https://www.orthodoxie.net/kirchengemeinden"
      ],
      "address": [
        "in St. Konrad, Schnieglinger Str. 292, 90427 Nürnberg"
      ],
      "services": [
        "Göttliche Liturgie: sonntags, 11.00-12.30 Uhr"
      ]
    },
    {
      "id": "de-ep-kirchengemeinde-maria-entschlafung-lauf-erlangen-christophoruskapelle-sieboldstr-3-91052",
      "parent": "ep-germany",
      "kind": "parish",
      "rank": "Worship site",
      "name": "Greek Orthodox Erlangen: St. Christopher's Chapel",
      "local": "Erlangen: Christophoruskapelle",
      "country": "DE",
      "sources": [
        "https://www.orthodoxie.net/kirchengemeinden"
      ],
      "address": [
        "Sieboldstr. 3, 91052 Erlangen"
      ],
      "services": [
        "Göttliche Liturgie: sonntags, 8.00-10.00 Uhr"
      ]
    },
    {
      "id": "de-ep-kirchengemeinde-maria-entschlafung-lauf-schwabach-dreieinigkeitkirche-bahnhofstr-1-91126",
      "parent": "ep-germany",
      "kind": "parish",
      "rank": "Worship site",
      "name": "Greek Orthodox Schwabach: Trinity Church",
      "local": "Schwabach: Dreieinigkeitkirche",
      "country": "DE",
      "sources": [
        "https://www.orthodoxie.net/kirchengemeinden"
      ],
      "address": [
        "Bahnhofstr. 1, 91126 Schwabach"
      ],
      "services": [
        "Göttliche Liturgie: samstags, 9.00-10.00 Uhr"
      ]
    },
    {
      "id": "de-ep-kirchengemeinde-maria-entschlafung-lauf-bamberg-st-otto-siechenstr-61-96052-bamberg",
      "parent": "ep-germany",
      "kind": "parish",
      "rank": "Worship site",
      "name": "Greek Orthodox Bamberg: St. Otto",
      "local": "Bamberg: St. Otto",
      "country": "DE",
      "sources": [
        "https://www.orthodoxie.net/kirchengemeinden"
      ],
      "address": [
        "Siechenstr. 61, 96052 Bamberg"
      ]
    },
    {
      "id": "de-ep-kirchengemeinde-maria-entschlafung-lauf-bayreuth-nikolaikirche-erlanger-str-29-95444-bay",
      "parent": "ep-germany",
      "kind": "parish",
      "rank": "Worship site",
      "name": "Greek Orthodox Bayreuth: St. Nicholas Church",
      "local": "Bayreuth: Nikolaikirche",
      "country": "DE",
      "sources": [
        "https://www.orthodoxie.net/kirchengemeinden"
      ],
      "address": [
        "Erlanger Str. 29, 95444 Bayreuth"
      ]
    },
    {
      "id": "de-ep-kirchengemeinde-maria-entschlafung-lauf-hof-st-marien-bernhard-lichtenberg-platz-1-95028",
      "parent": "ep-germany",
      "kind": "parish",
      "rank": "Worship site",
      "name": "Greek Orthodox Court: St. Marien in Hof",
      "local": "Hof: St. Marien",
      "country": "DE",
      "sources": [
        "https://www.orthodoxie.net/kirchengemeinden"
      ],
      "address": [
        "Bernhard-Lichtenberg-Platz 1, 95028 Hof"
      ]
    },
    {
      "id": "de-ep-kirchengemeinde-heilige-drei-hierarchen-wurzburg-kirche-der-drei-hierarchen-wurzburg-mar",
      "parent": "ep-germany",
      "kind": "parish",
      "rank": "Parish",
      "name": "Greek Orthodox Church of the Three Hierarchs Würzburg",
      "local": "Kirche der Drei Hierarchen Würzburg",
      "country": "DE",
      "sources": [
        "https://www.orthodoxie.net/kirchengemeinden"
      ],
      "address": [
        "Martinstr. 13, 97070 Würzburg"
      ],
      "services": [
        "Göttliche Liturgie: jeden zweiten und vierten Samstag im Monat, 8.30-10.30 Uhr"
      ]
    },
    {
      "id": "de-ep-kirchengemeinde-heilige-drei-hierarchen-wurzburg-aschaffenburg-kirche-der-heiligen-ekate",
      "parent": "ep-germany",
      "kind": "parish",
      "rank": "Worship site",
      "name": "Greek Orthodox Aschaffenburg: Church of Saint Ekaterina",
      "local": "Aschaffenburg: Kirche der heiligen Ekaterina",
      "country": "DE",
      "sources": [
        "https://www.orthodoxie.net/kirchengemeinden"
      ],
      "address": [
        "Löherstr. 51 (neben dem Hotel Wilder Μann) , 63739 Aschaffenburg"
      ],
      "services": [
        "Göttliche Liturgie: jeden ersten Sonntag im Monat, 8.30-10.45 Uhr"
      ]
    },
    {
      "id": "de-ep-kirchengemeinde-heilige-drei-hierarchen-wurzburg-schweinfurt-kirche-des-heiligen-antoniu",
      "parent": "ep-germany",
      "kind": "parish",
      "rank": "Worship site",
      "name": "Greek Orthodox Schweinfurt: Church of St. Anthony the Great",
      "local": "Schweinfurt: Kirche des heiligen Antonius des Großen",
      "country": "DE",
      "sources": [
        "https://www.orthodoxie.net/kirchengemeinden"
      ],
      "address": [
        "Deutschhöferstr. 13, 97422 Schweinfurt"
      ],
      "services": [
        "Göttliche Liturgie: jeden dritten Sonntag im Monat, 8.30-10.45 Uhr"
      ]
    },
    {
      "id": "de-ep-kirchengemeinde-heilige-drei-hierarchen-wurzburg-kunzelsau-kirche-der-heiligen-konstanti",
      "parent": "ep-germany",
      "kind": "parish",
      "rank": "Worship site",
      "name": "Greek Orthodox Künzelsau: Church of Saints Constantine and Helena",
      "local": "Künzelsau: Kirche der heiligen Konstantin und Helena",
      "country": "DE",
      "sources": [
        "https://www.orthodoxie.net/kirchengemeinden"
      ],
      "address": [
        "Stuttgarter Str. 34, 74653 Künzelsau"
      ],
      "services": [
        "Göttliche Liturgie: jeden zweiten und vierten Sonntag im Monat, 8.30-11.00 Uhr"
      ]
    },
    {
      "id": "de-ep-kirchengemeinde-heilige-drei-hierarchen-wurzburg-fulda-severikirche-in-der-kapelle-sever",
      "parent": "ep-germany",
      "kind": "parish",
      "rank": "Worship site",
      "name": "Greek Orthodox Fulda: Severikirche (in the chapel)",
      "local": "Fulda: Severikirche (in der Kapelle)",
      "country": "DE",
      "sources": [
        "https://www.orthodoxie.net/kirchengemeinden"
      ],
      "address": [
        "Severiberg 3, 36037 Fulda"
      ],
      "services": [
        "Göttliche Liturgie: jeden ersten Samstag im Monat, 9.30-11.00 Uhr"
      ]
    },
    {
      "id": "de-ep-kirchengemeinde-heilige-apostel-petrus-und-paulus-stuttgart-kirche-der-heiligen-apostel",
      "parent": "ep-germany",
      "kind": "parish",
      "rank": "Parish",
      "name": "Greek Orthodox Church of the Holy Apostles Peter and Paul in Stuttgart",
      "local": "Kirche der heiligen Apostel Petrus und Paulus",
      "country": "DE",
      "sources": [
        "https://www.orthodoxie.net/kirchengemeinden"
      ],
      "address": [
        "Weilimdorfer Str. 213, 70469 Stuttgart-Feuerbach"
      ],
      "services": [
        "Göttliche Liturgie: sonntags, 8.30-11.30 Uhr"
      ]
    },
    {
      "id": "de-ep-kirchengemeinde-heilige-apostel-petrus-und-paulus-stuttgart-leonberg-kirche-der-heiligen",
      "parent": "ep-germany",
      "kind": "parish",
      "rank": "Worship site",
      "name": "Greek Orthodox Leonberg: Church of Saints Constantine and Helena",
      "local": "Leonberg: Kirche der heiligen Konstantin und Helena",
      "country": "DE",
      "sources": [
        "https://www.orthodoxie.net/kirchengemeinden"
      ],
      "address": [
        "in der Blosenbergkirche, Schleiermacherstr. 41, 71229 Leonberg"
      ],
      "services": [
        "Göttliche Liturgie: sonntags, 12.30 Uhr"
      ]
    },
    {
      "id": "de-ep-kirchengemeinde-heilige-apostel-petrus-und-paulus-stuttgart-weil-der-stadt-kirche-des-he",
      "parent": "ep-germany",
      "kind": "parish",
      "rank": "Worship site",
      "name": "Greek Orthodox Because of the city: Church of St. George in Weil der Stadt",
      "local": "Weil der Stadt: Kirche des heiligen Georg",
      "country": "DE",
      "sources": [
        "https://www.orthodoxie.net/kirchengemeinden"
      ],
      "address": [
        "in der Spitalkapelle, Stuttgarter Str. 51, 71263 Weil der Stadt"
      ],
      "services": [
        "Göttliche Liturgie: jeden ersten und dritten Sonntag im Monat, 9.00-11.30 Uhr"
      ]
    },
    {
      "id": "de-ep-kirchengemeinde-heilige-apostel-petrus-und-paulus-stuttgart-kornwestheim-kirche-der-heil",
      "parent": "ep-germany",
      "kind": "parish",
      "rank": "Worship site",
      "name": "Greek Orthodox Kornwestheim: Church of Saints Rafael, Nikolaos and Irini",
      "local": "Kornwestheim: Kirche der heiligen Rafael, Nikolaos und Irini",
      "country": "DE",
      "sources": [
        "https://www.orthodoxie.net/kirchengemeinden"
      ],
      "address": [
        "in der Martinskirche, Kirchstr. 15, 70806 Kornwestheim"
      ],
      "services": [
        "Göttliche Liturgie: jeden zweiten und vierten Sonntag im Monat, 12.00 Uhr"
      ]
    },
    {
      "id": "de-ep-kirchengemeinde-christi-himmelfahrt-stuttgart-kirche-der-himmelfahrt-christi-rotenwaldst",
      "parent": "ep-germany",
      "kind": "parish",
      "rank": "Parish",
      "name": "Greek Orthodox Church of the Ascension of Christ in Stuttgart",
      "local": "Kirche der Himmelfahrt Christi",
      "country": "DE",
      "sources": [
        "https://www.orthodoxie.net/kirchengemeinden"
      ],
      "address": [
        "Rotenwaldstr. 30 (Leipziger Platz), 70197 Stuttgart"
      ],
      "services": [
        "Göttliche Liturgie: sonntags, 8.30-11.30 Uhr"
      ]
    },
    {
      "id": "de-ep-kirchengemeinde-heiliger-prophet-elias-stuttgart-rumanischsprachig-kirche-des-heiligen-p",
      "parent": "ep-germany",
      "kind": "parish",
      "rank": "Parish",
      "name": "Greek Orthodox Church of the Holy Prophet Elijah in Stuttgart (Romanian-speaking)",
      "local": "Kirche des heiligen Propheten Elias",
      "country": "DE",
      "sources": [
        "https://www.orthodoxie.net/kirchengemeinden"
      ],
      "address": [
        "in der Leonhardkirche, Leonhardplatz 26, 70182 Stuttgart"
      ],
      "services": [
        "Göttliche Liturgie: jeden dritten Sonntag im Monat, 12.00 Uhr"
      ]
    },
    {
      "id": "de-ep-kirchengemeinde-maria-verkundigung-esslingen-kirche-der-verkundigung-maria-dammstr-1-1-7",
      "parent": "ep-germany",
      "kind": "parish",
      "rank": "Parish",
      "name": "Greek Orthodox Church of the Annunciation of Mary in Esslingen",
      "local": "Kirche der Verkündigung Mariä",
      "country": "DE",
      "sources": [
        "https://www.orthodoxie.net/kirchengemeinden"
      ],
      "address": [
        "Dammstr. 1/1, 73728 Esslingen"
      ],
      "services": [
        "Göttliche Liturgie: sonntags, 8.00-11.30 Uhr"
      ]
    },
    {
      "id": "de-ep-kirchengemeinde-maria-verkundigung-esslingen-filderstadt-kirche-der-heiligen-konstantin",
      "parent": "ep-germany",
      "kind": "parish",
      "rank": "Worship site",
      "name": "Greek Orthodox Filderstadt: Church of Saints Constantine and Helena",
      "local": "Filderstadt: Kirche der heiligen Konstantin und Helena",
      "country": "DE",
      "sources": [
        "https://www.orthodoxie.net/kirchengemeinden"
      ],
      "address": [
        "in St. Stephanos, Eugenstr. 19, 70794 Filderstadt"
      ],
      "services": [
        "Göttliche Liturgie: jeden ersten, zweiten und dritten Sonntag im Monat, 12.30-14.00 Uhr"
      ]
    },
    {
      "id": "de-ep-kirchengemeinde-heiliger-athanasios-bietigheim-bissingen-kirche-des-heiligen-athanasios",
      "parent": "ep-germany",
      "kind": "parish",
      "rank": "Parish",
      "name": "Greek Orthodox Church of Saint Athanasius in Bietigheim-Bissingen",
      "local": "Kirche des heiligen Athanasios",
      "country": "DE",
      "sources": [
        "https://www.orthodoxie.net/kirchengemeinden"
      ],
      "address": [
        "Talstr. 15, 74321 Bietigheim-Bissingen"
      ],
      "services": [
        "Göttliche Liturgie: sonntags, 9.30 Uhr"
      ]
    },
    {
      "id": "de-ep-kirchengemeinde-heilige-kyrillos-und-methodios-kirchheim-u-teck-kirche-der-heiligen-kyri",
      "parent": "ep-germany",
      "kind": "parish",
      "rank": "Parish",
      "name": "Greek Orthodox Church of Saints Kyrillos and Methodius in Teck",
      "local": "Kirche der heiligen Kyrillos und Methodios",
      "country": "DE",
      "sources": [
        "https://www.orthodoxie.net/kirchengemeinden"
      ],
      "address": [
        "Limburgstr. 65, 73230 Kirchheim u. Teck"
      ],
      "services": [
        "Göttliche Liturgie: sonntags, 8.30-11.00 Uhr"
      ]
    },
    {
      "id": "de-ep-kirchengemeinde-heilige-kyrillos-und-methodios-kirchheim-u-teck-goppingen-kirche-der-hei",
      "parent": "ep-germany",
      "kind": "parish",
      "rank": "Worship site",
      "name": "Greek Orthodox Göppingen: Church of Saint Barbara",
      "local": "Göppingen: Kirche der heiligen Barbara",
      "country": "DE",
      "sources": [
        "https://www.orthodoxie.net/kirchengemeinden"
      ],
      "address": [
        "Reuschstr. 27, 73033 Göppingen"
      ],
      "services": [
        "Göttliche Liturgie: jeden zweiten und vierten Sonntag im Monat, 12.30-13.40 Uhr"
      ]
    },
    {
      "id": "de-ep-kirchengemeinde-maria-entschlafung-reutlingen-kirche-der-entschlafung-maria-des-heiligen",
      "parent": "ep-germany",
      "kind": "parish",
      "rank": "Parish",
      "name": "Greek Orthodox Church of the Dormition of St. John the Forerunner in Reutlingen",
      "local": "Kirche der Entschlafung Mariä- des heiligen Johannes des Vorläufers",
      "country": "DE",
      "sources": [
        "https://www.orthodoxie.net/kirchengemeinden"
      ],
      "address": [
        "Am Heilbrunnen 148, 72766 Reutlingen"
      ],
      "services": [
        "Göttliche Liturgie: sonntags, 8.30-11.00 Uhr"
      ]
    },
    {
      "id": "de-ep-kirchengemeinde-maria-entschlafung-reutlingen-schwenningen-johanneskirche-mozartstr-42-7",
      "parent": "ep-germany",
      "kind": "parish",
      "rank": "Worship site",
      "name": "Greek Orthodox Schwenningen: St. John's Church",
      "local": "Schwenningen: Johanneskirche",
      "country": "DE",
      "sources": [
        "https://www.orthodoxie.net/kirchengemeinden"
      ],
      "address": [
        "Mozartstr. 42, 78054 Villingen-Schwenningen"
      ],
      "services": [
        "Göttliche Liturgie: jeden ersten Sonntag im Monat, 13.00-14.15 Uhr"
      ]
    },
    {
      "id": "de-ep-kirchengemeinde-maria-verkundigung-lorrach-rumanischsprachig-kirche-der-verkundigung-in",
      "parent": "ep-germany",
      "kind": "parish",
      "rank": "Parish",
      "name": "Greek Orthodox Church of the Annunciation in Lörrach (Romanian-speaking)",
      "local": "Kirche der Verkündigung",
      "country": "DE",
      "sources": [
        "https://www.orthodoxie.net/kirchengemeinden"
      ],
      "address": [
        "in der evangelischen Kirche, Rötteln 7, 79539 Lörrach-Rötteln"
      ],
      "services": [
        "Göttliche Liturgie: jeden ersten Sonntag im Monat, 15.00 Uhr"
      ]
    },
    {
      "id": "de-ep-kirchengemeinde-heiliger-johannes-der-theologe-freiburg-kirche-des-heiligen-johannes-des",
      "parent": "ep-germany",
      "kind": "parish",
      "rank": "Parish",
      "name": "Greek Orthodox Church of Saint John the Theologian in Freiburg",
      "local": "Kirche des heiligen Johannes des Theologen",
      "country": "DE",
      "sources": [
        "https://www.orthodoxie.net/kirchengemeinden"
      ],
      "address": [
        "in der Maria Schutz Kirche, Schützenallee 16, 79102 Freiburg i.B."
      ],
      "services": [
        "Göttliche Liturgie: jeden Sonntag, 8.00-9.30 Uhr"
      ]
    },
    {
      "id": "de-ep-kirchengemeinde-heiliger-johannes-der-theologe-freiburg-buhlertal-kirche-der-heiligen-ir",
      "parent": "ep-germany",
      "kind": "parish",
      "rank": "Worship site",
      "name": "Greek Orthodox Bühlertal: Church of Saint Irini",
      "local": "Bühlertal: Kirche der heiligen Irini",
      "country": "DE",
      "sources": [
        "https://www.orthodoxie.net/kirchengemeinden"
      ],
      "address": [
        "in der Kapelle gegenüber dem Rathaus, Laubenstr. 9, 77830 Bühlertal-Obertal"
      ],
      "services": [
        "Göttliche Liturgie: jeden ersten und dritten Sonntag im Monat, 8.30-10.00, und jeden Mittwoch, 18.00 Uhr"
      ]
    },
    {
      "id": "de-ep-kirchengemeinde-heiliger-johannes-der-theologe-freiburg-karlsruhe-kirche-der-heiligen-fo",
      "parent": "ep-germany",
      "kind": "parish",
      "rank": "Worship site",
      "name": "Greek Orthodox Karlsruhe: Church of Saint Foteini the Samaritan",
      "local": "Karlsruhe: Kirche der heiligen Foteini der Samariterin",
      "country": "DE",
      "sources": [
        "https://www.orthodoxie.net/kirchengemeinden"
      ],
      "address": [
        "in der Kirche Bruder Klaus, Waldeckstr. 9, 76139 Karlsruhe"
      ],
      "services": [
        "Göttliche Liturgie: sonntags, 11.30-13.30 Uhr"
      ]
    },
    {
      "id": "de-ep-kirchengemeinde-heiliger-johannes-der-theologe-freiburg-bruchsal-kirche-des-heiligen-ant",
      "parent": "ep-germany",
      "kind": "parish",
      "rank": "Worship site",
      "name": "Greek Orthodox Bruchsal: Church of Saint Antonio",
      "local": "Bruchsal: Kirche des heiligen Antonios",
      "country": "DE",
      "sources": [
        "https://www.orthodoxie.net/kirchengemeinden"
      ],
      "address": [
        "in St. Anton, Paul-Gerhard-Str. Ecke Fritz-Erler-Str., 76646 Bruchsal"
      ],
      "services": [
        "Göttliche Liturgie: jeden ersten Samstag und jeden zweiten und vierten Sonntag im Monat, 9.00 Uhr"
      ]
    },
    {
      "id": "de-ep-kirchengemeinde-geburt-der-mutter-des-herrn-freiburg-rumanischsprachig-kirche-der-geburt",
      "parent": "ep-germany",
      "kind": "parish",
      "rank": "Parish",
      "name": "Greek Orthodox Church of the Nativity of the Mother of the Lord in Freiburg (Romanian-speaking)",
      "local": "Kirche der Geburt der Mutter des Herrn",
      "country": "DE",
      "sources": [
        "https://www.orthodoxie.net/kirchengemeinden"
      ],
      "address": [
        "Schützenallee 16, 79102 Freiburg"
      ],
      "services": [
        "Göttliche Liturgie: jeden ersten, dritten, vierten und fünften Sonntag im Monat, 10.30 Uhr"
      ]
    },
    {
      "id": "de-ep-kirchengemeinde-auferstehung-des-herrn-sindelfingen-kirche-der-auferstehung-des-herrn-wo",
      "parent": "ep-germany",
      "kind": "parish",
      "rank": "Parish",
      "name": "Greek Orthodox Church of the Resurrection of the Lord in Sindelfingen",
      "local": "Kirche der Auferstehung des Herrn",
      "country": "DE",
      "sources": [
        "https://www.orthodoxie.net/kirchengemeinden"
      ],
      "address": [
        "Wolboldstr. 12, 71063 Sindelfingen"
      ],
      "services": [
        "Göttliche Liturgie: sonntags, 8.00-11.00 Uhr"
      ]
    },
    {
      "id": "de-ep-kirchengemeinde-auferstehung-des-herrn-sindelfingen-herrenberg-kirche-der-heiligen-dreie",
      "parent": "ep-germany",
      "kind": "parish",
      "rank": "Worship site",
      "name": "Greek Orthodox Herrenberg: Church of the Holy Trinity",
      "local": "Herrenberg: Kirche der Heiligen Dreieinigkeit",
      "country": "DE",
      "sources": [
        "https://www.orthodoxie.net/kirchengemeinden"
      ],
      "address": [
        "in St. Josef, Walter-Knoll-Str. 13, 71083 Herrenberg"
      ],
      "services": [
        "Göttliche Liturgie: sonntags, 12.30-14.00 Uhr"
      ]
    },
    {
      "id": "de-ep-kirchengemeinde-heiliger-johannes-der-taufer-pforzheim-rumanischsprachig-kirche-des-heil",
      "parent": "ep-germany",
      "kind": "parish",
      "rank": "Parish",
      "name": "Greek Orthodox Church of St. John the Baptist in Pforzheim (Romanian-speaking)",
      "local": "Kirche des heiligen Johannes des Täufers",
      "country": "DE",
      "sources": [
        "https://www.orthodoxie.net/kirchengemeinden"
      ],
      "address": [
        "in der Johanneskirche, Mathystr. 7, 75173 Pforzheim"
      ],
      "services": [
        "Göttliche Liturgie: jeden zweiten Sonntag im Monat, 12.00 Uhr"
      ]
    },
    {
      "id": "de-ep-kirchengemeinde-heiliger-jakobus-der-herrenbruder-muhlacker-kirche-des-heiligen-jakobus",
      "parent": "ep-germany",
      "kind": "parish",
      "rank": "Parish",
      "name": "Greek Orthodox Church of St. James the Lord's Brother in Mühlacker",
      "local": "Kirche des heiligen Jakobus des Herrenbruders",
      "country": "DE",
      "sources": [
        "https://www.orthodoxie.net/kirchengemeinden"
      ],
      "address": [
        "Bahnhofstr. 117, 75417 Mühlacker"
      ],
      "services": [
        "Göttliche Liturgie: sonntags, 8.00 Uhr"
      ]
    },
    {
      "id": "de-ep-kirchengemeinde-heiliger-jakobus-der-herrenbruder-muhlacker-heilbronn-kirche-der-heilige",
      "parent": "ep-germany",
      "kind": "parish",
      "rank": "Worship site",
      "name": "Greek Orthodox Heilbronn: Church of Saints Constantine and Helena",
      "local": "Heilbronn: Kirche der heiligen Konstantin und Helena",
      "country": "DE",
      "sources": [
        "https://www.orthodoxie.net/kirchengemeinden"
      ],
      "address": [
        "Goppeltstr. 5, 74076 Heilbronn"
      ],
      "services": [
        "Göttliche Liturgie: sonntags, 12.00 Uhr"
      ]
    },
    {
      "id": "de-ep-kirchengemeinde-heiliger-johannes-der-taufer-heilbronn-rumanischsprachig-kirche-des-heil",
      "parent": "ep-germany",
      "kind": "parish",
      "rank": "Parish",
      "name": "Greek Orthodox Church of St. John the Baptist in Heilbronn (Romanian-speaking)",
      "local": "Kirche des heiligen Johannes des Täufers",
      "country": "DE",
      "sources": [
        "https://www.orthodoxie.net/kirchengemeinden"
      ],
      "address": [
        "in der Augustinuskirche, Goethestr. 75, 74076 Heilbronn"
      ],
      "services": [
        "Göttliche Liturgie: jeden ersten Sonntag im Monat, 12.30 Uhr"
      ]
    },
    {
      "id": "de-ep-kirchengemeinde-heiliger-basilius-der-grosse-backnang-kirche-des-heiligen-basilius-des-g",
      "parent": "ep-germany",
      "kind": "parish",
      "rank": "Parish",
      "name": "Greek Orthodox Church of St. Basil the Great in Backnang",
      "local": "Kirche des heiligen Basilius des Großen",
      "country": "DE",
      "sources": [
        "https://www.orthodoxie.net/kirchengemeinden"
      ],
      "address": [
        "Im Seefeld 4, 71522 Backnang"
      ],
      "services": [
        "Göttliche Liturgie: sonntags, 8.30 Uhr"
      ]
    },
    {
      "id": "de-ep-kirchengemeinde-heilige-konstantin-und-helena-waiblingen-kirche-der-heiligen-konstantin",
      "parent": "ep-germany",
      "kind": "parish",
      "rank": "Parish",
      "name": "Greek Orthodox Church of Saints Constantine and Helena in Waiblingen",
      "local": "Kirche der heiligen Konstantin und Helena",
      "country": "DE",
      "sources": [
        "https://www.orthodoxie.net/kirchengemeinden"
      ],
      "address": [
        "Kurze Str. 39, 71332 Waiblingen"
      ],
      "services": [
        "Göttliche Liturgie: sonntags, 8.15 Uhr"
      ]
    },
    {
      "id": "de-ep-kirchengemeinde-heilige-konstantin-und-helena-waiblingen-schwabisch-gmund-st-michael-eut",
      "parent": "ep-germany",
      "kind": "parish",
      "rank": "Worship site",
      "name": "Greek Orthodox Schwäbisch Gmünd: St. Michael",
      "local": "Schwäbisch Gmünd: St. Michael",
      "country": "DE",
      "sources": [
        "https://www.orthodoxie.net/kirchengemeinden"
      ],
      "address": [
        "Eutighofer Str. 55, 73525 Schwäbisch Gmünd"
      ],
      "services": [
        "Göttliche Liturgie: jeden ersten Sonntag im Monat, 13.00-14.15 Uhr"
      ]
    },
    {
      "id": "de-ep-kirchengemeinde-heilige-konstantin-und-helena-waiblingen-schorndorf-stadtkirche-kirchpla",
      "parent": "ep-germany",
      "kind": "parish",
      "rank": "Worship site",
      "name": "Greek Orthodox Schorndorf: town church",
      "local": "Schorndorf: Stadtkirche",
      "country": "DE",
      "sources": [
        "https://www.orthodoxie.net/kirchengemeinden"
      ],
      "address": [
        "Kirchplatz, 73617 Schorndorf"
      ],
      "services": [
        "Göttliche Liturgie: jeden zweiten Sonntag im Monat, 13.00-14.15 Uhr"
      ]
    },
    {
      "id": "de-ep-kirchengemeinde-kreuzerhohung-mannheim-kreuzerhohungskirche-spiegelstr-4-68305-mannheim",
      "parent": "ep-germany",
      "kind": "parish",
      "rank": "Parish",
      "name": "Greek Orthodox Church of the Exaltation of the Cross in Mannheim",
      "local": "Kreuzerhöhungskirche",
      "country": "DE",
      "sources": [
        "https://www.orthodoxie.net/kirchengemeinden"
      ],
      "address": [
        "Spiegelstr. 4, 68305 Mannheim"
      ],
      "services": [
        "Göttliche Liturgie: sonntags, 9.00-12.00 Uhr"
      ]
    },
    {
      "id": "de-ep-kirchengemeinde-kreuzerhohung-mannheim-schwetzingen-st-maria-uhlandstr-8-68723-schwetzin",
      "parent": "ep-germany",
      "kind": "parish",
      "rank": "Worship site",
      "name": "Greek Orthodox Schwetzingen: St. Mary",
      "local": "Schwetzingen: St. Maria",
      "country": "DE",
      "sources": [
        "https://www.orthodoxie.net/kirchengemeinden"
      ],
      "address": [
        "Uhlandstr. 8, 68723 Schwetzingen"
      ],
      "services": [
        "Göttliche Liturgie: jeden dritten Sonntag im Monat, 15.00 Uhr"
      ]
    },
    {
      "id": "de-ep-kirchengemeinde-kreuzerhohung-mannheim-heidelberg-erloserkirche-plock-44-69117-heidelber",
      "parent": "ep-germany",
      "kind": "parish",
      "rank": "Worship site",
      "name": "Greek Orthodox Heidelberg: Church of the Redeemer",
      "local": "Heidelberg: Erlöserkirche",
      "country": "DE",
      "sources": [
        "https://www.orthodoxie.net/kirchengemeinden"
      ],
      "address": [
        "Plöck 44, 69117 Heidelberg"
      ],
      "services": [
        "Göttliche Liturgie: jeden zweiten Samstag im Monat, 10.00 Uhr"
      ]
    },
    {
      "id": "de-ep-kirchengemeinde-kreuzerhohung-mannheim-ladenburg-stadtkirche-kirchenstr-28-68526-ladenbu",
      "parent": "ep-germany",
      "kind": "parish",
      "rank": "Worship site",
      "name": "Greek Orthodox Ladenburg: town church",
      "local": "Ladenburg: Stadtkirche",
      "country": "DE",
      "sources": [
        "https://www.orthodoxie.net/kirchengemeinden"
      ],
      "address": [
        "Kirchenstr. 28, 68526 Ladenburg"
      ],
      "services": [
        "Göttliche Liturgie: jeden ersten Sonntag im Monat, 15.00 Uhr"
      ]
    },
    {
      "id": "de-ep-kirchengemeinde-auferstehung-des-herrn-saarbrucken-rumanischsprachig-kirche-der-auferste",
      "parent": "ep-germany",
      "kind": "parish",
      "rank": "Parish",
      "name": "Greek Orthodox Church of the Resurrection of the Lord in Saarbrücken (Romanian-speaking)",
      "local": "Kirche der Auferstehung des Herrn",
      "country": "DE",
      "sources": [
        "https://www.orthodoxie.net/kirchengemeinden"
      ],
      "address": [
        "in der Deutschherrenkapelle, Pfählerstr. 2, 66117 Saarbrücken"
      ],
      "services": [
        "Göttliche Liturgie: jeden zweiten, vierten und letzten Sonntag im Monat, 10.00 Uhr"
      ]
    },
    {
      "id": "de-ep-kirchengemeinde-maria-verkundigung-ludwigshafen-am-rhein-kirche-der-verkundigung-maria-h",
      "parent": "ep-germany",
      "kind": "parish",
      "rank": "Parish",
      "name": "Greek Orthodox Church of the Annunciation of Mary in Rhein",
      "local": "Kirche der Verkündigung Mariä",
      "country": "DE",
      "sources": [
        "https://www.orthodoxie.net/kirchengemeinden"
      ],
      "address": [
        "Hohenzollernstr. 2, 67063 Ludwigshafen a. R."
      ],
      "services": [
        "Göttliche Liturgie: sonntags, 8.30-11.15 Uhr"
      ]
    },
    {
      "id": "de-ep-kirchengemeinde-maria-verkundigung-ludwigshafen-am-rhein-worms-st-martin-martingasse-6-6",
      "parent": "ep-germany",
      "kind": "parish",
      "rank": "Worship site",
      "name": "Greek Orthodox Worms: St. Martin",
      "local": "Worms: St. Martin",
      "country": "DE",
      "sources": [
        "https://www.orthodoxie.net/kirchengemeinden"
      ],
      "address": [
        "Martingasse 6, 67547 Worms"
      ],
      "services": [
        "Göttliche Liturgie: jeden ersten Sonntag im Monat, 16.00 Uhr"
      ]
    },
    {
      "id": "de-ep-kirchengemeinde-maria-verkundigung-ludwigshafen-am-rhein-kaiserslautern-st-franziskus-ka",
      "parent": "ep-germany",
      "kind": "parish",
      "rank": "Worship site",
      "name": "Greek Orthodox Kaiserslautern: St. Francis",
      "local": "Kaiserslautern: St. Franziskus",
      "country": "DE",
      "sources": [
        "https://www.orthodoxie.net/kirchengemeinden"
      ],
      "address": [
        "Kantstr. 85, 67663 Kaiserslautern"
      ],
      "services": [
        "Göttliche Liturgie: jeden zweiten und vierten Samstag im Monat, 9.00 Uhr"
      ]
    },
    {
      "id": "de-ep-kirchengemeinde-heiliger-athanasios-trier-wird-von-der-kirchengemeinde-des-heiligen-unei",
      "parent": "ep-germany",
      "kind": "parish",
      "rank": "Parish",
      "name": "Greek Orthodox is cared for by the parish of the holy disinterested doctors of Luxembourg (Metropolitan of Belgium). in Trier",
      "local": "wird von der Kirchengemeinde des heiligen uneigennützigen Ärzte Luxemburg (Metropolie von Belgien) betreut",
      "country": "DE",
      "sources": [
        "https://www.orthodoxie.net/kirchengemeinden"
      ]
    },
    {
      "id": "de-ep-kirchengemeinde-heiliger-nikolaus-darmstadt-kirche-des-heiligen-nikolaus-heinrich-delp-s",
      "parent": "ep-germany",
      "kind": "parish",
      "rank": "Parish",
      "name": "Greek Orthodox Church of St. Nicholas in Darmstadt",
      "local": "Kirche des heiligen Nikolaus",
      "country": "DE",
      "sources": [
        "https://www.orthodoxie.net/kirchengemeinden"
      ],
      "address": [
        "Heinrich-Delp-Str. 235, 64297 Darmstadt"
      ],
      "services": [
        "Göttliche Liturgie: sonntags, 8.00-10.00 Uhr"
      ]
    },
    {
      "id": "de-ep-kirchengemeinde-heiliger-nikolaus-darmstadt-kelsterbach-kirche-der-heiligen-sofia-von-kl",
      "parent": "ep-germany",
      "kind": "parish",
      "rank": "Worship site",
      "name": "Greek Orthodox Kelsterbach: Church of Saint Sofia of Kleisoura",
      "local": "Kelsterbach: Kirche der heiligen Sofia von Kleisoura",
      "country": "DE",
      "sources": [
        "https://www.orthodoxie.net/kirchengemeinden"
      ],
      "address": [
        "Langer Kornweg 2, 65451 Kelsterbach"
      ],
      "services": [
        "Göttliche Liturgie: jeden ersten und dritten Sonntag im Monat, 12.00-13.30 Uhr"
      ]
    },
    {
      "id": "de-ep-kirchengemeinde-allerheiligen-offenbach-am-main-kirche-allerheiligen-gersprenzweg-42-630",
      "parent": "ep-germany",
      "kind": "parish",
      "rank": "Parish",
      "name": "Greek Orthodox Church of All Saints in Main",
      "local": "Kirche Allerheiligen",
      "country": "DE",
      "sources": [
        "https://www.orthodoxie.net/kirchengemeinden"
      ],
      "address": [
        "Gersprenzweg 42, 63071 Offenbach"
      ],
      "services": [
        "Göttliche Liturgie: sonntags, 8.30-11.30 Uhr"
      ]
    },
    {
      "id": "de-ep-kirchengemeinde-allerheiligen-offenbach-am-main-maintal-alte-evangelische-kirche-kirchga",
      "parent": "ep-germany",
      "kind": "parish",
      "rank": "Worship site",
      "name": "Greek Orthodox Maintal: Old Evangelical Church",
      "local": "Maintal: Alte Evangelische Kirche",
      "country": "DE",
      "sources": [
        "https://www.orthodoxie.net/kirchengemeinden"
      ],
      "address": [
        "Kirchgasse 6-8, 63477 Maintal-Dörnigheim"
      ],
      "services": [
        "Göttliche Liturgie: jeden zweiten und vierten Sonntag im Monat, 13.00-14.00 Uhr"
      ]
    },
    {
      "id": "de-ep-kirchengemeinde-heiliger-prophet-elias-frankfurt-am-main-kirche-des-propheten-elias-solm",
      "parent": "ep-germany",
      "kind": "parish",
      "rank": "Parish",
      "name": "Greek Orthodox Church of the Prophet Elijah in Main",
      "local": "Kirche des Propheten Elias",
      "country": "DE",
      "sources": [
        "https://www.orthodoxie.net/kirchengemeinden"
      ],
      "address": [
        "Solmsstr. 1, 60486 Frankfurt am Main"
      ],
      "services": [
        "Göttliche Liturgie: sonntags, 8.00 Uhr"
      ]
    },
    {
      "id": "de-ep-kirchengemeinde-heiliger-georgios-frankfurt-am-main-kirche-des-heiligen-georgios-sebasti",
      "parent": "ep-germany",
      "kind": "parish",
      "rank": "Parish",
      "name": "Greek Orthodox Church of Saint George in Main",
      "local": "Kirche des heiligen Georgios",
      "country": "DE",
      "sources": [
        "https://www.orthodoxie.net/kirchengemeinden"
      ],
      "address": [
        "Sebastian-Rinz-Str. 2a, 60323 Frankfurt am Main"
      ],
      "services": [
        "Göttliche Liturgie: sonntags, 8.30 Uhr"
      ]
    },
    {
      "id": "de-ep-kirchengemeinde-entschlafen-der-mutter-des-herrn-frankfurt-am-main-rumanischsprachig-kir",
      "parent": "ep-germany",
      "kind": "parish",
      "rank": "Parish",
      "name": "Greek Orthodox Church of the Dormition of the Mother of the Lord in Frankfurt am Main (Romanian-speaking)",
      "local": "Kirche des Entschlafens der Mutter des Herrn",
      "country": "DE",
      "sources": [
        "https://www.orthodoxie.net/kirchengemeinden"
      ],
      "address": [
        "in der Matthäuskirche, F.-Ebert-Anlage 33, 60327 Frankfurt am Main"
      ],
      "services": [
        "Göttliche Liturgie: jeden zweiten und vierten Sonntag im Monat, 12.15 Uhr"
      ]
    },
    {
      "id": "de-ep-kirchengemeinde-heiliger-georgios-wiesbaden-kirche-des-heiligen-georgios-rheingaustr-170",
      "parent": "ep-germany",
      "kind": "parish",
      "rank": "Parish",
      "name": "Greek Orthodox Church of Saint George in Wiesbaden",
      "local": "Kirche des heiligen Georgios",
      "country": "DE",
      "sources": [
        "https://www.orthodoxie.net/kirchengemeinden"
      ],
      "address": [
        "Rheingaustr. 170b, 65203 Wiesbaden"
      ],
      "services": [
        "Göttliche Liturgie: sonntags, 8.00-11.00 Uhr"
      ]
    },
    {
      "id": "de-ep-kirchengemeinde-kreuzerhohung-russelsheim-kirche-der-kreuzerhohung-russelsheim-godesberg",
      "parent": "ep-germany",
      "kind": "parish",
      "rank": "Parish",
      "name": "Greek Orthodox Church of the Exaltation of the Cross in Rüsselsheim",
      "local": "Kirche der Kreuzerhöhung Rüsselsheim",
      "country": "DE",
      "sources": [
        "https://www.orthodoxie.net/kirchengemeinden"
      ],
      "address": [
        "Godesberger Str. 32, 65428 Rüsselsheim am Main"
      ],
      "services": [
        "Göttliche Liturgie: sonntags, 9.00-12.00 Uhr"
      ]
    },
    {
      "id": "de-ep-kirchengemeinde-kreuzerhohung-russelsheim-walldorf-kirche-des-heiligen-nikolaos-in-der-e",
      "parent": "ep-germany",
      "kind": "parish",
      "rank": "Worship site",
      "name": "Greek Orthodox Walldorf: Church of Saint Nikolaos",
      "local": "Walldorf: Kirche des heiligen Nikolaos",
      "country": "DE",
      "sources": [
        "https://www.orthodoxie.net/kirchengemeinden"
      ],
      "address": [
        "in der evangelischen Kirche, Ludwigstr. 64, 64546 Mörfelden-Walldorf"
      ],
      "services": [
        "Göttliche Liturgie: jeden vierten Sonntag im Monat, 12.30-13.30 Uhr"
      ]
    },
    {
      "id": "de-ep-kirchengemeinde-heilige-uneigennutzige-arzte-wetzlar-giessen-petruskirche-wartweg-9-3539",
      "parent": "ep-germany",
      "kind": "parish",
      "rank": "Parish",
      "name": "Greek Orthodox Giessen: St. Peter's Church in Wetzlar",
      "local": "Gießen: Petruskirche",
      "country": "DE",
      "sources": [
        "https://www.orthodoxie.net/kirchengemeinden"
      ],
      "address": [
        "Wartweg 9, 35392 Gießen"
      ],
      "services": [
        "Göttliche Liturgie: sonntags, 12.00 Uhr"
      ]
    }
  ],
  "an-germany": [
    {
      "id": "de-an-koblenz-gemeinde-st-katharina",
      "parent": "an-germany",
      "kind": "parish",
      "rank": "Parish",
      "name": "Antiochian Orthodox Parish of St. Catherine",
      "local": "Gemeinde St. Katharina",
      "country": "DE",
      "sources": [
        "https://rum-orthodox.de/gemeinden/koblenz/"
      ],
      "address": [
        "Finkenherd 8",
        "56075 Koblenz"
      ]
    },
    {
      "id": "de-an-hueckelhoven-gemeinde-prophet-elias",
      "parent": "an-germany",
      "kind": "parish",
      "rank": "Parish",
      "name": "Antiochian Orthodox Church of Prophet Elijah",
      "local": "Gemeinde Prophet Elias",
      "country": "DE",
      "sources": [
        "https://rum-orthodox.de/gemeinden/hueckelhoven/"
      ],
      "address": [
        "Dinstühlerstraße 53",
        "41836 Hückelhoven"
      ]
    },
    {
      "id": "de-an-duelmen-gemeinde-der-verklarung",
      "parent": "an-germany",
      "kind": "parish",
      "rank": "Parish",
      "name": "Antiochian Orthodox Church of the Transfiguration",
      "local": "Gemeinde der Verklärung",
      "country": "DE",
      "sources": [
        "https://rum-orthodox.de/gemeinden/duelmen/"
      ],
      "address": [
        "josef heiming straße 3",
        "48249 Dülmen"
      ]
    },
    {
      "id": "de-an-isaak-der-syrer-gemeinde-heiligen-isaak-der-syrer",
      "parent": "an-germany",
      "kind": "parish",
      "rank": "Parish",
      "name": "Antiochian Orthodox Parish of Saint Isaac the Syrian",
      "local": "Gemeinde Heiligen Isaak der Syrer",
      "country": "DE",
      "sources": [
        "https://rum-orthodox.de/gemeinden/isaak_der_syrer/"
      ],
      "address": [
        "Goerdelerstraße 31",
        "23566 Lübeck"
      ]
    },
    {
      "id": "de-an-kreuz-gemeinde-des-heiligen-kreuzes",
      "parent": "an-germany",
      "kind": "parish",
      "rank": "Parish",
      "name": "Antiochian Orthodox Parish of the Holy Cross",
      "local": "Gemeinde des Heiligen Kreuzes",
      "country": "DE",
      "sources": [
        "https://rum-orthodox.de/gemeinden/kreuz/"
      ],
      "address": [
        "Shanghaiallee 12-14",
        "20457 Hamburg"
      ]
    },
    {
      "id": "de-an-leipzig-gemeinde-theophanie",
      "parent": "an-germany",
      "kind": "parish",
      "rank": "Parish",
      "name": "Antiochian Orthodox Theophany community",
      "local": "Gemeinde Theophanie",
      "country": "DE",
      "sources": [
        "https://rum-orthodox.de/gemeinden/leipzig/"
      ],
      "address": [
        "Nonnenmühlgasse 2",
        "04107 Leipzig"
      ]
    },
    {
      "id": "de-an-dresden-gemeinde-st-michael",
      "parent": "an-germany",
      "kind": "parish",
      "rank": "Parish",
      "name": "Antiochian Orthodox Parish of St. Michael",
      "local": "Gemeinde St. Michael",
      "country": "DE",
      "sources": [
        "https://rum-orthodox.de/gemeinden/dresden/"
      ],
      "address": [
        "Stauffenbergallee 9 C",
        "01099 Dresden"
      ]
    },
    {
      "id": "de-an-paderborn-gemeinde-st-raphael",
      "parent": "an-germany",
      "kind": "parish",
      "rank": "Parish",
      "name": "Antiochian Orthodox Parish of St. Raphael",
      "local": "Gemeinde St. Raphael",
      "country": "DE",
      "sources": [
        "https://rum-orthodox.de/gemeinden/paderborn/"
      ],
      "address": [
        "Arndtstraße 33",
        "33100 Paderborn"
      ]
    },
    {
      "id": "de-an-essen-gemeinde-st-josef-von-damaskus",
      "parent": "an-germany",
      "kind": "parish",
      "rank": "Parish",
      "name": "Antiochian Orthodox St. Joseph of Damascus Parish",
      "local": "Gemeinde St. Josef von Damaskus",
      "country": "DE",
      "sources": [
        "https://rum-orthodox.de/gemeinden/essen/"
      ],
      "address": [
        "An St. Albertus Magnus 45",
        "45136 Essen"
      ]
    },
    {
      "id": "de-an-muenchen-gemeinde-st-paisios",
      "parent": "an-germany",
      "kind": "parish",
      "rank": "Parish",
      "name": "Antiochian Orthodox Parish of St. Paisios",
      "local": "Gemeinde St. Paisios",
      "country": "DE",
      "sources": [
        "https://rum-orthodox.de/gemeinden/muenchen/"
      ],
      "address": [
        "Ungererstraße 131",
        "80805 München"
      ]
    },
    {
      "id": "de-an-elsenfeld-gemeinde-st-paulus",
      "parent": "an-germany",
      "kind": "parish",
      "rank": "Parish",
      "name": "Antiochian Orthodox Parish of St. Paul",
      "local": "Gemeinde St. Paulus",
      "country": "DE",
      "sources": [
        "https://rum-orthodox.de/gemeinden/elsenfeld/"
      ],
      "address": [
        "Adam-Zirkel-Straße 4",
        "63820 Elsenfeld"
      ]
    },
    {
      "id": "de-an-wiesbaden-gemeinde-st-johannes-chrysostomos",
      "parent": "an-germany",
      "kind": "parish",
      "rank": "Parish",
      "name": "Antiochian Orthodox Parish of St. John Chrysostom",
      "local": "Gemeinde St. Johannes Chrysostomos",
      "country": "DE",
      "sources": [
        "https://rum-orthodox.de/gemeinden/wiesbaden/"
      ],
      "address": [
        "Am Kupferberg 2",
        "65187 Wiesbaden-Bierbrich"
      ]
    },
    {
      "id": "de-an-walldorf-gemeinde-st-johannes-von-damaskus",
      "parent": "an-germany",
      "kind": "parish",
      "rank": "Parish",
      "name": "Antiochian Orthodox St. John of Damascus Parish",
      "local": "Gemeinde St. Johannes von Damaskus",
      "country": "DE",
      "sources": [
        "https://rum-orthodox.de/gemeinden/walldorf/"
      ],
      "address": [
        "Hauptstraße 1",
        "69190 Walldorf-Baden"
      ]
    },
    {
      "id": "de-an-schwenningen-gemeinde-st-georgios",
      "parent": "an-germany",
      "kind": "parish",
      "rank": "Parish",
      "name": "Antiochian Orthodox Parish of St. Georgios",
      "local": "Gemeinde St. Georgios",
      "country": "DE",
      "sources": [
        "https://rum-orthodox.de/gemeinden/schwenningen/"
      ],
      "address": [
        "Adolph-Kolping-Straße 8",
        "78054 Villingen-Schwenningen"
      ]
    },
    {
      "id": "de-an-stuttgart-gemeinde-st-johannes-der-taufer",
      "parent": "an-germany",
      "kind": "parish",
      "rank": "Parish",
      "name": "Antiochian Orthodox Parish of St. John the Baptist",
      "local": "Gemeinde St. Johannes der Täufer",
      "country": "DE",
      "sources": [
        "https://rum-orthodox.de/gemeinden/stuttgart/"
      ],
      "address": [
        "Daimlerstr. 2",
        "71263 Weil der Stadt"
      ]
    },
    {
      "id": "de-an-pforzheim-gemeinde-st-petrus-und-paulus",
      "parent": "an-germany",
      "kind": "parish",
      "rank": "Parish",
      "name": "Antiochian Orthodox Parish of St. Peter and Paul",
      "local": "Gemeinde St. Petrus und Paulus",
      "country": "DE",
      "sources": [
        "https://rum-orthodox.de/gemeinden/pforzheim/"
      ],
      "address": [
        "Julius-Heydegger-Straße 1",
        "75181 Pforzheim"
      ]
    },
    {
      "id": "de-an-osnabrueck-gemeinde-mutter-gottes-maria",
      "parent": "an-germany",
      "kind": "parish",
      "rank": "Parish",
      "name": "Antiochian Orthodox Parish Mother of God Mary",
      "local": "Gemeinde Mutter Gottes Maria",
      "country": "DE",
      "sources": [
        "https://rum-orthodox.de/gemeinden/osnabrueck/"
      ],
      "address": [
        "Lerchenstr. 131",
        "49088 Osnabrück"
      ]
    },
    {
      "id": "de-an-nuernberg-gemeinde-st-michael",
      "parent": "an-germany",
      "kind": "parish",
      "rank": "Parish",
      "name": "Antiochian Orthodox Parish of St. Michael",
      "local": "Gemeinde St. Michael",
      "country": "DE",
      "sources": [
        "https://rum-orthodox.de/gemeinden/nuernberg/"
      ],
      "address": [
        "Siemensstädter Str. 13",
        "90765 Fürth"
      ]
    },
    {
      "id": "de-an-muenster-gemeinde-mutter-gottes-maria",
      "parent": "an-germany",
      "kind": "parish",
      "rank": "Parish",
      "name": "Antiochian Orthodox Parish Mother of God Mary",
      "local": "Gemeinde Mutter Gottes Maria",
      "country": "DE",
      "sources": [
        "https://rum-orthodox.de/gemeinden/muenster/"
      ],
      "address": [
        "An der Alten Kirche 2",
        "48165 Münster"
      ]
    },
    {
      "id": "de-an-mannheim-gemeinde-st-petrus-und-paulus",
      "parent": "an-germany",
      "kind": "parish",
      "rank": "Parish",
      "name": "Antiochian Orthodox Parish of St. Peter and Paul",
      "local": "Gemeinde St. Petrus und Paulus",
      "country": "DE",
      "sources": [
        "https://rum-orthodox.de/gemeinden/mannheim/"
      ],
      "address": [
        "Kattowitzer Zeile 70",
        "68307 Mannheim"
      ]
    },
    {
      "id": "de-an-koeln-g-gemeinde-st-georgios",
      "parent": "an-germany",
      "kind": "parish",
      "rank": "Parish",
      "name": "Antiochian Orthodox Parish of St. Georgios",
      "local": "Gemeinde St. Georgios",
      "country": "DE",
      "sources": [
        "https://rum-orthodox.de/gemeinden/koeln-g/"
      ],
      "address": [
        "Pater-Adam-Müller-Platz 1",
        "50767 Köln"
      ]
    },
    {
      "id": "de-an-koeln-d-gemeinde-st-dimitrios",
      "parent": "an-germany",
      "kind": "parish",
      "rank": "Parish",
      "name": "Antiochian Orthodox Parish of St. Dimitrios",
      "local": "Gemeinde St. Dimitrios",
      "country": "DE",
      "sources": [
        "https://rum-orthodox.de/gemeinden/koeln-d/"
      ],
      "address": [
        "Geranien Weg 27-29",
        "50769 Köln"
      ]
    },
    {
      "id": "de-an-kassel-gemeinde-st-nikolaus",
      "parent": "an-germany",
      "kind": "parish",
      "rank": "Parish",
      "name": "Antiochian Orthodox Parish of St. Nicholas",
      "local": "Gemeinde St. Nikolaus",
      "country": "DE",
      "sources": [
        "https://rum-orthodox.de/gemeinden/kassel/"
      ],
      "address": [
        "Wolfhager Str. 268",
        "34128 Kassel"
      ]
    },
    {
      "id": "de-an-karlsruhe-gemeinde-st-petrus-und-paulus",
      "parent": "an-germany",
      "kind": "parish",
      "rank": "Parish",
      "name": "Antiochian Orthodox Parish of St. Peter and Paul",
      "local": "Gemeinde St. Petrus und Paulus",
      "country": "DE",
      "sources": [
        "https://rum-orthodox.de/gemeinden/karlsruhe/"
      ],
      "address": [
        "Philippsburger Str. 13",
        "76646 Bruchsal"
      ]
    },
    {
      "id": "de-an-hannover-gemeinde-erzengel-gabriel",
      "parent": "an-germany",
      "kind": "parish",
      "rank": "Parish",
      "name": "Antiochian Orthodox Parish of Archangel Gabriel",
      "local": "Gemeinde Erzengel Gabriel",
      "country": "DE",
      "sources": [
        "https://rum-orthodox.de/gemeinden/hannover/"
      ],
      "address": [
        "Mengendamm 16B",
        "30177 Hannover"
      ]
    },
    {
      "id": "de-an-hamburg-gemeinde-st-petrus",
      "parent": "an-germany",
      "kind": "parish",
      "rank": "Parish",
      "name": "Antiochian Orthodox Parish of St. Peter",
      "local": "Gemeinde St. Petrus",
      "country": "DE",
      "sources": [
        "https://rum-orthodox.de/gemeinden/hamburg/"
      ],
      "address": [
        "Kurzer Kamp 2",
        "25451 Quickborn"
      ]
    },
    {
      "id": "de-an-butzbach-gemeinde-st-petrus-und-paulus",
      "parent": "an-germany",
      "kind": "parish",
      "rank": "Parish",
      "name": "Antiochian Orthodox Parish of St. Peter and Paul",
      "local": "Gemeinde St. Petrus und Paulus",
      "country": "DE",
      "sources": [
        "https://rum-orthodox.de/gemeinden/butzbach/"
      ],
      "address": [
        "Himmrichsweg 10",
        "35510 Butzbach"
      ]
    },
    {
      "id": "de-an-berlin-gemeinde-st-georgios",
      "parent": "an-germany",
      "kind": "parish",
      "rank": "Parish",
      "name": "Antiochian Orthodox Parish of St. Georgios",
      "local": "Gemeinde St. Georgios",
      "country": "DE",
      "sources": [
        "https://rum-orthodox.de/gemeinden/berlin/"
      ],
      "address": [
        "Auguststr. 90",
        "10117 Berlin"
      ]
    },
    {
      "id": "de-an-achim-gemeinde-st-ignatius",
      "parent": "an-germany",
      "kind": "parish",
      "rank": "Parish",
      "name": "Antiochian Orthodox Parish of St. Ignatius",
      "local": "Gemeinde St. Ignatius",
      "country": "DE",
      "sources": [
        "https://rum-orthodox.de/gemeinden/achim/"
      ],
      "address": [
        "Magdeburger Str. 32",
        "28832 Achim"
      ]
    }
  ],
  "ru-berlin-and-germany": [
    {
      "id": "de-mp-aachen-gemeinde-zur-ehre-hl-tamara-zarin-von-georgien",
      "parent": "ru-berlin-and-germany",
      "kind": "parish",
      "rank": "Parish",
      "name": "Russian Orthodox Parish honoring St. Tamara, Tsarina of Georgia",
      "local": "Gemeinde zur Ehre Hl. Tamara, Zarin von Georgien",
      "country": "DE",
      "sources": [
        "https://rokmp.de/de/churches/prihod-tsaritsyi-gruzinskoy-tamaryi/"
      ],
      "address": [
        "Schützen Str. 13, 52062 Aachen"
      ]
    },
    {
      "id": "de-mp-aalen-gemeinde-der-darstellung-des-herrn",
      "parent": "ru-berlin-and-germany",
      "kind": "parish",
      "rank": "Parish",
      "name": "Russian Orthodox Church of the Presentation of the Lord",
      "local": "Gemeinde der Darstellung des Herrn",
      "country": "DE",
      "sources": [
        "https://rokmp.de/de/churches/prihod-sretenija-gospodnja/"
      ],
      "address": [
        "Langertstraße 116, 73431 Aalen, Германия"
      ]
    },
    {
      "id": "de-mp-altotting-gemeinde-zu-ehren-der-ikone-der-gottesmutter-wladimirskaja",
      "parent": "ru-berlin-and-germany",
      "kind": "parish",
      "rank": "Parish",
      "name": "Russian Orthodox Parish in honor of the icon of the Mother of God \"Vladimirskaya\"",
      "local": "Gemeinde zu Ehren der Ikone der Gottesmutter \"Wladimirskaja\"",
      "country": "DE",
      "sources": [
        "https://rokmp.de/de/churches/obshhina-pri-prihode-voskresenija-gospodnja-mjunhen/"
      ],
      "address": [
        "Ostpreußenstraße 2, 84503, Altötting, Deutschland"
      ]
    },
    {
      "id": "de-mp-bad-hersfeld-gemeinde-zu-ehren-des-hl-apostels-markus",
      "parent": "ru-berlin-and-germany",
      "kind": "parish",
      "rank": "Parish",
      "name": "Russian Orthodox Parish in honor of St. Mark the Apostle",
      "local": "Gemeinde zu Ehren des Hl. Apostels Markus",
      "country": "DE",
      "sources": [
        "https://rokmp.de/de/churches/prihod-sv-apostola-i-evangelista-marka/"
      ]
    },
    {
      "id": "de-mp-bad-kreuznach-gemeinde-des-hl-lebensspendenden-kreuzes",
      "parent": "ru-berlin-and-germany",
      "kind": "parish",
      "rank": "Parish",
      "name": "Russian Orthodox Parish of the Holy Life-Giving Cross",
      "local": "Gemeinde des Hl. Lebensspendenden Kreuzes",
      "country": "DE",
      "sources": [
        "https://rokmp.de/de/churches/prihod-sv-chestnogo-i-zhivotvoryashhego-kresta-gospodnya/"
      ],
      "address": [
        "Holbeinstraße 108, 55543, Bad Kreuznach, Deutschland"
      ]
    },
    {
      "id": "de-mp-bad-lippspringe-gemeinde-zu-ehren-der-hl-gottesmutter-ikone-feodorovskaya",
      "parent": "ru-berlin-and-germany",
      "kind": "parish",
      "rank": "Parish",
      "name": "Russian Orthodox Parish in honor of the Holy Mother of God Icon \"Feodorovskaya\"",
      "local": "Gemeinde zu Ehren der Hl. Gottesmutter-Ikone \"Feodorovskaya\"",
      "country": "DE",
      "sources": [
        "https://rokmp.de/de/churches/gemeinde-zu-ehren-der-hl-gottesmutter-ikone-feodorovskaya/"
      ],
      "address": [
        "Maximilian-Kolbe-Straße 2, 33175 Bad Lippspringe, Германия"
      ]
    },
    {
      "id": "de-mp-bad-reichenhall-gemeinde-zu-ehren-der-hll-wera-nadezhda-lubow-und-ihren-mutter-sofia",
      "parent": "ru-berlin-and-germany",
      "kind": "parish",
      "rank": "Parish",
      "name": "Russian Orthodox Parish in honor of St. Vera, Nadezhda, Lubow and their mother Sofia",
      "local": "Gemeinde zu Ehren der Hll. Wera, Nadezhda, Lubow und ihren Mutter Sofia",
      "country": "DE",
      "sources": [
        "https://rokmp.de/de/churches/prihod-svjatyh-muchenic-very-nadezhdy-ljubovi-i-materi-ih-sofii/"
      ]
    },
    {
      "id": "de-mp-baden-baden-christi-verklarungs-gemeinde",
      "parent": "ru-berlin-and-germany",
      "kind": "parish",
      "rank": "Parish",
      "name": "Russian Orthodox Christ Transfiguration Church",
      "local": "Christi-Verklärungs-Gemeinde",
      "country": "DE",
      "sources": [
        "https://rokmp.de/de/churches/prihod-preobrazheniya-gospodnya/"
      ],
      "address": [
        "Königsberger Str. 16a, 76532 Baden-Baden"
      ]
    },
    {
      "id": "de-mp-bamberg-hl-ehrw-sebastian-von-karaganda",
      "parent": "ru-berlin-and-germany",
      "kind": "parish",
      "rank": "Parish",
      "name": "Russian Orthodox St. Venerable Sebastian of Karaganda",
      "local": "Hl. Ehrw. Sebastian von Karaganda",
      "country": "DE",
      "sources": [
        "https://rokmp.de/de/churches/obshhina-prp-sevastiana-karagandinskogo/"
      ]
    },
    {
      "id": "de-mp-bayreuth-gemeinde-hll-12-apostel",
      "parent": "ru-berlin-and-germany",
      "kind": "parish",
      "rank": "Parish",
      "name": "Russian Orthodox Parish of Hll. 12 apostles",
      "local": "Gemeinde Hll. 12 Apostel",
      "country": "DE",
      "sources": [
        "https://rokmp.de/de/churches/obshhina-dvenadtsati-apostolov/"
      ],
      "address": [
        "Leuschnerstraße 80, 95447, Bayreuth, Deutschland"
      ]
    },
    {
      "id": "de-mp-berlin-christi-auferstehungs-kathedrale",
      "parent": "ru-berlin-and-germany",
      "kind": "parish",
      "rank": "Cathedral",
      "name": "Russian Orthodox Christ's Resurrection Cathedral",
      "local": "Christi-Auferstehungs-Kathedrale",
      "country": "DE",
      "sources": [
        "https://rokmp.de/de/churches/hohenzollerndamm-166-10713-berlin/"
      ],
      "address": [
        "Hohenzollerndamm 166, 10713 Berlin"
      ]
    },
    {
      "id": "de-mp-berlin-hl-sergius-von-radonezh-kirche",
      "parent": "ru-berlin-and-germany",
      "kind": "parish",
      "rank": "Parish",
      "name": "Russian Orthodox St. Sergius of Radonezh Church",
      "local": "Hl.-Sergius-von-Radonezh-Kirche",
      "country": "DE",
      "sources": [
        "https://rokmp.de/de/churches/hram-prp-sergiya-radonezhskogo/"
      ]
    },
    {
      "id": "de-mp-berlin-gemeinde-im-stadtbezirk-von-berlin-marzahn-hellersdorf",
      "parent": "ru-berlin-and-germany",
      "kind": "parish",
      "rank": "Parish",
      "name": "Russian Orthodox Municipality in the Marzahn - Hellersdorf district of Berlin",
      "local": "Gemeinde im Stadtbezirk von Berlin Marzahn - Hellersdorf",
      "country": "DE",
      "sources": [
        "https://rokmp.de/de/churches/obshhina-ravnoap-knyazya-vladimira-v-rayone-g-berlina-martsan-hellersdorf/"
      ]
    },
    {
      "id": "de-mp-berlin-hll-konstantin-und-helena-kirche",
      "parent": "ru-berlin-and-germany",
      "kind": "parish",
      "rank": "Parish",
      "name": "Russian Orthodox St. Constantine and Helena Church",
      "local": "Hll.-Konstantin-und-Helena-Kirche",
      "country": "DE",
      "sources": [
        "https://rokmp.de/de/churches/hll-konstantin-und-helena-kirche/"
      ],
      "address": [
        "Wittestr. 37, 13509 Berlin-Tegel"
      ]
    },
    {
      "id": "de-mp-berlin-hl-isidor-von-rostov-gemeinde",
      "parent": "ru-berlin-and-germany",
      "kind": "parish",
      "rank": "Parish",
      "name": "Russian Orthodox St. Isidore of Rostov Parish",
      "local": "Hl. Isidor von Rostov Gemeinde",
      "country": "DE",
      "sources": [
        "https://rokmp.de/de/churches/obshhina-isidora-rostovskogo/"
      ],
      "address": [
        "Alt-Lankwitz 43, 12247 Berlin, Германия"
      ]
    },
    {
      "id": "de-mp-berlin-gemeinde-in-spandau",
      "parent": "ru-berlin-and-germany",
      "kind": "parish",
      "rank": "Parish",
      "name": "Russian Orthodox Community in Spandau",
      "local": "Gemeinde in Spandau",
      "country": "DE",
      "sources": [
        "https://rokmp.de/de/churches/obshhina-v-shpandau/"
      ],
      "address": [
        "Melanchthonplatz 1, 13595, Berlin, Deutschland"
      ]
    },
    {
      "id": "de-mp-berlin-gemeinde-zu-ehren-des-hl-grossmartyrers-johann-von-suceava",
      "parent": "ru-berlin-and-germany",
      "kind": "parish",
      "rank": "Parish",
      "name": "Russian Orthodox Parish in honor of the Great Martyr John of Suceava",
      "local": "Gemeinde zu Ehren des Hl. Großmärtyrers Johann von Suceava",
      "country": "DE",
      "sources": [
        "https://rokmp.de/de/churches/obshhina-vo-imja-sv-vmch-ioanna-sochavskogo/"
      ],
      "address": [
        "Robert-Siewert-Straße 67, 10318 Берлин, Германия"
      ]
    },
    {
      "id": "de-mp-bischofsheim-an-der-rhon-kirche-d-hl-nektarius-von-aigina-und-hl-prokopius-von-ustiug",
      "parent": "ru-berlin-and-germany",
      "kind": "parish",
      "rank": "Parish",
      "name": "Russian Orthodox Church d. St. Nectarius of Aegina and St. Procopius of Ustiug",
      "local": "Kirche d. Hl. Nektarius von Aigina und Hl. Prokopius von Ustiug",
      "country": "DE",
      "sources": [
        "https://rokmp.de/de/churches/hram-svt-nektarya-eginskogo-i-blzh-prokopiya-ustyuzhskogo/"
      ],
      "address": [
        "Fastnachtsgasse 4, 97653 Bischofsheim (Rhön)"
      ]
    },
    {
      "id": "de-mp-bonn-maria-schutz-kirche",
      "parent": "ru-berlin-and-germany",
      "kind": "parish",
      "rank": "Parish",
      "name": "Russian Orthodox Church of the Protection of Mary",
      "local": "Mariä-Schutz-Kirche",
      "country": "DE",
      "sources": [
        "https://rokmp.de/de/churches/prihod-pokrova-presvyatoy-bogoroditsyi/"
      ],
      "address": [
        "Am Draitschbusch 2A, 53177, Bonn, Deutschland"
      ]
    },
    {
      "id": "de-mp-brandenburg-gemeinde-der-ikone-von-gottesmutter-freude-aller-betrubten",
      "parent": "ru-berlin-and-germany",
      "kind": "parish",
      "rank": "Parish",
      "name": "Russian Orthodox Parish of the Icon of the Mother of God \"Joy of All Who Sorrow\"",
      "local": "Gemeinde der Ikone von Gottesmutter \"Freude aller Betrübten\"",
      "country": "DE",
      "sources": [
        "https://rokmp.de/de/churches/prihod-ikonyi-bozhiey-materi-vseh-skorbyashhih-radost/"
      ],
      "address": [
        "Brahmsstraße 12A, 14772, Brandenburg an der Havel, Deutschland"
      ]
    },
    {
      "id": "de-mp-bremen-gemeinde-der-hll-kaiserlichen-martyrer",
      "parent": "ru-berlin-and-germany",
      "kind": "parish",
      "rank": "Parish",
      "name": "Russian Orthodox Parish of St. Imperial martyr",
      "local": "Gemeinde der Hll. Kaiserlichen Märtyrer",
      "country": "DE",
      "sources": [
        "https://rokmp.de/de/churches/prihod-tsarstvennyih-strastoterptsev/"
      ],
      "address": [
        "Kleine Westerholzstraße 17, 28309, Bremen, Deutschland"
      ]
    },
    {
      "id": "de-mp-bremerhaven-gemeinde-zu-ehren-der-hll-anna-von-kiew-und-wladimir-abarzumow",
      "parent": "ru-berlin-and-germany",
      "kind": "parish",
      "rank": "Parish",
      "name": "Russian Orthodox Parish in honor of St. Anna of Kyiv and Vladimir Abarzumov",
      "local": "Gemeinde zu Ehren der Hll. Anna von Kiew und Wladimir Abarzumow",
      "country": "DE",
      "sources": [
        "https://rokmp.de/de/churches/evangelischen-kirche-des-hl-erzengel-michaels/"
      ]
    },
    {
      "id": "de-mp-celle-gemeinde-der-gottesmutterikone-iwerskaja",
      "parent": "ru-berlin-and-germany",
      "kind": "parish",
      "rank": "Parish",
      "name": "Russian Orthodox Parish of the Icon of the Mother of God \"Iverskaya\"",
      "local": "Gemeinde der Gottesmutterikone \"Iwerskaja\"",
      "country": "DE",
      "sources": [
        "https://rokmp.de/de/churches/obshhina-ikonyi-bozhiey-materi-iverskaya/"
      ]
    },
    {
      "id": "de-mp-chemnitz-gemeinde-zu-maria-geburt",
      "parent": "ru-berlin-and-germany",
      "kind": "parish",
      "rank": "Parish",
      "name": "Russian Orthodox Parish of the Nativity of Mary",
      "local": "Gemeinde zu Maria Geburt",
      "country": "DE",
      "sources": [
        "https://rokmp.de/de/churches/gemeinde-zu-maria-geburt/"
      ],
      "address": [
        "Hohe Straße 1, 09112 Chemnitz"
      ]
    },
    {
      "id": "de-mp-dachau-christi-auferstehungs-gedachtniskapelle",
      "parent": "ru-berlin-and-germany",
      "kind": "parish",
      "rank": "Chapel",
      "name": "Russian Orthodox Christ's Resurrection Memorial Chapel",
      "local": "Christi-Auferstehungs-Gedächtniskapelle",
      "country": "DE",
      "sources": [
        "https://rokmp.de/de/churches/voskresenskaya-chasovnya-pamyatnik/"
      ],
      "address": [
        "85221 Dachau, Alte Römerstr. 75"
      ]
    },
    {
      "id": "de-mp-demmin-gemeinde-zu-ehren-des-hl-nikolaus-von-japan",
      "parent": "ru-berlin-and-germany",
      "kind": "parish",
      "rank": "Parish",
      "name": "Russian Orthodox Parish in honor of St. Nicholas of Japan",
      "local": "Gemeinde zu Ehren des Hl. Nikolaus von Japan",
      "country": "DE",
      "sources": [
        "https://rokmp.de/de/churches/obshhina-svt-ravnoap-nikolaya-yaponskogo/"
      ],
      "address": [
        "St. Bartholomäus Kirche, Kirchplatz 7, 17109 Demmin"
      ]
    },
    {
      "id": "de-mp-dieburg-russisch-orthodoxe-gemeinde-des-heiligen-luka",
      "parent": "ru-berlin-and-germany",
      "kind": "parish",
      "rank": "Parish",
      "name": "Russian Orthodox Russian Orthodox Parish of Saint Luke",
      "local": "Russisch-orthodoxe Gemeinde des Heiligen Luka",
      "country": "DE",
      "sources": [
        "https://rokmp.de/de/churches/prihod-svjatitelja-luki-krymskogo/"
      ],
      "address": [
        "Kapuzinerkloster / Russische Kirche, Minnefeld 36, 64807 Дибург, Германия"
      ]
    },
    {
      "id": "de-mp-dortmund-kirchengemeinde-zu-ehren-der-heiligen-dreifaltigkeit",
      "parent": "ru-berlin-and-germany",
      "kind": "parish",
      "rank": "Parish",
      "name": "Russian Orthodox Parish in honor of the Holy Trinity",
      "local": "Kirchengemeinde zu Ehren der Heiligen Dreifaltigkeit",
      "country": "DE",
      "sources": [
        "https://rokmp.de/de/churches/prihod-svyatoy-zhivonachalnoy-troitsyi/"
      ],
      "address": [
        "Flurstr. 39, 44145"
      ]
    },
    {
      "id": "de-mp-dresden-kirche-d-ehrw-symeon-vom-wunderbaren-berge",
      "parent": "ru-berlin-and-germany",
      "kind": "parish",
      "rank": "Parish",
      "name": "Russian Orthodox Church d. Venerable Symeon of the Wonderful Mountains",
      "local": "Kirche d. Ehrw. Symeon vom Wunderbaren Berge",
      "country": "DE",
      "sources": [
        "https://rokmp.de/de/churches/hram-prp-simeona-divnogortsa/"
      ],
      "address": [
        "Fritz-Löffler-Str. 19, 01069 Dresden"
      ]
    },
    {
      "id": "de-mp-duisburg-kirchengemeinde-zur-gottesmutterikone-freude-und-trost-zu-duisburg",
      "parent": "ru-berlin-and-germany",
      "kind": "parish",
      "rank": "Parish",
      "name": "Russian Orthodox Parish of the Mother of God icon \"Joy and Consolation\" in Duisburg",
      "local": "Kirchengemeinde zur Gottesmutterikone \"Freude und Trost\" zu Duisburg",
      "country": "DE",
      "sources": [
        "https://rokmp.de/de/churches/obshhina-ikonyi-bozhiey-materi-otrada-i-uteshenie/"
      ],
      "address": [
        "Norbertuskirchplatz 10 47166 Duisburg"
      ]
    },
    {
      "id": "de-mp-dusseldorf-maria-obhut-kirche",
      "parent": "ru-berlin-and-germany",
      "kind": "parish",
      "rank": "Parish",
      "name": "Russian Orthodox Maria-Obhut-Church",
      "local": "Maria-Obhut-Kirche",
      "country": "DE",
      "sources": [
        "https://rokmp.de/de/churches/hram-pokrova-presvyatoy-bogoroditsyi-predstavitelstvo-russkoy-pravoslavnoy-tserkvi-v-germanii/"
      ],
      "address": [
        "Germany, 40227 Duesseldorf, Ellerstr. 213"
      ]
    },
    {
      "id": "de-mp-erfurt-gemeinde-in-erfurt",
      "parent": "ru-berlin-and-germany",
      "kind": "parish",
      "rank": "Parish",
      "name": "Russian Orthodox Community in Erfurt",
      "local": "Gemeinde in Erfurt",
      "country": "DE",
      "sources": [
        "https://rokmp.de/de/churches/obshhina-v-gorode-erfurt/"
      ]
    },
    {
      "id": "de-mp-essen-gemeinde-zu-den-hll-uneigennutzigen-kosmas-und-damian-zu-essen",
      "parent": "ru-berlin-and-germany",
      "kind": "parish",
      "rank": "Parish",
      "name": "Russian Orthodox Community of the Holy Food for unselfish Kosmas and Damian",
      "local": "Gemeinde zu den Hll. Uneigennützigen Kosmas und Damian zu Essen",
      "country": "DE",
      "sources": [
        "https://rokmp.de/de/churches/gemeinde-zu-den-hll-uneigennutzigen-kosmas-und-damian-zu-essen/"
      ],
      "address": [
        "Schonnebeckhöfe, 202, 45327 Essen"
      ]
    },
    {
      "id": "de-mp-frankfurt-oder-christus-erloser-gemeinde",
      "parent": "ru-berlin-and-germany",
      "kind": "parish",
      "rank": "Parish",
      "name": "Russian Orthodox Christ the Redeemer Church",
      "local": "Christus-Erlöser-Gemeinde",
      "country": "DE",
      "sources": [
        "https://rokmp.de/de/churches/christus-erloser-gemeinde/"
      ],
      "address": [
        "Bahnhofstraße 3, 15295 Brieskow-Finkenheerd, Германия"
      ]
    },
    {
      "id": "de-mp-frankfurt-am-main-gemeinde-zu-ehren-der-hieromart-kyprianos-und-martt-justina",
      "parent": "ru-berlin-and-germany",
      "kind": "parish",
      "rank": "Parish",
      "name": "Russian Orthodox Community in honor of Hieromart. Kyprianos and Martt. Justina",
      "local": "Gemeinde zu Ehren der Hieromart. Kyprianos und Martt. Justina",
      "country": "DE",
      "sources": [
        "https://rokmp.de/de/churches/gemeinde-zu-ehren-der-hieromart-kyprianos-und-martt-justina/"
      ],
      "address": [
        "Fuldaer Str. 20, 60386 Frankfurt am Main, Франкфурт-Ост, Германия"
      ]
    },
    {
      "id": "de-mp-freiburg-im-breisgau-hl-nikolaus-in-freiburg",
      "parent": "ru-berlin-and-germany",
      "kind": "parish",
      "rank": "Parish",
      "name": "Russian Orthodox St. Nicholas in Freiburg",
      "local": "Hl. Nikolaus in Freiburg",
      "country": "DE",
      "sources": [
        "https://rokmp.de/de/churches/gemeinde-des-hl-nikolaus/"
      ],
      "address": [
        "Auwaldstraße 94A, 79110 Freiburg im Breisgau, Германия"
      ]
    },
    {
      "id": "de-mp-friedrichshafen-ailingen-gemeinde-in-friedrichshafen",
      "parent": "ru-berlin-and-germany",
      "kind": "parish",
      "rank": "Parish",
      "name": "Russian Orthodox Community in Friedrichshafen",
      "local": "Gemeinde in Friedrichshafen",
      "country": "DE",
      "sources": [
        "https://rokmp.de/de/churches/obshhina-v-fridrishafen/"
      ],
      "address": [
        "Kirchstraße 51, 88131 Bodolz, Германия"
      ]
    },
    {
      "id": "de-mp-fulda-gemeinde-zu-ehren-des-festes-begegnung-des-herrn",
      "parent": "ru-berlin-and-germany",
      "kind": "parish",
      "rank": "Parish",
      "name": "Russian Orthodox Parish in honor of the Feast of the Encounter of the Lord",
      "local": "Gemeinde zu Ehren des Festes Begegnung des Herrn",
      "country": "DE",
      "sources": [
        "https://rokmp.de/de/churches/obshhina-sreteniya-gospodnya/"
      ],
      "address": [
        "Ratgarstr.13 36037 Fulda"
      ]
    },
    {
      "id": "de-mp-giessen-gemeinde-zu-ehren-der-shirovizer-gottesmutterikone",
      "parent": "ru-berlin-and-germany",
      "kind": "parish",
      "rank": "Parish",
      "name": "Russian Orthodox Parish in honor of the Shirovitz Mother of God icon",
      "local": "Gemeinde zu Ehren der Shirovizer Gottesmutterikone",
      "country": "DE",
      "sources": [
        "https://rokmp.de/de/churches/obshhina-v-chest-ikonyi-bozhiey-materi-zhirovitskaya/"
      ],
      "address": [
        "Egerländer Straße, 35435 Веттенберг-Krofdorf-Gleiberg, Германия"
      ]
    },
    {
      "id": "de-mp-gifhorn-braunschweig-hl-nikolaus-kirche",
      "parent": "ru-berlin-and-germany",
      "kind": "parish",
      "rank": "Parish",
      "name": "Russian Orthodox St. Nicholas Church",
      "local": "Hl.-Nikolaus-Kirche",
      "country": "DE",
      "sources": [
        "https://rokmp.de/de/churches/hram-svt-nikolaya-chudotvortsa/"
      ]
    },
    {
      "id": "de-mp-greifswald-gemeinde-zu-ehren-der-hl-matrona-von-moskau",
      "parent": "ru-berlin-and-germany",
      "kind": "parish",
      "rank": "Parish",
      "name": "Russian Orthodox Parish in honor of St. Matrona of Moscow",
      "local": "Gemeinde zu Ehren der Hl. Matrona von Moskau",
      "country": "DE",
      "sources": [
        "https://rokmp.de/de/churches/obshhina-blzh-matronyi-moskovskoy/"
      ],
      "address": [
        "An der Christuskirche 1, 17491 Greifswald"
      ]
    },
    {
      "id": "de-mp-gotschendorf-st-georg-mannerkloster-in-gotschendorf",
      "parent": "ru-berlin-and-germany",
      "kind": "parish",
      "rank": "Parish",
      "name": "Russian Orthodox St. George men's monastery in Götschendorf",
      "local": "St.-Georg Männerkloster in Götschendorf",
      "country": "DE",
      "sources": [
        "https://rokmp.de/de/churches/monastyir-vmch-georgiya-pobedonostsa-v-gyotshendorfe/"
      ],
      "address": [
        "Germany, St. Georgskloster, Russische Orthodoxe Kirche Götschendorf 33, 17268 Milmersdorf"
      ]
    },
    {
      "id": "de-mp-gottingen-gemeinde-des-hl-erzengels-michael",
      "parent": "ru-berlin-and-germany",
      "kind": "parish",
      "rank": "Parish",
      "name": "Russian Orthodox Parish of St. Archangel Michael",
      "local": "Gemeinde des Hl. Erzengels Michael",
      "country": "DE",
      "sources": [
        "https://rokmp.de/de/churches/prihod-arhistratiga-bozhiya-mihaila/"
      ],
      "address": [
        "Stauffenbergring 4, 37075 Göttingen"
      ]
    },
    {
      "id": "de-mp-hagen-gemeinde-der-ikone-von-gottes-mutter-schau-auf-demut",
      "parent": "ru-berlin-and-germany",
      "kind": "parish",
      "rank": "Parish",
      "name": "Russian Orthodox Parish of the Icon of the Mother of God \"Look at Humility\"",
      "local": "Gemeinde der Ikone von Gottes Mutter \"Schau auf Demut\"",
      "country": "DE",
      "sources": [
        "https://rokmp.de/de/churches/obshhina-v-chest-ikony-bozhiej-materi-prizri-na-smirenie/"
      ],
      "address": [
        "Schillerstraße 14-16, 58089 Hagen, Германия"
      ]
    },
    {
      "id": "de-mp-halberstadt-kirchengemeinde-des-heiligen-erstmartyrers-und-archidiakons-stephanus",
      "parent": "ru-berlin-and-germany",
      "kind": "parish",
      "rank": "Parish",
      "name": "Russian Orthodox Parish of the Holy First Martyr and Archdeacon Stephen",
      "local": "Kirchengemeinde des heiligen Erstmärtyrers und Archidiakons Stephanus",
      "country": "DE",
      "sources": [
        "https://rokmp.de/de/churches/obshhina-v-halbershtadte/"
      ],
      "address": [
        "Moritzplan 1, 38820 Halberstadt, Германия"
      ]
    },
    {
      "id": "de-mp-halle-saale-kreuzerhohungs-gemeinde",
      "parent": "ru-berlin-and-germany",
      "kind": "parish",
      "rank": "Parish",
      "name": "Russian Orthodox Church of the Exaltation of the Cross",
      "local": "Kreuzerhöhungs-Gemeinde",
      "country": "DE",
      "sources": [
        "https://rokmp.de/de/churches/prihod-vozdvizheniya-kresta-gospodnya/"
      ],
      "address": [
        "Haus 24, Franckeplatz 1, 06110 Halle (Saale)"
      ]
    },
    {
      "id": "de-mp-hamburg-gemeinde-des-hl-johannes-von-kronstadt",
      "parent": "ru-berlin-and-germany",
      "kind": "parish",
      "rank": "Parish",
      "name": "Russian Orthodox Parish of St. John of Kronstadt",
      "local": "Gemeinde des Hl. Johannes von Kronstadt",
      "country": "DE",
      "sources": [
        "https://rokmp.de/de/churches/hram-prav-ioanna-kronshtadtskogo/"
      ],
      "address": [
        "Tschaikowskyplatz 1, 20355, Hamburg, Deutschland"
      ]
    },
    {
      "id": "de-mp-hamburg-die-holzkirche-der-hl-myrontragerinnen",
      "parent": "ru-berlin-and-germany",
      "kind": "parish",
      "rank": "Parish",
      "name": "Russian Orthodox The wooden church of the Holy Myron Bearers",
      "local": "Die Holzkirche der Hl. Myronträgerinnen",
      "country": "DE",
      "sources": [
        "https://rokmp.de/de/churches/derevyannyiy-hram-svv-zhen-mironosits/"
      ],
      "address": [
        "Holstenkamp 89, 22525 Hamburg"
      ]
    },
    {
      "id": "de-mp-hamburg-gemeinde-hll-kirill-und-method",
      "parent": "ru-berlin-and-germany",
      "kind": "parish",
      "rank": "Parish",
      "name": "Russian Orthodox Parish of Hll. Kirill and Methodius",
      "local": "Gemeinde Hll. Kirill und Method",
      "country": "DE",
      "sources": [
        "https://rokmp.de/de/churches/prihod-ravnoapp-kirilla-i-mefodiya/"
      ]
    },
    {
      "id": "de-mp-hameln-landkreis-hameln-pyrmont-gemeinde-landkreis-hameln-pyrmont",
      "parent": "ru-berlin-and-germany",
      "kind": "parish",
      "rank": "Parish",
      "name": "Russian Orthodox Municipality of the Hameln-Pyrmont district",
      "local": "Gemeinde Landkreis Hameln-Pyrmont",
      "country": "DE",
      "sources": [
        "https://rokmp.de/de/churches/gameln-pirmont/"
      ],
      "address": [
        "Lohstraße 8, 31785 Hameln"
      ]
    },
    {
      "id": "de-mp-hannover-maria-verkundigung-gemeinde",
      "parent": "ru-berlin-and-germany",
      "kind": "parish",
      "rank": "Parish",
      "name": "Russian Orthodox Annunciation Parish",
      "local": "Mariä-Verkündigung-Gemeinde",
      "country": "DE",
      "sources": [
        "https://rokmp.de/de/churches/prihod-blagoveshheniya-presvyatoy-bogoroditsyi-2/"
      ]
    },
    {
      "id": "de-mp-hof-gemeinde-der-hl-nina",
      "parent": "ru-berlin-and-germany",
      "kind": "parish",
      "rank": "Parish",
      "name": "Russian Orthodox Parish of St. Nina",
      "local": "Gemeinde der Hl. Nina",
      "country": "DE",
      "sources": [
        "https://rokmp.de/de/churches/prihod-svjatoj-ravnoapostolnoj-niny/"
      ],
      "address": [
        "Neue Heimat, 95191 Leupoldsgrün, Hof, Германия"
      ]
    },
    {
      "id": "de-mp-homburg-gemeinde-zu-ehren-der-heiligen-fursten-peter-und-fevronia-wundertater-von-murom",
      "parent": "ru-berlin-and-germany",
      "kind": "parish",
      "rank": "Parish",
      "name": "Russian Orthodox Parish in honor of the holy princes Peter and Fevronia, miracle workers of Murom",
      "local": "Gemeinde zu Ehren der heiligen Fürsten Peter und Fevronia, Wundertäter von Murom",
      "country": "DE",
      "sources": [
        "https://rokmp.de/de/churches/obshhina-v-g-homburg/"
      ],
      "address": [
        "Römisch-Katholische Stadtpfarrkirche St. Michael, Санкт-Михаэль-штрассе 7, 66424 Homburg, Германия"
      ]
    },
    {
      "id": "de-mp-husum-christlich-orthodoxe-gemeinde",
      "parent": "ru-berlin-and-germany",
      "kind": "parish",
      "rank": "Parish",
      "name": "Russian Orthodox Christian Orthodox community",
      "local": "Christlich-orthodoxe Gemeinde",
      "country": "DE",
      "sources": [
        "https://rokmp.de/de/churches/pravoslavnaja-obshhina/"
      ],
      "address": [
        "Bonhoefferweg 1, 25813 Husum, Германия"
      ]
    },
    {
      "id": "de-mp-jena-gemeinde-in-jena",
      "parent": "ru-berlin-and-germany",
      "kind": "parish",
      "rank": "Parish",
      "name": "Russian Orthodox Community in Jena",
      "local": "Gemeinde in Jena",
      "country": "DE",
      "sources": [
        "https://rokmp.de/de/churches/obshhina-v-gorode-yena/"
      ],
      "address": [
        "Werner-Seelenbinder-Straße 26, 07747, Jena, Deutschland"
      ]
    },
    {
      "id": "de-mp-kaiserslautern-gottesmutter-von-vladimir-gemeinde",
      "parent": "ru-berlin-and-germany",
      "kind": "parish",
      "rank": "Parish",
      "name": "Russian Orthodox Mother of God of Vladimir Parish",
      "local": "Gottesmutter von Vladimir Gemeinde",
      "country": "DE",
      "sources": [
        "https://rokmp.de/de/churches/gottesmutter-von-vladimir-gemeinde/"
      ],
      "address": [
        "Kloster Str.6 D- 67655 Kaiserslautern"
      ]
    },
    {
      "id": "de-mp-kassel-gemeinde-der-hll-neumartyrer-von-russland",
      "parent": "ru-berlin-and-germany",
      "kind": "parish",
      "rank": "Parish",
      "name": "Russian Orthodox Parish of St. New Martyrs of Russia",
      "local": "Gemeinde der Hll. Neumärtyrer von Russland",
      "country": "DE",
      "sources": [
        "https://rokmp.de/de/churches/gemeinde-der-hll-neumartyrer-von-russland/"
      ],
      "address": [
        "Steinweg, 34117 Kassel"
      ]
    },
    {
      "id": "de-mp-kempten-hll-nikolaus-gemeinde",
      "parent": "ru-berlin-and-germany",
      "kind": "parish",
      "rank": "Parish",
      "name": "Russian Orthodox Hll. Nicholas Parish",
      "local": "Hll. Nikolaus-Gemeinde",
      "country": "DE",
      "sources": [
        "https://rokmp.de/de/churches/hll-nikolaus-gemeinde/"
      ],
      "address": [
        "Fürstenstraße 9, 87439 Kempten (Allgäu), Германия"
      ]
    },
    {
      "id": "de-mp-krefeld-gemeinde-der-hl-grossmartyrerin-barbara-zu-krefeld",
      "parent": "ru-berlin-and-germany",
      "kind": "parish",
      "rank": "Parish",
      "name": "Russian Orthodox Parish of the Holy Great Martyr Barbara in Krefeld",
      "local": "Gemeinde der Hl. Großmärtyrerin Barbara zu Krefeld",
      "country": "DE",
      "sources": [
        "https://rokmp.de/de/churches/obshhina-svyatoy-velikomuchenitsyi-varvaryi/"
      ],
      "address": [
        "Wielandstr. 11, 47799 Krefeld"
      ]
    },
    {
      "id": "de-mp-koln-hll-konstantin-und-helena-kirche",
      "parent": "ru-berlin-and-germany",
      "kind": "parish",
      "rank": "Parish",
      "name": "Russian Orthodox St. Constantine and Helena Church",
      "local": "Hll.-Konstantin-und-Helena-Kirche",
      "country": "DE",
      "sources": [
        "https://rokmp.de/de/churches/hll-konstantin-und-helena-kirche-koln/"
      ],
      "address": [
        "Maria-Ablaß-Platz 14, 50668 Köln"
      ]
    },
    {
      "id": "de-mp-lahr-gemeinde-des-heiligen-geistes",
      "parent": "ru-berlin-and-germany",
      "kind": "parish",
      "rank": "Parish",
      "name": "Russian Orthodox Church of the Holy Spirit",
      "local": "Gemeinde des Heiligen Geistes",
      "country": "DE",
      "sources": [
        "https://rokmp.de/de/churches/obshhina-svyatago-duha/"
      ],
      "address": [
        "Untere Hauptstraße 33, 77933 Lahr/Schwarzwald, Германия"
      ]
    },
    {
      "id": "de-mp-leverkusen-gemeinde-des-hl-alexander-swirsky",
      "parent": "ru-berlin-and-germany",
      "kind": "parish",
      "rank": "Parish",
      "name": "Russian Orthodox Parish of St. Alexander Swirsky",
      "local": "Gemeinde des Hl. Alexander Swirsky",
      "country": "DE",
      "sources": [
        "https://rokmp.de/de/churches/obshhina-sv-prep-aleksandra-svirskogo/"
      ]
    },
    {
      "id": "de-mp-lippstadt-irchengemeinde-des-hl-tichon-patriarchen-von-moskau-und-ganz-russland",
      "parent": "ru-berlin-and-germany",
      "kind": "parish",
      "rank": "Parish",
      "name": "Russian Orthodox Parish of St. Tikhon, Patriarch of Moscow and All Russia",
      "local": "Кirchengemeinde des Hl. Tichon, Patriarchen von Moskau und ganz Russland",
      "country": "DE",
      "sources": [
        "https://rokmp.de/de/churches/obshhina-vo-imja-svjatitelja-tihona-patriarha-moskovskogo-i-vseja-rossii/"
      ],
      "address": [
        "Beckumer Straße 118, 59555 Lippstadt, Германия"
      ]
    },
    {
      "id": "de-mp-mainz-hl-martyrer-christophor-pfarrei",
      "parent": "ru-berlin-and-germany",
      "kind": "parish",
      "rank": "Parish",
      "name": "Russian Orthodox Holy Martyr Christopher Parish",
      "local": "Hl.-Märtyrer-Christophor- Pfarrei",
      "country": "DE",
      "sources": [
        "https://rokmp.de/de/churches/hl-martyrer-christophor-gemeinde/"
      ],
      "address": [
        "Berliner Straße 39A, 55131 Mainz, Германия"
      ]
    },
    {
      "id": "de-mp-monchengladbach",
      "parent": "ru-berlin-and-germany",
      "kind": "parish",
      "rank": "Parish",
      "name": "Russian Orthodox (Русский) Приход св. преп. Антония Великого",
      "local": "(Русский) Приход св. преп. Антония Великого",
      "country": "DE",
      "sources": [
        "https://rokmp.de/de/churches/prihod-sv-prep-antoniya-velikogo/"
      ],
      "address": [
        "Am Torfbend 19, 41238 Mönchengladbach"
      ]
    },
    {
      "id": "de-mp-munchen-christi-auferstehungspfarrei",
      "parent": "ru-berlin-and-germany",
      "kind": "parish",
      "rank": "Parish",
      "name": "Russian Orthodox Christ's Resurrection Parish",
      "local": "Christi-Auferstehungspfarrei",
      "country": "DE",
      "sources": [
        "https://rokmp.de/de/churches/christi-auferstehungsgemeinde/"
      ],
      "address": [
        "Knappertsbuschstraße 26, 81927 München, Германия"
      ]
    },
    {
      "id": "de-mp-munchen-kirche-der-kreuzerhohung",
      "parent": "ru-berlin-and-germany",
      "kind": "parish",
      "rank": "Parish",
      "name": "Russian Orthodox Church of the Exaltation of the Cross",
      "local": "Kirche der Kreuzerhöhung",
      "country": "DE",
      "sources": [
        "https://rokmp.de/de/churches/hram-vozdvizheniya-chestnago-i-zhivotvoryashhego-kresta-gospodnya-pri-yuzhnoy-rezidentsii-pravyashhago-arhiereya/"
      ],
      "address": [
        "Glyzinenstraße 38, 80935 Мюнхен, Германия"
      ]
    },
    {
      "id": "de-mp-neuruppin-gemeinde-in-neuruppin",
      "parent": "ru-berlin-and-germany",
      "kind": "parish",
      "rank": "Parish",
      "name": "Russian Orthodox Community in Neuruppin",
      "local": "Gemeinde in Neuruppin",
      "country": "DE",
      "sources": [
        "https://rokmp.de/de/churches/prihod-vmch-georgiya-pobedonostsa/"
      ]
    },
    {
      "id": "de-mp-neuss-gemeinde-zu-den-hll-erzengeln",
      "parent": "ru-berlin-and-germany",
      "kind": "parish",
      "rank": "Parish",
      "name": "Russian Orthodox Community of the Holy Archangels",
      "local": "Gemeinde zu den Hll. Erzengeln",
      "country": "DE",
      "sources": [
        "https://rokmp.de/de/churches/gemeinde-zu-den-hll-erzengeln/"
      ],
      "address": [
        "Alexianerplatz 1, 41464 Neuss"
      ]
    },
    {
      "id": "de-mp-nienburg-gemeinde-des-hl-lazarus",
      "parent": "ru-berlin-and-germany",
      "kind": "parish",
      "rank": "Parish",
      "name": "Russian Orthodox Parish of St. Lazarus",
      "local": "Gemeinde des Hl. Lazarus",
      "country": "DE",
      "sources": [
        "https://rokmp.de/de/churches/prihod-sv-lazarja/"
      ],
      "address": [
        "Martinsheidestraße 8, 31582 Nienburg/Weser, Германия"
      ]
    },
    {
      "id": "de-mp-nurnberg-gemeinde-zu-ehren-der-seligen-xenia-von-st-petersburg",
      "parent": "ru-berlin-and-germany",
      "kind": "parish",
      "rank": "Parish",
      "name": "Russian Orthodox Parish in honor of Blessed Xenia of St. Petersburg",
      "local": "Gemeinde zu Ehren der Seligen Xenia von St.-Petersburg",
      "country": "DE",
      "sources": [
        "https://rokmp.de/de/churches/gemeinde-zu-ehren-der-seligen-xenia-von-st-petersburg/"
      ],
      "address": [
        "Glockenhofstraße 30, 90478 Nürnberg, Германия"
      ]
    },
    {
      "id": "de-mp-osnabruck-gemeinde-zu-ehren-der-hl-grossmartyrerin-paraskewa",
      "parent": "ru-berlin-and-germany",
      "kind": "parish",
      "rank": "Parish",
      "name": "Russian Orthodox Parish in honor of the Holy Great Martyr Paraskeva",
      "local": "Gemeinde zu Ehren der Hl. Großmärtyrerin Paraskewa",
      "country": "DE",
      "sources": [
        "https://rokmp.de/de/churches/gemeinde-zu-ehren-des-hl-grosmartyrer-georgij/"
      ],
      "address": [
        "Mühlenbreede, 49504 Lotte-Wersen, Германия"
      ]
    },
    {
      "id": "de-mp-passau-gemeinde-in-passau",
      "parent": "ru-berlin-and-germany",
      "kind": "parish",
      "rank": "Parish",
      "name": "Russian Orthodox Community in Passau",
      "local": "Gemeinde in Passau",
      "country": "DE",
      "sources": [
        "https://rokmp.de/de/churches/passau-kirche/"
      ],
      "address": [
        "Dom St. Stephan, Domplatz, 94032 Passau, Германия"
      ]
    },
    {
      "id": "de-mp-pforzheim-epiphanie-gemeinde",
      "parent": "ru-berlin-and-germany",
      "kind": "parish",
      "rank": "Parish",
      "name": "Russian Orthodox Epiphany community",
      "local": "Epiphanie Gemeinde",
      "country": "DE",
      "sources": [
        "https://rokmp.de/de/churches/epiphanie-gemeinde/"
      ]
    },
    {
      "id": "de-mp-potsdam-hll-alexander-nevskij-kirche",
      "parent": "ru-berlin-and-germany",
      "kind": "parish",
      "rank": "Parish",
      "name": "Russian Orthodox St. Alexander Nevsky Church",
      "local": "Hll.-Alexander-Nevskij-Kirche",
      "country": "DE",
      "sources": [
        "https://rokmp.de/de/churches/hll-alexander-nevskij-kirche/"
      ],
      "address": [
        "Russische Kolonie 14, 14469 Potsdam"
      ]
    },
    {
      "id": "de-mp-rostock-gemeinde-zu-ehren-der-seligen-xenia-von-st-petersburg",
      "parent": "ru-berlin-and-germany",
      "kind": "parish",
      "rank": "Parish",
      "name": "Russian Orthodox Parish in honor of Blessed Xenia of St. Petersburg",
      "local": "Gemeinde zu Ehren der Seligen Xenia von St.-Petersburg",
      "country": "DE",
      "sources": [
        "https://rokmp.de/de/churches/gemeinde-zu-ehren-der-seligen-xenia-von-st-petersburg-2/"
      ],
      "address": [
        "Thünenstr. 9, Rostock 18057"
      ]
    },
    {
      "id": "de-mp-saarbrucken-gemeinde-des-hl-panteleimon",
      "parent": "ru-berlin-and-germany",
      "kind": "parish",
      "rank": "Parish",
      "name": "Russian Orthodox Parish of St. Panteleimon",
      "local": "Gemeinde des Hl. Panteleimon",
      "country": "DE",
      "sources": [
        "https://rokmp.de/de/churches/gemeinde-des-hl-panteleimon/"
      ],
      "address": [
        "Schumannstr, 25, 66111 Saarbrücken"
      ]
    },
    {
      "id": "de-mp-schweinfurt-hl-johannes-der-taufer-gemeinde",
      "parent": "ru-berlin-and-germany",
      "kind": "parish",
      "rank": "Parish",
      "name": "Russian Orthodox St. John the Baptist Parish",
      "local": "Hl. Johannes der Täufer Gemeinde",
      "country": "DE",
      "sources": [
        "https://rokmp.de/de/churches/hl-johannes-der-taufer-gemeinde/"
      ],
      "address": [
        "Friedenstraße 17, 97421 Schweinfurt, Германия"
      ]
    },
    {
      "id": "de-mp-schwerin-gemeinde-des-hl-grossmart-demetrius-von-thessaloniki",
      "parent": "ru-berlin-and-germany",
      "kind": "parish",
      "rank": "Parish",
      "name": "Russian Orthodox Parish of St. Großmart. Demetrius of Thessalonica",
      "local": "Gemeinde des Hl. Großmart. Demetrius von Thessaloniki",
      "country": "DE",
      "sources": [
        "https://rokmp.de/de/churches/hl-grosmart-demetrius-von-thessaloniki/"
      ],
      "address": [
        "Hamburger Allee 120 19063 Schwerin Deutschland"
      ]
    },
    {
      "id": "de-mp-singen-gemeinde-des-erzengels-michael-und-aller-himmlischen-korperlosen-machte",
      "parent": "ru-berlin-and-germany",
      "kind": "parish",
      "rank": "Parish",
      "name": "Russian Orthodox Community of the Archangel Michael and all heavenly, incorporeal powers",
      "local": "Gemeinde des Erzengels Michael und aller himmlischen, körperlosen Mächte",
      "country": "DE",
      "sources": [
        "https://rokmp.de/de/churches/prihod-arhangela-mihaila-i-vseh-nebesnyih-sil-besplotnyih/"
      ]
    },
    {
      "id": "de-mp-stade-gemeinde-der-hll-mart-adrian-und-natalia",
      "parent": "ru-berlin-and-germany",
      "kind": "parish",
      "rank": "Parish",
      "name": "Russian Orthodox Parish of St. Mart. Adrian and Natalia",
      "local": "Gemeinde der Hll. Märt. Adrian und Natalia",
      "country": "DE",
      "sources": [
        "https://rokmp.de/de/churches/gemeinde-der-hll-maert-adrian-und-natalia/"
      ],
      "address": [
        "Bockhorster Weg 27, 21682 Stade, Германия"
      ]
    },
    {
      "id": "de-mp-stendal-gemeinde-des-heiligen-apostels-jakobus",
      "parent": "ru-berlin-and-germany",
      "kind": "parish",
      "rank": "Parish",
      "name": "Russian Orthodox Parish of the Holy Apostle James",
      "local": "Gemeinde des Heiligen Apostels Jakobus",
      "country": "DE",
      "sources": [
        "https://rokmp.de/de/churches/prihod-svjatogo-apostola-iakova/"
      ]
    },
    {
      "id": "de-mp-stralsund-gemeinde-zu-ehren-des-hl-grossmartyrers-georgij",
      "parent": "ru-berlin-and-germany",
      "kind": "parish",
      "rank": "Parish",
      "name": "Russian Orthodox Parish in honor of the Holy Great Martyr Georgy",
      "local": "Gemeinde zu Ehren des Hl. Großmärtyrers Georgij",
      "country": "DE",
      "sources": [
        "https://rokmp.de/de/churches/obshhina-vmch-georgiya-pobedonostsa/"
      ],
      "address": [
        "Marienstrasse 16, 18439 Stralsund"
      ]
    },
    {
      "id": "de-mp-stuttgart-hl-prophet-elias-gemeinde",
      "parent": "ru-berlin-and-germany",
      "kind": "parish",
      "rank": "Parish",
      "name": "Russian Orthodox Holy Prophet Elijah Congregation",
      "local": "Hl.-Prophet-Elias-Gemeinde",
      "country": "DE",
      "sources": [
        "https://rokmp.de/de/churches/hl-prophet-elias-gemeinde/"
      ],
      "address": [
        "Steigerwald Strasse 10, 70469 Stuttgart"
      ]
    },
    {
      "id": "de-mp-sulingen-maria-entschlafen-gemeinde",
      "parent": "ru-berlin-and-germany",
      "kind": "parish",
      "rank": "Parish",
      "name": "Russian Orthodox Dormition Parish",
      "local": "Mariä-Entschlafen-Gemeinde",
      "country": "DE",
      "sources": [
        "https://rokmp.de/de/churches/obshhina-uspeniya-presvyatoy-bogorodtsyi/"
      ],
      "address": [
        "Edenstrasse 57, 27232 Sulingen"
      ]
    },
    {
      "id": "de-mp-trier-wittlich-gemeinde-der-hll-40-martyrer-von-sebaste",
      "parent": "ru-berlin-and-germany",
      "kind": "parish",
      "rank": "Parish",
      "name": "Russian Orthodox Parish of St. 40 martyrs of Sebaste",
      "local": "Gemeinde der Hll. 40 Märtyrer von Sebaste",
      "country": "DE",
      "sources": [
        "https://rokmp.de/de/churches/hll-vierzig-martyrer-von-sebastia/"
      ],
      "address": [
        "Neustraße 11, 54528 Salmtal-Дёрбах, Германия"
      ]
    },
    {
      "id": "de-mp-tubingen-gemeinde-d-hl-maria-von-agypten",
      "parent": "ru-berlin-and-germany",
      "kind": "parish",
      "rank": "Parish",
      "name": "Russian Orthodox community d. Saint Mary of Egypt",
      "local": "Gemeinde d. Hl. Maria von Ägypten",
      "country": "DE",
      "sources": [
        "https://rokmp.de/de/churches/gemeinde-d-hl-maria-von-agypten/"
      ]
    },
    {
      "id": "de-mp-ulm-kirche-der-gottesmutterikone-das-zeichen-von-kursk",
      "parent": "ru-berlin-and-germany",
      "kind": "parish",
      "rank": "Parish",
      "name": "Russian Orthodox Church of the Icon of the Mother of God \"The Sign\" of Kursk",
      "local": "Kirche der Gottesmutterikone \"Das Zeichen\" von Kursk",
      "country": "DE",
      "sources": [
        "https://rokmp.de/de/churches/hram-ikony-kurskaya-korennaya/"
      ],
      "address": [
        "Judenhof 9, 89073 Ulm"
      ]
    },
    {
      "id": "de-mp-ulm-kirchengemeinde-d-hll-valentin-und-pasikratus",
      "parent": "ru-berlin-and-germany",
      "kind": "parish",
      "rank": "Parish",
      "name": "Russian Orthodox Parish d. Hll. Valentine and Pasikratus",
      "local": "Kirchengemeinde d. Hll. Valentin und Pasikratus",
      "country": "DE",
      "sources": [
        "https://rokmp.de/de/churches/kirchengemeinde-d-hll-valentin-und-pasikratus/"
      ]
    },
    {
      "id": "de-mp-weimar-hl-maria-magdalena-kirche",
      "parent": "ru-berlin-and-germany",
      "kind": "parish",
      "rank": "Parish",
      "name": "Russian Orthodox St. Mary Magdalene Church",
      "local": "Hl.-Maria-Magdalena-Kirche",
      "country": "DE",
      "sources": [
        "https://rokmp.de/de/churches/hram-ravnoap-marii-magdalinyi/"
      ],
      "address": [
        "Auf dem historischen Friedhof neben der Fürstengruft, D-99423 Weimar/Thüringen (Deutschland)"
      ]
    },
    {
      "id": "de-mp-wertheim-gemeinde-zu-ehren-der-hl-grossmartyrerin-irina",
      "parent": "ru-berlin-and-germany",
      "kind": "parish",
      "rank": "Parish",
      "name": "Russian Orthodox Parish in honor of St. Great Martyr Irina",
      "local": "Gemeinde zu Ehren der hl. Großmärtyrerin Irina",
      "country": "DE",
      "sources": [
        "https://rokmp.de/de/churches/obshhina-vmts-irinyi/"
      ],
      "address": [
        "Willi-Brand-Str. 1 97877 Wertheim"
      ]
    },
    {
      "id": "de-mp-worms-russische-orthodoxe-gemeinde-zu-ehren-der-drei-hierarchen-basilius-der-grosse-greg",
      "parent": "ru-berlin-and-germany",
      "kind": "parish",
      "rank": "Parish",
      "name": "Russian Orthodox Russian Orthodox community in honor of the Three Hierarchs Basil the Great, Gregory the Theologian and John Chrysostom",
      "local": "Russische Orthodoxe Gemeinde zu Ehren der Drei Hierarchen Basilius der Große, Gregorius der Theologe und Johannes Chrysostomus",
      "country": "DE",
      "sources": [
        "https://rokmp.de/de/churches/russische-orthodoxe-gemeinde-zu-ehren-der-drei-hierarchen-basilius-der-grose-gregorius-der-theologe-und-johannes-chrysostomus/"
      ],
      "address": [
        "Heidenturmkirche St. Paulus, Paulusplatz 2-4, 67547 Worms, Германия"
      ]
    },
    {
      "id": "de-mp-wuppertal-gemeinde-d-hll-neumartyrerinnen-grossfurstin-elisabeth-und-nonne-warwara",
      "parent": "ru-berlin-and-germany",
      "kind": "parish",
      "rank": "Parish",
      "name": "Russian Orthodox community d. Hll. New martyrs Grand Duchess Elisabeth and nun Warwara",
      "local": "Gemeinde d. Hll. Neumärtyrerinnen Großfürstin Elisabeth und Nonne Warwara",
      "country": "DE",
      "sources": [
        "https://rokmp.de/de/churches/prihod-prmtsts-vel-kn-elisavetyi-i-inokini-varvaryi/"
      ],
      "address": [
        "St. Anna Kapelle bei Kliniken St. Antonius, Vogelsangstrasse 106, 42109 Wuppertal"
      ]
    },
    {
      "id": "de-mp-wurzburg-kirche-zur-verkundigung-an-die-allheilige-gottesgebarerin",
      "parent": "ru-berlin-and-germany",
      "kind": "parish",
      "rank": "Parish",
      "name": "Russian Orthodox Church of the Annunciation to the All Holy Theotokos",
      "local": "Kirche zur Verkündigung an die Allheilige Gottesgebärerin",
      "country": "DE",
      "sources": [
        "https://rokmp.de/de/churches/prihod-blagoveshheniya-presvyatoy-bogoroditsyi/"
      ],
      "address": [
        "Zeller Straße 45, 97082 Würzburg"
      ]
    }
  ],
  "ru-germany-rocor": [
    {
      "id": "de-rocor-alzey-gemeinde-der-hl-gottgeweihten-grossfurstin-elisabeth",
      "parent": "ru-germany-rocor",
      "kind": "parish",
      "rank": "Parish",
      "name": "ROCOR Parish of the Holy Grand Duchess Elisabeth",
      "local": "Gemeinde der Hl. Gottgeweihten Großfürstin Elisabeth",
      "country": "DE",
      "sources": [
        "https://rocor.de/kirche/gemeinde-grossfuerstin-elisabeth-alzey"
      ],
      "address": [
        "Kirchenplatz 7, 55232 Alzey"
      ],
      "site": "https://pravoslav-kirche-alzey.de/de/herzlich-willkommen/"
    },
    {
      "id": "de-rocor-amberg-gemeinde-der-hll-apostel-peter-und-paul",
      "parent": "ru-germany-rocor",
      "kind": "parish",
      "rank": "Parish",
      "name": "ROCOR Parish of St. Apostles Peter and Paul",
      "local": "Gemeinde der Hll. Apostel Peter und Paul",
      "country": "DE",
      "sources": [
        "https://rocor.de/kirche/kirche-apostel-peter-paul-amberg"
      ],
      "address": [
        "Breslauer Straße 15, 92224 Amberg"
      ],
      "site": "https://peter-paul-roka.de"
    },
    {
      "id": "de-rocor-augsburg-gemeinde-der-gottesmutterikone-freude-aller-trauernden",
      "parent": "ru-germany-rocor",
      "kind": "parish",
      "rank": "Parish",
      "name": "ROCOR Parish of the Icon of the Mother of God \"Joy of All Who Sorrow\"",
      "local": "Gemeinde der Gottesmutterikone \"Freude aller Trauernden\"",
      "country": "DE",
      "sources": [
        "https://rocor.de/kirche/kirche-gottesmutter-freude-trauernden-augsburg"
      ],
      "address": [
        "Stadtberger Str. 26a, 86157 Augsburg"
      ],
      "site": "https://www.rocor-augsburg.de"
    },
    {
      "id": "de-rocor-bad-ems-gemeinde-der-hl-neumartyrerin-zarin-alexandra",
      "parent": "ru-germany-rocor",
      "kind": "parish",
      "rank": "Parish",
      "name": "ROCOR Parish of St. New Martyr Tsarina Alexandra",
      "local": "Gemeinde der hl. Neumärtyrerin Zarin Alexandra",
      "country": "DE",
      "sources": [
        "https://rocor.de/kirche/kirche-hl-alexandra-bad-ems"
      ],
      "address": [
        "Wilhelmsallee 12, 56130 Bad Ems"
      ],
      "site": "http://www.ruskirche-bad-ems.de/"
    },
    {
      "id": "de-rocor-bad-homburg-vor-der-hohe-gemeinde-aller-heiligen",
      "parent": "ru-germany-rocor",
      "kind": "parish",
      "rank": "Parish",
      "name": "ROCOR Parish of All Saints",
      "local": "Gemeinde Aller Heiligen",
      "country": "DE",
      "sources": [
        "https://rocor.de/kirche/allerheiligen-kirche-bad-homburg"
      ],
      "address": [
        "Kaiser-Friedrich-Promenade, 61348 Bad Homburg vor der Höhe"
      ]
    },
    {
      "id": "de-rocor-bad-kissingen-gemeinde-des-hl-sergij-von-radonezh",
      "parent": "ru-germany-rocor",
      "kind": "parish",
      "rank": "Parish",
      "name": "ROCOR Parish of St. Sergius of Radonezh",
      "local": "Gemeinde des Hl. Sergij von Radonezh",
      "country": "DE",
      "sources": [
        "https://rocor.de/kirche/kirche-hl-sergius-radonezh-bad-kissingen"
      ],
      "address": [
        "Salinenstrasse 20, 97688 Bad Kissingen"
      ],
      "site": "https://www.orthodox-kissingen.de"
    },
    {
      "id": "de-rocor-bad-nauheim-gemeinde-der-hll-innokentios-und-seraphim-von-sarov",
      "parent": "ru-germany-rocor",
      "kind": "parish",
      "rank": "Parish",
      "name": "ROCOR Parish of St. Innokentios and Seraphim of Sarov",
      "local": "Gemeinde der Hll. Innokentios und Seraphim von Sarov",
      "country": "DE",
      "sources": [
        "https://rocor.de/kirche/kirche-innokentios-seraphim-bad-nauheim"
      ],
      "address": [
        "Reinhardstrasse 14., 61231 Bad Nauheim"
      ]
    },
    {
      "id": "de-rocor-baden-baden-gemeinde-der-verklarung-christi",
      "parent": "ru-germany-rocor",
      "kind": "parish",
      "rank": "Parish",
      "name": "ROCOR Parish of the Transfiguration of Christ",
      "local": "Gemeinde der Verklärung Christi",
      "country": "DE",
      "sources": [
        "https://rocor.de/kirche/christi-verklaerungskirche-baden-baden"
      ],
      "address": [
        "Lichtentaler Straße 76, 76530 Baden-Baden"
      ],
      "site": "https://rok-baden-baden.de"
    },
    {
      "id": "de-rocor-berlin-gemeinde-maria-schutz",
      "parent": "ru-germany-rocor",
      "kind": "parish",
      "rank": "Parish",
      "name": "ROCOR Parish of Maria Schutz",
      "local": "Gemeinde Maria Schutz",
      "country": "DE",
      "sources": [
        "https://rocor.de/kirche/pokrov-kirche-berlin"
      ],
      "address": [
        "Wintersteinstraße 24, 10587 Berlin"
      ],
      "site": "https://www.pokrov.de"
    },
    {
      "id": "de-rocor-bielefeld-gemeinde-der-verklarung-christi",
      "parent": "ru-germany-rocor",
      "kind": "parish",
      "rank": "Parish",
      "name": "ROCOR Parish of the Transfiguration of Christ",
      "local": "Gemeinde der Verklärung Christi",
      "country": "DE",
      "sources": [
        "https://rocor.de/kirche/christi-verklaerungskirche-bielefeld"
      ],
      "address": [
        "Am Beckhof 18, 33689 Bielefeld"
      ],
      "site": "https://russische-kirche-bielefeld.de"
    },
    {
      "id": "de-rocor-bochum-gemeinde-des-hl-grossmartyrers-georg",
      "parent": "ru-germany-rocor",
      "kind": "parish",
      "rank": "Parish",
      "name": "ROCOR Parish of St. Great Martyr George",
      "local": "Gemeinde des hl. Großmärtyrers Georg",
      "country": "DE",
      "sources": [
        "https://rocor.de/kirche/kirche-hl-georg-bochum"
      ],
      "address": [
        "Feldsieperstr. 129, 44809 Bochum"
      ],
      "site": "https://orthodox-bochum.de"
    },
    {
      "id": "de-rocor-buchendorf-frauenkloster-der-hl-gottgeweihten-grossfurstin-elisabeth",
      "parent": "ru-germany-rocor",
      "kind": "monastery",
      "rank": "Monastery",
      "name": "ROCOR Women's monastery of the Holy Grand Duchess Elisabeth",
      "local": "Frauenkloster der Hl. Gottgeweihten Großfürstin Elisabeth",
      "country": "DE",
      "sources": [
        "https://rocor.de/kirche/frauenkloster-hl-elisabeth-buchendorf"
      ],
      "address": [
        "Forstenrieder-Park-Str. 2, 82131 Buchendorf"
      ],
      "site": "http://www.orth-frauenkloster.de/"
    },
    {
      "id": "de-rocor-cloppenburg-gemeinde-des-hl-seraphim-von-sarov",
      "parent": "ru-germany-rocor",
      "kind": "parish",
      "rank": "Parish",
      "name": "ROCOR Parish of St. Seraphim of Sarov",
      "local": "Gemeinde des hl. Seraphim von Sarov",
      "country": "DE",
      "sources": [
        "https://rocor.de/kirche/kirche-hl-seraphim-sarov-cloppenburg"
      ],
      "address": [
        "Brookweg 26, 49661 Cloppenburg"
      ],
      "site": "https://www.roka-cloppenburg.de"
    },
    {
      "id": "de-rocor-cottbus-gemeinde-des-hl-johannes-von-shanghai-und-san-francisco",
      "parent": "ru-germany-rocor",
      "kind": "parish",
      "rank": "Parish",
      "name": "ROCOR Parish of St. John of Shanghai and San Francisco",
      "local": "Gemeinde des Hl. Johannes von Shanghai und San Francisco",
      "country": "DE",
      "sources": [
        "https://rocor.de/kirche/gemeinde-hl-johannes-shanghai-cottbus"
      ],
      "address": [
        "Virchowstr.41, 03044 Cottbus"
      ],
      "site": "https://www.cottbus-orthodox.de"
    },
    {
      "id": "de-rocor-darmstadt-mathildenhohe-gemeinde-der-hl-maria-magdalena",
      "parent": "ru-germany-rocor",
      "kind": "parish",
      "rank": "Parish",
      "name": "ROCOR Parish of St. Mary Magdalene",
      "local": "Gemeinde der Hl. Maria Magdalena",
      "country": "DE",
      "sources": [
        "https://rocor.de/kirche/kirche-hl-maria-magdalena-darmstadt"
      ],
      "address": [
        "Nikolaiweg 18, 64287 Darmstadt-Mathildenhöhe"
      ],
      "site": "http://darmstadt-church.de/"
    },
    {
      "id": "de-rocor-deggendorf-gemeinde-des-hl-panteleimon",
      "parent": "ru-germany-rocor",
      "kind": "parish",
      "rank": "Parish",
      "name": "ROCOR Parish of St. Panteleimon",
      "local": "Gemeinde des Hl. Panteleimon",
      "country": "DE",
      "sources": [
        "https://rocor.de/kirche/gemeinde-hl-panteleimon-deggendorf"
      ],
      "address": [
        "Haselbeck Straße 6, 94469 Deggendorf"
      ]
    },
    {
      "id": "de-rocor-dingolfing-gemeinde-aller-heiligen",
      "parent": "ru-germany-rocor",
      "kind": "parish",
      "rank": "Parish",
      "name": "ROCOR Parish of All Saints",
      "local": "Gemeinde Aller Heiligen",
      "country": "DE",
      "sources": [
        "https://rocor.de/kirche/gemeinde-allerheiligen-dingolfing"
      ],
      "address": [
        "Brunn, 84130 Dingolfing"
      ]
    },
    {
      "id": "de-rocor-duren-gemeinde-der-hl-anna",
      "parent": "ru-germany-rocor",
      "kind": "parish",
      "rank": "Parish",
      "name": "ROCOR Parish of St. Anne",
      "local": "Gemeinde der Hl. Anna",
      "country": "DE",
      "sources": [
        "https://rocor.de/kirche/anna-gemeinde-dueren"
      ],
      "address": [
        "Bismarck Str. 24, 52351 Düren"
      ],
      "site": "https://rok-sanktanna-dueren.de"
    },
    {
      "id": "de-rocor-engen-gemeinde-der-gottesmutterikone-freude-aller-trauernden",
      "parent": "ru-germany-rocor",
      "kind": "parish",
      "rank": "Parish",
      "name": "ROCOR Parish of the Icon of the Mother of God \"Joy of All Who Sorrow\"",
      "local": "Gemeinde der Gottesmutterikone \"Freude aller Trauernden\"",
      "country": "DE",
      "sources": [
        "https://rocor.de/kirche/kirche-gottesmutter-freude-trauernden-engen"
      ],
      "address": [
        "Jahnstr. 3a, 78234 Engen"
      ],
      "site": "https://roka-engen.usite.pro"
    },
    {
      "id": "de-rocor-erlangen-gemeinde-der-allheiligen-dreiheit",
      "parent": "ru-germany-rocor",
      "kind": "parish",
      "rank": "Parish",
      "name": "ROCOR Parish of the All Holy Trinity",
      "local": "Gemeinde der Allheiligen Dreiheit",
      "country": "DE",
      "sources": [
        "https://rocor.de/kirche/dreifaltigkeitskirche-erlangen"
      ],
      "address": [
        "Stintzingstr. 20, 91058 Erlangen"
      ],
      "site": "https://orthodoxe-kirche-erlangen.de/de/"
    },
    {
      "id": "de-rocor-ettringen-gemeinde-der-hll-fides-spes-caritas-und-sophia",
      "parent": "ru-germany-rocor",
      "kind": "parish",
      "rank": "Parish",
      "name": "ROCOR Parish of St. Fides, Spes, Caritas and Sophia",
      "local": "Gemeinde der Hll. Fides, Spes, Caritas und Sophia",
      "country": "DE",
      "sources": [
        "https://rocor.de/kirche/gemeinde-vera-nadezhda-ljubov-ettringen"
      ],
      "address": [
        "Friedhofweg 1, 86833 Ettringen"
      ],
      "site": "http://rocor-ettringen.de/?lang=de"
    },
    {
      "id": "de-rocor-flensburg-gemeinde-des-hl-prokopij",
      "parent": "ru-germany-rocor",
      "kind": "parish",
      "rank": "Parish",
      "name": "ROCOR Parish of St. Prokopij",
      "local": "Gemeinde des hl. Prokopij",
      "country": "DE",
      "sources": [
        "https://rocor.de/kirche/gemeinde-apostel-peter-paul-flensburg"
      ],
      "address": [
        "Bauer Landstraße 17, 24534 Flensburg"
      ],
      "site": "https://prokopij.de/flindex_de.html"
    },
    {
      "id": "de-rocor-frankfurt-hausen-gemeinde-des-hl-nikolaus-von-myra",
      "parent": "ru-germany-rocor",
      "kind": "parish",
      "rank": "Parish",
      "name": "ROCOR Parish of St. Nicholas of Myra",
      "local": "Gemeinde des Hl. Nikolaus von Myra",
      "country": "DE",
      "sources": [
        "https://rocor.de/kirche/kirche-hl-nikolaus-frankfurt"
      ],
      "address": [
        "Am Industriehof 18, 60487 Frankfurt-Hausen"
      ],
      "site": "http://www.svnikolay.com/?lang=de-DE"
    },
    {
      "id": "de-rocor-freudenstadt-gemeinde-der-hl-ephrosinia-grossfurstin-von-moskau",
      "parent": "ru-germany-rocor",
      "kind": "parish",
      "rank": "Parish",
      "name": "ROCOR Parish of St. Ephrosinia, Grand Duchess of Moscow",
      "local": "Gemeinde der hl. Ephrosinia, Großfürstin von Moskau",
      "country": "DE",
      "sources": [
        "https://rocor.de/kirche/kirche-hl-ephrosinia-freudenstadt"
      ],
      "address": [
        "Parkweg 13, 72250 Freudenstadt"
      ],
      "site": "http://russische-orthodoxe-kirche-freudenstadt.de/"
    },
    {
      "id": "de-rocor-gerolstein-gemeinde-des-hl-athanasius-von-alexandria",
      "parent": "ru-germany-rocor",
      "kind": "parish",
      "rank": "Parish",
      "name": "ROCOR Parish of St. Athanasius of Alexandria",
      "local": "Gemeinde des Hl. Athanasius von Alexandria",
      "country": "DE",
      "sources": [
        "https://rocor.de/kirche/gemeinde-hl-athanasius-gerolstein"
      ],
      "address": [
        "Sarresdorfer Str. 19, 54568 Gerolstein"
      ],
      "site": "https://eifel-orthodox.de"
    },
    {
      "id": "de-rocor-gronau-gemeinde-der-einfuhrung-der-allreinen-gottesmutter-in-den-tempel",
      "parent": "ru-germany-rocor",
      "kind": "parish",
      "rank": "Parish",
      "name": "ROCOR Congregation of the Introduction of the All-Pure Mother of God into the Temple in den Tempel",
      "local": "Gemeinde der Einführung der Allreinen Gottesmutter in den Tempel",
      "country": "DE",
      "sources": [
        "https://rocor.de/kirche/einfuehrung-der-allreinen-gottesmutter-in-den-tempel"
      ],
      "address": [
        "Steinstraße 60, 48599 Gronau"
      ],
      "site": "https://pravoslavievgronau.tilda.ws/page"
    },
    {
      "id": "de-rocor-hamburg-gemeinde-des-hl-prokopij",
      "parent": "ru-germany-rocor",
      "kind": "parish",
      "rank": "Parish",
      "name": "ROCOR Parish of St. Procopius",
      "local": "Gemeinde des Hl. Prokopij",
      "country": "DE",
      "sources": [
        "https://rocor.de/kirche/kirche-hl-prokopij-ustjug-hamburg"
      ],
      "address": [
        "Hagenbeckstraße 10, 22527 Hamburg"
      ],
      "site": "https://www.prokopij.de/index_de.html"
    },
    {
      "id": "de-rocor-hannover-gemeinde-der-geburt-christi",
      "parent": "ru-germany-rocor",
      "kind": "parish",
      "rank": "Parish",
      "name": "ROCOR Church of the Nativity",
      "local": "Gemeinde der Geburt Christi",
      "country": "DE",
      "sources": [
        "https://rocor.de/kirche/christi-geburt-gemeinde-hannover"
      ],
      "address": [
        "Plüschowstr 6, 30163 Hannover"
      ],
      "site": "https://christi-geburt-gemeinde.de/ru/"
    },
    {
      "id": "de-rocor-hannover-gemeinde-der-gottesmutterikone-von-kursk",
      "parent": "ru-germany-rocor",
      "kind": "parish",
      "rank": "Parish",
      "name": "ROCOR Parish of the Icon of the Mother of God \"of Kursk\"",
      "local": "Gemeinde der Gottesmutterikone \"von Kursk\"",
      "country": "DE",
      "sources": [
        "https://rocor.de/kirche/kirche-gottesmutter-kurskaja-hannover"
      ],
      "address": [
        "Königsworther Straße 12, 30167 Hannover"
      ],
      "site": "http://www.ruskirche-hannover.de/"
    },
    {
      "id": "de-rocor-hildesheim-gemeinde-der-gottesmutterikone-necajannaja-radost",
      "parent": "ru-germany-rocor",
      "kind": "parish",
      "rank": "Parish",
      "name": "ROCOR Parish of the Icon of Our Lady \"Nečajannaja Radost'\"",
      "local": "Gemeinde der Gottesmutterikone \"Nečajannaja Radost'\"",
      "country": "DE",
      "sources": [
        "https://rocor.de/kirche/orthodoxe-gemeinde-hildesheim"
      ],
      "address": [
        "Stiftskirchenweg 5, 31139 Hildesheim"
      ],
      "site": "https://hram-hildesheim.de"
    },
    {
      "id": "de-rocor-homburg-gemeinde-der-hl-olga",
      "parent": "ru-germany-rocor",
      "kind": "parish",
      "rank": "Parish",
      "name": "ROCOR Parish of St. Olga",
      "local": "Gemeinde der Hl. Olga",
      "country": "DE",
      "sources": [
        "https://rocor.de/kirche/gemeinde-hl-olga-homburg"
      ],
      "address": [
        "Bodelschwinghstr. 5, 66424 Homburg"
      ]
    },
    {
      "id": "de-rocor-idar-oberstein-gemeinde-des-hl-johannes-von-shanghai-und-san-francisco",
      "parent": "ru-germany-rocor",
      "kind": "parish",
      "rank": "Parish",
      "name": "ROCOR Parish of St. John of Shanghai and San Francisco",
      "local": "Gemeinde des Hl. Johannes von Shanghai und San Francisco",
      "country": "DE",
      "sources": [
        "https://rocor.de/kirche/gemeinde-hl-johannes-shanghai-idar-oberstein"
      ],
      "address": [
        "Hauptstr. 317, 55743 Idar-Oberstein"
      ]
    },
    {
      "id": "de-rocor-ingolstadt-gemeinde-des-hl-nikolaus-von-myra",
      "parent": "ru-germany-rocor",
      "kind": "parish",
      "rank": "Parish",
      "name": "ROCOR Parish of St. Nicholas of Myra",
      "local": "Gemeinde des Hl. Nikolaus von Myra",
      "country": "DE",
      "sources": [
        "https://rocor.de/kirche/hl-nikolaus-kirche-ingolstadt"
      ],
      "address": [
        "Esplanade 38, 85049 Ingolstadt"
      ],
      "site": "https://rocor-ingolstadt.de"
    },
    {
      "id": "de-rocor-karlsruhe-gemeinde-des-hl-johannes-von-shanghai-und-san-francisco",
      "parent": "ru-germany-rocor",
      "kind": "parish",
      "rank": "Parish",
      "name": "ROCOR Parish of St. John of Shanghai and San Francisco",
      "local": "Gemeinde des Hl. Johannes von Shanghai und San Francisco",
      "country": "DE",
      "sources": [
        "https://rocor.de/kirche/kirche-hl-johannes-shanghai-karlsruhe"
      ],
      "address": [
        "Bernhard-Lichtenberg-Straße 46, 76189 Karlsruhe"
      ]
    },
    {
      "id": "de-rocor-kassel-gemeinde-des-hl-panteleimon",
      "parent": "ru-germany-rocor",
      "kind": "parish",
      "rank": "Parish",
      "name": "ROCOR Parish of St. Panteleimon",
      "local": "Gemeinde des Hl. Panteleimon",
      "country": "DE",
      "sources": [
        "https://rocor.de/kirche/gemeinde-hl-panteleimon-kassel"
      ],
      "address": [
        "Renthof, 34121 Kassel"
      ]
    },
    {
      "id": "de-rocor-kirchheim-unter-teck-gemeinde-der-hll-kyrill-und-method",
      "parent": "ru-germany-rocor",
      "kind": "parish",
      "rank": "Parish",
      "name": "ROCOR Parish of St. Cyril and Methodius",
      "local": "Gemeinde der Hll. Kyrill und Method",
      "country": "DE",
      "sources": [
        "https://rocor.de/kirche/gemeinde-kyrill-methodius-kirchheim"
      ],
      "address": [
        "Limburgerstr. 65, 73230 Kirchheim unter Teck"
      ],
      "site": "https://rok-kirchheim-teck.de/"
    },
    {
      "id": "de-rocor-koln-gemeinde-des-hl-panteleimon",
      "parent": "ru-germany-rocor",
      "kind": "parish",
      "rank": "Parish",
      "name": "ROCOR Parish of St. Panteleimon",
      "local": "Gemeinde des Hl. Panteleimon",
      "country": "DE",
      "sources": [
        "https://rocor.de/kirche/gemeinde-hl-panteleimon-koeln"
      ],
      "address": [
        "Neue Str. 1, 51149 Köln"
      ],
      "site": "https://rocor.koeln"
    },
    {
      "id": "de-rocor-landshut-gemeinde-des-hl-nikolaus-von-myra",
      "parent": "ru-germany-rocor",
      "kind": "parish",
      "rank": "Parish",
      "name": "ROCOR Parish of St. Nicholas of Myra",
      "local": "Gemeinde des Hl. Nikolaus von Myra",
      "country": "DE",
      "sources": [
        "https://rocor.de/kirche/hl-nikolaus-gemeinde-landshut"
      ],
      "address": [
        "Regierungsplatz 541, 84028 Landshut"
      ]
    },
    {
      "id": "de-rocor-lauingen-donau-gemeinde-der-heiligen-martyrin-afra-in-lauingen",
      "parent": "ru-germany-rocor",
      "kind": "parish",
      "rank": "Parish",
      "name": "ROCOR Parish of the Holy Martyr Afra in Lauingen",
      "local": "Gemeinde der heiligen Märtyrin Afra in Lauingen",
      "country": "DE",
      "sources": [
        "https://rocor.de/kirche/---"
      ],
      "address": [
        "Johannesstrasse 5, 89415 Lauingen (Donau)"
      ],
      "site": "https://rocor-dillingen-donau.de/"
    },
    {
      "id": "de-rocor-lubeck-gemeinde-des-hl-prokopij",
      "parent": "ru-germany-rocor",
      "kind": "parish",
      "rank": "Parish",
      "name": "ROCOR Parish of St. Procopius",
      "local": "Gemeinde des Hl. Prokopij",
      "country": "DE",
      "sources": [
        "https://rocor.de/kirche/kirche-hl-prokopij-ustijug-luebeck"
      ],
      "address": [
        "Glockengiesserst.2, 23552 Lübeck"
      ],
      "site": "https://www.prokopij-luebeck.de"
    },
    {
      "id": "de-rocor-malmo-gemeinde-der-gottesmutterikone-von-kursk",
      "parent": "ru-germany-rocor",
      "kind": "parish",
      "rank": "Parish",
      "name": "ROCOR Parish of the Icon of the Mother of God \"of Kursk\"",
      "local": "Gemeinde der Gottesmutterikone \"von Kursk\"",
      "country": "DE",
      "sources": [
        "https://rocor.de/kirche/orthodoxe-kirche-malmoe-schweden"
      ],
      "address": [
        "Cedergatan 4, 21216 Malmö"
      ],
      "site": "https://www.heligeherman.se"
    },
    {
      "id": "de-rocor-mannheim-gemeinde-des-hl-alexander-von-der-newa",
      "parent": "ru-germany-rocor",
      "kind": "parish",
      "rank": "Parish",
      "name": "ROCOR Parish of St. Alexander of the Neva",
      "local": "Gemeinde des Hl. Alexander von der Newa",
      "country": "DE",
      "sources": [
        "https://rocor.de/kirche/kirche-hl-alexander-nevskij-mannheim"
      ],
      "address": [
        "Gärtnerst 10, 68169 Mannheim"
      ],
      "site": "https://russische-kirche-mannhem.de"
    },
    {
      "id": "de-rocor-memmingen-gemeinde-des-hl-johannes-v-euboa",
      "parent": "ru-germany-rocor",
      "kind": "parish",
      "rank": "Parish",
      "name": "ROCOR Parish of St. John V. Euboea",
      "local": "Gemeinde des Hl. Johannes v. Euböa",
      "country": "DE",
      "sources": [
        "https://rocor.de/kirche/gemeinde-hl-johannes-euboea-memmingen"
      ],
      "address": [
        "Eisenacher Weg 2, 87700 Memmingen"
      ]
    },
    {
      "id": "de-rocor-mendig-gemeinde-des-hl-lukas-von-simferopol-und-der-krim",
      "parent": "ru-germany-rocor",
      "kind": "parish",
      "rank": "Parish",
      "name": "ROCOR Parish of St. Luke of Simferopol and Crimea",
      "local": "Gemeinde des Hl. Lukas von Simferopol und der Krim",
      "country": "DE",
      "sources": [
        "https://rocor.de/kirche/gemeinde-hl-lukas-krim-mayen"
      ],
      "address": [
        "Heidenstockstr. 45, 56743 Mendig"
      ]
    },
    {
      "id": "de-rocor-merzig-gemeinde-des-hl-kyrill-von-kazan",
      "parent": "ru-germany-rocor",
      "kind": "parish",
      "rank": "Parish",
      "name": "ROCOR Parish of St. Cyril of Kazan",
      "local": "Gemeinde des Hl. Kyrill von Kazan",
      "country": "DE",
      "sources": [
        "https://rocor.de/kirche/gemeinde-des-hl-kyrill-von-kazan"
      ],
      "address": [
        "Am Gaswerk 9, 66663 Merzig"
      ]
    },
    {
      "id": "de-rocor-munchen-gemeinde-des-hl-apostel-thomas",
      "parent": "ru-germany-rocor",
      "kind": "parish",
      "rank": "Parish",
      "name": "ROCOR Parish of St. Thomas the Apostle",
      "local": "Gemeinde des Hl. Apostel Thomas",
      "country": "DE",
      "sources": [
        "https://rocor.de/kirche/gemeinde-hl-apostel-thomas-muenchen"
      ],
      "address": [
        "Paul-Heyse-Str. 19 Rgb, 80336 München"
      ],
      "site": "https://apostel-thomas-kirche.de"
    },
    {
      "id": "de-rocor-munchen-gemeinde-des-hl-erzengels-michael",
      "parent": "ru-germany-rocor",
      "kind": "parish",
      "rank": "Parish",
      "name": "ROCOR Parish of St. Archangel Michael",
      "local": "Gemeinde des Hl. Erzengels Michael",
      "country": "DE",
      "sources": [
        "https://rocor.de/kirche/kirche-hl-erzengel-michael-muenchen"
      ],
      "address": [
        "Achatstr. 14, 80995 München"
      ],
      "site": "https://amichaelskirche.de"
    },
    {
      "id": "de-rocor-munchen-kathedrale-der-hll-neumartyrer-und-bekenner-russlands-und-des-hl-nikolaus",
      "parent": "ru-germany-rocor",
      "kind": "parish",
      "rank": "Parish",
      "name": "ROCOR Cathedral of St. New Martyrs and Confessors of Russia and St. Nicholas",
      "local": "Kathedrale der Hll. Neumärtyrer und Bekenner Russlands und des Hl. Nikolaus",
      "country": "DE",
      "sources": [
        "https://rocor.de/kirche/kathedrale-neomaertyrer-nikolaus-muenchen"
      ],
      "address": [
        "Lincolnstraße 58, 81549 München"
      ],
      "site": "https://sobor.de"
    },
    {
      "id": "de-rocor-munchen-obermenzing-diozesanverwaltung",
      "parent": "ru-germany-rocor",
      "kind": "parish",
      "rank": "Parish",
      "name": "ROCOR Diocesan administration",
      "local": "Diözesanverwaltung",
      "country": "DE",
      "sources": [
        "https://rocor.de/kirche/dioezesanverwaltung-muenchen"
      ],
      "address": [
        "Hofbauernstr. 26, 81247 München-Obermenzing"
      ]
    },
    {
      "id": "de-rocor-munchen-obermenzing-kloster-des-hl-hiob-von-pocaev",
      "parent": "ru-germany-rocor",
      "kind": "monastery",
      "rank": "Monastery",
      "name": "ROCOR Monastery of St. Job of Počaev",
      "local": "Kloster des Hl. Hiob von Počaev",
      "country": "DE",
      "sources": [
        "https://rocor.de/kirche/kloster-hl-hiob-pocaev-muenchen"
      ],
      "address": [
        "Hofbauernstr. 26, 81247 München-Obermenzing"
      ],
      "site": "https://www.hiobmon.org/"
    },
    {
      "id": "de-rocor-munster-gemeinde-der-gottesmutterikone-von-kazan",
      "parent": "ru-germany-rocor",
      "kind": "parish",
      "rank": "Parish",
      "name": "ROCOR Parish of the Icon of the Mother of God \"of Kazan\"",
      "local": "Gemeinde der Gottesmutterikone \"von Kazan\"",
      "country": "DE",
      "sources": [
        "https://rocor.de/kirche/gemeinde-gottesmutter-kazan-muenster"
      ],
      "address": [
        "Osttor 81, 48165 Münster"
      ],
      "site": "https://rocor-muenster.de"
    },
    {
      "id": "de-rocor-neckarsulm-gemeinde-des-hl-johannes-von-shanghai-und-san-francisco",
      "parent": "ru-germany-rocor",
      "kind": "parish",
      "rank": "Parish",
      "name": "ROCOR Parish of St. John of Shanghai and San Francisco",
      "local": "Gemeinde des Hl. Johannes von Shanghai und San Francisco",
      "country": "DE",
      "sources": [
        "https://rocor.de/kirche/gemeinde-hl-johannes-heilbronn"
      ],
      "address": [
        "Brahmsweg 2, 74172 Neckarsulm"
      ],
      "site": "https://rus-kirche-heilbronn.de"
    },
    {
      "id": "de-rocor-neumunster-gemeinde-der-allheiligen-dreiheit",
      "parent": "ru-germany-rocor",
      "kind": "parish",
      "rank": "Parish",
      "name": "ROCOR Parish of the All Holy Trinity",
      "local": "Gemeinde der Allheiligen Dreiheit",
      "country": "DE",
      "sources": [
        "https://rocor.de/kirche/dreifaltigkeitskirche-neumuenster"
      ],
      "address": [
        "Prehnsfelder Weg 1, 24537 Neumünster"
      ],
      "site": "https://prokopij.de/neumindex_de.html"
    },
    {
      "id": "de-rocor-nurnberg-gemeinde-der-geburt-der-gottesmutter-maria",
      "parent": "ru-germany-rocor",
      "kind": "parish",
      "rank": "Parish",
      "name": "ROCOR Parish of the Nativity of the Mother of God",
      "local": "Gemeinde der Geburt der Gottesmutter Maria",
      "country": "DE",
      "sources": [
        "https://rocor.de/kirche/gemeinde-gottesmutter-geburt-nuernberg"
      ],
      "address": [
        "Saalfelder Straße 12, 90491 Nürnberg"
      ],
      "site": "https://www.nuernberg.cerkov.ru"
    },
    {
      "id": "de-rocor-oldenburg-gemeinde-maria-schutz",
      "parent": "ru-germany-rocor",
      "kind": "parish",
      "rank": "Parish",
      "name": "ROCOR Parish of Maria Schutz",
      "local": "Gemeinde Maria Schutz",
      "country": "DE",
      "sources": [
        "https://rocor.de/kirche/maria-schutz-kirche-oldenburg"
      ],
      "address": [
        "Bauordenstraße 70, 26133 Oldenburg"
      ],
      "site": "https://orthodox-oldenburg.de"
    },
    {
      "id": "de-rocor-peine-gemeinde-der-gottesmutterikone-skoroposlushnica",
      "parent": "ru-germany-rocor",
      "kind": "parish",
      "rank": "Parish",
      "name": "ROCOR Parish of the Icon of Our Lady \"Skoroposlushnica\"",
      "local": "Gemeinde der Gottesmutterikone \"Skoroposlushnica\"",
      "country": "DE",
      "sources": [
        "https://rocor.de/kirche/gemeinde-der-gottesmutterikone-skoroposlushnica"
      ],
      "address": [
        "Martin-Luther-Straße 7, 31228 Peine"
      ],
      "site": "http://ruskirche-peine.de"
    },
    {
      "id": "de-rocor-petershagen-gemeinde-des-hl-grossfursten-wladimir",
      "parent": "ru-germany-rocor",
      "kind": "parish",
      "rank": "Parish",
      "name": "ROCOR Parish of St. Grand Duke Vladimir",
      "local": "Gemeinde des hl. Großfürsten Wladimir",
      "country": "DE",
      "sources": [
        "https://rocor.de/kirche/gemeinde-hl-vladimir-minden"
      ],
      "address": [
        "Schulstraße 7, 32469 Petershagen"
      ],
      "site": "http://www.russische-orthodoxe-kirche-in-minden.de/"
    },
    {
      "id": "de-rocor-ravensburg-gemeinde-des-hl-ignatij-vom-kaukasus",
      "parent": "ru-germany-rocor",
      "kind": "parish",
      "rank": "Parish",
      "name": "ROCOR Parish of St. Ignatius of the Caucasus",
      "local": "Gemeinde des Hl. Ignatij vom Kaukasus",
      "country": "DE",
      "sources": [
        "https://rocor.de/kirche/--"
      ],
      "address": [
        "Abteistr 2, 88214 Ravensburg"
      ],
      "site": "https://weingarten-orthodox-pravoslavnaja.cerkov.ru/"
    },
    {
      "id": "de-rocor-regensburg-gemeinde-maria-schutz",
      "parent": "ru-germany-rocor",
      "kind": "parish",
      "rank": "Parish",
      "name": "ROCOR Parish of Maria Schutz",
      "local": "Gemeinde Maria Schutz",
      "country": "DE",
      "sources": [
        "https://rocor.de/kirche/maria-schutz-kirche-regensburg"
      ],
      "address": [
        "Prüfeninger Str.18, 93049 Regensburg"
      ],
      "site": "https://www.pokrova.de"
    },
    {
      "id": "de-rocor-reutlingen-gemeinde-des-entschlafens-der-gottesmutter-maria",
      "parent": "ru-germany-rocor",
      "kind": "parish",
      "rank": "Parish",
      "name": "ROCOR Parish of the Dormition of Mary, Mother of God",
      "local": "Gemeinde des Entschlafens der Gottesmutter Maria",
      "country": "DE",
      "sources": [
        "https://rocor.de/kirche/gemeinde-mariae-entschlafung-reutlingen"
      ],
      "address": [
        "Nikolaiplatz 1, 72764 Reutlingen"
      ],
      "site": "https://www.rok-reutlingen.de/"
    },
    {
      "id": "de-rocor-roding-gemeinde-des-hl-spyridon",
      "parent": "ru-germany-rocor",
      "kind": "parish",
      "rank": "Parish",
      "name": "ROCOR Parish of St. Spyridon",
      "local": "Gemeinde des Hl. Spyridon",
      "country": "DE",
      "sources": [
        "https://rocor.de/kirche/gemeinde-hl-spyridon-roding"
      ],
      "address": [
        "Ludwigstr. 5, 93426 Roding"
      ],
      "site": "http://orthodox-roding.ucoz.de/"
    },
    {
      "id": "de-rocor-rosenheim-gemeinde-der-gottesmutterikone-von-iveron",
      "parent": "ru-germany-rocor",
      "kind": "parish",
      "rank": "Parish",
      "name": "ROCOR Parish of the Iveron Mother of God icon",
      "local": "Gemeinde der Gottesmutterikone \"von Iveron\"",
      "country": "DE",
      "sources": [
        "https://rocor.de/kirche/gemeinde-gottesmutter-iwerskaja-rosenheim"
      ],
      "address": [
        "Kaiserstr. 48, 83022 Rosenheim"
      ]
    },
    {
      "id": "de-rocor-saarbrucken-gemeinde-der-hl-eugenia",
      "parent": "ru-germany-rocor",
      "kind": "parish",
      "rank": "Parish",
      "name": "ROCOR Parish of St. Eugenia",
      "local": "Gemeinde der Hl. Eugenia",
      "country": "DE",
      "sources": [
        "https://rocor.de/kirche/gemeinde-hl-eugenia-saarbruecken"
      ],
      "address": [
        "Lindenhofstr. 1, 66115 Saarbrücken"
      ],
      "site": "https://saar-orthodox.de"
    },
    {
      "id": "de-rocor-salzgitter-gemeinde-des-hl-nikolaus-von-myra",
      "parent": "ru-germany-rocor",
      "kind": "parish",
      "rank": "Parish",
      "name": "ROCOR Parish of St. Nicholas of Myra",
      "local": "Gemeinde des Hl. Nikolaus von Myra",
      "country": "DE",
      "sources": [
        "https://rocor.de/kirche/hl-nikolaus-kirche-salzgitter"
      ],
      "address": [
        "Posthof 16, 38226 Salzgitter"
      ],
      "site": "https://www.orthodox-salzgitter.com"
    },
    {
      "id": "de-rocor-schwabisch-gmund-gemeinde-des-hl-innokentij-von-irkutsk",
      "parent": "ru-germany-rocor",
      "kind": "parish",
      "rank": "Parish",
      "name": "ROCOR Parish of St. Innokenty of Irkutsk",
      "local": "Gemeinde des Hl. Innokentij von Irkutsk",
      "country": "DE",
      "sources": [
        "https://rocor.de/kirche/gemeinde-hl-innokentius-schwaebisch-gmuend"
      ],
      "address": [
        "Königsturmstraße 40, 73525 Schwäbisch Gmünd"
      ],
      "site": "https://russ-orth-kirche-gmuend.com"
    },
    {
      "id": "de-rocor-siegen-gemeinde-der-hl-neumartyrerin-zarin-alexandra",
      "parent": "ru-germany-rocor",
      "kind": "parish",
      "rank": "Parish",
      "name": "ROCOR Parish of the Holy New Martyr Tsarina Alexandra",
      "local": "Gemeinde der Hl. Neumärtyrerin Zarin Alexandra",
      "country": "DE",
      "sources": [
        "https://rocor.de/kirche/gemeinde-hl-alexandra-siegen"
      ],
      "address": [
        "Zwinglistr. 1, 57080 Siegen"
      ],
      "site": "https://pc-si.de/"
    },
    {
      "id": "de-rocor-straubing-gemeinde-der-geburt-des-hl-propheten-und-vorlaufers-johannes",
      "parent": "ru-germany-rocor",
      "kind": "parish",
      "rank": "Parish",
      "name": "ROCOR Parish of the Birth of St. Prophet and forerunner John",
      "local": "Gemeinde der Geburt des hl. Propheten und Vorläufers Johannes",
      "country": "DE",
      "sources": [
        "https://rocor.de/kirche/kirche-hl-johannes-taeufer-straubing"
      ],
      "address": [
        "Tilsiter Str.7, 94315 Straubing"
      ],
      "site": "https://pravmirstr.ucoz.ru/"
    },
    {
      "id": "de-rocor-stuttgart-gemeinde-des-hl-nikolaus-von-myra",
      "parent": "ru-germany-rocor",
      "kind": "parish",
      "rank": "Parish",
      "name": "ROCOR Parish of St. Nicholas of Myra",
      "local": "Gemeinde des Hl. Nikolaus von Myra",
      "country": "DE",
      "sources": [
        "https://rocor.de/kirche/hl-nikolaus-kirche-stuttgart"
      ],
      "address": [
        "Seidenstr. 69, 70174 Stuttgart"
      ],
      "site": "http://www.rok-stuttgart.de/index.php/de/"
    },
    {
      "id": "de-rocor-stuttgart-rotenberg-grabkapelle-der-hl-katharina",
      "parent": "ru-germany-rocor",
      "kind": "parish",
      "rank": "Chapel",
      "name": "ROCOR Grave chapel of St. Catherine",
      "local": "Grabkapelle der Hl. Katharina",
      "country": "DE",
      "sources": [
        "https://rocor.de/kirche/hl-katharine-grabkapelle-stuttgart"
      ],
      "address": [
        "Seidenstr. 69, 70174 Stuttgart-Rotenberg"
      ],
      "site": "https://www.rok-stuttgart.de"
    },
    {
      "id": "de-rocor-sudmoslesfehn-gemeinde-maria-schutz",
      "parent": "ru-germany-rocor",
      "kind": "parish",
      "rank": "Parish",
      "name": "ROCOR Parish of Maria Schutz",
      "local": "Gemeinde Maria Schutz",
      "country": "DE",
      "sources": [
        "https://rocor.de/kirche/gemeinde-gottesmutter-schutz-suedmoslesfehn"
      ],
      "address": [
        "Diedrich-Dannemann-Strasse 234, 26203 Südmoslesfehn"
      ],
      "site": "http://orthodox-oldenburg.de/index.php/de/"
    },
    {
      "id": "de-rocor-trier-kurenz-gemeinde-der-hll-konstantin-und-helena",
      "parent": "ru-germany-rocor",
      "kind": "parish",
      "rank": "Parish",
      "name": "ROCOR Parish of St. Constantine and Helena",
      "local": "Gemeinde der Hll. Konstantin und Helena",
      "country": "DE",
      "sources": [
        "https://rocor.de/kirche/gemeinde-konstantin-helena-konz"
      ],
      "address": [
        "Domänenstr, 54296 Trier-Kürenz"
      ],
      "site": "https://trier-orthodox.de"
    },
    {
      "id": "de-rocor-unterkirnach-schwarzwald-gemeinde-der-gottesmutterikone-von-kazan",
      "parent": "ru-germany-rocor",
      "kind": "parish",
      "rank": "Parish",
      "name": "ROCOR Parish of the Icon of the Mother of God \"of Kazan\"",
      "local": "Gemeinde der Gottesmutterikone \"von Kazan\"",
      "country": "DE",
      "sources": [
        "https://rocor.de/kirche/gemeinde-gottesmutter-kazan-unterkirnach"
      ],
      "address": [
        "Kirnachtal 3-5, 78089 Unterkirnach-Schwarzwald"
      ]
    },
    {
      "id": "de-rocor-weilheim-in-oberbayern-gemeinde-der-hl-katharina-von-alexandrien",
      "parent": "ru-germany-rocor",
      "kind": "parish",
      "rank": "Parish",
      "name": "ROCOR Parish of St. Catherine of Alexandria",
      "local": "Gemeinde der hl. Katharina von Alexandrien",
      "country": "DE",
      "sources": [
        "https://rocor.de/kirche/----"
      ],
      "address": [
        "Fischergasse 3, 82362 Weilheim in Oberbayern"
      ]
    },
    {
      "id": "de-rocor-wiesbaden-gemeinde-d-hl-elisabeth",
      "parent": "ru-germany-rocor",
      "kind": "parish",
      "rank": "Parish",
      "name": "ROCOR community d. St. Elizabeth",
      "local": "Gemeinde d. Hl. Elisabeth",
      "country": "DE",
      "sources": [
        "https://rocor.de/kirche/kirche-hl-elisabeth-wiesbaden"
      ],
      "address": [
        "Christian-Spielmann-Weg 1, 65193 Wiesbaden"
      ],
      "site": "https://www.rok-wiesbaden.de"
    }
  ],
  "sr-dusseldorf-germany": [
    {
      "id": "de-sr-serbian-orthodox-parish-in-augsburg-c-kirche-der-hl-stefan-und-jelena-jelisaveta-stiljan",
      "parent": "sr-dusseldorf-germany",
      "kind": "parish",
      "rank": "Parish",
      "name": "Serbian Orthodox Church of St. Stefan and Jelena-Jelisaveta Štiljanović in Augsburg",
      "local": "Храм Cветих Стефана и Јелене (Штиљановић) / Kirche der Hl. Stefan und Jelena-Jelisaveta Štiljanović",
      "country": "DE",
      "sources": [
        "https://eparhija-nemacka.com/augzburg/"
      ],
      "address": [
        "Kreutzerstr. 22, D - 86154 Augsburg"
      ]
    },
    {
      "id": "de-sr-serbian-orthodox-parish-in-munchen-kirche-des-heiligen-martyrer-johannes-vladimir-furst",
      "parent": "sr-dusseldorf-germany",
      "kind": "parish",
      "rank": "Parish",
      "name": "Serbian Orthodox Church of the Holy Martyr John - Vladimir, Prince of Serbia in München",
      "local": "Храм Светог Јована Владимира, краља српског / Kirche des Heiligen Märtyrer Johannes - Vladimir, Fürst von Serbien",
      "country": "DE",
      "sources": [
        "https://eparhija-nemacka.com/minhen/"
      ],
      "address": [
        "Putzbrunner Str. 49, D - 81739 München -Neuperlach"
      ]
    },
    {
      "id": "de-sr-serbian-orthodox-worship-site-in-munchen-munchen-maria-schutz-und-furbitte-kirche-maria",
      "parent": "sr-dusseldorf-germany",
      "kind": "parish",
      "rank": "Worship site",
      "name": "Serbian Orthodox Mary's Protection and Intercession Church of Mary's Protection in München",
      "local": "Минхен / München: Покров Пресвете Богородице /Mariä Schutz und Fürbitte Kirche Mariä Schutz",
      "country": "DE",
      "sources": [
        "https://eparhija-nemacka.com/minhen/"
      ],
      "address": [
        "Dominikuszentrum, Hildegard-von-Bingen- Anger 1-3, D - 80937 München - Harthof"
      ]
    },
    {
      "id": "de-sr-serbian-orthodox-worship-site-in-rosenheim-rosenheim-e-hochfest-begegnung-des-herrn-im-t",
      "parent": "sr-dusseldorf-germany",
      "kind": "parish",
      "rank": "Worship site",
      "name": "Serbian Orthodox Solemn meeting of the Lord in the Temple of the Evangelical Lutheran Church of the Redeemer Königstr. 23 in Rosenheim",
      "local": "Розенхајм / Rosenheim: Сретењe Господње /Hochfest Begegnung des Herrn im Tempel Ev.-Luth-Erlöserkirche Königstr. 23",
      "country": "DE",
      "sources": [
        "https://eparhija-nemacka.com/minhen/"
      ],
      "address": [
        "D - 83022 Rosenheim"
      ]
    },
    {
      "id": "de-sr-serbian-orthodox-parish-in-nurnberg-k-kirche-der-hl-apostelgleichen-kyrill-und-method-kr",
      "parent": "sr-dusseldorf-germany",
      "kind": "parish",
      "rank": "Parish",
      "name": "Serbian Orthodox Church of the Holy Apostles Cyril and Methodius in Nürnberg",
      "local": "Храм Светих Kирила и Методија / Kirche der Hl. Apostelgleichen Kyrill und Method",
      "country": "DE",
      "sources": [
        "https://eparhija-nemacka.com/nirnberg/"
      ],
      "address": [
        "Kranichstr. 4, D - 90427 Nürnberg"
      ]
    },
    {
      "id": "de-sr-serbian-orthodox-worship-site-in-bamberg-bamberg-ukrainisch-griech-kath-kirche-st-nikola",
      "parent": "sr-dusseldorf-germany",
      "kind": "parish",
      "rank": "Worship site",
      "name": "Serbian Orthodox Bamberg: Ukrainian Greek Catholic. Church of St. Nicholas",
      "local": "Бамберг /Bamberg: Ukrainisch Griech.-Kath. Kirche St. Nikolaus",
      "country": "DE",
      "sources": [
        "https://eparhija-nemacka.com/nirnberg/"
      ],
      "address": [
        "Andreas Hofer Str. 21, D - 96049 Bamberg-Gaustadt"
      ]
    },
    {
      "id": "de-sr-serbian-orthodox-worship-site-in-bayreuth-bayreuth-ev-luth-epiphanias-kirche-warmenstein",
      "parent": "sr-dusseldorf-germany",
      "kind": "parish",
      "rank": "Worship site",
      "name": "Serbian Orthodox Bayreuth: Ev-luth. Epiphany Church",
      "local": "Бајројт / Bayreuth: Ev-luth. Epiphanias Kirche",
      "country": "DE",
      "sources": [
        "https://eparhija-nemacka.com/nirnberg/"
      ],
      "address": [
        "Warmensteinacher Str. 85, D - 85448 Bayreuth"
      ]
    },
    {
      "id": "de-sr-serbian-orthodox-worship-site-in-erlangen-erlangen-ev-luth-kirche-friedrich-str-15-d-910",
      "parent": "sr-dusseldorf-germany",
      "kind": "parish",
      "rank": "Worship site",
      "name": "Serbian Orthodox Erlangen: Evangelical Lutheran Church",
      "local": "Ерланген / Erlangen: Ev.-luth.-Kirche",
      "country": "DE",
      "sources": [
        "https://eparhija-nemacka.com/nirnberg/"
      ],
      "address": [
        "Friedrich Str. 15, D - 91054 Erlangen"
      ]
    },
    {
      "id": "de-sr-serbian-orthodox-worship-site-in-ingolstadt-ingolstadt-st-johannes-kirche-ettinger-str-4",
      "parent": "sr-dusseldorf-germany",
      "kind": "parish",
      "rank": "Worship site",
      "name": "Serbian Orthodox Ingolstadt: St. John's Church",
      "local": "Инголштат / Ingolstadt: St. Johannes Kirche",
      "country": "DE",
      "sources": [
        "https://eparhija-nemacka.com/nirnberg/"
      ],
      "address": [
        "Ettinger Str. 47, D - 85057 Ingolstadt"
      ]
    },
    {
      "id": "de-sr-serbian-orthodox-worship-site-in-neumarkt-neumarkt-christuskirche-seel-str-11-d-92318-ne",
      "parent": "sr-dusseldorf-germany",
      "kind": "parish",
      "rank": "Worship site",
      "name": "Serbian Orthodox Neumarkt: Christ Church",
      "local": "Нојмаркт / Neumarkt: Christuskirche",
      "country": "DE",
      "sources": [
        "https://eparhija-nemacka.com/nirnberg/"
      ],
      "address": [
        "Seel Str. 11, D - 92318 Neumarkt"
      ]
    },
    {
      "id": "de-sr-serbian-orthodox-worship-site-in-weissenburg-weissenburg-st-nikolaus-kirche-d-98781-wulz",
      "parent": "sr-dusseldorf-germany",
      "kind": "parish",
      "rank": "Worship site",
      "name": "Serbian Orthodox Weissenburg: St. Nicholas Church in Weißenburg",
      "local": "Вајсенбург / Weißenburg: St. Nikolaus Kirche",
      "country": "DE",
      "sources": [
        "https://eparhija-nemacka.com/nirnberg/"
      ],
      "address": [
        "D - 98781 Wülzburg-Weißenburg"
      ]
    },
    {
      "id": "de-sr-serbian-orthodox-parish-in-regensburg-pfarrei-des-hl-simeon-der-myronspender-st-nikolaus",
      "parent": "sr-dusseldorf-germany",
      "kind": "parish",
      "rank": "Parish",
      "name": "Serbian Orthodox Parish of St. Simeon the Donor of Myron in Regensburg",
      "local": "Парохија преподобног Симеона Мироточивог / Pfarrei des Hl. Simeon der Myronspender",
      "country": "DE",
      "sources": [
        "https://eparhija-nemacka.com/regensburg/"
      ],
      "address": [
        "St. Nikolaus Kirche, Obere Regenstr. 27 D - 93059 Regensburg"
      ]
    },
    {
      "id": "de-sr-serbian-orthodox-worship-site-in-pasau-pasau-bartholomaus-kapelle-prinz-eugen-str-1-d-94",
      "parent": "sr-dusseldorf-germany",
      "kind": "parish",
      "rank": "Worship site",
      "name": "Serbian Orthodox Pasau: Bartholomew Chapel",
      "local": "Пасау / Pasau: Bartholomäus Kapelle",
      "country": "DE",
      "sources": [
        "https://eparhija-nemacka.com/regensburg/"
      ],
      "address": [
        "Prinz Eugen Str. 1, D - 94032 Passau"
      ]
    },
    {
      "id": "de-sr-serbian-orthodox-worship-site-in-landshut-landshut-auferstehungskirche-fliederstr-17-d-8",
      "parent": "sr-dusseldorf-germany",
      "kind": "parish",
      "rank": "Worship site",
      "name": "Serbian Orthodox Landshut: Church of the Resurrection",
      "local": "Ландсхут / Landshut: Auferstehungskirche",
      "country": "DE",
      "sources": [
        "https://eparhija-nemacka.com/regensburg/"
      ],
      "address": [
        "Fliederstr. 17, D - 84032 Landshut"
      ]
    },
    {
      "id": "de-sr-serbian-orthodox-worship-site-in-burghausen-burghausen-st-anna-kapuzinerkloster-mautners",
      "parent": "sr-dusseldorf-germany",
      "kind": "parish",
      "rank": "Worship site",
      "name": "Serbian Orthodox Burghausen: St. Anna Capuchin Monastery",
      "local": "Бургхаузен / Burghausen: St. Anna Kapuzinerkloster",
      "country": "DE",
      "sources": [
        "https://eparhija-nemacka.com/regensburg/"
      ],
      "address": [
        "Mautnerstr. 238, D - 84489 Burghausen"
      ]
    },
    {
      "id": "de-sr-serbian-orthodox-worship-site-in-freising-freising-altottinger-kapelle-brunnhausgasse-2",
      "parent": "sr-dusseldorf-germany",
      "kind": "parish",
      "rank": "Worship site",
      "name": "Serbian Orthodox Freising: Altöttinger Kapelle Brunnhausgasse 2-4",
      "local": "Фрајзинг / Freising: Altöttinger Kapelle Brunnhausgasse 2-4",
      "country": "DE",
      "sources": [
        "https://eparhija-nemacka.com/regensburg/"
      ],
      "address": [
        "Bahnhofstraße 3, D - 35354 Freising"
      ]
    },
    {
      "id": "de-sr-serbian-orthodox-parish-in-karlsruhe-kirche-der-ehrwurdigen-mutter-paraskeva-erzbergerst",
      "parent": "sr-dusseldorf-germany",
      "kind": "parish",
      "rank": "Parish",
      "name": "Serbian Orthodox Church of Venerable Mother Paraskeva in Karlsruhe",
      "local": "Храм преподобне мајке Параскеве / Kirche der Ehrwürdigen Mutter Paraskeva",
      "country": "DE",
      "sources": [
        "https://eparhija-nemacka.com/karlsrue/"
      ],
      "address": [
        "Erzbergerstr. 170, D - 76149 Karlsruhe - Nordstadt"
      ]
    },
    {
      "id": "de-sr-serbian-orthodox-worship-site-in-pforzheim-pforzheim-ev-gemeinde-haidach-marienburger-st",
      "parent": "sr-dusseldorf-germany",
      "kind": "parish",
      "rank": "Worship site",
      "name": "Serbian Orthodox Pforzheim: Ev. Haidach community",
      "local": "Пфорцхајм / Pforzheim: Ev. Gemeinde Haidach",
      "country": "DE",
      "sources": [
        "https://eparhija-nemacka.com/karlsrue/"
      ],
      "address": [
        "Marienburger Str. 16, D - 75181 Pforzheim"
      ]
    },
    {
      "id": "de-sr-serbian-orthodox-worship-site-in-gaggenau-gaggenau-ev-markuskirche-amalienbergstr-11-d-7",
      "parent": "sr-dusseldorf-germany",
      "kind": "parish",
      "rank": "Worship site",
      "name": "Serbian Orthodox Gaggenau: Ev. St. Mark's Church",
      "local": "Гагенау / Gaggenau: Ev. Markuskirche",
      "country": "DE",
      "sources": [
        "https://eparhija-nemacka.com/karlsrue/"
      ],
      "address": [
        "Amalienbergstr. 11, D - 76571 Gaggenau"
      ]
    },
    {
      "id": "de-sr-serbian-orthodox-parish-in-mannheim-kirche-des-ehrwurdigen-simon-des-monchen-deidesheime",
      "parent": "sr-dusseldorf-germany",
      "kind": "parish",
      "rank": "Parish",
      "name": "Serbian Orthodox Church of the Venerable Simon the Monk in Mannheim",
      "local": "Храм преподобнога Симона Монаха / Kirche des Ehrwürdigen Simon des Mönchen",
      "country": "DE",
      "sources": [
        "https://eparhija-nemacka.com/manhajm/"
      ],
      "address": [
        "Deidesheimer Strasse 21, D - 68309 Mannheim - Käfertal"
      ]
    },
    {
      "id": "de-sr-serbian-orthodox-worship-site-in-speyer-speyer-st-bernhard-kirche-hirschgrabenstr-3-d-67",
      "parent": "sr-dusseldorf-germany",
      "kind": "parish",
      "rank": "Worship site",
      "name": "Serbian Orthodox Speyer: St. Bernhard Church",
      "local": "Шпејер / Speyer: St. Bernhard Kirche",
      "country": "DE",
      "sources": [
        "https://eparhija-nemacka.com/manhajm/"
      ],
      "address": [
        "Hirschgrabenstr. 3, D - 67346 Speyer"
      ]
    },
    {
      "id": "de-sr-serbian-orthodox-worship-site-in-heidelberg-heidelberg-st-bonifatius-kirche-blumenstr-20",
      "parent": "sr-dusseldorf-germany",
      "kind": "parish",
      "rank": "Worship site",
      "name": "Serbian Orthodox Heidelberg: St. Boniface Church",
      "local": "Хајделберг / Heidelberg: St. Bonifatius Kirche",
      "country": "DE",
      "sources": [
        "https://eparhija-nemacka.com/manhajm/"
      ],
      "address": [
        "Blumenstr. 20, D - 69115 Heidelberg"
      ]
    },
    {
      "id": "de-sr-serbian-orthodox-parish-in-ulm-kirche-der-heiligen-wundertater-und-uneigennutzigen-kosma",
      "parent": "sr-dusseldorf-germany",
      "kind": "parish",
      "rank": "Parish",
      "name": "Serbian Orthodox Church of the Holy Miracle Workers and Unselfish Cosmas and Damian in Ulm",
      "local": "Храм Светих бесребреника Козме и Дамјана / Kirche der Heiligen Wundertäter und Uneigennützigen Kosmas und Damian",
      "country": "DE",
      "sources": [
        "https://eparhija-nemacka.com/ulm/"
      ],
      "address": [
        "Furttenbachstr. 11, D - 89077 Ulm"
      ]
    },
    {
      "id": "de-sr-serbian-orthodox-worship-site-in-riedlingen-riedlingen-ev-christuskirche-grabenstr-14-d",
      "parent": "sr-dusseldorf-germany",
      "kind": "parish",
      "rank": "Worship site",
      "name": "Serbian Orthodox Riedlingen: Ev. Christ Church",
      "local": "Ридлинген / Riedlingen: Ev. Christuskirche",
      "country": "DE",
      "sources": [
        "https://eparhija-nemacka.com/ulm/"
      ],
      "address": [
        "Grabenstr. 14, D - 88499 Riedlingen"
      ]
    },
    {
      "id": "de-sr-serbian-orthodox-parish-in-villingen-schwenningen-a-kirche-des-hl-erzengels-michael-unte",
      "parent": "sr-dusseldorf-germany",
      "kind": "parish",
      "rank": "Parish",
      "name": "Serbian Orthodox Church of St. Archangel Michael in Villingen-Schwenningen",
      "local": "Храм Светог архангела Михаилa / Kirche des Hl. Erzengels Michael",
      "country": "DE",
      "sources": [
        "https://eparhija-nemacka.com/filingen-sveningen/"
      ],
      "address": [
        "Unterer Dammweg 6/3, D - 78050 Villingen-Schwenningen"
      ]
    },
    {
      "id": "de-sr-serbian-orthodox-worship-site-in-tuttlingen-tuttlingen-auferstehungskirche-mohlstr-23-d",
      "parent": "sr-dusseldorf-germany",
      "kind": "parish",
      "rank": "Worship site",
      "name": "Serbian Orthodox Tuttlingen: Church of the Resurrection",
      "local": "Тутлинген / Tuttlingen: Auferstehungskirche",
      "country": "DE",
      "sources": [
        "https://eparhija-nemacka.com/filingen-sveningen/"
      ],
      "address": [
        "Mohlstr. 23, D-78532 Tuttlingen"
      ]
    },
    {
      "id": "de-sr-serbian-orthodox-worship-site-in-albstadt-albstadt-thomaskirche-ostheimerstr-36-d-72458",
      "parent": "sr-dusseldorf-germany",
      "kind": "parish",
      "rank": "Worship site",
      "name": "Serbian Orthodox Albstadt: Thomaskirche",
      "local": "Албштат / Albstadt: Thomaskirche",
      "country": "DE",
      "sources": [
        "https://eparhija-nemacka.com/filingen-sveningen/"
      ],
      "address": [
        "Ostheimerstr. 36, D-72458 Albstadt"
      ]
    },
    {
      "id": "de-sr-serbian-orthodox-worship-site-in-singen-singen-st-michael-kapelle-uhlandstrasse-d-78224",
      "parent": "sr-dusseldorf-germany",
      "kind": "parish",
      "rank": "Worship site",
      "name": "Serbian Orthodox Singing: St.Michael Chapel in Singen",
      "local": "Зинген / Singen: St.Michael Kapelle",
      "country": "DE",
      "sources": [
        "https://eparhija-nemacka.com/filingen-sveningen/"
      ],
      "address": [
        "Uhlandstrasse D-78224 Singen"
      ]
    },
    {
      "id": "de-sr-serbian-orthodox-worship-site-in-blumberg-blumberg-marienkapelle-waldshuterstrasse-d-781",
      "parent": "sr-dusseldorf-germany",
      "kind": "parish",
      "rank": "Worship site",
      "name": "Serbian Orthodox Blumberg: Lady Chapel",
      "local": "Блумберг / Blumberg: Marienkapelle",
      "country": "DE",
      "sources": [
        "https://eparhija-nemacka.com/filingen-sveningen/"
      ],
      "address": [
        "Waldshuterstrasse D-78176 Blumberg"
      ]
    },
    {
      "id": "de-sr-serbian-orthodox-parish-in-frankfurt-kirche-der-auferstehung-christi-sondershausenstr-51",
      "parent": "sr-dusseldorf-germany",
      "kind": "parish",
      "rank": "Parish",
      "name": "Serbian Orthodox Church of the Resurrection of Christ in Frankfurt",
      "local": "Храм Васкрсења Христовог / Kirche der Auferstehung Christi",
      "country": "DE",
      "sources": [
        "https://eparhija-nemacka.com/frankfurt/"
      ],
      "address": [
        "Sondershausenstr. 51, D - 60326 Frankfurt аm Main"
      ]
    },
    {
      "id": "de-sr-serbian-orthodox-worship-site-in-frankfurt-frankfurt-beethovenplatz-1-60325-frankfurt-am",
      "parent": "sr-dusseldorf-germany",
      "kind": "parish",
      "rank": "Worship site",
      "name": "Serbian Orthodox Frankfurt: Church of the Holy Apostle Luke",
      "local": "Франкфурт / Frankfurt: Храм Светог апостола Луке",
      "country": "DE",
      "sources": [
        "https://eparhija-nemacka.com/frankfurt/"
      ],
      "address": [
        "Beethovenplatz 1, 60325 - Frankfurt am Main"
      ]
    },
    {
      "id": "de-sr-serbian-orthodox-worship-site-in-aschaffenburg-aschaffenburg-st-josef-kirche-uhlandstr-1",
      "parent": "sr-dusseldorf-germany",
      "kind": "parish",
      "rank": "Worship site",
      "name": "Serbian Orthodox Aschaffenburg: St. Joseph Church",
      "local": "Ашафенбург / Aschaffenburg: St. Josef Kirche",
      "country": "DE",
      "sources": [
        "https://eparhija-nemacka.com/frankfurt/"
      ],
      "address": [
        "Uhlandstr. 15, D - 63741 - Aschaffenburg"
      ]
    },
    {
      "id": "de-sr-serbian-orthodox-parish-in-friedrichshafen-kirche-der-serbischen-neumartyrer-adelheidstr",
      "parent": "sr-dusseldorf-germany",
      "kind": "parish",
      "rank": "Parish",
      "name": "Serbian Orthodox Church of the Serbian New Martyrs in Friedrichshafen",
      "local": "Храм Светих српских новомученика / Kirche der Serbischen Neumärtyrer",
      "country": "DE",
      "sources": [
        "https://eparhija-nemacka.com/fridrihshafen/"
      ],
      "address": [
        "Adelheidstr. 4, D - 88046 Friedrichshafen"
      ]
    },
    {
      "id": "de-sr-serbian-orthodox-worship-site-in-konstanz-konstanz-schottenkapelle-schlotten-str-73-d-78",
      "parent": "sr-dusseldorf-germany",
      "kind": "parish",
      "rank": "Worship site",
      "name": "Serbian Orthodox Konstanz: Schottenkapelle",
      "local": "Констанц / Konstanz: Schottenkapelle",
      "country": "DE",
      "sources": [
        "https://eparhija-nemacka.com/fridrihshafen/"
      ],
      "address": [
        "Schlotten Str. 73, D - 78462 Konstanz"
      ]
    },
    {
      "id": "de-sr-serbian-orthodox-parish-in-stuttgart-kirche-der-synaxis-der-serbischen-heiligen-mohringe",
      "parent": "sr-dusseldorf-germany",
      "kind": "parish",
      "rank": "Parish",
      "name": "Serbian Orthodox Church of the Synaxis of Serbian Saints in Stuttgart",
      "local": "Храм сабора српских Светитеља / Kirche der Synaxis der serbischen Heiligen",
      "country": "DE",
      "sources": [
        "https://eparhija-nemacka.com/stutgart/"
      ],
      "address": [
        "Möhringer Str. 81а, D - 70199 Stuttgart - Heslach"
      ]
    },
    {
      "id": "de-sr-serbian-orthodox-worship-site-in-goppingen-goppingen-marstallstr-21-d-73033-goppingen",
      "parent": "sr-dusseldorf-germany",
      "kind": "parish",
      "rank": "Worship site",
      "name": "Serbian Orthodox Göppingen: Храм Светог архангела Михаила",
      "local": "Гепинген / Göppingen: Храм Светог архангела Михаила",
      "country": "DE",
      "sources": [
        "https://eparhija-nemacka.com/stutgart/"
      ],
      "address": [
        "Marstallstr. 21, D - 73033 Göppingen"
      ]
    },
    {
      "id": "de-sr-serbian-orthodox-worship-site-in-calw-calw-ev-versohnungskirche-wielandstr-12-d-75365-ca",
      "parent": "sr-dusseldorf-germany",
      "kind": "parish",
      "rank": "Worship site",
      "name": "Serbian Orthodox Calw: Ev. Church of Reconciliation",
      "local": "Калв / Calw: Ev. Versöhnungskirche",
      "country": "DE",
      "sources": [
        "https://eparhija-nemacka.com/stutgart/"
      ],
      "address": [
        "Wielandstr. 12, D - 75365 Calw - Heumaden"
      ]
    },
    {
      "id": "de-sr-serbian-orthodox-worship-site-in-reutlingen-reutlingen-ev-katharinenkirche-rommelsbacher",
      "parent": "sr-dusseldorf-germany",
      "kind": "parish",
      "rank": "Worship site",
      "name": "Serbian Orthodox Reutlingen: Ev. St. Catherine's Church",
      "local": "Ројтлинген / Reutlingen: Ev. Katharinenkirche",
      "country": "DE",
      "sources": [
        "https://eparhija-nemacka.com/stutgart/"
      ],
      "address": [
        "Rommelsbacherstr. 2, D - 72760 Reutlingen"
      ]
    },
    {
      "id": "de-sr-serbian-orthodox-parish-in-limburg-limburg",
      "parent": "sr-dusseldorf-germany",
      "kind": "parish",
      "rank": "Parish",
      "name": "Serbian Orthodox Limburg",
      "local": "Limburg",
      "country": "DE",
      "sources": [
        "https://eparhija-nemacka.com/arhijerejski-namjesnici/"
      ]
    },
    {
      "id": "de-sr-serbian-orthodox-parish-in-altena-kirche-des-hl-simeon-der-myronspender-graf-eberhard-st",
      "parent": "sr-dusseldorf-germany",
      "kind": "parish",
      "rank": "Parish",
      "name": "Serbian Orthodox Church of St. Simeon the Myron Donor in Altena",
      "local": "Храм Св. Симеона Мироточивога / Kirche des Hl. Simeon der Myronspender",
      "country": "DE",
      "sources": [
        "https://eparhija-nemacka.com/altena/"
      ],
      "address": [
        "Graf-Eberhard-Str. 1, D-58762 Altena"
      ]
    },
    {
      "id": "de-sr-serbian-orthodox-worship-site-in-griechische-kirche-elfriedenhohe-1-d-58095-hagen",
      "parent": "sr-dusseldorf-germany",
      "kind": "parish",
      "rank": "Worship site",
      "name": "Serbian Orthodox Hagen: Griechische Kirche in Хаген",
      "local": "Хаген: Griechische Kirche",
      "country": "DE",
      "sources": [
        "https://eparhija-nemacka.com/altena/"
      ],
      "address": [
        "Elfriedenhöhe 1, D-58095 Hagen"
      ]
    },
    {
      "id": "de-sr-serbian-orthodox-parish-in-aachen-kirche-der-christi-himmelfahrt-tannenweg-14-d-52146-wu",
      "parent": "sr-dusseldorf-germany",
      "kind": "parish",
      "rank": "Parish",
      "name": "Serbian Orthodox Church of the Ascension of Christ in Aachen",
      "local": "Храм Вазнесења Господњег / Kirche der Christi Himmelfahrt",
      "country": "DE",
      "sources": [
        "https://eparhija-nemacka.com/ahen/"
      ],
      "address": [
        "Tannenweg 14 D-52146 Würselen / Aachen"
      ]
    },
    {
      "id": "de-sr-serbian-orthodox-parish-in-bonn-bonn",
      "parent": "sr-dusseldorf-germany",
      "kind": "parish",
      "rank": "Parish",
      "name": "Serbian Orthodox Bonn",
      "local": "Bonn",
      "country": "DE",
      "sources": [
        "https://eparhija-nemacka.com/arhijerejski-namjesnici/"
      ]
    },
    {
      "id": "de-sr-serbian-orthodox-parish-in-bielefeld-kirche-des-hl-basilius-des-wundertaters-von-ostrog",
      "parent": "sr-dusseldorf-germany",
      "kind": "parish",
      "rank": "Parish",
      "name": "Serbian Orthodox Church of St. Basil the Wonderworker of Ostrog in Bielefeld",
      "local": "Храм Светог Василија Острошког Чудотворца / Kirche des Hl. Basilius des Wundertäters von Ostrog",
      "country": "DE",
      "sources": [
        "https://eparhija-nemacka.com/bilefeld/"
      ],
      "address": [
        "Wellensiek 69a , D - 33619 Bielefeld - Dornberg"
      ]
    },
    {
      "id": "de-sr-serbian-orthodox-parish-in-wuppertal-kirche-der-geburt-der-allheiligen-gottesgebarerin-h",
      "parent": "sr-dusseldorf-germany",
      "kind": "parish",
      "rank": "Parish",
      "name": "Serbian Orthodox Church of the Nativity of the Most Holy Theotokos in Wuppertal",
      "local": "Храм Рођења Пресвете Богородице / Kirche der Geburt der Allheiligen Gottesgebärerin",
      "country": "DE",
      "sources": [
        "https://eparhija-nemacka.com/vupertal/"
      ],
      "address": [
        "Hombüchel 53-55, D - 42105 Wuppertal - Elberfeld"
      ]
    },
    {
      "id": "de-sr-serbian-orthodox-parish-in-dusseldorf-kathedralkirche-des-heiligen-sava-wanheimer-str-54",
      "parent": "sr-dusseldorf-germany",
      "kind": "parish",
      "rank": "Parish",
      "name": "Serbian Orthodox Cathedral Church of Saint Sava in Düsseldorf",
      "local": "Саборни храм Светог Саве / Kathedralkirche des Heiligen Sava",
      "country": "DE",
      "sources": [
        "https://eparhija-nemacka.com/diseldorf/"
      ],
      "address": [
        "Wanheimer Str. 54, D - 40472 Düsseldorf-Lichtenbroich"
      ]
    },
    {
      "id": "de-sr-serbian-orthodox-parish-in-dortmund-kirche-des-hl-apostel-und-evangelisten-lukas-engelbe",
      "parent": "sr-dusseldorf-germany",
      "kind": "parish",
      "rank": "Parish",
      "name": "Serbian Orthodox Church of the Holy Apostle and Evangelist Luke in Dortmund",
      "local": "Храм Светог апостола и јеванђелиста Луке / Kirche des Hl. Apostel und Evangelisten Lukas",
      "country": "DE",
      "sources": [
        "https://eparhija-nemacka.com/dortmund/"
      ],
      "address": [
        "Engelbertstr. 5, D - 44379 Dortmund"
      ]
    },
    {
      "id": "de-sr-serbian-orthodox-parish-in-essen-kirche-des-heiligen-erstmartyrern-und-erzdiakonen-steph",
      "parent": "sr-dusseldorf-germany",
      "kind": "parish",
      "rank": "Parish",
      "name": "Serbian Orthodox Church of the Holy First Martyr and Archdeacon Stephen in Essen",
      "local": "Храм Светог архиђакона Стефана / Kirche des Heiligen Erstmärtyrern und Erzdiakonen Stephanos",
      "country": "DE",
      "sources": [
        "https://eparhija-nemacka.com/esen/"
      ],
      "address": [
        "Im Looscheid 27, D - 45141 Essen - Stoppenberg"
      ]
    },
    {
      "id": "de-sr-serbian-orthodox-worship-site-in-kapelle-des-hl-stefan-von-decani-st-agnes-kirche-kapell",
      "parent": "sr-dusseldorf-germany",
      "kind": "parish",
      "rank": "Worship site",
      "name": "Serbian Orthodox Chapel of St. Stephen of Dečani St. Agnes Church in Kapelle des Hl. Stefan von Dečani St. Agnes-Kirche",
      "local": "Капела Светог краља Стефана Дечанског / Kapelle des Hl. Stefan von Dečani St. Agnes-Kirche",
      "country": "DE",
      "sources": [
        "https://eparhija-nemacka.com/esen/"
      ],
      "address": [
        "Am Kreuzberg 2, D - 46397 Bocholt"
      ]
    },
    {
      "id": "de-sr-serbian-orthodox-parish-in-koln-kirche-der-erhohung-des-allehrwurdigen-und-lebenspendend",
      "parent": "sr-dusseldorf-germany",
      "kind": "parish",
      "rank": "Parish",
      "name": "Serbian Orthodox Church of the Exaltation of the Most Venerable and Life-Giving Cross and Chapel of St. Arseniye of Srem in Köln",
      "local": "Храм воздвижења часнога Крста Господњег и капела Светог Арсенија Сремца / Kirche der Erhöhung des allehrwürdigen und lebenspendenden Kreuzes und Kapelle des Hl. Arsenije von Srem",
      "country": "DE",
      "sources": [
        "https://eparhija-nemacka.com/keln/"
      ],
      "address": [
        "Frankenplatz 15, D - 51149 Köln - Porz"
      ]
    },
    {
      "id": "de-sr-serbian-orthodox-worship-site-in-siegen-siegen-am-rain-17-d-56074-siegen-kaan-marienborn",
      "parent": "sr-dusseldorf-germany",
      "kind": "parish",
      "rank": "Worship site",
      "name": "Serbian Orthodox Winning: Am Rain 17 in Siegen",
      "local": "Зиген / Siegen: Am Rain 17",
      "country": "DE",
      "sources": [
        "https://eparhija-nemacka.com/keln/"
      ],
      "address": [
        "D - 56074 Siegen - Kaan / Marienborn"
      ]
    },
    {
      "id": "de-sr-serbian-orthodox-parish-in-berlin-kirche-des-heiligen-sava-ruppiner-str-28-d-13355-berli",
      "parent": "sr-dusseldorf-germany",
      "kind": "parish",
      "rank": "Parish",
      "name": "Serbian Orthodox Church of Saint Sava in Berlin",
      "local": "Храм Светог Саве / Kirche des Heiligen Sava",
      "country": "DE",
      "sources": [
        "https://eparhija-nemacka.com/berlin/"
      ],
      "address": [
        "Ruppiner Str. 28, D - 13355 Berlin - Wedding"
      ]
    },
    {
      "id": "de-sr-serbian-orthodox-parish-in-bremen-kirche-der-weiche-der-kirche-des-hl-grossmartyrers-geo",
      "parent": "sr-dusseldorf-germany",
      "kind": "parish",
      "rank": "Parish",
      "name": "Serbian Orthodox Church of the Church of St. George the Great Martyr in Lydda in Bremen",
      "local": "Храм обновљења храма Светог Георгија- Ђурђиц / Kirche der Weiche der Kirche des Hl. Großmärtyrers Georg in Lydda",
      "country": "DE",
      "sources": [
        "https://eparhija-nemacka.com/bremen/"
      ],
      "address": [
        "Geschwister-Scholl-Str. 136, D - 28327 Bremen"
      ]
    },
    {
      "id": "de-sr-serbian-orthodox-parish-in-kassel-kirche-des-heiligen-martyrers-furst-lazarus-johann-seb",
      "parent": "sr-dusseldorf-germany",
      "kind": "parish",
      "rank": "Parish",
      "name": "Serbian Orthodox Church of the Holy Martyr Prince Lazarus in Kassel",
      "local": "Храм Светога кнеза Лазара / Kirche des Heiligen Märtyrers Fürst Lazarus",
      "country": "DE",
      "sources": [
        "https://eparhija-nemacka.com/kasel/"
      ],
      "address": [
        "Johann-Sebastian Bach Str. 20, D - 34134 Kassel - Niederzwehren"
      ]
    },
    {
      "id": "de-sr-serbian-orthodox-worship-site-in-erfurt-erfurt-saal-im-restaurant-fontana-futter-strasse",
      "parent": "sr-dusseldorf-germany",
      "kind": "parish",
      "rank": "Worship site",
      "name": "Serbian Orthodox Erfurt: Hall in the Fontana restaurant",
      "local": "Ерфурт / Erfurt: Saal im Restaurant Fontana",
      "country": "DE",
      "sources": [
        "https://eparhija-nemacka.com/kasel/"
      ],
      "address": [
        "Futter Straße 18/19, D - 99084 Erfurt"
      ]
    },
    {
      "id": "de-sr-serbian-orthodox-worship-site-in-paderborn-paderborn-marktkirche-kamp-2-d-33098-paderbor",
      "parent": "sr-dusseldorf-germany",
      "kind": "parish",
      "rank": "Worship site",
      "name": "Serbian Orthodox Paderborn: Market Church",
      "local": "Падерборн / Paderborn: Marktkirche",
      "country": "DE",
      "sources": [
        "https://eparhija-nemacka.com/kasel/"
      ],
      "address": [
        "Kamp 2, D - 33098 Paderborn"
      ]
    },
    {
      "id": "de-sr-serbian-orthodox-worship-site-in-lippstadt-lippstadt-kirchplatz-1-d-59590-monninghausen",
      "parent": "sr-dusseldorf-germany",
      "kind": "parish",
      "rank": "Worship site",
      "name": "Serbian Orthodox Lippstadt: Kirchplatz 1",
      "local": "Липштат / Lippstadt: Kirchplatz 1",
      "country": "DE",
      "sources": [
        "https://eparhija-nemacka.com/kasel/"
      ],
      "address": [
        "D - 59590 Mönninghausen"
      ]
    },
    {
      "id": "de-sr-serbian-orthodox-worship-site-in-fulda-fulda-kreuzkirche-haderwaldstr-89a-d-36041-fulda",
      "parent": "sr-dusseldorf-germany",
      "kind": "parish",
      "rank": "Worship site",
      "name": "Serbian Orthodox Fulda: Church of the Cross",
      "local": "Фулда / Fulda: Kreuzkirche",
      "country": "DE",
      "sources": [
        "https://eparhija-nemacka.com/kasel/"
      ],
      "address": [
        "Haderwaldstr. 89a, D - 36041 Fulda"
      ]
    },
    {
      "id": "de-sr-serbian-orthodox-parish-in-osnabruck-kirche-des-hl-grossmartyrers-und-siegestragers-geor",
      "parent": "sr-dusseldorf-germany",
      "kind": "parish",
      "rank": "Parish",
      "name": "Serbian Orthodox Church of the Holy Great Martyr and Victory Bearer George in Osnabrück",
      "local": "Храм Светог великомученика и победоносца Георгија / Kirche des Hl. Grossmärtyrers und Siegesträgers Georg",
      "country": "DE",
      "sources": [
        "https://eparhija-nemacka.com/osnabrik/"
      ],
      "address": [
        "Wersenerstr. 85, D - 49090 Osnabrück - Eversburg"
      ]
    },
    {
      "id": "de-sr-serbian-orthodox-worship-site-in-lingen-lingen-heinrich-str-1-d-49809-lingen",
      "parent": "sr-dusseldorf-germany",
      "kind": "parish",
      "rank": "Worship site",
      "name": "Serbian Orthodox Lingen: Капела св. Арх. Михаила",
      "local": "Линген / Lingen: Капела св. Арх. Михаила",
      "country": "DE",
      "sources": [
        "https://eparhija-nemacka.com/osnabrik/"
      ],
      "address": [
        "Heinrich Str. 1, D - 49809 Lingen"
      ]
    },
    {
      "id": "de-sr-serbian-orthodox-worship-site-in-munster-munster-ev-epiphaniaskirche-karntner-str-23-25",
      "parent": "sr-dusseldorf-germany",
      "kind": "parish",
      "rank": "Worship site",
      "name": "Serbian Orthodox Münster: Ev. Epiphany Church",
      "local": "Минстер / Münster: Ev. Epiphaniaskirche",
      "country": "DE",
      "sources": [
        "https://eparhija-nemacka.com/osnabrik/"
      ],
      "address": [
        "Kärntner Str. 23-25, D - 48145 Münster"
      ]
    },
    {
      "id": "de-sr-serbian-orthodox-parish-in-hannover-kirche-mengendamm-16-c-d-30177-hannover-list",
      "parent": "sr-dusseldorf-germany",
      "kind": "parish",
      "rank": "Parish",
      "name": "Serbian Orthodox Church: in Hannover",
      "local": "Црква / Kirche:",
      "country": "DE",
      "sources": [
        "https://eparhija-nemacka.com/hanover/"
      ],
      "address": [
        "Mengendamm 16 c, D -30177 Hannover - List"
      ]
    },
    {
      "id": "de-sr-serbian-orthodox-parish-in-hamburg-kirche-des-hl-erzengels-michael-schellingstr-7-9-d-22",
      "parent": "sr-dusseldorf-germany",
      "kind": "parish",
      "rank": "Parish",
      "name": "Serbian Orthodox Church of St. Archangel Michael in Hamburg",
      "local": "Храм Светога архангела Михаила /Kirche des Hl. Erzengels Michael",
      "country": "DE",
      "sources": [
        "https://eparhija-nemacka.com/hamburg/"
      ],
      "address": [
        "Schellingstr. 7-9, D -22089 Hamburg,"
      ]
    },
    {
      "id": "de-sr-serbian-orthodox-worship-site-in-kiel-kiel-jakobi-ost-kirche-knoopen-weg-53-d-24103-kiel",
      "parent": "sr-dusseldorf-germany",
      "kind": "parish",
      "rank": "Worship site",
      "name": "Serbian Orthodox Kiel: Jakobi-Ost Church",
      "local": "Кил / Kiel: Jakobi-Ost Kirche",
      "country": "DE",
      "sources": [
        "https://eparhija-nemacka.com/hamburg/"
      ],
      "address": [
        "Knoopen Weg 53, D - 24103 Kiel"
      ]
    },
    {
      "id": "de-sr-serbian-orthodox-worship-site-in-lubeck-lubeck-hl-georgios-kirche-kleine-alte-fahre-6a-d",
      "parent": "sr-dusseldorf-germany",
      "kind": "parish",
      "rank": "Worship site",
      "name": "Serbian Orthodox Lübeck: St. Georgios Church",
      "local": "Либек / Lübeck: Hl. Georgios Kirche",
      "country": "DE",
      "sources": [
        "https://eparhija-nemacka.com/hamburg/"
      ],
      "address": [
        "Kleine Alte Fähre 6a, D - 23552 Lübeck"
      ]
    },
    {
      "id": "de-sr-dormition-of-the-mother-of-god-monastery",
      "parent": "sr-dusseldorf-germany",
      "kind": "monastery",
      "rank": "Monastery",
      "name": "Serbian Orthodox Monastery of the Assumption of the Blessed Virgin Mary",
      "local": "Манастир Успења Пресвете Богородице",
      "country": "DE",
      "sources": [
        "https://eparhija-nemacka.com/manastir-uspenja-presvete-bogorodice/"
      ]
    }
  ],
  "ro-germany": [
    {
      "id": "de-ro-aachen-parohia-sfanta-treime",
      "parent": "ro-germany",
      "kind": "parish",
      "rank": "Parish",
      "name": "Romanian Orthodox \"Holy Trinity\" Parish in Aachen",
      "local": "Parohia \"Sfânta Treime\" - Aachen",
      "country": "DE",
      "sources": [
        "https://mitropolia-ro.de/parohii-germania/"
      ],
      "address": [
        "Theresienkirche, Pontstraße 43, 52062 Aachen"
      ]
    },
    {
      "id": "de-ro-altotting-trostberg-parohia-adormirea-maicii-domnului",
      "parent": "ro-germany",
      "kind": "parish",
      "rank": "Parish",
      "name": "Romanian Orthodox Parish \"Assumption of the Virgin Mary\" - Altötting in Altötting - Trostberg",
      "local": "Parohia \"Adormirea Maicii Domnului\" - Altötting - Trostberg",
      "country": "DE",
      "sources": [
        "https://mitropolia-ro.de/parohii-germania/"
      ],
      "address": [
        "Neuöttinger Str. 24, 84503 Altötting"
      ]
    },
    {
      "id": "de-ro-amberg-parohia-sfanta-treime-sf-ier-nicolae-si-sf-cuv-paisie-si-cleopa-de-la-sihastria",
      "parent": "ro-germany",
      "kind": "parish",
      "rank": "Parish",
      "name": "Romanian Orthodox \"Holy Trinity\", \"St. Ier. Nicholas\" and \"St. Cuv. Paisie and Cleopa from Sihăstria\" parish in Amberg",
      "local": "Parohia \"Sfânta Treime\", \"Sf. Ier. Nicolae\" și \"Sf. Cuv. Paisie și Cleopa de la Sihăstria\" - Amberg",
      "country": "DE",
      "sources": [
        "https://mitropolia-ro.de/parohii-germania/"
      ],
      "address": [
        "Nelkenweg 1, 92245 Kümmersbruck"
      ]
    },
    {
      "id": "de-ro-ansbach-parohia-sfanta-treime",
      "parent": "ro-germany",
      "kind": "parish",
      "rank": "Parish",
      "name": "Romanian Orthodox \"Holy Trinity\" Parish in Ansbach",
      "local": "Parohia \"Sfânta Treime\" - Ansbach",
      "country": "DE",
      "sources": [
        "https://mitropolia-ro.de/parohii-germania/"
      ],
      "address": [
        "Dreieinigkeitskirche, Kirchenstr.2, 91522 Ansbach"
      ]
    },
    {
      "id": "de-ro-apolda-parohia-sf-ap-petru-si-pavel",
      "parent": "ro-germany",
      "kind": "parish",
      "rank": "Parish",
      "name": "Romanian Orthodox \"St. Ap. Peter and Paul\" Parish in Apolda",
      "local": "Parohia \"Sf. Ap. Petru și Pavel\" - Apolda",
      "country": "DE",
      "sources": [
        "https://mitropolia-ro.de/parohii-germania/"
      ],
      "address": [
        "Bahnhofstr. 22, 99510 Apolda"
      ]
    },
    {
      "id": "de-ro-aschaffenburg-parohia-intampinarea-domnului-si-sf-mc-ecaterina",
      "parent": "ro-germany",
      "kind": "parish",
      "rank": "Parish",
      "name": "Romanian Orthodox Parish \"The Reception of the Lord\" and \"St. Mc. Catherine\" in Aschaffenburg",
      "local": "Parohia \"Întâmpinarea Domnului\" și \"Sf. Mc. Ecaterina\" - Aschaffenburg",
      "country": "DE",
      "sources": [
        "https://mitropolia-ro.de/parohii-germania/"
      ],
      "address": [
        "Spitalkapelle, Lamprechtstr. 2, 63739 Aschaffenburg"
      ]
    },
    {
      "id": "de-ro-augsburg-parohia-sf-arhid-stefan",
      "parent": "ro-germany",
      "kind": "parish",
      "rank": "Parish",
      "name": "Romanian Orthodox \"St. Archid. Stefan\" Parish in Augsburg",
      "local": "Parohia \"Sf. Arhid. Ştefan\" - Augsburg",
      "country": "DE",
      "sources": [
        "https://mitropolia-ro.de/parohii-germania/"
      ],
      "address": [
        "Don-Bosco-Platz 3, 86161 Augsburg"
      ]
    },
    {
      "id": "de-ro-backnang-winnenden-filia-sf-ioan-botezatorul-si-sf-ap-andrei",
      "parent": "ro-germany",
      "kind": "parish",
      "rank": "Filial community",
      "name": "Romanian Orthodox daughter of \"St. John the Baptist\" and \"St. Ap. Andrew\" - Backnang in Backnang - Winnenden",
      "local": "filia \"Sf. Ioan Botezătorul\" și \"Sf. Ap. Andrei\" - Backnang - Winnenden",
      "country": "DE",
      "sources": [
        "https://mitropolia-ro.de/parohii-germania/"
      ],
      "address": [
        "Im Seefeld 4, 71522 Backnang (Biserica greacă)"
      ]
    },
    {
      "id": "de-ro-bad-tolz-wolfratshausen-parohia-sf-ioan-botezatorul-si-sf-mc-sebastian",
      "parent": "ro-germany",
      "kind": "parish",
      "rank": "Parish",
      "name": "Romanian Orthodox \"St. John the Baptist\" and \"St. Mc. Sebastian\" parish - Bad Tölz in Bad Tölz - Wolfratshausen",
      "local": "Parohia \"Sf. Ioan Botezătorul\" şi \"Sf. Mc. Sebastian\" - Bad Tölz - Wolfratshausen",
      "country": "DE",
      "sources": [
        "https://mitropolia-ro.de/parohii-germania/"
      ],
      "address": [
        "St. Nikolauskapelle, Bundesstr.11, 82538 Geretsried"
      ]
    },
    {
      "id": "de-ro-bad-windsheim-uffenheim-parohia-sf-cuv-parascheva-de-la-iasi-si-walburga-din-heidenheim",
      "parent": "ro-germany",
      "kind": "parish",
      "rank": "Parish",
      "name": "Romanian Orthodox Parish \"St. Cuv. Parascheva from Iasi and Walburga from Heidenheim\" in Bad Windsheim-Uffenheim",
      "local": "Parohia \"Sf. Cuv. Parascheva de la Iaşi şi Walburga din Heidenheim\" - Bad Windsheim-Uffenheim",
      "country": "DE",
      "sources": [
        "https://mitropolia-ro.de/parohii-germania/"
      ],
      "address": [
        "Marienkirche, Würzburger Str. 19, 97215 Uffenheim"
      ]
    },
    {
      "id": "de-ro-bamberg-parohia-sf-cuv-parascheva-si-sf-mc-kilian-kolonat-si-totnan",
      "parent": "ro-germany",
      "kind": "parish",
      "rank": "Parish",
      "name": "Romanian Orthodox Parish of \"St. Cuv. Parascheva\" and \"St. Mc. Kilian, Kolonat and Totnan\" in Bamberg",
      "local": "Parohia \"Sf. Cuv. Parascheva\" şi \"Sf. Mc. Kilian, Kolonat și Totnan\" - Bamberg",
      "country": "DE",
      "sources": [
        "https://mitropolia-ro.de/parohii-germania/"
      ],
      "address": [
        "St. Johannes Kirche, Andreas-Hofer-Str. 21, 96049 Bamberg"
      ]
    },
    {
      "id": "de-ro-bayreuth-parohia-nasterea-maicii-domnului",
      "parent": "ro-germany",
      "kind": "parish",
      "rank": "Parish",
      "name": "Romanian Orthodox Parish \"Nativity of the Mother of God\" in Bayreuth",
      "local": "Parohia \"Nașterea Maicii Domnului\" - Bayreuth",
      "country": "DE",
      "sources": [
        "https://mitropolia-ro.de/parohii-germania/"
      ],
      "address": [
        "Dreifaltigkeitskirche Föhrenweg 5, 95463 Bindlach"
      ]
    },
    {
      "id": "de-ro-bechhofen-dinkelsbuhl-parohia-nasterea-maicii-domnului-si-sf-cuv-arsenie-de-la-prislop",
      "parent": "ro-germany",
      "kind": "parish",
      "rank": "Parish",
      "name": "Romanian Orthodox Parish \"Nativity of the Mother of God\" and \"St. Arsenius of Prislop\" - Bechhofen in Bechhofen - Dinkelsbühl",
      "local": "Parohia \"Nașterea Maicii Domnului\" și \"Sf. Cuv. Arsenie de la Prislop\" - Bechhofen - Dinkelsbühl",
      "country": "DE",
      "sources": [
        "https://mitropolia-ro.de/parohii-germania/"
      ],
      "address": [
        "Dinkelsbühler Str. 16, 91572 Bechhofen"
      ]
    },
    {
      "id": "de-ro-berlin-parohia-sf-arhangheli-mihail-si-gavriil",
      "parent": "ro-germany",
      "kind": "parish",
      "rank": "Parish",
      "name": "Romanian Orthodox Parish \"St. Archangels Michael and Gabriel\" in Berlin",
      "local": "Parohia \"Sf. Arhangheli Mihail şi Gavriil\" - Berlin",
      "country": "DE",
      "sources": [
        "https://mitropolia-ro.de/parohii-germania/"
      ],
      "address": [
        "Heerstr. 63, 14055 Berlin - Charlottenburg"
      ]
    },
    {
      "id": "de-ro-berlin-parohia-sf-imparati-constantin-si-elena",
      "parent": "ro-germany",
      "kind": "parish",
      "rank": "Parish",
      "name": "Romanian Orthodox \"St. Emperors Constantine and Elena\" Parish in Berlin",
      "local": "Parohia \"Sf. Împărați Constantin și Elena\" - Berlin",
      "country": "DE",
      "sources": [
        "https://mitropolia-ro.de/parohii-germania/"
      ],
      "address": [
        "Prenzlauer Allee 1, 10405 Berlin"
      ]
    },
    {
      "id": "de-ro-biberach-an-der-riss-parohia-sf-ierarh-nectarie-si-sfintii-cuv-cleopa-si-paisie-de-la-si",
      "parent": "ro-germany",
      "kind": "parish",
      "rank": "Parish",
      "name": "Romanian Orthodox Parish \"St. Hierarch Nectarie\" and \"Saints Cuv. Cleopa and Paisie from Sihăstria\" in Biberach an der Riß",
      "local": "Parohia \"Sf. Ierarh Nectarie\" și \"Sfinții Cuv. Cleopa și Paisie de la Sihăstria\" - Biberach an der Riß",
      "country": "DE",
      "sources": [
        "https://mitropolia-ro.de/parohii-germania/"
      ],
      "address": [
        "Ulmer Str. 10, 88400 Biberach an der Riß"
      ]
    },
    {
      "id": "de-ro-bielefeld-parohia-acoperamantul-maicii-domnului",
      "parent": "ro-germany",
      "kind": "parish",
      "rank": "Parish",
      "name": "Romanian Orthodox Parish \"Coverage of the Mother of God\" in Bielefeld",
      "local": "Parohia \"Acoperământul Maicii Domnului\" - Bielefeld",
      "country": "DE",
      "sources": [
        "https://mitropolia-ro.de/parohii-germania/"
      ],
      "address": [
        "\"Auferstehung Christi\", Feilenhauerweg 2, 33659 Bielefeld"
      ]
    },
    {
      "id": "de-ro-bocholt-filie",
      "parent": "ro-germany",
      "kind": "parish",
      "rank": "Filial community",
      "name": "Romanian Orthodox daughter in Bocholt",
      "local": "filie - Bocholt",
      "country": "DE",
      "sources": [
        "https://mitropolia-ro.de/parohii-germania/"
      ],
      "address": [
        "Finkestrasse 1, 46414, Rhede"
      ]
    },
    {
      "id": "de-ro-bonn-parohia-sf-mc-stefan-cassius-si-florentius",
      "parent": "ro-germany",
      "kind": "parish",
      "rank": "Parish",
      "name": "Romanian Orthodox \"St. Mc. Stefan, Cassius and Florentius\" Parish in Bonn",
      "local": "Parohia \"Sf. Mc. Ştefan, Cassius şi Florentius\" - Bonn",
      "country": "DE",
      "sources": [
        "https://mitropolia-ro.de/parohii-germania/"
      ],
      "address": [
        "Legionsweg 16, 53117 Bonn"
      ]
    },
    {
      "id": "de-ro-borken-parohia-nasterea-sfantului-ioan-botezatorul-si-sf-cuv-ioan-casian-si-gherman",
      "parent": "ro-germany",
      "kind": "parish",
      "rank": "Parish",
      "name": "Romanian Orthodox \"Birth of St. John the Baptist\" and \"St. St. John Casian and German\" Parish in Borken",
      "local": "Parohia \"Nașterea Sfântului Ioan Botezătorul\" și \"Sf. Cuv. Ioan Casian și Gherman\" - Borken",
      "country": "DE",
      "sources": [
        "https://mitropolia-ro.de/parohii-germania/"
      ],
      "address": [
        "Landbergstr. 42, 48712 Gescher"
      ]
    },
    {
      "id": "de-ro-borkum-filia-nasterea-maicii-domnului",
      "parent": "ro-germany",
      "kind": "parish",
      "rank": "Filial community",
      "name": "Romanian Orthodox Branch \"Nativity of the Mother of God\" in Borkum",
      "local": "Filia \"Nașterea Maicii Domnului\" - Borkum",
      "country": "DE",
      "sources": [
        "https://mitropolia-ro.de/parohii-germania/"
      ],
      "address": [
        "Maria Meeresstern-Kirche, Kirchstraße 30, 26757 Borkum"
      ],
      "services": [
        "(slujbe în a patra duminică din lună)"
      ]
    },
    {
      "id": "de-ro-boblingen-parohia-sf-ioan-evanghelistul-si-sf-mc-afra-din-augsburg",
      "parent": "ro-germany",
      "kind": "parish",
      "rank": "Parish",
      "name": "Romanian Orthodox \"St. John the Evangelist\" and \"St. Mc. Afra from Augsburg\" parish in Böblingen",
      "local": "Parohia \"Sf. Ioan Evanghelistul\" și \"Sf. Mc. Afra din Augsburg\" - Böblingen",
      "country": "DE",
      "sources": [
        "https://mitropolia-ro.de/parohii-germania/"
      ],
      "address": [
        "Hans Thoma Platz 1, 71065 Sindelfingen"
      ]
    },
    {
      "id": "de-ro-bremen-parohia-sf-ier-luca-al-crimeii",
      "parent": "ro-germany",
      "kind": "parish",
      "rank": "Parish",
      "name": "Romanian Orthodox \"St. Jer. Luke of the Crimea\" Parish in Bremen",
      "local": "Parohia \"Sf. Ier. Luca al Crimeii\" - Bremen",
      "country": "DE",
      "sources": [
        "https://mitropolia-ro.de/parohii-germania/"
      ],
      "address": [
        "Hannoversche Strasse 20, 28790 Schwanewede"
      ]
    },
    {
      "id": "de-ro-bremerhaven-parohia-sf-ier-spiridon-si-ulrich",
      "parent": "ro-germany",
      "kind": "parish",
      "rank": "Parish",
      "name": "Romanian Orthodox \"St. Jer. Spyridon and Ulrich\" Parish in Bremerhaven",
      "local": "Parohia \"Sf. Ier. Spiridon și Ulrich\" - Bremerhaven",
      "country": "DE",
      "sources": [
        "https://mitropolia-ro.de/parohii-germania/"
      ],
      "address": [
        "Bahnhofstr. 14, 27612 Loxstedt"
      ]
    },
    {
      "id": "de-ro-bruchsal-parohia-sf-arhangheli-mihail-si-gavriil",
      "parent": "ro-germany",
      "kind": "parish",
      "rank": "Parish",
      "name": "Romanian Orthodox Parish \"St. Archangels Michael and Gabriel\" in Bruchsal",
      "local": "Parohia \"Sf. Arhangheli Mihail și Gavriil\" - Bruchsal",
      "country": "DE",
      "sources": [
        "https://mitropolia-ro.de/parohii-germania/"
      ],
      "address": [
        "Weingartener Str. 70, 76297 Staffort (Stutensee)"
      ]
    },
    {
      "id": "de-ro-cham-parohia-sfintii-doctori-fara-de-arginti",
      "parent": "ro-germany",
      "kind": "parish",
      "rank": "Parish",
      "name": "Romanian Orthodox Parish \"Holy Doctors without money\" in Cham",
      "local": "Parohia \"Sfinţii Doctori fără de arginţi\" - Cham",
      "country": "DE",
      "sources": [
        "https://mitropolia-ro.de/parohii-germania/"
      ],
      "address": [
        "Klosterstrasse 2, 93413 Cham"
      ]
    },
    {
      "id": "de-ro-chemnitz-parohia-sf-mc-vitus-si-sf-voievod-stefan-cel-mare",
      "parent": "ro-germany",
      "kind": "parish",
      "rank": "Parish",
      "name": "Romanian Orthodox Parish of \"St. Mc. Vitus\" and \"St. Governor Stephen the Great\" in Chemnitz",
      "local": "Parohia \"Sf. Mc. Vitus\" și \"Sf. Voievod Ștefan cel Mare\" - Chemnitz",
      "country": "DE",
      "sources": [
        "https://mitropolia-ro.de/parohii-germania/"
      ],
      "address": [
        "Zwickauerstr. 315, 09116 Chemnitz"
      ]
    },
    {
      "id": "de-ro-coburg-parohia-sf-cuv-teofana-basarab-si-sf-ier-kilian",
      "parent": "ro-germany",
      "kind": "parish",
      "rank": "Parish",
      "name": "Romanian Orthodox \"St. Cuv. Teofana Basarab\" and \"St. Jer. Kilian\" Parish in Coburg",
      "local": "Parohia \"Sf. Cuv. Teofana Basarab\" și \"Sf. Ier. Kilian\" - Coburg",
      "country": "DE",
      "sources": [
        "https://mitropolia-ro.de/parohii-germania/"
      ],
      "address": [
        "Am Moos 1, 96465 Neustadt bei Coburg"
      ]
    },
    {
      "id": "de-ro-dachau-parohia-acoperamantul-maicii-domnului-si-sf-alto",
      "parent": "ro-germany",
      "kind": "parish",
      "rank": "Parish",
      "name": "Romanian Orthodox Parish \"The Covering of the Mother of God\" and \"St. Alto\" in Dachau",
      "local": "Parohia \"Acoperământul Maicii Domnului\" și \"Sf. Alto\" - Dachau",
      "country": "DE",
      "sources": [
        "https://mitropolia-ro.de/parohii-germania/"
      ],
      "address": [
        "Münchner Str. 39, 85232 Bergkirchen, Dachau"
      ]
    },
    {
      "id": "de-ro-donauworth-parohia-sf-treime-sf-cuv-teodora-de-la-sihla-si-sf-mc-afra",
      "parent": "ro-germany",
      "kind": "parish",
      "rank": "Parish",
      "name": "Romanian Orthodox \"Holy Trinity\", \"Holy Cuv. Teodora de la Sihla\" and \"Holy Mc. Afra\" parish in Donauwörth",
      "local": "Parohia \"Sf. Treime\", \"Sf. Cuv. Teodora de la Sihla\" și \"Sf. Mc. Afra\" - Donauwörth",
      "country": "DE",
      "sources": [
        "https://mitropolia-ro.de/parohii-germania/"
      ],
      "address": [
        "Kapellstr. 1, 86609 Donauwörth"
      ]
    },
    {
      "id": "de-ro-dortmund-parohia-sf-cuv-dimitrie-cel-nou",
      "parent": "ro-germany",
      "kind": "parish",
      "rank": "Parish",
      "name": "Romanian Orthodox Parish \"St. Dimitrie the New\" in Dortmund",
      "local": "Parohia \"Sf. Cuv. Dimitrie cel Nou\" - Dortmund",
      "country": "DE",
      "sources": [
        "https://mitropolia-ro.de/parohii-germania/"
      ],
      "address": [
        "St. Georg-Kirche, Steinkühlerweg 217, 44263 Dortmund"
      ]
    },
    {
      "id": "de-ro-dresden-parohia-buna-vestire",
      "parent": "ro-germany",
      "kind": "parish",
      "rank": "Parish",
      "name": "Romanian Orthodox \"Good Annunciation\" Parish in Dresden",
      "local": "Parohia \"Buna Vestire\" - Dresden",
      "country": "DE",
      "sources": [
        "https://mitropolia-ro.de/parohii-germania/"
      ],
      "address": [
        "Kapelle des Striesener Friedhofes, Gottleubaer Str. 2, 01277 Dresden"
      ]
    },
    {
      "id": "de-ro-duisburg-parohia-sf-ier-nicolae-si-sfintii-mucenici-epictet-si-astion",
      "parent": "ro-germany",
      "kind": "parish",
      "rank": "Parish",
      "name": "Romanian Orthodox Parish of \"St. Ier. Nicholas\" and \"Holy Martyrs Epictetus and Astion\" in Duisburg",
      "local": "Parohia \"Sf. Ier. Nicolae\" și \"Sfinţii Mucenici Epictet şi Astion\" - Duisburg",
      "country": "DE",
      "sources": [
        "https://mitropolia-ro.de/parohii-germania/"
      ],
      "address": [
        "St. Suitbert-Kirche, Molbergstrasse 12, 47249 Duisburg"
      ]
    },
    {
      "id": "de-ro-duren-parohia-sf-mc-filofteia-de-la-arges",
      "parent": "ro-germany",
      "kind": "parish",
      "rank": "Parish",
      "name": "Romanian Orthodox \"St. Mc. Filofteia de la Argeș\" parish in Düren",
      "local": "Parohia \"Sf. Mc. Filofteia de la Argeș\" - Düren",
      "country": "DE",
      "sources": [
        "https://mitropolia-ro.de/parohii-germania/"
      ],
      "address": [
        "Krankenhaus Düren, Roonstrasse 30 52351, Düren"
      ]
    },
    {
      "id": "de-ro-dusseldorf-parohia-sfanta-treime-si-sf-nicolae",
      "parent": "ro-germany",
      "kind": "parish",
      "rank": "Parish",
      "name": "Romanian Orthodox \"Holy Trinity\" and \"St. Nicholas\" Parish in Düsseldorf",
      "local": "Parohia \"Sfânta Treime\" şi \"Sf. Nicolae\" - Düsseldorf",
      "country": "DE",
      "sources": [
        "https://mitropolia-ro.de/parohii-germania/"
      ],
      "address": [
        "Degerstr. 27, 40235 Düsseldorf"
      ]
    },
    {
      "id": "de-ro-eberbach-odenwald-parohia-sf-ap-andrei",
      "parent": "ro-germany",
      "kind": "parish",
      "rank": "Parish",
      "name": "Romanian Orthodox \"St. Ap. Andrew\" Parish in Eberbach-Odenwald-",
      "local": "Parohia \"Sf. Ap. Andrei\" - Eberbach-Odenwald-",
      "country": "DE",
      "sources": [
        "https://mitropolia-ro.de/parohii-germania/"
      ],
      "address": [
        "Höhenstraße 13, 69412 Eberbach"
      ]
    },
    {
      "id": "de-ro-emden-parohia",
      "parent": "ro-germany",
      "kind": "parish",
      "rank": "Parish",
      "name": "Romanian Orthodox The parish in Emden",
      "local": "Parohia - Emden",
      "country": "DE",
      "sources": [
        "https://mitropolia-ro.de/parohii-germania/"
      ],
      "address": [
        "Jahnstraße 9, 26725 Emden"
      ]
    },
    {
      "id": "de-ro-erding-ebersberg-parohia-duminica-tuturor-sfintilor",
      "parent": "ro-germany",
      "kind": "parish",
      "rank": "Parish",
      "name": "Romanian Orthodox \"Sunday of All Saints\" Parish in Erding-Ebersberg",
      "local": "Parohia \"Duminica Tuturor Sfinților\" - Erding-Ebersberg",
      "country": "DE",
      "sources": [
        "https://mitropolia-ro.de/parohii-germania/"
      ],
      "address": [
        "Biserica St. Georg (Pöring) - Burgstraße 24, 85604 Zorneding"
      ]
    },
    {
      "id": "de-ro-erlangen-parohia-sfintii-apostoli-petru-si-pavel",
      "parent": "ro-germany",
      "kind": "parish",
      "rank": "Parish",
      "name": "Romanian Orthodox \"Holy Apostles Peter and Paul\" Parish in Erlangen",
      "local": "Parohia \"Sfinţii Apostoli Petru şi Pavel\" - Erlangen",
      "country": "DE",
      "sources": [
        "https://mitropolia-ro.de/parohii-germania/"
      ],
      "address": [
        "St. Kunigund, Holzschuherring 40, 91058 Erlangen"
      ]
    },
    {
      "id": "de-ro-essen-bochum-parohia-sfintii-romani",
      "parent": "ro-germany",
      "kind": "parish",
      "rank": "Parish",
      "name": "Romanian Orthodox \"Romanian Saints\" Parish - Essen in Essen - Bochum",
      "local": "Parohia \"Sfinţii Români\" - Essen - Bochum",
      "country": "DE",
      "sources": [
        "https://mitropolia-ro.de/parohii-germania/"
      ],
      "address": [
        "Am Trappen 1, 44879 Bochum"
      ]
    },
    {
      "id": "de-ro-essen-ii-parohia-nasterea-maicii-domnului-si-sf-cuvioasa-teodora-de-la-sihla",
      "parent": "ro-germany",
      "kind": "parish",
      "rank": "Parish",
      "name": "Romanian Orthodox Parish of \"The Nativity of the Mother of God\" and \"St. Pious Theodora of Sihla\" in Essen II",
      "local": "Parohia \"Nașterea Maicii Domnului\" și \"Sf.Cuvioasă Teodora de la Sihla\" - Essen II",
      "country": "DE",
      "sources": [
        "https://mitropolia-ro.de/parohii-germania/"
      ],
      "address": [
        "Flandersbacher Str. 84, 42489 Wülfrath"
      ]
    },
    {
      "id": "de-ro-esslingen-parohia-nasterea-maicii-domnului",
      "parent": "ro-germany",
      "kind": "parish",
      "rank": "Parish",
      "name": "Romanian Orthodox Parish \"Nativity of the Mother of God\" in Esslingen",
      "local": "Parohia \"Naşterea Maicii Domnului\" - Esslingen",
      "country": "DE",
      "sources": [
        "https://mitropolia-ro.de/parohii-germania/"
      ],
      "address": [
        "Finkenweg 59, 73730 Esslingen am Neckar"
      ]
    },
    {
      "id": "de-ro-ettlingen-parohia-sf-arhid-stefan",
      "parent": "ro-germany",
      "kind": "parish",
      "rank": "Parish",
      "name": "Romanian Orthodox \"St. Arch. Stephen\" Parish in Ettlingen",
      "local": "Parohia \"Sf. Arhid. Ștefan\" - Ettlingen",
      "country": "DE",
      "sources": [
        "https://mitropolia-ro.de/parohii-germania/"
      ],
      "address": [
        "Frühlingstr. 17, 76275 Ettlingen-Bruchhausen"
      ]
    },
    {
      "id": "de-ro-flensburg-filie",
      "parent": "ro-germany",
      "kind": "parish",
      "rank": "Filial community",
      "name": "Romanian Orthodox daughter in Flensburg",
      "local": "filie - Flensburg",
      "country": "DE",
      "sources": [
        "https://mitropolia-ro.de/parohii-germania/"
      ],
      "address": [
        "Ansgarstrasse 1 ,24944 Flensburg"
      ]
    },
    {
      "id": "de-ro-frankfurt-am-main-parohia-acoperamantul-maicii-domnului",
      "parent": "ro-germany",
      "kind": "parish",
      "rank": "Parish",
      "name": "Romanian Orthodox Parish \"Coverage of the Mother of God\" in Frankfurt am Main",
      "local": "Parohia \"Acoperământul Maicii Domnului\" - Frankfurt am Main",
      "country": "DE",
      "sources": [
        "https://mitropolia-ro.de/parohii-germania/"
      ],
      "address": [
        "Ziegelhüttenweg 149 60598, Frankfurt Am Main"
      ]
    },
    {
      "id": "de-ro-frankfurt-am-main-parohia-sf-ap-bartolomeu",
      "parent": "ro-germany",
      "kind": "parish",
      "rank": "Parish",
      "name": "Romanian Orthodox \"St. Ap. Bartholomew\" Parish in Frankfurt am Main",
      "local": "Parohia \"Sf. Ap. Bartolomeu\" - Frankfurt am Main",
      "country": "DE",
      "sources": [
        "https://mitropolia-ro.de/parohii-germania/"
      ],
      "address": [
        "Funckstr. 14, 60486 Frankfurt am Main"
      ]
    },
    {
      "id": "de-ro-frankfurt-am-main-parohia-sf-cuv-xenia-din-petersburg",
      "parent": "ro-germany",
      "kind": "parish",
      "rank": "Parish",
      "name": "Romanian Orthodox \"St. Cuv. Xenia of Petersburg\" Parish in Frankfurt am Main",
      "local": "Parohia \"Sf. Cuv. Xenia din Petersburg\" - Frankfurt am Main",
      "country": "DE",
      "sources": [
        "https://mitropolia-ro.de/parohii-germania/"
      ],
      "address": [
        "Nordring 71, 60388 Frankfurt am Main"
      ]
    },
    {
      "id": "de-ro-freiburg-im-breisgau-parohia-sf-m-mc-mina",
      "parent": "ro-germany",
      "kind": "parish",
      "rank": "Parish",
      "name": "Romanian Orthodox \"St. M. Mc. Mina\" Parish in Freiburg im Breisgau",
      "local": "Parohia \"Sf. M. Mc. Mina\" - Freiburg im Breisgau",
      "country": "DE",
      "sources": [
        "https://mitropolia-ro.de/parohii-germania/"
      ],
      "address": [
        "Universitätskirche, Bertoldstr. 17, 79098 Freiburg"
      ]
    },
    {
      "id": "de-ro-freudenstadt-calw-parohia-adormirea-maicii-domnului-si-sf-cuv-parascheva",
      "parent": "ro-germany",
      "kind": "parish",
      "rank": "Parish",
      "name": "Romanian Orthodox Parish \"Assumption of the Virgin Mary\" and \"St. Cuv. Parascheva\" - Freudenstadt in Freudenstadt - Calw",
      "local": "Parohia \"Adormirea Maicii Domnului\" și \"Sf. Cuv. Parascheva\" - Freudenstadt - Calw",
      "country": "DE",
      "sources": [
        "https://mitropolia-ro.de/parohii-germania/"
      ],
      "address": [
        "Ruhesteinstr. 516, 72270 Baiersbronn"
      ]
    },
    {
      "id": "de-ro-friedberg-hessen-parohia-sf-cuv-parascheva-sf-ier-calinic-de-la-cernica-si-luca-al-crime",
      "parent": "ro-germany",
      "kind": "parish",
      "rank": "Parish",
      "name": "Romanian Orthodox \"St. Cuv. Parascheva\" Parish, \"St. Jer. Calinic from Cernica and Luke of the Crimea\" in Friedberg / Hessen",
      "local": "Parohia \"Sf. Cuv. Parascheva\", \"Sf. Ier. Calinic de la Cernica și Luca al Crimeei\" - Friedberg / Hessen",
      "country": "DE",
      "sources": [
        "https://mitropolia-ro.de/parohii-germania/"
      ],
      "address": [
        "Wintersteinstraße 39, 61169 Friedberg (Hessen)"
      ]
    },
    {
      "id": "de-ro-friedrichshafen-filie",
      "parent": "ro-germany",
      "kind": "parish",
      "rank": "Filial community",
      "name": "Romanian Orthodox daughter in Friedrichshafen",
      "local": "filie - Friedrichshafen",
      "country": "DE",
      "sources": [
        "https://mitropolia-ro.de/parohii-germania/"
      ],
      "address": [
        "Biserica Sârbă, Adelheidstr. 4, Friedrichshafen"
      ],
      "services": [
        "(slujbe în a 2-a duminică din lună)"
      ]
    },
    {
      "id": "de-ro-fulda-parohia-inaltarea-domnului-si-sf-ier-bonifatiu",
      "parent": "ro-germany",
      "kind": "parish",
      "rank": "Parish",
      "name": "Romanian Orthodox \"Ascension of the Lord\" and \"St. Jer. Boniface\" Parish in Fulda",
      "local": "Parohia \"Înălțarea Domnului\" și \"Sf. Ier. Bonifațiu\" - Fulda",
      "country": "DE",
      "sources": [
        "https://mitropolia-ro.de/parohii-germania/"
      ],
      "address": [
        "Heilig Geist Kirche, Loeherstrasse 1, Fulda 36037"
      ]
    },
    {
      "id": "de-ro-furstenfeldbruck-filia-sf-apostoli-petru-si-pavel",
      "parent": "ro-germany",
      "kind": "parish",
      "rank": "Filial community",
      "name": "Romanian Orthodox Branch \"St. Apostles Peter and Paul\" in Fürstenfeldbruck",
      "local": "Filia \"Sf. Apostoli Petru şi Pavel\" - Fürstenfeldbruck",
      "country": "DE",
      "sources": [
        "https://mitropolia-ro.de/parohii-germania/"
      ],
      "address": [
        "Stockmeierweg 7, 82256 Fürstenfeldbruck"
      ]
    },
    {
      "id": "de-ro-furth-parohia-sf-cuv-parascheva-de-la-iasi",
      "parent": "ro-germany",
      "kind": "parish",
      "rank": "Parish",
      "name": "Romanian Orthodox Parish \"St. Cuv. Parascheva from Iași\" in Fürth",
      "local": "Parohia \"Sf. Cuv. Parascheva de la Iași\" - Fürth",
      "country": "DE",
      "sources": [
        "https://mitropolia-ro.de/parohii-germania/"
      ],
      "address": [
        "Markgrafenstraße 1 90513 Zirndorf"
      ]
    },
    {
      "id": "de-ro-garmisch-partenkirchen-parohia-sf-ier-nicolae-si-corbinian",
      "parent": "ro-germany",
      "kind": "parish",
      "rank": "Parish",
      "name": "Romanian Orthodox \"St. Ier. Nicholas and Corbinian\" Parish in Garmisch-Partenkirchen",
      "local": "Parohia \"Sf. Ier. Nicolae şi Corbinian\" - Garmisch-Partenkirchen",
      "country": "DE",
      "sources": [
        "https://mitropolia-ro.de/parohii-germania/"
      ],
      "address": [
        "Heilandkirche - Am Kirchbichl 8, 82496, Oberau"
      ]
    },
    {
      "id": "de-ro-gelsenkirchen-parohia-nasterea-sfantului-ioan-botezatorul",
      "parent": "ro-germany",
      "kind": "parish",
      "rank": "Parish",
      "name": "Romanian Orthodox Parish \"The Birth of Saint John the Baptist in Gelsenkirchen",
      "local": "Parohia \"Nașterea Sfântului Ioan Botezătorul - Gelsenkirchen",
      "country": "DE",
      "sources": [
        "https://mitropolia-ro.de/parohii-germania/"
      ],
      "address": [
        "Theodor-Otte-Straße 78, 45897 Gelsenkirchen"
      ]
    },
    {
      "id": "de-ro-giessen-parohia-inaltarea-sf-cruci",
      "parent": "ro-germany",
      "kind": "parish",
      "rank": "Parish",
      "name": "Romanian Orthodox Parish \"The Exaltation of the Holy Cross\" in Gießen",
      "local": "Parohia \"Înălţarea Sf. Cruci\" - Gießen",
      "country": "DE",
      "sources": [
        "https://mitropolia-ro.de/parohii-germania/"
      ],
      "address": [
        "Bismarckstr. 41, 35418 Großen Buseck"
      ]
    },
    {
      "id": "de-ro-gotha-erfurt-parohia-acoperamantul-maicii-domnului",
      "parent": "ro-germany",
      "kind": "parish",
      "rank": "Parish",
      "name": "Romanian Orthodox Parish \"The Covering of the Mother of God\" - Gotha in Gotha - Erfurt",
      "local": "Parohia \"Acoperământul Maicii Domnului\" - Gotha - Erfurt",
      "country": "DE",
      "sources": [
        "https://mitropolia-ro.de/parohii-germania/"
      ],
      "address": [
        "Südstrasse 4 B , 99867 Gotha"
      ]
    },
    {
      "id": "de-ro-gorlitz-filia-sf-m-mc-dimitrie-izvoratorul-de-mir",
      "parent": "ro-germany",
      "kind": "parish",
      "rank": "Filial community",
      "name": "Romanian Orthodox the branch of \"St. M. Mc. Demetrius the Fountain of Mir\" in Görlitz",
      "local": "filia \"Sf. M. Mc. Dimitrie Izvorâtorul de Mir\" - Görlitz",
      "country": "DE",
      "sources": [
        "https://mitropolia-ro.de/parohii-germania/"
      ],
      "address": [
        "biserica Sf. Jadwiga, Carolusstraße 51, 022827 Görlitz"
      ]
    },
    {
      "id": "de-ro-gottingen-parohia-sf-cuv-ghelasie-de-la-ramet",
      "parent": "ro-germany",
      "kind": "parish",
      "rank": "Parish",
      "name": "Romanian Orthodox Parish \"St. Cuv. Gelasie from Râmeț\" in Göttingen",
      "local": "Parohia \"Sf. Cuv. Ghelasie de la Râmeț\" - Göttingen",
      "country": "DE",
      "sources": [
        "https://mitropolia-ro.de/parohii-germania/"
      ],
      "address": [
        "St. Heinrich-Straße 5, 37081-Göttingen"
      ]
    },
    {
      "id": "de-ro-grosshennersdorf-filie",
      "parent": "ro-germany",
      "kind": "parish",
      "rank": "Filial community",
      "name": "Romanian Orthodox daughter in Großhennersdorf",
      "local": "filie - Großhennersdorf",
      "country": "DE",
      "sources": [
        "https://mitropolia-ro.de/parohii-germania/"
      ],
      "address": [
        "Kirchgasse 1, 02747 Herrnhut"
      ]
    },
    {
      "id": "de-ro-gschwend-filia-sf-imparati-constantin-si-elena",
      "parent": "ro-germany",
      "kind": "parish",
      "rank": "Filial community",
      "name": "Romanian Orthodox the branch of \"St. Emperors Constantine and Elena\" in Gschwend",
      "local": "filia \"Sf. Împărați Constantin și Elena\" - Gschwend",
      "country": "DE",
      "sources": [
        "https://mitropolia-ro.de/parohii-germania/"
      ],
      "address": [
        "Heilig Kreuz Kirche, Lindenstraße 28, 74417 Gschwend"
      ]
    },
    {
      "id": "de-ro-gummersbach-parohia-invierea-domnului-acoperamantul-maicii-domnului-si-sf-trei-ierarhi",
      "parent": "ro-germany",
      "kind": "parish",
      "rank": "Parish",
      "name": "Romanian Orthodox The \"Resurrection of the Lord\", \"Covering of the Mother of God\" and \"St. Three Hierarchs\" in Gummersbach",
      "local": "Parohia \"Învierea Domnului\", \"Acoperământul Maicii Domnului\" și \"Sf. Trei Ierarhi\" - Gummersbach",
      "country": "DE",
      "sources": [
        "https://mitropolia-ro.de/parohii-germania/"
      ],
      "address": [
        "Bickenbachstraße 98, 51643 Gummersbach"
      ]
    },
    {
      "id": "de-ro-gunzburg-parohia-sf-arh-mihail-si-gavriil",
      "parent": "ro-germany",
      "kind": "parish",
      "rank": "Parish",
      "name": "Romanian Orthodox Parish \"St. Arch. Michael and Gabriel\" in Günzburg",
      "local": "Parohia \"Sf. Arh. Mihail și Gavriil\" - Günzburg",
      "country": "DE",
      "sources": [
        "https://mitropolia-ro.de/parohii-germania/"
      ],
      "address": [
        "Peter-Henlein-Str. 5, 89331 Burgau"
      ]
    },
    {
      "id": "de-ro-gutersloh-parohia-sf-cuv-paisie-de-la-neamt",
      "parent": "ro-germany",
      "kind": "parish",
      "rank": "Parish",
      "name": "Romanian Orthodox \"St. Cuv. Paisie de la Neamț\" Parish in Gütersloh",
      "local": "Parohia \"Sf. Cuv. Paisie de la Neamț\" - Gütersloh",
      "country": "DE",
      "sources": [
        "https://mitropolia-ro.de/parohii-germania/"
      ],
      "address": [
        "Dr.-Thomas-Plaßmann-Weg, 33335 Gütersloh"
      ]
    },
    {
      "id": "de-ro-hagen-parohia-nasterea-maicii-domnului-si-sf-pr-mart-dumitru-staniloae",
      "parent": "ro-germany",
      "kind": "parish",
      "rank": "Parish",
      "name": "Romanian Orthodox Parish of \"The Nativity of the Mother of God\" and \"St. Pr. Mart. Dumitru Stăniloae\" in Hagen",
      "local": "Parohia \"Nașterea Maicii Domnului\" și \"Sf. Pr. Mărt. Dumitru Stăniloae\" - Hagen",
      "country": "DE",
      "sources": [
        "https://mitropolia-ro.de/parohii-germania/"
      ],
      "address": [
        "Büddingstraße 56, 58135 Hagen"
      ]
    },
    {
      "id": "de-ro-halle-saale-parohia-sf-prooroc-ilie-si-sf-mc-mauritiu",
      "parent": "ro-germany",
      "kind": "parish",
      "rank": "Parish",
      "name": "Romanian Orthodox \"St. Prophet Ilie\" and \"St. Mc. Mauriţiu\" Parish in Halle / Saale",
      "local": "Parohia \"Sf. Prooroc Ilie\" şi \"Sf. Mc. Mauriţiu\" - Halle / Saale",
      "country": "DE",
      "sources": [
        "https://mitropolia-ro.de/parohii-germania/"
      ],
      "address": [
        "Ernst-Thälmann-Str. 50, 06179 Teutschenthal"
      ]
    },
    {
      "id": "de-ro-hamburg-parohia-sf-ioan-botezatorul",
      "parent": "ro-germany",
      "kind": "parish",
      "rank": "Parish",
      "name": "Romanian Orthodox \"St. John the Baptist\" Parish in Hamburg",
      "local": "Parohia \"Sf. Ioan Botezătorul\" - Hamburg",
      "country": "DE",
      "sources": [
        "https://mitropolia-ro.de/parohii-germania/"
      ],
      "address": [
        "Tegelweg 151, 22159 Hamburg"
      ]
    },
    {
      "id": "de-ro-hamburg-harburg-parohia-sf-martiri-brancoveni-si-sf-ier-ansgar",
      "parent": "ro-germany",
      "kind": "parish",
      "rank": "Parish",
      "name": "Romanian Orthodox \"St. Martiri Brâncoveni\" and \"St. Ier. Ansgar\" parish in Hamburg-Harburg",
      "local": "Parohia \"Sf. Martiri Brâncoveni\" și \"Sf. Ier. Ansgar\" - Hamburg-Harburg",
      "country": "DE",
      "sources": [
        "https://mitropolia-ro.de/parohii-germania/"
      ],
      "address": [
        "Biserica St. Altfried, Am Felde 48, 21217 Seevetal"
      ]
    },
    {
      "id": "de-ro-hanau-parohia-sf-ioan-botezatorul",
      "parent": "ro-germany",
      "kind": "parish",
      "rank": "Parish",
      "name": "Romanian Orthodox \"St. John the Baptist\" Parish in Hanau",
      "local": "Parohia \"Sf. Ioan Botezătorul\" - Hanau",
      "country": "DE",
      "sources": [
        "https://mitropolia-ro.de/parohii-germania/"
      ],
      "address": [
        "Karlstr. 47, 63456 Hanau-Steinheim"
      ]
    },
    {
      "id": "de-ro-hannover-parohia-sf-cuv-paraschiva",
      "parent": "ro-germany",
      "kind": "parish",
      "rank": "Parish",
      "name": "Romanian Orthodox \"St. Cuv. Paraschiva\" Parish in Hannover",
      "local": "Parohia \"Sf. Cuv. Paraschiva\" - Hannover",
      "country": "DE",
      "sources": [
        "https://mitropolia-ro.de/parohii-germania/"
      ],
      "address": [
        "Spittastrasse 2, 30519 Hannover"
      ]
    },
    {
      "id": "de-ro-hasloh-filie",
      "parent": "ro-germany",
      "kind": "parish",
      "rank": "Filial community",
      "name": "Romanian Orthodox daughter in Hasloh",
      "local": "filie - Hasloh",
      "country": "DE",
      "sources": [
        "https://mitropolia-ro.de/parohii-germania/"
      ],
      "address": [
        "Kronkamp 8, 25474 Hasloh"
      ]
    },
    {
      "id": "de-ro-heidelberg-parohia-sfanta-treime",
      "parent": "ro-germany",
      "kind": "parish",
      "rank": "Parish",
      "name": "Romanian Orthodox \"Holy Trinity\" Parish in Heidelberg",
      "local": "Parohia \"Sfânta Treime\" - Heidelberg",
      "country": "DE",
      "sources": [
        "https://mitropolia-ro.de/parohii-germania/"
      ],
      "address": [
        "Christophstraße 2, 69214 Eppelheim"
      ]
    },
    {
      "id": "de-ro-heidenheim-an-der-brenz-parohia-sf-mc-pantelimon-si-sf-cuv-teodora-de-la-sihla",
      "parent": "ro-germany",
      "kind": "parish",
      "rank": "Parish",
      "name": "Romanian Orthodox \"St. Mc. Pantelimon\" and \"St. Cuv. Teodora de la Sihla\" parish in Heidenheim an der Brenz",
      "local": "Parohia \"Sf. Mc. Pantelimon\" și \"Sf. Cuv. Teodora de la Sihla\" - Heidenheim an der Brenz",
      "country": "DE",
      "sources": [
        "https://mitropolia-ro.de/parohii-germania/"
      ],
      "address": [
        "Iglauerstrasse 23, 89518 Heidenheim an der Brenz"
      ]
    },
    {
      "id": "de-ro-heilbronn-parohia-intrarea-in-biserica-a-maicii-domnului-si-sf-mc-kilian",
      "parent": "ro-germany",
      "kind": "parish",
      "rank": "Parish",
      "name": "Romanian Orthodox \"The Entry into the Church of the Mother of God\" and \"St. Mc. Kilian\" Parish in Heilbronn",
      "local": "Parohia \"Intrarea în biserică a Maicii Domnului\" și \"Sf. Mc. Kilian\" - Heilbronn",
      "country": "DE",
      "sources": [
        "https://mitropolia-ro.de/parohii-germania/"
      ],
      "address": [
        "Gartenstr. 8, 74177, Bad Friedrichshall"
      ]
    },
    {
      "id": "de-ro-hersbruck-parohia-sf-ier-nicolae-si-sf-cuv-gheorghe-de-la-cernica",
      "parent": "ro-germany",
      "kind": "parish",
      "rank": "Parish",
      "name": "Romanian Orthodox Parish of \"St. Ier. Nicolae\" and \"St. Cuv. Gheorghe de la Cernica\" in Hersbruck",
      "local": "Parohia \"Sf. Ier. Nicolae\" și \"Sf. Cuv. Gheorghe de la Cernica\" - Hersbruck",
      "country": "DE",
      "sources": [
        "https://mitropolia-ro.de/parohii-germania/"
      ],
      "address": [
        "Hans-Pirner-Str. 65, Ottensoos"
      ]
    },
    {
      "id": "de-ro-ingolstadt-parohia-sf-ierarh-calinic-de-la-cernica-si-sf-willibald-din-eichstatt",
      "parent": "ro-germany",
      "kind": "parish",
      "rank": "Parish",
      "name": "Romanian Orthodox Parish of \"St. Hierarch Calinic from Cernica\" and \"St. Willibald from Eichstätt\" in Ingolstadt",
      "local": "Parohia \"Sf. Ierarh Calinic de la Cernica\" și \"Sf. Willibald din Eichstätt\" - Ingolstadt",
      "country": "DE",
      "sources": [
        "https://mitropolia-ro.de/parohii-germania/"
      ],
      "address": [
        "Marienkirche, Regensburger Str. 192, 85055 Ingolstadt"
      ]
    },
    {
      "id": "de-ro-itzehoe-steinburg-parohia-nasterea-maicii-domnului-si-sf-martiri-nasaudeni",
      "parent": "ro-germany",
      "kind": "parish",
      "rank": "Parish",
      "name": "Romanian Orthodox Parish of \"The Nativity of the Mother of God\" and \"St. Martyrs Nasăudeni\" in Itzehoe / Steinburg",
      "local": "Parohia \"Nașterea Maicii Domnului\" și \"Sf. Martiri Năsăudeni\" - Itzehoe / Steinburg",
      "country": "DE",
      "sources": [
        "https://mitropolia-ro.de/parohii-germania/"
      ],
      "address": [
        "Lindenstraße 102A, 25548 Kellinghusen"
      ]
    },
    {
      "id": "de-ro-kaiserslautern-parohia-sf-mc-gheorghe-sf-cuv-parascheva",
      "parent": "ro-germany",
      "kind": "parish",
      "rank": "Parish",
      "name": "Romanian Orthodox Parish \"Sf. Mc. Gheorghe\", \"Sf. Cuv. Parascheva\" in Kaiserslautern",
      "local": "Parohia \"Sf. Mc. Gheorghe\", \"Sf. Cuv. Parascheva\" - Kaiserslautern",
      "country": "DE",
      "sources": [
        "https://mitropolia-ro.de/parohii-germania/"
      ],
      "address": [
        "Am Wäldchen 11, 67661 Kaiserslautern, Germania"
      ]
    },
    {
      "id": "de-ro-karlsruhe-parohia-nasterea-maicii-domnului",
      "parent": "ro-germany",
      "kind": "parish",
      "rank": "Parish",
      "name": "Romanian Orthodox Parish \"Nativity of the Mother of God\" in Karlsruhe",
      "local": "Parohia \"Naşterea Maicii Domnului\" - Karlsruhe",
      "country": "DE",
      "sources": [
        "https://mitropolia-ro.de/parohii-germania/"
      ],
      "address": [
        "Lutherkirche, Durlacher Allee 23, 76131 Karlsruhe"
      ]
    },
    {
      "id": "de-ro-kassel-parohia-buna-vestire",
      "parent": "ro-germany",
      "kind": "parish",
      "rank": "Parish",
      "name": "Romanian Orthodox \"Good Annunciation\" Parish in Kassel",
      "local": "Parohia \"Buna Vestire\" - Kassel",
      "country": "DE",
      "sources": [
        "https://mitropolia-ro.de/parohii-germania/"
      ],
      "address": [
        "Lassallestraße 2, 34119 Kassel"
      ]
    },
    {
      "id": "de-ro-kaufbeuren-filie",
      "parent": "ro-germany",
      "kind": "parish",
      "rank": "Filial community",
      "name": "Romanian Orthodox daughter in Kaufbeuren",
      "local": "filie - Kaufbeuren",
      "country": "DE",
      "sources": [
        "https://mitropolia-ro.de/parohii-germania/"
      ],
      "address": [
        "Augsburgerstr. 8, 87600 Kaufbeuren"
      ]
    },
    {
      "id": "de-ro-kempten-parohia-sf-ioan-de-la-suceava-si-sf-ierarh-bonifatiu",
      "parent": "ro-germany",
      "kind": "parish",
      "rank": "Parish",
      "name": "Romanian Orthodox \"St. John of Suceava\" and \"St. Hierarch Boniface\" Parish in Kempten",
      "local": "Parohia \"Sf. Ioan de la Suceava\" și \"Sf. Ierarh Bonifațiu\" - Kempten",
      "country": "DE",
      "sources": [
        "https://mitropolia-ro.de/parohii-germania/"
      ],
      "address": [
        "\"St. Michael\" Kirche, Memminger Str. 119, 87439 Kempten"
      ]
    },
    {
      "id": "de-ro-kiel-parohia-sf-ier-nicolae",
      "parent": "ro-germany",
      "kind": "parish",
      "rank": "Parish",
      "name": "Romanian Orthodox \"St. Ier. Nicholas\" Parish in Kiel",
      "local": "Parohia \"Sf. Ier. Nicolae\" - Kiel",
      "country": "DE",
      "sources": [
        "https://mitropolia-ro.de/parohii-germania/"
      ],
      "address": [
        "Erlöserkirche, Am Wohld 6, 24109 Kiel"
      ]
    },
    {
      "id": "de-ro-kirchheim-unter-teck-parohia-sf-treime",
      "parent": "ro-germany",
      "kind": "parish",
      "rank": "Parish",
      "name": "Romanian Orthodox \"Holy Trinity\" Parish in Kirchheim unter Teck",
      "local": "Parohia \"Sf. Treime\" - Kirchheim unter Teck",
      "country": "DE",
      "sources": [
        "https://mitropolia-ro.de/parohii-germania/"
      ],
      "address": [
        "Donntalstr.3 73252 Lenningen"
      ]
    },
    {
      "id": "de-ro-kleve-parohia-buna-vestire-si-sf-cuv-vasile-de-la-poiana-marului",
      "parent": "ro-germany",
      "kind": "parish",
      "rank": "Parish",
      "name": "Romanian Orthodox \"Buna Vestire\" and \"St. Vasile de la Poiana Mărului\" parish in Kleve",
      "local": "Parohia \"Buna Vestire\" și \"Sf. Cuv. Vasile de la Poiana Mărului\" - Kleve",
      "country": "DE",
      "sources": [
        "https://mitropolia-ro.de/parohii-germania/"
      ],
      "address": [
        "Hermespl. 15, 47533 Kleve-Warbeyen"
      ]
    },
    {
      "id": "de-ro-koblenz-parohia-botezul-domnului-si-sf-mc-laurentiu",
      "parent": "ro-germany",
      "kind": "parish",
      "rank": "Parish",
      "name": "Romanian Orthodox \"Baptism of God\" and \"St. Mc. Lawrence\" Parish in Koblenz",
      "local": "Parohia \"Botezul Domnului\" şi \"Sf. Mc. Laurenţiu\" - Koblenz",
      "country": "DE",
      "sources": [
        "https://mitropolia-ro.de/parohii-germania/"
      ],
      "address": [
        "Koblenzer Strasse 14, 56073 Koblenz (duminica);"
      ]
    },
    {
      "id": "de-ro-konstanz-parohia-pogorarea-sfantului-duh-si-sf-cuv-teodora-de-la-sihla",
      "parent": "ro-germany",
      "kind": "parish",
      "rank": "Parish",
      "name": "Romanian Orthodox \"Descent of the Holy Spirit\" and \"Saint Teodora de la Sihla\" Parish in Konstanz",
      "local": "Parohia \"Pogorârea Sfântului Duh\" și \"Sf. Cuv. Teodora de la Sihla\" - Konstanz",
      "country": "DE",
      "sources": [
        "https://mitropolia-ro.de/parohii-germania/"
      ],
      "address": [
        "Petruskirche,Wollmatingerstr. 58, 78467 Konstanz"
      ]
    },
    {
      "id": "de-ro-koln-parohia-duminica-tuturor-sfintilor",
      "parent": "ro-germany",
      "kind": "parish",
      "rank": "Parish",
      "name": "Romanian Orthodox \"Sunday of All Saints\" Parish in Köln",
      "local": "Parohia \"Duminica Tuturor Sfinţilor\" - Köln",
      "country": "DE",
      "sources": [
        "https://mitropolia-ro.de/parohii-germania/"
      ],
      "address": [
        "St. Elisabeth, Elisabeth-Breuer-Str. 48, 51065 Köln/Mülheim"
      ]
    },
    {
      "id": "de-ro-koln-parohia-pogorarea-sfantului-duh-sf-arhid-stefan-si-sf-mc-ursula",
      "parent": "ro-germany",
      "kind": "parish",
      "rank": "Parish",
      "name": "Romanian Orthodox \"Descent of the Holy Spirit\", \"St. Archid. Stefan\" and \"St. Mc. Ursula\" parish in Köln",
      "local": "Parohia \"Pogorârea Sfântului Duh\", \"Sf. Arhid. Ștefan\" și \"Sf. Mc. Ursula\" - Köln",
      "country": "DE",
      "sources": [
        "https://mitropolia-ro.de/parohii-germania/"
      ],
      "address": [
        "Decksteiner Str. 5, 50935 Köln (în cartierul Lindenthal)"
      ]
    },
    {
      "id": "de-ro-krefeld-parohia-sf-ap-andrei-si-sf-martiri-brancoveni",
      "parent": "ro-germany",
      "kind": "parish",
      "rank": "Parish",
      "name": "Romanian Orthodox \"St. Ap. Andrei\" and \"St. Martiri Brâncoveni\" Parish in Krefeld",
      "local": "Parohia \"Sf. Ap. Andrei\" și \"Sf. Martiri Brâncoveni\" - Krefeld",
      "country": "DE",
      "sources": [
        "https://mitropolia-ro.de/parohii-germania/"
      ],
      "address": [
        "Bahnhofstraße 12, 47447 Moers"
      ]
    },
    {
      "id": "de-ro-krefeld-parohia-sf-arh-mihail-si-gavriil-si-sf-cuv-onufrie-de-la-vorona",
      "parent": "ro-germany",
      "kind": "parish",
      "rank": "Parish",
      "name": "Romanian Orthodox \"St. Arch. Mihail and Gavriil\" and \"St. Cuv. Onufrie de la Vorona\" parish in Krefeld",
      "local": "Parohia \"Sf. Arh. Mihail și Gavriil\" și \"Sf. Cuv. Onufrie de la Vorona\" - Krefeld",
      "country": "DE",
      "sources": [
        "https://mitropolia-ro.de/parohii-germania/"
      ],
      "address": [
        "Hubertusstraße 226, 47798 Krefeld"
      ]
    },
    {
      "id": "de-ro-kunzelsau-parohia-sf-ier-nicolae-si-sf-cuv-ioan-iacob-de-la-neamt-vacanta",
      "parent": "ro-germany",
      "kind": "parish",
      "rank": "Parish",
      "name": "Romanian Orthodox Parish of \"St. Ier. Nicolae\" and \"St. Cuv. Ioan Jacob de la Neamț\" - vacation in Künzelsau",
      "local": "Parohia \"Sf. Ier. Nicolae\" și \"Sf. Cuv. Ioan Iacob de la Neamț\" - vacantă - Künzelsau",
      "country": "DE",
      "sources": [
        "https://mitropolia-ro.de/parohii-germania/"
      ],
      "address": [
        "Kirchgasse 5, 74653 Künzelsau"
      ]
    },
    {
      "id": "de-ro-lahr-parohia-sf-ier-grigorie-palama-si-sf-cuv-arsenie-de-la-prislop",
      "parent": "ro-germany",
      "kind": "parish",
      "rank": "Parish",
      "name": "Romanian Orthodox \"St. Ier. Grigorie Palama\" and \"St. Cuv. Arsenie de la Prislop\" parish in Lahr",
      "local": "Parohia \"Sf. Ier. Grigorie Palama\" și \"Sf. Cuv. Arsenie de la Prislop\" - Lahr",
      "country": "DE",
      "sources": [
        "https://mitropolia-ro.de/parohii-germania/"
      ],
      "address": [
        "Jammstrasse 2, 77933 Lahr/Schwarzwald"
      ]
    },
    {
      "id": "de-ro-landau-in-der-pfalz-parohia-sfintii-trei-ierarhi",
      "parent": "ro-germany",
      "kind": "parish",
      "rank": "Parish",
      "name": "Romanian Orthodox \"Three Holy Hierarchs\" Parish in Landau in der Pfalz",
      "local": "Parohia \"Sfinții Trei Ierarhi\" - Landau in der Pfalz",
      "country": "DE",
      "sources": [
        "https://mitropolia-ro.de/parohii-germania/"
      ],
      "address": [
        "Herrengasse 6-8, 76872 Minfeld"
      ]
    },
    {
      "id": "de-ro-landsberg-am-lech-parohia-nasterea-maicii-domnului-si-sf-mc-afra",
      "parent": "ro-germany",
      "kind": "parish",
      "rank": "Parish",
      "name": "Romanian Orthodox Parish of \"The Nativity of the Mother of God\" and \"St. Mc. Afra\" in Landsberg am Lech",
      "local": "Parohia \"Nașterea Maicii Domnului\" și \"Sf. Mc. Afra\" - Landsberg am Lech",
      "country": "DE",
      "sources": [
        "https://mitropolia-ro.de/parohii-germania/"
      ],
      "address": [
        "Paul-Waldmann-Weg 3, 86929 Penzing"
      ]
    },
    {
      "id": "de-ro-landshut-parohia-sf-ioan-valahul",
      "parent": "ro-germany",
      "kind": "parish",
      "rank": "Parish",
      "name": "Romanian Orthodox \"St. Ioan Valahul\" Parish in Landshut",
      "local": "Parohia \"Sf. Ioan Valahul\" - Landshut",
      "country": "DE",
      "sources": [
        "https://mitropolia-ro.de/parohii-germania/"
      ],
      "address": [
        "Marienplatz 9, 84036 Landshut"
      ]
    },
    {
      "id": "de-ro-leipzig-parohia-sf-m-mc-gheorghe",
      "parent": "ro-germany",
      "kind": "parish",
      "rank": "Parish",
      "name": "Romanian Orthodox Parish \"Sf. M. Mc. Gheorghe\" in Leipzig",
      "local": "Parohia \"Sf. M. Mc. Gheorghe\" - Leipzig",
      "country": "DE",
      "sources": [
        "https://mitropolia-ro.de/parohii-germania/"
      ],
      "address": [
        "Russenstr. 194, 04288 Leipzig"
      ]
    },
    {
      "id": "de-ro-leverkusen-parohia-inaltarea-domnului-sf-m-mc-ecaterina-si-sf-ier-remigius",
      "parent": "ro-germany",
      "kind": "parish",
      "rank": "Parish",
      "name": "Romanian Orthodox Parish of \"Ascension of the Lord\", \"St. M. Mc. Catherine\" and \"St. Jer. Remigius\" in Leverkusen",
      "local": "Parohia \"Înălțarea Domnului\", \"Sf. M. Mc. Ecaterina\" și \"Sf. Ier. Remigius\" - Leverkusen",
      "country": "DE",
      "sources": [
        "https://mitropolia-ro.de/parohii-germania/"
      ],
      "address": [
        "Kölner Str. 42, 51379 Leverkusen"
      ]
    },
    {
      "id": "de-ro-ludwigsburg-parohia-sfintii-apostoli-petru-si-pavel",
      "parent": "ro-germany",
      "kind": "parish",
      "rank": "Parish",
      "name": "Romanian Orthodox \"Saints Peter and Paul\" Parish in Ludwigsburg",
      "local": "Parohia \"Sfinții Apostoli Petru și Pavel\" - Ludwigsburg",
      "country": "DE",
      "sources": [
        "https://mitropolia-ro.de/parohii-germania/"
      ],
      "address": [
        "slujire duminicală: Neue Weingärten Str. 18, 71634 Ludwigsburg - Eglosheim și In Nonnenpfad 25, 71076 Unterriexingen"
      ]
    },
    {
      "id": "de-ro-lubeck-filie",
      "parent": "ro-germany",
      "kind": "parish",
      "rank": "Filial community",
      "name": "Romanian Orthodox daughter in Lübeck",
      "local": "filie - Lübeck",
      "country": "DE",
      "sources": [
        "https://mitropolia-ro.de/parohii-germania/"
      ],
      "address": [
        "Kleine Altefähre 6 a, 23552 Lübeck"
      ],
      "services": [
        "(slujbe în a 3-a duminică din lună)"
      ]
    },
    {
      "id": "de-ro-magdeburg-filie",
      "parent": "ro-germany",
      "kind": "parish",
      "rank": "Filial community",
      "name": "Romanian Orthodox daughter in Magdeburg",
      "local": "filie - Magdeburg",
      "country": "DE",
      "sources": [
        "https://mitropolia-ro.de/parohii-germania/"
      ]
    },
    {
      "id": "de-ro-mainz-gensingen-filie",
      "parent": "ro-germany",
      "kind": "parish",
      "rank": "Filial community",
      "name": "Romanian Orthodox subsidiary - Mainz in Mainz - Gensingen",
      "local": "filie - Mainz - Gensingen",
      "country": "DE",
      "sources": [
        "https://mitropolia-ro.de/parohii-germania/"
      ],
      "address": [
        "Kirche St. Martin, Römerstraße 25, 55457 Gensingen"
      ]
    },
    {
      "id": "de-ro-mannheim-parohia-invierea-domnului",
      "parent": "ro-germany",
      "kind": "parish",
      "rank": "Parish",
      "name": "Romanian Orthodox \"Resurrection of the Lord\" Parish in Mannheim",
      "local": "Parohia \"Învierea Domnului\" - Mannheim",
      "country": "DE",
      "sources": [
        "https://mitropolia-ro.de/parohii-germania/"
      ],
      "address": [
        "Alter Postweg 12-14, 68309 Mannheim"
      ]
    },
    {
      "id": "de-ro-melle-parohia-sf-ap-bartolomeu-si-sf-ier-iosif-cel-nou-de-la-partos",
      "parent": "ro-germany",
      "kind": "parish",
      "rank": "Parish",
      "name": "Romanian Orthodox The parish of St. Rev. Bartholomew\" and \"St. Ier. Joseph the New from Partoș\" in Melle",
      "local": "Parohia ,,Sf. Ap. Bartolomeu\" și ,,Sf.Ier. Iosif cel Nou de la Partoș\" - Melle",
      "country": "DE",
      "sources": [
        "https://mitropolia-ro.de/parohii-germania/"
      ],
      "address": [
        "Am Kirchpl.16, 49326 Melle-Wellingholzhausen"
      ]
    },
    {
      "id": "de-ro-memmingen-parohia-nasterea-maicii-domnului-si-sf-ier-rupert-din-salzburg-vacanta",
      "parent": "ro-germany",
      "kind": "parish",
      "rank": "Parish",
      "name": "Romanian Orthodox Parish of \"The Nativity of the Mother of God\" and \"St. Jer. Rupert of Salzburg\" - vacant in Memmingen",
      "local": "Parohia \"Nașterea Maicii Domnului\" și \"Sf. Ier. Rupert din Salzburg\" - vacantă - Memmingen",
      "country": "DE",
      "sources": [
        "https://mitropolia-ro.de/parohii-germania/"
      ],
      "address": [
        "Kirchengässchen 1, 87766 Memmingerberg"
      ]
    },
    {
      "id": "de-ro-miesbach-parohia-intrarea-in-biserica-maicii-domnului-si-sf-mc-alexander-schmorell",
      "parent": "ro-germany",
      "kind": "parish",
      "rank": "Parish",
      "name": "Romanian Orthodox Parish \"Entrance to the Church of the Mother of God\" and \"St. Mc. Alexander Schmorell\" in Miesbach",
      "local": "Parohia \"Intrarea în biserică Maicii Domnului\" și \"Sf. Mc. Alexander Schmorell\" - Miesbach",
      "country": "DE",
      "sources": [
        "https://mitropolia-ro.de/parohii-germania/"
      ],
      "address": [
        "Münchener Straße 5, 83714 Miesbach"
      ]
    },
    {
      "id": "de-ro-minden-parohia-buna-vestire-si-sf-proor-ilie-tesviteanul",
      "parent": "ro-germany",
      "kind": "parish",
      "rank": "Parish",
      "name": "Romanian Orthodox \"Buna Vestire\" and \"St. Proor. Ilie Tesviteanul\" parish in Minden",
      "local": "Parohia \"Buna Vestire\" și \"Sf. Proor. Ilie Tesviteanul\" - Minden",
      "country": "DE",
      "sources": [
        "https://mitropolia-ro.de/parohii-germania/"
      ],
      "address": [
        "Ovelgönner Weg 31, 32549 Bad Oeynhausen"
      ]
    },
    {
      "id": "de-ro-monchengladbach-parohia-sf-ier-calinic-de-la-cernica",
      "parent": "ro-germany",
      "kind": "parish",
      "rank": "Parish",
      "name": "Romanian Orthodox Parish \"St. Ier. Calinic from Cernica\" in Mönchengladbach",
      "local": "Parohia \"Sf. Ier. Calinic de la Cernica\" - Mönchengladbach",
      "country": "DE",
      "sources": [
        "https://mitropolia-ro.de/parohii-germania/"
      ],
      "address": [
        "Dechant-Stroux-Straße 22, 41748 Viersen"
      ]
    },
    {
      "id": "de-ro-munchen-centrul-bisericesc-inaltarea-sf-cruci-si-sf-ier-calinic-de-la-cernica",
      "parent": "ro-germany",
      "kind": "parish",
      "rank": "Parish",
      "name": "Romanian Orthodox Church Center \"The Ascension of St. Cruci\" and \"St. Ier. Calinic from Cernica\" in München",
      "local": "Centrul Bisericesc \"Înălțarea sf. Cruci\" și \"Sf. Ier. Calinic de la Cernica\" - München",
      "country": "DE",
      "sources": [
        "https://mitropolia-ro.de/parohii-germania/"
      ],
      "address": [
        "Kastelburgstr. 84-88, 81245 München"
      ]
    },
    {
      "id": "de-ro-munchen-manastirea-sf-cuv-siluan-athonitul",
      "parent": "ro-germany",
      "kind": "monastery",
      "rank": "Monastery",
      "name": "Romanian Orthodox \"St. Cuv. Siluan Athonite\" monastery in München",
      "local": "Mănăstirea \"Sf. Cuv. Siluan Athonitul\" - München",
      "country": "DE",
      "sources": [
        "https://mitropolia-ro.de/parohii-germania/"
      ],
      "address": [
        "Kastelburgstr. 84-88, 81245 München"
      ]
    },
    {
      "id": "de-ro-munchen-parohia-nasterea-domnului",
      "parent": "ro-germany",
      "kind": "parish",
      "rank": "Parish",
      "name": "Romanian Orthodox \"Nativity of God\" Parish in München",
      "local": "Parohia \"Naşterea Domnului\" - München",
      "country": "DE",
      "sources": [
        "https://mitropolia-ro.de/parohii-germania/"
      ],
      "address": [
        "St. Willibrord, Blumenstraße 36, 80331 München"
      ]
    },
    {
      "id": "de-ro-munster-parohia-sf-ier-spiridon-si-sf-mc-petronilla",
      "parent": "ro-germany",
      "kind": "parish",
      "rank": "Parish",
      "name": "Romanian Orthodox Parish of \"St. Jer. Spiridon\" and \"St. Mc. Petronilla\" in Münster",
      "local": "Parohia \"Sf. Ier. Spiridon\" și \"Sf. Mc. Petronilla\" - Münster",
      "country": "DE",
      "sources": [
        "https://mitropolia-ro.de/parohii-germania/"
      ],
      "address": [
        "Dyckburgstraße 222, 48157, Münster"
      ]
    },
    {
      "id": "de-ro-nagold-parohia-sf-pror-david-si-sf-ier-bonifatie",
      "parent": "ro-germany",
      "kind": "parish",
      "rank": "Parish",
      "name": "Romanian Orthodox Parish of \"St. Pror. David\" and \"St. Jer. Boniface\" in Nagold",
      "local": "Parohia \"Sf. Pror. David\" și \"Sf. Ier. Bonifatie\" - Nagold",
      "country": "DE",
      "sources": [
        "https://mitropolia-ro.de/parohii-germania/"
      ],
      "address": [
        "Öschelbronner Str. 35, 71131 Jettingen"
      ]
    },
    {
      "id": "de-ro-neuburg-parohia-sf-imparati-constantin-si-elena",
      "parent": "ro-germany",
      "kind": "parish",
      "rank": "Parish",
      "name": "Romanian Orthodox \"St. Emperors Constantine and Elena\" Parish in Neuburg",
      "local": "Parohia \"Sf. Împărați Constantin și Elena\" - Neuburg",
      "country": "DE",
      "sources": [
        "https://mitropolia-ro.de/parohii-germania/"
      ],
      "address": [
        "Bahnhofstraße 104, 86633 Neuburg an der Donau"
      ]
    },
    {
      "id": "de-ro-neumarkt-in-der-oberpfalz-parohia-sf-mc-marina",
      "parent": "ro-germany",
      "kind": "parish",
      "rank": "Parish",
      "name": "Romanian Orthodox \"St. Mc. Marina\" Parish in Neumarkt in der Oberpfalz",
      "local": "Parohia \"Sf. Mc. Marina\" - Neumarkt in der Oberpfalz",
      "country": "DE",
      "sources": [
        "https://mitropolia-ro.de/parohii-germania/"
      ],
      "address": [
        "Wildbad 1, 92318 Neumarkt in der Oberpfalz"
      ]
    },
    {
      "id": "de-ro-neuss-parohia-adormirea-maicii-domnului-si-sf-mc-ioan-cel-nou-de-la-suceava",
      "parent": "ro-germany",
      "kind": "parish",
      "rank": "Parish",
      "name": "Romanian Orthodox Parish \"Assumption of the Virgin Mary\" and \"St. Mc. John the New from Suceava\" in Neuss",
      "local": "Parohia \"Adormirea Maicii Domnului\" și \"Sf. Mc. Ioan cel Nou de la Suceava\" - Neuss",
      "country": "DE",
      "sources": [
        "https://mitropolia-ro.de/parohii-germania/"
      ],
      "address": [
        "Blücherstraße 20, 41460 Neuss"
      ]
    },
    {
      "id": "de-ro-norderney-filia-buna-vestire",
      "parent": "ro-germany",
      "kind": "parish",
      "rank": "Filial community",
      "name": "Romanian Orthodox Branch \"Good News\" in Norderney",
      "local": "Filia \"Buna Vestire\" - Norderney",
      "country": "DE",
      "sources": [
        "https://mitropolia-ro.de/parohii-germania/"
      ],
      "address": [
        "Goebenstraße 1b, 26548 Norderney"
      ],
      "services": [
        "(slujbe în prima sâmbătă din lună)"
      ]
    },
    {
      "id": "de-ro-nordlingen-filie",
      "parent": "ro-germany",
      "kind": "parish",
      "rank": "Filial community",
      "name": "Romanian Orthodox daughter in Nördlingen",
      "local": "filie - Nördlingen",
      "country": "DE",
      "sources": [
        "https://mitropolia-ro.de/parohii-germania/"
      ],
      "address": [
        "Im Brühl 1, 86751 Mönchsdeggingen"
      ]
    },
    {
      "id": "de-ro-nurnberg-manastirea-sf-martiri-brancoveni-nurnberg",
      "parent": "ro-germany",
      "kind": "monastery",
      "rank": "Monastery",
      "name": "Romanian Orthodox \"St. Martiri Brancoveni\" monastery Nuremberg in Nürnberg",
      "local": "Mănăstirea \"Sf. Martiri Brâncoveni\" Nürnberg - Nürnberg",
      "country": "DE",
      "sources": [
        "https://mitropolia-ro.de/parohii-germania/"
      ],
      "address": [
        "Fürther Str. 166-168, 90429 Nürnberg"
      ],
      "services": [
        "Slujire în zilele de peste săptămână (8:00 respectiv 17:00); vinerea - Sf. Maslu (17:00); Sf. Liturghie duminicală, de la orele 9:45"
      ]
    },
    {
      "id": "de-ro-nurnberg-parohia-sf-mc-dimitrie-izvoratorul-de-mir",
      "parent": "ro-germany",
      "kind": "parish",
      "rank": "Parish",
      "name": "Romanian Orthodox Parish \"St. Mc. Dimitrie Izvorâtorul de Mir\" in Nürnberg",
      "local": "Parohia \"Sf. Mc. Dimitrie Izvorâtorul de Mir\" - Nürnberg",
      "country": "DE",
      "sources": [
        "https://mitropolia-ro.de/parohii-germania/"
      ],
      "address": [
        "Fürther Str. 166, 90429 Nürnberg"
      ]
    },
    {
      "id": "de-ro-nurnberg-ii-langwasser-parohia-sf-ier-vasile-cel-mare-si-izvorul-tamaduirii",
      "parent": "ro-germany",
      "kind": "parish",
      "rank": "Parish",
      "name": "Romanian Orthodox Parish of \"St. Ier. Basil the Great\" and \"Izvorul Tămăduirii\" - Nuremberg II in Nürnberg II - Langwasser",
      "local": "Parohia \"Sf. Ier. Vasile cel Mare\" și \"Izvorul Tămăduirii\" - Nürnberg II - Langwasser",
      "country": "DE",
      "sources": [
        "https://mitropolia-ro.de/parohii-germania/"
      ],
      "address": [
        "Dr.-Linnert-Ring 30, 90473 Nürnberg"
      ]
    },
    {
      "id": "de-ro-offenbach-am-main-parohia-sf-ier-nicolae",
      "parent": "ro-germany",
      "kind": "parish",
      "rank": "Parish",
      "name": "Romanian Orthodox \"St. Ier. Nicholas\" Parish in Offenbach am Main",
      "local": "Parohia \"Sf. Ier. Nicolae\" - Offenbach am Main",
      "country": "DE",
      "sources": [
        "https://mitropolia-ro.de/parohii-germania/"
      ],
      "address": [
        "Backstr. 16, 63069 Offenbach am Main"
      ]
    },
    {
      "id": "de-ro-offenburg-parohia-sfanta-treime",
      "parent": "ro-germany",
      "kind": "parish",
      "rank": "Parish",
      "name": "Romanian Orthodox \"Holy Trinity\" Parish in Offenburg",
      "local": "Parohia \"Sfânta Treime\" - Offenburg",
      "country": "DE",
      "sources": [
        "https://mitropolia-ro.de/parohii-germania/"
      ],
      "address": [
        "Haydnstrasse 1, 77694 Kehl"
      ]
    },
    {
      "id": "de-ro-oldenburg-parohia-sf-ap-andrei-si-sf-ier-willehad",
      "parent": "ro-germany",
      "kind": "parish",
      "rank": "Parish",
      "name": "Romanian Orthodox \"St. Ap. Andrew\" and \"St. Jer. Willehad\" Parish in Oldenburg",
      "local": "Parohia \"Sf. Ap. Andrei\" și \"Sf. Ier. Willehad\" - Oldenburg",
      "country": "DE",
      "sources": [
        "https://mitropolia-ro.de/parohii-germania/"
      ],
      "address": [
        "Litteler Str. 6, 26203 Wardenburg"
      ]
    },
    {
      "id": "de-ro-olpe-filia-sf-ier-luca-al-crimeei-si-sf-cuv-cleopa-si-paisie-de-la-sihastria",
      "parent": "ro-germany",
      "kind": "parish",
      "rank": "Filial community",
      "name": "Romanian Orthodox filia \"St. Ier. Luke of Crimea\" and \"St. Cuv. Cleopa and Paisie from Sihăstria\" in Olpe",
      "local": "filia \"Sf. Ier. Luca al Crimeei\" și \"Sf. Cuv. Cleopa și Paisie de la Sihăstria\" - Olpe",
      "country": "DE",
      "sources": [
        "https://mitropolia-ro.de/parohii-germania/"
      ],
      "address": [
        "Kreuzkapelle, Am Bratzkopf 57462 Olpe"
      ]
    },
    {
      "id": "de-ro-osnabruck-parohia-sf-teodosie-de-la-brazi-si-sf-cuv-parascheva-de-la-iasi",
      "parent": "ro-germany",
      "kind": "parish",
      "rank": "Parish",
      "name": "Romanian Orthodox \"St. Teodosie de la Brazi\" and \"St. Cuv. Parascheva de la Iași\" parish in Osnabrück",
      "local": "Parohia \"Sf. Teodosie de la Brazi\" și \"Sf. Cuv. Parascheva de la Iași\" - Osnabrück",
      "country": "DE",
      "sources": [
        "https://mitropolia-ro.de/parohii-germania/"
      ],
      "address": [
        "Wasserwerkstraße 79, 49086 Osnabrück"
      ]
    },
    {
      "id": "de-ro-paderborn-parohia-nasterea-maicii-domnului-si-sf-ier-liborius",
      "parent": "ro-germany",
      "kind": "parish",
      "rank": "Parish",
      "name": "Romanian Orthodox Parish of \"The Nativity of the Mother of God\" and \"St. Jer. Liborius\" in Paderborn",
      "local": "Parohia \"Naşterea Maicii Domnului\" şi \"Sf. Ier. Liborius\" - Paderborn",
      "country": "DE",
      "sources": [
        "https://mitropolia-ro.de/parohii-germania/"
      ],
      "address": [
        "Burgstr. 4, 33142 Büren"
      ]
    },
    {
      "id": "de-ro-papenburg-filia-sf-ap-petru-si-pavel-sf-ap-iacov-si-sf-ier-nectarie",
      "parent": "ro-germany",
      "kind": "parish",
      "rank": "Filial community",
      "name": "Romanian Orthodox Filia \"St. Ap. Peter and Paul\", St. Ap. Iacov\" and \"St. Jer. Nectary\" in Papenburg",
      "local": "Filia \"Sf. Ap. Petru și Pavel\", Sf. Ap. Iacov\" și \"Sf. Ier. Nectarie\" - Papenburg",
      "country": "DE",
      "sources": [
        "https://mitropolia-ro.de/parohii-germania/"
      ],
      "address": [
        "Kirchstr. 14, 26871 Papenburg"
      ],
      "services": [
        "(slujbe în prima duminică din lună)"
      ]
    },
    {
      "id": "de-ro-passau-vilshofen-parohia-acoperamantul-maicii-domnului",
      "parent": "ro-germany",
      "kind": "parish",
      "rank": "Parish",
      "name": "Romanian Orthodox Parish \"Coverage of the Mother of God\" in Passau-Vilshofen",
      "local": "Parohia \"Acoperământul Maicii Domnului\" - Passau-Vilshofen",
      "country": "DE",
      "sources": [
        "https://mitropolia-ro.de/parohii-germania/"
      ],
      "address": [
        "Aidenbacher Str. 92, 94474 Vilshofen an der Donau"
      ]
    },
    {
      "id": "de-ro-perleberg-prignitz-parohia-intrarea-maicii-domnului-in-biserica-si-sf-ierarh-nicolae",
      "parent": "ro-germany",
      "kind": "parish",
      "rank": "Parish",
      "name": "Romanian Orthodox The parish \"The Entry of the Mother of God into the Church\" and \"St. Hierarch Nicholas\" in Perleberg (Prignitz)",
      "local": "Parohia \"Intrarea Maicii Domnului in Biserica\" si \"Sf. Ierarh Nicolae\" - Perleberg (Prignitz)",
      "country": "DE",
      "sources": [
        "https://mitropolia-ro.de/parohii-germania/"
      ],
      "address": [
        "Dorfkirche Quitzow, Dorfstraße 37, 19348 Perleberg"
      ]
    },
    {
      "id": "de-ro-pfaffenhofen-an-der-ilm-parohia-pogorarea-sfantului-duh",
      "parent": "ro-germany",
      "kind": "parish",
      "rank": "Parish",
      "name": "Romanian Orthodox \"Descent of the Holy Spirit\" Parish in Pfaffenhofen an der Ilm",
      "local": "Parohia \"Pogorârea Sfântului Duh\" - Pfaffenhofen an der Ilm",
      "country": "DE",
      "sources": [
        "https://mitropolia-ro.de/parohii-germania/"
      ],
      "address": [
        "Hauptplatz 34, 85276 Pfaffenhofen"
      ]
    },
    {
      "id": "de-ro-pfarrkirchen-parohia-sf-ier-iosif-de-la-partos",
      "parent": "ro-germany",
      "kind": "parish",
      "rank": "Parish",
      "name": "Romanian Orthodox Parish \"St. Jer. Joseph from Partos\" in Pfarrkirchen",
      "local": "Parohia \"Sf. Ier. Iosif de la Partoș\" - Pfarrkirchen",
      "country": "DE",
      "sources": [
        "https://mitropolia-ro.de/parohii-germania/"
      ],
      "address": [
        "Franziskaner Klosterkirche 1, Eggenfelden, 84307"
      ]
    },
    {
      "id": "de-ro-pforzheim-parohia-sf-mc-zotic-atal-camasie-si-filip-de-la-niculitel",
      "parent": "ro-germany",
      "kind": "parish",
      "rank": "Parish",
      "name": "Romanian Orthodox Parish \"St. Mc. Zotic, Atal, Camasie and Filip de la Niculitel\" in Pforzheim",
      "local": "Parohia \"Sf. Mc. Zotic, Atal, Camasie și Filip de la Niculițel\" - Pforzheim",
      "country": "DE",
      "sources": [
        "https://mitropolia-ro.de/parohii-germania/"
      ],
      "address": [
        "Obere Stöckstraße 1 75180 Pforzheim Büchenbronn"
      ]
    },
    {
      "id": "de-ro-plauen-parohia-sf-ioan-iacob-hozevitul-de-la-neamt",
      "parent": "ro-germany",
      "kind": "parish",
      "rank": "Parish",
      "name": "Romanian Orthodox Parish \"St. Ioan Iacob the Hozevit from Neamt\" in Plauen",
      "local": "Parohia \"Sf. Ioan Iacob Hozevitul de la Neamț\" - Plauen",
      "country": "DE",
      "sources": [
        "https://mitropolia-ro.de/parohii-germania/"
      ],
      "address": [
        "Friedlerstrasse ° 10, 08525 Plauen"
      ]
    },
    {
      "id": "de-ro-potsdam-parohia-sf-cuv-paisie-de-la-neamt",
      "parent": "ro-germany",
      "kind": "parish",
      "rank": "Parish",
      "name": "Romanian Orthodox Parish \"St. Cuv. Paisie from Neamt\" in Potsdam",
      "local": "Parohia \"Sf. Cuv. Paisie de la Neamț\" - Potsdam",
      "country": "DE",
      "sources": [
        "https://mitropolia-ro.de/parohii-germania/"
      ],
      "address": [
        "Geiselbergstraße 52, 14476 Potsdam-Golm"
      ]
    },
    {
      "id": "de-ro-ravensburg-parohia-sf-m-mc-gheorghe",
      "parent": "ro-germany",
      "kind": "parish",
      "rank": "Parish",
      "name": "Romanian Orthodox Parish \"St. M. Mc. George\" in Ravensburg",
      "local": "Parohia \"Sf. M. Mc. Gheorghe\" - Ravensburg",
      "country": "DE",
      "sources": [
        "https://mitropolia-ro.de/parohii-germania/"
      ],
      "address": [
        "Ravensburger Str. 41, 88250 Weingarten"
      ]
    },
    {
      "id": "de-ro-recklinghausen-parohia-sf-cuv-parascheva-de-la-iasi-si-sf-cuv-serafim-de-sarov",
      "parent": "ro-germany",
      "kind": "parish",
      "rank": "Parish",
      "name": "Romanian Orthodox Parish \"St. Cuv. Parascheva from Iasi\" and \"St. Cuv. Seraphim of Sarov\" in Recklinghausen",
      "local": "Parohia \"Sf. Cuv. Parascheva de la Iași\" și \"Sf. Cuv. Serafim de Sarov\" - Recklinghausen",
      "country": "DE",
      "sources": [
        "https://mitropolia-ro.de/parohii-germania/"
      ],
      "address": [
        "Friedrich-Ebert-Straße 231, 45659 Recklinghausen"
      ]
    },
    {
      "id": "de-ro-reutlingen-filie",
      "parent": "ro-germany",
      "kind": "parish",
      "rank": "Filial community",
      "name": "Romanian Orthodox daughter in Reutlingen",
      "local": "filie - Reutlingen",
      "country": "DE",
      "sources": [
        "https://mitropolia-ro.de/parohii-germania/"
      ],
      "address": [
        "Christuskirche, Lohmühlestraße 30, 72762 Reutlingen"
      ],
      "services": [
        "(slujbe în a doua duminică din lună)"
      ]
    },
    {
      "id": "de-ro-rheine-parohia-sf-arh-mihail-si-gavriil-si-sf-ier-nectarie-de-eghina",
      "parent": "ro-germany",
      "kind": "parish",
      "rank": "Parish",
      "name": "Romanian Orthodox Parish \"St. Arch. Michael and Gabriel\" and \"St. Jer. Nectaria of Aegina\" in Rheine",
      "local": "Parohia \"Sf. Arh. Mihail și Gavriil\" și \"Sf. Ier. Nectarie de Eghina\" - Rheine",
      "country": "DE",
      "sources": [
        "https://mitropolia-ro.de/parohii-germania/"
      ],
      "address": [
        "Kirchstraße 4, 48432 Rheine"
      ]
    },
    {
      "id": "de-ro-rheda-wiedenbruck-parohia-sfintii-arhangheli",
      "parent": "ro-germany",
      "kind": "parish",
      "rank": "Parish",
      "name": "Romanian Orthodox \"Holy Archangels\" Parish in Rheda-Wiedenbrück",
      "local": "Parohia \"Sfinții Arhangheli\" - Rheda-Wiedenbrück",
      "country": "DE",
      "sources": [
        "https://mitropolia-ro.de/parohii-germania/"
      ],
      "address": [
        "Nonenstraße 96, 33378 Rheda-Wiedenbrück"
      ]
    },
    {
      "id": "de-ro-romnitz-schitul-sf-paisie-aghioritul-si-sf-procopie-din-lubeck",
      "parent": "ro-germany",
      "kind": "monastery",
      "rank": "Monastery",
      "name": "Romanian Orthodox Hermitage \"St. Paisie Aghiorit\" and \"St. Procopius of Lübeck\" in Römnitz",
      "local": "Schitul \"Sf. Paisie Aghioritul\" și \"Sf. Procopie din Lübeck\" - Römnitz",
      "country": "DE",
      "sources": [
        "https://mitropolia-ro.de/parohii-germania/"
      ],
      "address": [
        "Hoheleuchte 1, 23909 Römnitz"
      ]
    },
    {
      "id": "de-ro-rosenheim-parohia-intampinarea-domnului",
      "parent": "ro-germany",
      "kind": "parish",
      "rank": "Parish",
      "name": "Romanian Orthodox \"The Reception of the Lord\" Parish in Rosenheim",
      "local": "Parohia \"Întâmpinarea Domnului\" - Rosenheim",
      "country": "DE",
      "sources": [
        "https://mitropolia-ro.de/parohii-germania/"
      ],
      "address": [
        "Biserica Sf. Quirinius, Fürstätt 24, 83024 Rosenheim"
      ]
    },
    {
      "id": "de-ro-rostock-parohia-nasterea-maicii-domnului-si-sf-ier-iosif-cel-nou-de-la-partos",
      "parent": "ro-germany",
      "kind": "parish",
      "rank": "Parish",
      "name": "Romanian Orthodox The Parish of \"The Nativity of the Mother of God\" and \"St. Jer. Joseph the New from Partoș\" in Rostock",
      "local": "Parohia \"Nașterea Maicii Domnului\" și \"Sf. Ier. Iosif cel Nou de la Partoș\" - Rostock",
      "country": "DE",
      "sources": [
        "https://mitropolia-ro.de/parohii-germania/"
      ],
      "address": [
        "Reuteshäger Weg 4, 180069 Rostock"
      ]
    },
    {
      "id": "de-ro-saarbrucken-parohia-nasterea-maicii-domnului-si-sf-imparati-constantin-si-elena",
      "parent": "ro-germany",
      "kind": "parish",
      "rank": "Parish",
      "name": "Romanian Orthodox The Parish of \"The Nativity of the Mother of God\" and \"St. Emperors Constantine and Elena\" in Saarbrücken",
      "local": "Parohia \"Naşterea Maicii Domnului\" și \"Sf. Împărați Constantin și Elena\" - Saarbrücken",
      "country": "DE",
      "sources": [
        "https://mitropolia-ro.de/parohii-germania/"
      ],
      "address": [
        "Emsweg 2, 66115 Saarbrücken"
      ]
    },
    {
      "id": "de-ro-salzgitter-parohia-invierea-domnului",
      "parent": "ro-germany",
      "kind": "parish",
      "rank": "Parish",
      "name": "Romanian Orthodox \"Resurrection of the Lord\" Parish in Salzgitter",
      "local": "Parohia \"Învierea Domnului\" - Salzgitter",
      "country": "DE",
      "sources": [
        "https://mitropolia-ro.de/parohii-germania/"
      ],
      "address": [
        "Wehrstraße 14, 38226 Salzgitter"
      ]
    },
    {
      "id": "de-ro-schleswig-filie",
      "parent": "ro-germany",
      "kind": "parish",
      "rank": "Filial community",
      "name": "Romanian Orthodox daughter in Schleswig",
      "local": "filie - Schleswig",
      "country": "DE",
      "sources": [
        "https://mitropolia-ro.de/parohii-germania/"
      ],
      "address": [
        "Königsberger Str. 18, 24837 Schleswig"
      ]
    },
    {
      "id": "de-ro-schrobenhausen-parohia-sfintii-apostoli-petru-si-pavel",
      "parent": "ro-germany",
      "kind": "parish",
      "rank": "Parish",
      "name": "Romanian Orthodox \"Saints Peter and Paul\" Parish in Schrobenhausen",
      "local": "Parohia \"Sfinții Apostoli Petru și Pavel\" - Schrobenhausen",
      "country": "DE",
      "sources": [
        "https://mitropolia-ro.de/parohii-germania/"
      ],
      "address": [
        "Lenbachstr. 30, 86529 Schrobenhausen"
      ]
    },
    {
      "id": "de-ro-schwabach-roth-parohia-sf-ier-calinic-de-la-cernica-si-sf-elisabeta",
      "parent": "ro-germany",
      "kind": "parish",
      "rank": "Parish",
      "name": "Romanian Orthodox Parish \"St. Jer. Calinic from Cernica\" and \"St. Elisabeth\" - Schwabach in Schwabach - Roth",
      "local": "Parohia \"Sf. Ier. Calinic de la Cernica\" şi \"Sf. Elisabeta\" - Schwabach - Roth",
      "country": "DE",
      "sources": [
        "https://mitropolia-ro.de/parohii-germania/"
      ],
      "address": [
        "Ostring 36, 91126 Schwabach"
      ]
    },
    {
      "id": "de-ro-schwabisch-gmund-parohia-sf-ap-andrei",
      "parent": "ro-germany",
      "kind": "parish",
      "rank": "Parish",
      "name": "Romanian Orthodox Parish \"St. Rev. Andrei\" in Schwäbisch Gmünd",
      "local": "Parohia \"Sf. Ap. Andrei\" - Schwäbisch Gmünd",
      "country": "DE",
      "sources": [
        "https://mitropolia-ro.de/parohii-germania/"
      ],
      "address": [
        "St. Katharina Kapelle, Schwerzerallee 1/3, 73525 Schwäbisch Gmünd"
      ]
    },
    {
      "id": "de-ro-schwabisch-hall-parohia-sf-ap-petru-si-pavel-si-sf-elisabeta",
      "parent": "ro-germany",
      "kind": "parish",
      "rank": "Parish",
      "name": "Romanian Orthodox Parish \"St. Rev. Peter and Paul\" and \"St. Elizabeth\" in Schwäbisch Hall",
      "local": "Parohia \"Sf. Ap. Petru și Pavel\" şi \"Sf. Elisabeta\" - Schwäbisch Hall",
      "country": "DE",
      "sources": [
        "https://mitropolia-ro.de/parohii-germania/"
      ],
      "address": [
        "Elisabethenstr. 5, 74523 Gottwollshausen Schwäbisch Hall"
      ]
    },
    {
      "id": "de-ro-schweinfurt-parohia-adormirea-maicii-domnului-si-sf-ier-ghelasie-de-la-ramet",
      "parent": "ro-germany",
      "kind": "parish",
      "rank": "Parish",
      "name": "Romanian Orthodox The parish \"Assumption of the Virgin\" and \"St. Jer. Gelasie from Râmeț\" in Schweinfurt",
      "local": "Parohia \"Adormirea Maicii Domnului\" și \"Sf. Ier. Ghelasie de la Râmeț\" - Schweinfurt",
      "country": "DE",
      "sources": [
        "https://mitropolia-ro.de/parohii-germania/"
      ],
      "address": [
        "Glockenhof 9 97424 Schweinfurt"
      ]
    },
    {
      "id": "de-ro-siegen-parohia-sfanta-treime",
      "parent": "ro-germany",
      "kind": "parish",
      "rank": "Parish",
      "name": "Romanian Orthodox \"Holy Trinity\" Parish in Siegen",
      "local": "Parohia \"Sfânta Treime\" - Siegen",
      "country": "DE",
      "sources": [
        "https://mitropolia-ro.de/parohii-germania/"
      ],
      "address": [
        "Biserica \"Sf. Împ. Constantin şi Elena\", Am Rain 17, 57074 Siegen"
      ]
    },
    {
      "id": "de-ro-sigmaringen-parohia-sf-cuv-parascheva-de-la-iasi",
      "parent": "ro-germany",
      "kind": "parish",
      "rank": "Parish",
      "name": "Romanian Orthodox Parish \"St. Cuv. Paraskeva from Iasi\" in Sigmaringen",
      "local": "Parohia \"Sf. Cuv. Parascheva de la Iași\" - Sigmaringen",
      "country": "DE",
      "sources": [
        "https://mitropolia-ro.de/parohii-germania/"
      ],
      "address": [
        "Sauerlandstrasse 19, 72517 Sigmaringendorf"
      ]
    },
    {
      "id": "de-ro-sogel-parohia-sf-ap-petru-si-pavel-sf-ap-iacov-si-sf-ier-nectarie",
      "parent": "ro-germany",
      "kind": "parish",
      "rank": "Parish",
      "name": "Romanian Orthodox Parish \"St. Rev. Peter and Paul\", St. Rev. Jacob\" and \"St. Jer. Nectaria\" in Sögel",
      "local": "Parohia \"Sf. Ap. Petru și Pavel\", Sf. Ap. Iacov\" și \"Sf. Ier. Nectarie\" - Sögel",
      "country": "DE",
      "sources": [
        "https://mitropolia-ro.de/parohii-germania/"
      ],
      "address": [
        "Sprakeler Straße 54, 49751, Sögel"
      ]
    },
    {
      "id": "de-ro-speyer-parohia-sf-cuv-paisie-de-la-neamt",
      "parent": "ro-germany",
      "kind": "parish",
      "rank": "Parish",
      "name": "Romanian Orthodox \"St. Cuv. Paisie de la Neamț\" Parish in Speyer",
      "local": "Parohia \"Sf. Cuv. Paisie de la Neamț\" - Speyer",
      "country": "DE",
      "sources": [
        "https://mitropolia-ro.de/parohii-germania/"
      ],
      "address": [
        "Kurt-Schumacher-Straße 39, 67346 Speyer"
      ]
    },
    {
      "id": "de-ro-starnberg-parohia-acoperamantul-maicii-domnului-si-sf-ier-ulrich",
      "parent": "ro-germany",
      "kind": "parish",
      "rank": "Parish",
      "name": "Romanian Orthodox Parish \"The Covering of the Mother of God\" and \"St. Jer. Ulrich\" in Starnberg",
      "local": "Parohia \"Acoperământul Maicii Domnului\" și \"Sf. Ier. Ulrich\" - Starnberg",
      "country": "DE",
      "sources": [
        "https://mitropolia-ro.de/parohii-germania/"
      ],
      "address": [
        "Kaiser-Wilhelm-Straße 16 82319 Starnberg,"
      ]
    },
    {
      "id": "de-ro-straubing-parohia-sf-imp-constantin-si-elena",
      "parent": "ro-germany",
      "kind": "parish",
      "rank": "Parish",
      "name": "Romanian Orthodox \"St. Emperor Constantine and Elena\" Parish in Straubing",
      "local": "Parohia \"Sf. Împ. Constantin şi Elena\" - Straubing",
      "country": "DE",
      "sources": [
        "https://mitropolia-ro.de/parohii-germania/"
      ],
      "address": [
        "Theresienplatz 46, 94315 Straubing"
      ]
    },
    {
      "id": "de-ro-stuttgart-parohia-nasterea-domnului",
      "parent": "ro-germany",
      "kind": "parish",
      "rank": "Parish",
      "name": "Romanian Orthodox \"Nativity of God\" Parish in Stuttgart",
      "local": "Parohia \"Naşterea Domnului\" - Stuttgart",
      "country": "DE",
      "sources": [
        "https://mitropolia-ro.de/parohii-germania/"
      ],
      "address": [
        "Stammheimer Str. 104, 70435 Stuttgart"
      ]
    },
    {
      "id": "de-ro-traunreut-parohia-sf-trei-ierarhi",
      "parent": "ro-germany",
      "kind": "parish",
      "rank": "Parish",
      "name": "Romanian Orthodox Parish \"Sf. Trei Hierarchi\" in Traunreut",
      "local": "Parohia \"Sf. Trei Ierarhi\" - Traunreut",
      "country": "DE",
      "sources": [
        "https://mitropolia-ro.de/parohii-germania/"
      ],
      "address": [
        "Siebenbürgenerstraße 2, 83301 Traunreut"
      ]
    },
    {
      "id": "de-ro-trier-parohia-sf-imparati-constantin-si-elena",
      "parent": "ro-germany",
      "kind": "parish",
      "rank": "Parish",
      "name": "Romanian Orthodox \"St. Emperors Constantine and Elena\" Parish in Trier",
      "local": "Parohia \"Sf. Împărați Constantin și Elena\" - Trier",
      "country": "DE",
      "sources": [
        "https://mitropolia-ro.de/parohii-germania/"
      ],
      "address": [
        "Propstei 2, 54296 Trier"
      ]
    },
    {
      "id": "de-ro-trossingen-parohia-sf-prooroc-ioan-botezatorul-si-acoperamantul-maicii-domnului",
      "parent": "ro-germany",
      "kind": "parish",
      "rank": "Parish",
      "name": "Romanian Orthodox \"St. Prophet John the Baptist\" and \"Coverage of the Mother of God\" Parish in Trossingen",
      "local": "Parohia \"Sf. Prooroc Ioan Botezătorul\" și \"Acoperământul Maicii Domnului\" - Trossingen",
      "country": "DE",
      "sources": [
        "https://mitropolia-ro.de/parohii-germania/"
      ],
      "address": [
        "Görlitzerstraße 24, 78052 Villingen"
      ]
    },
    {
      "id": "de-ro-tubingen-parohia-sf-m-mc-gheorghe-si-sf-cuv-siluan-athonitul",
      "parent": "ro-germany",
      "kind": "parish",
      "rank": "Parish",
      "name": "Romanian Orthodox Parish \"Sf. M. Mc. Gheorghe\" and \"Sf. Cuv. Siluan Athonite\" in Tübingen",
      "local": "Parohia \"Sf. M. Mc. Gheorghe\" și \"Sf. Cuv. Siluan Athonitul\" - Tübingen",
      "country": "DE",
      "sources": [
        "https://mitropolia-ro.de/parohii-germania/"
      ],
      "address": [
        "Drosselweg 10 (im Sand), 72076 Tübingen"
      ]
    },
    {
      "id": "de-ro-ulm-parohia-sf-ap-petru-si-pavel",
      "parent": "ro-germany",
      "kind": "parish",
      "rank": "Parish",
      "name": "Romanian Orthodox \"St. Ap. Peter and Paul\" Parish in Ulm",
      "local": "Parohia \"Sf. Ap. Petru şi Pavel\" - Ulm",
      "country": "DE",
      "sources": [
        "https://mitropolia-ro.de/parohii-germania/"
      ],
      "address": [
        "Weihungstr. 26, 89079 Ulm-Wiblingen"
      ]
    },
    {
      "id": "de-ro-vechta-parohia-sf-atanasie-patelarie-si-sf-ier-ansgar",
      "parent": "ro-germany",
      "kind": "parish",
      "rank": "Parish",
      "name": "Romanian Orthodox \"St. Athanasius Patelarie\" and \"St. Jer. Ansgar\" Parish in Vechta",
      "local": "Parohia \"Sf. Atanasie Patelarie\" și \"Sf. Ier. Ansgar\" - Vechta",
      "country": "DE",
      "sources": [
        "https://mitropolia-ro.de/parohii-germania/"
      ],
      "address": [
        "Landwehrstrasse 2, 49377 Vechta"
      ],
      "services": [
        "(slujbe în prima și a treia duminică din lună)"
      ]
    },
    {
      "id": "de-ro-waldkraiburg-parohia-toti-sfintii",
      "parent": "ro-germany",
      "kind": "parish",
      "rank": "Parish",
      "name": "Romanian Orthodox \"All Saints\" Parish in Waldkraiburg",
      "local": "Parohia \"Toți Sfinţii\" - Waldkraiburg",
      "country": "DE",
      "sources": [
        "https://mitropolia-ro.de/parohii-germania/"
      ],
      "address": [
        "Salesianer Don Bosco Kirche, Waldwinkelstr.1, 84544 Aschau/Inn"
      ]
    },
    {
      "id": "de-ro-waldshut-tiengen-parohia-sfintii-ioachim-si-ana",
      "parent": "ro-germany",
      "kind": "parish",
      "rank": "Parish",
      "name": "Romanian Orthodox \"Saints Joachim and Ana\" Parish in Waldshut-Tiengen",
      "local": "Parohia \"Sfinții Ioachim și Ana\" - Waldshut-Tiengen",
      "country": "DE",
      "sources": [
        "https://mitropolia-ro.de/parohii-germania/"
      ],
      "address": [
        "Kalvarierberg Kapelle, 79761 Waldshut-Tiengen"
      ]
    },
    {
      "id": "de-ro-wertheim-parohia-botezul-domnului",
      "parent": "ro-germany",
      "kind": "parish",
      "rank": "Parish",
      "name": "Romanian Orthodox \"Baptism of the Lord\" Parish in Wertheim",
      "local": "Parohia \"Botezul Domnului\" - Wertheim",
      "country": "DE",
      "sources": [
        "https://mitropolia-ro.de/parohii-germania/"
      ],
      "address": [
        "Bismarckstr. 5, 97877 Wertheim"
      ]
    },
    {
      "id": "de-ro-wittlich-parohia-sf-cuv-serafim-cel-milostiv-de-la-sambata",
      "parent": "ro-germany",
      "kind": "parish",
      "rank": "Parish",
      "name": "Romanian Orthodox Parish \"St. Seraphim the Merciful from Saturday\" in Wittlich",
      "local": "Parohia \"Sf. Cuv. Serafim cel Milostiv de la Sâmbăta\" - Wittlich",
      "country": "DE",
      "sources": [
        "https://mitropolia-ro.de/parohii-germania/"
      ],
      "address": [
        "Hauptstrasse 42, 54492 Lösnich"
      ]
    },
    {
      "id": "de-ro-wiesbaden-parohia-sf-ier-bonifatiu-si-sf-ier-ghelasie-de-la-ramet",
      "parent": "ro-germany",
      "kind": "parish",
      "rank": "Parish",
      "name": "Romanian Orthodox Parish of \"St. Ier. Boniface\" and \"St. Ier. Ghelasie from Râmeț\" in Wiesbaden",
      "local": "Parohia \"Sf. Ier. Bonifațiu\" şi \"Sf. Ier. Ghelasie de la Râmeț\" - Wiesbaden",
      "country": "DE",
      "sources": [
        "https://mitropolia-ro.de/parohii-germania/"
      ],
      "address": [
        "Loh 14, 65199 Wiesbaden"
      ]
    },
    {
      "id": "de-ro-wilhelmshaven-filia-sf-cuv-antipa-de-la-calapodesti-si-sf-matrona-de-la-moscova",
      "parent": "ro-germany",
      "kind": "parish",
      "rank": "Filial community",
      "name": "Romanian Orthodox the daughter of \"St. Cuv. Antipa from Calapodesti\" and \"St. Matrona from Moscow\" in Wilhelmshaven",
      "local": "filia \"Sf. Cuv. Antipa de la Calapodești\" și \"Sf. Matrona de la Moscova\" - Wilhelmshaven",
      "country": "DE",
      "sources": [
        "https://mitropolia-ro.de/parohii-germania/"
      ],
      "address": [
        "Hunrichstrasse 6, 26388 Wilhelmshaven"
      ]
    },
    {
      "id": "de-ro-wolfsburg-filie",
      "parent": "ro-germany",
      "kind": "parish",
      "rank": "Filial community",
      "name": "Romanian Orthodox daughter in Wolfsburg",
      "local": "filie - Wolfsburg",
      "country": "DE",
      "sources": [
        "https://mitropolia-ro.de/parohii-germania/"
      ],
      "address": [
        "St. Heinrich-Kirchengemeinde, Am Stemmelteich 2, 38444 Wolfsburg"
      ],
      "services": [
        "(slujbe în a 4-a duminică din lună)"
      ]
    },
    {
      "id": "de-ro-worms-parohia-sf-ioan-botezatorul-si-sf-ap-andrei",
      "parent": "ro-germany",
      "kind": "parish",
      "rank": "Parish",
      "name": "Romanian Orthodox \"St. John the Baptist\" and \"St. Ap. Andrew\" Parish in Worms",
      "local": "Parohia \"Sf. Ioan Botezătorul\" și \"Sf. Ap. Andrei\" - Worms",
      "country": "DE",
      "sources": [
        "https://mitropolia-ro.de/parohii-germania/"
      ],
      "address": [
        "Neuoffsteiner Str. 15, 67591 Offstein (Worms)"
      ]
    },
    {
      "id": "de-ro-wuppertal-parohia-sf-arhid-laurentiu",
      "parent": "ro-germany",
      "kind": "parish",
      "rank": "Parish",
      "name": "Romanian Orthodox \"St. Archid. Laurentiu\" Parish in Wuppertal",
      "local": "Parohia \"Sf. Arhid. Laurențiu\" - Wuppertal",
      "country": "DE",
      "sources": [
        "https://mitropolia-ro.de/parohii-germania/"
      ],
      "address": [
        "Leipziger-Str. 41, 42109 Wuppertal"
      ]
    },
    {
      "id": "de-ro-wurzburg-parohia-sf-ap-andrei",
      "parent": "ro-germany",
      "kind": "parish",
      "rank": "Parish",
      "name": "Romanian Orthodox \"St. Ap. Andrew\" Parish in Würzburg",
      "local": "Parohia \"Sf. Ap. Andrei\" - Würzburg",
      "country": "DE",
      "sources": [
        "https://mitropolia-ro.de/parohii-germania/"
      ],
      "address": [
        "Biserica Sf. Barbara, Barbarastr. 44, 97074 Würzburg"
      ]
    },
    {
      "id": "de-ro-zittau-parohia-sf-treime-si-sf-mc-sofia-pistis-elpis-si-agapis",
      "parent": "ro-germany",
      "kind": "parish",
      "rank": "Parish",
      "name": "Romanian Orthodox \"Holy Trinity\" and \"St. Mc. Sophia, Pistis, Elpis and Agapis\" Parish in Zittau",
      "local": "Parohia \"Sf. Treime\" și \"Sf. Mc. Sofia, Pistis, Elpis și Agapis\" - Zittau",
      "country": "DE",
      "sources": [
        "https://mitropolia-ro.de/parohii-germania/"
      ],
      "address": [
        "Weberkirche, Innere Weberstrasse 46, 02763 Zittau"
      ]
    },
    {
      "id": "de-ro-weissenburg-gunzenhausen-parohia-sfintii-arhangheli-mihail-si-gavriil",
      "parent": "ro-germany",
      "kind": "parish",
      "rank": "Parish",
      "name": "Romanian Orthodox Parish \"Saints Archangels Michael and Gabriel\" in Weissenburg-Gunzenhausen",
      "local": "Parohia \"Sfinţii Arhangheli Mihail și Gavriil\" - Weissenburg-Gunzenhausen",
      "country": "DE",
      "sources": [
        "https://mitropolia-ro.de/parohii-germania/"
      ],
      "address": [
        "Holzgasse 3, 91781 Weißenburg in Bayern"
      ]
    },
    {
      "id": "de-ro-wesselburen-filia-sf-ap-bartolomeu",
      "parent": "ro-germany",
      "kind": "parish",
      "rank": "Filial community",
      "name": "Romanian Orthodox Filia \"St. Ap. Bartholomew\" in Wesselburen",
      "local": "filia \"Sf. Ap. Bartolomeu\" - Wesselburen",
      "country": "DE",
      "sources": [
        "https://mitropolia-ro.de/parohii-germania/"
      ],
      "address": [
        "Schulstraße 17, 25764 Reinsbüttel"
      ]
    }
  ],
  "ru-archdiocese-western-europe": [
    {
      "id": "de-ru-trad-stuttgart-gemeinde-zu-ehren-des-heiligen-und-rechtglaubigen-fursten-alexander-nevskij",
      "parent": "ru-archdiocese-western-europe",
      "kind": "parish",
      "rank": "Parish",
      "name": "Russian Tradition Orthodox Parish in honor of the holy and orthodox Prince Alexander Nevsky",
      "local": "Gemeinde zu Ehren des heiligen und rechtgläubigen Fürsten Alexander Nevskij",
      "country": "DE",
      "sources": [
        "https://erzbistum.net/gemeinden/"
      ],
      "address": [
        "Kapelle im Pragriedhof Friedhofstrasse 44 70191 Stuttgart"
      ],
      "languages": [
        "Kirchenslawisch",
        "Deutsch"
      ]
    },
    {
      "id": "de-ru-trad-balingen-gemeinde-zu-ehren-des-hl-martin-von-tours",
      "parent": "ru-archdiocese-western-europe",
      "kind": "parish",
      "rank": "Parish",
      "name": "Russian Tradition Orthodox Parish in honor of St. Martin of Tours",
      "local": "Gemeinde zu Ehren des hl. Martin von Tours",
      "country": "DE",
      "sources": [
        "https://erzbistum.net/gemeinden/"
      ],
      "address": [
        "Siechenkapelle Tübinger Str. 48 72336 Balingen"
      ],
      "languages": [
        "Deutsch"
      ]
    },
    {
      "id": "de-ru-trad-albstadt-gemeinde-zu-ehren-des-hl-sergius-von-radonesch-communaute",
      "parent": "ru-archdiocese-western-europe",
      "kind": "parish",
      "rank": "Parish",
      "name": "Russian Tradition Orthodox Parish in honor of St. Sergius of Radonezh (Communaut)",
      "local": "Gemeinde zu Ehren des hl. Sergius von Radonesch (Communaute)",
      "country": "DE",
      "sources": [
        "https://erzbistum.net/gemeinden/"
      ],
      "address": [
        "Schloßstrasse 42 72461 Albstadt"
      ],
      "languages": [
        "Deutsch"
      ]
    },
    {
      "id": "de-ru-trad-karlsruhe-gemeinde-zu-ehren-der-hl-apostel-petrus-und-paulus",
      "parent": "ru-archdiocese-western-europe",
      "kind": "parish",
      "rank": "Parish",
      "name": "Russian Tradition Orthodox Parish in honor of St. Apostles Peter and Paul",
      "local": "Gemeinde zu Ehren der hl. Apostel Petrus und Paulus",
      "country": "DE",
      "sources": [
        "https://erzbistum.net/gemeinden/"
      ],
      "address": [
        "Gottesdienste in der Alt-Katholischen Kirche Röntgenstraße 1 76133 Karlsruhe"
      ],
      "languages": [
        "Kirchenslawisch"
      ]
    },
    {
      "id": "de-ru-trad-bruchsal-gemeinde-zu-ehren-des-festes-maria-geburt",
      "parent": "ru-archdiocese-western-europe",
      "kind": "parish",
      "rank": "Parish",
      "name": "Russian Tradition Orthodox Community in honor of the feast of the Nativity of Mary",
      "local": "Gemeinde zu Ehren des Festes Maria Geburt",
      "country": "DE",
      "sources": [
        "https://erzbistum.net/gemeinden/"
      ],
      "address": [
        "Gottesdienste in der St. Jakobus Kirche Amalienstraße 44 76689 Karlsdorf-Neuthard"
      ],
      "languages": [
        "Kirchenslawisch"
      ]
    },
    {
      "id": "de-ru-trad-dusseldorf-gemeinde-zu-ehren-des-heiligen-nikolaus-des-wundertaters",
      "parent": "ru-archdiocese-western-europe",
      "kind": "parish",
      "rank": "Parish",
      "name": "Russian Tradition Orthodox Parish in honor of Saint Nicholas the Wonderworker",
      "local": "Gemeinde zu Ehren des Heiligen Nikolaus des Wundertäters",
      "country": "DE",
      "sources": [
        "https://erzbistum.net/gemeinden/"
      ],
      "address": [
        "Josefskapelle Dillenburger Weg 50 40229 Düsseldorf"
      ],
      "languages": [
        "Kirchenslawisch",
        "Deutsch"
      ]
    },
    {
      "id": "de-ru-trad-klausen-kloster-maria-geburt",
      "parent": "ru-archdiocese-western-europe",
      "kind": "monastery",
      "rank": "Monastery",
      "name": "Russian Tradition Orthodox Monastery of the Nativity of the Virgin Mary",
      "local": "Kloster Mariä Geburt",
      "country": "DE",
      "sources": [
        "https://erzbistum.net/gemeinden/"
      ],
      "address": [
        "Bernkastelerstrasse 1 54524 Klausen, 54524, Allemagne"
      ],
      "languages": [
        "Kirchenslawisch",
        "Deutsch"
      ]
    },
    {
      "id": "de-ru-trad-regensburg-orthodoxe-kirchengemeinde-verklarung-christi",
      "parent": "ru-archdiocese-western-europe",
      "kind": "parish",
      "rank": "Parish",
      "name": "Russian Tradition Orthodox Orthodox parish Transfiguration of Christ",
      "local": "Orthodoxe Kirchengemeinde Verklärung Christi",
      "country": "DE",
      "sources": [
        "https://erzbistum.net/gemeinden/"
      ],
      "address": [
        "Wollwirkergasse 25 93047 Regensburg"
      ],
      "languages": [
        "Deutsch",
        "Englisch"
      ]
    },
    {
      "id": "de-ru-trad-regensburg-monastische-bruderschaft-zu-ehren-der-gottesgebarerin-des-zeichens",
      "parent": "ru-archdiocese-western-europe",
      "kind": "monastery",
      "rank": "Monastery",
      "name": "Russian Tradition Orthodox Monastic brotherhood in honor of the Theotokos of the Sign",
      "local": "Monastische Bruderschaft zu Ehren der Gottesgebärerin des Zeichens",
      "country": "DE",
      "sources": [
        "https://erzbistum.net/gemeinden/"
      ],
      "address": [
        "Maximilianstraße 15 93047 Regensburg"
      ],
      "languages": [
        "Deutsch",
        "Englisch"
      ]
    },
    {
      "id": "de-ru-trad-hannover-orthodoxe-kirchengemeinde-heiliger-seraphim-von-sarow",
      "parent": "ru-archdiocese-western-europe",
      "kind": "parish",
      "rank": "Parish",
      "name": "Russian Tradition Orthodox Orthodox parish of Saint Seraphim of Sarov",
      "local": "Orthodoxe Kirchengemeinde Heiliger Seraphim von Sarow",
      "country": "DE",
      "sources": [
        "https://erzbistum.net/gemeinden/"
      ],
      "address": [
        "Alt-Katholische Pfarrkirche St. Maria Angelica Brabeckstrasse 24 30559 Hannover"
      ],
      "languages": [
        "Deutsch"
      ]
    },
    {
      "id": "de-ru-trad-ingelheim-am-rhein-orthodoxe-kirchengemeinde-st-andreas-und-st-nikolaus",
      "parent": "ru-archdiocese-western-europe",
      "kind": "parish",
      "rank": "Parish",
      "name": "Russian Tradition Orthodox Orthodox parish of St. Andrew and St. Nicholas",
      "local": "Orthodoxe Kirchengemeinde St. Andreas und St. Nikolaus",
      "country": "DE",
      "sources": [
        "https://erzbistum.net/gemeinden/"
      ],
      "address": [
        "Neuweg 11 55218 Ingelheim am Rhein"
      ],
      "languages": [
        "Kirchenslawisch",
        "Deutsch",
        "Englisch"
      ]
    }
  ],
  "bg-western-central-europe": [
    {
      "id": "de-bg-st-tsar-boris-the-baptizer-bulgarian-orthodox-community-in-berlin",
      "parent": "bg-western-central-europe",
      "kind": "parish",
      "rank": "Parish",
      "name": "St Tsar Boris the Baptizer Bulgarian Orthodox Community in Berlin",
      "local": "БПЦО \"Св. цар Борис Покръстител\" - гр. Берлин",
      "country": "DE",
      "sources": [
        "https://bg-patriarshia.bg/west-eu-diocese-temples"
      ],
      "address": [
        "Hermannstrasse 84/90, D-12051 Berlin"
      ]
    },
    {
      "id": "de-bg-st-george-the-trophy-bearer-bulgarian-orthodox-community-in-dusseldorf",
      "parent": "bg-western-central-europe",
      "kind": "parish",
      "rank": "Parish",
      "name": "St George the Trophy-Bearer Bulgarian Orthodox Community in Düsseldorf",
      "local": "БПЦО \"Св. Георги Победоносец\" - гр. Дюселдорф",
      "country": "DE",
      "sources": [
        "https://bg-patriarshia.bg/west-eu-diocese-temples"
      ],
      "address": [
        "Theodor str. 1",
        "D-50389 Weseeling"
      ]
    },
    {
      "id": "de-bg-nativity-of-the-mother-of-god-bulgarian-orthodox-community-in-cologne-and-bonn",
      "parent": "bg-western-central-europe",
      "kind": "parish",
      "rank": "Parish",
      "name": "Nativity of the Mother of God Bulgarian Orthodox Community in Cologne and Bonn",
      "local": "БПЦО \"Св. Рождество Богородично\" - гр. Кьолн и гр. Бон",
      "country": "DE",
      "sources": [
        "https://bg-patriarshia.bg/west-eu-diocese-temples"
      ],
      "address": [
        "Gotenstr. 5, D-53175 Воnn"
      ]
    },
    {
      "id": "de-bg-st-clement-of-ohrid-bulgarian-orthodox-community-in-munich",
      "parent": "bg-western-central-europe",
      "kind": "parish",
      "rank": "Parish",
      "name": "St Clement of Ohrid Bulgarian Orthodox Community in Munich",
      "local": "БПЦО \"Св. Климент Охридски\" - гр. Мюнхен",
      "country": "DE",
      "sources": [
        "https://bg-patriarshia.bg/west-eu-diocese-temples"
      ],
      "address": [
        "Max-Planck-Str. 7, D-81675 München"
      ]
    },
    {
      "id": "de-bg-st-nicholas-the-wonderworker-bulgarian-orthodox-community-in-regensburg",
      "parent": "bg-western-central-europe",
      "kind": "parish",
      "rank": "Parish",
      "name": "St Nicholas the Wonderworker Bulgarian Orthodox Community in Regensburg",
      "local": "БПЦО \"Св. Николай Мирликийски Чудотворец\" - гр. Регенсбург",
      "country": "DE",
      "sources": [
        "https://bg-patriarshia.bg/west-eu-diocese-temples"
      ]
    },
    {
      "id": "de-bg-bulgarian-orthodox-mission-in-nuremberg",
      "parent": "bg-western-central-europe",
      "kind": "parish",
      "rank": "Mission",
      "name": "Bulgarian Orthodox Mission in Nuremberg",
      "local": "Православна мисия - Нюнберг",
      "country": "DE",
      "sources": [
        "https://bg-patriarshia.bg/west-eu-diocese-temples"
      ]
    },
    {
      "id": "de-bg-st-petka-of-tarnovo-bulgarian-orthodox-community-in-mannheim",
      "parent": "bg-western-central-europe",
      "kind": "parish",
      "rank": "Parish",
      "name": "St Petka of Tarnovo Bulgarian Orthodox Community in Mannheim",
      "local": "БПЦО \"Св. Петка Търновска\" - гр. Манхайм",
      "country": "DE",
      "sources": [
        "https://bg-patriarshia.bg/west-eu-diocese-temples"
      ],
      "address": [
        "August Bebel strasse 47",
        "68199 Mannheim"
      ]
    },
    {
      "id": "de-bg-st-tsar-boris-michael-the-baptizer-bulgarian-orthodox-community-in-frankfurt",
      "parent": "bg-western-central-europe",
      "kind": "parish",
      "rank": "Parish",
      "name": "St Tsar Boris-Michael the Baptizer Bulgarian Orthodox Community in Frankfurt",
      "local": "БПЦО \"Св. цар Борис-Михаил Покръстител\" - гр. Франкфурт",
      "country": "DE",
      "sources": [
        "https://bg-patriarshia.bg/west-eu-diocese-temples"
      ],
      "address": [
        "Waldmeisterpfad 6, D-65933 Frankfurt am Main"
      ]
    },
    {
      "id": "de-bg-sts-cyril-and-methodius-bulgarian-orthodox-community-in-hamburg",
      "parent": "bg-western-central-europe",
      "kind": "parish",
      "rank": "Parish",
      "name": "Sts Cyril and Methodius Bulgarian Orthodox Community in Hamburg",
      "local": "БПЦО \"Св. Кирил и Методий\" - гр. Хамбург",
      "country": "DE",
      "sources": [
        "https://bg-patriarshia.bg/west-eu-diocese-temples"
      ],
      "address": [
        "Biedermannpl. 1",
        "22083 Hamburg"
      ]
    },
    {
      "id": "de-bg-sts-cyril-and-methodius-bulgarian-orthodox-community-in-stuttgart",
      "parent": "bg-western-central-europe",
      "kind": "parish",
      "rank": "Parish",
      "name": "Sts Cyril and Methodius Bulgarian Orthodox Community in Stuttgart",
      "local": "БПЦО \"Св. Кирил и Методий\" - гр. Щутгарт",
      "country": "DE",
      "sources": [
        "https://bg-patriarshia.bg/west-eu-diocese-temples"
      ],
      "address": [
        "Zuckerbergstr. 11, 70378 Stuttgart-Steinhaldenfeld"
      ]
    },
    {
      "id": "de-bg-st-theodosius-of-tarnovo-bulgarian-orthodox-community-in-bruhl",
      "parent": "bg-western-central-europe",
      "kind": "parish",
      "rank": "Parish",
      "name": "St Theodosius of Tarnovo Bulgarian Orthodox Community in Brühl",
      "local": "БПЦО \"Св. преп. Теодосий Търновски\" - гр. Брюл",
      "country": "DE",
      "sources": [
        "https://bg-patriarshia.bg/west-eu-diocese-temples"
      ]
    },
    {
      "id": "de-bg-entry-of-the-mother-of-god-bulgarian-orthodox-community-in-mainz",
      "parent": "bg-western-central-europe",
      "kind": "parish",
      "rank": "Parish",
      "name": "Entry of the Mother of God Bulgarian Orthodox Community in Mainz",
      "local": "БПЦО \"Въведение Богородично\" - гр. Майнц",
      "country": "DE",
      "sources": [
        "https://bg-patriarshia.bg/news/tsarkovnata-ni-obshtnost-v-maynts-otbelyaza-tarzhestveno-svo"
      ]
    },
    {
      "id": "de-bg-st-barbara-bulgarian-orthodox-community-in-leipzig",
      "parent": "bg-western-central-europe",
      "kind": "parish",
      "rank": "Parish",
      "name": "St Barbara Bulgarian Orthodox Community in Leipzig",
      "local": "БПЦО \"Св. вмчца Варвара\" - гр. Лайпциг",
      "country": "DE",
      "sources": [
        "https://bg-patriarshia.bg/news/balgarskata-pravoslavna-tsarkovna-obshtina-sv-varvara-v-gr-l"
      ]
    },
    {
      "id": "de-bg-holy-trinity-monastery-in-buchhagen-dreifaltigkeitskloster-buchhagen",
      "parent": "bg-western-central-europe",
      "kind": "monastery",
      "rank": "Monastery",
      "name": "Holy Trinity Monastery in Buchhagen",
      "local": "Dreifaltigkeitskloster Buchhagen",
      "country": "DE",
      "sources": [
        "https://bg-patriarshia.bg/news/priziv-za-podkrepa-na-bratstvoto-na-pravoslavnia-manastir-v"
      ]
    }
  ],
  "ukraine-uoc": [
    {
      "id": "de-uoc-all-saints-uoc-parish-in-berlin",
      "parent": "ukraine-uoc",
      "kind": "parish",
      "rank": "Parish",
      "name": "All Saints UOC Parish in Berlin",
      "local": "Парафія Української Православної Церкви на честь Всіх святих у Берліні",
      "country": "DE",
      "sources": [
        "https://vzcz.church.ua/2022/08/29/pochala-diyati-gromada-upc-v-berlini/"
      ],
      "address": [
        "Zabel-Krüger-Damm 219",
        "13469 Berlin"
      ]
    },
    {
      "id": "de-uoc-holy-archangel-michael-uoc-parish-in-berlin",
      "parent": "ukraine-uoc",
      "kind": "parish",
      "rank": "Parish",
      "name": "Holy Archangel Michael UOC Parish in Berlin",
      "local": "Парафія Української Православної Церкви на честь Архістратига Божого Михаїла у Берліні",
      "country": "DE",
      "sources": [
        "https://vzcz.church.ua/2024/01/08/v-berlini-pochala-diyati-druga-parafiya-upc/"
      ]
    },
    {
      "id": "de-uoc-protection-of-the-mother-of-god-uoc-parish-in-hamburg",
      "parent": "ukraine-uoc",
      "kind": "parish",
      "rank": "Parish",
      "name": "Protection of the Mother of God UOC Parish in Hamburg",
      "local": "Парафія УПЦ на честь Покрови Пресвятої Богородиці в м. Гамбург",
      "country": "DE",
      "sources": [
        "https://news.church.ua/2023/03/24/keruyuchij-parafiyami-upc-zakordonom-vidviduje-ukrajinski-gromadi-v-nimechchini/"
      ]
    },
    {
      "id": "de-uoc-st-nicholas-the-wonderworker-uoc-parish-in-gera",
      "parent": "ukraine-uoc",
      "kind": "parish",
      "rank": "Parish",
      "name": "St Nicholas the Wonderworker UOC Parish in Gera",
      "local": "Парафія УПЦ на честь святителя Миколая Чудотворця в м. Гера",
      "country": "DE",
      "sources": [
        "https://vzcz.church.ua/2025/05/27/jepiskop-veniamin-ocholiv-svyatkovi-bogosluzhinnya-na-parafiyax-upc-v-drezdeni-ta-geri/"
      ]
    },
    {
      "id": "de-uoc-nativity-of-the-mother-of-god-uoc-parish-in-plauen",
      "parent": "ukraine-uoc",
      "kind": "parish",
      "rank": "Parish",
      "name": "Nativity of the Mother of God UOC Parish in Plauen",
      "local": "Парафія УПЦ на честь Різдва Пресвятої Богородиці в м. Плауен",
      "country": "DE",
      "sources": [
        "https://news.church.ua/2023/03/24/keruyuchij-parafiyami-upc-zakordonom-vidviduje-ukrajinski-gromadi-v-nimechchini/"
      ]
    },
    {
      "id": "de-uoc-holy-myrrh-bearing-women-uoc-community-in-halberstadt",
      "parent": "ukraine-uoc",
      "kind": "parish",
      "rank": "Parish",
      "name": "Holy Myrrh-Bearing Women UOC Community in Halberstadt",
      "local": "Громада УПЦ на честь святих жінок-мироносиць у Гальберштадті",
      "country": "DE",
      "sources": [
        "https://news.church.ua/2022/09/16/u-nimechchini-pochali-diyati-novi-gromadi-upc/"
      ],
      "address": [
        "Liebfrauenkirche",
        "Domplatz 46",
        "38820 Halberstadt"
      ],
      "services": [
        "Saturday at 10:00."
      ]
    },
    {
      "id": "de-uoc-uoc-community-in-dingelstadt",
      "parent": "ukraine-uoc",
      "kind": "parish",
      "rank": "Parish",
      "name": "UOC Community in Dingelstädt",
      "local": "Громада Української Православної Церкви у Дінгельштедті",
      "country": "DE",
      "sources": [
        "https://news.church.ua/2022/09/16/u-nimechchini-pochali-diyati-novi-gromadi-upc/"
      ],
      "address": [
        "Familienzentrum Kloster Kerbscher Berg",
        "Kefferhäuser Str. 24",
        "37351 Dingelstädt"
      ],
      "services": [
        "Sunday at 10:00."
      ]
    },
    {
      "id": "de-uoc-holy-life-giving-trinity-uoc-parish-in-leipzig",
      "parent": "ukraine-uoc",
      "kind": "parish",
      "rank": "Parish",
      "name": "Holy Life-Giving Trinity UOC Parish in Leipzig",
      "local": "Свято-Троїцька парафія УПЦ у місті Лейпциг",
      "country": "DE",
      "sources": [
        "https://vzcz.church.ua/2024/07/02/jepiskop-veniamin-vidvidav-parafiji-upc-v-lejpcigu-ta-kelni/"
      ]
    },
    {
      "id": "de-uoc-pochaev-icon-of-the-mother-of-god-uoc-parish-in-cologne",
      "parent": "ukraine-uoc",
      "kind": "parish",
      "rank": "Parish",
      "name": "Pochaev Icon of the Mother of God UOC Parish in Cologne",
      "local": "Парафія УПЦ на честь Почаївської ікони Пресвятої Богородиці в місті Кельн",
      "country": "DE",
      "sources": [
        "https://vzcz.church.ua/2024/07/02/jepiskop-veniamin-vidvidav-parafiji-upc-v-lejpcigu-ta-kelni/"
      ]
    },
    {
      "id": "de-uoc-holy-apostle-andrew-the-first-called-uoc-parish-in-worms",
      "parent": "ukraine-uoc",
      "kind": "parish",
      "rank": "Parish",
      "name": "Holy Apostle Andrew the First-Called UOC Parish in Worms",
      "local": "Парафія Української Православної Церкви на честь святого апостола Андрія Первозванного в місті Вормс",
      "country": "DE",
      "sources": [
        "https://vzcz.church.ua/2023/11/14/v-nimechchini-vidkrito-pershij-tipovij-xram-upc/"
      ]
    },
    {
      "id": "de-uoc-sts-cyril-and-methodius-uoc-parish-in-dresden",
      "parent": "ukraine-uoc",
      "kind": "parish",
      "rank": "Parish",
      "name": "Sts Cyril and Methodius UOC Parish in Dresden",
      "local": "Парафія УПЦ на честь святих рівноапостольних Мефодія і Кирила в місті Дрезден",
      "country": "DE",
      "sources": [
        "https://vzcz.church.ua/2025/05/27/jepiskop-veniamin-ocholiv-svyatkovi-bogosluzhinnya-na-parafiyax-upc-v-drezdeni-ta-geri/"
      ]
    },
    {
      "id": "de-uoc-st-willehad-and-all-saints-uoc-parish-in-bremen",
      "parent": "ukraine-uoc",
      "kind": "parish",
      "rank": "Parish",
      "name": "St Willehad and All Saints UOC Parish in Bremen",
      "local": "Парафія УПЦ на честь святителя Віллехада, першого єпископа Бременського, та всіх святих у місті Бремен",
      "country": "DE",
      "sources": [
        "https://news.church.ua/2026/08/25/parafiya-upc-u-bremeni-peredala-avtomobil-dlya-zsu/"
      ]
    },
    {
      "id": "de-uoc-peschansk-icon-of-the-mother-of-god-uoc-parish-in-hannover",
      "parent": "ukraine-uoc",
      "kind": "parish",
      "rank": "Parish",
      "name": "Peschansk Icon of the Mother of God UOC Parish in Hannover",
      "local": "Парафія УПЦ на честь Піщанської ікони Божої Матері м. Ганновер",
      "country": "DE",
      "sources": [
        "https://vzcz.church.ua/2025/01/13/u-lejpcigu-ta-gamburzi-vidbulisya-festivali-kolyadok/"
      ]
    },
    {
      "id": "de-uoc-uoc-parish-in-nuremberg",
      "parent": "ukraine-uoc",
      "kind": "parish",
      "rank": "Parish",
      "name": "UOC Parish in Nuremberg",
      "local": "Парафія Української Православної Церкви у Нюрнберзі",
      "country": "DE",
      "sources": [
        "https://vzcz.church.ua/2025/01/13/u-lejpcigu-ta-gamburzi-vidbulisya-festivali-kolyadok/"
      ]
    },
    {
      "id": "de-uoc-look-upon-humility-icon-of-the-mother-of-god-uoc-parish-in-jena",
      "parent": "ukraine-uoc",
      "kind": "parish",
      "rank": "Parish",
      "name": "Look Upon Humility Icon of the Mother of God UOC Parish in Jena",
      "local": "Громада УПЦ на честь ікони Божої Матері \"Призри на смирення\" в місті Єна",
      "country": "DE",
      "sources": [
        "https://vzcz.church.ua/2026/02/12/parafiya-upc-v-nimechchini-organizuvala-zbir-koshtiv-na-dopomogu-blagodijnij-jidalni-na-kijivshhini/"
      ]
    }
  ],
  "ep-ukrainian-western-europe": [
    {
      "id": "de-ep-ukr-ukrainian-orthodox-parish-in-augsburg-augsburg-gemeinder-der-hl-grossmartyrerin-barbara",
      "parent": "ep-ukrainian-western-europe",
      "kind": "parish",
      "rank": "Parish",
      "name": "Ukrainian Orthodox Augsburg - Parish of the Holy Great Martyr Barbara",
      "local": "Augsburg - Gemeinder der Hl. Großmärtyrerin Barbara",
      "country": "DE",
      "sources": [
        "https://www.uokd.de/gemeinden"
      ],
      "address": [
        "Dominikanergasse 5, 86150 Augsburg"
      ]
    },
    {
      "id": "de-ep-ukr-ukrainian-orthodox-parish-in-bad-kissing-bad-kissing-gemeinde-der-geburt-der-gottesgebar",
      "parent": "ep-ukrainian-western-europe",
      "kind": "parish",
      "rank": "Parish",
      "name": "Ukrainian Orthodox Bad Kissing - Parish of the Nativity of the Theotokos",
      "local": "Bad Kissing - Gemeinde der Geburt der Gottesgebärerin",
      "country": "DE",
      "sources": [
        "https://www.uokd.de/gemeinden"
      ],
      "address": [
        "Kapellenstraße 17, 97688 Bad Kissing"
      ]
    },
    {
      "id": "de-ep-ukr-ukrainian-orthodox-parish-in-berlin-berlin-gemeinde-des-hl-fursten-ihor-von-tschernihiw",
      "parent": "ep-ukrainian-western-europe",
      "kind": "parish",
      "rank": "Parish",
      "name": "Ukrainian Orthodox Berlin - Parish of St. Prince Ihor of Chernihiv",
      "local": "Berlin - Gemeinde des Hl. Fürsten Ihor von Tschernihiw",
      "country": "DE",
      "sources": [
        "https://www.uokd.de/gemeinden"
      ],
      "address": [
        "St. Thomas Kirche",
        "Mariannenplatz 28",
        "10997 Berlin"
      ]
    },
    {
      "id": "de-ep-ukr-ukrainian-orthodox-parish-in-burghausen-burghausen-gemeinde-des-hl-hiob-von-potschajiw",
      "parent": "ep-ukrainian-western-europe",
      "kind": "parish",
      "rank": "Parish",
      "name": "Ukrainian Orthodox Burghausen - Parish of St. Job of Pochaiv",
      "local": "Burghausen - Gemeinde des Hl. Hiob von Potschajiw",
      "country": "DE",
      "sources": [
        "https://www.uokd.de/gemeinden"
      ],
      "address": [
        "St. Anna Kirche",
        "Kapuzienergasse 238",
        "84489 Burghausen"
      ]
    },
    {
      "id": "de-ep-ukr-ukrainian-orthodox-parish-in-dusseldorf-dusseldorf-gemeinde-des-hl-nikolaus-erzbischof-v",
      "parent": "ep-ukrainian-western-europe",
      "kind": "parish",
      "rank": "Parish",
      "name": "Ukrainian Orthodox Düsseldorf - Parish of St. Nicholas, Archbishop of Myra, miracle worker",
      "local": "Düsseldorf - Gemeinde des Hl. Nikolaus, Erzbischof von Myra, Wundertäter",
      "country": "DE",
      "sources": [
        "https://www.uokd.de/gemeinden"
      ],
      "address": [
        "In der Elb 2, 40229 Düsseldorf-Eller"
      ]
    },
    {
      "id": "de-ep-ukr-ukrainian-orthodox-parish-in-erfurt-erfurt-gemeinde-geburt-des-herrn",
      "parent": "ep-ukrainian-western-europe",
      "kind": "parish",
      "rank": "Parish",
      "name": "Ukrainian Orthodox Erfurt - Parish of the Birth of the Lord",
      "local": "Erfurt - Gemeinde Geburt des Herrn",
      "country": "DE",
      "sources": [
        "https://www.uokd.de/gemeinden"
      ],
      "address": [
        "Konrad-Zuse-Straße 12, 99099 Erfurt"
      ]
    },
    {
      "id": "de-ep-ukr-ukrainian-orthodox-parish-in-freising-b-munchen-freising-b-munchen-gemeinde-der-einfuhru",
      "parent": "ep-ukrainian-western-europe",
      "kind": "parish",
      "rank": "Parish",
      "name": "Ukrainian Orthodox Freising b. Munich - Community of Introduction to the Temple of the Theotokos in Freising b. München",
      "local": "Freising b. München - Gemeinde der Einführung in den Tempel der Gottesgebärerin",
      "country": "DE",
      "sources": [
        "https://www.uokd.de/gemeinden"
      ],
      "address": [
        "Paul-Gerhardt-Haus",
        "General-von-Stein-Str. 22",
        "85356 Freising"
      ]
    },
    {
      "id": "de-ep-ukr-ukrainian-orthodox-parish-in-hamburg-hamburg-gemeinde-des-hl-nikolaus-erzbischof-von-myr",
      "parent": "ep-ukrainian-western-europe",
      "kind": "parish",
      "rank": "Parish",
      "name": "Ukrainian Orthodox Hamburg - Parish of St. Nicholas, Archbishop of Myra, miracle worker",
      "local": "Hamburg - Gemeinde des Hl. Nikolaus, Erzbischof von Myra, Wundertäter",
      "country": "DE",
      "sources": [
        "https://www.uokd.de/gemeinden"
      ],
      "address": [
        "Bogenstraße 30, 20144 Hamburg"
      ]
    },
    {
      "id": "de-ep-ukr-ukrainian-orthodox-parish-in-hannover-hannover-gemeinde-des-heiligen-apostelgleichen-gro",
      "parent": "ep-ukrainian-western-europe",
      "kind": "parish",
      "rank": "Parish",
      "name": "Ukrainian Orthodox Hanover - Parish of the Holy Apostle-like Grand Duke Volodymir in Hannover",
      "local": "Hannover - Gemeinde des Heiligen, Apostelgleichen Großfürsten Wolodymir",
      "country": "DE",
      "sources": [
        "https://www.uokd.de/gemeinden"
      ],
      "address": [
        "Stöckener Straße 43, 30419 Hannover",
        "Kath. Kirche St. Adalbert"
      ]
    },
    {
      "id": "de-ep-ukr-ukrainian-orthodox-parish-in-ingolstadt-ingolstadt-gemeinde-der-hl-maria-schutz",
      "parent": "ep-ukrainian-western-europe",
      "kind": "parish",
      "rank": "Parish",
      "name": "Ukrainian Orthodox Ingolstadt - Parish of St. Mary Protection",
      "local": "Ingolstadt - Gemeinde der Hl. Maria-Schutz",
      "country": "DE",
      "sources": [
        "https://www.uokd.de/gemeinden"
      ],
      "address": [
        "Dreizehnerstr. 11, 85049 Ingolstadt"
      ]
    },
    {
      "id": "de-ep-ukr-ukrainian-orthodox-parish-in-karlsruhe-karlsruhe-gemeinde-des-hl-nikolaus-erzbischof-von",
      "parent": "ep-ukrainian-western-europe",
      "kind": "parish",
      "rank": "Parish",
      "name": "Ukrainian Orthodox Karlsruhe - Parish of St. Nicholas, Archbishop of Myra, miracle worker",
      "local": "Karlsruhe - Gemeinde des Hl. Nikolaus, Erzbischof von Myra, Wundertäter",
      "country": "DE",
      "sources": [
        "https://www.uokd.de/gemeinden"
      ],
      "address": [
        "Röntgenstr. 11, 76133 Karlsruhe"
      ]
    },
    {
      "id": "de-ep-ukr-ukrainian-orthodox-parish-in-kiel-kiel-gemeinde-allerheiligen",
      "parent": "ep-ukrainian-western-europe",
      "kind": "parish",
      "rank": "Parish",
      "name": "Ukrainian Orthodox Kiel - Parish of All Saints",
      "local": "Kiel - Gemeinde Allerheiligen",
      "country": "DE",
      "sources": [
        "https://www.uokd.de/gemeinden"
      ],
      "address": [
        "Bethlehem Kirche",
        "Möhrkestraße 9",
        "24159 Kiel"
      ]
    },
    {
      "id": "de-ep-ukr-ukrainian-orthodox-parish-in-krefeld-krefeld-gemeinde-der-hl-maria-schutz",
      "parent": "ep-ukrainian-western-europe",
      "kind": "parish",
      "rank": "Parish",
      "name": "Ukrainian Orthodox Krefeld - Parish of St. Mary Protection",
      "local": "Krefeld - Gemeinde der Hl. Maria-Schutz",
      "country": "DE",
      "sources": [
        "https://www.uokd.de/gemeinden"
      ],
      "address": [
        "Maria-Sohmann-Str. 45, 47802 Krefeld Traar"
      ]
    },
    {
      "id": "de-ep-ukr-ukrainian-orthodox-parish-in-landshut-landshut-gemeinde-des-hl-erzengel-michael",
      "parent": "ep-ukrainian-western-europe",
      "kind": "parish",
      "rank": "Parish",
      "name": "Ukrainian Orthodox Landshut - Parish of St. Archangel Michael",
      "local": "Landshut - Gemeinde des Hl. Erzengel Michael",
      "country": "DE",
      "sources": [
        "https://www.uokd.de/gemeinden"
      ],
      "address": [
        "Regierungsplatz 541, 84028 Landshut"
      ]
    },
    {
      "id": "de-ep-ukr-ukrainian-orthodox-parish-in-lindau-lindau-gemeinde-des-hl-apostel-johannes-d-theologen",
      "parent": "ep-ukrainian-western-europe",
      "kind": "parish",
      "rank": "Parish",
      "name": "Ukrainian Orthodox Lindau - Parish of the Holy Apostle John the Elder theologians",
      "local": "Lindau - Gemeinde des Hl. Apostel Johannes d. Theologen",
      "country": "DE",
      "sources": [
        "https://www.uokd.de/gemeinden"
      ],
      "address": [
        "Anheggerstr. 3, 88131 Lindau am Bodensee"
      ]
    },
    {
      "id": "de-ep-ukr-ukrainian-orthodox-parish-in-lubeck-lubeck-gemeinde-des-hl-makarii-von-kaniv",
      "parent": "ep-ukrainian-western-europe",
      "kind": "parish",
      "rank": "Parish",
      "name": "Ukrainian Orthodox Lübeck - Parish of St. Makarii of Kaniv",
      "local": "Lübeck - Gemeinde des Hl. Makarii von Kaniv",
      "country": "DE",
      "sources": [
        "https://www.uokd.de/gemeinden"
      ],
      "address": [
        "Kleine Altefähre 6a, 23552 Lübeck",
        "Griechisch-Orthodoxe Kirche des Hl. Georgios"
      ]
    },
    {
      "id": "de-ep-ukr-ukrainian-orthodox-parish-in-munchen-munchen-gemeinde-der-hl-maria-schutz",
      "parent": "ep-ukrainian-western-europe",
      "kind": "parish",
      "rank": "Parish",
      "name": "Ukrainian Orthodox Munich - Parish of St. Mary Protection in München",
      "local": "München - Gemeinde der Hl. Maria-Schutz",
      "country": "DE",
      "sources": [
        "https://www.uokd.de/gemeinden"
      ],
      "address": [
        "Innere-Wiener-Straße 1, 81667 München"
      ]
    },
    {
      "id": "de-ep-ukr-ukrainian-orthodox-parish-in-munchen-munchen-gemeinde-der-hl-apostelfursten-peter-und-pa",
      "parent": "ep-ukrainian-western-europe",
      "kind": "parish",
      "rank": "Parish",
      "name": "Ukrainian Orthodox Munich - Parish of the Holy Apostles Peter and Paul in München",
      "local": "München - Gemeinde der Hl. Apostelfürsten Peter und Paul",
      "country": "DE",
      "sources": [
        "https://www.uokd.de/gemeinden"
      ],
      "address": [
        "Granatstraße 1, 80995 München"
      ]
    },
    {
      "id": "de-ep-ukr-ukrainian-orthodox-parish-in-neu-ulm-neu-ulm-gemeinde-der-hl-kreuzerhohung",
      "parent": "ep-ukrainian-western-europe",
      "kind": "parish",
      "rank": "Parish",
      "name": "Ukrainian Orthodox Neu-Ulm - Parish of the Exaltation of the Holy Cross",
      "local": "Neu-Ulm - Gemeinde der Hl. Kreuzerhöhung",
      "country": "DE",
      "sources": [
        "https://www.uokd.de/gemeinden"
      ],
      "address": [
        "Hirthstr. 3, 89231 Neu-Ulm"
      ]
    },
    {
      "id": "de-ep-ukr-ukrainian-orthodox-parish-in-nurnberg-nurnberg-gemeinde-des-hl-nikolaus-erzbischof-von-m",
      "parent": "ep-ukrainian-western-europe",
      "kind": "parish",
      "rank": "Parish",
      "name": "Ukrainian Orthodox Nuremberg - Parish of St. Nicholas, Archbishop of Myra, miracle worker in Nürnberg",
      "local": "Nürnberg - Gemeinde des Hl. Nikolaus, Erzbischof von Myra, Wundertäter",
      "country": "DE",
      "sources": [
        "https://www.uokd.de/gemeinden"
      ],
      "address": [
        "Adam-Klein-Straße 45, 90429 Nürnberg",
        "Kath. Kirche St. Anton"
      ]
    },
    {
      "id": "de-ep-ukr-ukrainian-orthodox-parish-in-oldenburg-oldenburg-gemeinde-der-geburt-der-allheiligen-got",
      "parent": "ep-ukrainian-western-europe",
      "kind": "parish",
      "rank": "Parish",
      "name": "Ukrainian Orthodox Oldenburg - Parish of the Nativity of the All Holy Theotokos",
      "local": "Oldenburg - Gemeinde der Geburt der Allheiligen Gottesgebärerin",
      "country": "DE",
      "sources": [
        "https://www.uokd.de/gemeinden"
      ],
      "address": [
        "Brookweg 30, 26127 Oldenburg",
        "Kath. Kirche St. Christophorus"
      ]
    },
    {
      "id": "de-ep-ukr-ukrainian-orthodox-parish-in-ravensburg-ravensburg-gemeinde-des-hl-amphilochius-von-pots",
      "parent": "ep-ukrainian-western-europe",
      "kind": "parish",
      "rank": "Parish",
      "name": "Ukrainian Orthodox Ravensburg - Parish of St. Amphilochius of Pochaiv",
      "local": "Ravensburg - Gemeinde des Hl. Amphilochius von Potschajiw",
      "country": "DE",
      "sources": [
        "https://www.uokd.de/gemeinden"
      ],
      "address": [
        "Meersburger Str. 41, 88212 Ravensburg"
      ]
    },
    {
      "id": "de-ep-ukr-ukrainian-orthodox-parish-in-rosenheim-rosenheim-gemeinde-der-hl-sophia-und-ihrer-tochte",
      "parent": "ep-ukrainian-western-europe",
      "kind": "parish",
      "rank": "Parish",
      "name": "Ukrainian Orthodox Rosenheim - Parish of St. Sophia and Her Daughters Faith, Hope and Love",
      "local": "Rosenheim - Gemeinde der Hl. Sophia und Ihrer Töchter Glaube, Hoffnung und Liebe",
      "country": "DE",
      "sources": [
        "https://www.uokd.de/gemeinden"
      ],
      "address": [
        "St. Joseph Spitalkirche",
        "Innstraße 6, 83022 Rosenheim"
      ]
    },
    {
      "id": "de-ep-ukr-ukrainian-orthodox-parish-in-regensburg-regensburg-gemeinde-des-hl-nikolaus-erzbischof-v",
      "parent": "ep-ukrainian-western-europe",
      "kind": "parish",
      "rank": "Parish",
      "name": "Ukrainian Orthodox Regensburg - Parish of St. Nicholas, Archbishop of Myra, miracle worker",
      "local": "Regensburg - Gemeinde des Hl. Nikolaus, Erzbischof von Myra, Wundertäter",
      "country": "DE",
      "sources": [
        "https://www.uokd.de/gemeinden"
      ],
      "address": [
        "St.-Leonhards-Gasse 1, 93047 Regensburg",
        "Kath. Kirche St. Leonhard"
      ]
    },
    {
      "id": "de-ep-ukr-ukrainian-orthodox-parish-in-saarbrucken-saarbrucken-gemeinde-der-entschlafung-der-gotte",
      "parent": "ep-ukrainian-western-europe",
      "kind": "parish",
      "rank": "Parish",
      "name": "Ukrainian Orthodox Saarbrücken - Parish of the Dormition of the Theotokos",
      "local": "Saarbrücken - Gemeinde der Entschlafung der Gottesgebärerin",
      "country": "DE",
      "sources": [
        "https://www.uokd.de/gemeinden"
      ],
      "address": [
        "Krypta der Johanneskirche",
        "Blumenstraße 22, 66126 Saarbrücken"
      ]
    },
    {
      "id": "de-ep-ukr-ukrainian-orthodox-parish-in-schwerin-schwerin-gemeinde-des-hl-apostel-paulus",
      "parent": "ep-ukrainian-western-europe",
      "kind": "parish",
      "rank": "Parish",
      "name": "Ukrainian Orthodox Schwerin - Parish of the Holy Apostle Paul",
      "local": "Schwerin - Gemeinde des Hl. Apostel Paulus",
      "country": "DE",
      "sources": [
        "https://www.uokd.de/gemeinden"
      ],
      "address": [
        "Am Packhof 8, 19053 Schwerin"
      ]
    },
    {
      "id": "de-ep-ukr-ukrainian-orthodox-parish-in-straubing-straubing-gemeinde-des-hl-hiob-von-potschajiw",
      "parent": "ep-ukrainian-western-europe",
      "kind": "parish",
      "rank": "Parish",
      "name": "Ukrainian Orthodox Straubing - Parish of St. Job of Pochaiv",
      "local": "Straubing - Gemeinde des Hl. Hiob von Potschajiw",
      "country": "DE",
      "sources": [
        "https://www.uokd.de/gemeinden"
      ],
      "address": [
        "Friedhofstraße 32, 94315 Straubing"
      ]
    },
    {
      "id": "de-ep-ukr-ukrainian-orthodox-parish-in-stuttgart-stuttgart-gemeinde-der-hl-dreifaltigkeit",
      "parent": "ep-ukrainian-western-europe",
      "kind": "parish",
      "rank": "Parish",
      "name": "Ukrainian Orthodox Stuttgart - Parish of the Holy Trinity",
      "local": "Stuttgart - Gemeinde der Hl. Dreifaltigkeit",
      "country": "DE",
      "sources": [
        "https://www.uokd.de/gemeinden"
      ],
      "address": [
        "Gablenberger Hauptstraße 80, 70186 Stuttgart"
      ]
    },
    {
      "id": "de-ep-ukr-ukrainian-orthodox-parish-in-traunreut-traunreut-gemeinde-allerheiligen",
      "parent": "ep-ukrainian-western-europe",
      "kind": "parish",
      "rank": "Parish",
      "name": "Ukrainian Orthodox Traunreut - Parish of All Saints",
      "local": "Traunreut - Gemeinde Allerheiligen",
      "country": "DE",
      "sources": [
        "https://www.uokd.de/gemeinden"
      ],
      "address": [
        "Rumänisch-Orthodoxe Kirche",
        "Siebenbürgener Str. 2, 83301 Traunreut"
      ]
    },
    {
      "id": "de-ep-ukr-ukrainian-orthodox-parish-in-vechta-vechta-gemeinder-des-hl-panteleimon-grossmartyrer-un",
      "parent": "ep-ukrainian-western-europe",
      "kind": "parish",
      "rank": "Parish",
      "name": "Ukrainian Orthodox Vechta - parishioner of St. Panteleimon, great martyr and healer",
      "local": "Vechta - Gemeinder des Hl. Panteleimon, Großmärtyrer und Heiler",
      "country": "DE",
      "sources": [
        "https://www.uokd.de/gemeinden"
      ],
      "address": [
        "Feldmannskamp 1, 49377 Vechta"
      ]
    }
  ],
  "mk-europe": [
    {
      "id": "de-mk-macedonian-orthodox-church-community-in-dortmund",
      "parent": "mk-europe",
      "kind": "parish",
      "rank": "Parish",
      "name": "Macedonian Orthodox MPCO \"St. Cyril and Methodius\" - Dortmund",
      "local": "МПЦО \"Св. Кирил и Методиј\" - Дортмунд",
      "country": "DE",
      "sources": [
        "https://mpee.mk/category/d-o-r-t-m-u-n-d"
      ]
    },
    {
      "id": "de-mk-macedonian-orthodox-church-community-in-mainz",
      "parent": "mk-europe",
      "kind": "parish",
      "rank": "Parish",
      "name": "Macedonian Orthodox MPCO \"St. Nicholas\" - Mainz",
      "local": "МПЦО \"Св. Никола\" - Мајнц",
      "country": "DE",
      "sources": [
        "https://mpee.mk/category/m-a-j-n-c"
      ]
    },
    {
      "id": "de-mk-macedonian-orthodox-church-community-in-berlin",
      "parent": "mk-europe",
      "kind": "parish",
      "rank": "Parish",
      "name": "Macedonian Orthodox MPCO \"St. Kliment Ohridski\" - Berlin",
      "local": "МПЦО \"Св. Климент Охридски\" - Берлин",
      "country": "DE",
      "sources": [
        "https://mpee.mk/category/b-e-r-l-i-n-2"
      ]
    },
    {
      "id": "de-mk-macedonian-orthodox-church-community-in-laatzen-hannover",
      "parent": "mk-europe",
      "kind": "parish",
      "rank": "Parish",
      "name": "Macedonian Orthodox MPCO \"Sveti Spas\" - Latzen / Hanover in Laatzen / Hannover",
      "local": "МПЦО \"Свети Спас\" - Латцен / Хановер",
      "country": "DE",
      "sources": [
        "https://mpee.mk/category/l-a-t-c-e-n-xanover"
      ]
    },
    {
      "id": "de-mk-macedonian-orthodox-church-community-in-hamburg",
      "parent": "mk-europe",
      "kind": "parish",
      "rank": "Parish",
      "name": "Macedonian Orthodox Church Community in Hamburg",
      "local": "МПЦО - Хамбург",
      "country": "DE",
      "sources": [
        "https://mpee.mk/category/x-a-m-b-u-r-g"
      ]
    },
    {
      "id": "de-mk-macedonian-orthodox-church-community-in-munich",
      "parent": "mk-europe",
      "kind": "parish",
      "rank": "Parish",
      "name": "Macedonian Orthodox MPCO \"Holy Trinity\" - Munich",
      "local": "МПЦО \"Света Троица\" - Минхен",
      "country": "DE",
      "sources": [
        "https://mpee.mk/category/m-i-n-x-e-n"
      ]
    },
    {
      "id": "de-mk-macedonian-orthodox-church-community-in-ingolstadt",
      "parent": "mk-europe",
      "kind": "parish",
      "rank": "Parish",
      "name": "Macedonian Orthodox MPCO \"St. Nicholas\" - Inglostat in Ingolstadt",
      "local": "МПЦО \"Св. Никола\" - Инглоштат",
      "country": "DE",
      "sources": [
        "https://mpee.mk/category/i-n-g-l-o-s-t-a-t-2"
      ]
    },
    {
      "id": "de-mk-macedonian-orthodox-church-community-in-dusseldorf",
      "parent": "mk-europe",
      "kind": "parish",
      "rank": "Parish",
      "name": "Macedonian Orthodox MPCO \"Sveta Petka\" - Dusseldorf in Düsseldorf",
      "local": "МПЦО \"Света Петка\" - Диселдорф",
      "country": "DE",
      "sources": [
        "https://mpee.mk/category/d-i-s-e-l-d-o-r-f-2"
      ]
    },
    {
      "id": "de-mk-macedonian-orthodox-church-community-in-stuttgart",
      "parent": "mk-europe",
      "kind": "parish",
      "rank": "Parish",
      "name": "Macedonian Orthodox Church Community in Stuttgart",
      "local": "МПЦО - Штутгарт",
      "country": "DE",
      "sources": [
        "https://mpee.mk/category/s-t-u-t-g-a-r-t"
      ]
    },
    {
      "id": "de-mk-macedonian-orthodox-church-community-in-nuremberg",
      "parent": "mk-europe",
      "kind": "parish",
      "rank": "Parish",
      "name": "Macedonian Orthodox Church Community in Nuremberg",
      "local": "МПЦО - Нирнберг",
      "country": "DE",
      "sources": [
        "https://mpee.mk/category/n-i-r-n-b-e-r-g"
      ]
    },
    {
      "id": "de-mk-macedonian-orthodox-church-community-in-aalen",
      "parent": "mk-europe",
      "kind": "parish",
      "rank": "Parish",
      "name": "Macedonian Orthodox Church Community in Aalen",
      "local": "МПЦО - Аален",
      "country": "DE",
      "sources": [
        "https://mpee.mk/category/a-a-l-e-n-2"
      ]
    },
    {
      "id": "de-mk-macedonian-orthodox-church-community-in-sindelfingen",
      "parent": "mk-europe",
      "kind": "parish",
      "rank": "Parish",
      "name": "Macedonian Orthodox Church Community in Sindelfingen",
      "local": "МПЦО - Синделфинген",
      "country": "DE",
      "sources": [
        "https://mpee.mk/category/s-i-n-d-e-l-f-i-n-g-e-n"
      ]
    },
    {
      "id": "de-mk-macedonian-orthodox-church-community-in-cologne",
      "parent": "mk-europe",
      "kind": "parish",
      "rank": "Parish",
      "name": "Macedonian Orthodox MPCO \"Holy Trinity\" - Cologne",
      "local": "МПЦО \"Света Троица\" - Келн",
      "country": "DE",
      "sources": [
        "https://mpee.mk/category/k-e-l-n-2"
      ]
    },
    {
      "id": "de-mk-macedonian-orthodox-church-community-in-trier",
      "parent": "mk-europe",
      "kind": "parish",
      "rank": "Parish",
      "name": "Macedonian Orthodox MPCO \"St. Paul the Apostle\" - Trier",
      "local": "МПЦО \"Свети Апостол Павле\" - Триер",
      "country": "DE",
      "sources": [
        "https://mpee.mk/category/t-r-i-e-r-2"
      ]
    },
    {
      "id": "de-mk-macedonian-orthodox-church-community-in-fulda",
      "parent": "mk-europe",
      "kind": "parish",
      "rank": "Parish",
      "name": "Macedonian Orthodox MPCO \"Holy Three Saints\" - Fulda",
      "local": "МПЦО \"Свети Три Светители\" - Фулда",
      "country": "DE",
      "sources": [
        "https://mpee.mk/category/f-u-l-d-a"
      ]
    }
  ]
}

EXPECTED = {
  "ep-germany": 120,
  "an-germany": 29,
  "ru-berlin-and-germany": 94,
  "ru-germany-rocor": 74,
  "sr-dusseldorf-germany": 66,
  "ro-germany": 178,
  "ru-archdiocese-western-europe": 11,
  "bg-western-central-europe": 14,
  "ukraine-uoc": 15,
  "ep-ukrainian-western-europe": 30,
  "mk-europe": 15
}

ENGLISH_NAMES = {
    item["id"]: item["name"]
    for source_rows in ROWS.values()
    for item in source_rows
}


def clean(source):
    out = {key: value for key, value in source.items()
           if value not in (None, "", [])}
    out.setdefault("checked", CHECKED)
    sources = list(out.get("sources") or [])
    if not sources or len(sources) > 3:
        raise ValueError("%s must cite one to three sources" % out.get("id"))
    if not all(str(url).startswith("http") for url in sources):
        raise ValueError("%s carries a non-URL source" % out.get("id"))
    out["sources"] = sources
    out["cite"] = list(sources)
    for field in ("address", "services", "founded", "languages"):
        if (out.get(field) and
                (not isinstance(out[field], list) or
                 not all(isinstance(line, str) for line in out[field]))):
            raise ValueError("%s has invalid %s" % (out.get("id"), field))
    serialized = json.dumps(out, ensure_ascii=False)
    if any(mark in serialized for mark in ("\u2013", "\u2014",
                                            "\u2018", "\u2019",
                                            "\u201c", "\u201d")):
        raise ValueError("%s contains disallowed punctuation" % out.get("id"))
    return out


def build():
    payloads = {}
    seen = set(ROWS)
    all_new_ids = {item["id"] for source_rows in ROWS.values()
                   for item in source_rows}
    if len(all_new_ids) != sum(len(items) for items in ROWS.values()):
        raise ValueError("duplicate Germany source row id")
    for parent, source_rows in ROWS.items():
        rows = []
        branch_seen = {parent}
        pending = list(source_rows)
        while pending:
            progressed = False
            for source in list(pending):
                item = clean(source)
                if item.get("parent") not in branch_seen:
                    continue
                row_id = item.get("id")
                if not row_id or row_id in seen:
                    raise ValueError("duplicate or missing id: %s" % row_id)
                if item.get("kind") not in {"parish", "monastery"}:
                    raise ValueError("%s has unsupported kind" % row_id)
                if item.get("country") != "DE":
                    raise ValueError("%s is outside Germany" % row_id)
                if not item.get("name") or not item.get("local"):
                    raise ValueError("%s lacks a name" % row_id)
                if item.get("site") and not item["site"].startswith("http"):
                    raise ValueError("%s carries a non-URL site" % row_id)
                seen.add(row_id)
                branch_seen.add(row_id)
                rows.append(item)
                pending.remove(source)
                progressed = True
            if not progressed:
                raise ValueError("Germany child rows have unresolved parents")
        payloads[parent] = {
            "v": 1,
            "parent": parent,
            "country": "DE",
            "rows": rows,
        }
    actual = {parent: len(payload["rows"])
              for parent, payload in payloads.items()}
    if actual != EXPECTED:
        raise ValueError("Germany parent counts changed: %r" % actual)
    if len(ENGLISH_NAMES) != 646:
        raise ValueError("Germany English name coverage changed")
    return payloads


def manifest(payloads=None):
    payloads = payloads or build()
    return {
        parent: {
            "url": "/data/directory/%s.v1.json" % parent,
            "count": len(payload["rows"]),
            "country": "DE",
            "merge_required": True,
        }
        for parent, payload in sorted(payloads.items())
    }


def repository_problems(payloads):
    path = ROOT / "data" / "directory.v1.json"
    try:
        directory = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, ValueError) as exc:
        return ["cannot read %s: %s" % (path.relative_to(ROOT), exc)]
    base_ids = {item.get("id") for item in directory.get("rows", [])}
    errors = []
    for parent in payloads:
        if parent not in base_ids and parent not in SPINE_ROW_PROPOSALS:
            errors.append("missing directory parent: %s" % parent)
    for proposal_id, proposal in SPINE_ROW_PROPOSALS.items():
        if proposal_id in base_ids:
            existing = next(item for item in directory.get("rows", [])
                            if item.get("id") == proposal_id)
            compared = ("parent", "kind", "rank", "name", "local",
                        "country", "site", "sources")
            if any(existing.get(key) != proposal.get(key)
                   for key in compared):
                errors.append("published directory parent differs: %s" %
                              proposal_id)
        if proposal.get("parent") not in base_ids:
            errors.append("proposed directory parent has missing root: %s" %
                          proposal.get("parent"))
    new_ids = {item["id"] for payload in payloads.values()
               for item in payload["rows"]}
    duplicate_ids = sorted(new_ids & base_ids)
    if duplicate_ids:
        errors.append("Germany row IDs already in directory spine: %s" %
                      ", ".join(duplicate_ids))
    return errors


def main():
    parser = argparse.ArgumentParser()
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument("--check", action="store_true")
    mode.add_argument("--dump", action="store_true")
    args = parser.parse_args()
    try:
        payloads = build()
        errors = repository_problems(payloads)
    except (OSError, ValueError) as exc:
        print("directory Germany: %s" % exc, file=sys.stderr)
        return 1
    if errors:
        for error in errors:
            print(error, file=sys.stderr)
        return 1
    if args.dump:
        print(json.dumps(payloads, ensure_ascii=False, indent=2))
        return 0
    print("Germany branches: 646 rows")
    for parent, count in sorted(EXPECTED.items()):
        print("%s: %d" % (parent, count))
    print("spine proposal: ep-ukrainian-western-europe under constantinople")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
