#!/usr/bin/env python3
"""Ingest complete public domain BKV editions from the University of Fribourg.

The Bibliothek der Kirchenväter site publishes downloadable EPUB files for
many older German and French editions. Each catalogue entry below names the
exact BKV version page and the known number of divisions. The builder fetches
the EPUB, keeps every division and its notes, removes only scan page markers,
and stops if the source structure or normalized text has changed.

BKV's copyright notice says, to the editor's knowledge, that its texts are no
longer protected by copyright and may be used freely. These 1913 and 1918
editions are public domain. The source and digitizer remain in every record.

    python3 tools/ingest_bkv.py --check
    python3 tools/ingest_bkv.py --write
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
        "digest": "654b7b10cd0dbf4044f48740e416a04662d5e0a7305a8969a2b67b09e511f6ec",
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
        "digest": "d92dc0a26f4c2cd2d0050c82c0b894291497f28a455372e8e42e2b8df71b07ee",
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
        "units": 17,
        "first_heading": "1.",
        "last_heading": "18.",
        "digest": "c5c4d19b0291e1497ae002776583e0eef54e42bf436edbababfa543ebd88798c",
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
    required_metadata = (("Titel Version: " + entry["bkv_version"]),
                         "Sprache: deutsch") + entry["metadata_markers"]
    missing_metadata = [x for x in required_metadata if x not in frontmatter_text]
    if missing_metadata:
        raise ValueError("%s: edition metadata changed or is incomplete: %s"
                         % (entry["work_id"], ", ".join(missing_metadata)))

    if len(sections) != entry["units"]:
        raise ValueError("%s: expected %d divisions, found %d"
                         % (entry["work_id"], entry["units"], len(sections)))

    headings = []
    units = []
    used_notes = []
    for ordinal, (_, section) in enumerate(sections, 1):
        heading_node = next((x for x in section.iter()
                             if local_name(x.tag) == "h2"), None)
        if heading_node is None:
            raise ValueError("%s: division %d has no heading"
                             % (entry["work_id"], ordinal))
        heading = house(render(heading_node))
        headings.append(heading)

        paragraphs = []
        for node in section.iter():
            if local_name(node.tag) == "p":
                paragraph = house(render(node))
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
    return units, digest, len(footnotes)


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

    if args.write:
        ids = {entry["work_id"] for entry, _, _ in built}
        for entry, work, units in built:
            output = OUTDIR / (entry["work_id"] + ".json")
            output.write_text(json.dumps({"work": work, "units": units},
                                         ensure_ascii=False, indent=1) + "\n",
                              encoding="utf-8")
            print("wrote %s" % output.relative_to(ROOT))
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
            if by_id.get(entry["work_id"]) != work:
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
