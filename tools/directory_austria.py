#!/usr/bin/env python3
"""Validated directory fragments for canonical Orthodox bodies in Austria.

The parent jurisdictions also carry rows from other countries. This module
emits Austria-only fragments for later merging and never writes a shared
payload.

    python tools/directory_austria.py --check
    python tools/directory_austria.py --dump
"""

import argparse
import json
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent
CHECKED = "2026-11-14"

AUSTRIAN_BISHOPS = "https://orthodoxe-kirche.at/site/orthodoxedioezesen"
EP_PARISHES = "https://metropolisvonaustria.at/de/metropolis-de/pfarreien-de"
EP_MONASTERY = "https://metropolisvonaustria.at/de/metropolis-de/kloster-de"
SERBIAN_EAST = "https://www.crkva.at/de/parohije/bec/"
SERBIAN_CENTRAL = "https://www.crkva.at/de/pfarren/nord-ost-osterreich/"
SERBIAN_WEST = "https://www.crkva.at/de/pfarren/sud-west-osterreich/"
ROMANIAN_AUSTRIA = "https://mitropolia-ro.de/parohii-austria/"
MOSCOW_PARISHES = "https://austria-diocese.com/parishes/"
MOSCOW_CATHEDRAL = "https://austria-diocese.com/kafedralniy-sobor/"
ROCOR_GERMANY = "https://rocor.de/de/gemeinden-liste"
ROCOR_SALZBURG = (
    "https://directory.synod.com/listing/53/orthodoxe-kirche-maria-schutz/"
)
ANTIOCH_VIENNA = "https://rum-orthodox.de/gemeinden/wien/"
ANTIOCH_HALL = "https://rum-orthodox.de/gemeinden/innsbruck/"
BULGARIAN_DIRECTORY = "https://bg-patriarshia.bg/west-eu-diocese-temples"
GEORGIAN_AUSTRIA = (
    "https://www.orthodoxe-kirche.at/site/orthodoxedioezesen/"
    "georgischeorthodoxekirche"
)
MACEDONIAN_DIOCESE = "https://mpee.mk/"
MACEDONIAN_AUSTRIA = (
    "https://mpee.mk/post/istoriski-den-za-makedoncite-vo-avstrija-gradot-"
    "salcburg-ja-dobiva-cetvrtata-makedonska-crkovna-opstina"
)
MACEDONIAN_OLD_DIRECTORY = "https://www.mpc-evropa.de/hramovi.html"
UOC_AUSTRIA = (
    "https://vzcz.church.ua/2026/09/19/"
    "jepiskop-veniamin-vidvidav-parafiji-upc-v-avstriji-ta-ugorshhini/"
)


def row(row_id, parent, name, local, sources, rank="Parish", kind="parish",
        address=None, site=None, services=None, languages=None, founded=None):
    value = {
        "id": row_id,
        "parent": parent,
        "kind": kind,
        "rank": rank,
        "name": name,
        "local": local,
        "country": "AT",
        "sources": sources,
    }
    if address:
        value["address"] = address
    if site:
        value["site"] = site
    if services:
        value["services"] = services
    if languages:
        value["languages"] = languages
    if founded:
        value["founded"] = founded
    return value


