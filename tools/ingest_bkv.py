#!/usr/bin/env python3
"""Ingest complete public domain BKV editions from the University of Fribourg.

The Bibliothek der Kirchenväter site publishes downloadable EPUB files for
many older German and French editions. Each catalogue entry below names the
exact BKV version page and the known number of divisions. The builder fetches
the EPUB, keeps every division and its notes, removes only scan page markers,
and stops if the source structure or normalized text has changed.

BKV's copyright notice says, to the editor's knowledge, that its texts are no
longer protected by copyright and may be used freely. These historical
editions are public domain. The source and digitizer remain in every record.

    python3 tools/ingest_bkv.py --check
    python3 tools/ingest_bkv.py --write
    python3 tools/ingest_bkv.py --write-files-only --only cyprian-lords-prayer-de
    python3 tools/ingest_bkv.py --check --only polycarp-philippians-de
"""
import argparse
import hashlib
import html
import io
import json
import re
import sys
import tempfile
import urllib.parse
import urllib.request
import zipfile
from pathlib import Path
import xml.etree.ElementTree as ET


ROOT = Path(__file__).resolve().parent.parent
OUTDIR = ROOT / "data" / "library"
INDEX = OUTDIR / "works-index.json"
CACHE = Path(tempfile.gettempdir()) / "plithos-bkv"
CACHE.mkdir(parents=True, exist_ok=True)

UA = "Mozilla/5.0 (compatible; PlithosLibraryBuilder/1.0; +https://plithos.org)"
DIGITIZED = "University of Fribourg, Bibliothek der Kirchenväter"
RIGHTS = "Public domain"
RIGHTS_URL = "https://bkv.unifr.ch/de/about/copyrights"
BKV_LANGUAGE_NAMES = {
    "de": "deutsch",
    "fr": "französisch",
}

