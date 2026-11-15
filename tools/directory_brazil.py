#!/usr/bin/env python3
"""Validated current Eastern Orthodox directory fragments for Brazil.

Only bodies named by a competent current Church source are emitted. Search
results, historical bodies, and bodies lacking current jurisdictional
confirmation remain in the companion candidate ledger.

    python tools/directory_brazil.py --check
    python tools/directory_brazil.py --dump
"""

import argparse
import json
import re
import sys
from pathlib import Path


CHECKED = "2026-11-15"
ROOT = Path(__file__).resolve().parent.parent
CANDIDATE_LEDGER = ROOT / "tools" / "directory_candidates" / "brazil.json"

EP_GREEK = (
    "https://www.paroquia-ortodoxa-grega-rj.org/"
    "NOTA_ARQUIDIOCESE_2024.pdf"
)
ANTIOCH_PARISHES = "https://www.arquidioceseortodoxa.com.br/par%C3%B3quias"
ANTIOCH_CATHEDRAL = "https://www.arquidioceseortodoxa.com.br/hist%C3%B3rico"
ANTIOCH_VICARIATES = "https://www.antiochpatriarchate.org/en/category/108/"
EP_UKRAINIANS = (
    "https://ec-patr.org/entities/orthodoksoi-oykranoi-stis-ipa/"
)
MOSCOW_ROSTER = "https://southamerica.cerkov.ru/xramy-eparxii/"
MOSCOW_DIOCESE = "https://patriarchia.ru/org/141"
SERBIAN_DIRECTORY = (
    "https://www.iglesiaortodoxaserbiasca.org/_files/ugd/"
    "e8757a_bcd3fd85dc81441196589a1b3065f8bd.pdf"
)
SERBIAN_DIOCESE = "https://www.iglesiaortodoxaserbiasca.org/diocesis"
POLISH_DIRECTORY = (
    "https://www.orthodox.pl/administracja/diecezje/"
    "koscielne-jednostki-zagraniczne/"
)
ROCOR_DIRECTORY = "https://directory.synod.com/listings/"
ROCOR_DIOCESE = "https://iglesiarusa.info/"


def body(row_id, parent, name, local, rank, sources, address=None,
         site=None, kind="parish"):
    row = {
        "id": row_id,
        "parent": parent,
        "kind": kind,
        "rank": rank,
        "name": name,
        "local": local,
        "country": "BR",
        "sources": sources,
    }
    if address:
        row["address"] = address
    if site:
        row["site"] = site
    return row


EP_GREEK_ROWS = [
    body(
        "br-ep-brasilia-annunciation", "ep-buenos-aires",
        "Annunciation of the Theotokos Church in Brasília",
        "Igreja da Anunciação da Theotokos", "Church", [EP_GREEK],
        ["SGAN Quadra 910, Módulo B", "Brasília, DF 70790-100, Brazil"],
    ),
    body(
        "br-ep-sao-paulo-saint-peter-cathedral", "ep-buenos-aires",
        "Cathedral Church of Saint Peter in São Paulo",
        "Igreja Catedral de São Pedro", "Cathedral Parish", [EP_GREEK],
        ["Rua Bresser 793", "São Paulo, SP 03053-000, Brazil"],
    ),
    body(
        "br-ep-sao-paulo-dormition", "ep-buenos-aires",
        "Dormition of the Theotokos Church in São Paulo",
        "Igreja da Dormição da Theotokos", "Church", [EP_GREEK],
        ["Rua Albuquerque Maranhão 211, Cambuci",
         "São Paulo, SP 01540-020, Brazil"],
    ),
    body(
        "br-ep-florianopolis-saint-nicholas", "ep-buenos-aires",
        "Saint Nicholas Church in Florianópolis",
        "Igreja de São Nicolau", "Church", [EP_GREEK],
        ["Rua Tenente Silveira 494", "Florianópolis, SC 88010-301, Brazil"],
    ),
    body(
        "br-ep-sao-jose-john-theologian", "ep-buenos-aires",
        "Saint John the Theologian Church in São José",
        "Igreja de São João, o Teólogo", "Church", [EP_GREEK],
        ["Rua Francisco Inácio do Nascimento 470, Forquilhas",
         "São José, SC 88107-500, Brazil"],
    ),
    body(
        "br-ep-curitiba-saint-savvas", "ep-buenos-aires",
        "Saint Savvas Church in Curitiba",
        "Igreja de São Savas", "Church", [EP_GREEK],
        ["Rua Comendador Lustosa da Andrade 198, Bom Retiro",
         "Curitiba, PR 80520-350, Brazil"],
    ),
    body(
        "br-ep-porto-alegre-holy-apostles", "ep-buenos-aires",
        "Holy Apostles Church in Porto Alegre",
        "Igreja dos Santos Apóstolos", "Church", [EP_GREEK],
        ["Rua Monteiro Lobato 312", "Porto Alegre, RS, Brazil"],
    ),
    body(
        "br-ep-rio-saint-andrew", "ep-buenos-aires",
        "Saint Andrew Church in Rio de Janeiro",
        "Igreja de Santo André", "Church", [EP_GREEK],
        ["Rua Darke Mattos 46, Higienópolis",
         "Rio de Janeiro, RJ 21051-470, Brazil"],
    ),
    body(
        "br-ep-vitoria-saint-george", "ep-buenos-aires",
        "Saint George Church in Vitória",
        "Igreja de São Jorge", "Church", [EP_GREEK],
        ["Rua de Grécia 267, Praia do Canto", "Vitória, ES, Brazil"],
    ),
    body(
        "br-ep-goiania-peter-paul", "ep-buenos-aires",
        "Saints Peter and Paul Church in Goiânia",
        "Igreja de São Pedro e São Paulo", "Church", [EP_GREEK],
        ["Rua F 212, Quadra 513, Lote 22, Casa 01, Jardim América",
         "Goiânia, GO 74270-250, Brazil"],
    ),
    body(
        "br-ep-rio-pavuna-peter-paul", "ep-buenos-aires",
        "Holy Apostles Peter and Paul Church in Pavuna",
        "Igreja dos Santos Apóstolos Pedro e Paulo", "Church", [EP_GREEK],
        ["Rua Juerana 169, Pavuna", "Rio de Janeiro, RJ 21521-450, Brazil"],
    ),
    body(
        "br-ep-salvador-protection-mission", "ep-buenos-aires",
        "Protection of the Most Holy Mother of God Mission in Salvador",
        "Missão Ortodoxa da Proteção da Mãe de Deus Santíssima",
        "Mission", [EP_GREEK],
        ["Rua Juiz Orlando de Melo 61, Piatã", "Salvador, BA, Brazil"],
    ),
    body(
        "br-ep-jaragua-saint-nectarios-mission", "ep-buenos-aires",
        "Saint Nectarios Orthodox Mission in Jaraguá do Sul",
        "Missão Ortodoxa São Nectários", "Mission", [EP_GREEK],
        ["Jaraguá do Sul, SC, Brazil"],
    ),
]


