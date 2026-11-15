#!/usr/bin/env python3
"""The parish-scale Estonia branches of the Churches directory."""

import argparse
import json
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "data" / "directory"
CHECKED = "2026-11-14"
EAOK = "https://www.eoc.ee/"
EOKK = "https://et.orthodox.ee/parishes/"
ESTONIA_CHURCH_STRUCTURE = (
    "https://www.siseministeerium.ee/en/declaring-moscow-patriarchate-"
    "institution-supporting-military-aggression"
)


ENGLISH_NAMES = {
    "ee-eaok-priipalu-puha-vassili-suure-kirik": "Parish of Saint Basil the Great in Priipalu",
    "ee-eaok-vandra-apostlite-peetruse-pauluse-kogudus": "Parish of the Holy Apostles Peter and Paul in Vändra",
    "ee-eaok-velise-ristija-johannese-kogudus": "Parish of Saint John the Baptist in Velise",
    "ee-eaok-valga-issidori-peakirik": "Cathedral of Saint Isidore in Valga",
    "ee-eaok-uduvere-apostel-jaakobuse-kogudus": "Parish of the Apostle James in Uduvere",
    "ee-eaok-tallinn-puha-georgi": "Parish of Saint George in Tallinn",
    "ee-eaok-puutli-puha-nikolai-kirik": "Parish of Saint Nicholas in Puutli",
    "ee-eaok-paldiski-puha-georgi-kogudus": "Parish of Saint George in Paldiski",
    "ee-eaok-meeksi-ristija-johannese-kogudus": "Parish of Saint John the Baptist in Miikse",
    "ee-eaok-luhamaa-puhavaimu": "Parish of the Holy Spirit in Luhamaa",
    "ee-eaok-lelle-puha-kolmainu-kogudus": "Auxiliary Parish of the Holy Trinity in Lelle",
    "ee-eaok-laatre-puhavaimu-kirik": "Parish of the Holy Spirit in Laatre",
    "ee-eaok-laanemetsa-peeter-pauli-kirik": "Parish of the Holy Apostles Peter and Paul in Laanemetsa",
    "ee-eaok-kahri-peaingel-miikaeli-kogudus": "Parish of the Archangel Michael in Kähri",
    "ee-eaok-korgessaare-kristuse-sundimise-kogudus": "Parish of the Nativity of Christ in Kõrgessaare",
    "ee-eaok-obinitsa-issanda-muutmise-kogudus": "Parish of the Transfiguration of the Lord in Obinitsa",
    "ee-eaok-saatse-puha-paraskeva-kogudus": "Parish of Saint Paraskeva in Saatse",
    "ee-eaok-hiiumaa-jumalasunnitaja-sundimise-kogudus": "Parish of the Nativity of the Mother of God in Hiiumaa",
    "ee-eaok-haapsalu-maria-magdaleena-kogudus": "Parish of Saint Mary Magdalene in Haapsalu",
    "ee-eaok-ilmjarve-jumalailmutamise-kogudus": "Parish of the Theophany in Ilmjärve",
    "ee-eaok-kergu-puha-suurkannataja-sinaiida-kogudus": "Parish of the Great Martyr Zenaida in Kergu",
    "ee-eaok-karula-jumalaema-kaitsmise-kogudus": "Parish of the Protection of the Mother of God in Karula",
    "ee-eaok-angerja-issanda-taevaminemise-kogudus": "Parish of the Ascension of the Lord in Angerja",
    "ee-eaok-tallinn-siimeoni-hanna": "Parish of Saint Simeon and Anna the Prophetess in Tallinn",
    "ee-eaok-uue-virtsu-kristuse-sundimise": "Auxiliary Parish of the Nativity of Christ in Uue-Virtsu",
    "ee-eaok-tallinn-issanda-muutmise": "Cathedral of the Transfiguration of the Lord in Tallinn",
    "ee-eaok-varska-georgiuse": "Parish of Saint George in Värska",
    "ee-eaok-rannu-issanda-jeruusalemma-minemise-kogudus": "Parish of the Entry of the Lord into Jerusalem in Rannu",
    "ee-eaok-antsla-kraavi-prohvet-eelija-kogudus": "Parish of the Prophet Elijah in Antsla-Kraavi",
    "ee-eaok-vara-valgi-puha-neeva-aleksandri-abikogudus": "Auxiliary Parish of Saint Alexander Nevsky in Vara-Välgi",
    "ee-eaok-voopsu-puha-nikolai-kogudus": "Parish of Saint Nicholas in Võõpsu",
    "ee-eaok-tartu-jumalaema-uinumise-kogudus": "Parish of the Dormition of the Mother of God in Tartu",
    "ee-eaok-rapina-puha-sakariase-ja-elisabeti-kogudus": "Parish of Saints Zacharias and Elizabeth in Räpina",
    "ee-eaok-poltsamaa-puhavaimu-kogudus": "Parish of the Holy Spirit in Põltsamaa",
    "ee-eaok-plaani-puha-nikolai-kirik": "Parish of Saint Nicholas in Plaani",
    "ee-eaok-noo-puha-kolmainu-kogudus": "Parish of the Holy Trinity in Nõo",
    "ee-eaok-moniste-ritsiku-ristija-johannese-kogudus": "Parish of Saint John the Baptist in Mõniste-Ritsiku",
    "ee-eaok-mehikoorma-issandamuutmise-kogudus": "Parish of the Transfiguration of the Lord in Mehikoorma",
    "ee-eaok-lalsi-puha-nikolause-kogudus": "Parish of Saint Nicholas in Lalsi",
    "ee-eaok-kavilda-puha-aleksandri-kogudus": "Parish of Saint Alexander in Kavilda",
    "ee-eaok-kastolatsi-roomukuulutamise-kirik": "Parish of the Annunciation in Kastolatsi",
    "ee-eaok-karksi-nuia-puha-aleksei-kogudus": "Parish of Saint Alexius in Karksi-Nuia",
    "ee-eaok-kaarepere-vaga-suzdali-eufimi-ja-vaga-egiptuse-maria-kogudus": "Parish of Venerable Euthymius of Suzdal and Venerable Mary of Egypt in Kaarepere",
    "ee-eaok-tartu-puhade-aleksandrite-kogudus": "Parish of the Holy Alexanders in Tartu",
    "ee-eaok-voru-suurkannataja-ekaterina-kogudus": "Parish of the Great Martyr Catherine in Võru",
    "ee-eaok-tuhalaane-jumalaema-uinumise-kogudus": "Parish of the Dormition of the Mother of God in Tuhalaane",
    "ee-eaok-arussaare-issanda-taevaminemise-kogudus": "Parish of the Ascension of the Lord in Arussaare",
    "ee-eaok-ooriku-puha-kolmainu-kogudus": "Parish of the Holy Trinity in Ööriku",
    "ee-eaok-uruste-issanda-taevaminemise-kogudus": "Parish of the Ascension of the Lord in Uruste",
    "ee-eaok-treimani-puhade-apostlite-peetruse-ja-pauluse-kogudus": "Parish of the Holy Apostles Peter and Paul in Treimani",
    "ee-eaok-tornimae-neitsi-maria-kaitsmise-kogudus": "Parish of the Protection of the Virgin Mary in Tornimäe",
    "ee-eaok-tahkuranna-jumalasunnitaja-uinumise-kogudus": "Parish of the Dormition of the Mother of God in Tahkuranna",
    "ee-eaok-sindi-jumalailmumise-kogudus": "Parish of the Theophany in Sindi",
    "ee-eaok-seli-tostamaa-puha-vassilius-suure-kogudus": "Parish of Saint Basil the Great in Seli-Tõstamaa",
    "ee-eaok-reomae-apostel-andrease-kogudus": "Parish of the Apostle Andrew in Reomäe",
    "ee-eaok-parsama-puha-innokenti-kogudus": "Parish of Saint Innocent in Pärsama",
    "ee-eaok-parnu-issandamuutmise-kogudus": "Parish of the Transfiguration of the Lord in Pärnu",
    "ee-eaok-pootsi-kopu-puha-kolmainu-kogudus": "Parish of the Holy Trinity in Pootsi-Kõpu",
    "ee-eaok-piila-peaingel-miikaeli-kogudus": "Parish of the Archangel Michael in Piila",
    "ee-eaok-paadremaa-puha-kolmainu-kogudus": "Parish of the Holy Trinity in Paadrema",
    "ee-eaok-mustjala-prohvet-eeliase-kogudus": "Parish of the Prophet Elijah in Mustjala",
    "ee-eaok-muhu-rinsi-neitsi-maria-kaasani-puhakuju-kogudus": "Parish of the Kazan Icon of the Mother of God in Muhu-Rinsi",
    "ee-eaok-muhu-hellamaa-peetruse-ja-pauluse-kogudus": "Parish of Saints Peter and Paul in Muhu-Hellamaa",
    "ee-eaok-metskula-issanda-templisseviimise-kogudus": "Parish of the Presentation of the Lord in the Temple in Metsküla",
    "ee-eaok-lumanda-issanda-muutmise-kogudus": "Parish of the Transfiguration of the Lord in Lümanda",
    "ee-eaok-levala-puha-neeva-aleksandri-kogudus": "Parish of Saint Alexander Nevsky in Levala",
    "ee-eaok-leisi-puha-olga-kogudus": "Parish of Saint Olga in Leisi",
    "ee-eaok-laimjala-vassilius-suure-kogudus": "Parish of Saint Basil the Great in Laimjala",
    "ee-eaok-laiksaare-ristija-johannese-kogudus": "Parish of Saint John the Baptist in Laiksaare",
    "ee-eaok-kihnu-puha-nikolai-kogudus": "Parish of Saint Nicholas in Kihnu",
    "ee-eaok-kuressaare-puha-nikolai-kogudus": "Parish of Saint Nicholas in Kuressaare",
    "ee-eaok-joopre-puha-suurkannataja-georgiuse-kogudus": "Parish of the Great Martyr George in Jõõpre",
    "ee-eaok-haademeeste-issandamuutmise-kogudus": "Parish of the Transfiguration of the Lord in Häädemeeste",
    "ee-kirikla-monastery": "Monastery of the Holy Fathers of the Holy Mountain in Kirikla",
    "ee-reomae-monastery": "Monastery of the Glorious Forerunner John the Baptist and the Apostle Andrew in Reomäe",
    "ee-ekok-jumalaema-kiirestikuulja-ikooni-kirik-tallinn": "Parish of the Quick to Hear Icon of the Mother of God in Tallinn",
    "ee-ekok-hram-vo-imya-svyatitelya-nikolaya-chudotvorcza-ulica-vene-tallinn": "Parish of Saint Nicholas on Vene Street in Tallinn",
    "ee-ekok-hram-rozhdestva-presvyatoj-bogorodiczy-tallinn": "Parish of the Nativity of the Mother of God in Tallinn",
    "ee-ekok-hram-v-chest-proroka-i-predtechi-gospodnya-ioanna-krestitelya-tallinn": "Parish of Saint John the Baptist in Nõmme, Tallinn",
    "ee-ekok-hram-vo-imya-svyatitelya-nikolaya-chudotvorcza-kopli-tallinn": "Parish of Saint Nicholas in Kopli, Tallinn",
    "ee-ekok-hram-v-chest-ikony-bozhiej-materi-vseh-skorbyashhih-radost-tallinn": "Parish of the Joy of All Who Sorrow Icon of the Mother of God in Tallinn",
    "ee-ekok-hram-v-chest-arhangela-mihaila-maardu": "Parish of the Archangel Michael in Maardu",
    "ee-ekok-hram-kazanskoj-ikony-bozhiej-materi-sillamyae": "Parish of the Kazan Icon of the Mother of God in Sillamäe",
    "ee-ekok-hram-bogoyavleniya-jyhvi": "Parish of the Theophany in Jõhvi",
    "ee-ekok-hram-preobrazheniya-gospodnya-kohtla-yarve": "Parish of the Transfiguration of the Lord in Kohtla-Järve",
    "ee-ekok-hram-v-chest-velikomuchenika-georgiya-pobedonoscza-tartu": "Parish of Saint George in Tartu",
    "ee-ekok-hram-vladimirskoj-ikony-bozhiej-materi-valga": "Parish of the Vladimir Icon of the Mother of God in Valga",
    "ee-ekok-hram-v-chest-velikomucheniczy-ekateriny-pyarnu": "Parish of the Great Martyr Catherine in Pärnu",
    "ee-ekok-hram-rozhdestva-presvyatoj-bogorodiczy-rakvere": "Parish of the Nativity of the Mother of God in Rakvere",
    "ee-ekok-hram-vo-imya-prepodobnogo-sergiya-radonezhskogo-paldiski": "Parish of Venerable Sergius of Radonezh in Paldiski",
    "ee-ekok-hram-v-chest-rozhdestva-proroka-i-predtechi-gospodnya-ioanna-krestitelya-tapa": "Parish of Saint John the Baptist in Tapa",
    "ee-ekok-hram-v-chest-svyatogo-pravednogo-ioanna-kronshtadtskogo-loksa": "Parish of Saint John of Kronstadt in Loksa",
    "ee-ekok-hram-vo-imya-svyatogo-blagovernogo-knyazya-aleksandra-nevskogo-haapsalu": "Parish of Saint Alexander Nevsky in Haapsalu",
    "ee-ekok-hram-v-chest-proroka-i-predtechi-gospodnya-ioanna-krestitelya-vilyandi": "Parish of Saint John the Baptist in Viljandi",
    "ee-ekok-hram-presvyatoj-troiczy-tyuri": "Parish of the Holy Trinity in Türi",
    "ee-ekok-hram-v-chest-svyatoj-blazhennoj-ksenii-peterburgskoj-azeri": "Parish of Saint Xenia of Petersburg in Aseri",
    "ee-ekok-hram-pokrova-presvyatoj-bogorodiczy-kiviyli": "Parish of the Protection of the Mother of God in Kiviõli",
    "ee-ekok-voskresenskij-kafedralnyj-sobor-narva": "Cathedral of the Resurrection of Christ in Narva",
    "ee-ekok-hram-v-chest-narvskoj-ikony-bozhiej-materi-narva": "Parish of the Narva Icon of the Mother of God in Narva",
    "ee-ekok-hram-v-chest-svyatyh-dvenadczati-apostolov-narva": "Parish of the Twelve Holy Apostles in Narva",
    "ee-ekok-hram-v-chest-svyashhennomuchenikov-aleksandra-i-dimitriya-presviterov-narvskih-narva": "Parish of the Hieromartyrs Alexander and Demetrius, Presbyters of Narva",
    "ee-ekok-hram-v-chest-svyatyh-pravednyh-simeona-bogopriimcza-i-anny-prorochiczy-v-dome-popecheniya-narva": "Parish of Righteous Simeon the God-receiver and Anna the Prophetess at the Care Home in Narva",
    "ee-ekok-hram-v-chest-svyashhennomuchenika-ioanna-kochurova-narva": "Parish of the Hieromartyr John Kochurov in Narva",
    "ee-ekok-hram-kazanskoj-ikony-bozhiej-materi-narva-jyesuu": "Parish of the Kazan Icon of the Mother of God in Narva-Jõesuu",
    "ee-ekok-hram-svyatogo-ravnoapostolnogo-knyazya-vladimira-arhierejskoe-podvore-narva-jyesuu": "Episcopal Metochion of Saint Vladimir, Equal to the Apostles, in Narva-Jõesuu",
    "ee-ekok-hram-pokrova-presvyatoj-bogorodiczy-nina": "Parish of the Protection of the Mother of God in Nina",
    "ee-ekok-hram-vo-imya-svyatitelya-nikolaya-chudotvorcza-mustvee": "Parish of Saint Nicholas the Wonderworker in Mustvee",
    "ee-ekok-jumalaema-sundimise-kirik-alajoe": "Parish of the Nativity of the Mother of God in Alajõe",
    "ee-ekok-hram-bogoyavleniya-lohusuu": "Parish of the Theophany in Lohusuu",
    "ee-ekok-hram-v-chest-svyatitelya-nikolaya-arhiepiskopa-mir-likijskih-chudotvorcza-yaama": "Parish of Saint Nicholas the Wonderworker, Archbishop of Myra in Lycia, in Jaama",
    "ee-ekok-hram-v-chest-svyatyh-ravnoapostolnyh-konstantina-i-eleny-yaama": "Parish of Saints Constantine and Helen, Equal to the Apostles, in Jaama",
    "ee-ekok-hram-sreteniya-gospodnya-varnya": "Parish of the Meeting of the Lord in Varnja",
    "ee-ekok-hram-v-chest-chestnago-i-zhivotvoryashhego-kresta-gospodnya-jygeva": "Parish of the Precious and Life-Giving Cross of the Lord in Jõgeva",
    "ee-nevsky-stauropegic": "Alexander Nevsky Cathedral in Tallinn",
    "ee-puehtitsa-monastery": "Pühtitsa Dormition Stauropegic Convent",
}


