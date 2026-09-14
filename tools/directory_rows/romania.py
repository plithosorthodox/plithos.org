# -*- coding: utf-8 -*-
"""The eparchies of the Romanian Patriarchate, under their metropolises.

The Patriarchate publishes its metropolises one to a page, and each page
carries the archdioceses and bishoprics that sit under it, with the address
of every chancery. The ten metropolitan sees were read first and are in
tools/directory.py; these are the thirty-three suffragans beside them, read
from the page of the metropolis each belongs to.

Each row cites that page in both of the Patriarchate's own editions,
because the two carry different halves of it: the English edition gives the
see's name in English, the Romanian gives the see's own name and the
address in the words an envelope wants. Targoviste is the exception -
neither edition prints a Romanian address for it - and its street is taken
as the see itself writes it.

COUNTED AGAIN ON 14 SEPTEMBER 2026 AND NOTHING IS MISSING. All ten metropolis
pages were opened one by one and the sees on each were counted: thirteen under
Muntenia and Dobrudja, four under Moldavia and Bucovina, five under
Transylvania, three under Cluj, Maramures and Salaj, four under Oltenia, three
under Banat, three under Bessarabia, five under Western and Southern Europe,
two under Germany, Central and Northern Europe, and two under the Americas.
Forty-four, which is what this directory holds. The Patriarchate states no
total in prose on any page read, so the count is the sum of its own ten lists
and a reader can repeat it.

The diaspora is the whole of what the Patriarchate lists abroad: Hungary,
Serbia, Australia and New Zealand under Muntenia; Great Britain and Northern
Ireland, Italy, Spain and Portugal, Ireland and Iceland beside the Archdiocese
of Western Europe; Northern Europe beside the Archdiocese of Germany, Austria
and Luxembourg; and the Diocese of Canada beside the Metropolia at Chicago.

TWO THINGS WERE LOOKED FOR AND ARE NOT THERE. The Metropolis of Bessarabia
lists three eparchies and not four: no see of Dubasari and all Transnistria
appears on the Patriarchate's page for it, in either edition, nor on the
Metropolis's own front page, and a body no list names gets no row. And the
Romanian edition of the page of eparchies calls the tenth archdiocese the
Romanian Orthodox Archdiocese of the United States of America where the
English calls it the Metropolia of the Americas; both print the one address at
Chicago, so it is one see under two headings and not a row this directory is
short of.
"""

MUNTENIA = ["https://patriarhia.ro/en/organization-of-the-romanian-orthodox"
            "-church/metropolises/metropolis-of-muntenia-and-dobrudja/",
            "https://patriarhia.ro/organizarea-bisericii-ortodoxe-romane/"
            "mitropolii/mitropolia-munteniei-si-dobrogei/"]
MOLDAVIA = ["https://patriarhia.ro/en/organization-of-the-romanian-orthodox"
            "-church/metropolises/metropolis-of-moldavia-and-bucovina/",
            "https://patriarhia.ro/organizarea-bisericii-ortodoxe-romane/"
            "mitropolii/mitropolia-moldovei-si-bucovinei/"]
TRANSYLVANIA = ["https://patriarhia.ro/en/organization-of-the-romanian-"
                "orthodox-church/metropolises/metropolis-of-transylvania/",
                "https://patriarhia.ro/organizarea-bisericii-ortodoxe-"
                "romane/mitropolii/mitropolia-ardealului/"]
CLUJ = ["https://patriarhia.ro/en/organization-of-the-romanian-orthodox-"
        "church/metropolises/metropolis-of-cluj-maramures-and-salaj/",
        "https://patriarhia.ro/organizarea-bisericii-ortodoxe-romane/"
        "mitropolii/mitropolia-clujului-maramuresului-si-salajului/"]
OLTENIA = ["https://patriarhia.ro/en/organization-of-the-romanian-orthodox"
           "-church/metropolises/metropolis-of-oltenia/",
           "https://patriarhia.ro/organizarea-bisericii-ortodoxe-romane/"
           "mitropolii/mitropolia-olteniei/"]