ANTIOCH_SAO_PAULO_ROWS = [
    body(
        "br-an-sao-paulo-saint-paul-cathedral", "an-sao-paulo",
        "Orthodox Cathedral of Saint Paul in São Paulo",
        "Catedral Ortodoxa de São Paulo", "Cathedral Parish",
        [ANTIOCH_CATHEDRAL, ANTIOCH_PARISHES],
        ["Rua Vergueiro 1515, Paraíso", "São Paulo, SP 04101-000, Brazil"],
        site="https://www.arquidioceseortodoxa.com.br/",
    ),
    body(
        "br-an-sao-paulo-annunciation", "an-sao-paulo",
        "Annunciation to Our Lady Antiochian Orthodox Church in São Paulo",
        "Igreja Ortodoxa Antioquina da Anunciação a Nossa Senhora",
        "Church", [ANTIOCH_PARISHES],
        ["Rua Cavalheiro Basílio Jafet 115, Centro",
         "São Paulo, SP 01022-020, Brazil"],
    ),
    body(
        "br-an-sao-paulo-lar-sirio-saint-george", "an-sao-paulo",
        "Saint George Orthodox Chapel at Lar Sírio in São Paulo",
        "Capela Ortodoxa São Jorge (Lar Sírio Pró-Infância)", "Chapel",
        [ANTIOCH_PARISHES],
        ["Rua Serra da Bragança 1086, Tatuapé",
         "São Paulo, SP 03318-000, Brazil"],
    ),
    body(
        "br-an-sao-paulo-father-ibrahim-chapel", "an-sao-paulo",
        "Father Ibrahim Orthodox Chapel at Asilo Mão Branca in São Paulo",
        "Capela Ortodoxa 'Pe. Ibrahim' (Asilo Mão Branca)", "Chapel",
        [ANTIOCH_PARISHES],
        ["Avenida Santo Amaro 6487, Santo Amaro",
         "São Paulo, SP 04701-100, Brazil"],
    ),
    body(
        "br-an-sao-jose-rio-preto-saint-george", "an-sao-paulo",
        "Saint George Orthodox Parish in São José do Rio Preto",
        "Paróquia Ortodoxa São Jorge (de São José do Rio Preto)",
        "Parish", [ANTIOCH_PARISHES],
        ["Rua Marechal Deodoro 2827, Centro",
         "São José do Rio Preto, SP 15010-070, Brazil"],
    ),
    body(
        "br-an-santos-saint-george", "an-sao-paulo",
        "Saint George Orthodox Parish in Santos",
        "Paróquia Ortodoxa São Jorge (de Santos)", "Parish",
        [ANTIOCH_PARISHES],
        ["Avenida Ana Costa 323, Encruzilhada",
         "Santos, SP 11060-001, Brazil"],
    ),
    body(
        "br-an-bariri-saint-george", "an-sao-paulo",
        "Saint George Orthodox Parish in Bariri",
        "Paróquia Ortodoxa São Jorge (de Bariri)", "Parish",
        [ANTIOCH_PARISHES],
        ["Rua João Lemos 687, Centro", "Bariri, SP 17250-000, Brazil"],
    ),
    body(
        "br-an-lins-our-lady-tsambika", "an-sao-paulo",
        "Our Lady of Tsambika Orthodox Parish in Lins",
        "Paróquia Ortodoxa Nossa Senhora Tsambica (de Lins)", "Parish",
        [ANTIOCH_PARISHES],
        ["Rua Campos Sales 980, Centro", "Lins, SP 16400-000, Brazil"],
    ),
    body(
        "br-an-campinas-community", "an-sao-paulo",
        "Orthodox Community in Campinas",
        "Comunidade Ortodoxa de Campinas", "Community",
        [ANTIOCH_PARISHES], ["Campinas, SP, Brazil"],
    ),
    body(
        "br-an-piracicaba-community", "an-sao-paulo",
        "Orthodox Community in Piracicaba",
        "Comunidade Ortodoxa de Piracicaba", "Community",
        [ANTIOCH_PARISHES], ["Piracicaba, SP, Brazil"],
    ),
    body(
        "br-an-curitiba-saint-george", "an-sao-paulo",
        "Saint George Orthodox Parish in Curitiba",
        "Paróquia Ortodoxa São Jorge (de Curitiba)", "Parish",
        [ANTIOCH_PARISHES],
        ["Rua Brigadeiro Franco 375, Mercês",
         "Curitiba, PR 80430-210, Brazil"],
    ),
    body(
        "br-an-recife-saint-george-community", "an-sao-paulo",
        "Saint George Orthodox Community in Recife",
        "Comunidade Ortodoxa São Jorge (de Recife)", "Community",
        [ANTIOCH_PARISHES], ["Recife, PE, Brazil"],
    ),
    body(
        "br-an-anapolis-saint-george", "an-sao-paulo",
        "Saint George Orthodox Parish in Anápolis",
        "Paróquia Ortodoxa São Jorge (de Anápolis)", "Parish",
        [ANTIOCH_PARISHES],
        ["Rua Engenheiro Portela 651, Centro",
         "Anápolis, GO 75024-100, Brazil"],
    ),
    body(
        "br-an-goiania-saint-nicholas", "an-sao-paulo",
        "Saint Nicholas Orthodox Parish in Goiânia",
        "Paróquia Ortodoxa São Nicolau (de Goiânia)", "Parish",
        [ANTIOCH_PARISHES],
        ["Avenida A 195, Setor Oeste", "Goiânia, GO 74110-020, Brazil"],
    ),
    body(
        "br-an-ipameri-john-baptist", "an-sao-paulo",
        "Saint John the Baptist Orthodox Parish in Ipameri",
        "Paróquia Ortodoxa São João Batista (de Ipameri)", "Parish",
        [ANTIOCH_PARISHES],
        ["Rua Major Piranema 28, Centro", "Ipameri, GO, Brazil"],
    ),
    body(
        "br-an-catalao-community", "an-sao-paulo",
        "Antiochian Orthodox Community in Catalão",
        "Comunidade Ortodoxa Antioquina de Catalão", "Community",
        [ANTIOCH_PARISHES], ["Catalão, GO, Brazil"],
    ),
    body(
        "br-an-araguari-john-chrysostom", "an-sao-paulo",
        "Saint John Chrysostom Antiochian Orthodox Community in Araguari",
        "Comunidade Ortodoxa Antioquina São João Crisóstomo (de Araguari)",
        "Community", [ANTIOCH_PARISHES], ["Araguari, MG, Brazil"],
    ),
    body(
        "br-an-belo-horizonte-saint-george", "an-sao-paulo",
        "Saint George Orthodox Parish in Belo Horizonte",
        "Paróquia Ortodoxa São Jorge (de Belo Horizonte)", "Parish",
        [ANTIOCH_PARISHES],
        ["Rua Olegário Maciel 321, Centro",
         "Belo Horizonte, MG 30180-113, Brazil"],
    ),
    body(
        "br-an-guaxupe-prophet-elias", "an-sao-paulo",
        "Holy Prophet Elias Orthodox Parish in Guaxupé",
        "Paróquia Ortodoxa Santo Profeta Elias (de Guaxupé)", "Parish",
        [ANTIOCH_PARISHES],
        ["Rua Aparecida 227, Centro", "Guaxupé, MG 37800-000, Brazil"],
    ),
    body(
        "br-an-brasilia-saint-george", "an-sao-paulo",
        "Saint George Orthodox Parish in Brasília",
        "Paróquia Ortodoxa São Jorge (de Brasília)", "Parish",
        [ANTIOCH_PARISHES],
        ["SHIS QI 09, Área Especial C, Lote P, Lago Sul",
         "Brasília, DF 71625-009, Brazil"],
    ),
]


