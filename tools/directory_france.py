#!/usr/bin/env python3
"""Validated directory fragments for canonical Orthodox bodies in France.

This module emits France-only fragments for later merging and never writes a
shared payload.

    python tools/directory_france.py --check
    python tools/directory_france.py --dump
"""

import argparse
import json
import re
import sys
import unicodedata
from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent
CHECKED = "2026-11-15"

EP_PARISHES = "https://mgro.fr/fr/paroisses/"
ROMANIAN_FRANCE = (
    "https://www.mitropolia.eu/fr/site/184/"
    "paroisses-de-france-andorre-et-dom-tom.htm"
)
RUSSIAN_TRADITION = "https://archeveche.eu/lieux/"
KORSUN_API = (
    "https://cerkov-ru.com/api/v1/map/parishes?locale=fr&"
    "bbox=-10%2C40%2C15%2C55&country_code=FRA"
)
ROCOR_DIRECTORY = (
    "https://orthodox-europe.org/wp-content/uploads/2025/12/"
    "2026-Diocese-of-GB-and-W-Europe-Directory-PDF.pdf"
)
SERBIAN_FRANCE = "https://dioceseserbe.org/france/"
BULGARIAN_DIRECTORY = "https://bg-patriarshia.bg/west-eu-diocese-temples"
MACEDONIAN_DIRECTORY = "https://mpee.mk/category/zapadno-evropsko-namesnistvo"
MACEDONIAN_TOTALS = "https://mpee.mk/category/za-eparxijata"
UOKD_DIRECTORY = "https://www.uokd.de/gemeinden"
UOC_PARIS = (
    "https://vzcz.church.ua/2024/04/09/keruyuchij-zaxidnojevropejskim-"
    "vikariatstvom-upc-vidvidav-parafiyu-na-chest-pochajivskoji-ikoni-"
    "bozhoji-materi-v-parizhi/"
)
UOC_BESANCON = (
    "https://uoc-news.church/2023/09/27/keruyuchij-zaxidnojevropejskim-"
    "vikariatstvom-upc-vidvidav-mikolajivsku-parafiyu-u-francuzkomu-"
    "misti-bezanson/"
)
ANTIOCH_VAUCRESSON = "https://agoap.fr/about"
ANTIOCH_NICE = (
    "https://orthodoxesantiochenice.com/"
    "eglise-orthodoxe-dantioche-nice/"
)
ANTIOCH_DIRECTORY = (
    "https://www.antiochpatriarchate.org/en/page/224/"
)


def slug(value):
    value = unicodedata.normalize("NFKD", value)
    value = "".join(char for char in value if not unicodedata.combining(char))
    value = value.lower().replace("’", "'")
    value = re.sub(r"[^a-z0-9]+", "-", value).strip("-")
    return value


def row(row_id, parent, name, local, sources, rank="Parish", kind="parish",
        address=None, site=None):
    value = {
        "id": row_id,
        "parent": parent,
        "kind": kind,
        "rank": rank,
        "name": name,
        "local": local,
        "country": "FR",
        "sources": sources,
    }
    if address:
        value["address"] = address
    if site:
        value["site"] = site
    return value


def parse_rows(parent, prefix, tradition, source, data, details=False):
    rows = []
    for number, raw in enumerate(data.strip().splitlines(), 1):
        parts = [part.strip() for part in raw.split("|")]
        needed = 5 if details else 4
        if len(parts) != needed:
            raise ValueError("invalid %s source row %d" % (prefix, number))
        place, local, rank, address = parts[:4]
        sources = [source]
        if details:
            sources.append(parts[4])
        id_parts = ["fr", prefix, slug(place), slug(local)[:52].rstrip("-")]
        row_id = "-".join(part for part in id_parts if part)
        name = "%s %s in %s" % (tradition, rank, place)
        if sum(1 for item in data.splitlines()
               if item.strip().startswith(place + "|")) > 1:
            dedication = re.sub(
                r"^(Paroisse|Église|Eglise|Chapelle|Communauté|Cathédrale|"
                r"Monastère|Ermitage|Skite|Mission|Filiale)\s+", "", local,
                flags=re.I,
            )
            name += ": " + dedication
        kind = "monastery" if rank in {
            "Monastery", "Skete", "Hermitage", "Monastic Community"
        } else "parish"
        rows.append(row(
            row_id, parent, name, local, sources, rank=rank, kind=kind,
            address=[address] if address else None,
        ))
    return rows


