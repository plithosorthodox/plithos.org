#!/usr/bin/env python3
"""Directory rows for Sweden.

The rows are grouped by parent IDs already present in the directory spine.
Several parents cover other countries, so this module validates and exports
Sweden's contribution without writing shared branch payloads.

    python tools/directory_sweden.py --check
    python tools/directory_sweden.py --dump
"""

import argparse
import json
import sys


CHECKED = "2026-11-14"

EP_SWEDEN = "https://gomos.se/en/about-the-metropolis/parishes/"
EP_CENTRAL = "https://ec-patr.org/entities/iera-mitropoli-soyidias/"
RO_SWEDEN = (
    "https://episcopiascandinavia.se/"
    "parohiile-ortodoxe-romanesti-din-regatul-suediei/"
)
RO_MAP = (
    "https://episcopiascandinavia.se/wp-content/uploads/2026/10/"
    "3.-MOBIL_harta_parohii_Scandinavia_v3.html"
)
RO_MONASTERIES = (
    "https://episcopiascandinavia.se/"
    "manastirile-ortodoxe-romanesti-din-episcopia-ortodoxa-romana-a-europei-de-nord/"
)
RO_CHAPELS = (
    "https://episcopiascandinavia.se/"
    "paraclisele-episcopale-ale-episcopiei-ortodoxe-romane-a-europei-de-nord/"
)
RO_DALARNA = "https://www.dalaortodox.se/om-oss/"
RUSSIA_SWEDEN = "https://sweden.cerkov.ru/prixody/"
RUSSIA_MAP = "https://sweden.cerkov.ru/prihodi/"
BULGARIAN_SWEDEN = "https://bg-patriarshia.bg/west-eu-diocese-temples"
MACEDONIAN_SWEDEN = "https://mpc-oa.se/var-verksamhet/"
MACEDONIAN_MALMO = "https://mpc-oa.se/kontakt-malmo/"
MACEDONIAN_GOTHENBURG = "https://mpc-oa.se/kontakt-goteborg/"
MACEDONIAN_DIOCESE = "https://mpee.mk/category/za-eparxijata"
ANTIOCH_SWEDEN = "https://kristiuppstandelse.se/lankar/"
ANTIOCH_CENTRAL = (
    "https://www.antiochpatriarchate.org/en/page/2580/"
)
SERBIAN_SWEDEN = "https://www.crkva.se/razno/kontakta_oss.htm"
SERBIAN_REPORT = (
    "https://www.mucf.se/sites/default/files/2025/11/"
    "serbisk-ort.2024.master.pdf"
)
SERBIAN_CENTRAL = "https://www.spc.rs/en/96.dioceses-of-the-soc.html"
SERBIAN_STENSTORP = (
    "https://www.spc.rs/sr/news/iz-zivota-crkve/-/15157."
    "molitvena-proslava-svetih-kozme-i-damjana-u-svedskoj.html"
)
SERBIAN_PROTECTION = (
    "https://spc.rs/sr/news/iz-zivota-crkve/18068."
    "slava-manastira-pokrova-presvete-bogorodice-u-svedskoj.html"
)
GEORGIAN_SWEDEN = (
    "https://www.skr.org/medlemskyrkor/den-georgiska-ortodoxa-kyrkan/"
)
GEORGIAN_SAINT_ANNA = "https://heligaanna.nu/om-oss/"
UOC_SWEDEN = (
    "https://uoc-news.church/2026/08/21/"
    "ijerarxi-upc-vidvidali-ukrajinski-parafiji-u-shveciji-norvegiji-ta-ugorshhini/"
)
UOC_STOCKHOLM = "https://www.ukrortodox.com/stockholm"
OCU_SWEDEN = (
    "https://www.rivne-cerkva.rv.ua/news/"
    "5893-ukrainskyi-front-u-krainakh-skandynavii-shvetsiia-norvehiia.html"
)


def row(row_id, parent, name, local, address, sources,
        rank="Parish", kind="parish", site=None):
    value = {
        "id": row_id,
        "parent": parent,
        "kind": kind,
        "rank": rank,
        "name": name,
        "local": local,
        "country": "SE",
        "sources": sources,
    }
    if address:
        value["address"] = address
    if site:
        value["site"] = site
    return value


