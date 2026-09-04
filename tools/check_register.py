#!/usr/bin/env python3
"""
Hold each language to its own way of naming a saint.

English has one honorific and gives it to everyone: Saint Nicholas, Saint
Sergius, Saint Anne. Most of the languages this site publishes in do not
work that way. A saint carries the title of his order - his rank - and that
title is the honorific. Russian does not say "святой Сергий"; it says
"преподобный Сергий", because Sergius was a monastic, and "святитель
Николай" for a bishop, "благоверный князь Александр" for a prince,
"праведный Симеон Богоприимец" for a righteous man. The bare word святой
stands before a rank, not before a name: "святой апостол Андрей" is right,
"святой Андрей" is the English sentence wearing Russian words.

That is a defect no spellchecker finds, because every word in it is
correctly spelled and correctly declined. It survives proofreading too: it
reads as slightly stiff rather than as wrong, and only a native ear catches
that nobody would say it. So it is checked mechanically here.

Two things are asserted.

    A rank must follow the bare honorific. Свят- may be followed by
      апостол, пророк, мученик, святитель, преподобный, праведный,
      благоверный and the rest, but not directly by a person's name.

    The monastic saint takes the monastic title. Russian преподобный,
      Ukrainian преподобний, Greek Ὅσιος, Romanian Cuviosul. This is the
      one distinction every language on the site makes and English does
      not make at all, so it is the one most often lost.

Romanian and Greek are held only to the monastic rule. Sfântul and Ἅγιος
before a name are ordinary in both, and prove nothing either way.

    python3 tools/check_register.py
    python3 tools/check_register.py --lang ru --show 20

What this cannot do is tell whether the sentence after the honorific reads
as though a native speaker wrote it. Nothing mechanical can. It closes the
one hole that is closable.
"""
import argparse
import importlib
import importlib.util
import json
import pkgutil
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
PAGE = ROOT / "index.html"
INFO_DIR = Path(__file__).resolve().parent / "saint_info"
LIVES_DIR = Path(__file__).resolve().parent / "saint_lives"

# Which commemorations are monastic. Taken from the English rank, which the
# calendar carries for every one of them. A monastic who is also a martyr is
# a monastic here: both languages that distinguish them build the compound on
# the monastic stem (преподобномученик, Cuviosul Mucenic).
MONASTIC_WORDS = (
    "Monk", "Monastic", "Abbot", "Abbess", "Nun", "Hieromonk", "Archimandrite",
    "Schemamonk", "Hieroschemamonk", "Hermit", "Anchorite", "Stylite",
    "Recluse", "Igumen", "Monk-martyr", "Nun-martyr",
)
# "Elder" is deliberately absent: English uses it both for the monastic
# starets and for any aged man, and Eleazar the Maccabee is not a monk.
#
# Ranks that are emphatically not monastic even though the word "Monk" or a
# monastic house may appear in the title.
NOT_MONASTIC_WORDS = ("Bishop", "Archbishop", "Metropolitan", "Patriarch",
                      "Pope", "Apostle", "Prophet", "Prince", "Princess",
                      "Hierarch", "Fool-for-Christ", "Passion-bearer",
                      "Passionbearer", "Righteous", "Deaconess", "Icon")