# The digest is calculated from the normalized headings and full unit text.
# It therefore catches a shortened download, a missing note, or source drift,
# while permitting the EPUB container itself to be regenerated.
CATALOGUE = [
    {
        "work_id": "polycarp-philippians-de",
        "edition_of": "polycarp-to-the-philippians",
        "url": "https://bkv.unifr.ch/works/cpg-1040/versions/der-brief-des-polykarp-von-smyrna-an-die-gemeinde-von-philippi-bkv/divisions",
        "language": "de",
        "title": "Der Brief des Polykarp von Smyrna an die Gemeinde von Philippi",
        "author": "St Polycarp of Smyrna",
        "date": "c. 110",
        "translator": "Franz Zeller",
        "pub_year": 1918,
        "source": "Die Apostolischen Väter (Bibliothek der Kirchenväter, 1. Reihe, Band 35), pp. 163-170",
        "source_class": "patristic",
        "description": "Franz Zeller's 1918 German translation of Polycarp's letter to the church at Philippi.",
        "bkv_version": "Der Brief des Polykarp von Smyrna an die Gemeinde von Philippi (BKV)",
        "metadata_markers": ("übersetzt von Franz Zeller", "Band 35",
                             "München 1918", "163-170"),
        "units": 14,
        "first_heading": "1. Kap. Anerkennung der Nächstenliebe und des Glaubens der Philipper.",
        "last_heading": "14. Kap. Empfehlungen und Grüße.",
        "digest": "3b9689df45b9c73d0ab080d15fb85245dca815b0a3365bf17cbba1d427f182b4",
    },
    {
        "work_id": "epistle-to-diognetus-de",
        "edition_of": "epistle-to-diognetus",
        "url": "https://bkv.unifr.ch/works/cpg-1112/versions/brief-an-diognet-bkv/divisions",
        "language": "de",
        "title": "Brief an Diognet",
        "author": "Mathetes",
        "date": "2nd century",
        "translator": "Gerhard Rauschen",
        "pub_year": 1913,
        "source": "Frühchristliche Apologeten und Märtyrerakten, Band I (Bibliothek der Kirchenväter, 1. Reihe, Band 12), pp. 161-173",
        "source_class": "patristic",
        "description": "Gerhard Rauschen's 1913 German translation of the Epistle to Diognetus.",
        "bkv_version": "Brief an Diognet (BKV)",
        "metadata_markers": ("übersetzt von Dr. Gerhard Rauschen",
                             "Band 12", "München 1913", "161-173"),
        "units": 12,
        "first_heading": "1. Veranlassung und Inhalt des Briefes.",
        "last_heading": "12. Der letzte Prüfstein der Erkenntnis ist das Leben.",
        "digest": "666bfd0cc1f819993dab2d550c4381ddfe0ba9a8fd1b8d0c60a10c01b7be62c2",
    },
    {
        "work_id": "scillitan-martyrs-de",
        "edition_of": "scillitan-martyrs",
        "url": "https://bkv.unifr.ch/works/-28x/versions/das-leiden-des-scilitanischen-martyrer-bkv/divisions",
        "language": "de",
        "title": "Das Leiden des Scilitanischen Märtyrer",
        "author": "The proconsular record",
        "date": "180",
        "translator": "Gerhard Rauschen",
        "pub_year": 1913,
        "source": "Frühchristliche Apologeten, Band II (Bibliothek der Kirchenväter, 1. Reihe, Band 14)",
        "source_class": "hagiographic",
        "description": "Gerhard Rauschen's 1913 German translation of the proconsular record of the Scillitan Martyrs.",
        "bkv_version": "Das Leiden des Scilitanischen Märtyrer (BKV)",
        "metadata_markers": ("übersetzt von Gerhard Rauschen (Märtyrerakten)",
                             "Band 14", "München 1913"),
        "units": 1,
        "first_heading": "1.",
        "last_heading": "1.",
        "digest": "e8cb6816d3d211026bb56374884fa0ac3dc9875bdee9a09237cb9044a4d59437",
    },
    {
        "work_id": "epistle-of-barnabas-de",
        "edition_of": "epistle-of-barnabas",
        "url": "https://bkv.unifr.ch/works/cpg-1050/versions/barnabasbrief-bkv/divisions",
        "language": "de",
        "title": "Barnabasbrief",
        "author": "St Barnabas the Apostle",
        "date": "late 1st-early 2nd century",
        "translator": "Franz Zeller",
        "pub_year": 1918,
        "source": "Die Apostolischen Väter (Bibliothek der Kirchenväter, 1. Reihe, Band 35), pp. 76-105",
        "source_class": "patristic",
        "description": "Franz Zeller's 1918 German translation of the Epistle of Barnabas.",
        "bkv_version": "Barnabasbrief (BKV)",
        "metadata_markers": ("übersetzt von Franz Zeller", "Band 35",
                             "München 1918", "76-105"),
        "units": 21,
        "first_heading": "1. Kap. Gruß und Freude über die Berufung.",
        "last_heading": "21. Kap. Wandle in Gottes Geboten, denn der Herr ist nahe.",
        "source_substitutions": ({
            "from": "(https://bkv.unifr.ch/works/103/versions/116/scans/wörtlich: der Pest)",
            "to": "(wörtlich: der Pest)",
            "count": 1,
        },),
        "digest": "b0f121ac178bab3d164e20539591055b6247d7e93c6409734c2e3f9488938bfb",
    },
    {
        "work_id": "clement-first-epistle-de",
        "edition_of": "clement-of-rome-first-epistle",
        "url": "https://bkv.unifr.ch/works/cpg-1001/versions/clem-1clem-bkv/divisions",
        "language": "de",
        "title": "Erster Brief an die Korinther",
        "author": "St Clement of Rome",
        "date": "c. 96",
        "translator": "Franz Zeller",
        "pub_year": 1918,
        "source": "Die Apostolischen Väter (Bibliothek der Kirchenväter, 1. Reihe, Band 35), pp. 25-69",
        "source_class": "patristic",
        "description": "Franz Zeller's 1918 German translation of the First Epistle of Clement to the Corinthians.",
        "bkv_version": "Erster Brief an die Korinther (BKV)",
        "metadata_markers": ("übersetzt von Franz Zeller", "Band 35",
                             "München 1918", "25-69"),
        "units": 65,
        "first_heading": "1. Kap. Der gute Stand der Korinthergemeinde vor dem Streit.",
        "last_heading": "65. Kap. Anordnungen über den Gang der Verhandlungen und Segen.",
        "digest": "389e4714e542c8e159997141b19055cee3810d31c28ac376ed24bd2f70aefca7",
    },
    {
        "work_id": "second-clement-de",
        "edition_of": "second-clement",
        "url": "https://bkv.unifr.ch/works/cpg-1003/versions/zweiter-brief-des-klemens-an-die-korinther-bkv/divisions",
        "language": "de",
        "title": "Zweiter Brief des Klemens an die Korinther",
        "author": "An unknown preacher",
        "date": "c. 140",
        "translator": "Franz Zeller",
        "pub_year": 1918,
        "source": "Die Apostolischen Väter (Bibliothek der Kirchenväter, 1. Reihe, Band 35), pp. 294-307",
        "source_class": "patristic",
        "description": "Franz Zeller's 1918 German translation of the ancient homily traditionally called Second Clement.",
        "bkv_version": "Zweiter Brief des Klemens an die Korinther (BKV)",
        "metadata_markers": ("übersetzt von Franz Zeller", "Band 35",
                             "München 1918", "294-307"),
        "units": 20,
        "first_heading": "1. Kap. Unsere Anschauung über Christus und sein Erlösungswerk muss erhaben sein.",
        "last_heading": "20. Kap. Das Glück der Gottlosen darf uns nicht verwirren; die Gerechten bekommen ihren Lohn im Jenseits.",
        "digest": "709d0ffaf7cf9edb460be1cb5d3bc0b8aac0585331907aba16f3c72c5bc0bfa6",
    },
    {
        "work_id": "didache-de",
        "edition_of": "didache",
        "url": "https://bkv.unifr.ch/works/cpg-1753/versions/didache-lehre-der-zwolf-apostel-bkv/divisions",
        "language": "de",
        "title": "Didache - Lehre der zwölf Apostel",
        "author": "The Twelve Apostles",
        "date": "c. 100",
        "translator": "Franz Zeller",
        "pub_year": 1918,
        "source": "Die Apostolischen Väter (Bibliothek der Kirchenväter, 1. Reihe, Band 35), pp. 6-16",
        "source_class": "patristic",
        "description": "Franz Zeller's 1918 German translation of the Didache.",
        "bkv_version": "Didache - Lehre der zwölf Apostel (BKV)",
        "metadata_markers": ("übersetzt von Franz Zeller", "Band 35",
                             "München 1918", "6-16"),
        "units": 16,
        "first_heading": "1. Kap. Die zwei Wege. Der Weg des Lebens verlangt Gottes- und Nächstenliebe.",
        "last_heading": "16. Kap. Harret aus im Guten bis zum Ende, wo sich die falschen Propheten mehren.",
        "digest": "63d702c1a752be1e8e79c7ed47ba646fe4b6f4dd4438cdc842993ce69cf6758a",
    },
    {
        "work_id": "justin-first-apology-de",
        "edition_of": "justin-first-apology",
        "url": "https://bkv.unifr.ch/works/cpg-1073a/versions/erste-apologie-bkv/divisions",
        "language": "de",
        "title": "Erste Apologie",
        "author": "St Justin the Philosopher",
        "date": "c. 155",
        "translator": "Gerhard Rauschen",
        "pub_year": 1913,
        "source": "Frühchristliche Apologeten und Märtyrerakten, Band I (Bibliothek der Kirchenväter, 1. Reihe, Band 12), pp. 65-138",
        "source_class": "patristic",
        "description": "Gerhard Rauschen's 1913 German translation of the First Apology of St Justin.",
        "bkv_version": "Erste Apologie (BKV)",
        "metadata_markers": ("übersetzt von Dr. Gerhard Rauschen", "Band 12",
                             "München 1913", "65-138"),
        "units": 68,
        "first_heading": "1. Widmung.",
        "last_heading": "68. Schluß und Reskript des Kaisers Hadrian über die Christenprozesse.",
        "digest": "46c0464f7a2bbc57d84596b860def0a0e3bafdf6938b940c8b7a363f91213bc0",
    },
    {
        "work_id": "justin-second-apology-de",
        "edition_of": "justin-second-apology",
        "url": "https://bkv.unifr.ch/works/cpg-1073b/versions/zweite-apologie-bkv/divisions",
        "language": "de",
        "title": "Zweite Apologie",
        "author": "St Justin the Philosopher",
        "date": "c. 155",
        "translator": "Gerhard Rauschen",
        "pub_year": 1913,
        "source": "Frühchristliche Apologeten und Märtyrerakten, Band I (Bibliothek der Kirchenväter, 1. Reihe, Band 12), pp. 139-155",
        "source_class": "patristic",
        "description": "Gerhard Rauschen's 1913 German translation of the Second Apology of St Justin.",
        "bkv_version": "Zweite Apologie (BKV)",
        "metadata_markers": ("übersetzt von Dr. Gerhard Rauschen", "Band 12",
                             "München 1913", "139-155"),
        "units": 15,
        "first_heading": "1. Schlechte Menschen und Dämonen wetteifern in Feindseligkeiten gegen die Christen.",
        "last_heading": "15. Schluß.",
        "digest": "a5baa5c2ef9cbaae79f42fba14ce938d42b775ea4e696c06e1400be54936939e",
    },
    {
        "work_id": "athanasius-incarnation-de",
        "edition_of": "athanasius-on-the-incarnation",
        "url": "https://bkv.unifr.ch/works/cpg-2091/versions/uber-die-menschwerdung-des-logos-und-dessen-leibliche-erscheinung-unter-uns-bkv/divisions",
        "language": "de",
        "title": "Über die Menschwerdung des Logos und dessen leibliche Erscheinung unter uns",
        "author": "St Athanasius the Great",
        "date": "c. 318",
        "translator": "Anton Stegmann and Hans Mertel",
        "pub_year": 1917,
        "source": "Athanasius, Ausgewählte Schriften, Band 2 (Bibliothek der Kirchenväter, 1. Reihe, Band 31), 1917",
        "source_class": "patristic",
        "description": "Anton Stegmann and Hans Mertel's 1917 German translation of St Athanasius on the Incarnation of the Word.",
        "bkv_version": "Über die Menschwerdung des Logos und dessen leibliche Erscheinung unter uns (BKV)",
        "metadata_markers": ("übersetzt von Anton Stegmann und Hans Mertel",
                             "Band 31", "München 1917"),
        "units": 57,
        "first_heading": "1.",
        "last_heading": "57.",
        "strip_terminal_markers": ("PAGE 40",),
        "digest": "35532da7eb5294eeda3dc8ee0631805c8c00618b20eb519c892b27613277fe81",
    },
    {
        "work_id": "chrysostom-priesthood-de",
        "edition_of": "chrysostom-on-the-priesthood",
        "url": "https://bkv.unifr.ch/works/cpg-4316/versions/uber-das-priestertum-bkv/divisions",
        "language": "de",
        "title": "Über das Priestertum",
        "author": "St John Chrysostom",
        "date": "c. 386",
        "translator": "Joh. Chrysostomus Baur",
        "pub_year": 1916,
        "source": "Des heiligen Kirchenlehrers Johannes Chrysostomus ausgewählte Schriften, Band 4 (Bibliothek der Kirchenväter, 1. Reihe, Band 27), 1916",
        "source_class": "patristic",
        "description": "Joh. Chrysostomus Baur's 1916 German translation of St John Chrysostom on the priesthood.",
        "bkv_version": "Über das Priestertum (BKV)",
        "metadata_markers": ("übers. von Joh. Chrysostomus Baur",
                             "Band 27", "München 1916"),
        "units": 6,
        "first_heading": "1. Buch",
        "last_heading": "6. Buch",
        "digest": "94e6f15ec1dcbb0544ebfd29903ee2968223be4d42cd57d140b0f86b589f35c6",
    },
    {
        "work_id": "martyrdom-of-justin-de",
        "edition_of": "martyrdom-of-justin",
        "url": "https://bkv.unifr.ch/works/-26/versions/martyrium-des-hl-justin-und-seiner-genossen-bkv/divisions",
        "language": "de",
        "title": "Martyrium des Hl. Justin und seiner Genossen",
        "author": "The Roman court record",
        "date": "c. 165",
        "translator": "Gerhard Rauschen",
        "pub_year": 1913,
        "source": "Frühchristliche Apologeten, Band II (Bibliothek der Kirchenväter, 1. Reihe, Band 14), 1913",
        "source_class": "hagiographic",
        "description": "Gerhard Rauschen's 1913 German translation of the court record of St Justin and his companions.",
        "bkv_version": "Martyrium des Hl. Justin und seiner Genossen (BKV)",
        "metadata_markers": ("übersetzt von Gerhard Rauschen (Märtyrerakten)",
                             "Band 14", "München 1913"),
        "units": 6,
        "first_heading": "1.",
        "last_heading": "6.",
        "digest": "1b6182a1dd8281cb8b12211b4eeb5d9f5405e1442e2f532ebacbb5d860eb556b",
    },
    {
        "work_id": "liturgy-of-st-james-de",
        "edition_of": "liturgy-of-st-james",
        "url": "https://bkv.unifr.ch/works/-2/versions/die-griechische-jakobusliturgie-bkv/divisions",
        "language": "de",
        "title": "Die griechische Jakobusliturgie",
        "author": "St James the Brother of the Lord",
        "date": "4th-5th century",
        "translator": "Remigius Storf",
        "pub_year": 1912,
        "source": "Griechische Liturgien (Bibliothek der Kirchenväter, 1. Reihe, Band 5), 1912",
        "source_class": "liturgical",
        "description": "Remigius Storf's 1912 German edition of the Divine Liturgy of St James.",
        "bkv_version": "Die griechische Jakobusliturgie (BKV)",
        "metadata_markers": ("Übers. von Remigius Storf", "Band 5",
                             "München 1912"),
        "units": 3,
        "first_heading": "A. Vorbereitungsgebete [Prothesis].",
        "last_heading": "C. Messe Der Gläubigen.",
        "digest": "329a941e26a1448630a2902b88f1e0c8b72a6608ac9e1fa100005550c2494d9b",
    },
    {
        "work_id": "liturgy-of-st-mark-de",
        "edition_of": "liturgy-of-st-mark",
        "url": "https://bkv.unifr.ch/works/-3/versions/die-griechische-markusliturgie-bkv/divisions",
        "language": "de",
        "title": "Die griechische Markusliturgie",
        "author": "St Mark the Evangelist",
        "date": "4th-5th century",
        "translator": "Remigius Storf",
        "pub_year": 1912,
        "source": "Griechische Liturgien (Bibliothek der Kirchenväter, 1. Reihe, Band 5), 1912",
        "source_class": "liturgical",
        "description": "Remigius Storf's 1912 German edition of the Divine Liturgy of St Mark.",
        "bkv_version": "Die griechische Markusliturgie (BKV)",
        "metadata_markers": ("Übers. von Remigius Storf", "Band 5",
                             "München 1912"),
        "units": 3,
        "first_heading": "A. Vorbereitungsgebete (Prothesis).",
        "last_heading": "C. Messe der Gläubigen",
        "digest": "60cca49f3ac41de68b688505ada83097d869d731abbb2186ddb058cce99e8829",
    },
    {
        "work_id": "life-of-hilarion-de",
        "edition_of": "life-of-hilarion",
        "url": "https://bkv.unifr.ch/works/cpl-618/versions/leben-des-hl-einsiedlers-hilarion-bkv/divisions",
        "language": "de",
        "title": "Leben des hl. Einsiedlers Hilarion",
        "author": "St Jerome",
        "date": "c. 391",
        "translator": "Ludwig Schade",
        "pub_year": 1914,
        "source": "Des heiligen Kirchenvaters Hieronymus ausgewählte Schriften, Band 1 (Bibliothek der Kirchenväter, 1. Reihe, Band 52), 1914",
        "source_class": "hagiographic",
        "description": "Ludwig Schade's 1914 German translation of St Jerome's Life of St Hilarion.",
        "bkv_version": "Leben des hl. Einsiedlers Hilarion (BKV)",
        "metadata_markers": ("übers. von Ludwig Schade", "Band 52", "1914"),
        "units": 47,
        "first_heading": "1.",
        "last_heading": "47.",
        "digest": "62f0ef094a63a0e4ed0e403e02836c4d570fe4521832d95eb41e20c6199d5522",
    },
    {
        "work_id": "life-of-malchus-de",
        "edition_of": "life-of-malchus",
        "url": "https://bkv.unifr.ch/works/cpl-619/versions/leben-und-gefangenschaft-des-monches-malchus-bkv/divisions",
        "language": "de",
        "title": "Leben und Gefangenschaft des Mönches Malchus",
        "author": "St Jerome",
        "date": "c. 391",
        "translator": "Ludwig Schade",
        "pub_year": 1914,
        "source": "Des heiligen Kirchenvaters Hieronymus ausgewählte Schriften, Band 1 (Bibliothek der Kirchenväter, 1. Reihe, Band 15), 1914",
        "source_class": "hagiographic",
        "description": "Ludwig Schade's 1914 German translation of St Jerome's Life of Malchus.",
        "bkv_version": "Leben und Gefangenschaft des Mönches Malchus (BKV)",
        "metadata_markers": ("übers. von Ludwig Schade", "Band 15", "1914"),
        "units": 10,
        "first_heading": "1.",
        "last_heading": "10.",
        "digest": "02b7eeb90f5eb689b5ecafe4f92c9a3f2befc7a543ee90f519e03679924c10ca",
    },
    {
        "work_id": "life-of-paul-hermit-de",
        "edition_of": "life-of-paul-the-hermit",
        "url": "https://bkv.unifr.ch/works/cpl-617/versions/leben-des-hl-paulus-des-ersten-einsiedlers-bkv/divisions",
        "language": "de",
        "title": "Leben des hl. Paulus, des ersten Einsiedlers",
        "author": "St Jerome",
        "date": "c. 375",
        "translator": "Ludwig Schade",
        "pub_year": 1914,
        "source": "Des heiligen Kirchenvaters Hieronymus ausgewählte Schriften, Band 1 (Bibliothek der Kirchenväter, 1. Reihe, Band 15), 1914",
        "source_class": "hagiographic",
        "description": "Ludwig Schade's 1914 German translation of St Jerome's Life of St Paul the First Hermit.",
        "bkv_version": "Leben des hl. Paulus, des ersten Einsiedlers (BKV)",
        "metadata_markers": ("übers. von Ludwig Schade", "Band 15", "1914"),
        "units": 18,
        "first_heading": "1.",
        "last_heading": "18.",
        "footnote_repair": {
            "id": "fn2",
            "marker": "## 2.",
            "prefix_end": "[Antonius].",
            "tail_markers": ("[^2]", "[^3]", "[^4]"),
        },
        "supplement_divisions": ({
            "url": "https://bkv.unifr.ch/de/works/cpl-617/versions/leben-des-hl-paulus-des-ersten-einsiedlers-bkv/divisions/3",
            "cache": "life-of-paul-hermit-de-division-2.html",
            "heading": "2.",
            "before_heading": "3.",
            "notes": 3,
            "digest": "52ad28c5ddbd3ea8261b3e64243f1f9573f75bf24e216cdd8477ce5cb2e4cf44",
        },),
        "digest": "4b3c69d740887323790464ff1034e86ba000657f1cefcc96d0286171a5ff0a8b",
    },
    {
        "work_id": "cyprian-on-mortality-de",
        "edition_of": "cyprian-on-mortality",
        "url": "https://bkv.unifr.ch/works/cpl-44/versions/uber-die-sterblichkeit-bkv/divisions",
        "language": "de",
        "title": "Über die Sterblichkeit",
        "author": "St Cyprian of Carthage",
        "date": "c. 252",
        "translator": "Julius Baer",
        "pub_year": 1918,
        "source": "Des heiligen Kirchenvaters Caecilius Cyprianus sämtliche Schriften (Bibliothek der Kirchenväter, 1. Reihe, Band 34), 1918",
        "source_class": "patristic",
        "description": "Julius Baer's 1918 German translation of St Cyprian's treatise On the Mortality.",
        "bkv_version": "Über die Sterblichkeit (BKV)",
        "metadata_markers": ("Identifier: CPL 44", "übers. von Julius Baer",
                             "Band 34", "München 1918"),
        "units": 7,
        "first_heading": "Einleitung",
        "last_heading": "Schluss",
        "digest": "a8edda3948ef24b18cd44691702c058e64362255417427ae3f2eab64333825b1",
    },
    {
        "work_id": "cyprian-on-the-lapsed-de",
        "edition_of": "cyprian-on-the-lapsed",
        "url": "https://bkv.unifr.ch/works/cpl-42/versions/uber-die-gefallenen-bkv/divisions",
        "language": "de",
        "title": "Über die Gefallenen",
        "author": "St Cyprian of Carthage",
        "date": "251",
        "translator": "Julius Baer",
        "pub_year": 1918,
        "source": "Des heiligen Kirchenvaters Caecilius Cyprianus sämtliche Schriften (Bibliothek der Kirchenväter, 1. Reihe, Band 34), 1918",
        "source_class": "patristic",
        "description": "Julius Baer's 1918 German translation of St Cyprian's treatise On the Lapsed.",
        "bkv_version": "Über die Gefallenen (BKV)",
        "metadata_markers": ("Identifier: CPL 42", "übers. von Julius Baer",
                             "Band 34", "München 1918"),
        "units": 3,
        "first_heading": "Einleitung",
        "last_heading": "Schluss",
        "digest": "603ba99e683839d4734e854a4697f731ecdbbbae3186429fc47a109e6525f237",
    },
    {
        "work_id": "cyprian-unity-of-the-church-de",
        "edition_of": "cyprian-unity-of-the-church",
        "url": "https://bkv.unifr.ch/works/cpl-41/versions/uber-die-einheit-der-katholischen-kirche-bkv/divisions",
        "language": "de",
        "title": "Über die Einheit der katholischen Kirche",
        "author": "St Cyprian of Carthage",
        "date": "c. 251",
        "translator": "Julius Baer",
        "pub_year": 1918,
        "source": "Des heiligen Kirchenvaters Caecilius Cyprianus sämtliche Schriften (Bibliothek der Kirchenväter, 1. Reihe, Band 34), 1918",
        "source_class": "patristic",
        "description": "Julius Baer's 1918 German translation of St Cyprian's treatise On the Unity of the Church.",
        "bkv_version": "Über die Einheit der katholischen Kirche (BKV)",
        "metadata_markers": ("Identifier: CPL 41", "übers. von Julius Baer",
                             "Band 34", "München 1918"),
        "units": 6,
        "first_heading": "Einleitung",
        "last_heading": "Schluss",
        "digest": "b9006f41e9ae613d11263847818aee8a93db83d16dab2a1a8f0bb0cd835c14ee",
    },
    {
        "work_id": "cyprian-on-patience-de",
        "edition_of": "cyprian-on-patience",
        "url": "https://bkv.unifr.ch/works/cpl-48/versions/vom-segen-der-geduld-bkv/divisions",
        "language": "de",
        "title": "Vom Segen der Geduld",
        "author": "St Cyprian of Carthage",
        "date": "256",
        "translator": "Julius Baer",
        "pub_year": 1918,
        "source": "Des heiligen Kirchenvaters Caecilius Cyprianus sämtliche Schriften (Bibliothek der Kirchenväter, 1. Reihe, Band 34), 1918",
        "source_class": "patristic",
        "description": "Julius Baer's 1918 German translation of St Cyprian's treatise On the Advantage of Patience.",
        "bkv_version": "Vom Segen der Geduld (BKV)",
        "metadata_markers": ("Identifier: CPL 48", "übers. von Julius Baer",
                             "Band 34", "München 1918"),
        "units": 7,
        "first_heading": "Einleitung",
        "last_heading": "Schluss",
        "digest": "f998fee6269fb07330afdd58cf96677dfd57fef5ac2b49bc3b25d001187cd5a8",
    },
    {
        "work_id": "cyprian-jealousy-and-envy-de",
        "edition_of": "cyprian-jealousy-and-envy",
        "url": "https://bkv.unifr.ch/works/cpl-49/versions/uber-eifersucht-und-neid-bkv/divisions",
        "language": "de",
        "title": "Über Eifersucht und Neid",
        "author": "St Cyprian of Carthage",
        "date": "256",
        "translator": "Julius Baer",
        "pub_year": 1918,
        "source": "Des heiligen Kirchenvaters Caecilius Cyprianus sämtliche Schriften (Bibliothek der Kirchenväter, 1. Reihe, Band 34), 1918",
        "source_class": "patristic",
        "description": "Julius Baer's 1918 German translation of St Cyprian's treatise On Jealousy and Envy.",
        "bkv_version": "Über Eifersucht und Neid (BKV)",
        "metadata_markers": ("Identifier: CPL 49", "übers. von Julius Baer",
                             "Band 34", "München 1918"),
        "units": 4,
        "first_heading": "Einleitung",
        "last_heading": "Schluss",
        "digest": "8212c7c7ce3c81ca23bef755284a6705e4a46aee6e11e64b8e34cecd8025ce7b",
    },
    {
        "work_id": "cyprian-works-and-alms-de",
        "edition_of": "cyprian-works-and-alms",
        "url": "https://bkv.unifr.ch/works/cpl-47/versions/uber-gute-werke-und-almosen-bkv/divisions",
        "language": "de",
        "title": "Über gute Werke und Almosen",
        "author": "St Cyprian of Carthage",
        "date": "c. 253",
        "translator": "Julius Baer",
        "pub_year": 1918,
        "source": "Des heiligen Kirchenvaters Caecilius Cyprianus sämtliche Schriften (Bibliothek der Kirchenväter, 1. Reihe, Band 34), 1918",
        "source_class": "patristic",
        "description": "Julius Baer's 1918 German translation of St Cyprian's treatise On Works and Alms.",
        "bkv_version": "Über gute Werke und Almosen (BKV)",
        "metadata_markers": ("Identifier: CPL 47", "übers. von Julius Baer",
                             "Band 34", "München 1918"),
        "units": 26,
        "first_heading": "1. In der Wohltätigkeit hat uns der gütige Gott ein Mittel gegeben zur Sicherung unseres Heils.",
        "last_heading": "26. Wie dem Christen in den Zeiten der Verfolgung die rote Märtyrerkrone winkt, so gilt es im Frieden, durch Almosen und gute Werke die weiße Siegeskrone zu gewinnen.",
        "digest": "20b2a054e16c0df71729d8b2b1bcf3ef0dae06a18af5c9794418e861fcca2411",
    },
    {
        "work_id": "cyprian-to-demetrian-de",
        "edition_of": "cyprian-to-demetrian",
        "url": "https://bkv.unifr.ch/works/cpl-46/versions/an-demetrianus-bkv/divisions",
        "language": "de",
        "title": "An Demetrianus",
        "author": "St Cyprian of Carthage",
        "date": "c. 252",
        "translator": "Julius Baer",
        "pub_year": 1918,
        "source": "Des heiligen Kirchenvaters Caecilius Cyprianus sämtliche Schriften (Bibliothek der Kirchenväter, 1. Reihe, Band 34), 1918",
        "source_class": "patristic",
        "description": "Julius Baer's 1918 German translation of St Cyprian's address To Demetrian.",
        "bkv_version": "An Demetrianus (BKV)",
        "metadata_markers": ("Identifier: CPL 46", "übers. von Julius Baer",
                             "Band 34", "München 1918"),
        "units": 5,
        "first_heading": "Einleitung",
        "last_heading": "Schluss",
        "digest": "23b45203cbd05b132cc9fb2a27ca624ca50093ad5513efbaefd2fd51a2a2e686",
    },
    {
        "work_id": "cyprian-dress-of-virgins-de",
        "edition_of": "cyprian-dress-of-virgins",
        "url": "https://bkv.unifr.ch/works/cpl-40/versions/uber-die-haltung-der-jungfrauen-bkv/divisions",
        "language": "de",
        "title": "Über die Haltung der Jungfrauen",
        "author": "St Cyprian of Carthage",
        "date": "c. 249",
        "translator": "Julius Baer",
        "pub_year": 1918,
        "source": "Des heiligen Kirchenvaters Caecilius Cyprianus sämtliche Schriften (Bibliothek der Kirchenväter, 1. Reihe, Band 34), 1918",
        "source_class": "patristic",
        "description": "Julius Baer's 1918 German translation of St Cyprian's treatise On the Dress of Virgins.",
        "bkv_version": "Über die Haltung der Jungfrauen (BKV)",
        "metadata_markers": ("Identifier: CPL 40", "übers. von Julius Baer",
                             "Band 34", "München 1918"),
        "units": 5,
        "first_heading": "Einleitung",
        "last_heading": "Schluss",
        "digest": "54c84a30e5a0803c969b0e64439dc63195dffb1314d3fd12873e28aa23e9f255",
    },
    {
        "work_id": "cyprian-lords-prayer-de",
        "edition_of": "cyprian-lords-prayer",
        "url": "https://bkv.unifr.ch/works/cpl-43/versions/uber-das-gebet-des-herrn-bkv/divisions",
        "language": "de",
        "title": "Über das Gebet des Herrn",
        "author": "St Cyprian of Carthage",
        "date": "c. 252",
        "translator": "Julius Baer",
        "pub_year": 1918,
        "source": "Des heiligen Kirchenvaters Caecilius Cyprianus sämtliche Schriften (Bibliothek der Kirchenväter, 1. Reihe, Band 34), 1918",
        "source_class": "patristic",
        "description": "Julius Baer's 1918 German translation of St Cyprian's treatise On the Lord's Prayer.",
        "bkv_version": "Über das Gebet des Herrn (BKV)",
        "metadata_markers": ("Identifier: CPL 43", "übers. von Julius Baer",
                             "Band 34", "München 1918"),
        "units": 6,
        "first_heading": "Einleitung",
        "last_heading": "Schlussteil II",
        "digest": "4e2c3011857d3860813b5c7433d4b2e97ecb85c673b0a22c8ca0cc6d25832c70",
    },
    {
        "work_id": "life-and-passion-of-cyprian-de",
        "edition_of": "life-and-passion-of-cyprian",
        "url": "https://bkv.unifr.ch/works/cpl-52/versions/leben-des-cacilius-cyprianus-von-diakon-pontius-bkv/divisions",
        "language": "de",
        "title": "Leben des Cäcilius Cyprianus von Diakon Pontius",
        "author": "Pontius the Deacon",
        "date": "c. 259",
        "translator": "Julius Baer",
        "pub_year": 1918,
        "source": "Des heiligen Kirchenvaters Caecilius Cyprianus sämtliche Schriften (Bibliothek der Kirchenväter, 1. Reihe, Band 34), 1918",
        "source_class": "hagiographic",
        "description": "Julius Baer's 1918 German translation of Pontius the Deacon's Life and Passion of St Cyprian.",
        "bkv_version": "Leben des Cäcilius Cyprianus von Diakon Pontius (BKV)",
        "metadata_markers": ("Identifier: CPL 52", "übers. von Julius Baer",
                             "Band 34", "München 1918"),
        "units": 19,
        "first_heading": "1. Der Zweck des Buches und die Schwierigkeit der Aufgabe.",
        "last_heading": "19. Nachruf auf Cyprian als den ersten bischöflichen Märtyrer Afrikas.",
        "digest": "2d2d4906bfe2526762c05b7755079dcc71efcfd76d21fad54c7f17a7c8030166",
    },
    {
        "work_id": "cyprian-to-donatus-de",
        "edition_of": "cyprian-to-donatus",
        "url": "https://bkv.unifr.ch/works/cpl-38/versions/an-donatus-bkv/divisions",
        "language": "de",
        "title": "An Donatus",
        "author": "St Cyprian of Carthage",
        "date": "c. 246",
        "translator": "Julius Baer",
        "pub_year": 1918,
        "source": "Des heiligen Kirchenvaters Caecilius Cyprianus sämtliche Schriften (Bibliothek der Kirchenväter, 1. Reihe, Band 34), 1918",
        "source_class": "patristic",
        "description": "Julius Baer's 1918 German translation of St Cyprian's address To Donatus.",
        "bkv_version": "An Donatus (BKV)",
        "metadata_markers": ("Identifier: CPL 38", "übers. von Julius Baer",
                             "Band 34", "München 1918"),
        "units": 5,
        "first_heading": "Einleitung",
        "last_heading": "Schluss",
        "digest": "d17515da1cb1a4fa54d2a6b90ed0930704a1408fd31539b94ccbefa8e64de6fb",
    },
    {
        "work_id": "seventh-council-of-carthage-de",
        "edition_of": "seventh-council-of-carthage",
        "url": "https://bkv.unifr.ch/works/cpl-56/versions/die-ausserungen-der-87-bischofe-uber-die-notwendigkeit-der-ketzertaufe-bkv/divisions",
        "language": "de",
        "title": "Die Äußerungen der 87 Bischöfe über die Notwendigkeit der Ketzertaufe",
        "author": "The eighty-seven bishops at Carthage",
        "date": "256",
        "translator": "Julius Baer",
        "pub_year": 1918,
        "source": "Des heiligen Kirchenvaters Caecilius Cyprianus sämtliche Schriften (Bibliothek der Kirchenväter, 1. Reihe, Band 34), 1918",
        "source_class": "conciliar",
        "description": "Julius Baer's 1918 German translation of Cyprian's introduction and closing words for the council. The statements of the eighty-seven bishops are not included in this edition.",
        "bkv_version": "Die Äußerungen der 87 Bischöfe über die Notwendigkeit der Ketzertaufe (BKV)",
        "metadata_markers": ("Identifier: CPL 56", "übers. von Julius Baer",
                             "Band 34", "München 1918"),
        "units": 2,
        "first_heading": "Einleitung.",
        "last_heading": "Schlußwort.",
        "digest": "a564c91524d9d481f6f827ac1dcda0bb52e043ce5a7e81be01492d30c27c8176",
    },
    {
        "work_id": "cyprian-dress-of-virgins-fr",
        "edition_of": "cyprian-dress-of-virgins",
        "url": "https://bkv.unifr.ch/works/cpl-40/versions/de-la-conduite-des-vierges/divisions",
        "language": "fr",
        "title": "De la conduite des vierges",
        "author": "St Cyprian of Carthage",
        "date": "c. 249",
        "translator": "M. l'abbé Thibaut",
        "pub_year": 1909,
        "source": "Oeuvres de Saint Cyprien, edited by Dom H. Leclercq (Paris-Poitiers, 1909), translation by M. l'abbé Thibaut (Tours, 1869)",
        "source_class": "patristic",
        "description": "M. l'abbé Thibaut's 1869 French translation of St Cyprian's treatise On the Dress of Virgins, in Dom H. Leclercq's 1909 edition.",
        "bkv_version": "De la conduite des vierges",
        "metadata_markers": ("Identifier: CPL 40", "Dom H. Leclercq",
                             "1909", "M. l'abbé Thibaut", "Tours 1869"),
        "units": 5,
        "first_heading": "Introduction",
        "last_heading": "Fin",
        "digest": "b49b8c35340a7fb13e816b86e6bf1ac70604b118e3cfbbfd0a65e1c9af95be86",
    },
    {
        "work_id": "cyprian-unity-of-the-church-fr",
        "edition_of": "cyprian-unity-of-the-church",
        "url": "https://bkv.unifr.ch/works/cpl-41/versions/de-lunite-de-leglise/divisions",
        "language": "fr",
        "title": "De l'unité de l'église",
        "author": "St Cyprian of Carthage",
        "date": "c. 251",
        "translator": "M. l'abbé Thibaut",
        "pub_year": 1909,
        "source": "Oeuvres de Saint Cyprien, edited by Dom H. Leclercq (Paris-Poitiers, 1909), translation by M. l'abbé Thibaut (Tours, 1869)",
        "source_class": "patristic",
        "description": "M. l'abbé Thibaut's 1869 French translation of St Cyprian's treatise On the Unity of the Church, in Dom H. Leclercq's 1909 edition.",
        "bkv_version": "De l'unité de l'église",
        "metadata_markers": ("Identifier: CPL 41", "Dom H. Leclercq",
                             "1909", "M. l'abbé Thibaut", "Tours 1869"),
        "units": 6,
        "first_heading": "Introduction",
        "last_heading": "Fin",
        "digest": "5b8cf498e975dcd42d92a00f7b727d28efd091e53bbc9a4779a67fbe6ff48c13",
    },
    {
        "work_id": "cyprian-on-the-lapsed-fr",
        "edition_of": "cyprian-on-the-lapsed",
        "url": "https://bkv.unifr.ch/works/cpl-42/versions/des-tombes/divisions",
        "language": "fr",
        "title": "Des Tombés",
        "author": "St Cyprian of Carthage",
        "date": "251",
        "translator": "M. l'abbé Thibaut",
        "pub_year": 1909,
        "source": "Oeuvres de Saint Cyprien, edited by Dom H. Leclercq (Paris-Poitiers, 1909), translation by M. l'abbé Thibaut (Tours, 1869)",
        "source_class": "patristic",
        "description": "M. l'abbé Thibaut's 1869 French translation of St Cyprian's treatise On the Lapsed, in Dom H. Leclercq's 1909 edition.",
        "bkv_version": "Des Tombés",
        "metadata_markers": ("Identifier: CPL 42", "Dom H. Leclercq",
                             "1909", "M. l'abbé Thibaut", "Tours 1869"),
        "units": 3,
        "first_heading": "Introduction",
        "last_heading": "Fin",
        "digest": "fccd6f79567937f56679a932296136c2aeb6fab0df9dac1d32d8a2f1cf759069",
    },
    {
        "work_id": "cyprian-lords-prayer-fr",
        "edition_of": "cyprian-lords-prayer",
        "url": "https://bkv.unifr.ch/works/cpl-43/versions/de-loraison-dominicale/divisions",
        "language": "fr",
        "title": "De l'Oraison Dominicale",
        "author": "St Cyprian of Carthage",
        "date": "c. 252",
        "translator": "M. l'abbé Thibaut",
        "pub_year": 1909,
        "source": "Oeuvres de Saint Cyprien, edited by Dom H. Leclercq (Paris-Poitiers, 1909), translation by M. l'abbé Thibaut (Tours, 1869)",
        "source_class": "patristic",
        "description": "M. l'abbé Thibaut's 1869 French translation of St Cyprian's treatise On the Lord's Prayer, in Dom H. Leclercq's 1909 edition.",
        "bkv_version": "De l'Oraison Dominicale",
        "metadata_markers": ("Identifier: CPL 43", "Dom H. Leclercq",
                             "1909", "M. l'abbé Thibaut", "Tours 1869"),
        "units": 6,
        "first_heading": "Introduction",
        "last_heading": "Fin 2",
        "digest": "705336fbcce729c75a6876e0189f3b26775bbd349a7a5537da2d22031a65b289",
    },
    {
        "work_id": "cyprian-on-mortality-fr",
        "edition_of": "cyprian-on-mortality",
        "url": "https://bkv.unifr.ch/works/cpl-44/versions/de-la-mortalitate/divisions",
        "language": "fr",
        "title": "De la mortalitaté",
        "author": "St Cyprian of Carthage",
        "date": "c. 252",
        "translator": "M. l'abbé Thibaut",
        "pub_year": 1909,
        "source": "Oeuvres de Saint Cyprien, edited by Dom H. Leclercq (Paris-Poitiers, 1909), translation by M. l'abbé Thibaut (Tours, 1869)",
        "source_class": "patristic",
        "description": "M. l'abbé Thibaut's 1869 French translation of St Cyprian's treatise On the Mortality, in Dom H. Leclercq's 1909 edition.",
        "bkv_version": "De la mortalitaté",
        "metadata_markers": ("Identifier: CPL 44", "Dom H. Leclercq",
                             "1909", "M. l'abbé Thibaut", "Tours 1869"),
        "units": 7,
        "first_heading": "Introduction",
        "last_heading": "Fin",
        "digest": "5aaba825e313fd4a3d429ecb7269bd845358c94e53e6c48518d114a3e1441fc9",
    },
    {
        "work_id": "cyprian-to-demetrian-fr",
        "edition_of": "cyprian-to-demetrian",
        "url": "https://bkv.unifr.ch/works/cpl-46/versions/a-demetrien/divisions",
        "language": "fr",
        "title": "A Démétrien",
        "author": "St Cyprian of Carthage",
        "date": "c. 252",
        "translator": "M. l'abbé Thibaut",
        "pub_year": 1909,
        "source": "Oeuvres de Saint Cyprien, edited by Dom H. Leclercq (Paris-Poitiers, 1909), translation by M. l'abbé Thibaut (Tours, 1869)",
        "source_class": "patristic",
        "description": "M. l'abbé Thibaut's 1869 French translation of St Cyprian's address To Demetrian, in Dom H. Leclercq's 1909 edition.",
        "bkv_version": "A Démétrien",
        "metadata_markers": ("Identifier: CPL 46", "Dom H. Leclercq",
                             "1909", "M. l'abbé Thibaut", "Tours 1869"),
        "units": 5,
        "first_heading": "Préface",
        "last_heading": "Fin",
        "digest": "82a04a1c2d77e8e80600bd17f7abb83acdae85bcb61183791b6acea59e5d2d62",
    },
    {
        "work_id": "cyprian-works-and-alms-fr",
        "edition_of": "cyprian-works-and-alms",
        "url": "https://bkv.unifr.ch/works/cpl-47/versions/des-bonnes-oeuvres-et-de-laumone/divisions",
        "language": "fr",
        "title": "Des bonnes Oeuvres et de l'Aumône",
        "author": "St Cyprian of Carthage",
        "date": "c. 253",
        "translator": "M. l'abbé Thibaut",
        "pub_year": 1909,
        "source": "Oeuvres de Saint Cyprien, edited by Dom H. Leclercq (Paris-Poitiers, 1909), translation by M. l'abbé Thibaut (Tours, 1869)",
        "source_class": "patristic",
        "description": "M. l'abbé Thibaut's 1869 French translation of St Cyprian's treatise On Works and Alms, in Dom H. Leclercq's 1909 edition.",
        "bkv_version": "Des bonnes Oeuvres et de l'Aumône",
        "metadata_markers": ("Identifier: CPL 47", "Dom H. Leclercq",
                             "1909", "M. l'abbé Thibaut", "Tours 1869"),
        "units": 26,
        "first_heading": "1.",
        "last_heading": "26.",
        "digest": "88a59a32f2f0848e2df16d50c9ea732a83a27922bc2389d401b67b54d7f773ec",
    },
    {
        "work_id": "cyprian-on-patience-fr",
        "edition_of": "cyprian-on-patience",
        "url": "https://bkv.unifr.ch/works/cpl-48/versions/avantages-des-la-patience/divisions",
        "language": "fr",
        "title": "Avantages des la patience",
        "author": "St Cyprian of Carthage",
        "date": "256",
        "translator": "M. l'abbé Thibaut",
        "pub_year": 1909,
        "source": "Oeuvres de Saint Cyprien, edited by Dom H. Leclercq (Paris-Poitiers, 1909), translation by M. l'abbé Thibaut (Tours, 1869)",
        "source_class": "patristic",
        "description": "M. l'abbé Thibaut's 1869 French translation of St Cyprian's treatise On the Advantage of Patience, in Dom H. Leclercq's 1909 edition.",
        "bkv_version": "Avantages des la patience",
        "metadata_markers": ("Identifier: CPL 48", "Dom H. Leclercq",
                             "1909", "M. l'abbé Thibaut", "Tours 1869"),
        "units": 7,
        "first_heading": "Introduction",
        "last_heading": "Fin",
        "digest": "af6ce337aad3656d63c0a6910fc45127ca71ef0277f6127130746694ea2141f1",
    },
    {
        "work_id": "cyprian-jealousy-and-envy-fr",
        "edition_of": "cyprian-jealousy-and-envy",
        "url": "https://bkv.unifr.ch/works/cpl-49/versions/de-la-jalusie-et-de-lenvie/divisions",
        "language": "fr",
        "title": "De la jalusie et de l'envie",
        "author": "St Cyprian of Carthage",
        "date": "256",
        "translator": "M. l'abbé Thibaut",
        "pub_year": 1909,
        "source": "Oeuvres de Saint Cyprien, edited by Dom H. Leclercq (Paris-Poitiers, 1909), translation by M. l'abbé Thibaut (Tours, 1869)",
        "source_class": "patristic",
        "description": "M. l'abbé Thibaut's 1869 French translation of St Cyprian's treatise On Jealousy and Envy, in Dom H. Leclercq's 1909 edition.",
        "bkv_version": "De la jalusie et de l'envie",
        "metadata_markers": ("Identifier: CPL 49", "Dom H. Leclercq",
                             "1909", "M. l'abbé Thibaut", "Tours 1869"),
        "units": 4,
        "first_heading": "Introduction",
        "last_heading": "Fin",
        "digest": "7d2f2c7df1a445adf5da391eec4fba53ed9490fabf5acf5eb0b978e4bb60b3be",
    },
]


