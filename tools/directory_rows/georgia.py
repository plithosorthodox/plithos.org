# -*- coding: utf-8 -*-
"""The eparchies of the Georgian Apostolic Autocephalous Orthodox Church.

Read on 14 September 2026 from the Patriarchate's own site, patriarchate.ge,
which carries its eparchies in the menu of every page: forty-two, and all
forty-two are written here.

THE SITE RENDERS THROUGH SCRIPT AND ITS PAGES CARRY NO LIST IN THEIR MARKUP.
The eparchies are held one to an entry and drawn into the menu when a reader
opens any page; the Patriarchate's own per-eparchy pages carry news and
nothing else - several hold none at all - so the row cites the Patriarchate
itself, which is where the list is published and where a reader will find it.

THE PATRIARCHATE PUBLISHES NO ADDRESS FOR ANY EPARCHY, and no telephone and
no seat. What it publishes is the name, in Georgian, and that is what `local`
carries, letter for letter as the Patriarchate sets it. `name` is the English
of it: these are place names with settled English spellings, and the eparchy
word is rendered as the Church's own - eparchy, not diocese.

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

The Holy Synod's own page gives the Metropolitan of Akhalkalaki a third city,
Kars, that the list of eparchies does not. The list is what is published as
the list, and the row follows it.

EPARCHIES ABROAD ARE NOT HERE, and it is a gap rather than a judgement. The
Patriarchate's list of eparchies holds only the eparchies in Georgia; its
Synod page names hierarchs of Western Europe, of Belgium and Holland and of
North America besides, which is enough to know those sees exist and not
enough to say where they sit. A row needs a country, and no official page
read here gives one for them. The address the old patriarchate.ge published
for the eparchy abroad is gone with that site, and the Western European
eparchy's own domain no longer answers. They are deferred for a seat, on the
same terms as the Georgian body in North America that docs/DIRECTORY.md
already defers.

ONE EPARCHY HAS A SITE OF ITS OWN that answered here, Kutaisi and Gaenati,
and it carries the link. The addresses orthodoxy.ge lists for diocesan sites
are of 2019 and most of the domains are gone: Batumi, Khoni, Ruisi and
Urbnisi, Poti and the Western European eparchy all fail to resolve, and the
one at shemoqmedi.ge answers with an empty page. None of them is published.
"""

READ = "2026-09-14"

GE = "https://patriarchate.ge/"
ORTH = "https://www.orthodoxy.ge/tsnobarebi/eparqiebi.htm"