ROWS = {
    "ep-sweden": [
        row(
            "se-ep-stockholm-saint-george-cathedral", "ep-sweden",
            "Saint George Greek Orthodox Cathedral in Stockholm",
            "St George Greek Orthodox Cathedral",
            ["Birger Jarlsgatan 92", "114 20 Stockholm"],
            [EP_SWEDEN, EP_CENTRAL], rank="Cathedral",
        ),
        row(
            "se-ep-uppsala-saint-paul", "ep-sweden",
            "Saint Paul Greek Orthodox Parish in Uppsala",
            "St Paul Greek Orthodox Parish",
            ["Sysslomansgatan 46", "752 27 Uppsala"], [EP_SWEDEN],
        ),
        row(
            "se-ep-gothenburg-holy-trinity", "ep-sweden",
            "Holy Trinity Greek Orthodox Parish in Gothenburg",
            "Holy Trinity Greek Orthodox Parish",
            ["Sehlstedtsgatan 10", "417 20 Göteborg"], [EP_SWEDEN],
        ),
        row(
            "se-ep-stockholm-saint-nicholas-finnish", "ep-sweden",
            "Saint Nicholas Finnish Orthodox Parish in Stockholm",
            "St Nicholas Finnish Orthodox Parish",
            ["Bellmansgatan 13", "118 47 Stockholm"], [EP_SWEDEN],
            site="https://www.ortodox-finsk.se/",
        ),
        row(
            "se-ep-kalmar-apostle-cleopas", "ep-sweden",
            "Apostle Cleopas Greek Orthodox Parish in Kalmar",
            "Apostle Cleopas Greek Orthodox Parish",
            ["Skogssalen chapel", "Kungsgårdsvägen 2B", "393 37 Kalmar"],
            [EP_SWEDEN],
        ),
        row(
            "se-ep-boras-entry-theotokos", "ep-sweden",
            "Entry of the Theotokos into the Temple Greek Orthodox Parish in Boras",
            "Entry of the Theotokos into the Temple Greek Orthodox Parish",
            ["St Birgitta Griftegård", "Götagatan 14", "504 30 Borås"],
            [EP_SWEDEN],
        ),
        row(
            "se-ep-jonkoping-constantine-helen", "ep-sweden",
            "Saints Constantine and Helen Greek Orthodox Parish in Jonkoping",
            "Sts Constantine and Helen Greek Orthodox Parish",
            ["Erik Dahlbergsgatan 10", "553 37 Jönköping"], [EP_SWEDEN],
        ),
        row(
            "se-ep-malmo-apostle-andrew", "ep-sweden",
            "Apostle Andrew Greek Orthodox Parish in Malmo",
            "Apostle Andrew Greek Orthodox Parish", [], [EP_SWEDEN],
            site="https://greekorthodoxchurchmalmo.com/",
        ),
        row(
            "se-ep-overkalix-transfiguration-mission", "ep-sweden",
            "Transfiguration of Christ Orthodox Missionary Community in Overkalix",
            "Transfiguration of Christ Orthodox Missionary Community",
            ["Knusvägen 10", "956 32 Överkalix"], [EP_SWEDEN],
            rank="Mission",
        ),
        row(
            "se-ep-orebro-demetrios-nestor", "ep-sweden",
            "Saints Demetrios and Nestor Greek Orthodox Parish in Orebro",
            "Sts Demetrios and Nestor Greek Orthodox Parish",
            ["Gode Herden Kapell", "Björkrisvägen 18", "702 34 Örebro"],
            [EP_SWEDEN],
        ),
        row(
            "se-ep-lulea-saint-tychon", "ep-sweden",
            "Saint Tychon Parish in Lulea", "St Tychon Parish",
            ["Hertsökyrkan", "Hertsötorget 16-18", "974 52 Luleå"],
            [EP_SWEDEN],
        ),
        row(
            "se-ep-rattvik-saint-nicholas-hermitage", "ep-sweden",
            "Saint Nicholas Hermitage in Rattvik", "Saint Nicholas Hermitage",
            [], [EP_SWEDEN], rank="Hermitage", kind="monastery",
        ),
    ],
    "ro-northern-europe": [
        row(
            "se-ro-arboga-saint-sven-mission", "ro-northern-europe",
            "Saint Sven the Venerable Martyr Mission in Arboga",
            "Misiunea Sfântul Cuvios Mucenic Sven de la Arboga", [],
            [RO_SWEDEN, RO_MAP], rank="Mission",
        ),
        row(
            "se-ro-birka-saint-nithard-mission", "ro-northern-europe",
            "Saint Nithard and the Saints of Birka Mission",
            "Misiunea Sfântul Cuvios Întâi Sfințit Mucenic Nithard Preotul cu Soborul Sfinților Ierarhi și Mărturisitori, Mucenici și Cuvioși din Birka",
            ["Björkö island", "near Stockholm"], [RO_SWEDEN, RO_MAP],
            rank="Mission",
        ),
        row(
            "se-ro-boden-lady-of-lapland", "ro-northern-europe",
            "Lady of Lapland Icon and Saints Bartholomew, Barnabas, Luke, and the Chinese Martyrs Parish in Boden",
            "Parohia Cinstirea Icoanei Maicii Domnului \"Stăpâna Laponiei\" de la Boden, Sfinții Apostoli Bartolomeu și Barnaba; Sfântul Ierarh Luca, arhiepiscopul Crimeei și Sfinții Mucenici Chinezi de la Beijing",
            ["Johanneskyrka", "Drottninggatan 37", "961 77 Boden"],
            [RO_SWEDEN, RO_MAP],
        ),
        row(
            "se-ro-boras-unfading-flower", "ro-northern-europe",
            "Unfading Flower Icon, Holy Archangels, and Transylvanian Metropolitans Parish in Boras",
            "Parohia Cinstirea Icoanei Maicii Domnului \"Floarea neveștejită\" de la Borås, Soborul Sfinților Arhangheli și Soborul Sfinților Mitropoliți ai Transilvaniei",
            ["Kyrkvägen 2", "517 71 Olsfors"], [RO_SWEDEN, RO_MAP],
        ),
        row(
            "se-ro-eskilstuna-light-of-world", "ro-northern-europe",
            "Light of the World Icon and Saints Athanasius, Esper, Zoe, Cyriacus, Theodulus, and Matrona Parish in Eskilstuna",
            "Parohia Cinstirea Icoanei Maicii Domnului \"Luminătoarea lumii\" de la Eskilstuna, Sfântul Ierarh Atanasie Patelarie de la Dunărea de Jos, Patriarhul Constantinopolului, Sfinții Mucenici Esper și soția sa, Zoe, cu cei doi fii, Chiriac și Teodul, și Sfânta Cuvioasă Matrona de la Moscova",
            ["Åsbyvägen 37", "632 22 Eskilstuna"], [RO_SWEDEN, RO_MAP],
        ),
        row(
            "se-ro-eskilstuna-saint-eskil-filial", "se-ro-eskilstuna-light-of-world",
            "Swedish Filial Parish of Saint Eskil of Tuna in Eskilstuna",
            "Filia suedeză Sfântul Sfințit Mucenic Eskil, Episcop de Tuna",
            ["Saint Anna of Novgorod Church", "Åsbyvägen 37", "632 22 Eskilstuna"],
            [RO_SWEDEN], rank="Filial Parish",
        ),
        row(
            "se-ro-gothenburg-inexhaustible-cup", "ro-northern-europe",
            "Inexhaustible Cup and Nursing Mother Icons, Pentecost, and Moldavian Metropolitans Parish in Gothenburg",
            "Parohia (Paraclis Episcopal) Cinstirea Icoanelor Maicii Domnului \"Potirul Nesecat\" și \"Alăptătoarea de la Țibleș\", Pogorârea Sfântului Duh și Soborul Sfinților Mitropoliți ai Moldovei",
            ["Sankt Matteus kapell", "Sannaplan 3", "Göteborg"],
            [RO_SWEDEN, RO_MAP],
        ),
        row(
            "se-ro-forsbacka-prodromita", "ro-northern-europe",
            "Prodromita and Nursing Mother Icons and Saints Veronica, Euphemia, Paisius, Cleopa, and Paisios Parish in Forsbacka",
            "Parohia Cinstirea Icoanelor Maicii Domnului \"Prodromița\" și \"Alăptătoarea de la Țibleș\", Sfintele Veronica Mironosița și Eufimia Mucenița și Sfinții Cuvioși Paisie și Cleopa de la Sihăstria și Paisie Aghioritul",
            ["Strandgatan 5", "Forsbacka"], [RO_SWEDEN, RO_MAP],
        ),
        row(
            "se-ro-gotland-saint-nicholas-filial", "ro-northern-europe",
            "Saint Nicholas and Saints Botvid and Esbiorn Filial Parish on Gotland",
            "Filia Sfântul Ierarh Nicolae şi Sfinții Mucenici Botvid și Esbiorn de la Hammarby",
            ["Gotland"], [RO_SWEDEN, RO_MAP], rank="Filial Parish",
        ),
        row(
            "se-ro-halmstad-saints-thecla-silouan-sven-filial", "se-ro-gothenburg-inexhaustible-cup",
            "Saints Thecla, Silouan the Athonite, and Sven Filial Parish in Halmstad",
            "Filia Sfânta Muceniță întocmai cu Apostolii Tecla, Sfântul Cuvios Siluan Athonitul și Sfântul Cuvios Mucenic Sven din Arboga",
            ["Halmstad"], [RO_SWEDEN, RO_MAP], rank="Filial Parish",
        ),
        row(
            "se-ro-helsingborg-voice-of-pure-joy", "ro-northern-europe",
            "Voice of Pure Joy Icon and Saint Joseph the New Parish in Helsingborg",
            "Parohia Cinstirea Icoanei Maicii Domnului \"Glasul Curatei Bucurii\" de la Helsingborg și Sfântul Ierarh Iosif cel Nou de la Partoș",
            ["Västra Sönnarslöv 2362", "264 92 Klippan"],
            [RO_SWEDEN, RO_MAP], site="https://www.biserica-ortodoxa-helsingborg.se/",
        ),
        row(
            "se-ro-husaby-saints-olav-astrid-mission", "ro-northern-europe",
            "Saint Olav the Giver and Queen Astrid Mission in Husaby",
            "Misiunea Sfântul Mucenic Olav Dăruitorul, Regele Suediei, și soția sa, Binecredincioasa Astrida Regina",
            ["Husaby"], [RO_SWEDEN, RO_MAP], rank="Mission",
        ),
        row(
            "se-ro-jonkoping-protectress-of-orphans", "ro-northern-europe",
            "Protectress of Orphans Icon, Protection of the Mother of God, and Saints Daniel and Paisius Parish in Jonkoping",
            "Parohia Cinstirea Icoanei Maicii Domnului \"Ocrotitoarea orfanilor\" de la Jönköping, Acoperământul Maicii Domnului și Sfinții Cuvioși Daniil Sihastrul și Paisie de la Neamț",
            ["Ceciliakyrka", "Ebba Ramsays väg 20", "Jönköping"],
            [RO_SWEDEN, RO_MAP], site="https://www.bisericajonkoping.se/",
        ),
        row(
            "se-ro-nybro-saved-from-drowning", "ro-northern-europe",
            "Saved from Drowning Icon and Saints Charalambos, Valentina, Anna, Yaroslav, and Vladimir Parish in Nybro and Kalmar",
            "Parohia Cinstirea Icoanei Maicii Domnului \"Salvatoarea de la înec\" de la Kalmar, Sfântul Sfințit Mucenic Haralambie şi Sfânta Muceniță Valentina din Cezareea și Sfânta Cuvioasă Ana Vikinga, Cneaghina de la Novgorod, cu soțul Sfântul Cneaz Iaroslav cel Înțelept și fiul, Sfântul Cneaz Vladimir",
            ["Kvarneslättsgatan", "Nybro"], [RO_SWEDEN, RO_MAP],
        ),
        row(
            "se-ro-kinna-saint-matthew-filial", "se-ro-boras-unfading-flower",
            "Saint Matthew the Apostle and Evangelist Filial Parish in Kinna",
            "Filia Sfântul Apostol și Evanghelist Matei", ["Kinna"],
            [RO_SWEDEN, RO_MAP], rank="Filial Parish",
        ),
        row(
            "se-ro-kiruna-saints-barbara-john-alexander-mission", "ro-northern-europe",
            "Saints Barbara, John of Damascus, and Alexander Hotovitsky Mission in Kiruna",
            "Misiunea Sfânta Mare Muceniță Varvara, Sfântul Cuvios Ioan Damaschin și Sfântul Neomartir Alexandru Hotovitski Preotul din Helsinki",
            ["Kiruna"], [RO_SWEDEN, RO_MAP], rank="Mission",
        ),
        row(
            "se-ro-solvesborg-nursing-mother", "ro-northern-europe",
            "Nursing Mother Icon and the Nasăud Martyrs Parish in Solvesborg",
            "Parohia Cinstirea Icoanei Maicii Domnului \"Hrănitoarea cu lapte\" de la Sölvesborg și Sfinții Martiri Năsăudeni: Atanasie din Bichigiu, Vasile din Mocod, Grigore din Zagra și Vasile din Telciu",
            ["Bancks Väg 4", "294 35 Sölvesborg"], [RO_SWEDEN, RO_MAP],
            site="https://www.bisericasolvesborg.se/",
        ),
        row(
            "se-ro-stockholm-saint-george", "ro-northern-europe",
            "Saint George the Great Martyr Parish in Stockholm",
            "Parohia Sfântul Mare Mucenic Gheorghe",
            ["Matteus Kyrka", "Vanadisvägen 35", "Stockholm"],
            [RO_SWEDEN, RO_MAP], site="https://www.borss.se/",
        ),
        row(
            "se-ro-kristianstad-saint-demetrius-filial", "se-ro-solvesborg-nursing-mother",
            "Saint Demetrius the Myrrh-Streamer Filial Parish in Kristianstad",
            "Filia Sfântul Mare Mucenic Dimitrie, Izvorâtorul de mir",
            ["Kristianstad"], [RO_SWEDEN, RO_MAP], rank="Filial Parish",
        ),
        row(
            "se-ro-leksand-peter-paul", "ro-northern-europe",
            "Holy Apostles Peter and Paul Swedish Orthodox Parish in Leksand",
            "Parohia Ortodoxă Suedeză Sfinții Apostoli Petru și Pavel",
            ["Östra Rönnäs Jofsvägen 4", "793 91 Leksand"],
            [RO_SWEDEN, RO_DALARNA], site="https://www.dalaortodox.se/",
        ),
        row(
            "se-ro-linkoping-saint-lazarus-filial", "se-ro-stockholm-saint-george",
            "Saint Lazarus Filial Parish in Linkoping",
            "Filia Sfântul și Dreptul Lazăr",
            ["Bankekind or Örtomta", "Askeby kyrka", "Linköping"],
            [RO_SWEDEN, RO_MAP], rank="Filial Parish",
        ),
        row(
            "se-ro-lulea-saints-pachomius-jacob-putna-mission", "ro-northern-europe",
            "Saints Pachomius, Jacob of Putna, Sila, Paisius, and Nathan Mission in Lulea",
            "Misiunea Sfântul Cuvios Pahomie cel Mare, Sfântul Ierarh Iacob Putneanul și Sfinții Cuvioși Sila, Paisie și Natan de la Sihăstria Putnei",
            ["Luleå"], [RO_SWEDEN, RO_MAP], rank="Mission",
        ),
        row(
            "se-ro-lund-guide-of-youth", "ro-northern-europe",
            "Guide of Youth and Nursing Mother Icons and Saints Stephen and Lawrence Parish in Lund",
            "Parohia Cinstirea Icoanelor Maicii Domnului \"Povățuitoarea tinerilor\" și \"Alăptătoarea de la Țibleș\", Sfinţii Mucenici și Arhidiaconi Ștefan și Laurențiu",
            ["Hardeberga Kyrka 404", "247 91 Södra Sandby"],
            [RO_SWEDEN, RO_MAP],
        ),
        row(
            "se-ro-malmo-pentecost", "ro-northern-europe",
            "Pentecost Parish in Malmo", "Parohia Pogorârea Sfântului Duh",
            ["Vanåsgatan 66", "216 20 Malmö"], [RO_SWEDEN, RO_MAP],
        ),
        row(
            "se-ro-munktorp-saint-david-mission", "ro-northern-europe",
            "Saint David the Confessor Mission in Munktorp",
            "Misiunea Sfântul Cuvios David Mărturisitorul din Muktorp",
            ["Munktorp"], [RO_SWEDEN, RO_MAP], rank="Mission",
        ),
        row(
            "se-ro-orebro-saints-theodore-filial", "se-ro-stockholm-saint-george",
            "Saints Theodore Stratelates and Theodore the Recruit Filial Parish in Orebro",
            "Filia Sfinții Mari Mucenici Teodor Stratilat și Teodor Tiron",
            ["Gode Herdens Kapell", "Björkrisvägen 18", "Örebro"],
            [RO_SWEDEN, RO_MAP], rank="Filial Parish",
        ),
        row(
            "se-ro-skara-saints-odinkar-adalvard-stephen-mission", "ro-northern-europe",
            "Saints Odinkar, Adalvard, and Stephen of Norrala Mission in Skara",
            "Misiunea Sfinții Ierarhi Odincar cel Bătrân și Adalvard cel Bătrân, Episcopi de Skara şi Sfântul Sfințitul Mucenic Ștefan Episcopul de la Norrala",
            ["Skara"], [RO_SWEDEN, RO_MAP], rank="Mission",
        ),
        row(
            "se-ro-huddinge-dormition", "ro-northern-europe",
            "Dormition and In Giving Birth You Preserved Virginity Icon Parish in Huddinge",
            "Parohia Adormirea Maicii Domnului şi Cinstirea Icoanei Maicii Domnului \"Întru naștere Fecioria ai păzit\" de la Stockholm",
            ["Flemingsbergs kyrka", "Diagnosvägen 14-16", "Huddinge"],
            [RO_SWEDEN, RO_MAP],
        ),
        row(
            "se-ro-tungelsta-holy-trinity", "ro-northern-europe",
            "Holy Trinity, Saint John the Baptist, and Saint John Maximovitch Parish in Tungelsta",
            "Parohia Sfânta Treime, Sfântul Proroc Ioan Botezătorul și Sfântul Ierarh Ioan Maximovici",
            ["Kvarnvägen 30", "Tungelsta"], [RO_SWEDEN, RO_MAP],
        ),
        row(
            "se-ro-sundsvall-saint-signilda-mission", "ro-northern-europe",
            "Saint Signilda of the Aland Islands Mission in Sundsvall",
            "Misiunea Sfânta Cuvioasă Signilda de pe Insulele Alandia, în Golful Botnic",
            ["Sundsvall"], [RO_SWEDEN, RO_MAP], rank="Mission",
        ),
        row(
            "se-ro-trollhattan-saint-nectarios", "ro-northern-europe",
            "Saint Nectarios of Aegina Parish in Trollhattan",
            "Parohia Sfântul Ierarh Nectarie de la Eghina",
            ["Trollhättan"], [RO_SWEDEN, RO_MAP],
        ),
        row(
            "se-ro-ulricehamn-saint-bartholomew-mission", "ro-northern-europe",
            "Saint Bartholomew the Priest Martyr Mission in Ulricehamn",
            "Misiunea Sfântul Sfințitul Mucenic Bartolomeu (Berthil) Preotul de la Ulricehamn",
            ["Ulricehamn"], [RO_SWEDEN, RO_MAP], rank="Mission",
        ),
        row(
            "se-ro-umea-saints-niphon-athanasius-mission", "ro-northern-europe",
            "Saints Niphon and Athanasius III Mission in Umea",
            "Misiunea Sfinții Ierarhi Nifon şi Atanasie al III-lea Patelarie de la Dunărea de Jos, Patriarhii Constantinopolului",
            ["Umeå"], [RO_SWEDEN, RO_MAP], rank="Mission",
        ),
        row(
            "se-ro-uppsala-guide-of-children", "ro-northern-europe",
            "Guide of Children Icon, Three Holy Hierarchs, and Romanian Metropolitans Parish in Uppsala",
            "Parohia Cinstirea Icoanei Maicii Domnului \"Povățuitoarea copiilor\" de la Uppsala, Sfinții Trei Ierarhi: Vasile, Grigorie și Ioan şi Sfinții Ierarhi Iachint de Vicina, Antim Ivireanul şi Grigorie Dascălul cu Soborul Sfinților Mitropoliți ai Țării Românești",
            ["Ulleråkersvägen 40A", "Uppsala"], [RO_SWEDEN, RO_MAP],
            site="https://ortodoxuppsala.se/parohia-romaneasca/",
        ),
        row(
            "se-ro-uppsala-ulfrid-eric-filial", "se-ro-uppsala-guide-of-children",
            "Swedish Orthodox Filial Parish of Saints Ulfrid and Eric in Uppsala",
            "Filia Ortodoxă Suedeză Sfinții Mucenici Ulfrid și Eric Pelerinul de la Uppsala",
            ["Uppsala"], [RO_SWEDEN], rank="Filial Parish",
        ),
        row(
            "se-ro-vasteras-constantine-helen", "ro-northern-europe",
            "Saints Constantine and Helen Parish in Vasteras",
            "Parohia Sfinții Împărați Constantin și mama sa Elena",
            ["Meditationsrummet på Kyrkbackgården", "Västerås"],
            [RO_SWEDEN, RO_MAP],
        ),
        row(
            "se-ro-vastervik-basil-leontius-filial", "se-ro-nybro-saved-from-drowning",
            "Saints Basil the Great and Leontius Filial Parish in Vastervik",
            "Filia Sfinții Ierarhi Vasile cel Mare şi Leontie de la Rădăuți",
            ["Västervik"], [RO_SWEDEN, RO_MAP], rank="Filial Parish",
        ),
        row(
            "se-ro-varnamo-daniel-three-youths-filial", "se-ro-jonkoping-protectress-of-orphans",
            "Prophet Daniel and the Three Holy Youths Filial Parish in Varnamo",
            "Filia Sfântul Proroc Daniel și Sfinții trei tineri: Anania, Azaria și Misail",
            ["Träffgatan 1", "331 53 Värnamo"], [RO_SWEDEN, RO_MAP],
            rank="Filial Parish",
        ),
        row(
            "se-ro-vaxjo-full-of-grace", "ro-northern-europe",
            "Full of Grace and Nursing Mother Icons, Exaltation of the Cross, and Saints Joseph and Sigfrid Parish in Vaxjo",
            "Parohia Cinstirea Icoanelor Maicii Domnului \"Cea cu Har dăruită\" de la Växjö și \"Alăptătoarea de la Țibleș\", Înălțarea Sfintei Cruci şi Sfinții Ierarhi Mărturisitori Iosif din Maramureș şi Sigfrid de Växjö, cu Sfinții Unaman, Sunaman și Vinaman",
            ["Västrabokyrkan", "Arabygatan 44", "352 36 Växjö"],
            [RO_SWEDEN, RO_MAP], site="https://www.parohiavaxjo.se/",
        ),
        row(
            "se-ro-haninge-saint-andrew-monastery", "ro-northern-europe",
            "Saint Andrew and All Romanian Voivode Saints Monastery in Haninge",
            "Mănăstirea Sfântul Apostol Andrei şi Toți Sfinții Voievozi Români",
            ["Hässlingbyvägen 7", "136 91 Haninge"],
            [RO_MONASTERIES, RO_MAP], rank="Monastery", kind="monastery",
        ),
        row(
            "se-ro-forsbacka-nursing-mother-monastery", "ro-northern-europe",
            "Nursing Mother Icon and Saints Paisius and Cleopa Monastery in Forsbacka",
            "Mănăstirea Cinstirea Icoanei Maicii Domnului \"Alăptătoarea de la Țibleș\" și Sfinții Cuvioși Paisie și Cleopa de la Sihăstria",
            ["Strandgatan 5", "Forsbacka"], [RO_MONASTERIES, RO_MAP],
            rank="Monastery", kind="monastery",
        ),
        row(
            "se-ro-uppsala-ulfrid-eric-cell", "ro-northern-europe",
            "Saints Ulfrid and Eric Monastic Cell in Uppsala",
            "Chilia Sfinții Mucenici Ulfrid și Eric Pelerinul de la Uppsala",
            ["Uppsala"], [RO_MONASTERIES, RO_MAP], rank="Monastic Cell",
            kind="monastery",
        ),
        row(
            "se-ro-haninge-saint-mina-episcopal-chapel", "ro-northern-europe",
            "Saint Mina and Romanian Saints Episcopal Chapel in Haninge",
            "Paraclisul episcopal Sfântul Mare Mucenic Mina, Cinstirea Icoanei Maicii Domnului \"Eu sunt cu voi și nimeni împotriva voastră\", Cinstirea Icoanei Maicii Domnului pe tron, Sfântul Apostol Andrei, Toți Sfinții Voievozi Români și Sfinții Cuvioși Macarie cel Mare și Macarie Alexandrinul",
            ["Hässlingbyvägen 7", "137 95 Österhaninge"],
            [RO_CHAPELS], rank="Episcopal Chapel",
        ),
    ],
    "russia": [
        row(
            "se-ru-stockholm-saint-sergius", "russia",
            "Saint Sergius of Radonezh Parish in Stockholm",
            "Сергиевский приход в Стокгольме",
            ["Alvastravägen 8", "126 50 Hägersten"],
            [RUSSIA_SWEDEN, RUSSIA_MAP],
        ),
        row(
            "se-ru-vasteras-kazan-icon", "russia",
            "Kazan Icon of the Mother of God Parish in Vasteras",
            "Приход во имя Казанской иконы Божией Матери в Вестеросе",
            ["Atmosfärvägen 8", "721 31 Västerås"],
            [RUSSIA_SWEDEN, RUSSIA_MAP],
        ),
        row(
            "se-ru-gothenburg-protection", "russia",
            "Protection of the Mother of God Parish in Gothenburg",
            "Приход во имя Покрова Божией Матери в Гётеборге",
            ["Runstavsgatan 9", "Göteborg"], [RUSSIA_SWEDEN, RUSSIA_MAP],
        ),
        row(
            "se-ru-karlstad-look-down-with-mercy", "russia",
            "Look Down with Mercy Icon of the Mother of God Parish in Karlstad",
            "Приход в честь иконы Божией Матери \"Призри на смирение\" в Карлстаде",
            ["Drottninggatan 31", "Karlstad"], [RUSSIA_SWEDEN, RUSSIA_MAP],
        ),
        row(
            "se-ru-lulea-unexpected-joy", "russia",
            "Unexpected Joy Icon of the Mother of God Parish in Lulea",
            "Приход в честь иконы Божией Матери \"Нечаянная радость\" в Лулео",
            ["Professorsvägen 9", "Luleå"], [RUSSIA_SWEDEN, RUSSIA_MAP],
        ),
        row(
            "se-ru-umea-peter-paul", "russia",
            "Holy Apostles Peter and Paul Parish in Umea",
            "Приход в честь святых первоверховных апостолов Петра и Павла в Умео",
            ["Olle Fiskares väg 10", "Umeå"], [RUSSIA_SWEDEN, RUSSIA_MAP],
        ),
        row(
            "se-ru-uppsala-saint-nicholas", "russia",
            "Saint Nicholas Parish in Uppsala",
            "Приход во имя святителя Николая Чудотворца в Уппсале", [],
            [RUSSIA_SWEDEN, RUSSIA_MAP],
        ),
        row(
            "se-ru-gavle-dormition", "russia",
            "Dormition of the Mother of God Parish in Gavle",
            "Приход Успения Божией Матери в Евле", [],
            [RUSSIA_SWEDEN, RUSSIA_MAP],
        ),
        row(
            "se-ru-jonkoping-archangel-michael", "russia",
            "Archangel Michael Parish in Jonkoping",
            "Приход Архистратига Божия Михаила в Йенчепинге",
            ["Klostergatan 70B", "Jönköping"], [RUSSIA_SWEDEN, RUSSIA_MAP],
        ),
        row(
            "se-ru-helsingborg-resurrection", "russia",
            "Resurrection of Christ Parish in Helsingborg",
            "Приход Воскресения Христова в Хельсингборге",
            ["Nedre Eneborgsvägen", "252 68 Helsingborg"],
            [RUSSIA_SWEDEN, RUSSIA_MAP],
        ),
    ],
    "bg-western-central-europe": [
        row(
            "se-bg-stockholm-saint-paisius", "bg-western-central-europe",
            "Saint Paisius of Hilendar Bulgarian Orthodox Church Community in Stockholm",
            "БПЦО \"Св. Паисий Хилендарски\" - гр. Стокхолм",
            ["Birger Jarlsgatan 98", "Stockholm"], [BULGARIAN_SWEDEN],
            rank="Church Community",
        ),
        row(
            "se-bg-malmo-theotokos", "bg-western-central-europe",
            "Mother of God Bulgarian Orthodox Church Community in Malmo",
            "БПЦО \"Св. Богородица\" - гр. Малмьо", [], [BULGARIAN_SWEDEN],
            rank="Church Community",
        ),
        row(
            "se-bg-gothenburg-saint-demetrius", "bg-western-central-europe",
            "Saint Demetrius Bulgarian Orthodox Church Community in Gothenburg",
            "БПЦО \"Св. Димитър\" - гр. Гьотеборг", [], [BULGARIAN_SWEDEN],
            rank="Church Community",
        ),
    ],
    "mk-europe": [
        row(
            "se-mk-malmo-saint-naum", "mk-europe",
            "Saint Naum of Ohrid Macedonian Orthodox Parish in Malmo",
            "Makedonska Ortodoxa Kyrkoförsamlingen Sv. Naum Ohridski",
            ["Danska Vägen 30", "212 29 Malmö"],
            [MACEDONIAN_SWEDEN, MACEDONIAN_MALMO, MACEDONIAN_DIOCESE],
            site=MACEDONIAN_MALMO,
        ),
        row(
            "se-mk-gothenburg-cyril-methodius", "mk-europe",
            "Saints Cyril and Methodius Macedonian Orthodox Parish in Gothenburg",
            "Makedonska Ortodoxa Kyrkoförsamlingen Sv. Kiril i Metodij",
            ["Atmosfärgatan 2", "415 61 Göteborg"],
            [MACEDONIAN_SWEDEN, MACEDONIAN_GOTHENBURG, MACEDONIAN_DIOCESE],
            site=MACEDONIAN_GOTHENBURG,
        ),
    ],
    "antioch": [
        row(
            "se-antioch-sodertalje-annunciation-cathedral", "antioch",
            "Annunciation of the Mother of God Cathedral Parish in Sodertalje",
            "Jungfru Marie Bebådelses ortodoxa församling",
            ["Nyköpingsvägen 20", "151 32 Södertälje"],
            [ANTIOCH_SWEDEN, ANTIOCH_CENTRAL], rank="Cathedral Parish",
        ),
        row(
            "se-antioch-upplands-vasby-john-damascus", "antioch",
            "Saint John of Damascus Parish in Upplands Vasby",
            "Helige Johannes av Damaskus", ["Upplands Väsby"],
            [ANTIOCH_SWEDEN, ANTIOCH_CENTRAL],
        ),
        row(
            "se-antioch-norrkoping-saint-george", "antioch",
            "Saint George Parish in Norrkoping", "Helige Georgios i Norrköping",
            ["Borgs kyrka", "605 97 Norrköping"],
            [ANTIOCH_SWEDEN, ANTIOCH_CENTRAL],
        ),
        row(
            "se-antioch-motala-saint-nicholas", "antioch",
            "Saint Nicholas Parish in Motala", "Helige Nikolaos i Motala",
            ["Motala"], [ANTIOCH_SWEDEN, ANTIOCH_CENTRAL],
        ),
        row(
            "se-antioch-orebro-saint-basil", "antioch",
            "Saint Basil Parish in Orebro", "Helige Basileios i Örebro",
            ["Sturegatan 9", "Örebro"], [ANTIOCH_SWEDEN, ANTIOCH_CENTRAL],
        ),
        row(
            "se-antioch-eskilstuna-saint-demetrius", "antioch",
            "Saint Demetrius Parish in Eskilstuna", "Helige Demetrios i Eskilstuna",
            ["Eskilstuna"], [ANTIOCH_SWEDEN, ANTIOCH_CENTRAL],
        ),
        row(
            "se-antioch-nykoping-resurrection", "antioch",
            "Resurrection of Christ Parish in Nykoping", "Kristi Uppståndelse i Nyköping",
            ["Nyköping"], [ANTIOCH_SWEDEN, ANTIOCH_CENTRAL],
        ),
        row(
            "se-antioch-gavle-prophet-elijah", "antioch",
            "Prophet Elijah Parish in Gavle", "Helige Profeten Elias i Gävle",
            ["Forellplan 3", "806 31 Gävle"], [ANTIOCH_SWEDEN, ANTIOCH_CENTRAL],
        ),
        row(
            "se-antioch-trollhattan-peter-paul", "antioch",
            "Saints Peter and Paul Parish in Trollhattan",
            "Helige Petrus och Paulus i Trollhättan", ["Trollhättan"],
            [ANTIOCH_SWEDEN, ANTIOCH_CENTRAL],
        ),
        row(
            "se-antioch-jonkoping-andrew-crete", "antioch",
            "Saint Andrew of Crete Parish in Jonkoping",
            "Helige Andreas av Kreta i Jönköping", ["Jönköping"],
            [ANTIOCH_SWEDEN, ANTIOCH_CENTRAL],
        ),
        row(
            "se-antioch-gothenburg-saint-demetrius", "antioch",
            "Saint Demetrius Parish in Gothenburg", "Helige Dimitrios i Göteborg",
            ["Göteborg"], [ANTIOCH_SWEDEN, ANTIOCH_CENTRAL],
        ),
        row(
            "se-antioch-gothenburg-resurrection", "antioch",
            "Resurrection of Christ Parish in Gothenburg",
            "Kristi Uppståndelses Ortodoxa församling",
            ["Sankt Matteus kapell and Sveti Stefan Dečanski", "Göteborg"],
            [ANTIOCH_SWEDEN, ANTIOCH_CENTRAL], site="https://kristiuppstandelse.se/",
        ),
        row(
            "se-antioch-uddevalla-theophany", "antioch",
            "Holy Theophany Parish in Uddevalla", "Heliga Teofania i Uddevalla",
            ["Vargstigen 3", "451 54 Uddevalla"],
            [ANTIOCH_SWEDEN, ANTIOCH_CENTRAL],
        ),
        row(
            "se-antioch-hammaro-saint-olav", "antioch",
            "Saint Olav Parish in Hammaro and Karlstad",
            "Helige Olavs Ortodoxa Församling",
            ["Bärstavägen 1", "663 41 Hammarö"],
            [ANTIOCH_SWEDEN, ANTIOCH_CENTRAL], site="https://www.heligeolav.se/",
        ),
    ],
    "sr-scandinavia": [
        row(
            "se-sr-stockholm-saint-sava", "sr-scandinavia",
            "Saint Sava Serbian Orthodox Parish in Stockholm",
            "Parohija Svetog Save u Stokholmu",
            ["Bägerstavägen 68", "120 47 Enskede Gård"],
            [SERBIAN_SWEDEN, SERBIAN_REPORT, SERBIAN_CENTRAL],
        ),
        row(
            "se-sr-malmo-cyril-methodius", "sr-scandinavia",
            "Saints Cyril and Methodius Serbian Orthodox Parish in Malmo",
            "Kyrkoförsamlingen S:t Cyril och Methodius i Malmö",
            ["Cedergatan 4", "215 67 Malmö"],
            [SERBIAN_SWEDEN, SERBIAN_REPORT], site="https://www.crkva.se/",
        ),
        row(
            "se-sr-vasteras-saint-nicholas", "sr-scandinavia",
            "Saint Nicholas Serbian Orthodox Parish in Vasteras",
            "Helige Nikolaus församling i Västerås", [],
            [SERBIAN_SWEDEN, SERBIAN_REPORT],
        ),
        row(
            "se-sr-olofstrom-saint-george-monastery", "sr-scandinavia",
            "Saint George Monastery in Olofstrom",
            "Manastir Svetog Georgija u Olofstromu",
            ["Järnvägsgatan 34", "293 39 Olofström"],
            [SERBIAN_SWEDEN, SERBIAN_REPORT, SERBIAN_CENTRAL],
            rank="Monastery", kind="monastery",
        ),
        row(
            "se-sr-jonkoping-nativity-theotokos", "sr-scandinavia",
            "Nativity of the Mother of God Serbian Orthodox Parish in Jonkoping",
            "Parohija Rođenja Presvete Bogorodice u Jenćepingu",
            ["Lagastigen 24", "567 92 Vaggeryd"],
            [SERBIAN_SWEDEN, SERBIAN_REPORT, SERBIAN_STENSTORP],
        ),
        row(
            "se-sr-stenstorp-cosmas-damian-church", "se-sr-jonkoping-nativity-theotokos",
            "Saints Cosmas and Damian Church in Stenstorp",
            "Црква Светих бесребреника Козме и Дамјана у Стенсторпу",
            ["Edelfeldtsgatan 16", "521 60 Stenstorp", "Falköping"],
            [SERBIAN_STENSTORP], rank="Church",
        ),
        row(
            "se-sr-gothenburg-stephen-decani", "sr-scandinavia",
            "Saint Stephen of Decani Serbian Orthodox Parish in Gothenburg",
            "Helige Stefan Dečanski församling i Göteborg",
            ["Runstavsgatan 9", "415 08 Göteborg"],
            [SERBIAN_SWEDEN, SERBIAN_REPORT],
        ),
        row(
            "se-sr-helsingborg-saint-basil", "sr-scandinavia",
            "Saint Basil the Great Serbian Orthodox Parish in Helsingborg",
            "Helige Basileios den Store församling i Helsingborg",
            ["Nedre Eneborgsvägen 7", "252 68 Helsingborg"],
            [SERBIAN_SWEDEN, SERBIAN_REPORT],
        ),
        row(
            "se-sr-halmstad-saint-paraskeva", "sr-scandinavia",
            "Saint Paraskeva Serbian Orthodox Parish in Halmstad",
            "Heliga moder Paraskeva församling i Halmstad",
            ["Forellvägen 1", "302 61 Halmstad"],
            [SERBIAN_SWEDEN, SERBIAN_REPORT], site="https://www.svetapetka.se/",
        ),
        row(
            "se-sr-kristianstad-saint-demetrius", "sr-scandinavia",
            "Saint Demetrius of Thessaloniki Serbian Orthodox Parish in Kristianstad",
            "Heliga Demetrios av Thessaloniki församling",
            ["Allegatan 18", "291 05 Kristianstad"],
            [SERBIAN_SWEDEN, SERBIAN_REPORT],
        ),
        row(
            "se-sr-bredared-mary-magdalene", "sr-scandinavia",
            "Saint Mary Magdalene Serbian Orthodox Parish for Western Sweden",
            "Heliga Maria Magdalena församling för västra Sverige",
            ["Ingelstorp Liderna 1", "504 96 Bredared"],
            [SERBIAN_SWEDEN, SERBIAN_REPORT],
        ),
        row(
            "se-sr-bredared-holy-trinity-monastery", "sr-scandinavia",
            "Holy Trinity Monastery in Bredared", "Heliga Treenighetens kloster",
            ["Ingelstorp Liderna 1", "504 96 Bredared"],
            [SERBIAN_SWEDEN, SERBIAN_REPORT], rank="Monastery", kind="monastery",
        ),
        row(
            "se-sr-vaxtorp-protection-monastery", "sr-scandinavia",
            "Protection of the Mother of God Monastery in Vaxtorp",
            "Манастир Покрова Пресвете Богородице у Шведској",
            ["Smedjeryd 415", "312 98 Våxtorp"],
            [SERBIAN_SWEDEN, SERBIAN_REPORT, SERBIAN_PROTECTION],
            rank="Monastery", kind="monastery",
        ),
    ],
    "georgia": [
        row(
            "se-ge-stockholm-saint-george", "georgia",
            "Saint George Georgian Orthodox Parish in Stockholm",
            "Helige Giorgis Georgisk-Ortodoxa församling",
            ["Kyrkvägen 27", "Stocksund"], [GEORGIAN_SWEDEN],
        ),
        row(
            "se-ge-stockholm-saint-anna-novgorod", "georgia",
            "Saint Anna of Novgorod Orthodox Parish in Stockholm",
            "Heliga Anna av Novgorods ortodoxa församling",
            ["Kyrkvägen 27", "Stocksund"],
            [GEORGIAN_SWEDEN, GEORGIAN_SAINT_ANNA], site="https://heligaanna.nu/",
        ),
    ],
    "ukraine-uoc": [
        row(
            "se-uoc-stockholm-pochaiv-icon", "ukraine-uoc",
            "Parish of the Pochaiv Icon of the Most Holy Theotokos in Stockholm",
            "Парафія на честь Почаївської ікони Пресвятої Богородиці у Стокгольмі",
            ["Nynäsvägen 3C", "136 47 Haninge"],
            [UOC_SWEDEN, UOC_STOCKHOLM],
            site=UOC_STOCKHOLM,
        ),
        row(
            "se-uoc-gothenburg-parish", "ukraine-uoc",
            "Ukrainian Orthodox Church Parish in Gothenburg",
            "Парафія Української Православної Церкви у Гетеборзі",
            ["Göteborg"], [UOC_SWEDEN],
        ),
    ],
    "ukraine-ocu": [
        row(
            "se-ocu-stockholm-faith-hope-love-sophia", "ukraine-ocu",
            "Ukrainian Orthodox Parish of Martyrs Faith, Hope, Love, and Sophia in Stockholm",
            "Українська Православна Громада святих мучениць Віри, Надії, Любові та матері їх Софії в Стокгольмі",
            ["Stockholm"], [OCU_SWEDEN], rank="Community",
        ),
    ],
}