HOUSE_TRANSLATION = str.maketrans({
    "\u2010": "-", "\u2011": "-", "\u2012": "-", "\u2013": "-",
    "\u2014": "-", "\u2015": "-", "\u2018": "'", "\u2019": "'",
    "\u201a": "'", "\u201b": "'", "\u201c": '"', "\u201d": '"',
    "\u201e": '"', "\u201f": '"', "\u00a0": " ",
})


def local_name(tag):
    return tag.rsplit("}", 1)[-1]


def has_class(node, name):
    return name in node.attrib.get("class", "").split()


def house(text):
    text = html.unescape(text or "").translate(HOUSE_TRANSLATION)
    return re.sub(r"\s+", " ", text).strip()


def quoted_url(url):
    parts = urllib.parse.urlsplit(url)
    return urllib.parse.urlunsplit((parts.scheme, parts.netloc,
                                    urllib.parse.quote(parts.path),
                                    parts.query, parts.fragment))


def fetch(url, cache_name):
    path = CACHE / cache_name
    if path.exists():
        return path.read_bytes()
    req = urllib.request.Request(quoted_url(url), headers={"User-Agent": UA})
    with urllib.request.urlopen(req, timeout=45) as response:
        body = response.read()
    path.write_bytes(body)
    return body


def epub_for(entry):
    page = fetch(entry["url"], entry["work_id"] + ".html").decode("utf-8")
    links = [html.unescape(x) for x in re.findall(r'href="([^"]+)"', page,
                                                  flags=re.I)]
    epubs = [urllib.parse.urljoin(entry["url"], x)
             for x in links if x.lower().endswith(".epub")]
    if len(epubs) != 1:
        raise ValueError("%s: expected one EPUB link, found %d"
                         % (entry["work_id"], len(epubs)))
    return fetch(epubs[0], entry["work_id"] + ".epub")


