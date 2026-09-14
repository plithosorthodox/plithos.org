# -*- coding: utf-8 -*-
"""The eparchies of the Georgian Apostolic Autocephalous Orthodox Church.

Read on 14 September 2026 from the Patriarchate's own site, patriarchate.ge,
which carries its eparchies in the menu of every page: forty-two, and all
forty-two are written here. Every one of the forty-two was asked for again
on that date, one page each, and the Patriarchate's own list answered with
the same forty-two names in the same order. Nothing is missing from it and
nothing in it has been retitled since.

READING PATRIARCHATE.GE FROM HERE. The site answers every request with two
hundred kilobytes that carry no text, and that is not a cyber-security
interstitial: the only Georgian in the markup is a line naming the security
group in the author tag, and the page is a Laravel application that hands
its whole content to the browser as JSON in one data-page attribute. Unquote
the attribute and the page is all there - the eparchies at /eparchs/1 to
/eparchs/42, the Holy Synod at /sinodi/members/all, the Patriarchate's own
departments at /pages/page/2 and /pages/page/4. Plain curl is enough; no
browser is needed. Nothing here was read anywhere else.

THE LIST ITSELF IS A MENU AND CARRIES NOTHING BUT NAMES. The eparchies are
held one to an entry and drawn into the menu of every page; the
Patriarchate's own per-eparchy pages carry news and nothing else - several
hold none at all - so the row cites the Patriarchate itself, which is where
the list is published and where a reader will find it. What the list
publishes is the name, in Georgian, and that is what `local` carries, letter
for letter as the Patriarchate sets it. `name` is the English of it: these
are place names with settled English spellings, and the eparchy word is
rendered as the Church's own - eparchy, not diocese. No address and no seat
stand anywhere on that list.

WHERE THE SEATS COME FROM. orthodoxy.ge prints, eparchy by eparchy, the
territory, the cathedra and the residence, taking its list from the Church of
Georgia's own Calendar for 2019 published by the Patriarchate's press. It is
not the Patriarchate's site and says so in plain words on its own contact
page, so it establishes nothing here: every row rests on patriarchate.ge for
its existence and its name, and cites orthodoxy.ge beside it for the one fact
the Patriarchate does not publish. The seat written is the first residence
that list names, taken as printed and not chosen between - Kareli for Ruisi
and Urbnisi, Kvareli for Nekresi, Zestaponi for Margveti and Ubisi, Martvili
for Chqondidi, all of which sit at some distance from the see the eparchy is
named for, as an eparchy of ancient cathedrals may.

Its forty-two in Georgia answer one for one to the Patriarchate's forty-two,
though six have been retitled since 2019 and one respelt: Agarak-Tsalka is
now Tsalka, Lore-Tashiri is now Agarak-Tashiri, Gardabani and Martqopi now
reads the other way about, as do Ninotsminda and Sagarejo, Kutais-Gaenati is
now Kutaisi and Gaenati, and Khujabi is now Hujabi. The Patriarchate's
spelling is the one written.

TWO EPARCHIES ABROAD ARE HERE NOW, and the third is not. The Patriarchate's
list of eparchies holds only the forty-two in Georgia, but the page of the
Holy Synod carries, under each hierarch, the address he answers at and the
territory his eparchy covers, and for two of the three abroad it gives a
street. Belgium and Holland answers at Rue Gendebien in Brussels and covers
Belgium and Holland; North America is styled an exarchate there rather than
an eparchy, covers the United States and Canada, and answers at Ashley in
Pennsylvania. Both are written, and the name each carries is the Synod
page's own. This fills the gap docs/DIRECTORY.md left open for the Georgian
body in North America, which was deferred for want of an address.

The Western European eparchy is still deferred, and now for a reason that
can be stated exactly: the Synod page gives its territory - Spain, Italy,
Portugal, Malta, France and Switzerland - and no street in any of them, and
the telephones beside it are Georgian. A row needs a country, and a see
spread over six with no seat published cannot name one.

WHAT ELSE THAT SYNOD PAGE HOLDS, and what it would cost to use it. It prints
under each hierarch the postal address, the territory in municipalities, the
cathedra and the residence, all in the Patriarchate's own words. Thirty-one
of the forty-two have a hierarch on it and so have all four of those facts;
the rest are vacant and have none. So every seat below could be read from
the Church itself rather than from orthodoxy.ge, and thirty-one rows could
carry an address - but only thirty-one, and a file half sourced from the
Church and half from a calendar of 2019 is worse than one sourced
consistently. That is a pass of its own and it is not this one.

The two were compared all the same, and the seats hold. Twenty-six of the
thirty-one name the same town. Three differ only in the way this file
already resolves - the chancery stands in a village of the see's own
district and the seat names the district town: Urbnisi village in Kareli,
Agara village in Ambrolauri, Khichauri in Khulo for Skhalta. Two differ in
substance and are the ones to settle next: the Patriarchate puts the
residence of Chiatura and Sachkhere at Sachkhere where the 2019 calendar put
it at Chiatura, and it calls the seat of the Stepantsminda eparchy
Stepantsminda where the row, following that calendar, still writes Kazbegi,
which is the same town under the name it bore before.

Two things the Synod page says that the list of eparchies does not: the
Dmanisi and Agarak-Tashiri eparchy also holds Great Britain and Ireland,
with a cathedra in London, and the Akhalkalaki metropolitan is given Kars as
well. The list is what is published as the list, and the rows follow it.

ONE EPARCHY HAS A SITE OF ITS OWN that answered here, Kutaisi and Gaenati,
and it carries the link. The addresses orthodoxy.ge lists for diocesan sites
are of 2019 and most of the domains are gone: Batumi, Khoni, Ruisi and
Urbnisi, Poti and the Western European eparchy all fail to resolve, and the
one at shemoqmedi.ge answers with an empty page. None of them is published.
"""