EP_DATA = r"""
Clermont-Ferrand|Paroisse l’Annonciation-de-la-Mère-de-Dieu-et-Saint-Nicolas|Parish|15 rue du Grand Verger, 63260 Aubiat; 11 rue de Lavot, 63130 Royat|https://mgro.fr/fr/paroisse/paroisse-lannonciation-de-la-mere-de-dieu-et-saint-nicolas/
Grenoble|Paroisse Saint-Georges|Parish|3 rue Général Mangin, 38100 Grenoble|https://mgro.fr/fr/paroisse/paroisse-saint-georges/
Lyon|Paroisse l’Annonciation-de-la-Mère-de-Dieu|Parish|45 rue du Père Chevrier, 69007 Lyon; 20 rue Saint Lazare, 69007 Lyon|https://mgro.fr/fr/paroisse/paroisse-lannonciation-de-la-mere-de-dieu-2/
Lyon|Paroisse la-Sainte-Rencontre|Parish|Église Saint-Camille, 76 bis rue des Docks, 69009 Lyon|https://mgro.fr/fr/paroisse/paroisse-la-sainte-rencontre/
Lyon|Paroisse Saint-Alexis-d’Ugine-et-Sainte-Marie-de-Paris|Parish|76 bis rue des Docks, 69009 Lyon|https://mgro.fr/fr/paroisse/paroisse-saint-alexis-dugine-et-sainte-marie-de-paris/
Pont-de-Chéruy|Paroisse Saint-Alexandre|Parish|73 rue du Réveil, 38230 Charvieu-Chavagneux|https://mgro.fr/fr/paroisse/paroisse-saint-alexandre/
Saint-Jean-en-Royans|Paroisse la-Dormition-de-la-Très-Sainte-Mère-de-Dieu|Parish|La Prade, 26190 Saint-Jean-en-Royans|https://mgro.fr/fr/paroisse/paroisse-la-dormition-de-la-tres-sainte-mere-de-dieu/
Saint-Étienne|Paroisse la-Sainte-Trinité|Parish|51 ter rue de la Jomayère, 42100 Saint-Étienne|https://mgro.fr/fr/paroisse/paroisse-la-sainte-trinite-2/
Brest|Paroisse le-Christ-Sauveur|Parish||https://mgro.fr/fr/paroisse/paroisse-le-christ-sauveur/
Quimper|Paroisse Saint-Jacques-le-Frère-du-Seigneur|Parish|Rue de la Chapelle de Cuzon, 29000 Quimper|https://mgro.fr/fr/paroisse/paroisse-saint-jacques-le-frere-du-seigneur/
Rennes|Paroisse Saint-Jean-de-Cronstadt-et-Saint-Nectaire-D’Égine|Parish|Chapelle Saint-François-Xavier, rue Touiller, 35000 Rennes|https://mgro.fr/fr/paroisse/paroisse-saint-jean-de-cronstadt-et-saint-nectaire-degine/
Romorantin-Lanthenay|Chapelle Saint-Roche|Chapel|Place Maubert, 41200 Romorantin-Lanthenay|https://mgro.fr/fr/paroisse/chapelle-saint-roche/
Bernwiller|Chapelle Saint-Grégoire -l’Athonite-et-Sainte-Anastasie-la-Romaine|Chapel|3 rue Louis Werner, 68210 Bernwiller|https://mgro.fr/fr/paroisse/chapelle-saint-gregoire-lathonite-et-sainte-anastasie-la-romaine/
Bischwiller|Paroisse la-Dormition-de-la-Mère-de-Dieu|Parish|33 rue du Maréchal Joffre, 67240 Bischwiller; 9 avenue des Consulats, 67210 Obernai|https://mgro.fr/fr/paroisse/paroisse-la-dormition-de-la-mere-de-dieu/
Metz|Paroisse les-Trois-Saints-Hiérarques|Parish|1 rue des Tanneurs / 2 rue du Champé, 57000 Metz|https://mgro.fr/fr/paroisse/paroisse-les-trois-saints-hierarques/
Nilvange|Paroisse Saint-Nicolas-et-la-Sainte-Trinité|Parish|22 rue de Verdun, 57240 Nilvange|https://mgro.fr/fr/paroisse/paroisse-saint-nicolas-et-la-sainte-trinite/
Strasbourg|Paroisse les-Trois-Saints-Docteurs-et-Hiérarques|Parish|7 rue de la Manufacture des Tabacs, 67000 Strasbourg|https://mgro.fr/fr/paroisse/paroisse-les-trois-saints-docteurs-et-hierarques/
Strasbourg|Paroisse Saint-Jean-Cassien|Parish|Chapelle de la Rencontre, 1 place de l'Hippodrome, 67100 Strasbourg|https://mgro.fr/fr/paroisse/paroisse-saint-jean-cassien/
Lille|Paroisse Saint-Apôtre-Paul|Parish|108 rue Princesse, 59000 Lille|https://mgro.fr/fr/paroisse/paroisse-saint-apotre-paul/
Boulogne-Billancourt|Paroisse Saint-Nicolas|Parish|132 bis rue du Point du Jour, 92100 Boulogne-Billancourt|https://mgro.fr/fr/paroisse/paroisse-saint-nicolas/
Châtenay-Malabry|Paroisse Saints-Pierre-et-Paul|Parish|43 avenue du Plessis, 92290 Châtenay-Malabry|https://mgro.fr/fr/paroisse/paroisse-saints-pierre-et-paul/
Châtenay-Malabry|Paroisse Saints-Raphaël-Nicolas-et-Irène|Parish|15 Petite Voie des Vignes, 92290 Châtenay-Malabry|https://mgro.fr/fr/paroisse/paroisse-saints-raphael-nicolas-et-irene/
Clairefontaine|Paroisse Saint-Alexis-d’Ugine|Parish|10 rue de Rambouillet, 78120 Clairefontaine|https://mgro.fr/fr/paroisse/paroisse-saint-alexis-dugine/
Meudon|Paroisse Saint-Jean-le-Théologien|Parish|45 rue de la Belgique, 92190 Meudon|https://mgro.fr/fr/paroisse/paroisse-saint-jean-le-theologien/
Moisenay|Paroisse Notre-Dame-de-Kazan|Parish|2 chemin du moulin de la roue, 77950 Moisenay|https://mgro.fr/fr/paroisse/paroisse-notre-dame-de-kazan/
Neuilly-sur-Seine|Paroisse le-Saint-Apôtre-et-Évangéliste-Matthieu|Parish|Chapelle de l'Annonciation, 158 avenue Charles de Gaulle, 92200 Neuilly-sur-Seine|https://mgro.fr/fr/paroisse/paroisse-le-saint-apotre-et-evangeliste-matthieu/
Paris|Cathédrale Saint-Stéphane|Cathedral|7 rue Georges Bizet, 75116 Paris|https://mgro.fr/fr/paroisse/cathedrale-saint-stephane/
Paris|Paroisse Géorgienne Sainte-Nino|Parish|6-8 rue de la Rosière, 75015 Paris|https://mgro.fr/fr/paroisse/paroisse-georgienne-sainte-nino/
Paris|Paroisse la-Présentation-du-Sauveur-au-Temple|Parish|100 avenue Maurice Berteaux, 78500 Sartrouville|https://mgro.fr/fr/paroisse/paroisse-la-presentation-du-sauveur-au-temple/
Paris|Paroisse Notre-Dame-du-Signe|Parish|87 boulevard Exelmans, 75016 Paris|https://mgro.fr/fr/paroisse/paroisse-notre-dame-du-signe/
Paris|Paroisse Saints-Constantin-et-Hélène|Parish|2 bis rue Laferrière, 75009 Paris|https://mgro.fr/fr/paroisse/paroisse-saints-constantin-et-helene/
Colombelles|Paroisse Saint-Serge-et-Saint-Vigor|Parish|Rue Raspail, 14460 Colombelles|https://mgro.fr/fr/paroisse/paroisse-saint-serge-et-saint-vigor/
Orgères|Paroisse Saint-Georges-et-Saint-Porphyre|Parish|61230 Orgères|https://mgro.fr/fr/paroisse/paroisse-saint-georges-et-saint-porphyre/
Biarritz|Paroisse la-Protection-de-la-Très-Sainte-Mère-de-Dieu-et-Saint-Alexandre-Nevsky|Parish|8 avenue de l'Impératrice, 64200 Biarritz|https://mgro.fr/fr/paroisse/paroisse-la-protection-de-la-tres-sainte-mere-de-dieu-et-saint-alexandre-nevsky/
Bordeaux|Paroisse la-Présentation-de-la-Vierge-au-Temple|Parish|278 rue du Jardin Public, 33300 Bordeaux|https://mgro.fr/fr/paroisse/paroisse-la-presentation-de-la-vierge-au-temple/
Madaillan|Paroisse Saint-Sophrony-l’Athonite-et-Sainte-Marie-Madeleine|Parish|Église St Barthélémy, 47360 Madaillan|https://mgro.fr/fr/paroisse/paroisse-saint-sophrony-lathonite-et-sainte-marie-madeleine/
Lourdes|Paroisse la-Sainte-Rencontre|Parish|2 avenue Jean Prat, 65100 Lourdes|https://mgro.fr/fr/paroisse/paroisse-la-sainte-rencontre-2/
Montpellier|Paroisse Sainte-Philothée-d’Athènes|Parish|324 avenue de la Gare, 34750 Villeneuve-Lès-Maguelone|https://mgro.fr/fr/paroisse/paroisse-sainte-philothee-dathenes/
Nîmes|Paroisse Saint-Antoine-le-Grand-et-la-Pêche-Miraculeuse|Parish|Chapelle Sainte-Thérèse, 573 chemin de la Planète, Nîmes|https://mgro.fr/fr/paroisse/paroisse-saint-antoine-le-grand-et-la-peche-miraculeuse/
Angers|Paroisse Saint-Dimitri-de-Paris|Parish|16 rue du Prieuré, 49100 Angers|https://mgro.fr/fr/paroisse/paroisse-saint-dimitri-de-paris/
La Chapelle-Achard|Église Saint-Nicolas (chapelle Achard)|Church|Église de la Chapelle Achard|https://mgro.fr/fr/paroisse/eglise-saint-nicolas-chapelle-achard/
Le Mans|Paroisse la-Nativité-du-Christ|Parish|8 rue Clos Margot, 72000 Le Mans|https://mgro.fr/fr/paroisse/paroisse-la-nativite-du-christ/
Nantes|Paroisse Saint-Basile-le-Grand-et-Saint-Alexis-le-Juste|Parish|53 boulevard de la Beaujoire, 44300 Nantes|https://mgro.fr/fr/paroisse/paroisse-saint-basile-le-grand-et-saint-alexis-le-juste/
Aix-en-Provence|Église les-Saints-Archanges|Church|13 rue Bédarrides, 13100 Aix-en-Provence|https://mgro.fr/fr/paroisse/eglise-les-saints-archanges/
Antibes|Paroisse Tous-les-Saints-de-la-Terre-de-Russie-et-Dans-les-Contrées-de-la-Provence|Parish|Avenue du 11 novembre, 06600 Antibes|https://mgro.fr/fr/paroisse/paroisse-tous-les-saints-de-la-terre-de-russie-et-dans-les-contrees-de-la-provence/
Avignon|Paroisse Saints-Côme-et-Damien|Parish|9 rue du Poème du Rhône, 84000 Avignon|https://mgro.fr/fr/paroisse/paroisse-saints-come-et-damien/
Le Cannet|Paroisse Saint-Spyridon-de-Trimythonte|Parish|15 avenue Notre Dame des Anges, 06110 Le Cannet|https://mgro.fr/fr/paroisse/paroisse-saint-spyridon-de-trimythonte/
Marseille|Paroisse l’Annonciation-de-la-Mère-de-Dieu|Parish|12 rue Maurice-Korsec, 13001 Marseille|https://mgro.fr/fr/paroisse/paroisse-lannonciation-de-la-mere-de-dieu/
Marseille|Paroisse la-Dormition-de-la-Mère-de-Dieu|Parish|23 rue de la Grande Armée, 13001 Marseille|https://mgro.fr/fr/paroisse/paroisse-la-dormition-de-la-mere-de-dieu-2/
Marseille|Paroisse Saint-Georges|Parish|16 rue Clapier, 13001 Marseille|https://mgro.fr/fr/paroisse/paroisse-saint-georges-2/
Marseille|Paroisse Saint-Irénée|Parish|1 rue Raoul Ponchon, 13010 Marseille|https://mgro.fr/fr/paroisse/paroisse-saint-irenee/
Nice|Paroisse Saint-Spyridon|Parish|2 avenue Désambrois, 06000 Nice|https://mgro.fr/fr/paroisse/paroisse-saint-spyridon/
Port-Saint-Louis-du-Rhône|Paroisse Saint-Dimitri-et-Sainte-Anne|Parish|1 rue Paul Louis Courrier, 13230 Port-Saint-Louis-du-Rhône|https://mgro.fr/fr/paroisse/paroisse-saint-dimitri-et-sainte-anne/
Port-de-Bouc|Paroisse Sainte-Catherine|Parish|20 rue Paul Vella, 13110 Port-de-Bouc|https://mgro.fr/fr/paroisse/paroisse-sainte-catherine/
Saint-Raphaël|Paroisse Saint-Raphaël-l’Archange|Parish|115 avenue Victor Bontemps, 83700 Saint-Raphaël|https://mgro.fr/fr/paroisse/paroisse-saint-raphael-larchange/
Salin-de-Giraud|Paroisse la-Dormition-de-la-Vierge|Parish|Quartier des Batignolles, 13129 Salin-de-Giraud|https://mgro.fr/fr/paroisse/paroisse-la-dormition-de-la-vierge/
Toulon|Église la-Résurrection|Church|97 rue Centrale, 83000 Toulon|https://mgro.fr/fr/paroisse/eglise-la-resurrection/
Toulon|Paroisse la-Sainte-Trinité|Parish|131 rue Marius Andrieu, 83200 Toulon|https://mgro.fr/fr/paroisse/paroisse-la-sainte-trinite/
"""