LANGS = {
    # Bengali sets the place first in the genitive and the rank before the
    # name, as the 1,528 commemorations already do. The bare word for holy is
    # সন্ত - never সাধু, which a Bengali reader hears as a Hindu ascetic - and
    # it may stand before a bare name, so only the monastic rule is asserted.
    # See docs/BENGALI.md, where every form below is counted.
    "bn": {
        "generic": r'^\W*(?:সন্ত|পবিত্র)\b',
        "ranks": (r'শ্রদ্ধেয়|শহীদ|যাজক-শহীদ|মহান শহীদ|কুমারী শহীদ|নতুন শহীদ|'
                  r'ক্লেশভোগী|স্বীকারকারী|ভাববাদী|প্রেরিত|প্রেরিততুল্য|সত্তরজনের|'
                  r'ধার্মিক|ধন্য|খ্রীষ্টের জন্য মূর্খ|অলৌকিককর্মী|আলোকদাতা|'
                  r'নিঃস্বার্থ|কুমারী|বিশপ|আর্চবিশপ|মেট্রোপলিটন|প্যাট্রিয়ার্ক|'
                  r'যাজক|ডিকন|মঠাধ্যক্ষ|আর্কিমান্দ্রিত|সন্ন্যাসী|সন্ন্যাসিনী|'
                  r'নির্জনবাসী|স্তম্ভবাসী|রাজকুমার|রাজকুমারী|রাজা|সম্রাট|সম্রাজ্ঞী|'
                  r'ঈশ্বরমাতা|ঈশ্বরের মাতা|আইকন|উৎসব|প্রধান দূত|পিতা|মাতা'),
        "monastic": r'শ্রদ্ধেয়|সন্ন্যাসী|সন্ন্যাসিনী|মঠাধ্যক্ষ|নির্জনবাসী|স্তম্ভবাসী|আর্কিমান্দ্রিত',
        "strict": False,
    },

    # Italian sets san or santa before the name and carries the rank
    # after it; the monastic is venerabile, which is the distinction the
    # generic pattern is meant to catch standing alone.
    "it": {
        "generic": r"^\W*(?:(?:[Ii]l|[Ll][ae]|[Ii]|[Gg]li)\s+)?[Ss]an(?:t[oaie]\b|t'|\b)",
        "ranks": (r'[Vv]enerabil|[Aa]postol|[Pp]rofet|[Ee]vangelist|[Mm]artir|[Ii]eromartir|[Nn]eomartir|[Pp]rotomartir|[Cc]onfessor|[Gg]iust|[Gg]erarc|[Ii]gumen|[Aa]bat|[Bb]adess|[Aa]rchimandrit|[Mm]onac|[Vv]escov|[Aa]rcivescov|[Mm]etropolit|[Pp]atriarc|[Dd]iacon|[Ss]acerdot|[Pp]resbiter|[Ll]ettor|[Pp]rincip|\b[Rr]e\b|[Ii]mperator|[Ii]mperatric|[Zz]ar|[Ss]tilita|[Ee]remit|[Aa]nacoret|[Rr]eclus|[Aa]scet|[Ss]chema|[Vv]ergin|[Ff]est|[Ss]inassi|[Ii]con|[Aa]nargir|[Mm]irofor|[Mm]irovlit|[Tt]aumaturg|[Ff]olle per Cristo|[Pp]ari agli [Aa]postoli|[Bb]eat|[Pp]adr[ei]|[Mm]adre di Dio|[Ii]lluminat|[Ii]nnograf|[Ii]conograf|[Aa]rcangel|[Pp]recursor|[Pp]ortator|[Cc]enobiarc|[Ss]ovran|[Rr]egin'),
        "monastic": r'[Vv]enerabil',
        "strict": False,
    },

    # French sets the rank before the name in the received shape - le saint
    # apotre, le saint martyr - and the monastic takes the word his order is
    # given rather than the bare saint.
    "fr": {
        "generic": r'^\W*(?:(?:[Ll]e|[Ll]a|[Ll]es|[Nn]otre|[Nn]os)\s+)?[Ss]aint(?:es|e|s)?\b',
        "ranks": (r'[Aa]pôtre|[Pp]rophèt|[Éé]vangéliste|[Mm]artyr|[Hh]iérarque|[Éé]vêque|[Aa]rchevêque|[Mm]étropolite|[Pp]atriarche|[Pp]ape|[Hh]igoumène|[Aa]bbesse|[Aa]rchimandrite|[Hh]iéromoine|[Mm]oine|[Mm]oniale|[Ee]rmite|[Aa]nachorète|[Rr]eclus|[Ss]tylite|[Aa]scèt|[Ss]tarets|[Ss]chémamoine|[Vv]énérable|[Cc]onfesseur|[Jj]uste|[Bb]ienheureu|[Aa]nargyre|[Tt]haumaturge|[Mm]yroblyte|[Mm]yrophore|[Ff]ol(?:le)?[- ]en[- ]Christ|[Éé]gal(?:e)?[- ]aux[- ][Aa]pôtres|[Pp]orte[- ]passion|[Pp]orteu(?:r|se) de la Passion|[Pp]rince|[Pp]rincesse|[Rr]oi|[Rr]eine|[Ee]mpereur|[Ii]mpératrice|[Tt]sar|[Ff]idèle|[Dd]iacre|[Dd]iaconesse|[Pp]rêtre|[Pp]resbytre|[Aa]rchiprêtre|[Vv]ierge|[Ii]lluminat|[Hh]ymnographe|[Ii]conographe|[Mm]édecin|[Ss]oldat|[Ss]ynaxe|[Ff]ête|[Ii]cône|[Aa]rchange|[Pp]uissances incorporelles|[Pp]ère|[Mm]ère|[Aa]ïeu|[Aa]ncêtre|[Cc]énobiarque|[Ss]tratélate'),
        "monastic": r'[Vv]énérable|[Mm]oine|[Mm]oniale|[Hh]igoumène|[Aa]bbesse|[Ee]rmite|[Aa]nachorète|[Rr]eclus|[Ss]tylite|[Aa]scèt|[Ss]tarets|[Ss]chémamoine|[Mm]onast',
        "strict": False,
    },

    # Spanish sets the title before the name and inflects it for the name:
    # san before a masculine name, santo only before To- and Do-, santa before
    # a feminine one. The monastic is venerable, which is the distinction the
    # generic pattern below is meant to catch when it stands alone.
    "es": {
        "generic": r'^\W*(?:(?:[Ee]l|[Ll]a|[Ll]os|[Ll]as|[Nn]uestr[oa]s?)\s+)?[Ss]an(?:t[oa]s?)?\b',
        "ranks": (r'[Vv]enerable|[Mm]ártir|[Aa]póstol|[Pp]rofet|[Ee]vangelist|[Jj]erarca|[Cc]onfesor|[Jj]ust[oa]|[Aa]nárgir|[Ll]oc[oa] por Cristo|[Pp]ortador|[Mm]irófor|[Tt]aumaturg|[Ii]luminador|[Oo]bispo|[Aa]rzobispo|[Mm]etropolit|[Pp]atriarca|[Aa]bad|[Ii]gumen|[Aa]rchimandrita|[Mm]onj|[Ee]rmitaño|[Aa]nacoret|[Rr]ecluso|[Ee]stilita|[Aa]sceta|[Pp]ríncipe|[Pp]rincesa|[Rr]ey|[Rr]eina|[Ee]mperador|[Ee]mperatriz|[Zz]ar\b|[Zz]arina|[Dd]iácon|[Ss]acerdote|[Pp]resbítero|[Vv]írgen|[Vv]irgen|[Hh]imnógrafo|[Ss]anador|[Ii]conógrafo|[Aa]rcángel|[Áá]ngel|[Ii]ncorpóre|[Ss]ínaxis|[Cc]oncilio|[Ff]iesta|[Ii]cono|[Tt]emplo|[Tt]raslación|[Hh]allazgo|[Cc]onmemoración|[Nn]iños|[Hh]ermanos|[Cc]ompañeros|[Mm]ujeres|[Ss]oldados|[Ee]sposos|[Aa]ntepasados|[Pp]atriarcas'),
        "monastic": r'[Vv]enerable',
        "strict": False,
    },

    # Portuguese sets Sao, Santo or Santa before the name and gives no
    # offence by it, as Spanish, Greek and Romanian do, so strict stays
    # False and only the monastic distinction is asserted: a monk is
    # veneravel, nosso veneravel pai, never merely santo. Note that the
    # apocopation is not the Spanish one - Santo stands before any
    # masculine name beginning with a vowel, not only before To- and Do- -
    # so the generic pattern spells out Sao and Santo separately rather
    # than treating the second as an optional tail of the first. Written
    # before the first line of the vocabulary; docs/PORTUGUESE.md settles
    # the register it is drawn from.
    "pt": {
        "generic": r'^\W*(?:(?:[Oo]|[Aa]|[Oo]s|[Aa]s|[Nn]oss[oa]s?)\s+)?(?:[Ss]ão|[Ss]ant[oa]s?)\b',
        "ranks": (r'[Vv]enerá(?:vel|veis)|[Mm]ártir|[Aa]póstol|[Pp]rofet|[Ee]vangelist|[Hh]ierarca|[Cc]onfessor|[Jj]ust[oa]|[Aa]nárgir|[Ll]ouc[oa] por Cristo|[Pp]ortador|[Mm]irófor|[Tt]aumaturg|[Ii]luminador|[Bb]ispo|[Aa]rcebispo|[Mm]etropolita|[Pp]atriarca|[Aa]bade|[Aa]badessa|[Ii]gumen|[Aa]rquimandrita|[Mm]ong|[Mm]onja|[Ee]remita|[Aa]nacoreta|[Rr]ecluso|[Ee]stilita|[Aa]sceta|[Ee]squemamonge|[Pp]ríncipe|[Pp]rincesa|[Gg]rão-príncipe|[Rr]ei\b|[Rr]ainha|[Ii]mperador|[Ii]mperatriz|[Cc]zar|[Dd]iácon|[Ss]acerdote|[Pp]resbítero|[Vv]irgem|[Vv]irgens|[Hh]inógrafo|[Ii]conógrafo|[Cc]urador|[Mm]édic|[Aa]rcanjo|[Aa]njo|[Ii]ncorpóre|[Ss]ínaxe|[Cc]oncílio|[Ff]esta|[Íí]cone|[Tt]emplo|[Tt]rasladação|[Dd]escoberta|[Cc]omemoração|[Cc]rianças|[Ii]rmãos|[Cc]ompanheiros|[Mm]ulheres|[Ss]oldados|[Cc]ônjuges|[Aa]ntepassados|[Pp]adres|[Pp]ai\b|[Pp]ais\b|[Mm]ãe\b'),
        "monastic": r'[Vv]enerá(?:vel|veis)',
        "strict": False,
    },

    # Georgian, like Greek, Romanian and Serbian, lets the plain honorific
    # stand before a name: წმინდა გიორგი is what the Patriarchate prints and
    # what data/saint-names.v1.ka.json prints four hundred and eighty-five
    # times. So strict stays False and only the monastic rule is asserted.
    # The monastic is ღირსი, truncated to ღირს before the name it qualifies -
    # Georgian attributive adjectives in -ი drop it before their noun - so the
    # stem is what is matched and not either whole word. The rank stems below
    # carry no case ending for the same reason: Georgian declines the rank
    # behind the honorific, and a stem matches every case of it.
    # docs/GEORGIAN.md settles the register they are drawn from.
    "ka": {
        "generic": r"^\W*წმი(?:ნ)?და",
        "ranks": (r"ღირს|მოწამე|დიდმოწამე|მღვდელ|ახალმოწამე|პირველმოწამე|"
                  r"ვნებათმძლე|აღმსარებელ|მართალ|ნეტარ|კეთილმორწმუნე|"
                  r"კეთილმსახურ|მოციქულ|წინასწარმეტყველ|განმანათლებელ|"
                  r"სასწაულმოქმედ|ეპისკოპოს|მიტროპოლიტ|პატრიარქ|პაპ|"
                  r"წინამძღ|არქიმანდრიტ|მონაზონ|სქემოსან|დაყუდებულ|განდეგილ|"
                  r"სვეტმდგომ|უვერცხლო|ქრისტესთვის სულ|ქალწულ|დიაკ|ხუცეს|"
                  r"ბერი|მეფე|დედოფალ|მთავარ|კრება|დღესასწაულ|ხსენებ|ხატ|"
                  r"ტაძარ|ნაწილ|ძმა|დედ|მამ|ყრმა|მთავრ"),
        "monastic": r"ღირს",
        "strict": False,
    },

    # Armenian, like Greek, Georgian and Romanian, lets the plain honorific
    # stand before a name: sourb Nikoghayos is what the names table prints some
    # four hundred and eighty times. So strict stays False and only the
    # monastic rule is asserted. The monastic is eraneli, which is what
    # data/saint-names.v1.hy.json gives Hosios three hundred and thirty-eight
    # times; it renders Blessed as well, and Armenian separates the two by the
    # rank noun that follows rather than by the honorific.
    #
    # The rank stems below carry no case ending: Armenian declines the noun
    # behind the honorific - nahatak, nahataki, nahatakner, nahatakneri - and a
    # stem matches every case of it. They are the table in docs/ARMENIAN.md,
    # which settles the register they are drawn from, and vardapet stands there
    # for the teacher and doctor of the Church and not for the archimandrite,
    # which is arkimandrit.
    "hy": {
        "generic": r"^\W*(?:[Սս]ուրբ|Ս\.)",
        "ranks": (r"երանելի|նահատակ|նախավկայ|վկայ|խոստովանող|առաքեալ|"
                  r"առաքելակից|մարգարէ|կարապետ|աւետարանիչ|սրբապետ|"
                  r"եպիսկոպոս|մետրոպոլիտ|պատրիարք|պապ|քահանայ|երէց|"
                  r"սարկաւագ|ընթերցող|վանահայր|վանամայր|արքիմանդրիտ|"
                  r"վանական|միանձնուհի|նորընծայ|ծերունի|սքեմաւոր|ճգնաւոր|"
                  r"անապատական|մենակեաց|սիւնակեաց|յիմար|անարծաթ|"
                  r"սքանչելագործ|լուսաւորիչ|իւղաբեր|իւղահոս|շարականագիր|"
                  r"սրբանկարիչ|կոյս|վարդապետ|չարչարակիր|ուղղահաւատ|"
                  r"բարեպաշտ|արդար|թագաւոր|թագուհի|կայսր|իշխան|"
                  r"հրեշտակապետ|հրեշտակ|ժողով|տօն|սրբապատկեր|պատկեր|"
                  r"տաճար|մասունք|խաչ|հայր|մայր|եղբայր|քոյր|աշակերտ|"
                  r"մանուկ|կին|զինուոր|բժիշկ"),
        "monastic": r"երանելի",
        "strict": False,
    },

    "ja": {
        "generic": r"^\W*聖",
        "ranks": (r"克肖|致命者|致命神品|致命女|大致命者|大致命女|新致命|"
                  r"原致命|致命|宣信者|証聖者|預言者|女預言者|義人|童貞|"
                  r"亜使徒|七十使徒|使徒|福音記者|佯狂者|福者|信仰篤|"
                  r"無報酬|柱行者|隠修士|成神者|不思議|載神|神品|"
                  r"主教|大主教|府主教|総主教|教皇|修道院長|修道士|修道女|"
                  r"司祭|長老|輔祭|誦経|医者|癒し者|神学者|金口|階梯者|"
                  r"携香|前駆|大天使|天使|生神女|諸聖|聖人|教師|啓蒙者|"
                  r"公|王|皇帝|皇后|王妃|神の人|大斎|主日|祭|会衆|"
                  r"シナクシス|聖像|聖堂|聖遺物|十字架|遺物|記憶|降誕|"
                  r"就寝|進堂|挙栄|神現|庇護|永眠|列聖|発見|移動|"
                  r"父|母|兄弟|姉妹|弟子|子|三聖"),
        "monastic": r"克肖",
        "strict": False,
    },

    # Chinese sets the rank before the name and the see before the rank, so
    # the honorific is never far from the head of the phrase. 圣 stands
    # freely before a name in the 1,528 commemorations already published -
    # 圣乔治, 圣使徒安德烈 - so strict stays False and only the monastic
    # distinction is asserted: a monastic is 可敬 and not merely 圣. The
    # rank words below are the renderings the names table prints, longest
    # first so that 大致命者 is not eaten by 致命者; see docs/CHINESE.md.
    "zh": {
        "generic": r"^\W*圣",
        "ranks": (r"童贞致命女|大修士品修士|为基督而愚者|与使徒同等|"
                  r"致命圣职人员|首位致命者|女修道院长|无偿医者|不取酬者|"
                  r"新致命者|新致命女|大致命者|大致命女|致命修士|致命司祭|"
                  r"致命主教|致命者|致命女|柱头修士|行奇迹者|载神者|"
                  r"七十门徒|七十使徒|总领天使|修道院长|大修士品|"
                  r"证道者|宣信者|受难者|启蒙者|光照者|可敬者|可敬|"
                  r"殉道者|圣愚|真福|义人|义者|先知|使徒|门徒|"
                  r"福音书作者|前驱|隐士|修女|修士|长老|执事|司祭|"
                  r"诵经者|修士大司祭|掌院|主教|大主教|都主教|牧首|教宗|"
                  r"诞神女|童贞女|皇帝|皇后|王公|大公|沙皇|"
                  r"圣像|圣髑|十字架|纪念|迁移|发现|安息|诞生|"
                  r"进堂|领报|举荣|节日|同伴|父|母|兄弟|姊妹|弟子|子"),
        "monastic": r"可敬",
        "strict": False,
    },

    # Korean puts every modifier before its head, so the see and the rank
    # stand in front of the name and 성 is almost never at the head of the
    # phrase - 미라의 성 니콜라오, 로마의 순교자 타티아나. The generic pattern
    # is therefore written to reach 성 wherever it falls rather than being
    # anchored to the first character, and the lookahead keeps it off the
    # ordinary words that merely begin with the same syllable - 성인, 성령,
    # 성모, 성당. strict stays False, because 성 before a name is ordinary
    # Korean and proves nothing either way, as in Greek, Romanian, Serbian
    # and Georgian. The monastic is 존경하올, which the 1,528 commemorations
    # of data/saint-names.v1.ko.json print 360 times against 존자 10 and
    # 성덕 2. The rank words are the renderings that table prints, longest
    # first so that 대순교자 is not eaten by 순교자; docs/KOREAN.md settles
    # the register they are drawn from and gives the count behind each.
    "ko": {
        "generic": r"^[^성]*성(?=\s*[가-힣])(?!인|령|모|당|찬|가|경|사|전|체|유|호|삼|자|물|직)",
        "ranks": (r"그리스도를 위한 바보|사도와 동등한 자|하느님의 어머니|"
                  r"주상 고행자|수도 대주교|무보수 의사|사제 순교자|"
                  r"동정 순교녀|수도 순교자|첫 부름 받은|새 순교자|"
                  r"대순교자|순교자|순교녀|존경하올|증거자|여예언자|"
                  r"예언자|사도|의인|의로운|총대주교|대주교|주교|교황|"
                  r"수도대사제|수도원장|수도자|수녀|사제|부제|독경자|"
                  r"고행자|은수자|기적행자|계몽자|수난자|복자|복녀|"
                  r"동정녀|동정|단식자|침묵자|치유자|신학자|황제|황후|"
                  r"공후|대공|여왕|왕|대천사|천사|시낙시스|이콘|성상|"
                  r"유물|십자가|축일|기념|이전|발견|안식|탄생|"
                  r"아버지|어머니|형제|자매|제자|아들|딸|청년|"
                  r"군인|의사|장군"),
        "monastic": r"존경하올",
        "strict": False,
    },

    "ru": {
        "generic": r"^\W*Свят(ой|ая|ые|ых)\b",
        "ranks": (r"апостол|пророк|мучени|преподобн|святител|праведн|"
                  r"благоверн|равноапостольн|страстотерпец|бессребреник|"
                  r"блаженн|исповедник|юродив|столпник|пустынник|затворник|"
                  r"царь|царица|князь|княгиня|игумен|игумения|архиепископ|"
                  r"епископ|митрополит|патриарх|диакон|пресвитер|иерей|"
                  r"архимандрит|схимонах|инок|монах|отшельник|дева|отроки?|"
                  r"жёны|жены|отцы|отец|праотец|богоотец|песнописец|"
                  r"земля|апостолов|обители|храм|икон|собор|праздник"),
        "monastic": r"[Пп]реподобн",
        "strict": True,
    },
    "uk": {
        "generic": r"^\W*Свят(ий|а|і|их)\b",
        "ranks": (r"апостол|пророк|пророчиц|мучени|преподобн|святител|праведн|"
                  r"благовірн|рівноапостольн|страстотерпец|безсрібник|"
                  r"блаженн|сповідник|юродив|стовпник|пустельник|затворник|"
                  r"цар|цариця|князь|княгиня|ігумен|архієпископ|єпископ|"
                  r"митрополит|патріарх|диякон|пресвітер|ієрей|архімандрит|"
                  r"схимонах|чернець|монах|самітник|діва|отроки?|отці|отець|"
                  r"праотець|праматір|піснописець|земля|обителі|храм|ікон|"
                  r"собор|свято"),
        "monastic": r"[Пп]реподобн",
        "strict": True,
    },
    "ro": {
        "generic": r"^\W*Sf[âa]nt(ul|a)\b",
        "ranks": (r"[Cc]uvio(s|ș|a)|[Mm]ucenic|[Aa]postol|[Pp]rooroc|[Dd]rept|"
                  r"[Bb]inecredincio|[Ff]ericit|[Ii]erarh|[Ee]gumen|[Ss]tareț|"
                  r"[Aa]rhiepiscop|[Ee]piscop|[Mm]itropolit|[Pp]atriarh|"
                  r"[Cc]neaz|[Cc]neaghin|[Îî]mpărat|[Dd]iacon|[Pp]reot|"
                  r"[Ss]tâlpnic|[Nn]ebun pentru Hristos|fără de arginți|"
                  r"[Pp]urtător de patimi|[Ss]obor|[Mm]onah|[Ss]ihastru|"
                  r"[Zz]ăvorât|[Pp]ostitor|[Mm]ironosiț|[Aa]rhimandrit|"
                  r"[Ss]chimonah|[Ff]ecioar|[Pp]raznic|[Ii]coana|[Ss]trămoș"),
        "monastic": r"[Cc]uvio(s|ș|a)",
    },
    "de": {
        "generic": r"^\W*(?:[DdSs](?:er|ie|as|eine?)\s+)?[Hh]eilige[nrsm]?\b",
        "ranks": (r"[Ee]hrwürdig|[Aa]postel|[Pp]rophet|[Mm]ärtyrer|"
                  r"[Bb]ekenner|[Gg]erecht|[Ss]elig|[Hh]ierarch|[Bb]ischof|"
                  r"[Ee]rzbischof|[Mm]etropolit|[Pp]atriarch|[Aa]bt|"
                  r"[Ii]gumen|[Ää]btissin|[Aa]rchimandrit|[Mm]önch|[Nn]onne|"
                  r"[Ee]insiedler|[Kk]lausner|[Ss]tylit|[Ss]äulensteher|"
                  r"[Gg]leichapostel|[Aa]postelgleich|[Pp]assionsträger|"
                  r"[Ll]eidensdulder|[Uu]neigennützig|[Aa]nargyr|"
                  r"[Nn]arr in Christo|[Nn]arr um Christi willen|[Ff]ürst|"
                  r"[Kk]önig|[Kk]aiser|[Dd]iakon|[Pp]riester|[Pp]resbyter|"
                  r"[Jj]ungfrau|[Aa]ltvater|[Ee]rzvater|[Ss]tammvater|"
                  r"[Mm]yrrhenträger|[Ww]undertäter|[Aa]sket|[Ss]chemamönch|"
                  r"[Ss]ynaxis|[Ii]kone|[Ff]est|[Vv]äter|[Vv]ater|[Kk]inder"),
        # German says "der heilige Nikolaus" without offence, as Greek and
        # Romanian do and Russian does not, so only the monastic distinction
        # is asserted: a monk is ehrwürdig, not merely heilig.
        "monastic": r"[Ee]hrwürdig",
    },
    "sr": {
        # Serbian, like Greek and Romanian, allows the plain honorific before
        # a name: Свети Никола is right. So only the monastic distinction is
        # asserted, and strict stays False.
        "generic": r"^\W*Свет(и|а|о|е|их|ог|ом|у)\b",
        # Stems, not whole words: Serbian declines the rank behind the
        # honorific, and the plural of мученик is мученици, so anything
        # spelled out in full matches the singular and misses the company.
        "ranks": (r"[Пп]реподобн|[Аа]постол|[Пп]ророк|[Мм]учени|[Сс]ветител|"
                  r"[Пп]раведн|[Бб]лаговерн|[Рр]авноапостол|[Сс]трастотрп|"
                  r"[Бб]есребреник|[Бб]лажен|[Ии]споведник|[Јј]уродив|"
                  r"[Сс]толпник|[Пп]устињак|[Зз]атворник|[Цц]ар|[Кк]нез|"
                  r"[Кк]негиња|[Ии]гуман|[Аа]рхиепископ|[Ее]пископ|"
                  r"[Мм]итрополит|[Пп]атријарх|[Ђђ]акон|[Пп]резвитер|"
                  r"[Сс]вештеник|[Аа]рхимандрит|[Сс]химонах|[Мм]онах|[Аа]рхијереј|"
                  r"[Дд]евиц|[Сс]абор|[Пп]разник|[Ии]кон|[Хх]рам|"
                  r"[Пп]росветител|[Чч]удотвор|[Оо]тац|[Оо]ц[иа]|"
                  r"[Жж]ене|[Мм]ироносиц|[Бб]есплотн|[Аа]рханђел|[Аа]нђел"),
        "monastic": r"[Пп]реподобн",
        "strict": False,
    },
    "el": {
        "generic": r"^\W*[ὉΟ]?\s?[ἍΆΑ]γι(ος|α|οι)\b",
        "ranks": (r"[ὅὍόΌοΟ]σ[ιί]|απόστολ|Απόστολ|προφήτ|Προφήτ|μάρτυ|Μάρτυ|"
                  r"μαρτυ|ιεράρχ|Ιεράρχ|δίκαι|Δίκαι|ηγούμεν|Ηγούμεν|"
                  r"επίσκοπ|Επίσκοπ|αρχιεπίσκοπ|Αρχιεπίσκοπ|μητροπολίτ|"
                  r"πατριάρχ|Πατριάρχ|μοναχ|Μοναχ|ομολογητ|Ομολογητ|"
                  r"στυλίτ|διάκον|πρεσβύτερ|ερημίτ|εγκλειστ|βασιλ|πρίγκιπ|"
                  r"σύναξ|Σύναξ|εορτ|Εορτ|εικόν|Εικόν|παρθέν|προπάτορ"),
        "monastic": r"[ὅὍόΌοΟ]σ[ιί]",
    },
    # Arabic, like Greek and Romanian, lets the plain honorific stand before
    # a name: al-qiddis Nicholas is what the Antiochian books print. So only
    # the monastic rule is asserted. The monastic is al-bar, al-bara, never
    # merely al-qiddis. The rank stems below carry no definite article
    # because al- is a prefix and a bare stem matches it either way.
    "ar": {
        "generic": r"^\W*(?:ال)?قديس(?:ة|ون|ين|ات|ان|تان)?\b",
        "ranks": (r"رئيس دير|رئيسة دير|رئيس أساقفة|رئيس كهنة|رئيس الشمامسة|"
                  r"عظيم في الشهداء|عظيمة في الشهيدات|شهيد في الكهنة|"
                  r"متباله|راهب بالإسكيم|حامل الآلام|معادل للرسل|عديم الفضة|عديمة الفضة|"
                  r"أرشمندريت|إمبراطور|بطريرك|مطران|أسقف|أمير|أميرة|ملك|ملكة|"
                  r"بتول|حبيس|راهب|راهبة|رسول|شماس|شهيد|كاهن|قس|ناسك|عمودي|معترف|"
                  r"نبي|صديق|بار|عيد|تذكار|سيناكس|أيقونة|إكليريكي"),
        "monastic": r"البار(?:ة)?\b",
        "strict": False,
    },

    # Swahili, as the Patriarchate of Alexandria prints it and as the site's
    # own fifteen hundred commemorations write it. Mtakatifu before a name is
    # ordinary here, as in Greek and Romanian, so only the monastic rule is
    # asserted; the monastic is Mheshimiwa and never merely Mtakatifu. The
    # plurals are the m-/wa- class of persons and are matched beside their
    # singulars, since a company of martyrs opens Mashahidi and not Shahidi.
    "sw": {
        "generic": r"^\W*(?:Mtakatifu|Watakatifu)\b",
        "ranks": (r"Mpumbavu kwa ajili ya Kristo|Wapumbavu kwa ajili ya Kristo|"
                  r"Mtawa wa Shahada Kuu|Asiyepokea-Malipo|Wasiopokea-Malipo|"
                  r"Abate \(Igumeni\)|Mtawa wa upweke|Mtawa wa Nguzo|"
                  r"Bikira Shahidi|Kuhani Shahidi|Makuhani Mashahidi|"
                  r"Sawa na Mitume|Sawa-na-Mitume|Mtawa wa kike|Aliyejitenga|"
                  r"Waliojitenga|Arkimandriti|Mbeba-Mateso|Wabeba-Mateso|"
                  r"Mkuu wa kike|Shahidi Mkuu|Mashahidi Wakuu|Shahidi Mpya|"
                  r"Shahidi Mtawa|Askofu Mkuu|Maaskofu Wakuu|Metropolita|"
                  r"Mwenye haki|Wenye haki|Mtenda-Miujiza|Watenda-Miujiza|"
                  r"Mheshimiwa|Waheshimiwa|Mwangazaji|Mbeba-Mungu|Mbarikiwa|"
                  r"Wabarikiwa|Mashahidi|Maaskofu|Mashemasi|Makasisi|"
                  r"Mabikira|Manabii|Patriaki|Mitume|Mkutano|Sinaksi|"
                  r"Shahidi|Shemasi|Sikukuu|Msomaji|Askofu|Bikira|Kasisi|"
                  r"Kuhani|Malkia|Watawa|Wakiri|Abesi|Abate|Mkiri|Mtawa|"
                  r"Mtume|Nabii|Ikoni|Masalia|Mkuu"),
        "monastic": r"(?:Mheshimiwa|Waheshimiwa)",
        "strict": False,
    },

    # Syriac lets the bare word for holy stand before a name, as Greek,
    # Romanian and Georgian do: data/saint-names.v1.arc.json prints
    # qaddisha and qaddishta straight before a name three hundred and
    # forty-three times. So strict stays False and only the monastic
    # rule is asserted: the monastic is meyaqra, never merely qaddisha.
    # The stems below carry no final alaph, because a rank inflects for
    # the feminine and takes seyame in the plural, and the seyame is a
    # combining mark written inside the word rather than after it. Drawn
    # from the published names table; docs/SYRIAC.md settles which of the
    # four published bodies wins where two of them disagree.
    # Urdu, like Greek, Romanian, Georgian and Syriac, lets the plain
    # honorific stand before a name: data/saint-names.v1.ur.json prints
    # sant four hundred times and nobody hears it as an evasion of rank.
    # What that table does keep apart is the monastic, jalil ul-qadr, from
    # the martyr and from the merely holy, so that alone is asserted.
    "ur": {
        "generic": r"^\W*(مقدسہ|مقدس|سینٹ)\b",
        "ranks": (r"رسولوں کے برابر|رسولوں کے ہمسر|مسیح کے لیے احمق|"
                  r"بے غرض معالج|بلامعاوضہ طبیب|مٹھ کے سربراہ|"
                  r"خدا کو قبول کرنے والے|سردار اسقف|میٹروپولیٹن|"
                  r"سرپرست اعلیٰ|پیٹریارک|جلیل القدر|کاہن شہید|عظیم شہید|"
                  r"کنواری شہید|خواتین شہداء|اولین شہید|نئے شہداء|"
                  r"معجزہ گر|خوشبو لانے والی|مُر بہانے والے|خدا بردار|جاں نثار|راستباز|معترفین|"
                  r"معترف|شہداء|شہیدہ|شہید|کنواری|نبیہ|نبی|رسول|"
                  r"مبارک|راہبہ|راہب|بشپ|اسقف|کاہن|شماس|پادری|"
                  r"بادشاہ|ملکہ|شہزادہ|شہزادی|والد|والدہ|"
                  r"معماری|ستون نشین|تنہائی نشین|روزہ دار|قاری"),
        "monastic": r"جلیل القدر|راہب",
        "strict": False,
    },

    "arc": {
        "generic": r"^\W*ܩܕܝ̈?ܫ",
        "ranks": (r"ܠܐ ܢܣ̈ܒܝ ܟܣܦܐ|ܐܣܝܐ ܕܠܐ ܟܣܦ|ܫܘܐ ܠܫܠܝ̈ܚܐ|"
                  r"ܫܘܝܬ ܠܫܠܝ̈ܚܐ|ܫܛܝܐ ܡܛܠ ܡܫܝܚܐ|ܥܒܕ ܬܕܡܪ̈ܬܐ|"
                  r"ܥܒ̈ܕܝ ܬܕܡܪ̈ܬܐ|ܣܒ̈ܠܝ ܚܫܐ|ܡܝܬܝܬ ܒܣ̈ܡܐ|"
                  r"ܡܪܕܐ ܡܘܪܘܢ|ܠܒܝܫ ܐܠܗܐ|ܨܝܪ ܝܘܩ̈ܢܐ|ܪܒ ܟܗ̈ܢܐ|"
                  r"ܪܝܫ ܟܗ̈ܢܐ|ܪ̈ܝܫܝ ܟܗ̈ܢܐ|ܪܝܫ ܐܦܣܩܘܦܐ|ܪܝܫ ܡܠܐܟ̈ܐ|"
                  r"ܪ̈ܝܫܝ ܡܠܐܟ̈ܐ|ܪܝܫܬ ܕܝܪܐ|ܪܝܫ ܕܝܪܐ|ܐܪܟܝܡܢܕܪܝܛܐ|"
                  r"ܡܝܛܪܘܦܘܠܝܛܐ|ܐܦܣ̈ܩܘܦܐ|ܐܦܣܩܘܦܐ|ܦܛܪܝܪܟܐ|ܐܣܛܘܢܪܐ|"
                  r"ܐܢܟܘܪܝܛܐ|ܐܣܟܡܝܐ|ܬܐܘܠܘܓܘܣ|ܡܢܗܪܢ|ܡܣܒܪܢܐ|ܡܙܡܪܢܐ|"
                  r"ܡܘܕ̈ܝܢܐ|ܡܘܕܝܢܐ|ܡܫܡ̈ܫܢܐ|ܡܫܡܫܢ|ܡܗܝܡܢܐ|ܡܝܩܪ|ܣܗ̈ܕ|"
                  r"ܣܗܕ|ܟܗ̈ܢܐ|ܟܗܢܐ|ܩܫܝܫܐ|ܕܝܪ̈ܝܐ|ܕܝܪܝ|ܒܬܘ̈ܠܬܐ|"
                  r"ܒܬܘܠܬܐ|ܢܒܝ|ܫܠܝ̈ܚܐ|ܫܠܝܚܐ|ܙܕܝ̈ܩܐ|ܙܕܝܩ|ܛܘܒܢ|"
                  r"ܚܫܘ̈ܫܐ|ܚܫܘܫܐ|ܥܢܘܝܐ|ܚܒܝܫ|ܫܬܝܩܐ|ܨܝܡܐ|ܩܪܘܝܐ|"
                  r"ܡܠܟܬܐ|ܡܠܟܐ|ܩܣܪ|ܐܡܝܪ̈ܬܐ|ܐܡܝܪܬܐ|ܪܫܐ|ܥܐܕܐ|ܟܢܘܫܝܐ|"
                  r"ܝܘܩܢܐ|ܐܒܗ̈ܬܐ|ܐܒܐ|ܐܡܐ"),
        "monastic": r"ܡܝܩܪ",
        "strict": False,
    },

    # Hindi, like Greek, Romanian, Georgian, Armenian and Serbian, lets the
    # plain honorific stand before a name: sant Nicholas is what
    # data/saint-names.v1.hi.json prints three hundred and ninety-two times.
    # So strict stays False and only the monastic rule is asserted. The
    # monastic is aadarniya, which the names table gives Venerable 385 times
    # against 2 for vandaniya; vandaniya is matched here as well because the
    # 119 calendar entries prefer it and a monastic named by either is named
    # rightly. The rank stems below carry no postposition: Hindi puts the
    # postposition after the noun, so a bare stem matches every case of it.
    # docs/HINDI.md settles the register they are drawn from.
    "hi": {
        "generic": r"^\W*(?:परम\s+)?(?:पवित्र\s+)?संत\b",
        "ranks": (r"आदरणीय|वंदनीय|महान शहीद|पुरोहित-शहीद|याजक शहीद|नवशहीद|"
                  r"मठवासी शहीद|कुँवारी शहीद|शहीद|स्वीकारकर्ता|धर्मी|धन्य|"
                  r"भविष्यवक्ता|भविष्यद्वक्ता|भविष्यवक्त्री|प्रेरित|"
                  r"चमत्कारकर्ता|चमत्कारी|निःशुल्क चिकित्सक|नि:शुल्क चिकित्सक|"
                  r"दुःख-वाहक|अग्रदूत|सुसमाचार-प्रचारक|महादूत|"
                  r"महाधर्माध्यक्ष|धर्माध्यक्ष|महानगराध्यक्ष|"
                  r"प्राधिधर्माध्यक्ष|कुलपति|बिशप|मठाधीशा|मठाधीश|"
                  r"आर्किमंड्राइट|पुरोहित|प्रेस्बिटर|याजक|डीकन|उपयाजक|"
                  r"मठवासी|भिक्षु|तपस्वी|वैरागी|एकांतवासी|स्तंभवासी|"
                  r"महाश्रेणी|कुँवारी|विधवा|राजकुमारी|राजकुमार|सम्राट|"
                  r"साम्राज्ञी|सम्राज्ञी|रानी|राजा|त्सार|प्रबोधक|प्रबोधिका|"
                  r"समवाय|पर्व|प्रतिमा|चिह्न|माता|पिता|पुत्र|बालक|"
                  r"प्रेरितों के समतुल्य|मसीह के लिए मूर्ख|ईश्वरमाता"),
        "monastic": r"आदरणीय|वंदनीय",
        "strict": False,
    },
}