def render(node):
    """Render XHTML text, omitting only scan markers and note backlinks."""
    out = [node.text or ""]
    for child in node:
        tag = local_name(child.tag)
        href = child.attrib.get("href", "")
        if tag == "a" and "/scans/" in href:
            pass
        elif tag == "a" and has_class(child, "footnote-back"):
            pass
        elif tag == "a" and has_class(child, "footnote-ref"):
            out.append("[%s]" % house("".join(child.itertext())))
        else:
            out.append(render(child))
        out.append(child.tail or "")
    return "".join(out)


def web_fragment_text(fragment):
    """Render the tightly asserted text fragment from a BKV division page."""
    def replace_sup(match):
        value = match.group(0)
        if "footnote-ref" not in value:
            return value
        label = re.sub(r"<[^>]+>", "", value)
        return "[%s]" % house(label)

    fragment = re.sub(r"<sup\b[^>]*>.*?</sup>", replace_sup, fragment,
                      flags=re.I | re.S)
    fragment = re.sub(
        r'<a\b[^>]*class="[^"]*footnote-backref[^"]*"[^>]*>.*?</a>',
        "", fragment, flags=re.I | re.S)
    fragment = re.sub(r"<br\s*/?>", "\n", fragment, flags=re.I)
    return house(re.sub(r"<[^>]+>", "", fragment))


