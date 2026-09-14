# -*- coding: utf-8 -*-
"""The dioceses of the Orthodox Church in America.

Audited on 14 September 2026 and found complete at fourteen. The rows are
older than this file: they were read on 13 September 2026 from the Church's
own directory of its dioceses, and each address off that diocese's own site,
and they carry that date because that is when each of them was read. They
have been moved here, unchanged, out of tools/directory.py, where they had
stood since before the dioceses were divided a file to a Church.

THE COUNT IS FOURTEEN AND IT IS THE CHURCH'S OWN LIST THAT SAYS SO. Its
directory at

    https://www.oca.org/dioceses

names fourteen and no more: Sitka and Alaska, the Albanian Archdiocese, the
Bulgarian Diocese, the Archdiocese of Canada, Eastern Pennsylvania, Mexico,
the Midwest, New England, New York and New Jersey, the Romanian Episcopate,
the South, Washington, the West, and Western Pennsylvania. Every one of the
fourteen was checked off against the rows here on 14 September 2026 and none
is missing and none is over.

THE STATUTE NAMES NO NUMBER, WHICH IS WHY THE LIST HAS TO DO IT. It was read
because a list of links is the weaker of the two sources, and this Church's
own law turns out to say nothing that would override it. Article I says only
that the Church has territorial jurisdiction in the United States and Canada
and exercises jurisdiction over its diocese in Mexico; Article VII defines a
diocese, leaves it to the Holy Synod to erect, merge and suppress them, and
provides for dioceses "not defined by a specific geographical area, but
rather composed of Parishes and institutions that are characterized by a
particular identity" - which is what the Albanian, Bulgarian and Romanian
bodies here are, and is why they are dioceses on this page rather than a
category of their own. No article numbers them.

THERE IS NOTHING BETWEEN THIS CHURCH AND ITS DIOCESES. The only subdivision
the Statute knows is beneath a diocese, not above it: "The Diocese may be
divided into Deaneries, each headed by a District Dean." No metropolitan
district, no exarchate, no province. So all fourteen hang off the Church
itself, and a later pass need not go looking for a middle rank.

Deaneries are not rows. They are an arrangement of parishes under a bishop
who already has a row, and parishes are a later pass on this site.

READ AGAIN ON 14 SEPTEMBER 2026, FROM EACH DIOCESE'S OWN DOOR. Every row here
cited one page - the Church's list of its dioceses - and a reader who could
not reach oca.org had nowhere else to go. Thirteen of the fourteen diocesan
sites answered and each names itself on its own front page, so each row now
cites its own as well as its Church's. Sitka and Alaska is the exception:
odosa.org refuses the request from here with a 403, so that row keeps its one
citation and its old reading date, because it was not re-read.

WHAT THE FOURTEEN CALL THEMSELVES, AND THE LANGUAGE THEY CALL IT IN. Eleven
of them publish their own name in English and in nothing else, and that is not
a gap: English is this Church's own language, and a Slavonic or Romanian form
invented for the row here would be this site putting words in a body's mouth.
Two publish a name in another language and those two carry it - Mexico, which
writes Diocesis de Mexico de la Iglesia Ortodoxa en America, and the Albanian
Archdiocese, which prints its name in Albanian on its own front page.

Five of the thirteen style themselves on their own sites in terms the Church's
list does not use - Philadelphia and Eastern Pennsylvania, Pittsburgh and
Western Pennsylvania, the Archdiocese of Washington, the Albanian Orthodox
Archdiocese in America, and the Bulgarian Diocese of Toledo. The list's name
stays as the row's name, because that is what the Church calls it, and the
body's own designation goes in `styled` beside it.

RANK IS THE WORD THE CHURCH'S OWN LIST USES. Its directory prints Diocese,
Archdiocese and Episcopate, and those three are what the rows carry. Nothing
here is guessed from a name: the Statute knows one thing beneath the Church,
a Diocese, and the list is where the other two words are actually written.

"""

READ = "2026-09-14"

OCA_DIOC = "https://www.oca.org/dioceses"