def english_types():
    """The English rank, and the English life beneath it.

    The rank alone is not enough. Seraphim of Sarov is filed under the bare
    word Saint, and nothing in that tells a script he was a monk - which is
    exactly the information the Slavonic and Romanian honorifics turn on. So
    the English name and life are read too: "Venerable" is English for
    Ὅσιος and преподобный and is decisive wherever it appears, and a life
    that calls its subject a monk is describing a monastic whatever the rank
    column happens to say."""
    src = PAGE.read_text(encoding="utf-8")
    import saint_info_en
    info = saint_info_en.load()
    return {k: "%s || %s || %s" % (v.get("type") or "", k, v.get("life") or "")
            for k, v in info.items()}


def is_monastic(blob):
    rank = blob.split(" || ")[0]
    for w in NOT_MONASTIC_WORDS:
        if re.search(r"\b%s\b" % re.escape(w), rank):
            return False
    if re.search(r"\bVenerable\b", blob):
        return True
    if any(re.search(r"\b%s\b" % re.escape(w), rank) for w in MONASTIC_WORDS):
        return True
    # The life is consulted only where the rank column says nothing useful.
    # Almost every bishop was tonsured before his consecration, and Russian
    # still calls him святитель, so reading the life for a rank that is
    # already given would turn every hierarch into a monastic.
    if rank.split(" \u00b7 ")[0].strip() not in ("Saint", "Venerable", ""):
        return False
    return bool(re.search(r"\b(a monk|a nun|the monastic life|as a monk|"
                          r"was tonsured|received the tonsure|monastic habit|"
                          r"a hermit|an anchorite)\b", blob))