UKRAINIAN_ROWS = [
    body(
        "br-epukr-curitiba-demetrios-cathedral",
        "ep-ukrainian-south-america",
        "Saint Demetrios Cathedral in Curitiba", "Catedral São Demétrio",
        "Cathedral Parish", [EP_UKRAINIANS], ["Curitiba, PR, Brazil"],
    ),
    body(
        "br-epukr-papanduva-volodymyr", "ep-ukrainian-south-america",
        "Saint Volodymyr the Great Parish in Papanduva",
        "São Valdomiro Magno", "Parish", [EP_UKRAINIANS],
        ["Papanduva, SC, Brazil"],
    ),
    body(
        "br-epukr-gurarany-cosmas-damian", "ep-ukrainian-south-america",
        "Saints Cosmas and Damian Parish in Gurarany",
        "SS. Cosme e Damião", "Parish", [EP_UKRAINIANS],
        ["Gurarany, SC, Brazil"],
    ),
    body(
        "br-epukr-jangada-holy-spirit", "ep-ukrainian-south-america",
        "Holy Spirit Parish in Jangada", "Espírito Santo", "Parish",
        [EP_UKRAINIANS], ["Jangada, SC, Brazil"],
    ),
    body(
        "br-epukr-xaxim-jangada-dormition", "ep-ukrainian-south-america",
        "Dormition of the Holy Mother of God Parish in Xaxim Jangada",
        "Dormição da Santa Mãe de Deus", "Parish", [EP_UKRAINIANS],
        ["Xaxim Jangada, SC, Brazil"],
    ),
    body(
        "br-epukr-vila-zulmira-john-baptist", "ep-ukrainian-south-america",
        "Saint John the Baptist Parish in Vila Zulmira",
        "São João Batista", "Parish", [EP_UKRAINIANS],
        ["Vila Zulmira, União da Vitória, PR, Brazil"],
    ),
    body(
        "br-epukr-uniao-vitoria-divine-providence",
        "ep-ukrainian-south-america",
        "Divine Providence Parish in União da Vitória",
        "Divina Providência", "Parish", [EP_UKRAINIANS],
        ["União da Vitória, PR, Brazil"],
    ),
    body(
        "br-epukr-joaquim-tavora-nicholas", "ep-ukrainian-south-america",
        "Saint Nicholas Parish in Joaquim Távora", "São Nicolau", "Parish",
        [EP_UKRAINIANS], ["Joaquim Távora, PR, Brazil"],
    ),
    body(
        "br-epukr-goncalves-junior-peter-paul",
        "ep-ukrainian-south-america",
        "Saints Peter and Paul Parish in Gonçalves Júnior",
        "SS. Pedro e Paulo", "Parish", [EP_UKRAINIANS],
        ["Gonçalves Júnior, Irati, PR, Brazil"],
    ),
    body(
        "br-epukr-curitiba-archangel-michael", "ep-ukrainian-south-america",
        "Archangel Michael Parish in Curitiba", "São Miguel Arcanjo",
        "Parish", [EP_UKRAINIANS], ["Curitiba, PR, Brazil"],
    ),
    body(
        "br-epukr-vila-burei-archangel-michael",
        "ep-ukrainian-south-america",
        "Archangel Michael Parish in Vila Burei", "São Miguel Arcanjo",
        "Parish", [EP_UKRAINIANS], ["Vila Burei, Palmital, PR, Brazil"],
    ),
    body(
        "br-epukr-ponta-grossa-george", "ep-ukrainian-south-america",
        "Saint George Parish in Ponta Grossa", "São Jorge", "Parish",
        [EP_UKRAINIANS], ["Ponta Grossa, PR, Brazil"],
    ),
    body(
        "br-epukr-osasco-protection", "ep-ukrainian-south-america",
        "Protection of the Holy Mother of God Parish in Osasco",
        "Proteção da Santa Mãe de Deus", "Parish", [EP_UKRAINIANS],
        ["Osasco, SP, Brazil"],
    ),
    body(
        "br-epukr-sao-caetano-protection", "ep-ukrainian-south-america",
        "Protection of the Holy Mother of God Parish in São Caetano do Sul",
        "Proteção da Santa Mãe de Deus", "Parish", [EP_UKRAINIANS],
        ["São Caetano do Sul, SP, Brazil"],
    ),
    body(
        "br-epukr-sao-caetano-volodymyr", "ep-ukrainian-south-america",
        "Saint Volodymyr the Great Parish in São Caetano do Sul",
        "São Valdomiro Magno", "Parish", [EP_UKRAINIANS],
        ["São Caetano do Sul, SP, Brazil"],
    ),
    body(
        "br-epukr-apucarana-protection", "ep-ukrainian-south-america",
        "Protection of the Holy Mother of God Parish in Apucarana",
        "Proteção da Santa Mãe de Deus", "Parish", [EP_UKRAINIANS],
        ["Apucarana, PR, Brazil"],
    ),
    body(
        "br-epukr-colonia-nova-ucrania-holy-spirit",
        "ep-ukrainian-south-america",
        "Holy Spirit Parish in Colônia Nova Ucrânia", "Espírito Santo",
        "Parish", [EP_UKRAINIANS],
        ["Colônia Nova Ucrânia, Apucarana, PR, Brazil"],
    ),
    body(
        "br-epukr-canoas-holy-trinity", "ep-ukrainian-south-america",
        "Holy Trinity Parish in Canoas", "SS. Trindade", "Parish",
        [EP_UKRAINIANS], ["Canoas, RS, Brazil"],
    ),
]