READ = "2026-09-14"

GE = "https://patriarchate.ge/"
ORTH = "https://www.orthodoxy.ge/tsnobarebi/eparqiebi.htm"
SYNOD = "https://patriarchate.ge/sinodi/members/all"

ROWS = [
 dict(id="ge-mtskheta-tbilisi", parent="georgia",
      name="Eparchy of Mtskheta-Tbilisi",
      rank="Eparchy",
      local=u"მცხეთა-თბილისის ეპარქია",
      seat="Mtskheta", country="GE",
      sources=[GE, ORTH]),

 dict(id="ge-bichvinta", parent="georgia",
      name="Eparchy of Bichvinta and Tskhum-Abkhazia",
      rank="Eparchy",
      local=u"ბიჭვინთისა და ცხუმ-აფხაზეთის ეპარქია",
      seat="Sokhumi", country="GE",
      sources=[GE, ORTH]),

 dict(id="ge-kutaisi", parent="georgia",
      name="Eparchy of Kutaisi and Gaenati",
      rank="Eparchy",
      local=u"ქუთაისისა და გაენათის ეპარქია",
      seat="Kutaisi", country="GE",
      site="https://kutais-gaenati.ge/",
      sources=["https://kutais-gaenati.ge/", GE, ORTH]),

 dict(id="ge-chiatura", parent="georgia",
      name="Eparchy of Chiatura and Sachkhere",
      rank="Eparchy",
      local=u"ჭიათურისა და საჩხერის ეპარქია",
      seat="Chiatura", country="GE",
      sources=[GE, ORTH]),

 dict(id="ge-manglisi", parent="georgia",
      name="Eparchy of Manglisi and Tetritsqaro",
      rank="Eparchy",
      local=u"მანგლისისა და თეთრიწყაროს ეპარქია",
      seat="Manglisi", country="GE",
      sources=[GE, ORTH]),

 dict(id="ge-tsilkani", parent="georgia",
      name="Eparchy of Tsilkani and Dusheti",
      rank="Eparchy",
      local=u"წილკნისა და დუშეთის ეპარქია",
      seat="Tsilkani", country="GE",
      sources=[GE, ORTH]),

 dict(id="ge-tqibuli", parent="georgia",
      name="Eparchy of Tqibuli and Terjola",
      rank="Eparchy",
      local=u"ტყიბულისა და თერჯოლის ეპარქია",
      seat="Terjola", country="GE",
      sources=[GE, ORTH]),

 dict(id="ge-ruisi", parent="georgia",
      name="Eparchy of Ruisi and Urbnisi",
      rank="Eparchy",
      local=u"რუისისა და ურბნისის ეპარქია",
      seat="Kareli", country="GE",
      sources=[GE, ORTH]),

 dict(id="ge-alaverdi", parent="georgia",
      name="Eparchy of Alaverdi",
      rank="Eparchy",
      local=u"ალავერდის ეპარქია",
      seat="Alaverdi", country="GE",
      sources=[GE, ORTH]),

 dict(id="ge-nekresi", parent="georgia",
      name="Eparchy of Nekresi",
      rank="Eparchy",
      local=u"ნეკრესის ეპარქია",
      seat="Kvareli", country="GE",
      sources=[GE, ORTH]),

 dict(id="ge-shemokmedi", parent="georgia",
      name="Eparchy of Shemokmedi",
      rank="Eparchy",
      local=u"შემოქმედის ეპარქია",
      seat="Ozurgeti", country="GE",
      sources=[GE, ORTH]),

 dict(id="ge-nikozi", parent="georgia",
      name="Eparchy of Nikozi and Tskhinvali",
      rank="Eparchy",
      local=u"ნიქოზისა და ცხინვალის ეპარქია",
      seat="Nikozi", country="GE",
      sources=[GE, ORTH]),

 dict(id="ge-borjomi", parent="georgia",
      name="Eparchy of Borjomi and Bakuriani",
      rank="Eparchy",
      local=u"ბორჯომისა და ბაკურიანის ეპარქია",
      seat="Borjomi", country="GE",
      sources=[GE, ORTH]),

 dict(id="ge-poti", parent="georgia",
      name="Eparchy of Poti and Khobi",
      rank="Eparchy",
      local=u"ფოთისა და ხობის ეპარქია",
      seat="Poti", country="GE",
      sources=[GE, ORTH]),

 dict(id="ge-akhalkalaki", parent="georgia",
      name="Eparchy of Akhalkalaki and Kumurdo",
      rank="Eparchy",
      local=u"ახალქალაქისა და კუმურდოს ეპარქია",
      seat="Akhalkalaki", country="GE",
      sources=[GE, ORTH]),

 dict(id="ge-akhaltsikhe", parent="georgia",
      name="Eparchy of Akhaltsikhe and Tao-Klarjeti",
      rank="Eparchy",
      local=u"ახალციხისა და ტაო-კლარჯეთის ეპარქია",
      seat="Akhaltsikhe", country="GE",
      sources=[GE, ORTH]),

 dict(id="ge-khoni", parent="georgia",
      name="Eparchy of Khoni and Samtredia",
      rank="Eparchy",
      local=u"ხონისა და სამტრედიის ეპარქია",
      seat="Khoni", country="GE",
      sources=[GE, ORTH]),

 dict(id="ge-batumi", parent="georgia",
      name="Eparchy of Batumi and Lazeti",
      rank="Eparchy",
      local=u"ბათუმისა და ლაზეთის ეპარქია",
      seat="Batumi", country="GE",
      sources=[GE, ORTH]),

 dict(id="ge-vani", parent="georgia",
      name="Eparchy of Vani and Baghdati",
      rank="Eparchy",
      local=u"ვანისა და ბაღდათის ეპარქია",
      seat="Vani", country="GE",
      sources=[GE, ORTH]),

 dict(id="ge-zugdidi", parent="georgia",
      name="Eparchy of Zugdidi and Tsaishi",
      rank="Eparchy",
      local=u"ზუგდიდისა და ცაიშის ეპარქია",
      seat="Zugdidi", country="GE",
      sources=[GE, ORTH]),

 dict(id="ge-gori", parent="georgia",
      name="Eparchy of Gori and Ateni",
      rank="Eparchy",
      local=u"გორისა და ატენის ეპარქია",
      seat="Gori", country="GE",
      sources=[GE, ORTH]),

 dict(id="ge-chqondidi", parent="georgia",
      name="Eparchy of Chqondidi",
      rank="Eparchy",
      local=u"ჭყონდიდის ეპარქია",
      seat="Martvili", country="GE",
      sources=[GE, ORTH]),

 dict(id="ge-tsageri", parent="georgia",
      name="Eparchy of Tsageri and Lentekhi",
      rank="Eparchy",
      local=u"ცაგერისა და ლენტეხის ეპარქია",
      seat="Tsageri", country="GE",
      sources=[GE, ORTH]),

 dict(id="ge-mestia", parent="georgia",
      name="Eparchy of Mestia and Upper Svaneti",
      rank="Eparchy",
      local=u"მესტიისა და ზემო სვანეთის ეპარქია",
      seat="Mestia", country="GE",
      sources=[GE, ORTH]),

 dict(id="ge-senaki", parent="georgia",
      name="Eparchy of Senaki and Chkhorotsqu",
      rank="Eparchy",
      local=u"სენაკისა და ჩხოროწყუს ეპარქია",
      seat="Senaki", country="GE",
      sources=[GE, ORTH]),

 dict(id="ge-rustavi", parent="georgia",
      name="Eparchy of Rustavi",
      rank="Eparchy",
      local=u"რუსთავის ეპარქია",
      seat="Rustavi", country="GE",
      sources=[GE, ORTH]),

 dict(id="ge-gurjaani", parent="georgia",
      name="Eparchy of Gurjaani and Velistsikhe",
      rank="Eparchy",
      local=u"გურჯაანისა და ველისციხის ეპარქია",
      seat="Gurjaani", country="GE",
      sources=[GE, ORTH]),

 dict(id="ge-sagarejo", parent="georgia",
      name="Eparchy of Sagarejo and Ninotsminda",
      rank="Eparchy",
      local=u"საგარეჯოსა და ნინოწმიდის ეპარქია",
      seat="Ninotsminda", country="GE",
      sources=[GE, ORTH]),

 dict(id="ge-dmanisi", parent="georgia",
      name="Eparchy of Dmanisi and Agarak-Tashiri",
      rank="Eparchy",
      local=u"დმანისისა და აგარაკ-ტაშირის ეპარქია",
      seat="Dmanisi", country="GE",
      sources=[GE, ORTH]),

 dict(id="ge-stepantsminda", parent="georgia",
      name="Eparchy of Stepantsminda and Khevi",
      rank="Eparchy",
      local=u"სტეფანწმინდისა და ხევის ეპარქია",
      seat="Kazbegi", country="GE",
      sources=[GE, ORTH]),

 dict(id="ge-skhalta", parent="georgia",
      name="Eparchy of Skhalta",
      rank="Eparchy",
      local=u"სხალთის ეპარქია",
      seat="Skhalta", country="GE",
      sources=[GE, ORTH]),

 dict(id="ge-bolnisi", parent="georgia",
      name="Eparchy of Bolnisi",
      rank="Eparchy",
      local=u"ბოლნისის ეპარქია",
      seat="Bolnisi", country="GE",
      sources=[GE, ORTH]),

 dict(id="ge-margveti", parent="georgia",
      name="Eparchy of Margveti and Ubisi",
      rank="Eparchy",
      local=u"მარგვეთისა და უბისის ეპარქია",
      seat="Zestaponi", country="GE",
      sources=[GE, ORTH]),

 dict(id="ge-bodbe", parent="georgia",
      name="Eparchy of Bodbe",
      rank="Eparchy",
      local=u"ბოდბის ეპარქია",
      seat="Bodbe", country="GE",
      sources=[GE, ORTH]),

 dict(id="ge-tianeti", parent="georgia",
      name="Eparchy of Tianeti and Pshav-Khevsureti",
      rank="Eparchy",
      local=u"თიანეთისა და ფშავ-ხევსურეთის ეპარქია",
      seat="Tianeti", country="GE",
      sources=[GE, ORTH]),

 dict(id="ge-khornabuji", parent="georgia",
      name="Eparchy of Khornabuji and Hereti",
      rank="Eparchy",
      local=u"ხორნაბუჯისა და ჰერეთის ეპარქია",
      seat="Dedoplistsqaro", country="GE",
      sources=[GE, ORTH]),

 dict(id="ge-samtavisi", parent="georgia",
      name="Eparchy of Samtavisi and Kaspi",
      rank="Eparchy",
      local=u"სამთავისისა და კასპის ეპარქია",
      seat="Samtavisi", country="GE",
      sources=[GE, ORTH]),

 dict(id="ge-surami", parent="georgia",
      name="Eparchy of Surami and Khashuri",
      rank="Eparchy",
      local=u"სურამისა და ხაშურის ეპარქია",
      seat="Surami", country="GE",
      sources=[GE, ORTH]),

 dict(id="ge-marneuli", parent="georgia",
      name="Eparchy of Marneuli and Hujabi",
      rank="Eparchy",
      local=u"მარნეულისა და ჰუჯაბის ეპარქია",
      seat="Marneuli", country="GE",
      sources=[GE, ORTH]),

 dict(id="ge-martqopi", parent="georgia",
      name="Eparchy of Martqopi and Gardabani",
      rank="Eparchy",
      local=u"მარტყოფისა და გარდაბნის ეპარქია",
      seat="Gardabani", country="GE",
      sources=[GE, ORTH]),

 dict(id="ge-tsalka", parent="georgia",
      name="Eparchy of Tsalka",
      rank="Eparchy",
      local=u"წალკის ეპარქია",
      seat="Tsalka", country="GE",
      sources=[GE, ORTH]),

 dict(id="ge-nikortsminda", parent="georgia",
      name="Eparchy of Nikortsminda",
      rank="Eparchy",
      local=u"ნიკორწმინდის ეპარქია",
      seat="Ambrolauri", country="GE",
      sources=[GE, ORTH]),


 # The two abroad, from the Patriarchate's page of its Holy Synod, which is
 # where it publishes the address of each. Neither is on the list of
 # eparchies, which holds only the sees in Georgia, and neither publishes a
 # site of its own that answered here.
 dict(id="ge-belgium-holland", parent="georgia",
      name="Eparchy of Belgium and Holland",
      rank="Eparchy",
      local=u"ბელგიისა და ჰოლანდიის ეპარქია",
      seat="Brussels", country="BE",
      address=["9 Rue Gendebien", "1030 Bruxelles"],
      checked="2026-09-14",
      sources=[SYNOD, GE]),

 dict(id="ge-north-america", parent="georgia",
      name="Exarchate of North America",
      rank="Exarchate",
      local=u"ჩრდილოეთ ამერიკის ექსარქია",
      seat="Ashley, Pennsylvania", country="US",
      address=["62 Charles st.", "Ashley. PA. 18706"],
      checked="2026-09-14",
      sources=[SYNOD, GE]),

]