EP_ROWS = [
    row("at-ep-vienna-holy-trinity", "ep-austria",
        "Holy Trinity Church Community in Vienna",
        "Kirchengemeinde zur Heiligen Dreifaltigkeit",
        [EP_PARISHES], rank="Church Community",
        address=["Fleischmarkt 13", "1010 Wien, Austria"]),
    row("at-ep-vienna-saint-george", "ep-austria",
        "St George Church Community in Vienna",
        "Kirchengemeinde zum Heiligen Georg",
        [EP_PARISHES], rank="Church Community",
        address=["Griechengasse 5", "1010 Wien, Austria"]),
    row("at-ep-vienna-vladimir-olga", "ep-austria",
        "Ukrainian-speaking Orthodox Parish of Sts Vladimir and Olga in Vienna",
        "Ukrainischsprachige Orthodoxe Kirchengemeinde zum Hl. Vladimir und zur Hl. Olga",
        [EP_PARISHES]),
    row("at-ep-vienna-john-chrysostom", "ep-austria",
        "German-speaking Orthodox Community of St John Chrysostom in Vienna",
        "Deutschsprachige Orthodoxe Gemeinde zum Hl. Johannes Chrysostomos",
        [EP_PARISHES], rank="Church Community",
        address=["Hafnersteig 8", "1010 Wien, Austria"],
        site="https://www.orthodoxie.at"),
    row("at-ep-st-polten-archangels", "ep-austria",
        "Ukrainian-speaking Orthodox Community of the Archangels in St Polten",
        "Ukrainischsprachige Orthodoxe Gemeinde der Erzengel (Sankt Pölten)",
        [EP_PARISHES], rank="Church Community",
        address=["St. Josefskirche, Josefstraße 46", "3100 St. Pölten, Austria"]),
    row("at-ep-perchtoldsdorf-protection", "ep-austria",
        "Ukrainian-speaking Orthodox Community of the Protection of the Mother of God in Perchtoldsdorf",
        "Ukrainischsprachige Orthodoxe Gemeinde Maria Schutz (Perchtoldsdorf)",
        [EP_PARISHES], rank="Church Community",
        address=["Martini-Kapelle, Paul-Katzberger-Platz 2",
                 "2380 Perchtoldsdorf, Austria"]),
    row("at-ep-jois-saint-nicholas", "ep-austria",
        "Ukrainian-speaking Community of St Nicholas in Jois",
        "Ukrainischsprachige Gemeinde zum Hl. Nikolaus (Jois)",
        [EP_PARISHES], rank="Church Community",
        address=["Herz-Jesu-Kirche, Hauptstraße 24a", "7093 Jois, Austria"]),
    row("at-ep-linz-presentation", "ep-austria",
        "Presentation of Christ Church Community in Linz",
        "Kirchengemeinde zur Begegnung des Herrn (Linz)",
        [EP_PARISHES], rank="Church Community",
        address=["Kirche St. Michael, Am Bindermichl 26", "4020 Linz, Austria"]),
    row("at-ep-linz-archangels", "ep-austria",
        "Ukrainian-speaking Orthodox Community of the Archangels in Linz",
        "Ukrainischsprachige Orthodoxe Gemeinde der Erzengel (Linz)",
        [EP_PARISHES], rank="Church Community"),
    row("at-ep-graz-cosmas-damian", "ep-austria",
        "Sts Cosmas and Damian Church Community in Graz",
        "Kirchengemeinde der Hl. Ärzte Kosmas und Damian (Graz)",
        [EP_PARISHES], rank="Church Community",
        address=["Universitätskirche Leechkirche, Rittergasse / Zinzendorfgasse 2",
                 "8030 Graz, Austria"]),
    row("at-ep-graz-andrew", "ep-austria",
        "Ukrainian-speaking Orthodox Community of St Andrew the First-Called in Graz",
        "Ukrainischsprachige Orthodoxe Gemeinde zum Hl. Apostel Andreas dem Erstberufenen (Graz)",
        [EP_PARISHES], rank="Church Community"),
    row("at-ep-leoben-perpetual-help", "ep-austria",
        "Mother of Perpetual Help Church Community in Leoben",
        "Kirchengemeinde zur Hl. Maria Mutter von der Immerwährenden Hilfe (Leoben)",
        [EP_PARISHES], rank="Church Community",
        address=["St. Alfonskirche, Gösserstraße 15", "8700 Leoben, Austria"]),
    row("at-ep-klagenfurt-all-saints", "ep-austria",
        "All Saints Church Community in Klagenfurt",
        "Kirchengemeinde Aller Heiligen (Klagenfurt)",
        [EP_PARISHES], rank="Church Community",
        address=["Kirche St. Markus, Kaufmanngasse 11", "9020 Klagenfurt, Austria"]),
    row("at-ep-salzburg-demetrios", "ep-austria",
        "St Demetrios Church Community in Salzburg",
        "Kirchengemeinde zum Heiligen Dimitrios (Salzburg)",
        [EP_PARISHES], rank="Church Community",
        address=["Kirche St. Erhard, Nonntaler Hauptstrasse 12",
                 "5020 Salzburg, Austria"]),
    row("at-ep-salzburg-resurrection", "ep-austria",
        "Ukrainian-speaking Community of the Resurrection of the Lord in Salzburg",
        "Ukrainischsprachige Gemeinde der Auferstehung des Herrn (Salzburg)",
        [EP_PARISHES], rank="Church Community",
        address=["Herz-Jesu-Heim, Hubnergasse 5-7", "5020 Salzburg, Austria"]),
    row("at-ep-innsbruck-john-baptist", "ep-austria",
        "St John the Baptist Church Community in Innsbruck",
        "Kirchengemeinde des Heiligen Johannes des Vorläufers (Innsbruck)",
        [EP_PARISHES], rank="Church Community",
        address=["Kirche der Siebererschule, Siebererstraße 7",
                 "6020 Innsbruck, Austria"]),
    row("at-ep-kufstein-holy-trinity", "ep-austria",
        "Holy Trinity Church Community in Kufstein",
        "Kirchengemeinde der Hl. Dreifaltigkeit (Kufstein)",
        [EP_PARISHES], rank="Church Community",
        address=["Dreifaltigkeitskirche, Pfarrplatz 2", "6330 Kufstein, Austria"]),
    row("at-ep-lauterach-three-hierarchs", "ep-austria",
        "Three Holy Hierarchs Church Community in Lauterach-Bregenz",
        "Kirchengemeinde der Hl. drei Hierarchen (Lauterach-Bregenz)",
        [EP_PARISHES], rank="Church Community",
        address=["Kloster Lauterach, Klosterstraße 1",
                 "6923 Lauterach-Bregenz, Austria"]),
    row("at-ep-st-andra-protection-paisios-monastery", "ep-austria",
        "Protection of the Mother of God and St Paisios of Mount Athos Monastery",
        "Kloster Schutz der Allerheiligsten Gottesgebärerin und des Heiligen Paisios aus dem Berg Athos",
        [EP_MONASTERY], rank="Monastery", kind="monastery",
        address=["Bahngasse 39-40", "7161 Sankt Andrä am Zicksee, Austria"],
        site="https://kloster-maria-schutz.metropolisvonaustria.at/",
        services=["Monday to Saturday: Matins and Divine Liturgy 06:00-09:00; supplication 12:15-12:45; evening service 17:00-18:00.",
                  "Sunday and feast days: Matins and Divine Liturgy 07:00-10:30; supplication 12:15-12:45; evening service 17:00-18:00."]),
]


