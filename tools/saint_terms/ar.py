# -*- coding: utf-8 -*-
"""Arabic for the vocabulary that stands beside the lives.

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
    "(Abibus) of Egypt": "(أبيبوس) المصري",
    "(Apphianus) and Edesius (Aedesius) of Lycia": "(أبيانوس) وإديسيوس (أيديسيوس) من ليكية",
    "(Eustace) the Confessor, Bishop of Bithynia": "(إفستاثيوس) المعترف، أسقف بيثينية",
    "(Jacob) the Presbyter, and Azadanes and Abdiesus the Deacons, of Persia": "(يعقوب) القس، وأزادانيس وعبديشوع الشماسان، من بلاد فارس",
    "(Vadim) of Persia": "(واديم) الفارسي",
    "(Voino-Yasenetsky), Archbishop of Simferopol and Crimea": "(فوينو-ياسينيتسكي)، رئيس أساقفة سيمفيروبول والقرم",
    "(also called Susanna), New Martyr of Lesbos": "(المدعوة أيضا سوسنة)، الشهيدة الجديدة من لسبوس",
    "(tonsured David and Euphrosyne), Wonderworkers of Murom": "(المحلوقان داود وإفروسيني)، العجائبيان في موروم",
    "A Cappadocian centurion bowing beneath the sword with his eyes lifted in thanksgiving, the walnut tree of the tradition behind him, the churches of Byzantium rising over his relics.": "قائد مئة من كبادوكية ينحني تحت السيف ورأسه مرفوع بالشكر، وشجرة الجوز التي يذكرها التقليد خلفه، وكنائس بيزنطية ترتفع فوق رفاته.",
    "A Celtic hermit of the Devon coast bearing his own severed head to the spring, the robbers behind him, crowned as a martyr among the saints of Britain.": "ناسك كلتي من ساحل ديفون يحمل رأسه المقطوع إلى النبع، واللصوص خلفه، مكللا شهيدا بين قديسي بريطانيا.",
    "A Christian general casting down the temples of Galatia, his twelve tribunes and his thousands of soldiers with their wives and children crowned around him, the converted sorcerer Callinicus among them.": "قائد مسيحي يهدم هياكل غلاطية، واثنا عشر من قواده وألوف من جنده مع نسائهم وأولادهم مكللون حوله، وبينهم الساحر كالينيكوس الذي اهتدى.",
    "A Christian of Alexandria standing before the tribunal to denounce its cruelty, the confession volunteered and the sword received.": "مسيحي من الإسكندرية يقف أمام المحكمة ليندد بقسوتها، اعتراف بذله من نفسه وسيف قبله.",
    "A Creole-Aleut priest in vestments holding a Gospel and a cross, against an Alaskan landscape.": "كاهن من الكريول والأليوت بالحلة الكهنوتية يحمل إنجيلا وصليبا، على خلفية من طبيعة ألاسكا.",
    "A Georgian bishop with a book and a restored church, schoolchildren and monasteries behind him.": "أسقف جورجي بكتاب وكنيسة أعاد بناءها، وتلاميذ مدارس وأديرة خلفه.",
    "A Georgian commander marking his forehead with the cross in his own blood, his soldiers crowned around him.": "قائد جورجي يرسم الصليب على جبهته بدمه، وجنوده مكللون حوله.",
    "A Georgian monk in prayer before the cave monastery of Gareji in the desert hills.": "راهب جورجي في الصلاة أمام دير المغاور في غاريجي بين تلال البرية.",
    "A Georgian monk-abbot holding a scroll or a book.": "راهب جورجي رئيس دير يحمل درجا أو كتابا.",
    "A Georgian prince and commander refusing to trample the icon of Christ before the conqueror, crowned as a great-martyr, the defender of the Georgian faith.": "أمير جورجي وقائد يأبى أن يدوس أيقونة المسيح أمام الفاتح، مكللا عظيما في الشهداء، حامي الإيمان الجورجي.",
    "A Gothic congregation at worship within the burning church, twenty-six crowns rising with the smoke, the queen gathering the holy remains from the ashes.": "جماعة قوطية في الصلاة داخل الكنيسة المشتعلة، وستة وعشرون إكليلا تصعد مع الدخان، والملكة تجمع الرفات المقدسة من الرماد.",
    "A Gothic general of Rome casting down his military belt before Aurelian, seventy soldiers confessing behind him, the river receiving the wonderworking commander.": "قائد قوطي في جيش رومة يطرح منطقة جنديته أمام أفرليانوس، وسبعون جنديا يعترفون خلفه، والنهر يتقبل القائد العجائبي.",
    "A Great Prince of Kyiv with the churches of Smolensk he raised, the monastic habit he longed for held by an angel, the elder Polycarp pointing him back to his throne.": "أمير كييف الأكبر مع كنائس سمولنسك التي شادها، والثوب الرهباني الذي اشتهاه يحمله ملاك، والشيخ بوليكاربوس يرده إلى عرشه.",
    "A Greek bishop preaching Christ to the pagan Rostov land, the first shepherd of a hostile flock, the see of Rostov founded amid the idols of the north.": "أسقف يوناني يبشر بالمسيح في أرض روستوف الوثنية، أول راع لرعية معادية، وكرسي روستوف يقوم بين أصنام الشمال.",
    "A Greek iconographer of Constantinople founding the island monastery of Lake Onega, the Sophia icon he copied in his hands, the peoples of the north gathering to his light at the age of one hundred and five.": "مصور أيقونات يوناني من القسطنطينية يؤسس دير الجزيرة في بحيرة أونيغا، وأيقونة الحكمة التي نسخها في يديه، وشعوب الشمال تجتمع إلى نوره وهو ابن مئة وخمس سنين.",
    "A Greek metropolitan enthroned at Moscow beside the shrine of Peter, standing unbowed before the khan of the Horde, the Church's charter of freedom in his hand.": "مطران يوناني على كرسي موسكو إلى جانب ضريح بطرس، يقف غير منحن أمام خان القبيلة، وميثاق حرية الكنيسة في يده.",
    "A Greek of Ephesus at the Apostle Paul's side, the Temple riot swirling around his innocent presence, the sickbed of Miletus and the sword of Rome completing his long companionship.": "يوناني من أفسس إلى جانب الرسول بولس، وشغب الهيكل يدور حول براءته، وفراش المرض في ميليتس وسيف رومة يتمان رفقته الطويلة.",
    "A Greek prince laying aside his rank for the monastic habit, the Uchma hermitage rising on the bank of the Volga, the exile made a wonderworker in his adopted land.": "أمير يوناني يضع رتبته جانبا ويلبس الثوب الرهباني، ومعتكف أوتشما يقوم على ضفة الفولغا، والغريب يصير عجائبيا في الأرض التي تبنته.",
    "A Patriarch of Constantinople seated upright in death as in blessing, the Mgar monastery of Lubny receiving the traveler, the two worlds of Greece and Rus' joined at his throne.": "بطريرك القسطنطينية جالسا في موته كأنه يبارك، ودير مغار في لوبني يستقبل المسافر، وعالما اليونان والروس مجتمعان عند عرشه.",
    "A Persian noble offering his severed members one by one, each with a prayer, angels gathering his prayers.": "شريف فارسي يقدم أعضاءه المقطوعة واحدا واحدا، مع كل عضو صلاة، والملائكة تجمع صلواته.",
    "A Persian soldier turned monk, the captive Cross of the Lord shining before him, the waters and the sword of Bethsaloe beneath his crown.": "جندي فارسي صار راهبا، وصليب الرب المسبي يلمع أمامه، ومياه بيت سلوخ وسيفها تحت إكليله.",
    "A Roman centurion kneeling before the Apostle Peter, or vested as a bishop holding a Gospel.": "قائد مئة روماني راكعا أمام الرسول بطرس، أو بحلة أسقف يحمل إنجيلا.",
    "A Roman general in armor holding a cross, his soldiers behind him, a spring at his feet.": "قائد روماني في سلاحه يحمل صليبا، وجنوده خلفه، وينبوع عند قدميه.",
    "A Roman maiden in flight across the sea with two servants, the convent of Saint Stephen at Mylasa, a cross of stars brighter than the sun above her repose.": "فتاة رومانية هاربة عبر البحر مع خادمتين، ودير القديس إسطفانوس في ميلاسا، وصليب من نجوم أشد بهاء من الشمس فوق رقادها.",
    "A Roman matron refusing the Arian rite, the fire kindled behind her, Saint Ambrose blessing from afar.": "سيدة رومانية تأبى الطقس الأريوسي، والنار تضرم خلفها، والقديس أمبروسيوس يبارك من بعيد.",
    "A Roman noblewoman scattering deeds and treasure to the poor, thousands of freed slaves behind her, her small cell on the Mount of Olives before her.": "شريفة رومانية تبدد صكوكها وكنوزها على الفقراء، وألوف من العبيد الذين أعتقتهم خلفها، وقلايتها الصغيرة على جبل الزيتون أمامها.",
    "A Roman senator opening his house to the Apostle Peter, the household at prayer becoming a church, the greeting of the epistle shining over the door.": "شيخ من مجلس رومة يفتح بيته للرسول بطرس، وأهل البيت في الصلاة يصيرون كنيسة، وتحية الرسالة تشرق فوق الباب.",
    "A Roman widow standing amid seven crowned sons, encouraging each to the contest, her own crown descending last.": "أرملة رومانية واقفة بين سبعة أبناء مكللين، تشجع كل واحد على الجهاد، وإكليلها ينزل آخر الجميع.",
    "A Russian captive in the winter night of Kazan, bound and wounded in the snow, alive at dawn with his confession unbroken.": "أسير روسي في ليل قازان الشتوي، مقيدا مجروحا في الثلج، حيا عند الفجر واعترافه غير منكسر.",
    "A Russian soldier-slave at prayer in his master's stable, the Turkish household softened by his faith, his incorrupt relics glorified across the Greek world.": "جندي روسي في العبودية يصلي في إسطبل سيده، وبيت التركي يلين بإيمانه، ورفاته غير البالية تمجد في العالم اليوناني كله.",
    "A Serbian prince leading his army at Kosovo, choosing the kingdom of heaven over the kingdom of earth, crowned as a great-martyr, his incorrupt relics the treasure of his people.": "أمير صربي يقود جيشه في كوسوفو، مختارا ملكوت السماء على ملك الأرض، مكللا عظيما في الشهداء، ورفاته غير البالية كنز شعبه.",
    "A Spanish dignitary in the Great Schema, the roads of his pilgrimage from Rome to Jerusalem behind him, the Saracen sword before him.": "وجيه إسباني في الإسكيم الكبير، ودروب حجه من رومة إلى أورشليم خلفه، وسيف السراسنة أمامه.",
})