# slug | parent | exact local name | address lines separated by / | own site
# | official body page | official directory page
EAOK_TSV = r"""
priipalu-puha-vassili-suure-kirik|ee-tallinn|Priipalu Püha Vassili Suure kirik|Priipalu küla, Valgamaa||https://www.eoc.ee/kogudus/priipalu-puha-vassili-suure-kirik/|https://www.eoc.ee/piiskopkond/tallinna-peapiiskopkond/
vandra-apostlite-peetruse-pauluse-kogudus|ee-tallinn|Vändra Apostlite Peetruse-Pauluse kogudus|Vana 92, Vändra, / Vändra vald, 87701 Pärnumaa||https://www.eoc.ee/kogudus/vandra-apostlite-peetruse-pauluse-kogudus/|https://www.eoc.ee/piiskopkond/tallinna-peapiiskopkond/
velise-ristija-johannese-kogudus|ee-tallinn|Velise Ristija Johannese kogudus|Velise, Märjamaa vald, 78201 Raplamaa||https://www.eoc.ee/kogudus/velise-ristija-johannese-kogudus/|https://www.eoc.ee/piiskopkond/tallinna-peapiiskopkond/
valga-issidori-peakirik|ee-tallinn|Valga Issidori peakirik|Pargi tn 1a, 68203 Valga||https://www.eoc.ee/kogudus/valga-issidori-peakirik/|https://www.eoc.ee/piiskopkond/tallinna-peapiiskopkond/
uduvere-apostel-jaakobuse-kogudus|ee-tallinn|Uduvere Apostel Jaakobuse kogudus|Kergu mnt 89, Pärnu-Jaagupi, / Halinga vald, 87201 Pärnumaa||https://www.eoc.ee/kogudus/uduvere-apostel-jaakobuse-kogudus/|https://www.eoc.ee/piiskopkond/tallinna-peapiiskopkond/
tallinn-puha-georgi|ee-tallinn|Tallinna Püha Georgi kogudus|Ahtri 7/Paadi 2, 10151 Tallinn|https://cerkva.ee/|https://www.eoc.ee/kogudus/1973-2/|https://www.eoc.ee/piiskopkond/tallinna-peapiiskopkond/
puutli-puha-nikolai-kirik|ee-tallinn|Puutli Püha Nikolai kirik|Puutli, Vastseliina vald, Võrumaa||https://www.eoc.ee/kogudus/puutli-puha-nikolai-kirik/|https://www.eoc.ee/piiskopkond/tallinna-peapiiskopkond/
paldiski-puha-georgi-kogudus|ee-tallinn|Paldiski Püha Georgi kogudus|Pakri 2, Paldiski / 76806 Harju maakond||https://www.eoc.ee/kogudus/paldiski-puha-georgi-kogudus/|https://www.eoc.ee/piiskopkond/tallinna-peapiiskopkond/
meeksi-ristija-johannese-kogudus|ee-tallinn|Miikse Ristija Johannese kogudus|Miikse küla, Meremäe vald, Võrumaa||https://www.eoc.ee/kogudus/meeksi-ristija-johannese-kogudus/|https://www.eoc.ee/piiskopkond/tallinna-peapiiskopkond/
luhamaa-puhavaimu|ee-tallinn|Luhamaa Pühavaimu kogudus|Luhamaa, Misso vald, 65011 Võrumaa||https://www.eoc.ee/kogudus/1963-2/|https://www.eoc.ee/piiskopkond/tallinna-peapiiskopkond/
lelle-puha-kolmainu-kogudus|ee-tallinn|Lelle Püha Kolmainu abikogudus|Lelle, Eidapere alevik, Kehtna vald / 79002 Raplamaa||https://www.eoc.ee/kogudus/lelle-puha-kolmainu-kogudus/|https://www.eoc.ee/piiskopkond/tallinna-peapiiskopkond/
laatre-puhavaimu-kirik|ee-tallinn|Laatre Pühavaimu kogudus|Laatre alevik, Tõlliste vald, Valgamaa||https://www.eoc.ee/kogudus/laatre-puhavaimu-kirik/|https://www.eoc.ee/piiskopkond/tallinna-peapiiskopkond/
laanemetsa-peeter-pauli-kirik|ee-tallinn|Laanemetsa Peeter-Pauli kogudus|Laanemetsa küla, Taheva vald, Valgamaa||https://www.eoc.ee/kogudus/laanemetsa-peeter-pauli-kirik/|https://www.eoc.ee/piiskopkond/tallinna-peapiiskopkond/
kahri-peaingel-miikaeli-kogudus|ee-tallinn|Kähri Peaingel Miikaeli kogudus|Kähri, Tänassilma küla, Põlva vald / 63309 Põlvamaa||https://www.eoc.ee/kogudus/kahri-peaingel-miikaeli-kogudus/|https://www.eoc.ee/piiskopkond/tallinna-peapiiskopkond/
korgessaare-kristuse-sundimise-kogudus|ee-tallinn|Kõrgessaare Kristuse Sündimise kogudus|Luidja Seltsimaja, Kõrgessaare vald / Hiiumaa||https://www.eoc.ee/kogudus/korgessaare-kristuse-sundimise-kogudus/|https://www.eoc.ee/piiskopkond/tallinna-peapiiskopkond/
obinitsa-issanda-muutmise-kogudus|ee-tallinn|Obinitsa Issanda Muutmise kogudus|Meremäe vald, 65301 Võrumaa||https://www.eoc.ee/kogudus/obinitsa-issanda-muutmise-kogudus/|https://www.eoc.ee/piiskopkond/tallinna-peapiiskopkond/
saatse-puha-paraskeva-kogudus|ee-tallinn|Saatse Püha Paraskeva kogudus|Saatse küla, Värska vald, Põlvamaa / Allika 2, Värska küla / Värska vald, Põlvamaa||https://www.eoc.ee/kogudus/saatse-puha-paraskeva-kogudus/|https://www.eoc.ee/piiskopkond/tallinna-peapiiskopkond/
hiiumaa-jumalasunnitaja-sundimise-kogudus|ee-tallinn|Hiiumaa Jumalasünnitaja Sündimise kogudus|Taterma küla, Käina vald / 92102 Hiiumaa|http://www.kirik-hiiumaal.ee|https://www.eoc.ee/kogudus/hiiumaa-jumalasunnitaja-sundimise-kogudus/|https://www.eoc.ee/piiskopkond/tallinna-peapiiskopkond/
haapsalu-maria-magdaleena-kogudus|ee-tallinn|Haapsalu Maria-Magdaleena kogudus||http://www.maria-magdaleena.net/|https://www.eoc.ee/kogudus/haapsalu-maria-magdaleena-kogudus/|https://www.eoc.ee/piiskopkond/tallinna-peapiiskopkond/
ilmjarve-jumalailmutamise-kogudus|ee-tallinn|Ilmjärve Jumalailmumise kogudus|Ilmjärve küla, Valgamaa||https://www.eoc.ee/kogudus/ilmjarve-jumalailmutamise-kogudus/|https://www.eoc.ee/piiskopkond/tallinna-peapiiskopkond/
kergu-puha-suurkannataja-sinaiida-kogudus|ee-tallinn|Kergu Püha Suurkannataja Sinaiida kogudus|Kergu, Kaisma vald, 87401 Pärnumaa||https://www.eoc.ee/kogudus/kergu-puha-suurkannataja-sinaiida-kogudus/|https://www.eoc.ee/piiskopkond/tallinna-peapiiskopkond/
karula-jumalaema-kaitsmise-kogudus|ee-tallinn|Karula Jumalaema kaitsmise kogudus|Pikkjärve küla, Karula vald, 68101 Valga maakond||https://www.eoc.ee/kogudus/karula-jumalaema-kaitsmise-kogudus/|https://www.eoc.ee/piiskopkond/tallinna-peapiiskopkond/
angerja-issanda-taevaminemise-kogudus|ee-tallinn|Angerja Issanda Taevaminemise kogudus|Viljandi mnt. 1, Kohila vald / 79801 Raplamaa||https://www.eoc.ee/kogudus/angerja-issanda-taevaminemise-kogudus/|https://www.eoc.ee/piiskopkond/tallinna-peapiiskopkond/
tallinn-siimeoni-hanna|ee-tallinn|Tallinna Püha Siimeoni ja Naisprohvet Hanna kogudus|Ahtri 7/Paadi 2, 10151 Tallinn||https://www.eoc.ee/kogudus/kogudus-1/|https://www.eoc.ee/piiskopkond/tallinna-peapiiskopkond/
uue-virtsu-kristuse-sundimise|ee-tallinn|Uue-Virtsu Kristuse Sündimise abikogudus|Kõmsi, Hanila vald, 90102 Läänemaa||https://www.eoc.ee/kogudus/kogudus-4/|https://www.eoc.ee/piiskopkond/tallinna-peapiiskopkond/
tallinn-issanda-muutmise|ee-tallinn|Tallinna Issanda Muutmise peakirik|Suur-Kloostri 14, 10133 Tallinn|http://www.platon.ee/|https://www.eoc.ee/kogudus/kogudus-3/|https://www.eoc.ee/piiskopkond/tallinna-peapiiskopkond/
varska-georgiuse|ee-tallinn|Värska Georgiuse kogudus|Allika 2, Värska alevik / Värska vald, 64001 Põlvamaa||https://www.eoc.ee/kogudus/kogudus-2/|https://www.eoc.ee/piiskopkond/tallinna-peapiiskopkond/
rannu-issanda-jeruusalemma-minemise-kogudus|ee-tartu|Rannu Issanda Jeruusalemma minemise kogudus|||https://www.eoc.ee/kogudus/rannu-issanda-jeruusalemma-minemise-kogudus/|https://www.eoc.ee/piiskopkond/tartu-piiskopkond/
antsla-kraavi-prohvet-eelija-kogudus|ee-tartu|Antsla-Kraavi prohvet Eelija kogudus|||https://www.eoc.ee/kogudus/antsla-kraavi-prohvet-eelija-kogudus/|https://www.eoc.ee/piiskopkond/tartu-piiskopkond/
vara-valgi-puha-neeva-aleksandri-abikogudus|ee-tartu|Vara-Välgi Püha Neeva Aleksandri abikogudus|Välgi küla, Vara vald, Tartu maakond||https://www.eoc.ee/kogudus/vara-valgi-puha-neeva-aleksandri-abikogudus/|https://www.eoc.ee/piiskopkond/tartu-piiskopkond/
voopsu-puha-nikolai-kogudus|ee-tartu|Võõpsu Püha Nikolai kogudus|Võõpsu, Räpina vald, 64401 Põlvamaa||https://www.eoc.ee/kogudus/voopsu-puha-nikolai-kogudus/|https://www.eoc.ee/piiskopkond/tartu-piiskopkond/
tartu-jumalaema-uinumise-kogudus|ee-tartu|Tartu Jumalaema Uinumise Kogudus|Magasini 1, 51005 Tartu||https://www.eoc.ee/kogudus/tartu-jumalaema-uinumise-kogudus/|https://www.eoc.ee/piiskopkond/tartu-piiskopkond/
rapina-puha-sakariase-ja-elisabeti-kogudus|ee-tartu|Räpina Püha Sakariase ja Elisabeti kogudus|Apteegi 5, Räpina 64505 Põlvamaa||https://www.eoc.ee/kogudus/rapina-puha-sakariase-ja-elisabeti-kogudus/|https://www.eoc.ee/piiskopkond/tartu-piiskopkond/
poltsamaa-puhavaimu-kogudus|ee-tartu|Põltsamaa Pühavaimu kogudus|Lossi 21, Põltsamaa, 48104 Jõgevamaa||https://www.eoc.ee/kogudus/poltsamaa-puhavaimu-kogudus/|https://www.eoc.ee/piiskopkond/tartu-piiskopkond/
plaani-puha-nikolai-kirik|ee-tartu|Plaani Püha Nikolai kirik|||https://www.eoc.ee/kogudus/plaani-puha-nikolai-kirik/|https://www.eoc.ee/piiskopkond/tartu-piiskopkond/
noo-puha-kolmainu-kogudus|ee-tartu|Nõo Püha Kolmainu kogudus|Vana-Nõo 20, 61601 Nõo, Tartumaa||https://www.eoc.ee/kogudus/noo-puha-kolmainu-kogudus/|https://www.eoc.ee/piiskopkond/tartu-piiskopkond/
moniste-ritsiku-ristija-johannese-kogudus|ee-tartu|Mõniste-Ritsiku Ristija Johannese kogudus|Varstu, Varstu vald, 66101 Võrumaa||https://www.eoc.ee/kogudus/moniste-ritsiku-ristija-johannese-kogudus/|https://www.eoc.ee/piiskopkond/tartu-piiskopkond/
mehikoorma-issandamuutmise-kogudus|ee-tartu|Mehikoorma Issandamuutmise kogudus|Mehikoorma alevik, Meeksi vald, Tartumaa||https://www.eoc.ee/kogudus/mehikoorma-issandamuutmise-kogudus/|https://www.eoc.ee/piiskopkond/tartu-piiskopkond/
lalsi-puha-nikolause-kogudus|ee-tartu|Lalsi Püha Nikolause kogudus|Lalsi küla, Kolga-Jaani vald, Viljandimaa||https://www.eoc.ee/kogudus/lalsi-puha-nikolause-kogudus/|https://www.eoc.ee/piiskopkond/tartu-piiskopkond/
kavilda-puha-aleksandri-kogudus|ee-tartu|Kavilda Püha Aleksandri kogudus|||https://www.eoc.ee/kogudus/kavilda-puha-aleksandri-kogudus/|https://www.eoc.ee/piiskopkond/tartu-piiskopkond/
kastolatsi-roomukuulutamise-kirik|ee-tartu|Kastolatsi Rõõmukuulutamise kirik|Kastolatsi küla, Valgamaa||https://www.eoc.ee/kogudus/kastolatsi-roomukuulutamise-kirik/|https://www.eoc.ee/piiskopkond/tartu-piiskopkond/
karksi-nuia-puha-aleksei-kogudus|ee-tartu|Karksi-Nuia Püha Aleksei kogudus|Pärnu mnt 16, Karksi-Nuia 69102 Viljandimaa||https://www.eoc.ee/kogudus/karksi-nuia-puha-aleksei-kogudus/|https://www.eoc.ee/piiskopkond/tartu-piiskopkond/
kaarepere-vaga-suzdali-eufimi-ja-vaga-egiptuse-maria-kogudus|ee-tartu|Kaarepere Vaga Suzdali Eufimi ja Vaga Egiptuse Maria kogudus|Kaarepere, Palamuse vald 49201 Jõgevamaa||https://www.eoc.ee/kogudus/kaarepere-vaga-suzdali-eufimi-ja-vaga-egiptuse-maria-kogudus/|https://www.eoc.ee/piiskopkond/tartu-piiskopkond/
tartu-puhade-aleksandrite-kogudus|ee-tartu|Tartu Pühade Aleksandrite kogudus|Sõbra tn 19 a, 50107 Tartu||https://www.eoc.ee/kogudus/tartu-puhade-aleksandrite-kogudus/|https://www.eoc.ee/piiskopkond/tartu-piiskopkond/
voru-suurkannataja-ekaterina-kogudus|ee-tartu|Võru Suurkannataja Ekaterina kogudus|Lembitu 1a, 65608 Võru||https://www.eoc.ee/kogudus/voru-suurkannataja-ekaterina-kogudus/|https://www.eoc.ee/piiskopkond/tartu-piiskopkond/
tuhalaane-jumalaema-uinumise-kogudus|ee-tartu|Tuhalaane Jumalaema Uinumise kogudus|Tuhalaane küla, Karksi vald 71022 Viljandimaa||https://www.eoc.ee/kogudus/tuhalaane-jumalaema-uinumise-kogudus/|https://www.eoc.ee/piiskopkond/tartu-piiskopkond/
arussaare-issanda-taevaminemise-kogudus|ee-tartu|Arussaare Issanda Taevaminemise kogudus|||https://www.eoc.ee/kogudus/arussaare-issanda-taevaminemise-kogudus/|https://www.eoc.ee/piiskopkond/tartu-piiskopkond/
ooriku-puha-kolmainu-kogudus|ee-parnu-saare|Ööriku Püha Kolmainu kogudus|Ööriku, Orissaare vald, 94601 Saaremaa||https://www.eoc.ee/kogudus/ooriku-puha-kolmainu-kogudus/|https://www.eoc.ee/piiskopkond/parnu-ja-saare-piiskopkond/
uruste-issanda-taevaminemise-kogudus|ee-parnu-saare|Uruste Issanda Taevaminemise kogudus|Uruste, Kihlepa, Audru vald / 88305 Pärnumaa||https://www.eoc.ee/kogudus/uruste-issanda-taevaminemise-kogudus/|https://www.eoc.ee/piiskopkond/parnu-ja-saare-piiskopkond/
treimani-puhade-apostlite-peetruse-ja-pauluse-kogudus|ee-parnu-saare|Treimani Pühade Apostlite Peetruse ja Pauluse kogudus|Treimani, Häädemeeste vald / 86003 Pärnumaa||https://www.eoc.ee/kogudus/treimani-puhade-apostlite-peetruse-ja-pauluse-kogudus/|https://www.eoc.ee/piiskopkond/parnu-ja-saare-piiskopkond/
tornimae-neitsi-maria-kaitsmise-kogudus|ee-parnu-saare|Tornimäe Neitsi Maria Kaitsmise kogudus|Tornimäe, Pöide vald, 94501 Saaremaa||https://www.eoc.ee/kogudus/tornimae-neitsi-maria-kaitsmise-kogudus/|https://www.eoc.ee/piiskopkond/parnu-ja-saare-piiskopkond/
tahkuranna-jumalasunnitaja-uinumise-kogudus|ee-parnu-saare|Tahkuranna Jumalasünnitaja Uinumise kogudus|Tahkuranna, Tahkuranna vald / 86501 Pärnumaa||https://www.eoc.ee/kogudus/tahkuranna-jumalasunnitaja-uinumise-kogudus/|https://www.eoc.ee/piiskopkond/parnu-ja-saare-piiskopkond/
sindi-jumalailmumise-kogudus|ee-parnu-saare|Sindi Jumalailmumise kogudus|Pärna 29, 86075 Sindi||https://www.eoc.ee/kogudus/sindi-jumalailmumise-kogudus/|https://www.eoc.ee/piiskopkond/parnu-ja-saare-piiskopkond/
seli-tostamaa-puha-vassilius-suure-kogudus|ee-parnu-saare|Seli-Tõstamaa Püha Vassilius Suure Kogudus|Seliste küla, Tõstamaa vald, Pärnumaa||https://www.eoc.ee/kogudus/seli-tostamaa-puha-vassilius-suure-kogudus/|https://www.eoc.ee/piiskopkond/parnu-ja-saare-piiskopkond/
reomae-apostel-andrease-kogudus|ee-parnu-saare|Reomäe Apostel Andrease kogudus|Reo, Pihtla vald, 94111 Saaremaa||https://www.eoc.ee/kogudus/reomae-apostel-andrease-kogudus/|https://www.eoc.ee/piiskopkond/parnu-ja-saare-piiskopkond/
parsama-puha-innokenti-kogudus|ee-parnu-saare|Pärsama Püha Innokenti kogudus|Pärsama, Leisi vald, 94201 Saaremaa||https://www.eoc.ee/kogudus/parsama-puha-innokenti-kogudus/|https://www.eoc.ee/piiskopkond/parnu-ja-saare-piiskopkond/
parnu-issandamuutmise-kogudus|ee-parnu-saare|Pärnu Issandamuutmise kogudus|Aia 5, 80011 Pärnu||https://www.eoc.ee/kogudus/parnu-issandamuutmise-kogudus/|https://www.eoc.ee/piiskopkond/parnu-ja-saare-piiskopkond/
pootsi-kopu-puha-kolmainu-kogudus|ee-parnu-saare|Pootsi-Kõpu Püha Kolmainu kogudus|Kõpu, Tõstamaa vald, 88103 Pärnumaa||https://www.eoc.ee/kogudus/pootsi-kopu-puha-kolmainu-kogudus/|https://www.eoc.ee/piiskopkond/parnu-ja-saare-piiskopkond/
piila-peaingel-miikaeli-kogudus|ee-parnu-saare|Piila Peaingel Miikaeli kogudus|Piila, Kaarma vald, 93823 Saaremaa||https://www.eoc.ee/kogudus/piila-peaingel-miikaeli-kogudus/|https://www.eoc.ee/piiskopkond/parnu-ja-saare-piiskopkond/
paadremaa-puha-kolmainu-kogudus|ee-parnu-saare|Paadrema Püha Kolmainu kogudus|Paadrema, Varbla vald, 88202 Pärnumaa||https://www.eoc.ee/kogudus/paadremaa-puha-kolmainu-kogudus/|https://www.eoc.ee/piiskopkond/parnu-ja-saare-piiskopkond/
mustjala-prohvet-eeliase-kogudus|ee-parnu-saare|Mustjala Prohvet Eeliase kogudus|Mustjala, Mustjala vald, 93601 Saaremaa||https://www.eoc.ee/kogudus/mustjala-prohvet-eeliase-kogudus/|https://www.eoc.ee/piiskopkond/parnu-ja-saare-piiskopkond/
muhu-rinsi-neitsi-maria-kaasani-puhakuju-kogudus|ee-parnu-saare|Muhu-Rinsi Neitsi Maria Kaasani Pühakuju kogudus|Rinsi, Muhu vald, 94701 Saaremaa||https://www.eoc.ee/kogudus/muhu-rinsi-neitsi-maria-kaasani-puhakuju-kogudus/|https://www.eoc.ee/piiskopkond/parnu-ja-saare-piiskopkond/
muhu-hellamaa-peetruse-ja-pauluse-kogudus|ee-parnu-saare|Muhu-Hellamaa Peetruse ja Pauluse kogudus|Hellamaa, Muhu vald, 94701 Saaremaa||https://www.eoc.ee/kogudus/muhu-hellamaa-peetruse-ja-pauluse-kogudus/|https://www.eoc.ee/piiskopkond/parnu-ja-saare-piiskopkond/
metskula-issanda-templisseviimise-kogudus|ee-parnu-saare|Metsküla Issanda Templisseviimise kogudus|Metsküla, Leisi vald, 93824 Saaremaa||https://www.eoc.ee/kogudus/metskula-issanda-templisseviimise-kogudus/|https://www.eoc.ee/piiskopkond/parnu-ja-saare-piiskopkond/
lumanda-issanda-muutmise-kogudus|ee-parnu-saare|Lümanda Issanda Muutmise kogudus|Lümanda, Lümanda vald, 93301 Saaremaa||https://www.eoc.ee/kogudus/lumanda-issanda-muutmise-kogudus/|https://www.eoc.ee/piiskopkond/parnu-ja-saare-piiskopkond/
levala-puha-neeva-aleksandri-kogudus|ee-parnu-saare|Levala Püha Neeva Aleksandri kogudus|Tumala, Orissaare vald, 94601 Saaremaa||https://www.eoc.ee/kogudus/levala-puha-neeva-aleksandri-kogudus/|https://www.eoc.ee/piiskopkond/parnu-ja-saare-piiskopkond/
leisi-puha-olga-kogudus|ee-parnu-saare|Leisi Püha Olga kogudus|Leisi, Leisi vald, 94202 Saaremaa||https://www.eoc.ee/kogudus/leisi-puha-olga-kogudus/|https://www.eoc.ee/piiskopkond/parnu-ja-saare-piiskopkond/
laimjala-vassilius-suure-kogudus|ee-parnu-saare|Laimjala Vassilius Suure kogudus|Kahtla, Laimjala vald, 94401 Saaremaa||https://www.eoc.ee/kogudus/laimjala-vassilius-suure-kogudus/|https://www.eoc.ee/piiskopkond/parnu-ja-saare-piiskopkond/
laiksaare-ristija-johannese-kogudus|ee-parnu-saare|Laiksaare Ristija Johannese kogudus|Urissaare küla, Häädemeeste vald / 86019 Pärnumaa||https://www.eoc.ee/kogudus/laiksaare-ristija-johannese-kogudus/|https://www.eoc.ee/piiskopkond/parnu-ja-saare-piiskopkond/
kihnu-puha-nikolai-kogudus|ee-parnu-saare|Kihnu Püha Nikolai kogudus|Linaküla, Kihnu vald, 88001 Pärnumaa||https://www.eoc.ee/kogudus/kihnu-puha-nikolai-kogudus/|https://www.eoc.ee/piiskopkond/parnu-ja-saare-piiskopkond/
kuressaare-puha-nikolai-kogudus|ee-parnu-saare|Kuressaare Püha Nikolai kogudus|Lossi 8, 93816 Kuressaare||https://www.eoc.ee/kogudus/kuressaare-puha-nikolai-kogudus/|https://www.eoc.ee/piiskopkond/parnu-ja-saare-piiskopkond/
joopre-puha-suurkannataja-georgiuse-kogudus|ee-parnu-saare|Jõõpre Püha Suurkannataja Georgiuse kogudus|Jõõpre, Audru vald, 88303 Pärnumaa||https://www.eoc.ee/kogudus/joopre-puha-suurkannataja-georgiuse-kogudus/|https://www.eoc.ee/piiskopkond/parnu-ja-saare-piiskopkond/
haademeeste-issandamuutmise-kogudus|ee-parnu-saare|Häädemeeste Issandamuutmise kogudus|Kooli 23, Häädemeeste, 86001 Pärnumaa||https://www.eoc.ee/kogudus/haademeeste-issandamuutmise-kogudus/|https://www.eoc.ee/piiskopkond/parnu-ja-saare-piiskopkond/
""".strip()