SERBIAN_ROWS = [
    row("at-sr-vienna-saint-sava-cathedral", "sr-austria-switzerland",
        "St Sava Cathedral in Vienna", "Саборна црква Светога Саве у трећем округу",
        [SERBIAN_EAST], rank="Cathedral",
        address=["Veithgasse 3", "1030 Wien, Austria"]),
    row("at-sr-vienna-nativity-theotokos", "sr-austria-switzerland",
        "Nativity of the Mother of God Church in Vienna",
        "Црква Рођења Пресвете Богородице у шеснаестом округу",
        [SERBIAN_EAST], rank="Church",
        address=["Neulerchenfelderstrasse 47", "1160 Wien, Austria"]),
    row("at-sr-vienna-resurrection", "sr-austria-switzerland",
        "Resurrection of Christ Church in Vienna",
        "Црква Васкрсења Христовог у другом округу",
        [SERBIAN_EAST], rank="Church",
        address=["Engerthstrasse 158", "1020 Wien, Austria"],
        site="https://www.vaskrs.com"),
    row("at-sr-vienna-akathist-theotokos", "sr-austria-switzerland",
        "Akathist to the Mother of God Church in Vienna",
        "Храм Акатиста Пресвете Богородице у дванаестом округу",
        [SERBIAN_EAST], rank="Church",
        address=["Lichtensterngasse 4A", "1120 Wien, Austria"]),
    row("at-sr-wiener-neustadt-platon", "sr-austria-switzerland",
        "Hieromartyr Platon of Banja Luka Church in Wiener Neustadt",
        "Црква светог свештеномученика Платона бањалучког",
        [SERBIAN_EAST], rank="Church",
        address=["Messenhausergasse 4", "2700 Wiener Neustadt, Austria"]),
    row("at-sr-st-polten-thomas", "sr-austria-switzerland",
        "Holy Apostle Thomas Church in St Polten", "Црква светог апостола Томе",
        [SERBIAN_EAST], rank="Church",
        address=["Hanuschplatz 1-5", "3100 St. Polten-Stattersdorf, Austria"]),
    row("at-sr-tulln-nicholas", "sr-austria-switzerland",
        "St Nicholas of Myra Church in Tulln", "Црква светог оца Николаја Мирликијског",
        [SERBIAN_EAST], rank="Church",
        address=["Grünwaldgasse 22", "3430 Tulln an der Donau, Austria"]),
    row("at-sr-gmunden-george", "sr-austria-switzerland",
        "Holy Great Martyr George Parish in Gmunden-Vocklabruck",
        "PFARRE HEILIGER GROSSMÄRTYRER GEORG", [SERBIAN_CENTRAL],
        address=["Miller-von-Aichholz-Strasse 25", "4810 Gmunden, Austria"],
        site="https://www.spc-gmunden.at"),
    row("at-sr-wels-entry-theotokos", "sr-austria-switzerland",
        "Entry of the Most Holy Mother of God Parish in Wels",
        "PFARRE ZUM TEMPELGANG DER ALLERHEILIGSTEN GOTTESGEBÄRERIN",
        [SERBIAN_CENTRAL], address=["Herrengasse 2", "4600 Wels, Austria"]),
    row("at-sr-enns-relics-sava", "sr-austria-switzerland",
        "Translation of the Relics of St Sava Church in Enns",
        "KIRCHE DER ÜBERTRAGUNG DER RELIQUIEN DES HEILIGEN SAVA",
        [SERBIAN_CENTRAL], rank="Church",
        address=["Stelzhamerstrasse 16", "4470 Enns, Austria"]),
    row("at-sr-braunau-mark", "sr-austria-switzerland",
        "Holy Apostle Mark Parish in Braunau am Inn",
        "PFARRE DES HEILIGEN APOSTEL MARKUS", [SERBIAN_CENTRAL],
        address=["Ringstrasse 39", "5280 Braunau am Inn, Austria"],
        site="http://www.spc-braunau.org"),
    row("at-sr-linz-basil-ostrog", "sr-austria-switzerland",
        "St Basil of Ostrog Church in Linz",
        "KIRCHE DES HEILIGEN VASILIJE VON OSTROG", [SERBIAN_CENTRAL],
        rank="Church", address=["Posthofstrasse 41", "4020 Linz, Austria"],
        site="https://www.spc-linz.at"),
    row("at-sr-graz-cyril-methodius", "sr-austria-switzerland",
        "Sts Cyril and Methodius Parish in Graz", "PFARRE HEILIGE KYRILL UND METHOD",
        [SERBIAN_CENTRAL], address=["Liebenauer Hauptstrasse 291", "8020 Graz, Austria"]),
    row("at-sr-klagenfurt-paraskeva", "sr-austria-switzerland",
        "Venerable Mother Paraskeva Parish in Klagenfurt",
        "PFARRE EHRWÜRDIGE MUTTER PARASKEVA", [SERBIAN_CENTRAL],
        address=["Kaufmanngasse 11", "9020 Klagenfurt, Austria"]),
    row("at-sr-villach-filial", "at-sr-klagenfurt-paraskeva",
        "Villach Filial Church of the Venerable Mother Paraskeva Parish",
        "Filialkirche in Villach", [SERBIAN_CENTRAL], rank="Filial Church",
        address=["Burgplatz 1", "9500 Villach, Austria"]),
    row("at-sr-spittal-filial", "at-sr-klagenfurt-paraskeva",
        "Spittal an der Drau Filial Church of the Venerable Mother Paraskeva Parish",
        "Filialkirche in Spital an der Drau", [SERBIAN_CENTRAL], rank="Filial Church",
        address=["Hammerfeld 1", "9800 Spittal an der Drau, Austria"]),
    row("at-sr-bregenz-constantine-helen", "sr-austria-switzerland",
        "Sts Constantine and Helen Parish in Bregenz",
        "PFARRE HL. KONSTANTIN UND HELENA", [SERBIAN_WEST],
        address=["St. Gebhardkirche, Wuhrwaldstraße 24", "6900 Bregenz, Austria"]),
    row("at-sr-innsbruck-john-baptist", "sr-austria-switzerland",
        "Nativity of St John the Baptist Parish in Innsbruck",
        "PFARRE GEBURT DES HEILIGEN JOHANNES DES TÄUFERS", [SERBIAN_WEST],
        address=["Sieberer Strasse 7", "6020 Innsbruck, Austria"],
        site="https://www.spc-innsbruck.at"),
    row("at-sr-reutte-filial", "at-sr-innsbruck-john-baptist",
        "Reutte Filial Church of the Nativity of St John the Baptist Parish",
        "Filialkirche in Reutte", [SERBIAN_WEST], rank="Filial Church",
        address=["Planseestrasse 49", "6600 Reutte, Austria"]),
    row("at-sr-kufstein-visarion", "sr-austria-switzerland",
        "St Visarion the Confessor Parish in Kufstein",
        "PFARRE HEILIGER VISARIJON DER BEKENNER", [SERBIAN_WEST],
        address=["Einfangstrasse 10", "6330 Kufstein, Austria"]),
    row("at-sr-fugen-filial", "at-sr-kufstein-visarion",
        "Fugen Filial Church of St Visarion the Confessor Parish",
        "Filialkirche in Fugen", [SERBIAN_WEST], rank="Filial Church",
        address=["Pfarrkirche Maria Himmelfahrt, Lindenweg 72", "6260 Fugen, Austria"]),
    row("at-sr-saalfelden-all-serbian-saints", "sr-austria-switzerland",
        "Synaxis of All Serbian Saints Church in Saalfelden",
        "KIRCHE DER SYNAXE ALLER SERBISCHEN HEILIGEN", [SERBIAN_WEST],
        rank="Church", address=["Anton-Wallner-Strasse 1a", "5760 Saalfelden, Austria"],
        site="https://www.spc-saalfelden.at"),
    row("at-sr-bischofshofen-filial", "at-sr-saalfelden-all-serbian-saints",
        "Bischofshofen Filial Church of the Synaxis of All Serbian Saints Church",
        "Filialkirche in Bischofshofen", [SERBIAN_WEST], rank="Filial Church",
        address=["Kloster Hl. Rupert", "5500 Bischofshofen, Austria"]),
    row("at-sr-salzburg-protection", "sr-austria-switzerland",
        "Protection and Intercession of the Mother of God Church in Salzburg",
        "KIRCHE MARIÄ SCHUTZ UND FÜRBITTE (POKROV)", [SERBIAN_WEST],
        rank="Church", address=["Schmiedingerstrasse 48", "5020 Salzburg, Austria"],
        site="https://www.spco-salzburg.org"),
    row("at-sr-feldkirch-nativity-theotokos", "sr-austria-switzerland",
        "Nativity of the Most Holy Mother of God Parish in Feldkirch",
        "PFARRE GEBURT DER ALLERHEILIGSTEN GOTTESGEBÄRERIN", [SERBIAN_WEST],
        address=["Frauenkirche, Churer Tor 2", "6800 Feldkirch, Austria"]),
]