MOSCOW_ROWS = [
    body(
        "br-ru-rio-zinaida", "ru-argentina-and-south-america",
        "Holy Martyr Zinaida Church in Rio de Janeiro",
        "Храм святой мученицы Зинаиды в Рио-де-Жанейро", "Church",
        [MOSCOW_ROSTER, MOSCOW_DIOCESE],
        ["Rua Monte Alegre 210, Santa Teresa",
         "Rio de Janeiro, RJ 20240-190, Brazil"],
    ),
    body(
        "br-ru-rio-protection-mission", "ru-argentina-and-south-america",
        "Protection of the Most Holy Theotokos Mission in Rio de Janeiro",
        "Миссия Покрова Пресвятой Богородицы в Рио-де-Жанейро", "Mission",
        [MOSCOW_ROSTER, MOSCOW_DIOCESE],
        ["Rua Monte Alegre 210, Santa Teresa",
         "Rio de Janeiro, RJ 20240-190, Brazil"],
    ),
    body(
        "br-ru-sao-paulo-annunciation", "ru-argentina-and-south-america",
        "Annunciation of the Mother of God Church in São Paulo",
        "Храм Благовещения Божией Матери в Сан-Паулу", "Church",
        [MOSCOW_ROSTER, MOSCOW_DIOCESE],
        ["Rua dos Sorocabanos 100, Ipiranga", "São Paulo, SP, Brazil"],
    ),
    body(
        "br-ru-brasilia-hodegetria", "ru-argentina-and-south-america",
        "Hodegetria Icon of the Mother of God Church in Brasília",
        "Храм в честь иконы Божией Матери \"Одигитрия\" в Бразилиа",
        "Church", [MOSCOW_ROSTER, MOSCOW_DIOCESE],
        ["Avenida das Nações, Acampamento Saturnino de Brito, Lote 09",
         "Brasília, DF 70210-550, Brazil"],
    ),
    body(
        "br-ru-porto-alegre-sergius", "ru-argentina-and-south-america",
        "Saint Sergius of Radonezh Church in Porto Alegre",
        "Храм преподобного Сергия Радонежского в Порту-Алегри", "Church",
        [MOSCOW_ROSTER, MOSCOW_DIOCESE],
        ["Avenida General Lucie Esteves 215",
         "Porto Alegre, RS 91030-310, Brazil"],
    ),
    body(
        "br-ru-santa-rosa-peter-paul", "ru-argentina-and-south-america",
        "Holy Chief Apostles Peter and Paul Church in Santa Rosa",
        "Храм святых первоверховных апостолов Петра и Павла в Санта Розе",
        "Church", [MOSCOW_ROSTER, MOSCOW_DIOCESE],
        ["Rua R. Barbosa 175", "Santa Rosa, RS, Brazil"],
    ),
    body(
        "br-ru-campina-missoes-john-theologian",
        "ru-argentina-and-south-america",
        "Holy Apostle and Evangelist John the Theologian Church in Campina das Missões",
        "Храм святого апостола и евангелиста Иоанна Богослова в Кампина-дас-Мисойнс",
        "Church", [MOSCOW_ROSTER, MOSCOW_DIOCESE],
        ["Linha Paca Sul", "Campina das Missões, RS 98975-000, Brazil"],
    ),
    body(
        "br-ru-manaus-faith-hope-love-sophia",
        "ru-argentina-and-south-america",
        "Community of the Holy Martyrs Faith, Hope, Love and Their Mother Sophia in Manaus",
        "Община во имя святых мучениц Веры, Надежды, Любови и матери их Софии в Манаусе",
        "Community", [MOSCOW_ROSTER, MOSCOW_DIOCESE],
        ["Manaus, AM, Brazil"],
    ),
    body(
        "br-ru-recife-apostle-matthew", "ru-argentina-and-south-america",
        "Holy Apostle and Evangelist Matthew Church in Recife",
        "Храм святого апостола и евангелиста Матфея г. Ресифи", "Church",
        [MOSCOW_ROSTER, MOSCOW_DIOCESE],
        ["Rua Zelindo Marafante 150, Piedade",
         "Jaboatão dos Guararapes, PE 54400-370, Brazil"],
    ),
]