def parse_division_page(entry, supplement):
    raw = fetch(supplement["url"], supplement["cache"]).decode("utf-8")
    match = re.search(
        r'<div class="">\s*<h2>(.*?)</h2>(.*?)'
        r'<div class="ornament">', raw, flags=re.I | re.S)
    if not match:
        raise ValueError("%s: supplement page structure changed"
                         % entry["work_id"])
    heading = web_fragment_text(match.group(1))
    body = match.group(2)
    parts = re.split(r'<div class="footnotes">', body, maxsplit=1,
                     flags=re.I)
    if len(parts) != 2:
        raise ValueError("%s: supplement footnotes are missing"
                         % entry["work_id"])
    paragraphs = [web_fragment_text(x) for x in
                  re.findall(r"<p>(.*?)</p>", parts[0], flags=re.I | re.S)]
    paragraphs = [x for x in paragraphs if x]
    notes = [web_fragment_text(x) for x in re.findall(
        r'<li\s+id="fn:[^"]+">\s*<p>(.*?)</p>\s*</li>', parts[1],
        flags=re.I | re.S)]
    refs = [int(x) for x in re.findall(r"\[(\d+)\]",
                                       " ".join(paragraphs))]
    expected_refs = list(range(1, supplement["notes"] + 1))
    if heading != supplement["heading"] or refs != expected_refs:
        raise ValueError("%s: supplement heading or references changed"
                         % entry["work_id"])
    if len(notes) != supplement["notes"] or any(not x for x in notes):
        raise ValueError("%s: expected %d supplement notes, found %d"
                         % (entry["work_id"], supplement["notes"], len(notes)))
    text = "\n\n".join(paragraphs)
    text += "\n\n" + "\n\n".join(
        "[%d] %s" % (number, note)
        for number, note in enumerate(notes, 1))
    canonical = json.dumps({"heading": heading, "text": text},
                           ensure_ascii=False, separators=(",", ":"))
    digest = hashlib.sha256(canonical.encode("utf-8")).hexdigest()
    if supplement["digest"] and digest != supplement["digest"]:
        raise ValueError("%s: supplement digest changed: %s"
                         % (entry["work_id"], digest))
    return heading, text, len(notes), digest