ROMANIAN_ROWS = [
    row("at-ro-amstetten-paisie-agatha", "ro-germany",
        "St Paisius of Neamt and St Agatha Parish in Amstetten",
        "Parohia \"Sf. Cuv. Paisie de la Neamț\" și \"Sf. Mc. Agata\"",
        [ROMANIAN_AUSTRIA], address=["Sudtirolerstrasse 1", "3300 Amstetten, Austria"]),
    row("at-ro-baden-brancoveanu", "ro-germany",
        "Holy Brancoveanu Martyrs Parish in Baden bei Wien",
        "Parohia \"Sf. Martiri Brâncoveni\"", [ROMANIAN_AUSTRIA],
        address=["Badener Strasse 28", "2522 Oberwaltersdorf, Austria"]),
    row("at-ro-bischofshofen-prodromita", "ro-germany",
        "Prodromita Mother of God Parish in Bischofshofen",
        "Parohia \"Maica Domnului Prodromița\"", [ROMANIAN_AUSTRIA],
        address=["Frauenkirche, Gaisberggasse", "5500 Bischofshofen, Austria"]),
    row("at-ro-braunau-john-florian", "ro-germany",
        "St John the Baptist and St Florian of Lorch Parish in Braunau am Inn",
        "Parohia \"Sfântul Ioan Botezătorul\" şi \"Sf. Florian de Lorch\"",
        [ROMANIAN_AUSTRIA], address=["Burgerspitalkirche, Palmplatz 10",
                                    "5280 Braunau am Inn, Austria"],
        site="https://www.parohia-braunau.at"),
    row("at-ro-bruck-calinic-sophrony", "ro-germany",
        "St Calinic of Cernica and St Sophrony Sakharov Parish in Bruck an der Mur-Kapfenberg",
        "Parohia \"Sf. Ier. Calinic de la Cernica\" și \"Sf. Cuv. Sofronie Saharov\"",
        [ROMANIAN_AUSTRIA], address=["Minoritenkirche, Minoritenplatz",
                                    "8600 Bruck an der Mur, Austria"],
        site="https://www.bruck-orthodox.at"),
    row("at-ro-dornbirn-protection-catherine-dionisie", "ro-germany",
        "Protection of the Mother of God, St Catherine and St Dionisie Parish in Dornbirn",
        "Parohia \"Acoperământul Maicii Domnului\", \"Sf. Mc. Ecaterina\" și \"Sf. Ier. Dionisie, Episcopul Cetății Albe-Ismail\"",
        [ROMANIAN_AUSTRIA], address=["Watzenegg 51", "6850 Dornbirn, Austria"]),
    row("at-ro-feldkirch-nativity-christ", "ro-germany",
        "Nativity of Christ Parish in Feldkirch", "Parohia \"Naşterea Domnului\"",
        [ROMANIAN_AUSTRIA], address=["Kapuzinerkloster, Bahnhofstrasse 4",
                                    "6800 Feldkirch, Austria"],
        site="https://www.biserica-romana.at"),
    row("at-ro-bregenz-filial", "at-ro-feldkirch-nativity-christ",
        "Bregenz Filial Church of the Nativity of Christ Parish",
        "Bregenz - filie", [ROMANIAN_AUSTRIA], rank="Filial Church",
        address=["Kloster der Redemptionistinnen, Klosterstrasse 1",
                 "6923 Lauterach, Austria"]),
    row("at-ro-ganserndorf-constantine-helena-arsenie", "ro-germany",
        "Sts Constantine and Helen and St Arsenie of Prislop Parish in Ganserndorf",
        "Parohia \"Sfinții Împărați Constantin și Elena\" și \"Sf. Cuv. Mărt. Arsenie de la Prislop\"",
        [ROMANIAN_AUSTRIA], address=["Oed Aigenstrasse 9", "2230 Ganserndorf, Austria"]),
    row("at-ro-gleisdorf-joseph-ruprecht", "ro-germany",
        "St Joseph the New of Partos and St Rupert of Salzburg Parish in Gleisdorf",
        "Parohia \"Sf. Ier. Iosif cel Nou de la Partoș și Ruprecht de Salzburg\"",
        [ROMANIAN_AUSTRIA], address=["Dietmannsdorferstrasse 460",
                                    "8181 St. Ruprecht an der Raab, Austria"],
        site="https://www.gleisdorf-orthodox.at"),
    row("at-ro-graz-nicholas", "ro-germany", "St Nicholas Parish in Graz",
        "Parohia \"Sf. Ier. Nicolae\"", [ROMANIAN_AUSTRIA],
        address=["Dreifaltigkeitskirche, Schlossbergplatz 1", "8010 Graz, Austria"],
        site="https://www.parohia-ortodoxa-graz.at"),
    row("at-ro-graz-andrew-florian", "ro-germany",
        "St Andrew and St Florian of Lorch Parish in Graz",
        "Parohia \"Sf. Ap. Andrei\" și \"Sf. Mc. Florian din Lorch\"",
        [ROMANIAN_AUSTRIA], address=["Kalvariengurtel 56", "8020 Graz, Austria"],
        site="https://www.sfantul-andrei-graz.at"),
    row("at-ro-innsbruck-john-confessors", "ro-germany",
        "St John the New of Suceava and the Transylvanian Confessors Parish in Innsbruck",
        "Parohia \"Sf. M. Mc. Ioan cel Nou de la Suceava\" și \"Sf. Mărturisitori Ardeleni\"",
        [ROMANIAN_AUSTRIA], address=["Biserica St. Pirmin, Radetzkystrasse 51",
                                    "6020 Innsbruck, Austria"]),
    row("at-ro-klagenfurt-demetrios", "ro-germany",
        "Great Martyr Demetrios the Myrrh-Streamer Parish in Klagenfurt",
        "Parohia \"Sf. Mc. Dimitrie Izvorâtorul de Mir\"", [ROMANIAN_AUSTRIA],
        address=["Flughafenstrasse 9-11", "9020 Klagenfurt, Austria"],
        site="https://www.rumkirche-klagenfurt.at"),
    row("at-ro-villach-filial", "at-ro-klagenfurt-demetrios",
        "Villach Filial Church of the Great Martyr Demetrios Parish",
        "Villach - filie", [ROMANIAN_AUSTRIA], rank="Filial Church",
        address=["Burgplatz 1", "9500 Villach, Austria"]),
    row("at-ro-knittelfeld-archangels", "ro-germany",
        "Holy Archangels Michael and Gabriel Parish in Knittelfeld",
        "Parohia \"Sf. Arhangheli Mihail şi Gavriil\"", [ROMANIAN_AUSTRIA],
        address=["Kapuziner Platz 4", "8720 Knittelfeld, Austria"],
        site="https://www.parohia-ortodoxa.org"),
    row("at-ro-krems-archangels-paisie", "ro-germany",
        "Holy Archangels Michael and Gabriel and St Paisius of Neamt Parish in Krems",
        "Parohia \"Sf. Arhangheli Mihail şi Gavriil\" și \"Sf. Cuv. Paisie de la Neamț\"",
        [ROMANIAN_AUSTRIA], address=["Lossgasse 2", "3500 Krems an der Donau, Austria"]),
    row("at-ro-kufstein-transylvanian-martyrs", "ro-germany",
        "Holy Transylvanian Martyrs Parish in Kufstein",
        "Parohia \"Sfinții Martiri Ardeleni\"", [ROMANIAN_AUSTRIA],
        address=["Krankenhausgasse 18", "6330 Kufstein, Austria"]),
    row("at-ro-liezen-andrew", "ro-germany", "St Andrew Parish in Liezen-Trieben",
        "Parohia \"Sf. Ap. Andrei\"", [ROMANIAN_AUSTRIA],
        address=["Niederhofen 23", "8950 Niederhofen, Austria"]),
    row("at-ro-linz-descent-holy-spirit", "ro-germany",
        "Descent of the Holy Spirit Parish in Linz",
        "Parohia \"Pogorârea Sfântului Duh\"", [ROMANIAN_AUSTRIA],
        address=["Frobelstrasse 30", "4020 Linz, Austria"]),
    row("at-ro-traun-calinic-martin", "ro-germany",
        "St Calinic of Cernica and St Martin of Tours Parish in Traun",
        "Parohia \"Sf. Ier. Calinic de la Cernica\" și \"Sf. Ier. Martin de Tours\"",
        [ROMANIAN_AUSTRIA], address=["Schubertstrasse 10", "4050 Traun, Austria"]),
    row("at-ro-mattighofen-parascheva", "ro-germany",
        "St Parascheva of Iasi Parish in Mattighofen",
        "Parohia \"Sf. Cuv. Parascheva de la Iași\"", [ROMANIAN_AUSTRIA],
        address=["Romerstrasse 12", "5230 Mattighofen, Austria"]),
    row("at-ro-modling-ascension-paisie-cleopa", "ro-germany",
        "Ascension of the Lord and Sts Paisie and Cleopa of Sihastria Parish in Modling",
        "Parohia \"Înălțarea Domnului\" și \"Sf. Cuv. Paisie și Cleopa de la Sihăstria\"",
        [ROMANIAN_AUSTRIA], address=["Weisses-Kreuz-Gasse 66", "2340 Modling, Austria"]),
    row("at-ro-oberpullendorf-sophrony", "ro-germany",
        "St Sophrony of Essex Parish in Oberpullendorf",
        "Parohia \"Sf. Cuv. Sofronie de la Essex\"", [ROMANIAN_AUSTRIA],
        address=["Ungargasse 62", "7350 Mitterpullendorf, Austria"]),
    row("at-ro-oberwart-confessors-paisios", "ro-germany",
        "Transylvanian Confessors and St Paisios the Athonite Parish in Oberwart",
        "Parohia \"Sf. Mărturisitori Ardeleni\" şi \"Sf. Cuv. Paisie Aghioritul\"",
        [ROMANIAN_AUSTRIA], address=["Kirchengasse 23", "7551 Stegersbach, Austria"],
        site="https://www.oberwart-orthodox.at"),
    row("at-ro-salzburg-archangels-epictetus-astion", "ro-germany",
        "Holy Archangels Michael and Gabriel and Sts Epictetus and Astion Parish in Salzburg",
        "Parohia \"Sf. Arhangheli Mihail şi Gavriil\" şi \"Sf. Mc. Epictet şi Astion\"",
        [ROMANIAN_AUSTRIA], address=["Robinigstrasse 48", "5020 Salzburg, Austria"],
        site="https://www.parohia-salzburg.ro"),
    row("at-ro-st-polten-hippolytus-brancoveanu", "ro-germany",
        "St Hippolytus of Rome and the Holy Brancoveanu Martyrs Parish in St Polten",
        "Parohia \"Sf. Ierarh Ipolit Romanul\" şi \"Sf. Martiri Brâncoveni\"",
        [ROMANIAN_AUSTRIA], address=["Salcherstrasse 43", "3104 St. Polten-Harland, Austria"],
        site="https://www.constantinbrancoveanu.at"),
    row("at-ro-stockerau-coloman-arsenie", "ro-germany",
        "St Coloman of Stockerau and St Arsenie of Prislop Parish in Stockerau",
        "Parohia \"Sf. Coloman din Stockerau\" și \"Sf. Cuv. Arsenie de la Prislop\"",
        [ROMANIAN_AUSTRIA], address=["Stockerauer Strasse 23", "2104 Spillern, Austria"]),
    row("at-ro-vienna-resurrection-andrew", "ro-germany",
        "Holy Resurrection and St Andrew Parish in Vienna",
        "Parohia \"La Sfânta Înviere\" şi \"Sf. Apostol Andrei\"",
        [ROMANIAN_AUSTRIA], address=["Simmeringer Hauptstrasse 161 / Kobelgasse 18",
                                    "1110 Wien, Austria"],
        site="https://www.rumkirche.at"),
    row("at-ro-vienna-antony-andrei-saguna", "ro-germany",
        "St Antony the Great and St Andrei Saguna Parish in Vienna",
        "Parohia \"Sf. Antonie cel Mare\" şi \"Sf. Ier. Andrei Şaguna\"",
        [ROMANIAN_AUSTRIA], address=["Pouthongasse 16", "1150 Wien, Austria"],
        site="https://www.sfantonie.at"),
    row("at-ro-vienna-holy-spirit-stephen", "ro-germany",
        "Descent of the Holy Spirit and St Stephen the Great Parish in Vienna",
        "Parohia \"Pogorârea Sfântului Duh\" şi \"Sf. Voievod Ștefan cel Mare\"",
        [ROMANIAN_AUSTRIA], address=["Bruno Marek Allee 7b", "1020 Wien, Austria"],
        site="https://www.sfstefan.at"),
    row("at-ro-vienna-john-suceava-chapel", "ro-germany",
        "St John the New of Suceava Romanian Chapel in Vienna",
        "Parohia \"Sf. Ioan cel Nou de la Suceava\" (Capela Românească)",
        [ROMANIAN_AUSTRIA], rank="Chapel",
        address=["Lowelstrasse 8/2", "1010 Wien, Austria"],
        site="https://www.capela.at"),
    row("at-ro-voitsberg-elijah-theodora", "ro-germany",
        "Prophet Elijah and St Theodora of Sihla Parish in Voitsberg",
        "Parohia \"Sf. Prooroc Ilie Tesviteanul\" și \"Sf. Cuv. Teodora de la Sihla\"",
        [ROMANIAN_AUSTRIA], address=["Josef-Radkohl-Strasse 18", "8570 Voitsberg, Austria"],
        site="https://www.voitsberg-orthodox.de"),
    row("at-ro-vocklabruck-annunciation-john-jacob", "ro-germany",
        "Annunciation and St John Jacob of Neamt Parish in Vocklabruck",
        "Parohia \"Buna Vestire\" și \"Sf. Cuvios Ioan Iacob de la Neamț\"",
        [ROMANIAN_AUSTRIA], address=["Salzburgerstrasse 16", "4840 Vocklabruck, Austria"]),
    row("at-ro-wels-protection-justin", "ro-germany",
        "Protection of the Mother of God and St Justin Martyr Parish in Wels",
        "Parohia \"Acoperământul Maicii Domnului\" și \"Sf. Iustin Martirul\"",
        [ROMANIAN_AUSTRIA], address=["Welser Strasse 15", "4614 Marchtrenk, Austria"]),
    row("at-ro-wiener-neustadt-nicholas-parascheva", "ro-germany",
        "St Nicholas and St Parascheva of Iasi Parish in Wiener Neustadt",
        "Parohia \"Sf. Ier. Nicolae\" și \"Sf. Cuv. Parascheva de la Iași\"",
        [ROMANIAN_AUSTRIA], address=["Gunthergasse 14", "2700 Wiener Neustadt, Austria"],
        site="https://www.sfantaparascheva.at"),
    row("at-ro-zell-confessors-filial", "at-ro-bischofshofen-prodromita",
        "Sts Visarion, Oprea and John of Gales Filial Church in Zell am See",
        "Filia \"Sf. Mărturisitori Visarion, Oprea și Ioan din Galeș\"",
        [ROMANIAN_AUSTRIA], rank="Filial Church",
        address=["Hofmannsthalstrasse 12", "5700 Zell am See, Austria"]),
]