ROMANIAN_DATA = r"""
Aix-en-Provence|Paroisse Saint-Jean-Cassien (29 fév.)|Parish|
Alençon|Filiale de la Paroisse Saint-André-et-Sainte-Alexandra (Caen)|Filial|
Amiens|Paroisse de la Résurrection-du-Seigneur|Parish|
Angers|Mission St. Ap. Thomas (6 octobre)|Mission|
Aubigny-sur-Nère|Paroisse en formation|Parish|
Auxerre|Paroisse du Saint Evangéliste Luc (18 octobre) et Saint Germain d’Auxerre (31 juillet)|Parish|
Avignon|Paroisse du Saint grand Martyr Mina et Saint Martin|Parish|
Belfort|Paroisse Saint Antoine le Grand (17 janvier)|Parish|
Besançon|Paroisse de la Protection-de-la-Mère-de-Dieu-et-Saint-Georges (1 oct. et 23 avr.)|Parish|
Bordeaux|Paroisse Saint-Joseph (19 mars)et Saint Jean Maximovici (2 juillet)|Parish|
Brest|Paroisse de la Sainte-et-Vivifiante-Croix (14 sept.)|Parish|
Brive|Paroisse en formation|Parish|
Cabariot|Paroisse St. Eutrope et St. Georges (3 mars et 23 avril)|Parish|
Caen|Paroisse Saint-André-et-Sainte-Alexandra (30 nov. et 21 avr.)|Parish|
Carcassonne|Paroisse Saint Gaudéric|Parish|
Castres|Mission de Castres|Mission|
Chartres|Paroisse de la Protection-de-la-Mère-de-Dieu (1 oct.)|Parish|
Chaumont|Paroisse Saint Joseph le Misericordieux, métropolite de Moldavie|Parish|
Chambéry|Mission de Chambéry|Mission|
Chantonnay|Paroisse du Saint - Apôtre - André et Saint - Philibert - de - Noirmoutier|Parish|
Châteaubriant|Filiale St - Silouane -l’Athonite- Paroisse de Nantes|Filial|
Cherbourg|Communauté Sainte-Cécile (22 nov.)|Community|
Clermont-Ferrand|Paroisse Saint-Nicolas (6 dec.)|Parish|
Dijon|Paroisse Saint Ap et Ev Jean (8 mai) et Saint Benign (1 nov.)|Parish|
Doué-la-Fontaine|Mission de Doué-la-Fontaine|Mission|
Figeac|Paroisse du Saint-Archange-Michel-et-de-Saint-Georges-du-Puy-en-Velay (6 sept. et 29 sept.)|Parish|
Grasse|Paroisse de la Troisième-Invention-du-Chef de Saint-Jean-le-Baptiste|Parish|
Grenoble|Paroisse de Tous-les-Saints|Parish|
Lamballe|Mission - Saints Marth. Brâncoveni et Saint Maxime le Témoin|Mission|
La Rochelle|Mission de La Rochelle|Mission|
La Terrasse|Mission - St. Marin de Tours - St. Alexis d'Ugine|Mission|
Le Havre|Paroisse du Saint-gd-mrt.-Georges et du Saint-Vén.-PaÏssy-de-Neamț|Parish|
Le Mans|Paroisse de la Dormition de la Très Sainte Mère de Dieu et Toujours Vierge Marie et Saint Victor de Le Mans|Parish|
Le Puy-en-Velay|Mission|Mission|
Lille|Paroisse Saint-Jean-le-Baptiste et Sainte Parascève (07 janv. et 14 oct.)|Parish|
Limoges|Paroisse en formation|Parish|
Lorient|Paroisse L’entrée de Notre-Dame dans l’église (21 novembre) et Sainte Xénie de Saint-Pétersbourg (24 janvier)|Parish|
Loudéac|Paroisse St. Mrt. Haralambos|Parish|
Lyon|Paroisse des Saints-Archanges-Michel-et-Gabriel (8 nov.) et Sainte Eugenie (24 decembre)|Parish|
Lyon|Paroisse des Saint Martyrs de Lyon et des Saints - Archanges|Parish|
Manosque|Paroisse Saint-Jean-Cassien (29 février), Saints Martyrs Brâncoveanu (16 août)|Parish|
Marignane|Paroisse Dimanche des Myrophores|Parish|
Marseille|Paroisse des Trois-Saints-Hiérarques (30 jan.)|Parish|
Metz|Paroisse Saint-Martin-et-Saint-Silouane (11 nov. et 24 sept.)|Parish|
Menton|Filiale de la paroisse de Saint Empereurs (voir Nice)|Filial|
Monestier|Paroisse Saint-Nectaire et Sainte-Foy (9 nov. et 6 oct.)|Parish|
Montbrison|Paroisse du Saint-et-glorieux-Martyr-Pantéléimon (27 juillet)|Parish|
Montélimar|Filiale de la paroisse d’Avignon (première dimanche du mois)|Filial|
Montpellier|Paroisse du Saint-Apôtre-André (30 nov.)|Parish|
Morlaix|Paroisse Saint Raphaël de Mytilène et ses compagnons martyrs|Parish|
Mulhouse|Paroisse des Saints-Côme-et-Damien (1 nov.)|Parish|
Nancy|Paroisse des Saints-Apôtres-Pierre-et-Paul (29 juin)|Parish|
Nantes|Paroisse des Saints-Apôtres-Pierre-et-Paul (29 juin)|Parish|
Niort|Paroisse St Nicolas et St Martyr Leger d’Autun (6 déc et 2 oct.)|Parish|
Nice|Paroisse des Saints-Constantin-et-Hélène (21 mai)|Parish|
Nîmes|Paroisse de la Sainte-Rencontre (2 fév.)|Parish|
Paris|Cathédrale Métropolitaine - Église Orthodoxe Roumaine de Paris; Paroisse des Saints-Archanges-Michel-Gabriel-et-Raphaël (8 nov.)|Cathedral|
Clichy et Meudon|Paroisse de la Descente-du-Saint-Esprit|Parish|
Paris|Paroisse Sainte-Parascève-et-Sainte-Geneviève (14 oct. et 3 jan.)|Parish|
Joinville-le-Pont|Paroisse Sainte-Geneviève-et-Saint-Martin (3 jan. et 11 nov.)|Parish|
Sucy-en-Brie|Paroisse Saint-Martin (11 nov.)|Parish|
Trappes|Paroisse Saint-Jean-Cassien-et-Sainte-Geneviève (29 fév. et 3 jan.) Trappes|Parish|
Montreuil|Paroisse de l’Ascension, Synaxe du Saint Jean Baptiste (7 janv.), Saint-Stéphane-le-Grand (2 juil.) - Montreuil|Parish|
La Courneuve et Romainville|Paroisse des Trois-Saints-Hiérarques (30 jan.)|Parish|
Limours|Résidence métropolitaine-Église de la Synaxe-de-la-Mère-de-Dieu-et-du-Saint-Prophète-Elie (26 déc.)|Church|
Palaiseau|Mission Saints-Joachim-et-Anne (9 sept.)|Mission|
Livry-Gargan|Paroisse de l’Exaltation-de-la-Sainte-Croix (14 sept.) et Dimanche de Saint Apôtre Thomas (2ème Dimanche après Pacques) - Livry-Gargan|Parish|
Louveciennes|Paroisse Saint-Germain-et-Saint-Cloud (28 mai et 7 sept.)|Parish|
Auvers-sur-Oise|Paroisse Saint Anthime l’Ibère - Auvers sur Oise|Parish|
Villeneuve-Saint-Georges|Paroisse de la Sainte-Trinité-et-du-Saint-mégalomarthyr-Georges|Parish|
Fontainebleau|Paroisse Les Saints Calinique de Cernica et Jean Maximovici, Fontainebleau|Parish|
Champigny-sur-Marne|Paroisse - La Sainte Rencontre de notre Seigneur Jésus-Christ - Champigny sur Marne|Parish|
Drancy|Paroisse St glorieux et gd-mart. Dimitrios le Myroblyte et St Ap. et Ev. Jean - Drancy|Parish|
Cachan|Paroisse - St Ap. et Ev. Jean - Cachan|Parish|
Aulnay-sous-Bois|Paroisse - Saint Spyridon - Aulnay-sous-Bois|Parish|
Villemomble|Paroisse - 1ère et 2ème Inventions du Chef de st Jean Baptiste; (24 février) - Villemomble|Parish|
Meaux-Montry|Paroisse Saint Marth. Sebasten - Meaux-Montry|Parish|
La Ferté-sous-Jouarre|Paroisse St. Jean Baptiste - La Ferte sous Jouarre|Parish|
Eaubonne|Paroisse en formation - Eaubonne|Parish|
Perpignan|Paroisse Saint Spyridon (12 dec.)|Parish|
Poitiers-Châtellerault|Filiale de la paroisse de Chantonnay|Filial|
Reims-Châlons-en-Champagne|Paroisse des Saints-Apôtres-Pierre-et-Paul (29 juin)|Parish|
Rennes|Paroisse des Saints-et-justes-ancêtres-de-Dieu-Joachim-et-Anne|Parish|
Rodez|Paroisse St. André et St. Tarcisse|Parish|
Rouen|Paroisse Saint-Silouane et Saint Victrice de Rouen (24 septembrie)|Parish|
Saint-Lizier|Paroisse Saint Seraphim de Sarov et Saint Isaac le Syrien|Parish|
Saint-Nazaire|Filiale de Nantes|Filial|
Saintes|Paroisse Saint-Eutrope-et-Saint-Georges|Parish|
Sarreguemines|Mission Saint Jean Climaque|Mission|
Strasbourg|Paroisse de Saint-Jean-le-Baptiste (24 juin)|Parish|
Tarbes-Lourdes-Pau|Paroisse Maica Domnului - Izvorul Vieții|Parish|
Thionville|Paroisse en fromation - Saint Jean Chrysostome|Parish|
Toulon|Paroisse St empereur Constantin le Grand et sa mère Hélène et Ste Agathe (5 février)|Parish|
Toulouse|Paroisse de la Protection-de-la-Mère-de-Dieu (1 oct.)|Parish|
Tours|Paroisse de Saint-Nectaire-d’Egine (9 nov.)|Parish|
Troyes|Paroisse Saint-Georges (23 avril)|Parish|
Vernon|Paroisse Sainte-Catherine-d’Alexandrie|Parish|
Vichy|Paroisse de la Transfiguration (6 août)|Parish|
Bastia, Ajaccio et Ghisonaccia|Paroisse de Saint-Grégoire-le-Théologien et de-la-Sainte-marthyre-Philothée-d’Argeș|Parish|
Le Gosier, Guadeloupe|Paroisse Saint-Georges (23 avr.)|Parish|
Nice|Paroisse de St Nicolas et de ste Alexandra (19 décembre et 06 mai)|Parish|
"""