ROWS = [
 # Sitka and Alaska was not re-read: odosa.org answers a 403 from here. The
 # row keeps the one citation it had and the date it was read on.
 dict(id="oca-alaska", parent="oca", name="Diocese of Sitka and Alaska",
      rank="Diocese", checked="2026-09-13",
      seat="Anchorage, Alaska", country="US",
      address=["430 C Street Ste 301", "Anchorage, AK 99501"],
      site="https://odosa.org/", source=OCA_DIOC),
 dict(id="oca-albanian", parent="oca", name="Albanian Archdiocese",
      styled="Albanian Orthodox Archdiocese in America",
      local=u"Kryepeshkopata Orthodhokse Shqiptare n\u00eb Amerik\u00ebs",
      rank="Archdiocese",
      seat="Boston, Massachusetts", country="US",
      address=["517 East Broadway", "South Boston, MA 02127-4415"],
      site="https://albanianarchdiocese.org/",
      sources=[OCA_DIOC, "https://albanianarchdiocese.org/"]),
 dict(id="oca-bulgarian", parent="oca", name="Bulgarian Diocese",
      styled="Bulgarian Diocese of Toledo", rank="Diocese",
      seat="Toledo, Ohio", country="US",
      address=["519 Brynhaven Dr", "Oregon, OH 43616-2809"],
      site="https://www.bdoca.org/",
      sources=[OCA_DIOC, "https://www.bdoca.org/"]),
 dict(id="oca-canada", parent="oca", name="Archdiocese of Canada",
      rank="Archdiocese",
      seat="Rawdon, Quebec", country="CA",
      address=["3441 15th Ave", "Rawdon, QC J0K 1S0"],
      site="https://www.archdiocese.ca/",
      sources=[OCA_DIOC, "https://www.archdiocese.ca/"]),
 dict(id="oca-eastern-pa", parent="oca", name="Diocese of Eastern Pennsylvania",
      styled="Diocese of Philadelphia and Eastern Pennsylvania",
      rank="Diocese",
      seat="Bath, Pennsylvania", country="US",
      address=["325 N Walnut St", "Bath, PA 18014"],
      site="https://doepa.org/",
      sources=[OCA_DIOC, "https://doepa.org/"]),
 dict(id="oca-mexico", parent="oca", name="Diocese of Mexico",
      local=u"Di\u00f3cesis de M\u00e9xico de la Iglesia Ortodoxa en Am\u00e9rica",
      rank="Diocese",
      seat="Mexico City", country="MX",
      address=["Calle Irapuato 53", "Penon de los Banos, Venustiano Carranza", "C.P. 15520, CDMX"],
      site="https://ocamexico.org/",
      sources=[OCA_DIOC, "https://ocamexico.org/"]),
 dict(id="oca-new-england", parent="oca", name="Diocese of New England",
      rank="Diocese",
      seat="Windsor, Connecticut", country="US",
      address=["9 River Bend Ln", "Windsor, CT 06095-1617"],
      site="https://www.dneoca.org/",
      sources=[OCA_DIOC, "https://www.dneoca.org/"]),
 dict(id="oca-ny-nj", parent="oca", name="Diocese of New York and New Jersey",
      rank="Diocese",
      seat="Bronxville, New York", country="US",
      address=["33 Hewitt Avenue", "Bronxville, NY 10708-2333"],
      site="https://www.nynjoca.org/",
      sources=[OCA_DIOC, "https://www.nynjoca.org/"]),
 dict(id="oca-midwest", parent="oca", name="Diocese of the Midwest",
      rank="Diocese",
      seat="Chicago, Illinois", country="US",
      address=["917 North Wood Street", "Chicago, IL 60622"],
      site="https://domoca.org/",
      sources=[OCA_DIOC, "https://domoca.org/"]),
 dict(id="oca-south", parent="oca", name="Diocese of the South",
      rank="Diocese",
      seat="Dallas, Texas", country="US",
      address=["4222 Wycliff Ave", "Dallas, TX 75219"],
      site="https://dosoca.org/",
      sources=[OCA_DIOC, "https://dosoca.org/"]),
 dict(id="oca-west", parent="oca", name="Diocese of the West",
      rank="Diocese",
      seat="San Francisco, California", country="US",
      address=["1520 Green St", "San Francisco, CA 94123-5102"],
      site="https://dowoca.org/",
      sources=[OCA_DIOC, "https://dowoca.org/"]),
 dict(id="oca-washington", parent="oca", name="Archdiocese of Washington, D.C.",
      styled="Archdiocese of Washington", rank="Archdiocese",
      seat="Alexandria, Virginia", country="US",
      address=["PO Box 31409", "Alexandria, VA 22310"],
      site="https://wdcoca.org/",
      sources=[OCA_DIOC, "https://wdcoca.org/"]),
 dict(id="oca-western-pa", parent="oca", name="Archdiocese of Western Pennsylvania",
      styled="Archdiocese of Pittsburgh and Western Pennsylvania",
      rank="Archdiocese",
      seat="Cranberry Township, Pennsylvania", country="US",
      address=["8641 Peters Rd", "Cranberry Township, PA 16066-3825"],
      site="https://www.ocadwpa.org/",
      sources=[OCA_DIOC, "https://www.ocadwpa.org/"]),
 dict(id="oca-romanian", parent="oca", name="Romanian Episcopate",
      styled="The Romanian Orthodox Episcopate of America",
      rank="Episcopate",
      founded="Established as a Diocese at a general Church Congress held in "
              "the city of Detroit, Michigan, on April 25-28, 1929.",
      seat="Jackson, Michigan", country="US",
      address=["2535 Grey Tower Rd", "Jackson, MI 49201"],
      site="https://roea.org/",
      sources=[OCA_DIOC, "https://roea.org/", "https://roea.org/about-roea/"]),
]
