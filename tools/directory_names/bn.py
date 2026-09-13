# -*- coding: utf-8 -*-
"""The directory's rows in Bengali.

The place first in the genitive, then the head, as the lives and the
commemorations write it: রাশিয়ার মণ্ডলী, আমেরিকার অর্থোডক্স মণ্ডলী. The second
of those is taken whole from what the site already prints, and so is the
adjectival রুশ অর্থোডক্স মণ্ডলী pattern that ম্যাসিডোনীয় অর্থোডক্স মণ্ডলী follows.

Two things had to be settled by counting.

  - **The Church, as a body, is মণ্ডলী and not গির্জা** - 3,097 against 1,690
    across the lives, the entries, the glossary and the vocabulary, and it is
    what the site itself prints for the Church of Rus' and for the Russian
    Orthodox Church. গির্জা carries the building, and the directory's heading
    keeps it for the plural; a row names the Church, so a row says মণ্ডলী.
  - **Antioch is আন্তিওখ**, 216 against আন্তিয়খ 7.

Macedonia is ম্যাসিডোনিয়া, 45 to মেসিডোনিয়া 14, and the adjective the site
already writes is ম্যাসিডোনীয়.

Constantinople keeps its received form কনস্টান্টিনোপল, written 1,286 times
here with no ইস্তাম্বুল beside it, and it stands as the seat of the Ecumenical
Patriarchate.

Written here because the site has never named them in Bengali, and named so
that nobody later mistakes them for received forms: তিরানা Tirana, স্কোপিয়ে
Skopje, প্রেশভ Presov, টোকিও Tokyo, তাল্লিন Tallinn, সিওসেট Syosset,
ফিনল্যান্ড Finland, জাপান Japan, এস্তোনিয়া Estonia and স্লোভাকিয়া Slovakia, the
last built on স্লোভাক, which the site already writes of the faithful of that
land. Three of them - টোকিও, সিওসেট and স্লোভাকিয়ার, which is স্লোভাকিয়া with
the genitive Bengali cannot leave off - are what the audit reports, and the
report is right. The rest answer to stems it already has.

মহাধর্মপ্রদেশ, for the Archbishopric of Ohrid, is ধর্মপ্রদেশ - the site's own
word for a diocese - under মহা-.
"""
NAMES = {
    "constantinople": u"কনস্টান্টিনোপলের মণ্ডলী",
    "alexandria": u"আলেকজান্দ্রিয়ার মণ্ডলী",
    "antioch": u"আন্তিওখের মণ্ডলী",
    "jerusalem": u"জেরুজালেমের মণ্ডলী",
    "russia": u"রাশিয়ার মণ্ডলী",
    "georgia": u"জর্জিয়ার মণ্ডলী",
    "serbia": u"সার্বিয়ার মণ্ডলী",
    "romania": u"রোমানিয়ার মণ্ডলী",
    "bulgaria": u"বুলগেরিয়ার মণ্ডলী",
    "cyprus": u"সাইপ্রাসের মণ্ডলী",
    "greece": u"গ্রিসের মণ্ডলী",
    "albania": u"আলবেনিয়ার মণ্ডলী",
    "poland": u"পোল্যান্ডের মণ্ডলী",
    "czech-slovakia": u"চেক ভূমি ও স্লোভাকিয়ার মণ্ডলী",
    "oca": u"আমেরিকার অর্থোডক্স মণ্ডলী",
    "macedonia": u"ম্যাসিডোনীয় অর্থোডক্স মণ্ডলী - ওহ্রিদের মহাধর্মপ্রদেশ",
    "ukraine-uoc": u"ইউক্রেনের মণ্ডলী",
    "ukraine-ocu": u"ইউক্রেনের অর্থোডক্স মণ্ডলী",
    "sinai": u"সিনাইয়ের মণ্ডলী",
    "finland": u"ফিনল্যান্ডের স্বায়ত্তশাসিত মণ্ডলী",
    "japan": u"জাপানের মণ্ডলী",
    "estonia-eaok": u"এস্তোনিয়ার অর্থোডক্স মণ্ডলী",
}
SEATS = {
    "Istanbul": u"কনস্টান্টিনোপল",
    "Alexandria": u"আলেকজান্দ্রিয়া",
    "Damascus": u"দামেস্ক",
    "Jerusalem": u"জেরুজালেম",
    "Moscow": u"মস্কো",
    "Tbilisi": u"তিবিলিসি",
    "Belgrade": u"বেলগ্রেড",
    "Bucharest": u"বুখারেস্ট",
    "Sofia": u"সোফিয়া",
    "Nicosia": u"নিকোসিয়া",
    "Athens": u"এথেন্স",
    "Tirana": u"তিরানা",
    "Warsaw": u"ওয়ারশ",
    "Prešov": u"প্রেশভ",
    "Syosset, New York": u"সিওসেট, নিউ ইয়র্ক",
    "Skopje": u"স্কোপিয়ে",
    "Kyiv": u"কিয়েভ",
    "Mount Sinai": u"সিনাই পর্বত",
    "Helsinki": u"হেলসিঙ্কি",
    "Tokyo": u"টোকিও",
    "Tallinn": u"তাল্লিন",
}
