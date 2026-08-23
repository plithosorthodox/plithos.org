# -*- coding: utf-8 -*-
"""Georgian for the vocabulary that stands beside the lives.

TEXT = {the phrase the index shows: the rendering}. The keys are the phrases
exactly as the index writes them, so a rendering cannot quietly attach itself
to the wrong saint.

A language may later declare PARTS and an expand() to assemble the compound
place-names from pieces rendered once, as the older languages do. It is an
optimisation and not a requirement: everything written in TEXT stands over
whatever expand() builds.
"""
TEXT = {
}

TEXT.update({
    "(Abibus) of Egypt": "(აბიბე) ეგვიპტელი",
    "(Apphianus) and Edesius (Aedesius) of Lycia": "(აპფიანე) და ედესი ლიკიელნი",
    "(Eustace) the Confessor, Bishop of Bithynia": "(ევსტათი) აღმსარებელი, ბითვინიის ეპისკოპოსი",
    "(Jacob) the Presbyter, and Azadanes and Abdiesus the Deacons, of Persia": "(იაკობ) ხუცესი და აზადანი და აბდიესი დიაკვნები, სპარსელნი",
    "(Vadim) of Persia": "(ვადიმ) სპარსელი",
    "(Voino-Yasenetsky), Archbishop of Simferopol and Crimea": "(ვოინო-იასენეცკი), სიმფეროპოლისა და ყირიმის მთავარეპისკოპოსი",
    "(also called Susanna), New Martyr of Lesbos": "(სუსანადაც წოდებული), ლესბოსელი ახალმოწამე",
    "(tonsured David and Euphrosyne), Wonderworkers of Murom": "(აღკვეცილნი დავითი და ევფროსინე), მურომის სასწაულმოქმედნი",
    "A Cappadocian centurion bowing beneath the sword with his eyes lifted in thanksgiving, the walnut tree of the tradition behind him, the churches of Byzantium rising over his relics.": "კაბადოკიელი ასისთავი, მახვილის ქვეშ დახრილი, თვალები მადლობით ზეაპყრობილი, გადმოცემის კაკლის ხე მის უკან, ბიზანტიის ეკლესიები მის ნაწილებზე აღმართული.",
    "A Celtic hermit of the Devon coast bearing his own severed head to the spring, the robbers behind him, crowned as a martyr among the saints of Britain.": "დევონის სანაპიროს კელტი განდეგილი, საკუთარი მოკვეთილი თავის მიმტანი წყაროსთან, ავაზაკები მის უკან, მოწამედ დაგვირგვინებული ბრიტანეთის წმინდანთა შორის.",
    "A Christian general casting down the temples of Galatia, his twelve tribunes and his thousands of soldiers with their wives and children crowned around him, the converted sorcerer Callinicus among them.": "ქრისტიანი მხედართმთავარი, გალატიის ტაძრების დამამხობელი, მისი თორმეტი ათასისთავი და ათასობით ჯარისკაცი ცოლ-შვილითურთ დაგვირგვინებულნი მის გარშემო, მოქცეული მოგვი კალინიკე მათ შორის.",
    "A Christian of Alexandria standing before the tribunal to denounce its cruelty, the confession volunteered and the sword received.": "ალექსანდრიელი ქრისტიანი, სამსჯავროს წინაშე მდგარი მისი სისასტიკის მხილებლად, ნებაყოფლობით აღსარებული და მახვილმიღებული.",
    "A Creole-Aleut priest in vestments holding a Gospel and a cross, against an Alaskan landscape.": "კრეოლ-ალეუტი მღვდელი შესამოსელში, სახარებითა და ჯვრით ხელში, ალასკის ხედის ფონზე.",
    "A Georgian bishop with a book and a restored church, schoolchildren and monasteries behind him.": "ქართველი ეპისკოპოსი წიგნითა და აღდგენილი ეკლესიით, მოწაფეები და მონასტრები მის უკან.",
    "A Georgian commander marking his forehead with the cross in his own blood, his soldiers crowned around him.": "ქართველი მხედართმთავარი, საკუთარი სისხლით შუბლზე ჯვრის მდებელი, მისი ჯარისკაცები დაგვირგვინებულნი მის გარშემო.",
    "A Georgian monk in prayer before the cave monastery of Gareji in the desert hills.": "ქართველი ბერი ლოცვად გარეჯის მღვიმური მონასტრის წინაშე უდაბნოს გორაკებში.",
    "A Georgian monk-abbot holding a scroll or a book.": "ქართველი მონაზონი-წინამძღვარი გრაგნილითა თუ წიგნით ხელში.",
    "A Georgian prince and commander refusing to trample the icon of Christ before the conqueror, crowned as a great-martyr, the defender of the Georgian faith.": "ქართველი მთავარი და მხედართმთავარი, დამპყრობლის წინაშე ქრისტეს ხატის გათელვაზე უარის მთქმელი, დიდმოწამედ დაგვირგვინებული, ქართული სარწმუნოების დამცველი.",
    "A Gothic congregation at worship within the burning church, twenty-six crowns rising with the smoke, the queen gathering the holy remains from the ashes.": "გოთთა კრებული ლოცვად მგზნებარე ეკლესიის შიგნით, ოცდაექვსი გვირგვინი კვამლთან ერთად ამავალი, დედოფალი წმინდა ნეშტის ფერფლიდან შემკრები.",
    "A Gothic general of Rome casting down his military belt before Aurelian, seventy soldiers confessing behind him, the river receiving the wonderworking commander.": "რომის გოთი მხედართმთავარი, ავრელიანეს წინაშე სამხედრო სარტყლის დამგდები, სამოცდაათი ჯარისკაცი მის უკან აღმსარებელი, მდინარე სასწაულმოქმედი წინამძღოლის მიმღები.",
    "A Great Prince of Kyiv with the churches of Smolensk he raised, the monastic habit he longed for held by an angel, the elder Polycarp pointing him back to his throne.": "კიევის დიდი მთავარი სმოლენსკის ეკლესიებით, რომელნიც აღმართა, ანგელოზის ხელთ სამონაზვნო სამოსელი, რომელსაც ესწრაფოდა, და ბერი პოლიკარპე, ტახტისკენ უკან მიმანიშნებელი.",
    "A Greek bishop preaching Christ to the pagan Rostov land, the first shepherd of a hostile flock, the see of Rostov founded amid the idols of the north.": "ბერძენი ეპისკოპოსი, ქრისტეს მქადაგებელი წარმართული როსტოვის მხარისთვის, მტრული სამწყსოს პირველი მწყემსი, როსტოვის საყდარი დაფუძნებული ჩრდილოეთის კერპთა შორის.",
    "A Greek iconographer of Constantinople founding the island monastery of Lake Onega, the Sophia icon he copied in his hands, the peoples of the north gathering to his light at the age of one hundred and five.": "კონსტანტინოპოლელი ბერძენი ხატმწერი, ონეგის ტბის კუნძულოვანი მონასტრის დამაარსებელი, სოფიის ხატი, რომელიც გადაწერა, მის ხელთ, ჩრდილოეთის ხალხები მის ნათელთან შემოკრებილნი ას ხუთი წლის ასაკში.",
    "A Greek metropolitan enthroned at Moscow beside the shrine of Peter, standing unbowed before the khan of the Horde, the Church's charter of freedom in his hand.": "ბერძენი მიტროპოლიტი, მოსკოვში პეტრეს კუბოსთან აღსაყდრებული, ურდოს ხანის წინაშე მოუდრეკლად მდგარი, ეკლესიის თავისუფლების სიგელი მის ხელთ.",
    "A Greek of Ephesus at the Apostle Paul's side, the Temple riot swirling around his innocent presence, the sickbed of Miletus and the sword of Rome completing his long companionship.": "ეფესოელი ბერძენი პავლე მოციქულის გვერდით, ტაძრის აღრეულობა მისი უბიწო ყოფნის გარშემო მღელვარე, მილეტის სნეულის სარეცელი და რომის მახვილი მისი ხანგრძლივი თანამგზავრობის დამასრულებელნი.",
    "A Greek prince laying aside his rank for the monastic habit, the Uchma hermitage rising on the bank of the Volga, the exile made a wonderworker in his adopted land.": "ბერძენი მთავარი, სამონაზვნო სამოსელისთვის თავისი წოდების დამტევებელი, უჩმის უდაბნო ვოლგის ნაპირზე აღმართული, დევნილი, თავის ნაშვილებ მხარეში სასწაულმოქმედად ქცეული.",
    "A Patriarch of Constantinople seated upright in death as in blessing, the Mgar monastery of Lubny receiving the traveler, the two worlds of Greece and Rus' joined at his throne.": "კონსტანტინოპოლის პატრიარქი, სიკვდილში წელში გამართული, ვითარცა კურთხევად, ლუბნის მღარის მონასტერი მოგზაურის მიმღები, საბერძნეთისა და რუსეთის ორი სამყარო მის ტახტთან შეერთებული.",
    "A Persian noble offering his severed members one by one, each with a prayer, angels gathering his prayers.": "სპარსელი დიდებული, თითოეული მოკვეთილი ასოს ლოცვითურთ შემწირველი, ანგელოზები მისი ლოცვების შემკრებნი.",
    "A Persian soldier turned monk, the captive Cross of the Lord shining before him, the waters and the sword of Bethsaloe beneath his crown.": "სპარსელი ჯარისკაცი, ბერად ქცეული, უფლის ტყვექმნილი ჯვარი მის წინაშე მბრწყინავი, ბეთსალოეს წყლები და მახვილი მისი გვირგვინის ქვეშ.",
    "A Roman centurion kneeling before the Apostle Peter, or vested as a bishop holding a Gospel.": "რომაელი ასისთავი, პეტრე მოციქულის წინაშე მუხლმოდრეკილი, ანუ ეპისკოპოსად შემოსილი, სახარების მპყრობელი.",
    "A Roman general in armor holding a cross, his soldiers behind him, a spring at his feet.": "რომაელი მხედართმთავარი აბჯარში, ჯვრის მპყრობელი, მისი ჯარისკაცები მის უკან, წყარო მის ფერხთით.",
    "A Roman maiden in flight across the sea with two servants, the convent of Saint Stephen at Mylasa, a cross of stars brighter than the sun above her repose.": "რომაელი ქალწული ზღვით მიმალული ორი მხევლითურთ, წმინდა სტეფანეს მონასტერი მილასაში, მზეზე უფრო ბრწყინვალე ვარსკვლავთა ჯვარი მისი მიცვალების ზემოთ.",
    "A Roman matron refusing the Arian rite, the fire kindled behind her, Saint Ambrose blessing from afar.": "რომაელი დიდებული ქალი, არიანული წესის უარმყოფელი, ცეცხლი მის უკან აღგზნებული, წმინდა ამბროსი შორიდან მაკურთხებელი.",
    "A Roman noblewoman scattering deeds and treasure to the poor, thousands of freed slaves behind her, her small cell on the Mount of Olives before her.": "რომაელი დიდგვაროვანი ქალი, გლახაკთათვის მამულის სიგელებისა და საუნჯის გამბნევი, ათასობით განთავისუფლებული მონა მის უკან, მისი მცირე სენაკი ზეთისხილის მთაზე მის წინაშე.",
    "A Roman senator opening his house to the Apostle Peter, the household at prayer becoming a church, the greeting of the epistle shining over the door.": "რომაელი სენატორი, პეტრე მოციქულისთვის თავისი სახლის გამღები, ლოცვად მდგარი სახლეულობა ეკლესიად ქცეული, ეპისტოლის მოკითხვა კარის ზემოთ მბრწყინავი.",
    "A Roman widow standing amid seven crowned sons, encouraging each to the contest, her own crown descending last.": "რომაელი ქვრივი, შვიდ დაგვირგვინებულ ძეს შორის მდგარი, თითოეულის ღვაწლისკენ მამხნევებელი, საკუთარი გვირგვინი უკანასკნელად ჩამომავალი.",
    "A Russian captive in the winter night of Kazan, bound and wounded in the snow, alive at dawn with his confession unbroken.": "რუსი ტყვე ყაზანის ზამთრის ღამეში, თოვლში შეკრული და დაჭრილი, გარიჟრაჟზე ცოცხალი, თავისი აღსარებით შეურყეველი.",
    "A Russian soldier-slave at prayer in his master's stable, the Turkish household softened by his faith, his incorrupt relics glorified across the Greek world.": "რუსი ჯარისკაცი-მონა ლოცვად თავისი ბატონის სადგომში, თურქული სახლეულობა მისი სარწმუნოებით დარბილებული, მისი უხრწნელი ნაწილები ბერძნულ სამყაროში განდიდებული.",
    "A Serbian prince leading his army at Kosovo, choosing the kingdom of heaven over the kingdom of earth, crowned as a great-martyr, his incorrupt relics the treasure of his people.": "სერბი მთავარი, კოსოვოზე თავისი ლაშქრის წინამძღოლი, მიწიერ სამეფოზე ზეციური სასუფევლის ამრჩევი, დიდმოწამედ დაგვირგვინებული, მისი უხრწნელი ნაწილები თავისი ერის საუნჯე.",
    "A Spanish dignitary in the Great Schema, the roads of his pilgrimage from Rome to Jerusalem behind him, the Saracen sword before him.": "ესპანელი დიდებული დიდ სქემაში, რომიდან იერუსალიმამდე მისი მოგზაურობის გზები მის უკან, სარკინოზთა მახვილი მის წინაშე.",
})