# slug | parent | exact local name | address | own site | official body page
EOKK_TSV = r"""
tallinna-aleksander-nevski-katedraal|russia|Tallinna Neeva Aleksandri katedraal|Lossi plats 10, 10130 Tallinn, Estonia|https://nevskysobor.ee|https://et.orthodox.ee/parishes/tallinna-aleksander-nevski-katedraal/
jumalaema-kiirestikuulja-ikooni-kirik-tallinn|ekok-tallinn|Jumalaema Kiirestikuulja ikooni kirik, Tallinn|Loopealse puiestee 8, 13915 Tallinn, Eesti|https://panagia.ee/index.php|https://et.orthodox.ee/parishes/jumalaema-kiirestikuulja-ikooni-kirik-tallinn/
hram-vo-imya-svyatitelya-nikolaya-chudotvorcza-ulica-vene-tallinn|ekok-tallinn|Püha Nikolai kirik Vene tänaval, Tallinn|Vene 24, 10124 Tallinn, Eesti|https://stnicolas.org/|https://et.orthodox.ee/parishes/hram-vo-imya-svyatitelya-nikolaya-chudotvorcza-ulica-vene-tallinn/
hram-rozhdestva-presvyatoj-bogorodiczy-tallinn|ekok-tallinn|Jumalaema Sündimise kirik, Tallinn|Liivalaia 38, 10145 Tallinn, Eesti|https://kaasanikirik.ee|https://et.orthodox.ee/parishes/hram-rozhdestva-presvyatoj-bogorodiczy-tallinn/
hram-v-chest-proroka-i-predtechi-gospodnya-ioanna-krestitelya-tallinn|ekok-tallinn|Nõmme Ristija Johannese kirik, Tallinn|Tähe 2, 11629 Tallinn, Eesti|https://www.nommejohannese.ee/|https://et.orthodox.ee/parishes/hram-v-chest-proroka-i-predtechi-gospodnya-ioanna-krestitelya-tallinn/
hram-vo-imya-svyatitelya-nikolaya-chudotvorcza-kopli-tallinn|ekok-tallinn|Püha Nikolai kirik Koplis, Tallinn|Treiali 6, 11712 Tallinn, Eesti||https://et.orthodox.ee/parishes/hram-vo-imya-svyatitelya-nikolaya-chudotvorcza-kopli-tallinn/
hram-v-chest-ikony-bozhiej-materi-vseh-skorbyashhih-radost-tallinn|ekok-tallinn|Jumalaema Kõikide kurbade Rõõmu ikooni kirik, Tallinn|Sitsi 15a, 10313 Tallinn, Eesti|https://tallinn-vsr.ru/|https://et.orthodox.ee/parishes/hram-v-chest-ikony-bozhiej-materi-vseh-skorbyashhih-radost-tallinn/
hram-v-chest-arhangela-mihaila-maardu|ekok-tallinn|Peaingel Miikaeli kirik, Maardu|Keemikute 40, 74112 Maardu, Harju maakond||https://et.orthodox.ee/parishes/hram-v-chest-arhangela-mihaila-maardu/
hram-kazanskoj-ikony-bozhiej-materi-sillamyae|ekok-tallinn|Jumalaema Kaasani ikooni kirik, Sillamäe|Jõe 1, 40232 Sillamäe, Ida-Viru maakond|http://silort.ee|https://et.orthodox.ee/parishes/hram-kazanskoj-ikony-bozhiej-materi-sillamyae/
hram-bogoyavleniya-jyhvi|ekok-tallinn|Jumalailmumise kirik, Jõhvi|Narva mnt 2, 41531 Jõhvi, Ida-Viru maakond|https://www.theophany.ee|https://et.orthodox.ee/parishes/hram-bogoyavleniya-jyhvi/
hram-preobrazheniya-gospodnya-kohtla-yarve|ekok-tallinn|Issanda Muutmise kirik, Kohtla-Järve|Järveküla tee 3, 30328 Kohtla-Järve, Ida-Viru maakond|https://k-jhram.ee/|https://et.orthodox.ee/parishes/hram-preobrazheniya-gospodnya-kohtla-yarve/
hram-v-chest-velikomuchenika-georgiya-pobedonoscza-tartu|ekok-tallinn|Püha Jüri kirik, Tartu|Narva maantee 103, 51008 Tartu, Tartu maakond|https://georgikirik.ee/ru/|https://et.orthodox.ee/parishes/hram-v-chest-velikomuchenika-georgiya-pobedonoscza-tartu/
hram-vladimirskoj-ikony-bozhiej-materi-valga|ekok-tallinn|Jumalaema Vladimiri ikooni kirik, Valga|Tehnika 7, 68205 Valga, Valga maakond|https://www.goldenmary.ee/|https://et.orthodox.ee/parishes/hram-vladimirskoj-ikony-bozhiej-materi-valga/
hram-v-chest-velikomucheniczy-ekateriny-pyarnu|ekok-tallinn|Püha suurmärter Katariina kirik, Pärnu|Vee 8, 80011 Pärnu, Pärnu maakond||https://et.orthodox.ee/parishes/hram-v-chest-velikomucheniczy-ekateriny-pyarnu/
hram-rozhdestva-presvyatoj-bogorodiczy-rakvere|ekok-tallinn|Jumalaema Sündimise kirik, Rakvere|Tallinna 17, 44306 Rakvere, Lääne-Viru maakond||https://et.orthodox.ee/parishes/hram-rozhdestva-presvyatoj-bogorodiczy-rakvere/
hram-vo-imya-prepodobnogo-sergiya-radonezhskogo-paldiski|ekok-tallinn|Radoneži vaga Sergi kirik, Paldiski|Tuule tänav 1, 76806 Paldiski, Harju maakond|https://orthodox-paldiski.ee/|https://et.orthodox.ee/parishes/hram-vo-imya-prepodobnogo-sergiya-radonezhskogo-paldiski/
hram-v-chest-rozhdestva-proroka-i-predtechi-gospodnya-ioanna-krestitelya-tapa|ekok-tallinn|Ristija Johannese kirik, Tapa|Pikk 1, 45106 Tapa, Lääne-Viru maakond|http://tapakirik.ee/|https://et.orthodox.ee/parishes/hram-v-chest-rozhdestva-proroka-i-predtechi-gospodnya-ioanna-krestitelya-tapa/
hram-v-chest-svyatogo-pravednogo-ioanna-kronshtadtskogo-loksa|ekok-tallinn|Kroonlinna püha Joanni kirik, Loksa|Posti tn. 17a, 74805 Loksa, Harju maakond||https://et.orthodox.ee/parishes/hram-v-chest-svyatogo-pravednogo-ioanna-kronshtadtskogo-loksa/
hram-vo-imya-svyatogo-blagovernogo-knyazya-aleksandra-nevskogo-haapsalu|ekok-tallinn|Neeva püha Aleksandri kirik, Haapsalu|Surnuaia 1, 90504 Haapsalu, Lääne maakond|http://nevski.ee|https://et.orthodox.ee/parishes/hram-vo-imya-svyatogo-blagovernogo-knyazya-aleksandra-nevskogo-haapsalu/
hram-v-chest-proroka-i-predtechi-gospodnya-ioanna-krestitelya-vilyandi|ekok-tallinn|Ristija Johannese kirik, Viljandi|Mäe tn. 8, 71004 Viljandi linn, Viljandi maakond||https://et.orthodox.ee/parishes/hram-v-chest-proroka-i-predtechi-gospodnya-ioanna-krestitelya-vilyandi/
hram-presvyatoj-troiczy-tyuri|ekok-tallinn|Püha Kolmainu kirik, Türi|Aia 2b, 72212 Türi, Järva maakond||https://et.orthodox.ee/parishes/hram-presvyatoj-troiczy-tyuri/
hram-v-chest-svyatoj-blazhennoj-ksenii-peterburgskoj-azeri|ekok-tallinn|Peterburi püha Ksenia kirik, Aseri|Pargi 8, 43401 Aseri, Ida-Viru maakond||https://et.orthodox.ee/parishes/hram-v-chest-svyatoj-blazhennoj-ksenii-peterburgskoj-azeri/
hram-pokrova-presvyatoj-bogorodiczy-kiviyli|ekok-tallinn|Kiviõli Jumalaema Kaitsmise kirik|Piiri 2, 43125 Kiviõli, Ida-Viru maakond||https://et.orthodox.ee/parishes/hram-pokrova-presvyatoj-bogorodiczy-kiviyli/
voskresenskij-kafedralnyj-sobor-narva|ekok-narva|Воскресенский кафедральный собор, Нарва|Bastrakovi 4, 20308 Narva, Estonia||https://et.orthodox.ee/parishes/voskresenskij-kafedralnyj-sobor-narva/
hram-v-chest-narvskoj-ikony-bozhiej-materi-narva|ekok-narva|Храм в честь Нарвской иконы Божией Матери, Нарва|Rakvere 39, 20306 Narva, Estonia|http://www.narva-hram.ee/|https://et.orthodox.ee/parishes/hram-v-chest-narvskoj-ikony-bozhiej-materi-narva/
hram-v-chest-svyatyh-dvenadczati-apostolov-narva|ekok-narva|Храм в честь святых двенадцати Апостолов, Нарва|Mõisa 4, 21006 Narva, Estonia||https://et.orthodox.ee/parishes/hram-v-chest-svyatyh-dvenadczati-apostolov-narva/
hram-v-chest-svyashhennomuchenikov-aleksandra-i-dimitriya-presviterov-narvskih-narva|ekok-narva|Храм в честь священномучеников Александра и Димитрия, пресвитеров Нарвских, Нарва|Joala 5b, 20103 Narva||https://et.orthodox.ee/parishes/hram-v-chest-svyashhennomuchenikov-aleksandra-i-dimitriya-presviterov-narvskih-narva/
hram-v-chest-svyatyh-pravednyh-simeona-bogopriimcza-i-anny-prorochiczy-v-dome-popecheniya-narva|ekok-narva|Храм в честь святых праведных Симеона Богоприимца и Анны Пророчицы в доме попечения, Нарва|||https://et.orthodox.ee/parishes/hram-v-chest-svyatyh-pravednyh-simeona-bogopriimcza-i-anny-prorochiczy-v-dome-popecheniya-narva/
hram-v-chest-svyashhennomuchenika-ioanna-kochurova-narva|ekok-narva|Храм в честь священномученика Иоанна Кочурова, Нарва|Igor Grafovi tn. 4, 20308 Narva, Estonia||https://et.orthodox.ee/parishes/hram-v-chest-svyashhennomuchenika-ioanna-kochurova-narva/
hram-kazanskoj-ikony-bozhiej-materi-narva-jyesuu|ekok-narva|Храм Казанской иконы Божией Матери, Нарва-Йыэсуу|Vabaduse 63, 29023 Narva, Ida-Viru maakond||https://et.orthodox.ee/parishes/hram-kazanskoj-ikony-bozhiej-materi-narva-jyesuu/
hram-svyatogo-ravnoapostolnogo-knyazya-vladimira-arhierejskoe-podvore-narva-jyesuu|ekok-narva|Храм святого равноапостольного князя Владимира (Архиерейское подворье), Нарва-Йыэсуу|Koidu 6, 29023 Narva-Jõesuu, Ida-Viru maakond||https://et.orthodox.ee/parishes/hram-svyatogo-ravnoapostolnogo-knyazya-vladimira-arhierejskoe-podvore-narva-jyesuu/
hram-pokrova-presvyatoj-bogorodiczy-nina|ekok-narva|Храм Покрова Пресвятой Богородицы, Нина|||https://et.orthodox.ee/parishes/hram-pokrova-presvyatoj-bogorodiczy-nina/
hram-vo-imya-svyatitelya-nikolaya-chudotvorcza-mustvee|ekok-narva|Храм во имя святителя Николая Чудотворца, Муствеэ|Tartu 14, 49604 Mustvee, Jõgeva maakond||https://et.orthodox.ee/parishes/hram-vo-imya-svyatitelya-nikolaya-chudotvorcza-mustvee/
jumalaema-sundimise-kirik-alajoe|ekok-narva|Jumalaema Sündimise kirik, Alajõe|Kooli 15a, 41001 Alajõe, Ida-Viru maakond||https://et.orthodox.ee/parishes/jumalaema-sundimise-kirik-alajoe/
hram-bogoyavleniya-lohusuu|ekok-narva|Храм Богоявления, Лохусуу|Järve tee 21, 42001 Lohusuu, Jõgeva maakond||https://et.orthodox.ee/parishes/hram-bogoyavleniya-lohusuu/
hram-v-chest-svyatitelya-nikolaya-arhiepiskopa-mir-likijskih-chudotvorcza-yaama|ekok-narva|Храм в честь Святителя Николая архиепископа Мир Ликийских Чудотворца, Яама|Kiriku 2, 41010 Jaama, Ida-Viru maakond||https://et.orthodox.ee/parishes/hram-v-chest-svyatitelya-nikolaya-arhiepiskopa-mir-likijskih-chudotvorcza-yaama/
hram-v-chest-svyatyh-ravnoapostolnyh-konstantina-i-eleny-yaama|ekok-narva|Храм в честь святых равноапостольных Константина и Елены, Яама|||https://et.orthodox.ee/parishes/hram-v-chest-svyatyh-ravnoapostolnyh-konstantina-i-eleny-yaama/
hram-sreteniya-gospodnya-varnya|ekok-narva|Храм Сретения Господня, Варнья|Kesk 3, 60305 Varnja, Tartu maakond||https://et.orthodox.ee/parishes/hram-sreteniya-gospodnya-varnya/
hram-v-chest-chestnago-i-zhivotvoryashhego-kresta-gospodnya-jygeva|ekok-narva|Храм в честь Честнаго и Животворящего Креста Господня, Йыгева|Suur 38, 48306 Jõgeva, Jõgeva maakond|https://www.jogevahram.ee/|https://et.orthodox.ee/parishes/hram-v-chest-chestnago-i-zhivotvoryashhego-kresta-gospodnya-jygeva/
""".strip()