ROMANIAN_MONASTIC_DATA = r"""
Limours|Communauté monastique de la Protection de la Mère de Dieu (1 octobre)|Monastic Community|1 boulevard du Général Leclerc, 91470 Limours
Cantauque|Communauté monastique de la Théotokos et de st Martin (25 mars et 11 novembre)|Monastic Community|
Castellane|Skyte de la St. Jean Casien (29 février)|Skete|
Godoncourt|Monastère la Nativité de la Mère de Dieu (8 septembre)|Monastery|116 rue Haute, 88410 Godoncourt
Rosiers|Communauté monastique de l’Annonciation (25 mars)|Monastic Community|
Kerbénéat|Communauté monastique du St Isaac le Syrien (28 janvier)|Monastic Community|
La Malvialle|Communauté monastique de l’ Exaltation de la Sainte Croix (14 septembre)|Monastic Community|
Le Ricardès|Communauté monastique de la Nativité de la Mère de Dieu (8 septembrie)|Monastic Community|
Le Vilar|Communauté monastique de la Dormition de la Mère de Dieu (15 août)|Monastic Community|Prieuré Santa Maria del Vilar, 66740 Villelongue dels Monts
Porquerolles|Communauté monastique Saint Marie L'Egyptienne (1 avril) et St Denys le Petit (1er septembre)|Monastic Community|Fort de la Repentance, 83400 Île de Porquerolles
Saint-Michel-la-Forêt|Communauté monastique des Stes Odile et Théodora de Sihla (13 décembre et 7 août)|Monastic Community|
Sauvagnac|Communauté monastique de l’Éntrée de la Mère de Dieu au Temple et du St Elie (21 novembre et 20 juillet)|Monastic Community|
"""


