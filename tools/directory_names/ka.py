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
country table this site has already settled, so the four countries the
Georgian pages never name are not settled twice. The lives do name two of
those peoples - ესტონელები and სლოვაკი მორწმუნენი - but not their countries.

Seven cities the Georgian pages have never had occasion to name are written
here: სტამბოლი, ტირანა, პრეშოვი, სიოსეტი, სკოპიე, ტალინი and ტოკიო. Georgian
keeps no Latin letter in a name, so Prešov is written out in Mkhedruli like
the rest. მთავარეპისკოპოსობა is built on მთავარეპისკოპოსი, which stands 783
times.

The official names are a third table, STYLED, and not a second version of the
first: the label is the list's word for a body and the style is the body's
own. Seven of the nine stood already in the Georgian this site publishes and
are taken whole - მსოფლიო საპატრიარქო, ალექსანდრიის and იერუსალიმის
საპატრიარქო, and the რუსეთის, სერბეთის, რუმინეთის and უკრაინის
მართლმადიდებელი ეკლესია of the commemorations.

Antioch follows the მოსკოვისა და სრულიად რუსეთის პატრიარქი the calendar
writes, with სრულიად doing the work of the English All; ბულგარეთის
საპატრიარქო follows ალექსანდრიის საპატრიარქო.

The word Greek in the English style of Antioch and of Jerusalem is the Rum
rite and communion, not the Greek nation, and no Georgian name for either
body carries it, so it is not written here.
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
STYLED = {
    "constantinople": u"მსოფლიო საპატრიარქო",
    "alexandria": u"ალექსანდრიის საპატრიარქო",
    "antioch": u"ანტიოქიისა და სრულიად აღმოსავლეთის საპატრიარქო",
    "jerusalem": u"იერუსალიმის საპატრიარქო",
    "russia": u"რუსეთის მართლმადიდებელი ეკლესია",
    "serbia": u"სერბეთის მართლმადიდებელი ეკლესია",
    "romania": u"რუმინეთის მართლმადიდებელი ეკლესია",
    "bulgaria": u"ბულგარეთის მართლმადიდებელი ეკლესია - ბულგარეთის საპატრიარქო",
    "ukraine-uoc": u"უკრაინის მართლმადიდებელი ეკლესია",
}