def fields(line, count):
    parts = [part.strip() for part in line.split("|")]
    if len(parts) != count:
        raise ValueError("bad Estonia source row: %s" % line)
    return parts


def eaok_rows():
    rows = []
    for line in EAOK_TSV.splitlines():
        slug, parent, local, address, site, detail, directory = fields(line, 7)
        row = dict(id="ee-eaok-" + slug, parent=parent, kind="parish",
                   rank="Parish", name=local, local=local, country="EE",
                   sources=[detail, directory])
        if address:
            row["address"] = [part.strip() for part in address.split("/")]
        if site:
            row["site"] = site
        rows.append(row)
    rows.extend([
        dict(id="ee-kirikla-monastery", parent="ee-tallinn",
             kind="monastery", rank="Monastery",
             name="Eesti Apostlik-Õigeusu Kiriku Püha Mäe Isade Püha Klooster Kiriklas",
             local="Eesti Apostlik-Õigeusu Kiriku Püha Mäe Isade Püha Klooster Kiriklas",
             country="EE",
             address=["Üiso", "Pihali küla", "Kohila vald",
                      "79703 Rapla maakond"],
             site="https://www.kiriklaklooster.ee/",
             sources=[
                 "https://www.eoc.ee/eesti-apostlik-oigeusu-kirik/kirikla-klooster/",
                 "https://www.kiriklaklooster.ee/",
             ]),
        dict(id="ee-reomae-monastery", parent="ee-parnu-saare",
             kind="monastery", rank="Monastery",
             name="Eesti Apostlik-Õigeusu Kiriku Aulise Eelkäija Ristija Johannese ja Apostel Andrease Püha Klooster Reomäel",
             local="Eesti Apostlik-Õigeusu Kiriku Aulise Eelkäija Ristija Johannese ja Apostel Andrease Püha Klooster Reomäel",
             country="EE",
             address=["Reo küla", "Pihtla vald", "94171 Saaremaa"],
             site="https://www.reomaeklooster.ee/",
             sources=[
                 "https://www.eoc.ee/eesti-apostlik-oigeusu-kirik/skiita/",
                 "https://www.reomaeklooster.ee/",
             ]),
    ])
    return rows