def modules(pkg, directory):
    sys.path.insert(0, str(directory.parent))
    out = {}
    for m in pkgutil.iter_modules([str(directory)]):
        mod = importlib.import_module("%s.%s" % (pkg, m.name))
        out[m.name] = dict(getattr(mod, "TEXT", {}))
    return out


def opening(text):
    return " ".join((text or "").split()[:14])


# A saint whose own Church says his name a particular way, where that way
# happens to be the bare honorific. This is not an exemption from the rule;
# it is the rule in CLAUDE.md that a received form is used and not
# re-rendered. Serbian says Свети Симеон Мироточиви of Stefan Nemanja and
# Света Петка of Parascheva - the second names half the churches in the
# country - and writing Преподобни over either would be the site correcting
# the Serbian Church in its own language. Anything added here needs that
# kind of reason, written down.
RECEIVED = {
    "sr": {
        "St Simeon the Myrrh-gusher",
        "Venerable Stephen (in monasticism Simeon), the Myrrhgusher and "
        "Prince of Serbia",
        "St Parascheva of Ia\u0219i",
        "Venerable Paraskevi (Petka) of Serbia",
    },
}


def audit(lang, entries, types, source):
    """Two findings, and the difference between them matters.

    An error is a saint introduced by the generic word for holy and nothing
    else - the English sentence in the language's words. A review is a saint
    given some other real rank than the one his order would suggest, which
    is a judgement a calendar may legitimately make and a script may not.
    """
    spec = LANGS[lang]
    if not spec.get("generic", "").strip():
        # An empty pattern matches at every position, so a blank left in a
        # scaffolded spec would pass every opening silently rather than
        # checking any of them.
        raise SystemExit(
            "%s has no generic pattern: the bare word for holy has still to "
            "be written into LANGS in tools/check_register.py" % lang)
    generic = re.compile(spec["generic"])
    ranks = re.compile(spec["ranks"])
    monastic = re.compile(spec["monastic"])
    errors, review = [], []
    for name, value in sorted(entries.items()):
        text = value.get("life") if isinstance(value, dict) else value
        head = opening(text)
        if not head:
            continue
        m = generic.match(head)
        opens_generic = bool(m) and not ranks.search(head[m.end():m.end() + 40])
        if is_monastic(types.get(name, "")):
            if monastic.search(head):
                continue
            if opens_generic:
                if name in RECEIVED.get(lang, ()):
                    review.append(("received form, left as the Church says it",
                                   source, name, head))
                    continue
                errors.append(("monastic given the generic honorific",
                               source, name, head))
            else:
                review.append(("monastic named by another rank",
                               source, name, head))
            continue
        if opens_generic and spec.get("strict"):
            errors.append(("bare honorific before a name", source, name, head))
    return errors, review