SERBIAN_ROWS = [
    body(
        "br-sr-recife-dormition", "sr-buenos-aires",
        "Dormition of the Mother of God Parish in Recife",
        "Paróquia Dormição da Mãe de Deus", "Parish",
        [SERBIAN_DIRECTORY, SERBIAN_DIOCESE],
        ["Avenida Flor de Santana 77, Parnamirim",
         "Recife, PE 52060-290, Brazil"],
    ),
    body(
        "br-sr-bom-conselho-transfiguration", "sr-buenos-aires",
        "Transfiguration of the Lord Mission in Bom Conselho",
        "Misión de la Transfiguración del Señor", "Mission",
        [SERBIAN_DIRECTORY, SERBIAN_DIOCESE],
        ["Sítio de Cancelas", "Bom Conselho, PE, Brazil"],
    ),
    body(
        "br-sr-camaragibe-holy-trinity-monastery", "sr-buenos-aires",
        "Holy Trinity Orthodox Monastery in Camaragibe",
        "Mosteiro Ortodoxo da Santíssima Trindade", "Monastery",
        [SERBIAN_DIRECTORY, SERBIAN_DIOCESE],
        ["Estrada de Aldeia, Km 5.8", "Camaragibe, PE 54792-990, Brazil"],
        kind="monastery",
    ),
    body(
        "br-sr-caruaru-john-chrysostom", "sr-buenos-aires",
        "Saint John Chrysostom Parish in Caruaru",
        "Paróquia São João Crisóstomo", "Parish",
        [SERBIAN_DIRECTORY, SERBIAN_DIOCESE],
        ["Vila Encanto, s/n", "Caruaru, PE 55032-580, Brazil"],
    ),
    body(
        "br-sr-belo-jardim-anthony-great", "sr-buenos-aires",
        "Saint Anthony the Great Parish in Belo Jardim",
        "Paróquia Santo Antônio, o Grande", "Parish",
        [SERBIAN_DIRECTORY, SERBIAN_DIOCESE],
        ["Loteamento Viana Moura, s/n", "Belo Jardim, PE, Brazil"],
    ),
    body(
        "br-sr-sao-paulo-peter-paul", "sr-buenos-aires",
        "Saints Peter and Paul Missionary Parish in Campinas and São Paulo",
        "Paróquia Missionária São Pedro e São Paulo", "Parish",
        [SERBIAN_DIRECTORY, SERBIAN_DIOCESE],
        ["Campinas and São Paulo, SP, Brazil"],
    ),
    body(
        "br-sr-raposa-james-brother-lord", "sr-buenos-aires",
        "Saint James the Brother of the Lord Parish in Raposa",
        "Parroquia Santiago Hermano del Señor, el Justo", "Parish",
        [SERBIAN_DIRECTORY, SERBIAN_DIOCESE],
        ["Avenida Régia 19A, Vila Laci", "Raposa, MA 65138-000, Brazil"],
    ),
    body(
        "br-sr-sao-luis-archangel-michael", "sr-buenos-aires",
        "Archangel Michael Orthodox Mission in São Luís",
        "Misión Ortodoxa San Miguel Arcángel", "Mission",
        [SERBIAN_DIRECTORY, SERBIAN_DIOCESE],
        ["Rua Carlos Macieira, Quadra 26, Casa 02, Bairro Coroado",
         "São Luís, MA, Brazil"],
    ),
    body(
        "br-sr-natal-cosmas-damian", "sr-buenos-aires",
        "Saints Cosmas and Damian Mission in Natal",
        "Misión Santos Cosme y Damián", "Mission",
        [SERBIAN_DIRECTORY, SERBIAN_DIOCESE],
        ["Avenida Afonso Pena 534, Petrópolis", "Natal, RN, Brazil"],
    ),
    body(
        "br-sr-maceio-basil-ostrog", "sr-buenos-aires",
        "Saint Basil of Ostrog Mission in Maceió",
        "Misión San Basilio de Ostrog", "Mission",
        [SERBIAN_DIRECTORY, SERBIAN_DIOCESE],
        ["Reserva Bella Vista, F2 no. 145, Bairro Antares",
         "Maceió, AL, Brazil"],
    ),
]