RUSSIAN_TRADITION_DATA = r"""
Paris|Cathédrale Saint-Alexandre-Nevsky|Cathedral||https://archeveche.eu/lieux/
Brest|Communauté de la Théophanie|Community||https://archeveche.eu/lieux/communaute-de-la-theophanie-fr/
Béthune|Communauté de Sainte-Clotilde-et-Saint-Vladimir|Community||https://archeveche.eu/lieux/communaute-de-sainte-clothilde-et-saint-vladimir/
Saintines|Communauté des Saints Dimitri et Marie et leurs compagnons|Community||https://archeveche.eu/lieux/communaute-des-saints-dimitri-et-marie-et-leurs-compagnons/
Paris|Communauté moldave de l’Annonciation-de-la-Mère-de-Dieu (crypte de la cathédrale)|Community||https://archeveche.eu/lieux/communaute-moldave-de-lannonciation-de-la-mere-de-dieu-crypte-de-la-cathedrale-fr/
Villeneuve-Saint-Georges|Communauté Monastique du Saint-Archange-Michel|Monastic Community||https://archeveche.eu/lieux/communaute-monastique-du-saint-archange-michel/
La Seyne-sur-Mer|Communauté orthodoxe de tradition russe de la Sainte-Résurrection|Community||https://archeveche.eu/lieux/communaute-orthodoxe-de-tradition-russe-de-la-sainte-resurrection-2/
Orange|Communauté Saint-Eutrope d’Orange|Community||https://archeveche.eu/lieux/communaute-saint-eutrope-dorange/
Paris|Église de la Présentation-de-la-Vierge-au-Temple|Church||https://archeveche.eu/lieux/eglise-de-la-presentation-de-la-vierge-au-temple/
Grenoble|Église de la Résurrection-du-Christ|Church||https://archeveche.eu/lieux/eglise-de-la-resurrection-du-christ/
Châlette-sur-Loing|Église de la Sainte-Trinité|Church||https://archeveche.eu/lieux/eglise-de-la-sainte-trinite/
Paris|Église de Saint-Séraphin-de-Sarov et de la Protection-de-la-Mère-de-Dieu|Church||https://archeveche.eu/lieux/eglise-de-saint-seraphin-de-sarov-et-de-la-protection-de-la-mere-de-dieu/
Asnières|Église du Christ-Sauveur|Church||https://archeveche.eu/lieux/eglise-du-christ-sauveur/
Chaville|Église Notre-Dame-Souveraine et Saint-Silouane|Church||https://archeveche.eu/lieux/eglise-notre-dame-souveraine-et-saint-silouane/
Nantes|Église orthodoxe de La Résurrection de Nantes et Pays de la Loire|Church||https://archeveche.eu/lieux/eglise-orthodoxe-la-resurrection/
Belfort|Église orthodoxe de la Résurrection du Christ|Church||https://archeveche.eu/lieux/eglise-orthodoxe-de-la-resurrection-du-christ/
Le Creusot|Église Saint-Alexandre-Nevsky|Church||https://archeveche.eu/lieux/eglise-saint-alexandre-nevsky/
Cormeilles-en-Parisis|Église Saint-Nicolas|Church||https://archeveche.eu/lieux/eglise-saint-nicolas-2/
Lille|Église Saint-Nicolas|Church||https://archeveche.eu/lieux/eglise-saint-nicolas-3/
Toulouse|Église Saint-Nicolas-le-Thaumaturge|Church||https://archeveche.eu/lieux/eglise-saint-nicolas/
Chelles|Église Saint-Séraphin-de-Sarov|Church||https://archeveche.eu/lieux/eglise-saint-seraphin-de-sarov/
Saint-Hilaire-le-Grand|Ermitage de Tous-les-Saints-de-la-Terre-Russe|Hermitage||https://archeveche.eu/lieux/ermitage-de-tous-les-saints-de-la-terre-russe/
Digne|Ermitage Saint-Jean|Hermitage||https://archeveche.eu/lieux/ermitage-saint-jean/
Lissac|Fraternité Orthodoxe Saint-Michel|Community||https://archeveche.eu/lieux/fraternite-orthodoxe-saint-michel/
Saint-Mars-de-Locquenay|Monastère Saint-Silouane|Monastery||https://archeveche.eu/lieux/monastere-saint-silouane/
Sainte-Geneviève-des-Bois|Paroisse de la Dormition-de-la-Mère-de-Dieu|Parish||https://archeveche.eu/lieux/paroisse-de-la-dormition-de-la-mere-de-dieu/
Le Lamentin, Martinique|Paroisse de la Mère de Dieu « Axion-Estin »|Parish|1442 Bois Carré, 97213 Le Lamentin, Martinique|https://archeveche.eu/lieux/paroisse-de-la-mere-de-dieu-axion-estin/
Saint-Prix|Paroisse de la Rencontre-du-Christ|Parish||https://archeveche.eu/lieux/paroisse-de-la-rencontre-du-christ/
Paris|Paroisse de la Trinité (crypte de la cathédrale)|Parish||https://archeveche.eu/lieux/paroisse-de-la-trinite-crypte-de-la-cathedrale/
Montpellier|Paroisse de Sainte-Hélène et de la Sainte-Croix|Parish||https://archeveche.eu/lieux/paroisse-de-sainte-helene-et-de-la-sainte-croix/
Olivet|Paroisse du Christ-Sauveur|Parish||https://archeveche.eu/lieux/du-christ-sauveur/
Vichy|Paroisse du Christ-Sauveur et de la Dormition|Parish||https://archeveche.eu/lieux/paroisse-du-christ-sauveur-et-de-la-dormition/
Poitiers|Paroisse la Trinité et Saint-Hilaire-de-Poitiers|Parish||https://archeveche.eu/lieux/paroisse-la-trinite-et-saint-hilaire-de-poitiers/
Compiègne|Paroisse Notre-Dame-de-Toute-Protection|Parish||https://archeveche.eu/lieux/communaute-notre-dame-de-toute-protection-de-loise/
L’Honor-de-Cos|Paroisse Notre-Dame-du-Prompt-Secours|Parish||https://archeveche.eu/lieux/paroisse-notre-dame-du-prompt-secours/
Angers|Paroisse Orthodoxe de l’Annonciation|Parish||https://archeveche.eu/lieux/communaute-de-lannonciation/
Audes|Paroisse Orthodoxe francophone Saint Marien en Bourbonnais|Parish||https://archeveche.eu/lieux/saint-marien-en-bourbonnais/
Vaux-sur-Mer|Paroisse orthodoxe Saint-Étienne en pays royannais|Parish||https://archeveche.eu/lieux/communaute-orthodoxe-saint-etienne/
Rochecorbon|Paroisse orthodoxe Saint-Martin-le-Miséricordieux-et-Saint-Georges-le-Victorieux|Parish||https://archeveche.eu/lieux/eglise-saint-martin-le-misericordieux/
Plérin|Paroisse Saint Brieuc - Plérin|Parish||https://archeveche.eu/lieux/communaute-saint-brieuc-plerin/
Plumaudan|Paroisse Saint Brieuc - Plumaudan|Parish||https://archeveche.eu/lieux/communaute-saint-brieuc/
Marseille|Paroisse Saint-Hermogène|Parish||https://archeveche.eu/lieux/paroisse-saint-hermogene/
Cannes|Paroisse Saint-Michel Archange|Parish||https://archeveche.eu/lieux/paroisse-saint-michel-archange/
Saint-André-les-Vergers|Paroisse Saint-Nicolas|Parish||https://archeveche.eu/lieux/paroisse-saint-nicolas/
Paris|Paroisse Saint-Serge-de-Radonège|Parish||https://archeveche.eu/lieux/paroisse-saint-serge-de-radonege/
Lannion|Paroisse Sainte-Anne|Parish||https://archeveche.eu/lieux/communaute-sainte-anne/
Saint-Julien-des-Points|Skite Sainte-Foy|Skete||https://archeveche.eu/lieux/skite-sainte-foy/
"""