MOSCOW_ROWS = [
    row("at-mp-vienna-nicholas-cathedral", "ru-vienna-and-austria",
        "St Nicholas Cathedral in Vienna", "Кафедральный собор Святителя Николая",
        [MOSCOW_CATHEDRAL, MOSCOW_PARISHES], rank="Cathedral",
        address=["Jauresgasse 2", "1030 Wien, Austria"],
        site="https://nikolsobor.org"),
    row("at-mp-vienna-lazarus", "ru-vienna-and-austria",
        "St Lazarus the Four-Days-Dead Church in Vienna",
        "Храм Святого Лазаря Четверодневного", [MOSCOW_PARISHES], rank="Church",
        address=["Simmeringer Hauptstrasse 234", "1110 Wien, Austria"]),
    row("at-mp-graz-protection", "ru-vienna-and-austria",
        "Protection of the Mother of God Parish in Graz",
        "Приход Покрова Пресвятой Богородицы (Грац)", [MOSCOW_PARISHES],
        address=["Schatzkammerkapelle, Mariahilferplatz 3", "8020 Graz, Austria"],
        site="https://pokrova-graz.at"),
    row("at-mp-innsbruck-protection", "ru-vienna-and-austria",
        "Protection of the Mother of God Parish in Innsbruck",
        "Приход Покрова Пресвятой Богородицы (Иннсбрук)", [MOSCOW_PARISHES],
        address=["Sieberer Strasse 7", "6020 Innsbruck, Austria"],
        site="https://www.russprihod.eu"),
    row("at-mp-laa-archangel-michael", "ru-vienna-and-austria",
        "Holy Archangel Michael Church in Laa an der Thaya",
        "Храм святого Архистратига Божия Михаила", [MOSCOW_PARISHES], rank="Church",
        address=["Ruhhofstrasse 93", "2136 Laa an der Thaya, Austria"],
        site="https://laacerkov.com"),
    row("at-mp-linz-new-martyrs", "ru-vienna-and-austria",
        "Holy New Martyrs and Confessors of Russia Parish in Linz",
        "Приход Святых Новомучеников и Исповедников Российских", [MOSCOW_PARISHES],
        address=["Biberweg 30, Pichling", "4030 Linz, Austria"]),
    row("at-mp-st-polten-hippolytus", "ru-vienna-and-austria",
        "St Hippolytus of Rome Community in St Polten",
        "Община святого Ипполита Римского", [MOSCOW_PARISHES], rank="Church Community",
        address=["Hanuschplatz 1", "3100 St. Polten-Stattersdorf, Austria"]),
]


