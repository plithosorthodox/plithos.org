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

TEXT.update({
    "A Swedish princess become mother of Rus, her sainted son Vladimir beside her, the crowns of France, Hungary, and Norway among her daughters, the nun's habit her final vesture.": "أميرة سويدية صارت أما للروس، وابنها القديس فلاديمير إلى جانبها، وتيجان فرنسا والمجر والنرويج بين بناتها، والثوب الرهباني آخر لباسها.",
    "A Syrian stranger standing three days in prayer in the church of Spoleto, the garden thieves fed at his table and converted, the offered estates refused with a smiling shake of the head.": "غريب سوري يقف ثلاثة أيام في الصلاة في كنيسة سبوليتو، ولصوص البستان يطعمهم على مائدته فيهتدون، والضياع المعروضة يردها بهزة رأس باسمة.",
    "A Tatar captive baptized and tonsured, founding a monastery on the shore of Lake Kozha in the far north, the wilderness hallowed by his prayer.": "أسير تتري اعتمد ولبس الثوب الرهباني، يؤسس ديرا على شاطئ بحيرة كوجا في أقصى الشمال، والبرية تتقدس بصلاته.",
    "A Yup'ik mother in a kuspuk holding a basin and towel, the northern lights above the tundra behind her.": "أم من اليوبيك في ثوب الكوسبوك تحمل مطهرة ومنشفة، وأنوار الشمال فوق التندرا خلفها.",
    "A barefoot ascetic in rags, blessing, at Novgorod.": "ناسك حافي القدمين في أسمال، يبارك، في نوفغورود.",
    "A barefoot fool in tattered clothing by a northern river, giving away what was given to him.": "متباله حافي القدمين في ثياب رثة عند نهر شمالي، يعطي ما أعطي له.",
    "A barefoot fool-for-Christ holding a head of cabbage, at Novgorod by the river.": "متباله بالمسيح حافي القدمين يحمل رأس ملفوف، في نوفغورود عند النهر.",
    "A barefoot fool-for-Christ in a sheepskin holding an axe, by the river defending the city.": "متباله بالمسيح حافي القدمين في فروة يحمل فأسا، عند النهر يدافع عن المدينة.",
    "A barefoot holy fool with long hair, holding a Psalter, of gentle and sorrowful aspect.": "متباله مقدس حافي القدمين طويل الشعر يحمل مزمورا، على وجهه وداعة وحزن.",
    "A basilica at Lydda, the tomb of Saint George within, hierarchs consecrating the church.": "بازيليكا في اللد وفيها قبر القديس جاورجيوس، ورؤساء كهنة يكرسون الكنيسة.",
    "A bearded missionary priest with a traveler's bag, the church of Jackson and the hills of California behind him.": "كاهن مرسل ذو لحية بحقيبة مسافر، وكنيسة جاكسون وتلال كاليفورنيا خلفه.",
    "A beggar beneath the staircase of his father's palace, unknown to all his household, the finished scroll of his life clasped in his dead hand while the emperor and the pope kneel to read it.": "شحاذ تحت سلم قصر أبيه، لا يعرفه أحد من أهل بيته، ودرج سيرته المكتمل مقبوض في يده الميتة بينما الإمبراطور والبابا يركعان ليقرآه.",
    "A bent elder in white on his knees upon the rock, the Theotokos of Tenderness before him, a bear at the edge of the forest clearing.": "شيخ منحن بثوب أبيض راكعا على الصخرة، وأيقونة والدة الإله الحنونة أمامه، ودب عند طرف فسحة الغابة.",
    "A bishop alone in an emptied city awaiting the persecutors, then crucified at Perge, teaching from the cross until his voice failed into glory.": "أسقف وحده في مدينة أخليت ينتظر المضطهدين، ثم مصلوبا في برغي، يعلم من على الصليب حتى انقطع صوته إلى المجد.",
    "A bishop and a presbyter of Persia holding crosses, swords above them.": "أسقف وقس من بلاد فارس يحملان صليبين، والسيوف فوقهما.",
    "A bishop and a virgin holding crosses, broken books of sorcery burning at their feet.": "أسقف وعذراء يحملان صليبين، وكتب السحر المكسورة تحترق عند أقدامهما.",
    "A bishop and his companions holding crosses, cast into a furnace, a soldier among them.": "أسقف ورفاقه يحملون صلبانا، مطروحين في أتون، وبينهم جندي.",
    "A bishop and presbyter cast into a pit, angels crowning them from above.": "أسقف وقس مطروحان في جب، وملائكة تكللهما من فوق.",
    "A bishop and theologian of Lycia with the scroll of his Banquet of the Ten Virgins, refuting the errors of Origen, crowned at the last with martyrdom.": "أسقف ولاهوتي من ليكية بدرج وليمة العذارى العشر، يفند أضاليل أوريجانس، مكللا في الآخر بالشهادة.",
    "A bishop answering the emperor that the Church's questions belong to the Church, the road of exile opening behind him.": "أسقف يجيب الإمبراطور بأن مسائل الكنيسة للكنيسة، وطريق المنفى ينفتح خلفه.",
    "A bishop baptizing an African king, a boy captive and a royal tutor shown in the scenes of his life.": "أسقف يعمد ملكا إفريقيا، وصبي أسير ومؤدب ملكي في مشاهد سيرته.",
    "A bishop barring the church door to an emperor, a beehive at his feet, a scroll of his hymns in hand.": "أسقف يسد باب الكنيسة في وجه إمبراطور، وخلية نحل عند قدميه، ودرج من تسابيحه في يده.",
    "A bishop before a fallen idol, a demon bearing a great stone altar behind him, hot springs at his feet.": "أسقف أمام صنم ساقط، وشيطان يحمل مذبحا حجريا عظيما خلفه، وينابيع حارة عند قدميه.",
    "A bishop before the burning temple of Marnas, the cross-guardian's keys at his belt, the Good Thief descending from the Cross in his vision, the Eudoxiana church rising over pagan Gaza.": "أسقف أمام هيكل مرناس المحترق، ومفاتيح حارس الصليب في منطقته، واللص اليمين ينزل عن الصليب في رؤياه، وكنيسة إفدوكسيانة ترتفع فوق غزة الوثنية.",
    "A bishop before the emperor, pointing to the emperor's son, teaching the honor due the Son of God.": "أسقف أمام الإمبراطور يشير إلى ابن الإمبراطور، يعلم أي كرامة تليق بابن الله.",
    "A bishop beheaded at the altar in mid-Liturgy, twenty-eight years of tribunals and torments ranged behind him like waves, Agathangelus crowned at his side.": "أسقف يقطع رأسه عند المذبح في وسط القداس، وثمانية وعشرون عاما من المحاكم والعذابات مصطفة خلفه كالأمواج، وأغاثانغيلوس مكللا إلى جانبه.",
    "A bishop beholding the ladder to heaven with his predecessor calling from above, one hundred and twenty-eight companions ascending behind him under the Persian sword.": "أسقف يعاين السلم إلى السماء وسلفه يناديه من فوق، ومئة وثمانية وعشرون رفيقا يصعدون خلفه تحت السيف الفارسي.",
    "A bishop by night in a plain cloak, leaving firewood at a poor widow's door, his cathedral of Belgorod behind him.": "أسقف في الليل بعباءة بسيطة يترك حطبا عند باب أرملة فقيرة، وكاتدرائيته في بلغورود خلفه.",
    "A bishop drinking the sorcerer's cup unharmed, the magician kneeling converted beside his cast-down instruments.": "أسقف يشرب كأس الساحر فلا يتأذى، والساحر راكعا قد اهتدى إلى جانب أدواته المطروحة.",
    "A bishop enthroned with a Gospel, the first hierarch of Jerusalem, of ascetic and venerable countenance.": "أسقف على العرش يحمل إنجيلا، أول رؤساء كهنة أورشليم، على وجهه نسك ووقار.",
    "A bishop holding a Gospel, refuting heretics who shrink before his word.": "أسقف يحمل إنجيلا، يفند الهراطقة فينكمشون أمام كلمته.",
    "A bishop holding a page of the alphabet he invented, the sacred birch of the Zyrians felled behind him, the sorcerer Pam turning from the fire and the water, a new people reading the Gospel in its own letters.": "أسقف يحمل صفحة من الأبجدية التي وضعها، وبتولة الزيريان المقدسة مقطوعة خلفه، والساحر بام يرتد عن النار والماء، وشعب جديد يقرأ الإنجيل بحروفه.",
    "A bishop holding a scroll of the Creed, the Theotokos and John the Theologian appearing above, a mountain moved behind.": "أسقف يحمل درج قانون الإيمان، ووالدة الإله ويوحنا اللاهوتي يظهران من فوق، وجبل قد انتقل خلفه.",
    "A bishop holding an icon of Christ against the imperial decree, the sick healed at his hands.": "أسقف يحمل أيقونة المسيح في وجه المرسوم الإمبراطوري، والمرضى يشفون على يديه.",
    "A bishop holding the book of the Divine Names, the darkened sun of the Crucifixion above him.": "أسقف يحمل كتاب الأسماء الإلهية، وشمس الصلب المظلمة فوقه.",
    "A bishop in a laborer's tunic drawing water and hauling wood at Nitria, the omophorion of Damascus folded away, heaven alone reading the monk's true rank.": "أسقف بثوب عامل يستقي الماء ويحمل الحطب في نيتريا، وأومفوريون دمشق مطوي بعيدا، والسماء وحدها تقرأ رتبة الراهب الحقيقية.",
    "A bishop in a mitre holding a crozier, with a gray beard and an ascetic, gentle face.": "أسقف بميطرة يحمل عكازا، بلحية بيضاء ووجه ناسك وديع.",
    "A bishop in monastic poverty, Cernica's island monastery at one hand and the Frasinei he founded at the other, the seminary and the printing press of Ramnic behind him, his face worn bright by fasting.": "أسقف في فقر رهباني، ودير جزيرة تشرنيكا عن يمينه وفراسيني الذي أسسه عن شماله، ومدرسة رمنيك ومطبعتها خلفه، ووجهه قد صقله الصوم.",
    "A bishop in the omophorion and mantle holding a book, of gentle and humble aspect.": "أسقف بالأومفوريون والعباءة يحمل كتابا، على وجهه وداعة وتواضع.",
    "A bishop in the omophorion and sakkos holding a Gospel book, with a Greek-style beard.": "أسقف بالأومفوريون والساكوس يحمل كتاب الإنجيل، بلحية على الطراز اليوناني.",
})