KORSUN_DATA = r"""
Marseille|Paroisse Notre-Dame-de-Kazan (Marseille)|Parish|1 boulevard Mont Rose, 13008 Marseille
Corse|Communauté diocésaine en Corse|Community|
Hauteville-sur-Mer|Chapelle Notre-Dame d'Ivéron à Hauteville-sur-Mer|Chapel|La Brasserie, Hauteville-sur-Mer, Normandie
Cannes|Communauté diocésaine Saint-Michel-Archange à Cannes|Community|3 impasse des deux Eglises, 06400 Cannes
Strasbourg|Eglise stauropégiaque de Tous les Saints à Strasbourg|Church|106 rue du Général Conrad, 67000 Strasbourg
Clermont-Ferrand|Paroisse Saint-Jean-Apôtre|Community|63 rue Pablo Picasso, Clermont-Ferrand
Chavenon|Eglise Saints-Barsanuphe-et-Jean à Chavenon|Church|03440 Chavenon
Perpignan|Paroisse Saint-Jean à Perpignan|Parish|11 rue Claude Monet, Perpignan
Ugine|Paroisse Saint-Nicolas à Ugine|Church|323 route de la Cry, Combloux
Grassac|Monastère féminin Notre-Dame-de-Chersonèse à Grassac|Monastery|10 chemin des noisetiers, Doumérac, 16380 Grassac
Nice|Cathédrale Saint-Nicolas (Nice)|Cathedral|avenue Nicolas II, 06000 Nice
Saint-Nicolas-de-Port|Communauté diocésaine Saint-Nicolas à Saint-Nicolas-de-Port|Community|1 rue des Trois Pucelles, 54210 Saint-Nicolas-de-Port
Vanves|Paroisse Sainte-Trinité (Vanves)|Church|16 rue Michel-Ange, Vanves
Strasbourg|Paroisse Saint-Grégoire-Palamas et Sainte-Attale (Strasbourg)|Parish|6 rue du Coq, 67000 Strasbourg
Vézelay|Paroisse Saint-Etienne et Saint-Germain (Vézelay)|Parish|Maison Romane, rue du Couvent, 89450 Vézelay
Valence|Communauté diocésaine à Valence|Community|St Pierre, place de la Liberté, 26500 Bourg-lès-Valence
Montpellier|Communauté diocésaine à Montpelier|Community|310 rue Léon Blum, 34000 Montpellier
Paris|Communauté diocésaine Sainte-Hélène à Paris|Community|92 rue Saint Denis, 75001 Paris
Puyloubard|Chapelle du Sauveur (Puyloubard)|Chapel|Puyloubard, Beaussac, 24340 Mareuil
Arras|Communauté Notre-Dame-Portaïtissa (Arras)|Community|4 rue du Vivier, 62000 Arras
Paris|Église cathédrale de Trois-Saints-Hiérarques à Paris|Cathedral|5 rue Pétel, 75015 Paris
Paris|La cathédrale de la Sainte Trinité à Paris|Cathedral|1 quai Branly, 75007 Paris
Montgeron|Eglise Saint-Séraphin de Sarov à Montgéron|Church|Rue du Moulin de Senlis, 91230 Montgeron
Limoges|Paroisse Notre-Dame du Prompt Secours à Limoges|Community|30 rue François Perrin, 87000 Limoges
Paris|Paroisse Notre-Dame-Joie-des-Affligés et Sainte-Geneviève (Paris)|Parish|4 rue Saint-Victor, 75005 Paris
Lyon|Paroisse de la Protection-de-la-Mère-de-Dieu (Lyon)|Parish|146 rue Sully, Lyon
Contrexéville|Communauté Saint-Prince-Vladimir-et-Sainte-Marie-Madeleine à Contrexéville|Community|rue de la Victoire et rue du Shah de Perse, 88140 Contrexéville
Chevrier|Communauté Saint-Martin-de-Tours à Chervier|Community|chemin de Pré-Benoît, 74520 Chevrier
Clamart|Paroisse Saints-Constantin-et-Hélène (Clamart)|Parish|4 bis rue Henry, 92140 Clamart
Sainte-Geneviève-des-Bois|Chapelle de la Maison russe (Sainte-Geneviève-des-Bois)|Chapel|Maison russe, rue de la Cossonnerie
Clamart|Chapelle du Saint-Esprit (Clamart)|Chapel|83 rue du Moulin-de-Pierre, 92140 Clamart
Saint-Louis|Paroisse Saint-Nicolas à Saint-Louis|Church|Alsace
Marcenat|Monastère féminin Notre-Dame-du-Signe à Marcenat|Monastery|La Traverse, 15190 Marcenat
Le Mesnil-Saint-Denis|Ermitage (skit) du Saint-Esprit au Mesnil-Saint-Denis|Skete|7 avenue des Bruyères, 78320 Le Mesnil-Saint-Denis
Épinay-sous-Sénart|Chapelle Saints-Martin-et-Genevieve à Épinay-sous-Sénart|Chapel|4 rue Sainte-Geneviève, Épinay-sous-Sénart
Épinay-sous-Sénart|Chapelle Saint-Martin-Sainte-Geneviève du Séminaire (Epinay-sous-Sénart)|Chapel|4 rue Sainte-Geneviève, Épinay-sous-Sénart
Bordeaux|Église Saint-Séraphim|Church|15 rue Saint François-Xavier, Bruges, 33520 Bordeaux
"""