POLISH_ROWS = [
    body(
        "br-pl-rio-most-holy-virgin-cathedral", "pl-rio-recife",
        "Cathedral of the Most Holy Virgin Mary in Rio de Janeiro",
        "Sobór Katedralny pw. Najświętszej Dziewicy Marii",
        "Cathedral Parish", [POLISH_DIRECTORY],
        ["Rua Saint Romain 226, Copacabana",
         "Rio de Janeiro, RJ 22071-060, Brazil"],
    ),
    body(
        "br-pl-cordeiro-john-forerunner", "pl-rio-recife",
        "Saint John the Forerunner Parish in Cordeiro",
        "Paróquia de São João o Precurssor", "Parish", [POLISH_DIRECTORY],
        ["Rua Dr. José Teixeira Portugal 181",
         "Cordeiro, RJ 28540-000, Brazil"],
    ),
    body(
        "br-pl-rio-benedict-nursia", "pl-rio-recife",
        "Saint Benedict of Nursia Parish in Rio de Janeiro",
        "Paróquia de São Bento de Núrsia", "Parish", [POLISH_DIRECTORY],
        ["Estrada do Cacuia 1198, Cacuia, Ilha do Governador",
         "Rio de Janeiro, RJ 21921-001, Brazil"],
    ),
    body(
        "br-pl-marica-george-mission", "pl-rio-recife",
        "Saint George the Victorious Mission in Maricá",
        "Missão de São Jorge o Vitorioso", "Mission", [POLISH_DIRECTORY],
        ["Rua Manoel Victor Marques, Lote 23, Araçatiba",
         "Maricá, RJ 24900-000, Brazil"],
    ),
    body(
        "br-pl-conde-catherine", "pl-rio-recife",
        "Saint Catherine the Great Parish in Conde",
        "Paróquia de Santa Catarina a Grande", "Parish", [POLISH_DIRECTORY],
        ["Sítio Alexandria, s/n, Pousada do Conde, Km 97.5, BR 101",
         "Conde, PB, Brazil"],
    ),
    body(
        "br-pl-recife-theophany", "pl-rio-recife",
        "Theophany of the Lord Parish in Recife",
        "Paróquia da Teofania do Senhor", "Parish", [POLISH_DIRECTORY],
        ["Rua Felipe Guerra 10, Várzea", "Recife, PE 50980-380, Brazil"],
    ),
    body(
        "br-pl-guarabira-peter-paul", "pl-rio-recife",
        "Saints Peter and Paul Parish in Guarabira",
        "Paróquia de São Pedro e São Paulo", "Parish", [POLISH_DIRECTORY],
        ["Rua Projetada, s/n, Alto da Boa Vista, Distrito do Pirpiri",
         "Guarabira, PB 58200-000, Brazil"],
    ),
    body(
        "br-pl-raposa-james-apostle", "pl-rio-recife",
        "Saint James the Apostle Parish in Raposa",
        "Paróquia de São Thiago Apóstolo", "Parish", [POLISH_DIRECTORY],
        ["Avenida Régia 19, Vila Laci", "Raposa, MA 65138-000, Brazil"],
    ),
    body(
        "br-pl-catole-anthony-mission", "pl-rio-recife",
        "Saint Anthony Mission in Catolé",
        "Missão de Santo Antônio", "Mission", [POLISH_DIRECTORY],
        ["Sítio Catolé, s/n, Zona Rural do Município de Mamanguape, BR 101",
         "Catolé, PB 58280-000, Brazil"],
    ),
    body(
        "br-pl-rio-tinto-protection-mission", "pl-rio-recife",
        "Protection of the Most Holy Virgin Mary Mission in Rio Tinto",
        "Missão da Proteção da Santíssima Virgem Maria", "Mission",
        [POLISH_DIRECTORY],
        ["Aldeia de Silva de Belém, s/n, Zona Rural do Município de Rio Tinto, BR 101",
         "Rio Tinto, PB 58297-000, Brazil"],
    ),
    body(
        "br-pl-sumare-elizabeth-mission", "pl-rio-recife",
        "New Martyr Elizabeth Mission in Sumaré",
        "Missão da Nova Mártir Elisabeth", "Mission", [POLISH_DIRECTORY],
        ["Avenida Ipê Amarelo 415, Casa 91, Condomínio Acácias, Parque Vila Flores",
         "Sumaré, SP 13175-667, Brazil"],
    ),
    body(
        "br-pl-conde-nicholas-monastery", "pl-rio-recife",
        "Saint Nicholas of Myra Orthodox Monastery in Conde",
        "Mosteiro Ortodoxo de São Nicolau de Mira", "Monastery",
        [POLISH_DIRECTORY],
        ["Sítio Alexandria, s/n, Pousada do Conde, Km 97.5, BR 101",
         "Conde, PB, Brazil"], kind="monastery",
    ),
]


def rocor(row_id, name, local, rank, address, listing):
    return body(
        row_id, "ru-south-america-rocor", name, local, rank,
        [listing, ROCOR_DIRECTORY, ROCOR_DIOCESE], address,
    )