BANAT = ["https://patriarhia.ro/en/organization-of-the-romanian-orthodox-"
         "church/metropolises/metropolis-of-banat/",
         "https://patriarhia.ro/organizarea-bisericii-ortodoxe-romane/"
         "mitropolii/mitropolia-banatului/"]
BESSARABIA = ["https://patriarhia.ro/en/organization-of-the-romanian-"
              "orthodox-church/metropolises/autonomous-of-old-calendar-"
              "metropolis-of-bessarabia-and-exarchate-of-lands/",
              "https://patriarhia.ro/organizarea-bisericii-ortodoxe-romane/"
              "mitropolii/mitropolia-basarabiei-autonoma-si-de-stil-vechi-"
              "si-exarhat-al-plaiurilor/"]
WESTERN_EUROPE = ["https://patriarhia.ro/en/organization-of-the-romanian-"
                  "orthodox-church/metropolises/romanian-orthodox-"
                  "metropolis-of-western-and-southern-europe/",
                  "https://patriarhia.ro/organizarea-bisericii-ortodoxe-"
                  "romane/mitropolii/mitropolia-ortodoxa-romana-a-europei-"
                  "occidentale-si-meridionale/"]
GERMANY = ["https://patriarhia.ro/en/organization-of-the-romanian-orthodox"
           "-church/metropolises/romanian-orthodox-metropolis-of-germany-"
           "central-and-northern-europe/",
           "https://patriarhia.ro/organizarea-bisericii-ortodoxe-romane/"
           "mitropolii/mitropolia-ortodoxa-romana-a-germaniei-europei-"
           "centrale-si-de-nord/"]
AMERICAS = ["https://patriarhia.ro/en/organization-of-the-romanian-orthodox"
            "-church/metropolises/romanian-orthodox-metropolia-of-the-"
            "americas/",
            "https://patriarhia.ro/organizarea-bisericii-ortodoxe-romane/"
            "mitropolii/mitropolia-ortodoxa-romana-a-celor-doua-americi/"]