ROCOR_DATA = r"""
Annecy|Communauté de Tous les Saints|Community|12 place Notre Dame, Annecy
Vichy|Eglise Saints Pierre et Paul|Church|Les Rochelles, Périgny, 03120 Lapalisse
Cannes|Eglise Archange Michel|Church|13 rue de la Plage, Mandelieu-la-Napoule
Lyon|Eglise Saint Jean le Russe|Church|77 cours Eugénie, Lyon
Marseille|Eglise Saint Georges|Church|16 rue Clapier, Marseille
Meudon|Résurrection du Christ|Church|8 rue des Bigots, Meudon
Menton|Mère de Dieu Joie de tous les Affligés|Church|14 rue Paul-Morillot, Menton
Nilvange|Sainte-Trinité et Saint Nicolas|Church|22 rue de Verdun, Nilvange
Paris|Tous les Saints glorifiés en Terre Russe|Church|19 rue Claude Lorrain, Paris
Pau|Saint Jean de Shanghai|Community|19 rue du Gabizos, Coarraze
Pau|Saint Alexandre Nevsky|Church|18 rue Jean-Réveil, Pau
Rouen|Saint Jean de Shanghai|Church|8 rue de l’Industrie, Rouen
"""


SERBIAN_DATA = r"""
Paris|Paroisse Saint-Sava|Cathedral|3 rue du Simplon, 75018 Paris
Bondy|AC orthodoxe serbe Bienheureuse Mère Parascève|Community|224 avenue du Rosny, 93140 Bondy
Asnières|AC orthodoxe St Jean de San Francisco|Community|2 rue Roger Campestre, 92600 Asnières
Pierrefitte-sur-Seine|Saint Basile d’Ostrog Métokhion orthodoxe serbe|Metochion|85 rue Parmentier, 93380 Pierrefitte-sur-Seine
Strasbourg|Paroisse orthodoxe serbe Saint Georges|Parish|2 rue de la Tour, 67200 Strasbourg
Mulhouse|Paroisse orthodoxe serbe St Archange Michel|Parish|9 rue d’Illzach, 68100 Mulhouse
Valmont|Paroisse de l’Eglise serbe orthodoxe Saint Lazare|Parish|Rue de la Furst, 57730 Valmont
Nancy|Paroisse orthodoxe serbe Saint Nicolas|Parish|1 quai de la Bataille, 54000 Nancy
Betting|Paroisse Saint Prince Lazare|Parish|98 route de Betting, 57800 Betting
Dijon|Paroisse orthodoxe serbe de la Ste Résurrection du Christ|Parish|Chapelle St François d’Assise, 20 boulevard de l’Ouest, 21000 Dijon
Chalon-sur-Saône|AC orthodoxe St Césaire et St Marcel|Community|22 rempart St Vincent, 71100 Chalon-sur-Saône
Lougres|Paroisse orthodoxe serbe Sainte Petka|Parish|Chapelle St Pierre, rue de la Bonne Fontaine, 25260 Lougres
Besançon|Paroisse orthodoxe serbe Saint Basile d’Ostrog|Parish|28a chemin des Quatrouillots, 25000 Besançon
Besançon|AC orthodoxe St Etienne et Ste Marie|Community|1 rue du Grand Charmont, 25000 Besançon
Lyon|Paroisse orthodoxe Saints Cyrille et Méthode|Parish|6B rue Hugues Guérin, 69008 Lyon
Ayze|Paroisse orthodoxe serbe de la Pentecôte|Parish|Eglise St Pierre, 74130 Ayze
Vitrolles|Paroisse orthodoxe serbe Nativité de la Mère de Dieu|Parish|Rue Henri Bosco, 13127 Vitrolles
Nice|AC orthodoxe de la Dormition|Community|3 rue Fodéré, 06300 Nice
Fontaine|Monastère de la Nativité de la Mère de Dieu|Monastery|Lieu-dit Bois-Salair, 53100 Fontaine
Castelsarrasin|AC orthodoxe St Nicolas d’Ohrid|Community|476 chemin des Dantous, 82100 Castelsarrasin
Lectoure|Monastère Sts Clair et Maurin - Basilique St Gény|Monastery|Route de Fleurance, 32700 Lectoure
Toulouse|Eglise St Saturnin|Church|108 avenue de Lavaur, 31500 Toulouse
Bordeaux|Eglise Sts Martial et Eutrope|Church|35 rue Peyronnet, 33800 Bordeaux
Tarbes|Eglise St Aventin|Church|112 avenue Aristide-Briand, 65000 Tarbes
Lille|AC Orthodoxe Saint Roi Milutin|Community|
Uchon|MONASTÈRE Centre orthodoxe ST HILAIRE - ST JEAN DAMASCÈNE|Monastery|
Chapey|ERMITAGE DE LA THÉOPHANIE|Hermitage|Colline de Chapey, 71190 Broye
Nérac|Eglise Archange Michel - Ste Foy|Church|Rue Faudauas, 47600 Nérac
Dénat d’Albi|Eglise Prophète Elie - St Denis|Church|Boulevard extérieur, 81120 Dénat d’Albi
"""


BULGARIAN_DATA = r"""
Paris|БПЦО "Св. патриарх Евтимий Търновски" - гр. Париж|Church Community|1 rue de la Croix Moreaux, Paris
Strasbourg|БПЦО "Св. Кирил и Методий" - гр. Страсбург|Church Community|9 rue du Petit-Marais, Strasbourg
Lyon|БПЦО "Св. Софроний Врачански" - гр. Лион|Church Community|
Lille|БПЦО "Св.св. ап. Петър и Павел" - гр. Лил|Church Community|
"""