ROCOR_ROWS = [
    rocor(
        "br-rocor-sao-paulo-nicholas-cathedral",
        "Saint Nicholas Orthodox Cathedral Parish in São Paulo",
        "Paróquia da Catedral Ortodoxa de São Nicolau", "Cathedral Parish",
        ["Rua Tamandaré 710", "São Paulo, SP 01525-000, Brazil"],
        "https://directory.synod.com/listing/61/raroquia-da-catedral-ortodoxa-de-sao-nicolau/",
    ),
    rocor(
        "br-rocor-niteroi-protection",
        "Protection of Our Lady Parish in Niterói",
        "Paróquia da Proteção de Nossa Senhora", "Parish",
        ["Avenida Anita Nilo Peçanha", "Niterói, RJ 24210-480, Brazil"],
        "https://directory.synod.com/listing/57/raroquia-da-rrotecao-de-nossa-senhora/",
    ),
    rocor(
        "br-rocor-vila-zelina-protection",
        "Protection of Our Lady Parish in Vila Zelina",
        "Paróquia da Proteção de Nossa Senhora", "Parish",
        ["Rua Montojo 15, Vila Zelina", "São Paulo, SP 03152, Brazil"],
        "https://directory.synod.com/listing/63/raroquia-da-rrotecao-de-nossa-senhora/",
    ),
    rocor(
        "br-rocor-vila-alpina-holy-trinity",
        "Holy Trinity Parish in Vila Alpina",
        "Paróquia da Santíssima Trindade", "Parish",
        ["Rua Paratiquara 151, Vila Alpina",
         "São Paulo, SP 03209-040, Brazil"],
        "https://directory.synod.com/listing/62/raroquia-da-santissima-trindade/",
    ),
    rocor(
        "br-rocor-balneario-mar-paulista-protection",
        "Protection of Our Lady Parish in Balneário Mar Paulista",
        "Paróquia de Nossa Senhora da Proteção", "Parish",
        ["Rua Mariana Borges 229, Balneário Mar Paulista",
         "São Paulo, SP 04463-190, Brazil"],
        "https://directory.synod.com/listing/60/raroquia-de-nossa-senhora-da-protecao/",
    ),
    rocor(
        "br-rocor-indianopolis-sergius",
        "Saint Sergius of Radonezh Parish in Indianópolis",
        "Paróquia de São Sérgio Radonejsky", "Parish",
        ["Rua Gaivota 898, Indianópolis",
         "São Paulo, SP 04522-032, Brazil"],
        "https://directory.synod.com/listing/59/raroquia-de-sao-sergio-radonejsky/",
    ),
    rocor(
        "br-rocor-sao-paulo-seraphim",
        "Saint Seraphim of Sarov Parish in São Paulo",
        "Paróquia de São Serafim de Sarov", "Parish",
        ["Caixa Postal 16650", "São Paulo, SP 03197-970, Brazil"],
        "https://directory.synod.com/listing/58/raroquia-de-sao-serafim-de-sarov/",
    ),
]


ROWS = {
    "ep-buenos-aires": EP_GREEK_ROWS,
    "an-sao-paulo": ANTIOCH_SAO_PAULO_ROWS,
    "ep-ukrainian-south-america": UKRAINIAN_ROWS,
    "ru-argentina-and-south-america": MOSCOW_ROWS,
    "sr-buenos-aires": SERBIAN_ROWS,
    "pl-rio-recife": POLISH_ROWS,
    "ru-south-america-rocor": ROCOR_ROWS,
}

ANTIOCH_SPINE_ROWS = [
    body(
        "an-rio-vicariate", "antioch",
        "Patriarchal Vicariate of Rio de Janeiro",
        "Vicariato Patriarcal do Rio de Janeiro", "Patriarchal Vicariate",
        [ANTIOCH_VICARIATES],
        ["Avenida Gomes Freire 559, 2 Andar, Centro",
         "Rio de Janeiro, RJ 20231-014, Brazil"],
        site="https://www.facebook.com/vicariato.rio.de.janeiro",
        kind="diocese",
    ),
]

EXPECTED = {
    "ep-buenos-aires": 13,
    "an-sao-paulo": 20,
    "ep-ukrainian-south-america": 18,
    "ru-argentina-and-south-america": 9,
    "sr-buenos-aires": 10,
    "pl-rio-recife": 12,
    "ru-south-america-rocor": 7,
}
ANTIOCH_SPINE_EXPECTED = 1
ALLOWED_KINDS = {"parish", "monastery", "diocese"}
ALLOWED_RANKS = {
    "Cathedral Parish", "Parish", "Church", "Chapel", "Mission",
    "Community", "Monastery", "Patriarchal Vicariate",
}

ENGLISH_NAMES = {
    row["id"]: row["name"]
    for row in sum(ROWS.values(), []) + ANTIOCH_SPINE_ROWS
}


def clean(source):
    row = {
        key: value for key, value in source.items()
        if value not in (None, "", [])
    }
    row.setdefault("checked", CHECKED)
    sources = list(row.get("sources") or [])
    if not sources or len(sources) > 3:
        raise ValueError("%s must cite one to three sources" % row.get("id"))
    if not all(str(url).startswith("https://") for url in sources):
        raise ValueError("%s carries a non-HTTPS source" % row.get("id"))
    row["sources"] = sources
    row["cite"] = list(sources)
    if row.get("site") and not row["site"].startswith("https://"):
        raise ValueError("%s carries a non-HTTPS site" % row.get("id"))
    return row


