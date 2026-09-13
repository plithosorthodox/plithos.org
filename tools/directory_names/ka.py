# -*- coding: utf-8 -*-
"""ეკლესიები და მათი კათედრები - the Churches and their seats, in Georgian.

Mkhedruli only, as docs/GEORGIAN.md requires, and nothing rendered afresh:
every see, country and city was read off the Georgian this site already
publishes - the place vocabulary beside the lives, the calendar entries and
the saints' names. So კონსტანტინოპოლი, ალექსანდრია, ანტიოქია,
იერუსალიმი, დამასკო, მოსკოვი, თბილისი, ბელგრადი, ბუქარესტი, სოფია,
ნიკოსია, ათენი, ვარშავა, კიევი, ნიუ-იორკი, ოხრიდი and სინის მთა are the
forms already printed.

Two of them would have been got wrong by ear. **ნიკოსია** is Nicosia in
Cyprus; ნიქოზი, which the corpus also carries, is Nikozi in Georgia and is
a different place. And **სინის მთა** is what the vocabulary writes for
Mount Sinai, against the bare სინა it writes for the region, so the seat
takes the mountain and the Church takes the region.

The name of a local Church is built head-last, as Georgian builds it and as
the corpus already has it: რუსეთის ეკლესია, სერბეთის ეკლესია, ანტიოქიის
ეკლესია, and ამერიკის მართლმადიდებელი ეკლესია, which the site writes
twenty times for the body in this row. ჩეხეთის მიწები is the vocabulary's
own rendering of the Czech Lands.

ესტონეთი, ფინეთი, იაპონია and სლოვაკეთი are taken unchanged from the
country table in tools/directory_words.py, where this site settled them
already. Five places the Georgian pages have never had occasion to name are
written here in the received Georgian form: სტამბოლი, ტირანა, პრეშოვი,
სიოსეტი, სკოპიე, ტალინი and ტოკიო.
"""
NAMES = {
    "constantinople": u"კონსტანტინოპოლის ეკლესია",
    "alexandria": u"ალექსანდრიის ეკლესია",
    "antioch": u"ანტიოქიის ეკლესია",
    "jerusalem": u"იერუსალიმის ეკლესია",
    "russia": u"რუსეთის ეკლესია",
    "georgia": u"საქართველოს ეკლესია",
    "serbia": u"სერბეთის ეკლესია",
    "romania": u"რუმინეთის ეკლესია",
    "bulgaria": u"ბულგარეთის ეკლესია",
    "cyprus": u"კვიპროსის ეკლესია",
    "greece": u"საბერძნეთის ეკლესია",
    "albania": u"ალბანეთის ეკლესია",
    "poland": u"პოლონეთის ეკლესია",
    "czech-slovakia": u"ჩეხეთის მიწებისა და სლოვაკეთის ეკლესია",
    "oca": u"ამერიკის მართლმადიდებელი ეკლესია",
    "macedonia": u"მაკედონიის მართლმადიდებელი ეკლესია - ოხრიდის მთავარეპისკოპოსობა",
    "ukraine-uoc": u"უკრაინის ეკლესია",
    "ukraine-ocu": u"უკრაინის მართლმადიდებელი ეკლესია",
    "sinai": u"სინის ეკლესია",
    "finland": u"ფინეთის ავტონომიური ეკლესია",
    "japan": u"იაპონიის ეკლესია",
    "estonia-eaok": u"ესტონეთის მართლმადიდებელი ეკლესია",
}
SEATS = {
    "Istanbul": u"სტამბოლი",
    "Alexandria": u"ალექსანდრია",
    "Damascus": u"დამასკო",
    "Jerusalem": u"იერუსალიმი",
    "Moscow": u"მოსკოვი",
    "Tbilisi": u"თბილისი",
    "Belgrade": u"ბელგრადი",
    "Bucharest": u"ბუქარესტი",
    "Sofia": u"სოფია",
    "Nicosia": u"ნიკოსია",
    "Athens": u"ათენი",
    "Tirana": u"ტირანა",
    "Warsaw": u"ვარშავა",
    "Prešov": u"პრეშოვი",
    "Syosset, New York": u"სიოსეტი, ნიუ-იორკი",
    "Skopje": u"სკოპიე",
    "Kyiv": u"კიევი",
    "Mount Sinai": u"სინის მთა",
    "Helsinki": u"ჰელსინკი",
    "Tokyo": u"ტოკიო",
    "Tallinn": u"ტალინი",
}
