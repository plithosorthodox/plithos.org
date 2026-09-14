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
"""

OCA_DIOC = "https://www.oca.org/dioceses"

ROWS = [
 dict(id="oca-alaska", parent="oca", name="Diocese of Sitka and Alaska",
      seat="Anchorage, Alaska", country="US",
      address=["430 C Street Ste 301", "Anchorage, AK 99501"],
      site="https://odosa.org/", source=OCA_DIOC),
 dict(id="oca-albanian", parent="oca", name="Albanian Archdiocese",
      seat="Boston, Massachusetts", country="US",
      address=["517 East Broadway", "South Boston, MA 02127-4415"],
      site="https://albanianarchdiocese.org/", source=OCA_DIOC),
 dict(id="oca-bulgarian", parent="oca", name="Bulgarian Diocese",
      seat="Toledo, Ohio", country="US",
      address=["519 Brynhaven Dr", "Oregon, OH 43616-2809"],
      site="https://www.bdoca.org/", source=OCA_DIOC),
 dict(id="oca-canada", parent="oca", name="Archdiocese of Canada",
      seat="Rawdon, Quebec", country="CA",
      address=["3441 15th Ave", "Rawdon, QC J0K 1S0"],
      site="https://www.archdiocese.ca/", source=OCA_DIOC),
 dict(id="oca-eastern-pa", parent="oca", name="Diocese of Eastern Pennsylvania",
      seat="Bath, Pennsylvania", country="US",
      address=["325 N Walnut St", "Bath, PA 18014"],
      site="https://doepa.org/", source=OCA_DIOC),
 dict(id="oca-mexico", parent="oca", name="Diocese of Mexico",
      seat="Mexico City", country="MX",
      address=["Calle Irapuato 53", "Penon de los Banos, Venustiano Carranza", "C.P. 15520, CDMX"],
      site="https://ocamexico.org/", source=OCA_DIOC),
 dict(id="oca-new-england", parent="oca", name="Diocese of New England",
      seat="Windsor, Connecticut", country="US",
      address=["9 River Bend Ln", "Windsor, CT 06095-1617"],
      site="https://www.dneoca.org/", source=OCA_DIOC),
 dict(id="oca-ny-nj", parent="oca", name="Diocese of New York and New Jersey",
      seat="Bronxville, New York", country="US",
      address=["33 Hewitt Avenue", "Bronxville, NY 10708-2333"],
      site="https://www.nynjoca.org/", source=OCA_DIOC),
 dict(id="oca-midwest", parent="oca", name="Diocese of the Midwest",
      seat="Chicago, Illinois", country="US",
      address=["917 North Wood Street", "Chicago, IL 60622"],
      site="https://domoca.org/", source=OCA_DIOC),
 dict(id="oca-south", parent="oca", name="Diocese of the South",
      seat="Dallas, Texas", country="US",
      address=["4222 Wycliff Ave", "Dallas, TX 75219"],
      site="https://dosoca.org/", source=OCA_DIOC),
 dict(id="oca-west", parent="oca", name="Diocese of the West",
      seat="San Francisco, California", country="US",
      address=["1520 Green St", "San Francisco, CA 94123-5102"],
      site="https://dowoca.org/", source=OCA_DIOC),
 dict(id="oca-washington", parent="oca", name="Archdiocese of Washington, D.C.",
      seat="Alexandria, Virginia", country="US",
      address=["PO Box 31409", "Alexandria, VA 22310"],
      site="https://wdcoca.org/", source=OCA_DIOC),
 dict(id="oca-western-pa", parent="oca", name="Archdiocese of Western Pennsylvania",
      seat="Cranberry Township, Pennsylvania", country="US",
      address=["8641 Peters Rd", "Cranberry Township, PA 16066-3825"],
      site="https://www.ocadwpa.org/", source=OCA_DIOC),
 dict(id="oca-romanian", parent="oca", name="Romanian Episcopate",
      seat="Jackson, Michigan", country="US",
      address=["2535 Grey Tower Rd", "Jackson, MI 49201"],
      site="https://roea.org/", source=OCA_DIOC),
]