def ekok_rows():
    rows = []
    for line in EOKK_TSV.splitlines():
        slug, parent, local, address, site, detail = fields(line, 6)
        if parent == "russia":
            continue
        row = dict(id="ee-ekok-" + slug, parent=parent, kind="parish",
                   rank="Parish", name=local, local=local, country="EE",
                   sources=[detail, EOKK])
        if address:
            row["address"] = [address]
        if site:
            row["site"] = site
        rows.append(row)
    return rows


DIRECT_RUSSIA_ROWS = [
    dict(id="ee-nevsky-stauropegic", parent="russia", kind="parish",
         rank="Stauropegic Parish",
         name=ENGLISH_NAMES["ee-nevsky-stauropegic"],
         local="Tallinna Neeva Aleksandri katedraal", country="EE",
         address=["Lossi plats 10, 10130 Tallinn, Estonia"],
         site="https://nevskysobor.ee",
         sources=[
             "https://et.orthodox.ee/parishes/tallinna-aleksander-nevski-katedraal/",
             "https://ru.orthodox.ee/church/eocmp-history/",
             ESTONIA_CHURCH_STRUCTURE,
         ]),
    dict(id="ee-puehtitsa-monastery", parent="russia", kind="monastery",
         rank="Stauropegic Convent",
         name=ENGLISH_NAMES["ee-puehtitsa-monastery"],
         local="Пюхтицкий Успенский ставропигиальный женский монастырь",
         country="EE",
         address=["Kuremäe küla, Alutaguse vald 41201, Ida-Virumaa, Eesti"],
         site="https://www.puhtitsa.ee/",
         sources=[
             "https://ru.orthodox.ee/documents/eocmp-statute/",
             "https://www.puhtitsa.ee/index.php/palomnikam/kontakt",
             ESTONIA_CHURCH_STRUCTURE,
         ]),
]