def parse_epub(entry, raw):
    with zipfile.ZipFile(io.BytesIO(raw)) as archive:
        roots = []
        for name in archive.namelist():
            if not name.lower().endswith((".xhtml", ".html")):
                continue
            try:
                roots.append((name, ET.fromstring(archive.read(name))))
            except ET.ParseError as exc:
                raise ValueError("%s: invalid XHTML in %s: %s"
                                 % (entry["work_id"], name, exc))

    frontmatter = []
    footnotes = {}
    sections = []
    for name, root in roots:
        for node in root.iter():
            if local_name(node.tag) == "p":
                value = house(render(node))
                if "Titel Werk:" in value or "Titel Version:" in value:
                    frontmatter.append(value)
            if local_name(node.tag) == "li" and node.attrib.get("id", "").startswith("fn"):
                footnotes[node.attrib["id"]] = house(render(node))
            if local_name(node.tag) == "section" and has_class(node, "level2"):
                sections.append((name, node))

    frontmatter_text = " ".join(frontmatter)
    if "Titel Werk:" not in frontmatter_text or "Titel Version:" not in frontmatter_text:
        raise ValueError("%s: bibliographic record is missing" % entry["work_id"])
    source_language = BKV_LANGUAGE_NAMES.get(entry["language"])
    if not source_language:
        raise ValueError("%s: unsupported BKV language %r"
                         % (entry["work_id"], entry["language"]))
    required_metadata = (("Titel Version: " + entry["bkv_version"]),
                         "Sprache: " + source_language) + entry["metadata_markers"]
    missing_metadata = [x for x in required_metadata if x not in frontmatter_text]
    if missing_metadata:
        raise ValueError("%s: edition metadata changed or is incomplete: %s"
                         % (entry["work_id"], ", ".join(missing_metadata)))

    repair = entry.get("footnote_repair")
    if repair:
        value = footnotes.get(repair["id"], "")
        if value.count(repair["marker"]) != 1:
            raise ValueError("%s: corrupt source note marker changed"
                             % entry["work_id"])
        prefix, tail = value.split(repair["marker"], 1)
        if not prefix.endswith(repair["prefix_end"]):
            raise ValueError("%s: corrupt source note prefix changed"
                             % entry["work_id"])
        if any(marker not in tail for marker in repair["tail_markers"]):
            raise ValueError("%s: corrupt source note tail changed"
                             % entry["work_id"])
        footnotes[repair["id"]] = prefix

    supplements = entry.get("supplement_divisions", ())
    expected_epub_units = entry["units"] - len(supplements)
    if len(sections) != expected_epub_units:
        raise ValueError("%s: expected %d EPUB divisions, found %d"
                         % (entry["work_id"], expected_epub_units,
                            len(sections)))

    rows = []
    used_notes = []
    stripped_markers = []
    substitutions = entry.get("source_substitutions", ())
    substitution_counts = [0 for _ in substitutions]
    for ordinal, (_, section) in enumerate(sections, 1):
        heading_node = next((x for x in section.iter()
                             if local_name(x.tag) == "h2"), None)
        if heading_node is None:
            raise ValueError("%s: division %d has no heading"
                             % (entry["work_id"], ordinal))
        heading = house(render(heading_node))

        paragraphs = []
        for node in section.iter():
            if local_name(node.tag) == "p":
                paragraph = house(render(node))
                for position, substitution in enumerate(substitutions):
                    count = paragraph.count(substitution["from"])
                    if count:
                        paragraph = paragraph.replace(substitution["from"],
                                                      substitution["to"])
                        substitution_counts[position] += count
                for marker in entry.get("strip_terminal_markers", ()):
                    if marker in paragraph:
                        if not paragraph.endswith(marker):
                            raise ValueError("%s: scan marker moved within division %d"
                                             % (entry["work_id"], ordinal))
                        paragraph = paragraph[:-len(marker)].rstrip()
                        stripped_markers.append(marker)
                if paragraph:
                    paragraphs.append(paragraph)
        text = "\n\n".join(paragraphs)
        refs = []
        for node in section.iter():
            if local_name(node.tag) == "a" and has_class(node, "footnote-ref"):
                ref = node.attrib.get("href", "").lstrip("#")
                if not ref or ref not in footnotes:
                    raise ValueError("%s: division %d has unresolved note %r"
                                     % (entry["work_id"], ordinal, ref))
                refs.append(ref)
        used_notes.extend(refs)
        if refs:
            notes = ["[%s] %s" % (ref[2:], footnotes[ref]) for ref in refs]
            text += "\n\n" + "\n\n".join(notes)
        if not text:
            raise ValueError("%s: division %d is empty"
                             % (entry["work_id"], ordinal))
        rows.append((heading, text))

    expected_markers = list(entry.get("strip_terminal_markers", ()))
    if stripped_markers != expected_markers:
        raise ValueError("%s: expected terminal markers %r, found %r"
                         % (entry["work_id"], expected_markers,
                            stripped_markers))
    for position, substitution in enumerate(substitutions):
        if substitution_counts[position] != substitution["count"]:
            raise ValueError("%s: expected source substitution %d time(s), found %d"
                             % (entry["work_id"], substitution["count"],
                                substitution_counts[position]))

    supplement_note_count = 0
    for supplement in supplements:
        heading, text, note_count, _ = parse_division_page(entry, supplement)
        positions = [i for i, row in enumerate(rows)
                     if row[0] == supplement["before_heading"]]
        if len(positions) != 1:
            raise ValueError("%s: supplement insertion point changed"
                             % entry["work_id"])
        rows.insert(positions[0], (heading, text))
        supplement_note_count += note_count

    headings = [row[0] for row in rows]
    units = []
    for ordinal, (heading, text) in enumerate(rows, 1):
        units.append({
            "unit_id": "%s::u%02d" % (entry["work_id"], ordinal),
            "work_id": entry["work_id"],
            "work_title": entry["title"],
            "author": entry["author"],
            "source_class": entry["source_class"],
            "ordinal": ordinal,
            "citation_anchor": heading,
            "text": text,
        })

    orphan_notes = sorted(set(footnotes) - set(used_notes))
    duplicate_notes = len(used_notes) - len(set(used_notes))
    if orphan_notes or duplicate_notes:
        raise ValueError("%s: notes do not map exactly: %d orphan, %d duplicate"
                         % (entry["work_id"], len(orphan_notes), duplicate_notes))

    if headings[0] != entry["first_heading"]:
        raise ValueError("%s: first heading changed: %r"
                         % (entry["work_id"], headings[0]))
    if headings[-1] != entry["last_heading"]:
        raise ValueError("%s: last heading changed: %r"
                         % (entry["work_id"], headings[-1]))

    canonical = json.dumps({"headings": headings,
                            "texts": [x["text"] for x in units]},
                           ensure_ascii=False, separators=(",", ":"))
    digest = hashlib.sha256(canonical.encode("utf-8")).hexdigest()
    if entry["digest"] and digest != entry["digest"]:
        raise ValueError("%s: normalized source digest changed: %s"
                         % (entry["work_id"], digest))
    for unit in units:
        if "\ufffd" in unit["text"]:
            raise ValueError("%s: replacement character in division %d"
                             % (entry["work_id"], unit["ordinal"]))
        if re.search(r"[\u2010-\u2015]", unit["text"]):
            raise ValueError("%s: forbidden dash in division %d"
                             % (entry["work_id"], unit["ordinal"]))
        artifacts = []
        for pattern, label in ((r"\bPAGE\s+\d+\b", "bare PAGE marker"),
                               (r"##\s+\d", "Markdown heading"),
                               (r"\[\^\d+\]", "Markdown footnote"),
                               (r"<[^>]+>", "HTML tag"),
                               (r"https?://", "source URL")):
            if re.search(pattern, unit["text"], flags=re.I):
                artifacts.append(label)
        if artifacts:
            raise ValueError("%s: source artifacts in division %d: %s"
                             % (entry["work_id"], unit["ordinal"],
                                ", ".join(artifacts)))
    return units, digest, len(footnotes) + supplement_note_count