ROCOR_ROWS = [
    row("at-rocor-salzburg-protection", "ru-germany-rocor",
        "Protection of the Mother of God Orthodox Church in Salzburg",
        "Orthodoxe Kirche Maria Schutz", [ROCOR_GERMANY, ROCOR_SALZBURG],
        rank="Church", address=["Christian-Doppler-Strasse 3a", "5020 Salzburg, Austria"],
        site="https://www.pokrovsbg.eu",
        services=["Weekly services."], languages=["Church Slavonic", "German"]),
]


ANTIOCH_ROWS = [
    row("at-an-vienna-peter-paul", "an-germany",
        "Sts Peter and Paul Community in Vienna", "Gemeinde St. Petrus und Paulus",
        [ANTIOCH_VIENNA], rank="Church Community",
        address=["Funfhausgasse 25", "1150 Wien, Austria"],
        services=["Sunday: Divine Liturgy at 11:00."]),
    row("at-an-hall-saint-george", "an-germany",
        "St George Community in Hall in Tirol", "Gemeinde St. Georgios",
        [ANTIOCH_HALL], rank="Church Community",
        address=["Straubstrasse 9", "6060 Hall in Tirol, Austria"],
        services=["First Sunday of each month: Divine Liturgy at 10:00."]),
]


BULGARIAN_ROWS = [
    row("at-bg-vienna-john-rila", "bg-western-central-europe",
        "St John of Rila Bulgarian Orthodox Church Community in Vienna",
        "БПЦО \"Св. Йоан Рилски\" - гр. Виена", [BULGARIAN_DIRECTORY],
        rank="Church Community", address=["Dunklengasse 21, Top 1",
                                          "1120 Wien, Austria"],
        site="https://www.bok.at"),
    row("at-bg-vienna-cyril-methodius-chapel", "bg-western-central-europe",
        "Sts Cyril and Methodius Episcopal Chapel in Vienna",
        "БПЦО \"Св. Кирил и Методий\", архиерейски параклис - гр. Виена",
        [BULGARIAN_DIRECTORY], rank="Episcopal Chapel",
        address=["Klagbaumgasse 4", "1040 Wien, Austria"]),
]