ENGLISH_NAMES = {
    item["id"]: item["name"]
    for source_rows in ROWS.values()
    for item in source_rows
}


EXPECTED = {
    "antioch": 14,
    "bg-western-central-europe": 3,
    "ep-sweden": 12,
    "georgia": 2,
    "mk-europe": 2,
    "ro-northern-europe": 43,
    "russia": 10,
    "sr-scandinavia": 13,
    "ukraine-ocu": 1,
    "ukraine-uoc": 2,
}


DIRECT_RUSSIA_ROWS = ROWS["russia"]


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
    if out.get("address") and (not isinstance(out["address"], list) or
                               not all(isinstance(line, str)
                                       for line in out["address"])):
        raise ValueError("%s has an invalid address" % out.get("id"))
    return out


def build():
    payloads = {}
    seen = set(ROWS)
    allowed_kinds = {"parish", "monastery"}
    for parent, source_rows in ROWS.items():
        rows = []
        branch_seen = {parent}
        for source in source_rows:
            item = clean(source)
            row_id = item.get("id")
            if not row_id or row_id in seen:
                raise ValueError("duplicate or missing id: %s" % row_id)
            if item.get("parent") not in branch_seen:
                raise ValueError("%s hangs off an unknown branch parent: %s" %
                                 (row_id, item.get("parent")))
            if item.get("kind") not in allowed_kinds:
                raise ValueError("%s has unsupported kind: %s" %
                                 (row_id, item.get("kind")))
            if item.get("country") != "SE":
                raise ValueError("%s is outside Sweden" % row_id)
            if not item.get("name") or not item.get("local"):
                raise ValueError("%s lacks a name" % row_id)
            if item.get("site") and not item["site"].startswith("http"):
                raise ValueError("%s carries a non-URL site" % row_id)
            if "\u2013" in json.dumps(item, ensure_ascii=False) or \
                    "\u2014" in json.dumps(item, ensure_ascii=False):
                raise ValueError("%s contains a long dash" % row_id)
            seen.add(row_id)
            branch_seen.add(row_id)
            rows.append(item)
        payloads[parent] = {
            "v": 1,
            "parent": parent,
            "country": "SE",
            "rows": rows,
        }
    actual = {parent: len(payload["rows"])
              for parent, payload in payloads.items()}
    if actual != EXPECTED:
        raise ValueError("Sweden parent counts changed: %r" % actual)
    row_ids = {item["id"] for source_rows in ROWS.values()
               for item in source_rows}
    if set(ENGLISH_NAMES) != row_ids or len(ENGLISH_NAMES) != 102:
        raise ValueError("Sweden English name coverage changed")
    return payloads


def manifest(payloads=None):
    payloads = payloads or build()
    return {
        parent: {
            "url": "/data/directory/%s.v1.json" % parent,
            "count": len(payload["rows"]),
            "countries": ["SE"],
        }
        for parent, payload in sorted(payloads.items())
    }


def main():
    parser = argparse.ArgumentParser()
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument("--check", action="store_true")
    mode.add_argument("--dump", action="store_true")
    args = parser.parse_args()
    try:
        payloads = build()
    except (OSError, ValueError) as exc:
        print("directory Sweden: %s" % exc, file=sys.stderr)
        return 1
    if args.dump:
        print(json.dumps(payloads, ensure_ascii=False, indent=2))
        return 0
    print("Sweden branches: 102 rows")
    for parent, entry in manifest(payloads).items():
        print("%s: %d" % (parent, entry["count"]))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