def work_record(entry):
    keys = ("work_id", "title", "author", "date", "translator", "pub_year",
            "source", "source_class", "description", "language", "edition_of")
    work = {key: entry[key] for key in keys}
    work["source_url"] = entry["url"]
    work["digitized"] = DIGITIZED
    work["rights"] = RIGHTS
    work["rights_url"] = RIGHTS_URL
    return work


def inherited_metadata(entry, index):
    candidates = [x for x in index
                  if x.get("work_id") == entry["edition_of"]
                  or x.get("edition_of") == entry["edition_of"]]
    base_path = OUTDIR / (entry["edition_of"] + ".json")
    if base_path.exists():
        candidates.append(json.loads(base_path.read_text(encoding="utf-8"))["work"])
    result = {}
    for field in ("saint", "is_saint", "purpose", "centuries", "century",
                  "period", "topics", "feast_day"):
        for candidate in candidates:
            if field in candidate:
                result[field] = candidate[field]
                break
    return result


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--write", action="store_true")
    parser.add_argument("--write-files-only", action="store_true")
    parser.add_argument("--check", action="store_true")
    parser.add_argument("--only", choices=[x["work_id"] for x in CATALOGUE])
    args = parser.parse_args()

    selected = [x for x in CATALOGUE
                if not args.only or x["work_id"] == args.only]
    index = json.loads(INDEX.read_text(encoding="utf-8"))
    built = []
    for entry in selected:
        try:
            units, digest, notes = parse_epub(entry, epub_for(entry))
        except (OSError, ValueError, zipfile.BadZipFile) as exc:
            print(exc)
            return 1
        work = work_record(entry)
        work.update(inherited_metadata(entry, index))
        built.append((entry, work, units))
        chars = sum(len(x["text"]) for x in units)
        print("%s: %d divisions, %d notes, %s characters, sha256 %s"
              % (entry["work_id"], len(units), notes, format(chars, ","), digest))

    if args.write or args.write_files_only:
        ids = {entry["work_id"] for entry, _, _ in built}
        for entry, work, units in built:
            output = OUTDIR / (entry["work_id"] + ".json")
            output.write_text(json.dumps({"work": work, "units": units},
                                         ensure_ascii=False, indent=1) + "\n",
                              encoding="utf-8")
            print("wrote %s" % output.relative_to(ROOT))
        if args.write:
            index = [x for x in index if x.get("work_id") not in ids]
            index.extend(work for _, work, _ in built)
            index.sort(key=lambda x: x["work_id"])
            INDEX.write_text(json.dumps(index, ensure_ascii=False, indent=1) + "\n",
                             encoding="utf-8")
            print("updated %s" % INDEX.relative_to(ROOT))
    elif args.check:
        failed = False
        by_id = {x.get("work_id"): x for x in index}
        for entry, work, units in built:
            output = OUTDIR / (entry["work_id"] + ".json")
            expected = {"work": work, "units": units}
            try:
                actual = json.loads(output.read_text(encoding="utf-8"))
            except (OSError, ValueError) as exc:
                print("stale or missing %s: %s" %
                      (output.relative_to(ROOT), exc))
                failed = True
            else:
                if actual != expected:
                    print("stale %s" % output.relative_to(ROOT))
                    failed = True
            indexed_work = by_id.get(entry["work_id"])
            if indexed_work is None or any(
                    indexed_work.get(key) != value
                    for key, value in work.items()):
                print("stale catalogue record: %s" % entry["work_id"])
                failed = True
        if failed:
            print("run with --write to refresh checked-in outputs")
            return 1
    else:
        print("nothing written; pass --write")
    return 0


if __name__ == "__main__":
    sys.exit(main())