GEORGIAN_ROWS = [
    row("at-ge-vienna-david-builder", "georgia",
        "St King David the Builder Georgian Orthodox Community in Vienna",
        "Georgisch-orthodoxe Gemeinde zum Heiligen König David d. Erneuerer in Wien",
        [GEORGIAN_AUSTRIA, AUSTRIAN_BISHOPS], rank="Church Community",
        address=["Brigitta-Kapelle, Forsthausgasse 15", "1200 Wien, Austria"],
        services=["Saturday 18:00: All-Night Vigil and confession.",
                  "Sunday and feast days 10:00: Divine Liturgy in Georgian."]),
    row("at-ge-graz-nino", "georgia", "St Nino Community in Graz",
        "Gemeinde der Hl. Nino in Graz", [GEORGIAN_AUSTRIA, AUSTRIAN_BISHOPS],
        rank="Church Community", address=["Mariengasse 31", "8020 Graz, Austria"],
        services=["Third Saturday of each month at 10:00."], founded=["2010"]),
    row("at-ge-linz-george", "georgia", "St George Community in Linz",
        "Gemeinde des Hl. Georgs in Linz", [GEORGIAN_AUSTRIA, AUSTRIAN_BISHOPS],
        rank="Church Community", address=["Posthofstrasse 41", "4020 Linz, Austria"],
        services=["Once monthly at 09:00 by arrangement with the Serbian church."],
        founded=["2009"]),
]