# The orders a language names a saint by, as the Saints index words them.
# A language that has written its vocabulary has already rendered nearly all
# of these, so the grammar below is drawn from that table rather than made up
# a second time in a different file.
RANKWORDS = ("Venerable", "Hierarch", "Apostle", "Prophet", "Martyr",
             "Great Martyr", "Hieromartyr", "Confessor", "Righteous",
             "Passion-bearer", "Unmercenary", "Fool-for-Christ", "New Martyr",
             "Equal-to-the-Apostles", "Virgin Martyr", "Virgin", "Feast",
             "Synaxis", "Bishop", "Archbishop", "Metropolitan", "Patriarch",
             "Abbot (Igumen)", "Abbess", "Archimandrite", "Monk", "Nun",
             "Deacon", "Priest", "Presbyter", "Prince", "Princess", "King",
             "Empress", "Stylite", "Hermit", "Recluse", "Schemamonk")


def scaffold(lang):
    """A draft register spec for a language, drawn from its own vocabulary.

    Two of the four slots can be derived and two cannot. The ranks are the
    renderings the terms table already carries, and the monastic honorific is
    whatever that table renders Venerable as. The bare word for holy, and
    whether the language forbids it before a name, are the language's own
    business and are left blank on purpose: Russian and Ukrainian forbid it,
    Greek, Romanian and German do not, and no table says which.
    """
    path = Path(__file__).resolve().parent / "saint_terms" / ("%s.py" % lang)
    if not path.exists():
        raise SystemExit(
            "no tools/saint_terms/%s.py yet - the vocabulary is written "
            "before the grammar, because the grammar is drawn from it.\n"
            "Begin it with: python3 tools/loop.py terms %s --start <Name>"
            % (lang, lang))
    spec = importlib.util.spec_from_file_location("_terms_%s" % lang, path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    text = getattr(mod, "TEXT", {})

    forms, missing = [], []
    for w in RANKWORDS:
        v = (text.get(w) or "").strip()
        if v:
            forms.append(v)
        else:
            missing.append(w)
    if not forms:
        raise SystemExit("%s renders none of the rank words yet" % lang)

    seen, ranks = set(), []
    for f in sorted(forms, key=lambda s: (-len(s), s)):
        if f.lower() not in seen:
            seen.add(f.lower())
            ranks.append(re.escape(f))

    monastic = (text.get("Venerable") or "").strip()
    print("# Drawn from tools/saint_terms/%s.py. Paste into LANGS in this\n"
          "# file, then do the two things a table cannot do for you:\n"
          "#   generic  the bare word for holy, with its inflections\n"
          "#   strict   True if this language forbids it before a name\n"
          "# and trim the ranks below to stems, so a declined form still\n"
          "# matches: Ehrwuerdiger -> [Ee]hrwuerdig." % lang)
    if missing:
        print("# The terms table renders no %s yet."
              % ", ".join(missing[:8])
              + (" (+%d more)" % (len(missing) - 8) if len(missing) > 8 else ""))
    print('    "%s": {' % lang)
    print('        "generic": r"",   # REQUIRED - the check refuses a blank')
    print('        "ranks": (r"%s"),' % "|".join(ranks))
    print('        "monastic": r"%s",' % (re.escape(monastic) or ""))
    print('        "strict": False,')
    print('    },')
    return 0


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--lang")
    ap.add_argument("--show", type=int, default=5)
    ap.add_argument("--scaffold", action="store_true",
                    help="draft this language's register spec from its terms")
    ap.add_argument("--review", type=int, metavar="N",
                    help="the next N openings worth a second look")
    args = ap.parse_args()

    if args.scaffold:
        if not args.lang:
            raise SystemExit("--scaffold needs --lang")
        return scaffold(args.lang)

    types = english_types()
    info = modules("saint_info", INFO_DIR)
    lives = modules("saint_lives", LIVES_DIR)

    langs = [args.lang] if args.lang else sorted(set(info) | set(lives))
    total = 0
    for lang in langs:
        if lang not in LANGS:
            print("%-4s no register rules written yet" % lang)
            continue
        e1, r1 = audit(lang, info.get(lang, {}), types, "calendar")
        e2, r2 = audit(lang, lives.get(lang, {}), types, "life")
        found, soft = e1 + e2, r1 + r2

        if args.review:
            # Sorted, so the same command tomorrow returns the same queue and
            # a run picked up after an interruption does not begin again.
            soft = sorted(soft, key=lambda f: (f[1], f[2]))
            print("%s: %d worth a second look" % (lang, len(soft)))
            for kind, src, name, head in soft[:args.review]:
                print("\n[%s] %s\n  %s\n  %s"
                      % (src, name, kind, head))
                order = (types.get(name) or "").split("||")[0].strip()
                print("  order: %s" % (order or "(none given)"))
            continue
        total += len(found)
        n = len(info.get(lang, {})) + len(lives.get(lang, {}))
        print("%-4s %4d of %d openings name a saint the English way   "
              "(%d more worth a second look)" % (lang, len(found), n, len(soft)))
        kinds = {}
        for kind, src, name, head in found:
            kinds.setdefault(kind, []).append((src, name, head))
        for kind in sorted(kinds, key=lambda k: -len(kinds[k])):
            print("       %-30s %4d" % (kind, len(kinds[kind])))
            for src, name, head in kinds[kind][:args.show]:
                print("           [%s] %s" % (src, name[:60]))
                print("                %s" % head[:100])

    if total:
        print("\n%d opening(s) name a saint the way English does." % total)
        return 1
    print("\nEvery opening names the saint the way the language does.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