ROWS = [
 dict(id="ge-mtskheta-tbilisi", parent="georgia",
      name="Eparchy of Mtskheta-Tbilisi",
      local=u"მცხეთა-თბილისის ეპარქია",
      seat="Mtskheta", country="GE",
      sources=[GE, ORTH]),

 dict(id="ge-bichvinta", parent="georgia",
      name="Eparchy of Bichvinta and Tskhum-Abkhazia",
      local=u"ბიჭვინთისა და ცხუმ-აფხაზეთის ეპარქია",
      seat="Sokhumi", country="GE",
      sources=[GE, ORTH]),

 dict(id="ge-kutaisi", parent="georgia",
      name="Eparchy of Kutaisi and Gaenati",
      local=u"ქუთაისისა და გაენათის ეპარქია",
      seat="Kutaisi", country="GE",
      site="https://kutais-gaenati.ge/",
      sources=["https://kutais-gaenati.ge/", GE, ORTH]),

 dict(id="ge-chiatura", parent="georgia",
      name="Eparchy of Chiatura and Sachkhere",
      local=u"ჭიათურისა და საჩხერის ეპარქია",
      seat="Chiatura", country="GE",
      sources=[GE, ORTH]),

 dict(id="ge-manglisi", parent="georgia",
      name="Eparchy of Manglisi and Tetritsqaro",
      local=u"მანგლისისა და თეთრიწყაროს ეპარქია",
      seat="Manglisi", country="GE",
      sources=[GE, ORTH]),

 dict(id="ge-tsilkani", parent="georgia",
      name="Eparchy of Tsilkani and Dusheti",
      local=u"წილკნისა და დუშეთის ეპარქია",
      seat="Tsilkani", country="GE",
      sources=[GE, ORTH]),

 dict(id="ge-tqibuli", parent="georgia",
      name="Eparchy of Tqibuli and Terjola",
      local=u"ტყიბულისა და თერჯოლის ეპარქია",
      seat="Terjola", country="GE",
      sources=[GE, ORTH]),

 dict(id="ge-ruisi", parent="georgia",
      name="Eparchy of Ruisi and Urbnisi",
      local=u"რუისისა და ურბნისის ეპარქია",
      seat="Kareli", country="GE",
      sources=[GE, ORTH]),

 dict(id="ge-alaverdi", parent="georgia",
      name="Eparchy of Alaverdi",
      local=u"ალავერდის ეპარქია",
      seat="Alaverdi", country="GE",
      sources=[GE, ORTH]),

 dict(id="ge-nekresi", parent="georgia",
      name="Eparchy of Nekresi",
      local=u"ნეკრესის ეპარქია",
      seat="Kvareli", country="GE",
      sources=[GE, ORTH]),

 dict(id="ge-shemokmedi", parent="georgia",
      name="Eparchy of Shemokmedi",
      local=u"შემოქმედის ეპარქია",
      seat="Ozurgeti", country="GE",
      sources=[GE, ORTH]),

 dict(id="ge-nikozi", parent="georgia",
      name="Eparchy of Nikozi and Tskhinvali",
      local=u"ნიქოზისა და ცხინვალის ეპარქია",
      seat="Nikozi", country="GE",
      sources=[GE, ORTH]),

 dict(id="ge-borjomi", parent="georgia",
      name="Eparchy of Borjomi and Bakuriani",
      local=u"ბორჯომისა და ბაკურიანის ეპარქია",
      seat="Borjomi", country="GE",
      sources=[GE, ORTH]),

 dict(id="ge-poti", parent="georgia",
      name="Eparchy of Poti and Khobi",
      local=u"ფოთისა და ხობის ეპარქია",
      seat="Poti", country="GE",
      sources=[GE, ORTH]),

 dict(id="ge-akhalkalaki", parent="georgia",
      name="Eparchy of Akhalkalaki and Kumurdo",
      local=u"ახალქალაქისა და კუმურდოს ეპარქია",
      seat="Akhalkalaki", country="GE",
      sources=[GE, ORTH]),

 dict(id="ge-akhaltsikhe", parent="georgia",
      name="Eparchy of Akhaltsikhe and Tao-Klarjeti",
      local=u"ახალციხისა და ტაო-კლარჯეთის ეპარქია",
      seat="Akhaltsikhe", country="GE",
      sources=[GE, ORTH]),

 dict(id="ge-khoni", parent="georgia",
      name="Eparchy of Khoni and Samtredia",
      local=u"ხონისა და სამტრედიის ეპარქია",
      seat="Khoni", country="GE",
      sources=[GE, ORTH]),

 dict(id="ge-batumi", parent="georgia",
      name="Eparchy of Batumi and Lazeti",
      local=u"ბათუმისა და ლაზეთის ეპარქია",
      seat="Batumi", country="GE",
      sources=[GE, ORTH]),

 dict(id="ge-vani", parent="georgia",
      name="Eparchy of Vani and Baghdati",
      local=u"ვანისა და ბაღდათის ეპარქია",
      seat="Vani", country="GE",
      sources=[GE, ORTH]),

 dict(id="ge-zugdidi", parent="georgia",
      name="Eparchy of Zugdidi and Tsaishi",
      local=u"ზუგდიდისა და ცაიშის ეპარქია",
      seat="Zugdidi", country="GE",
      sources=[GE, ORTH]),

 dict(id="ge-gori", parent="georgia",
      name="Eparchy of Gori and Ateni",
      local=u"გორისა და ატენის ეპარქია",
      seat="Gori", country="GE",
      sources=[GE, ORTH]),

 dict(id="ge-chqondidi", parent="georgia",
      name="Eparchy of Chqondidi",
      local=u"ჭყონდიდის ეპარქია",
      seat="Martvili", country="GE",
      sources=[GE, ORTH]),

 dict(id="ge-tsageri", parent="georgia",
      name="Eparchy of Tsageri and Lentekhi",
      local=u"ცაგერისა და ლენტეხის ეპარქია",
      seat="Tsageri", country="GE",
      sources=[GE, ORTH]),

 dict(id="ge-mestia", parent="georgia",
      name="Eparchy of Mestia and Upper Svaneti",
      local=u"მესტიისა და ზემო სვანეთის ეპარქია",
      seat="Mestia", country="GE",
      sources=[GE, ORTH]),

 dict(id="ge-senaki", parent="georgia",
      name="Eparchy of Senaki and Chkhorotsqu",
      local=u"სენაკისა და ჩხოროწყუს ეპარქია",
      seat="Senaki", country="GE",
      sources=[GE, ORTH]),

 dict(id="ge-rustavi", parent="georgia",
      name="Eparchy of Rustavi",
      local=u"რუსთავის ეპარქია",
      seat="Rustavi", country="GE",
      sources=[GE, ORTH]),

 dict(id="ge-gurjaani", parent="georgia",
      name="Eparchy of Gurjaani and Velistsikhe",
      local=u"გურჯაანისა და ველისციხის ეპარქია",
      seat="Gurjaani", country="GE",
      sources=[GE, ORTH]),

 dict(id="ge-sagarejo", parent="georgia",
      name="Eparchy of Sagarejo and Ninotsminda",
      local=u"საგარეჯოსა და ნინოწმიდის ეპარქია",
      seat="Ninotsminda", country="GE",
      sources=[GE, ORTH]),

 dict(id="ge-dmanisi", parent="georgia",
      name="Eparchy of Dmanisi and Agarak-Tashiri",
      local=u"დმანისისა და აგარაკ-ტაშირის ეპარქია",
      seat="Dmanisi", country="GE",
      sources=[GE, ORTH]),

 dict(id="ge-stepantsminda", parent="georgia",
      name="Eparchy of Stepantsminda and Khevi",
      local=u"სტეფანწმინდისა და ხევის ეპარქია",
      seat="Kazbegi", country="GE",
      sources=[GE, ORTH]),

 dict(id="ge-skhalta", parent="georgia",
      name="Eparchy of Skhalta",
      local=u"სხალთის ეპარქია",
      seat="Skhalta", country="GE",
      sources=[GE, ORTH]),

 dict(id="ge-bolnisi", parent="georgia",
      name="Eparchy of Bolnisi",
      local=u"ბოლნისის ეპარქია",
      seat="Bolnisi", country="GE",
      sources=[GE, ORTH]),

 dict(id="ge-margveti", parent="georgia",
      name="Eparchy of Margveti and Ubisi",
      local=u"მარგვეთისა და უბისის ეპარქია",
      seat="Zestaponi", country="GE",
      sources=[GE, ORTH]),

 dict(id="ge-bodbe", parent="georgia",
      name="Eparchy of Bodbe",
      local=u"ბოდბის ეპარქია",
      seat="Bodbe", country="GE",
      sources=[GE, ORTH]),

 dict(id="ge-tianeti", parent="georgia",
      name="Eparchy of Tianeti and Pshav-Khevsureti",
      local=u"თიანეთისა და ფშავ-ხევსურეთის ეპარქია",
      seat="Tianeti", country="GE",
      sources=[GE, ORTH]),

 dict(id="ge-khornabuji", parent="georgia",
      name="Eparchy of Khornabuji and Hereti",
      local=u"ხორნაბუჯისა და ჰერეთის ეპარქია",
      seat="Dedoplistsqaro", country="GE",
      sources=[GE, ORTH]),

 dict(id="ge-samtavisi", parent="georgia",
      name="Eparchy of Samtavisi and Kaspi",
      local=u"სამთავისისა და კასპის ეპარქია",
      seat="Samtavisi", country="GE",
      sources=[GE, ORTH]),

 dict(id="ge-surami", parent="georgia",
      name="Eparchy of Surami and Khashuri",
      local=u"სურამისა და ხაშურის ეპარქია",
      seat="Surami", country="GE",
      sources=[GE, ORTH]),

 dict(id="ge-marneuli", parent="georgia",
      name="Eparchy of Marneuli and Hujabi",
      local=u"მარნეულისა და ჰუჯაბის ეპარქია",
      seat="Marneuli", country="GE",
      sources=[GE, ORTH]),

 dict(id="ge-martqopi", parent="georgia",
      name="Eparchy of Martqopi and Gardabani",
      local=u"მარტყოფისა და გარდაბნის ეპარქია",
      seat="Gardabani", country="GE",
      sources=[GE, ORTH]),

 dict(id="ge-tsalka", parent="georgia",
      name="Eparchy of Tsalka",
      local=u"წალკის ეპარქია",
      seat="Tsalka", country="GE",
      sources=[GE, ORTH]),

 dict(id="ge-nikortsminda", parent="georgia",
      name="Eparchy of Nikortsminda",
      local=u"ნიკორწმინდის ეპარქია",
      seat="Ambrolauri", country="GE",
      sources=[GE, ORTH]),

]