MACEDONIAN_ROWS = [
    row("at-mk-vienna-naum-ohrid", "mk-europe",
        "St Naum of Ohrid Macedonian Orthodox Church Community in Vienna",
        "Црковна општина \"Св. Наум Охридски\" - Виена",
        [MACEDONIAN_DIOCESE, MACEDONIAN_OLD_DIRECTORY], rank="Church Community",
        address=["Siemensstrasse 24", "1210 Wien, Austria"]),
    row("at-mk-linz-demetrios", "mk-europe",
        "St Demetrios Macedonian Orthodox Church Community in Linz",
        "МПЦО \"Свети Димитриј\" Линц",
        [MACEDONIAN_DIOCESE, MACEDONIAN_AUSTRIA], rank="Church Community"),
    row("at-mk-villach-community", "mk-europe",
        "Macedonian Orthodox Church Community in Villach",
        "Македонска православна црковна општина во Филах",
        [MACEDONIAN_DIOCESE, MACEDONIAN_AUSTRIA], rank="Church Community"),
    row("at-mk-salzburg-community", "mk-europe",
        "Macedonian Orthodox Church Community in Salzburg",
        "Македонска православна црковна општина во Салцбург",
        [MACEDONIAN_DIOCESE, MACEDONIAN_AUSTRIA], rank="Church Community"),
]


UOC_ROWS = [
    row("at-uoc-vienna-kyiv-caves-fathers", "ukraine-uoc",
        "All Venerable Fathers of the Kyiv Caves Parish in Vienna",
        "Парафія Української Православної Церкви на честь преподобних отців Києво-Печерських у Відні",
        [UOC_AUSTRIA]),
    row("at-uoc-maria-ellend-community", "ukraine-uoc",
        "Ukrainian Orthodox Church Community in Maria Ellend",
        "Громада Української Православної Церкви в місті Марія Елленд",
        [UOC_AUSTRIA], rank="Church Community"),
]


ROWS = {
    "an-germany": ANTIOCH_ROWS,
    "bg-western-central-europe": BULGARIAN_ROWS,
    "ep-austria": EP_ROWS,
    "georgia": GEORGIAN_ROWS,
    "mk-europe": MACEDONIAN_ROWS,
    "ro-germany": ROMANIAN_ROWS,
    "ru-germany-rocor": ROCOR_ROWS,
    "ru-vienna-and-austria": MOSCOW_ROWS,
    "sr-austria-switzerland": SERBIAN_ROWS,
    "ukraine-uoc": UOC_ROWS,
}


EXPECTED = {
    "an-germany": 2,
    "bg-western-central-europe": 2,
    "ep-austria": 19,
    "georgia": 3,
    "mk-europe": 4,
    "ro-germany": 37,
    "ru-germany-rocor": 1,
    "ru-vienna-and-austria": 7,
    "sr-austria-switzerland": 25,
    "ukraine-uoc": 2,
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
    if "\u2013" in serialized or "\u2014" in serialized:
        raise ValueError("%s contains a long dash" % out.get("id"))
    return out


def build():
    payloads = {}
    seen = set(ROWS)
    all_new_ids = {item["id"] for source_rows in ROWS.values()
                   for item in source_rows}
    if len(all_new_ids) != sum(len(items) for items in ROWS.values()):
        raise ValueError("duplicate Austria source row id")
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
                if item.get("country") != "AT":
                    raise ValueError("%s is outside Austria" % row_id)
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
                raise ValueError("Austria child rows have unresolved parents")
        payloads[parent] = {
            "v": 1,
            "parent": parent,
            "country": "AT",
            "rows": rows,
        }
    actual = {parent: len(payload["rows"])
              for parent, payload in payloads.items()}
    if actual != EXPECTED:
        raise ValueError("Austria parent counts changed: %r" % actual)
    if len(ENGLISH_NAMES) != 102:
        raise ValueError("Austria English name coverage changed")
    return payloads


def manifest(payloads=None):
    payloads = payloads or build()
    return {
        parent: {
            "url": "/data/directory/%s.v1.json" % parent,
            "count": len(payload["rows"]),
            "country": "AT",
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
        if parent not in base_ids:
            errors.append("missing directory parent: %s" % parent)
    new_ids = {item["id"] for payload in payloads.values()
               for item in payload["rows"]}
    duplicate_ids = sorted(new_ids & base_ids)
    if duplicate_ids:
        errors.append("Austria row IDs already in directory spine: %s" %
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
        print("directory Austria: %s" % exc, file=sys.stderr)
        return 1
    if errors:
        for error in errors:
            print(error, file=sys.stderr)
        return 1
    if args.dump:
        print(json.dumps(payloads, ensure_ascii=False, indent=2))
        return 0
    print("Austria branches: 102 rows")
    for parent, count in sorted(EXPECTED.items()):
        print("%s: %d" % (parent, count))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