def validate_rows(source_rows, parent, all_seen, all_names):
    rows = []
    for source in source_rows:
        row = clean(source)
        row_id = row.get("id")
        if not row_id or row_id in all_seen:
            raise ValueError("duplicate or missing id: %s" % row_id)
        if not re.fullmatch(r"[a-z0-9-]+", row_id):
            raise ValueError("%s is not a stable ASCII id" % row_id)
        if row.get("parent") != parent:
            raise ValueError("%s hangs off the wrong parent" % row_id)
        if row.get("country") != "BR":
            raise ValueError("%s is outside Brazil" % row_id)
        if row.get("kind") not in ALLOWED_KINDS:
            raise ValueError("%s has an unsupported kind" % row_id)
        if row.get("rank") not in ALLOWED_RANKS:
            raise ValueError("%s has an unsupported rank" % row_id)
        name = row.get("name", "")
        local = row.get("local", "")
        if not name or not local:
            raise ValueError("%s lacks a usable local or English name" % row_id)
        if name[:1].islower() or "  " in name or name.endswith(" -"):
            raise ValueError("%s has malformed English text" % row_id)
        key = name.casefold()
        if key in all_names:
            raise ValueError("duplicate reader-facing name: %s and %s" % (
                all_names[key], row_id,
            ))
        if row.get("address") and (
                not isinstance(row["address"], list) or
                not all(isinstance(value, str) for value in row["address"])):
            raise ValueError("%s has an invalid address" % row_id)
        rendered = json.dumps(row, ensure_ascii=False)
        if any(mark in rendered for mark in ("\u2013", "\u2014", "\ufffd")):
            raise ValueError("%s has forbidden punctuation or encoding" % row_id)
        all_seen.add(row_id)
        all_names[key] = row_id
        rows.append(row)
    return rows


def build_all():
    all_seen = {"antioch"}
    all_names = {}
    spine = validate_rows(
        ANTIOCH_SPINE_ROWS, "antioch", all_seen, all_names,
    )
    if len(spine) != ANTIOCH_SPINE_EXPECTED:
        raise ValueError("Antioch spine count changed: %d" % len(spine))
    payloads = {}
    for parent, source_rows in ROWS.items():
        rows = validate_rows(source_rows, parent, all_seen, all_names)
        if len(rows) != EXPECTED[parent]:
            raise ValueError("%s count changed: %d" % (parent, len(rows)))
        payloads[parent] = {
            "v": 1,
            "parent": parent,
            "country": "BR",
            "rows": rows,
        }
    row_ids = {
        row["id"] for payload in payloads.values() for row in payload["rows"]
    } | {row["id"] for row in spine}
    if set(ENGLISH_NAMES) != row_ids or len(ENGLISH_NAMES) != 90:
        raise ValueError("Brazil English name map is out of sync")
    if sum(len(payload["rows"]) for payload in payloads.values()) != 89:
        raise ValueError("Brazil branch total must remain 89")
    return payloads, spine


def build():
    return build_all()[0]


def validate_candidate_ledger():
    ledger = json.loads(CANDIDATE_LEDGER.read_text(encoding="utf-8"))
    if ledger.get("v") != 1 or ledger.get("country") != "BR":
        raise ValueError("Brazil candidate ledger has the wrong schema or country")
    if ledger.get("checked") != CHECKED:
        raise ValueError("Brazil candidate ledger check date is out of sync")
    summary = ledger.get("published_summary") or {}
    if (summary.get("worship_bodies") != 89 or
            summary.get("total_rows_including_vicariate") != 90):
        raise ValueError("Brazil candidate ledger totals are out of sync")
    required_lists = ("candidates", "exclusions", "official_jurisdiction_audit")
    for key in required_lists:
        if not isinstance(ledger.get(key), list) or not ledger[key]:
            raise ValueError("Brazil candidate ledger lacks %s" % key)
    candidate_ids = []
    for item in ledger["candidates"]:
        candidate_id = item.get("candidate_id")
        if not candidate_id or not re.fullmatch(r"[a-z0-9-]+", candidate_id):
            raise ValueError("candidate ledger carries an invalid id")
        if item.get("country") != "BR":
            raise ValueError("%s is outside Brazil" % candidate_id)
        candidate_ids.append(candidate_id)
    if len(candidate_ids) != len(set(candidate_ids)):
        raise ValueError("Brazil candidate ledger has duplicate ids")
    for section in required_lists:
        for item in ledger[section]:
            sources = item.get("sources") or []
            if not sources or len(sources) > 3:
                raise ValueError("Brazil ledger item must cite one to three sources")
            if not all(str(url).startswith("https://") for url in sources):
                raise ValueError("Brazil ledger item carries a non-HTTPS source")
    rendered = json.dumps(ledger, ensure_ascii=False)
    if any(mark in rendered for mark in ("\u2013", "\u2014", "\ufffd")):
        raise ValueError("Brazil candidate ledger has forbidden punctuation")
    return ledger


def main():
    parser = argparse.ArgumentParser()
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument("--check", action="store_true")
    mode.add_argument("--dump", action="store_true")
    args = parser.parse_args()
    try:
        payloads, spine = build_all()
        validate_candidate_ledger()
    except (OSError, ValueError) as exc:
        print("directory Brazil: %s" % exc, file=sys.stderr)
        return 1
    if args.dump:
        print(json.dumps(
            {
                "branches": payloads,
                "antioch_spine_rows": spine,
            },
            ensure_ascii=False, indent=2, sort_keys=True,
        ))
    else:
        print(
            "Brazil: 89 verified worship bodies across 7 branches plus "
            "1 Antiochian patriarchal vicariate row"
        )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