def clean(row):
    out = {key: value for key, value in row.items()
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
    source_rows = eaok_rows() + ekok_rows()
    source_ids = {row["id"] for row in source_rows + DIRECT_RUSSIA_ROWS}
    name_ids = set(ENGLISH_NAMES)
    if source_ids != name_ids:
        missing = sorted(source_ids - name_ids)
        extra = sorted(name_ids - source_ids)
        raise ValueError("English name coverage mismatch; missing=%r extra=%r"
                         % (missing, extra))
    grouped = {parent: [] for parent in (
        "ee-tallinn", "ee-tartu", "ee-parnu-saare",
        "ekok-tallinn", "ekok-narva")}
    seen = set(grouped)
    for source in source_rows:
        row = clean(source)
        row_id = row.get("id")
        parent = row.get("parent")
        if not row_id or row_id in seen:
            raise ValueError("duplicate or missing id: %s" % row_id)
        if parent not in grouped:
            raise ValueError("%s hangs off unknown parent %s" % (row_id, parent))
        if row.get("kind") not in {"parish", "monastery"}:
            raise ValueError("%s has unsupported kind" % row_id)
        if not row.get("local") or row.get("country") != "EE":
            raise ValueError("%s lacks its Estonian source identity" % row_id)
        row["name"] = ENGLISH_NAMES[row_id]
        seen.add(row_id)
        grouped[parent].append(row)
    expected = {
        "ee-tallinn": 28,
        "ee-tartu": 20,
        "ee-parnu-saare": 27,
        "ekok-tallinn": 22,
        "ekok-narva": 16,
    }
    for parent, count in expected.items():
        if len(grouped[parent]) != count:
            raise ValueError("%s must publish exactly %d rows, not %d" %
                             (parent, count, len(grouped[parent])))
    return {
        parent: {"v": 1, "parent": parent, "country": "EE", "rows": rows}
        for parent, rows in grouped.items()
    }


def manifest(payloads=None):
    payloads = payloads or build()
    return {
        parent: {
            "url": "/data/directory/%s.v1.json" % parent,
            "count": len(payload["rows"]),
            "country": "EE",
        }
        for parent, payload in sorted(payloads.items())
    }


def encoded(payload):
    return json.dumps(payload, ensure_ascii=False,
                      separators=(",", ":")).encode("utf-8")


def output_path(parent):
    return OUT / ("%s.v1.json" % parent)


def write(payloads):
    OUT.mkdir(parents=True, exist_ok=True)
    for parent, payload in sorted(payloads.items()):
        path = output_path(parent)
        path.write_bytes(encoded(payload))
        print("wrote %s (%d rows)" %
              (path.relative_to(ROOT), len(payload["rows"])))


def problems(payloads):
    errors = []
    expected = set()
    for parent, payload in sorted(payloads.items()):
        path = output_path(parent)
        expected.add(path.name)
        if not path.exists():
            errors.append("missing %s" % path.relative_to(ROOT))
        elif path.read_bytes().replace(b"\r\n", b"\n") != encoded(payload):
            errors.append("stale %s" % path.relative_to(ROOT))
    for prefix in ("ee-", "ekok-"):
        for path in OUT.glob(prefix + "*.v1.json"):
            if path.name not in expected:
                errors.append("unexpected %s" % path.relative_to(ROOT))
    return errors


def main():
    parser = argparse.ArgumentParser()
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument("--write", action="store_true")
    mode.add_argument("--check", action="store_true")
    args = parser.parse_args()
    try:
        payloads = build()
        if args.write:
            write(payloads)
        errors = problems(payloads)
    except (OSError, ValueError) as exc:
        print("directory Estonia: %s" % exc, file=sys.stderr)
        return 1
    if errors:
        for error in errors:
            print(error, file=sys.stderr)
        return 1
    print("Estonia branches: 5 parents, 111 parishes, 2 monasteries; "
          "2 direct Moscow bodies exported for central integration")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