ROWS = {
    "ep-france": parse_rows(
        "ep-france", "ep", "Greek Orthodox", EP_PARISHES, EP_DATA,
        details=True,
    ),
    "ro-western-europe": (
        parse_rows(
            "ro-western-europe", "ro", "Romanian Orthodox",
            ROMANIAN_FRANCE, ROMANIAN_DATA,
        ) +
        parse_rows(
            "ro-western-europe", "ro-monastic", "Romanian Orthodox",
            "https://www.mitropolia.eu/fr/site/207/"
            "communautes-monastiques-de-france.htm",
            ROMANIAN_MONASTIC_DATA,
        )
    ),
    "ru-archdiocese-western-europe": parse_rows(
        "ru-archdiocese-western-europe", "russian-tradition",
        "Russian Tradition Orthodox", RUSSIAN_TRADITION,
        RUSSIAN_TRADITION_DATA, details=True,
    ),
    "ru-korsun": parse_rows(
        "ru-korsun", "korsun", "Russian Orthodox", KORSUN_API,
        KORSUN_DATA,
    ),
    "ru-great-britain-and-western-europe-rocor": (
        parse_rows(
            "ru-great-britain-and-western-europe-rocor", "rocor",
            "ROCOR", ROCOR_DIRECTORY, ROCOR_DATA,
        ) + [
            row(
                "fr-rocor-provemonte-lesna-convent",
                "ru-great-britain-and-western-europe-rocor",
                "Lesna Icon of the Mother of God Convent in Provemont",
                "Couvent de la Sainte Vierge de Lesna",
                ["https://directory.synod.com/listings/",
                 "https://www.synod.com/synod/en/rocor/enmonasteries.html"],
                rank="Monastery", kind="monastery",
                address=["1 rue du Moulin", "Provemont, 27150 Etrepagny"],
            ),
        ]
    ),
    "sr-western-europe": parse_rows(
        "sr-western-europe", "sr", "Serbian Orthodox", SERBIAN_FRANCE,
        SERBIAN_DATA,
    ),
    "bg-western-central-europe": parse_rows(
        "bg-western-central-europe", "bg", "Bulgarian Orthodox",
        BULGARIAN_DIRECTORY, BULGARIAN_DATA,
    ),
    "ep-ukrainian-western-europe": [
        row(
            "fr-ep-ukrainian-paris-apostle-simon",
            "ep-ukrainian-western-europe",
            "Holy Apostle Simon Ukrainian Orthodox Parish in Paris",
            "Paris - Gemeinde des Hl. Apostel Simon",
            [UOKD_DIRECTORY],
            address=["6 rue de Palestine", "75019 Paris"],
        ),
    ],
    "ukraine-uoc": [
        row(
            "fr-uoc-villejuif-pochaev-icon",
            "ukraine-uoc",
            "Pochaev Icon of the Mother of God Ukrainian Orthodox Parish in Paris",
            "парафія на честь Почаївської ікони Божої Матері в м. Париж",
            [UOC_PARIS],
            address=["52 avenue Louis Aragon", "94800 Villejuif"],
        ),
        row(
            "fr-uoc-besancon-saint-nicholas",
            "ukraine-uoc",
            "St Nicholas Ukrainian Orthodox Parish in Besançon",
            "Свято-Миколаївська парафія УПЦ у м. Безансон",
            [UOC_BESANCON],
            address=["2 rue du Passeur", "25000 Besançon"],
        ),
    ],
    "an-france": [
        row(
            "fr-an-vaucresson-saint-helen",
            "an-france", "St Helen Antiochian Orthodox Parish in Vaucresson",
            "Paroisse Orthodoxe Sainte-Hélène",
            [ANTIOCH_VAUCRESSON],
            address=["12 avenue de la Celle Saint-Cloud", "92420 Vaucresson"],
        ),
        row(
            "fr-an-tours-saint-gregory",
            "an-france", "St Gregory of Tours Antiochian Orthodox Parish",
            "Paroisse orthodoxe Saint Grégoire de Tours",
            ["https://eglise371.wixsite.com/saint-gregoire37"],
        ),
        row(
            "fr-an-nice-saint-ignatius",
            "an-france", "St Ignatius the God-Bearer Antiochian Orthodox Parish in Nice",
            "Paroisse orthodoxe d'Antioche Saint Ignace le Théophore",
            [ANTIOCH_NICE],
            address=["249 avenue Sainte-Marguerite", "06200 Nice"],
        ),
        row(
            "fr-an-villardonnel-burning-bush-monastery",
            "an-france", "Burning Bush Monastery in Villardonnel",
            "Monastère du Buisson Ardent",
            [ANTIOCH_DIRECTORY], rank="Monastery", kind="monastery",
            address=["La Barthe Haute", "11600 Villardonnel"],
        ),
    ],
    "mk-europe": [
        row(
            "fr-mk-paris-cyril-methodius",
            "mk-europe", "Sts Cyril and Methodius Macedonian Orthodox Church Community in Paris",
            "МПЦО „Св. Кирил и Методиј“ - Париз Франција",
            [MACEDONIAN_DIRECTORY, MACEDONIAN_TOTALS],
            rank="Church Community",
        ),
    ],
}


EXPECTED = {
    "an-france": 4,
    "bg-western-central-europe": 4,
    "ep-france": 58,
    "ep-ukrainian-western-europe": 1,
    "mk-europe": 1,
    "ro-western-europe": 113,
    "ru-archdiocese-western-europe": 47,
    "ru-great-britain-and-western-europe-rocor": 13,
    "ru-korsun": 37,
    "sr-western-europe": 29,
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
        raise ValueError("duplicate France source row id")
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
                if not re.fullmatch(r"[a-z0-9]+(?:-[a-z0-9]+)*", row_id):
                    raise ValueError("invalid France row id: %s" % row_id)
                if item.get("kind") not in {"parish", "monastery"}:
                    raise ValueError("%s has unsupported kind" % row_id)
                if item.get("country") != "FR":
                    raise ValueError("%s is outside France" % row_id)
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
                raise ValueError("France child rows have unresolved parents")
        payloads[parent] = {
            "v": 1,
            "parent": parent,
            "country": "FR",
            "rows": rows,
        }
    actual = {parent: len(payload["rows"])
              for parent, payload in payloads.items()}
    if actual != EXPECTED:
        raise ValueError("France parent counts changed: %r" % actual)
    if len(ENGLISH_NAMES) != sum(EXPECTED.values()):
        raise ValueError("France English name coverage changed")
    return payloads


def manifest(payloads=None):
    payloads = payloads or build()
    return {
        parent: {
            "url": "/data/directory/%s.v1.json" % parent,
            "count": len(payload["rows"]),
            "country": "FR",
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
        errors.append("France row IDs already in directory spine: %s" %
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
        print("directory France: %s" % exc, file=sys.stderr)
        return 1
    if errors:
        for error in errors:
            print(error, file=sys.stderr)
        return 1
    if args.dump:
        print(json.dumps(payloads, ensure_ascii=False, indent=2))
        return 0
    print("France branches: %d rows" % sum(EXPECTED.values()))
    for parent, count in sorted(EXPECTED.items()):
        print("%s: %d" % (parent, count))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