ROWS = [
 # Metropolis of Muntenia and Dobrudja. Bucharest and Tomis are already in
 # tools/directory.py; these are the rest of the list that page carries.
 dict(id="ro-targoviste", parent="romania",
      name="Archdiocese of Targoviste",
      local="Arhiepiscopia Targoviste",
      seat="Targoviste", country="RO",
      address=["Strada Mihai Bravu 11", "RO-130004 Targoviste, Dambovita"],
      site="https://arhiepiscopiatargovistei.ro/",
      sources=MUNTENIA + ["https://arhiepiscopiatargovistei.ro/"]),
 dict(id="ro-arges", parent="romania",
      name="Archdiocese of Arges and Muscel",
      local="Arhiepiscopia Argesului si Muscelului",
      seat="Curtea de Arges", country="RO",
      address=["Strada Basarabilor 23",
               "RO-115300 Curtea de Arges, Arges"],
      site="https://arhiepiscopiaargesuluisimuscelului.ro/",
      sources=MUNTENIA),
 # The Buzau chancery refused the request from here - a 403, not a silence -
 # so the row gives the Patriarchate rather than a link that may not open.
 dict(id="ro-buzau", parent="romania",
      name="Archdiocese of Buzau and Vrancea",
      local="Arhiepiscopia Buzaului si Vrancei",
      seat="Buzau", country="RO",
      address=["Aleea Episcopiei 3", "RO-120024 Buzau, Buzau"],
      sources=MUNTENIA),
 dict(id="ro-lower-danube", parent="romania",
      name="Archdiocese of Lower Danube",
      local="Arhiepiscopia Dunarii de Jos",
      seat="Galati", country="RO",
      address=["Strada Domneasca 104", "RO-800201 Galati, Galati"],
      site="https://www.edj.ro/", sources=MUNTENIA),
 dict(id="ro-slobozia", parent="romania",
      name="Diocese of Slobozia and Calarasi",
      local="Episcopia Sloboziei si Calarasilor",
      seat="Slobozia", country="RO",
      address=["Strada Episcopiei 2", "RO-920023 Slobozia, Ialomita"],
      site="https://sf-esc.ro/", sources=MUNTENIA),
 dict(id="ro-alexandria-teleorman", parent="romania",
      name="Diocese of Alexandria and Teleorman",
      local="Episcopia Alexandriei si Teleormanului",
      seat="Alexandria, Teleorman", country="RO",
      address=["Strada Carpati 11-15", "RO-140059 Alexandria, Teleorman"],
      site="https://episcopiaalexandriei.ro/", sources=MUNTENIA),
 dict(id="ro-giurgiu", parent="romania",
      name="Diocese of Giurgiu",
      local="Episcopia Giurgiului",
      seat="Giurgiu", country="RO",
      address=["Strada Episcopiei 13", "RO-080015 Giurgiu, Giurgiu"],
      site="https://episcopiagiurgiului.ro/", sources=MUNTENIA),
 dict(id="ro-tulcea", parent="romania",
      name="Diocese of Tulcea",
      local="Episcopia Tulcii",
      seat="Tulcea", country="RO",
      address=["Strada Mircea Voda 6A", "RO-820134 Tulcea, Tulcea"],
      site="https://www.episcopiatulcii.ro/", sources=MUNTENIA),
 dict(id="ro-dacia-felix", parent="romania",
      name="Diocese of Dacia Felix",
      local="Episcopia Daciei Felix",
      seat="Vrsac", country="RS",
      address=["Zarka Zrenjanina 60", "26300 Vrsac"],
      site="https://episcopiadaciafelix.ro/", sources=MUNTENIA),
 dict(id="ro-hungary", parent="romania",
      name="Romanian Orthodox Diocese of Hungary",
      local="Episcopia Ortodoxa Romana a Ungariei",
      seat="Gyula", country="HU",
      address=["Szent Miklos Park 2", "H-5700 Gyula"],
      # ortodoxia.hu, which the Patriarchate prints, has left the diocese's
      # hands and now redirects elsewhere; the row gives no link of its own.
      sources=MUNTENIA),
 dict(id="ro-australia-nz", parent="romania",
      name="Romanian Orthodox Diocese of Australia and New Zealand",
      local="Episcopia Ortodoxa Romana a Australiei si Noii Zeelande",
      seat="Melton West, Victoria", country="AU",
      address=["103 Porteous Road", "Harkness (Melton West) 3337, Victoria"],
      site="https://www.roeanz.com.au/", sources=MUNTENIA),

 # Metropolis of Moldavia and Bucovina. Jassy is already in directory.py.
 dict(id="ro-suceava", parent="romania",
      name="Archdiocese of Suceava and Radauti",
      local="Arhiepiscopia Sucevei si Radautilor",
      seat="Suceava", country="RO",
      address=["Strada Iancu Flondor 2", "RO-720027 Suceava, Suceava"],
      site="https://www.arhiepiscopiasucevei.ro/", sources=MOLDAVIA),
 dict(id="ro-roman", parent="romania",
      name="Archdiocese of Roman and Bacau",
      local="Arhiepiscopia Romanului si Bacaului",
      seat="Roman", country="RO",
      address=["Strada Alexandru cel Bun 5", "RO-611065 Roman, Neamt"],
      site="https://eprb.ro/", sources=MOLDAVIA),
 dict(id="ro-husi", parent="romania",
      name="Diocese of Husi",
      local="Episcopia Husilor",
      seat="Husi", country="RO",
      address=["Strada Stefan cel Mare 1", "RO-735100 Husi, Vaslui"],
      site="https://episcopiahusilor.ro/", sources=MOLDAVIA),

 # Metropolis of Transylvania. Sibiu is already in directory.py.
 dict(id="ro-alba-iulia", parent="romania",
      name="Archdiocese of Alba Iulia",
      local="Arhiepiscopia Alba Iuliei",
      seat="Alba Iulia", country="RO",
      address=["Strada Mihai Viteazul 16", "RO-510010 Alba Iulia, Alba"],
      site="https://reintregirea.ro/", sources=TRANSYLVANIA),
 dict(id="ro-oradea", parent="romania",
      name="Romanian Orthodox Diocese of Oradea",
      local="Episcopia Ortodoxa Romana a Oradiei",
      seat="Oradea", country="RO",
      address=["Strada Episcop Roman Ciorogariu 3",
               "RO-410017 Oradea, Bihor"],
      site="https://www.eparhiaortodoxaoradea.ro/", sources=TRANSYLVANIA),
 dict(id="ro-covasna", parent="romania",
      name="Diocese of Covasna and Harghita",
      local="Episcopia Covasnei si Harghitei",
      seat="Miercurea-Ciuc", country="RO",
      address=["Strada Miron Cristea 5",
               "RO-530112 Miercurea-Ciuc, Harghita"],
      site="https://episcopiacvhr.ro/", sources=TRANSYLVANIA),
 dict(id="ro-deva", parent="romania",
      name="Diocese of Deva and Hunedoara",
      local="Episcopia Devei si Hunedoarei",
      seat="Deva", country="RO",
      address=["Strada Andrei Saguna 1", "RO-330026 Deva, Hunedoara"],
      site="https://episcopiadevei.ro/", sources=TRANSYLVANIA),

 # Metropolis of Cluj, Maramures and Salaj. Vad, Feleac and Cluj is already
 # in directory.py.
 dict(id="ro-maramures", parent="romania",
      name="Romanian Orthodox Diocese of Maramures and Satmar",
      local="Episcopia Ortodoxa Romana a Maramuresului si Satmarului",
      seat="Baia Mare", country="RO",
      address=["Strada Avram Iancu 5", "RO-430313 Baia Mare, Maramures"],
      site="https://episcopiammsm.ro/", sources=CLUJ),
 dict(id="ro-salaj", parent="romania",
      name="Diocese of Salaj",
      local="Episcopia Salajului",
      seat="Zalau", country="RO",
      address=["Strada Episcopiei 18", "RO-450145 Zalau, Salaj"],
      site="https://episcopiasalajului.ro/", sources=CLUJ),

 # Metropolis of Oltenia. Craiova is already in directory.py.
 dict(id="ro-ramnic", parent="romania",
      name="Archdiocese of Ramnic",
      local="Arhiepiscopia Ramnicului",
      seat="Ramnicu Valcea", country="RO",
      address=["Strada Arhiepiscopiei 1",
               "RO-240178 Ramnicu-Valcea, Valcea"],
      site="https://arhiepiscopiaramnicului.ro/", sources=OLTENIA),
 dict(id="ro-severin", parent="romania",
      name="Diocese of Severin and Strehaia",
      local="Episcopia Severinului si Strehaiei",
      seat="Drobeta-Turnu Severin", country="RO",
      address=["Strada I.Gh. Bibicescu 6",
               "RO-220103 Drobeta-Turnu Severin, Mehedinti"],
      site="https://www.episcopiaseverinului.ro/", sources=OLTENIA),
 dict(id="ro-slatina", parent="romania",
      name="Diocese of Slatina and Romanati",
      local="Episcopia Slatinei si Romanatilor",
      seat="Slatina", country="RO",
      address=["Strada Fratii Buzesti 15", "RO-230080 Slatina, Olt"],
      site="https://www.episcopiaslatinei.ro/", sources=OLTENIA),

 # Metropolis of Banat. Timisoara is already in directory.py.
 dict(id="ro-arad", parent="romania",
      name="Archdiocese of Arad",
      local="Arhiepiscopia Aradului",
      seat="Arad", country="RO",
      address=["Strada Episcopiei 60-62", "RO-310084 Arad, Arad"],
      site="https://www.arhiepiscopiaaradului.ro/", sources=BANAT),
 dict(id="ro-caransebes", parent="romania",
      name="Diocese of Caransebes",
      local="Episcopia Caransebesului",
      seat="Caransebes", country="RO",
      address=["Strada Nicolae Corneanu 5",
               "RO-325400 Caransebes, Caras-Severin"],
      site="https://www.episcopiacaransebesului.ro/", sources=BANAT),

 # The Metropolis of Bessarabia. Chisinau is already in directory.py. Both
 # of these sees carry the name they held before as the Patriarchate prints
 # it, and the row keeps it.
 dict(id="ro-balti", parent="romania",
      name="Diocese of Balti (formerly Hotin)",
      local="Episcopia de Balti (fosta a Hotinului)",
      seat="Balti", country="MD",
      address=["Strada Orhei 64", "Balti"],
      site="https://episcopia.md/", sources=BESSARABIA),
 dict(id="ro-south-bessarabia", parent="romania",
      name="Diocese of South Bessarabia (formerly of Cetatea Alba-Ismail)",
      local="Episcopia Basarabiei de Sud (fosta de Cetatea Alba-Ismail)",
      seat="Cahul", country="MD",
      address=["Str. Bogdan Petriceicu Hasdeu Nr. 11A",
               "Municipiul Cahul"],
      site="https://www.episcopiabasarabieidesud.md/", sources=BESSARABIA),

 # Romanian Orthodox Metropolis of Western and Southern Europe. The
 # Archdiocese of Western Europe is already in directory.py.
 dict(id="ro-great-britain", parent="romania",
      name="Romanian Orthodox Archdiocese of Great Britain and Northern Ireland",
      local="Arhiepiscopia Ortodoxa Romana a Marii Britanii si Irlandei de Nord",
      seat="Enfield", country="GB",
      address=["St Paul's Centre, 102A Church Street",
               "Enfield, EN2 6AR"],
      site="https://roarch.org.uk/", sources=WESTERN_EUROPE),
 dict(id="ro-italy", parent="romania",
      name="Romanian Orthodox Diocese of Italy",
      local="Episcopia Ortodoxa Romana a Italiei",
      seat="Rome", country="IT",
      address=["Via Ardeatina 1741", "00134 Roma"],
      site="https://www.episcopia-italiei.it/", sources=WESTERN_EUROPE),
 dict(id="ro-spain", parent="romania",
      name="Romanian Orthodox Diocese of Spain and Portugal",
      local="Episcopia Ortodoxa Romana a Spaniei si Portugaliei",
      seat="Madrid", country="ES",
      address=["Calle Trompetas 7", "28054 Madrid"],
      site="https://www.obispadoortodoxo.es/", sources=WESTERN_EUROPE),
 dict(id="ro-ireland-iceland", parent="romania",
      name="Romanian Orthodox Diocese of Ireland and Iceland",
      local="Episcopia Ortodoxa Romana a Irlandei si Islandei",
      seat="Dublin", country="IE",
      address=["Drimnagh Castle, Long Mile Road", "Dublin 12, D12RP3F"],
      site="https://www.eorii.com/", sources=WESTERN_EUROPE),

 # Romanian Orthodox Metropolis of Germany, Central and Northern Europe.
 # The metropolis itself is already in directory.py.
 dict(id="ro-northern-europe", parent="romania",
      name="Romanian Orthodox Diocese of Northern Europe",
      local="Episcopia Ortodoxa Romana a Europei de Nord",
      seat="Haninge", country="SE",
      address=["Hasslingbyvagen 7", "13691 Haninge - Stockholm"],
      site="https://episcopiascandinavia.se/", sources=GERMANY),

 # Romanian Orthodox Metropolia of the Americas. The Metropolia itself is
 # already in directory.py, as romanian-americas.
 dict(id="ro-canada", parent="romania",
      name="Romanian Orthodox Diocese of Canada",
      local="Episcopia Ortodoxa Romana a Canadei",
      seat="Saint-Hubert, Quebec", country="CA",
      address=["2010 Boulevard Marie",
               "Saint-Hubert (Quebec) J4T 2B1"],
      site="https://www.episcopia.ca/", sources=AMERICAS),
]
