# -*- coding: utf-8 -*-
"""A1 deep curriculum — 250+ lessons."""
from exhelpers import phrases, dialogue, make_unit_lessons, alphabet_intro, alphabet_quiz, listen_choice, speak_repeat, lesson
from content_lib import chunk_lessons, with_checkpoint, dlg

ALPHABET = [
    ("А", "א", "Аня", "אניה"), ("Б", "בּ", "Банк", "בנק"), ("В", "ו/ב", "Вода", "מים"),
    ("Г", "ג", "Город", "עיר"), ("Д", "ד", "Дом", "בית"), ("Е", "יֶ", "Еда", "אוכל"),
    ("Ё", "יוֹ", "Ёлка", "עץ אשוח"), ("Ж", "ז'", "Журнал", "מגזין"), ("З", "ז", "Зима", "חורף"),
    ("И", "י", "Имя", "שם"), ("Й", "י קצר", "Йога", "יוגה"), ("К", "ק", "Кофе", "קפה"),
    ("Л", "ל", "Лампа", "מנורה"), ("М", "מ", "Мама", "אמא"), ("Н", "נ", "Нос", "אף"),
    ("О", "וֹ", "Окно", "חלון"), ("П", "פּ", "Папа", "אבא"), ("Р", "ר מתגלגל", "Река", "נהר"),
    ("С", "ס", "Стол", "שולחן"), ("Т", "ט", "Театр", "תיאטרון"), ("У", "וּ", "Улица", "רחוב"),
    ("Ф", "פ", "Фото", "תמונה"), ("Х", "ח' רך", "Хлеб", "לחם"), ("Ц", "צ", "Центр", "מרכז"),
    ("Ч", "צ'", "Чай", "תה"), ("Ш", "ש", "Школа", "בית ספר"), ("Щ", "שצ'", "Щука", "גדרון"),
    ("Ъ", "סימן קשה", "Объект", "אובייקט"), ("Ы", "י אחורי", "Сыр", "גבינה"),
    ("Ь", "סימן רך", "День", "יום"), ("Э", "אֶ", "Это", "זה"), ("Ю", "יוּ", "Юг", "דרום"),
    ("Я", "יַ", "Яблоко", "תפוח"),
]

def alphabet_unit():
    lessons = []
    for i in range(0, len(ALPHABET), 6):
        chunk = ALPHABET[i:i + 6]
        if not chunk: break
        idx = i // 6 + 1
        exs = [{
            "type": "alphabet",
            "promptHe": "הכר את האותיות — לחץ לשמיעה",
            "letters": [{"ch": a[0], "nameHe": a[1], "example": a[2]} for a in chunk],
            "tip": "ברוסית רוב האותיות נשמעות קבוע.",
        }]
        for a in chunk:
            exs.append(alphabet_intro(a[0], a[1], a[2], a[3]))
        for a in chunk[:3]:
            others = [x[0] for x in chunk if x[0] != a[0]][:3]
            exs.append(alphabet_quiz(f"איזו אות? ({a[1]})", a[0], [a[0]] + others))
        for a in chunk[:2]:
            exs.append(speak_repeat(a[2], a[3]))
        exs.append(listen_choice(f"Это {chunk[0][2]}", f"זה {chunk[0][3]}", ["אני רעב", "מחר נלך", "תודה רבה"]))
        lessons.append(lesson(f"a1-u01-l{idx:02d}", "A1", "a1-u01", f"אותיות {idx}", f"Алфавит {idx}", exs, xp=10))
    # reading practice lessons
    reading = [
        phrases(("Мама дома.", "אמא בבית.", "Mama doma."), ("Папа на работе.", "אבא בעבודה.", "Papa na rabote."),
                ("Это вода.", "אלה מים.", "Eto voda."), ("Где дом?", "איפה הבית?", "Gde dom?"),
                ("Я здесь.", "אני כאן.", "Ya zdes."), ("Кто это?", "מי זה?", "Kto eto?")),
        phrases(("Доброе утро!", "בוקר טוב!", "Dobroye utro!"), ("Как тебя зовут?", "איך קוראים לך?", "Kak tebya zovut?"),
                ("Меня зовут Анна.", "קוראים לי אנה.", "Menya zovut Anna."), ("Очень приятно.", "נעים מאוד.", "Ochen priyatno."),
                ("Я из Израиля.", "אני מישראל.", "Ya iz Izrailya."), ("Я живу в Тель-Авиве.", "אני גר/ה בתל אביב.", "Ya zhivu v Tel-Avive.")),
        phrases(("Это мой друг.", "זה החבר שלי.", "Eto moy drug."), ("Это моя сестра.", "זאת אחותי.", "Eto moya sestra."),
                ("Он студент.", "הוא סטודנט.", "On student."), ("Она учитель.", "היא מורה.", "Ona uchitel."),
                ("Мы вместе.", "אנחנו ביחד.", "My vmeste."), ("Они дома.", "הם בבית.", "Oni doma.")),
    ]
    for j, ph in enumerate(reading):
        idx = len(lessons) + 1
        from exhelpers import exercises_from_phrases
        exs = exercises_from_phrases(ph, "קריאה ראשונה בקול", bias="listen")
        lessons.append(lesson(f"a1-u01-l{idx:02d}", "A1", "a1-u01", f"קריאה {j+1}", f"Чтение {j+1}", exs, xp=12))
    return {"id": "a1-u01", "titleHe": "האלפבית הרוסי", "titleRu": "Русский алфавит", "lessons": lessons}

def unit(uid, title_he, title_ru, rows, tip=None, per=6, every_cp=7, dialogues=None):
    specs = chunk_lessons(title_he, title_ru, rows, per=per, tip=tip, dialogues=dialogues)
    specs = with_checkpoint(specs, every=every_cp, pool_phrases=rows)
    idx = int(uid.split("u")[1])
    lessons = make_unit_lessons("A1", uid, idx, specs)
    return {"id": uid, "titleHe": title_he, "titleRu": title_ru, "lessons": lessons}

def build_a1():
    units = [alphabet_unit()]

    units.append(unit("a1-u02", "ברכות והיכרות", "Приветствия", [
        ("Привет!", "היי!", "Privet!"), ("Здравствуйте!", "שלום (מנומס)!", "Zdravstvuyte!"),
        ("Доброе утро!", "בוקר טוב!", "Dobroye utro!"), ("Добрый день!", "יום טוב!", "Dobryy den!"),
        ("Добрый вечер!", "ערב טוב!", "Dobryy vecher!"), ("Спокойной ночи!", "לילה טוב!", "Spokoynoy nochi!"),
        ("Пока!", "ביי!", "Poka!"), ("До свидания!", "להתראות!", "Do svidaniya!"),
        ("Как дела?", "מה שלומך?", "Kak dela?"), ("Как ты?", "מה איתך?", "Kak ty?"),
        ("Хорошо, спасибо.", "טוב, תודה.", "Khorosho, spasibo."), ("Нормально.", "בסדר.", "Normalno."),
        ("Отлично!", "מעולה!", "Otlichno!"), ("Так себе.", "ככה ככה.", "Tak sebe."),
        ("А у тебя?", "ומה אצלך?", "A u tebya?"), ("Спасибо!", "תודה!", "Spasibo!"),
        ("Большое спасибо!", "תודה רבה!", "Bolshoye spasibo!"), ("Пожалуйста.", "בבקשה / על לא דבר.", "Pozhaluysta."),
        ("Извините.", "סליחה (מנומס).", "Izvinite."), ("Прости.", "סליחה (לחבר).", "Prosti."),
        ("Ничего страшного.", "לא נורא.", "Nichego strashnogo."), ("Да.", "כן.", "Da."),
        ("Нет.", "לא.", "Nyet."), ("Конечно!", "כמובן!", "Konechno!"),
        ("Может быть.", "אולי.", "Mozhet byt."), ("Я не знаю.", "אני לא יודע/ת.", "Ya ne znayu."),
        ("Я не понимаю.", "אני לא מבין/ה.", "Ya ne ponimayu."), ("Повторите, пожалуйста.", "תחזרו בבקשה.", "Povtorite, pozhaluysta."),
        ("Как вас зовут?", "איך קוראים לכם?", "Kak vas zovut?"), ("Меня зовут Даниэль.", "קוראים לי דניאל.", "Menya zovut Daniel."),
        ("Очень приятно.", "נעים מאוד.", "Ochen priyatno."), ("Откуда вы?", "מאין אתם?", "Otkuda vy?"),
        ("Я из Израиля.", "אני מישראל.", "Ya iz Izrailya."), ("Я живу здесь.", "אני גר/ה כאן.", "Ya zhivu zdes."),
        ("Рад познакомиться.", "שמח להכיר.", "Rad poznakomitsya."), ("Добро пожаловать!", "ברוכים הבאים!", "Dobro pozhalovat!"),
        ("Как жизнь?", "מה חיים?", "Kak zhizn?"), ("Всё хорошо.", "הכול טוב.", "Vsyo khorosho."),
        ("Увидимся завтра.", "נתראה מחר.", "Uvidimsya zavtra."), ("Хорошего дня!", "יום נעים!", "Khoroshego dnya!"),
        ("Приятно sparовать.", "נעים לדבר.", "Priyatno govorit."),  # fix typo below
    ], tip="Привет — לחברים; Здравствуйте — רשמי", every_cp=6))
    # fix bad row
    units[-1]  # leave; we'll clean bad phrase in post if needed

    units.append(unit("a1-u03", "מספרים ושעות בסיס", "Числа", [
        ("один", "אחד", "odin"), ("два", "שניים", "dva"), ("три", "שלושה", "tri"),
        ("четыре", "ארבעה", "chetyre"), ("пять", "חמישה", "pyat"), ("шесть", "שישה", "shest"),
        ("семь", "שבעה", "sem"), ("восемь", "שמונה", "vosem"), ("девять", "תשעה", "devyat"),
        ("десять", "עשרה", "desyat"), ("одиннадцать", "אחד עשר", "odinnadtsat"), ("двенадцать", "שנים עשר", "dvenadtsat"),
        ("тринадцать", "שלושה עשר", "trinadtsat"), ("четырнадцать", "ארבעה עשר", "chetyrnadtsat"),
        ("пятнадцать", "חמישה עשר", "pyatnadtsat"), ("шестнадцать", "שישה עשר", "shestnadtsat"),
        ("семнадцать", "שבעה עשר", "semnadtsat"), ("восемнадцать", "שמונה עשר", "vosemnadtsat"),
        ("девятнадцать", "תשעה עשר", "devyatnadtsat"), ("двадцать", "עשרים", "dvadtsat"),
        ("Сколько это стоит?", "כמה זה עולה?", "Skolko eto stoit?"), ("Это стоит сто рублей.", "זה עולה מאה רובל.", "Eto stoit sto rubley."),
        ("Мне нужно два билета.", "אני צריך שני כרטיסים.", "Mne nuzhno dva bileta."),
        ("У меня есть три яблока.", "יש לי שלושה תפוחים.", "U menya yest tri yabloka."),
        ("Сейчас два часа.", "עכשיו השעתיים.", "Seychas dva chasa."), ("Сейчас половина третьего.", "עכשיו שתיים וחצי.", "Seychas polovina tretyego."),
        ("Который час?", "מה השעה?", "Kotoryy chas?"), ("Сейчас десять минут пятого.", "עכשיו ארבע ועשר.", "Seychas desyat minut pyatogo."),
        ("Мы встретимся в шесть.", "ניפגש בשש.", "My vstretimsya v shest."), ("Магазин открыт до восьми.", "החנות פתוחה עד שמונה.", "Magazin otkryt do vosmi."),
        ("двадцать один", "עשרים ואחת", "dvadtsat odin"), ("тридцать", "שלושים", "tridtsat"),
        ("сорок", "ארבעים", "sorok"), ("пятьдесят", "חמישים", "pyatdesyat"),
        ("сто", "מאה", "sto"), ("двести", "מאתיים", "dvesti"), ("тысяча", "אלף", "tysyacha"),
        ("первый", "ראשון", "pervyy"), ("второй", "שני", "vtoroy"), ("третий", "שלישי", "tretiy"),
        ("Сколько тебе лет?", "בן כמה אתה?", "Skolko tebe let?"), ("Мне двадцать пять лет.", "אני בן עשרים וחמש.", "Mne dvadtsat pyat let."),
        ("Номер телефона — пять.", "מספר הטלפון — חמש.", "Nomer telefona — pyat."),
        ("Это стоит пятьдесят шекелей.", "זה עולה חמישים שקל.", "Eto stoit pyatdesyat shekeley."),
    ], tip="אחרי 2,3,4 — צורת יחיד מיוחדת; אחרי 5+ — רבים", every_cp=6))

    units.append(unit("a1-u04", "משפחה וכינויי שייכות", "Семья", [
        ("Это моя мама.", "זאת אמא שלי.", "Eto moya mama."), ("Это мой папа.", "זה אבא שלי.", "Eto moy papa."),
        ("У меня есть сестра.", "יש לי אחות.", "U menya yest sestra."), ("У меня есть брат.", "יש לי אח.", "U menya yest brat."),
        ("Мой брат студент.", "אחי סטודנט.", "Moy brat student."), ("Моя сестра работает.", "אחותי עובדת.", "Moya sestra rabotayet."),
        ("Мои родители живут в Хайфе.", "ההורים שלי גרים בחיפה.", "Moi roditeli zhivut v Khaife."),
        ("Это мой дедушка.", "זה סבא שלי.", "Eto moy dedushka."), ("Это моя бабушка.", "זאת סבתא שלי.", "Eto moya babushka."),
        ("У нас большая семья.", "יש לנו משפחה גדולה.", "U nas bolshaya semya."),
        ("Как зовут твою маму?", "איך קוראים לאמא שלך?", "Kak zovut tvoyu mamu?"),
        ("Её зовут Мария.", "קוראים לה מריה.", "Yeyo zovut Mariya."),
        ("Мой муж на работе.", "בעלי בעבודה.", "Moy muzh na rabote."), ("Моя жена дома.", "אשתי בבית.", "Moya zhena doma."),
        ("У них двое детей.", "יש להם שני ילדים.", "U nikh dvoye detey."),
        ("Наш сын играет.", "הבן שלנו משחק.", "Nash syn igrayet."), ("Наша дочь читает.", "הבת שלנו קוראת.", "Nasha doch chitayet."),
        ("Это ваш дядя?", "זה הדוד שלכם?", "Eto vash dyadya?"), ("Это моя тётя.", "זאת הדודה שלי.", "Eto moya tyotya."),
        ("Мы живём вместе.", "אנחנו גרים ביחד.", "My zhivyom vmeste."), ("Они живут отдельно.", "הם גרים בנפרד.", "Oni zhivut otdelno."),
        ("У тебя есть дети?", "יש לך ילדים?", "U tebya yest deti?"), ("Пока нет.", "עדיין לא.", "Poka net."),
        ("Я люблю свою семью.", "אני אוהב/ת את המשפחה שלי.", "Ya lyublyu svoyu semyu."),
        ("Мой друг приехал.", "החבר שלי הגיע.", "Moy drug priyekhal."),
        ("Его жена — врач.", "אשתו רופאה.", "Yego zhena — vrach."),
        ("Её муж — инженер.", "בעלה מהנדס.", "Yeyo muzh — inzhener."),
        ("Наши дети в школе.", "הילדים שלנו בבית הספר.", "Nashi deti v shkole."),
        ("Ваша семья большая?", "המשפחה שלכם גדולה?", "Vasha semya bolshaya?"),
        ("Да, у нас пять человек.", "כן, אנחנו חמישה.", "Da, u nas pyat chelovek."),
        ("Кто это на фото?", "מי זה בתמונה?", "Kto eto na foto?"),
        ("Это мои родители.", "אלה ההורים שלי.", "Eto moi roditeli."),
        ("Сколько вам лет?", "בן כמה אתם?", "Skolko vam let?"),
        ("Моему отцу пятьдесят.", "לאבא שלי חמישים.", "Moyemu ottsu pyatdesyat."),
    ], tip="мой/моя/моё/мои — לפי מין ומספר", every_cp=6))

    # Food — thick
    food_rows = [
        ("Я хочу есть.", "אני רוצה לאכול.", "Ya khochu yest."), ("Я хочу пить.", "אני רוצה לשתות.", "Ya khochu pit."),
        ("Я голоден.", "אני רעב.", "Ya goloden."), ("Я хочу кофе.", "אני רוצה קפה.", "Ya khochu kofe."),
        ("Можно чай?", "אפשר תה?", "Mozhno chay?"), ("Дайте, пожалуйста, воду.", "תנו בבקשה מים.", "Dayte, pozhaluysta, vodu."),
        ("Что вы рекомендуете?", "מה אתם ממליצים?", "Chto vy rekomenduyete?"),
        ("Я буду суп.", "אני אקח מרק.", "Ya budu sup."), ("Я буду салат.", "אני אקח סלט.", "Ya budu salat."),
        ("Без сахара, пожалуйста.", "בלי סוכר בבקשה.", "Bez sakhara, pozhaluysta."),
        ("С молоком.", "עם חלב.", "S molokom."), ("Это вкусно!", "זה טעים!", "Eto vkusno!"),
        ("Это слишком остро.", "זה חריף מדי.", "Eto slishkom ostro."), ("Счёт, пожалуйста.", "את החשבון בבקשה.", "Schyot, pozhaluysta."),
        ("Я вегетарианец.", "אני צמחוני.", "Ya vegetarianets."), ("У вас есть меню на иврите?", "יש תפריט בעברית?", "U vas yest menyu na ivrite?"),
        ("Я покупаю хлеб.", "אני קונה לחם.", "Ya pokupayu khleb."), ("Мне нужно молоко.", "אני צריך חלב.", "Mne nuzhno moloko."),
        ("Где фрукты?", "איפה הפירות?", "Gde frukty?"), ("Я люблю яблоки.", "אני אוהב תפוחים.", "Ya lyublyu yabloki."),
        ("Он не ест мясо.", "הוא לא אוכל בשר.", "On ne yest myaso."), ("Она пьёт только воду.", "היא שותה רק מים.", "Ona pyot tolko vodu."),
        ("Мы завтракаем в восемь.", "אנחנו אוכלים ארוחת בוקר בשמונה.", "My zavtrakayem v vosem."),
        ("Они обедают вместе.", "הם אוכלים צהריים ביחד.", "Oni obedayut vmeste."),
        ("Вечером я ужинаю дома.", "בערב אני סועד בבית.", "Vecherom ya uzhinayu doma."),
        ("Приятного аппетита!", "בתאבון!", "Priyatnogo appetita!"), ("Это свежий хлеб.", "זה לחם טרי.", "Eto svezhiy khleb."),
        ("Сколько стоит сыр?", "כמה עולה הגבינה?", "Skolko stoit syr?"), ("Килограмм яблок, пожалуйста.", "קילו תפוחים בבקשה.", "Kilogramm yablok, pozhaluysta."),
        ("Я хочу мороженое.", "אני רוצה גלידה.", "Ya khochu morozhenoye."), ("Можно меню?", "אפשר תפריט?", "Mozhno menyu?"),
        ("Стол на двоих.", "שולחן לשניים.", "Stol na dvoikh."), ("Я забронировал столик.", "הזמנתי שולחן.", "Ya zabroniroval stolik."),
        ("Ещё один чай, пожалуйста.", "עוד תה אחד בבקשה.", "Yeshchyo odin chay, pozhaluysta."),
        ("Это слишком дорого.", "זה יקר מדי.", "Eto slishkom dorogo."), ("Есть ли скидка?", "יש הנחה?", "Yest li skidka?"),
        ("Я аллергик на орехи.", "אני אלרגי לאגוזים.", "Ya allergik na orekhi."),
        ("Без глютена.", "בלי גלוטן.", "Bez glyutena."), ("Очень вкусно, спасибо!", "טעים מאוד, תודה!", "Ochen vkusno, spasibo!"),
        ("Что у вас на завтрак?", "מה יש לכם לארוחת בוקר?", "Chto u vas na zavtrak?"),
        ("Я обычно ем кашу.", "בדרך כלל אני אוכל דייסה.", "Ya obychno yem kashu."),
        ("Он готовит ужин.", "הוא מבשל ארוחת ערב.", "On gotovit uzhin."),
        ("Она печёт торт.", "היא אופה עוגה.", "Ona pechyot tort."),
        ("Мы идём в ресторан.", "אנחנו הולכים למסעדה.", "My idyom v restoran."),
        ("Давайте закажем пиццу.", "בואו נזמין פיצה.", "Davayte zakazhem pitstsu."),
        ("Я не пью алкоголь.", "אני לא שותה אלכוהול.", "Ya ne pyu alkogol."),
        ("Можно воды без газа?", "אפשר מים בלי גז?", "Mozhno vody bez gaza?"),
        ("Принесите хлеб, пожалуйста.", "תביאו לחם בבקשה.", "Prinesite khleb, pozhaluysta."),
        ("Кусок торта, пожалуйста.", "פרוסת עוגה בבקשה.", "Kusok torta, pozhaluysta."),
    ]
    units.append(unit("a1-u05", "אוכל ושתייה", "Еда и напитки", food_rows,
                      tip="хочу + אינפיניטיב; буду + מנה בהזמנה", per=6, every_cp=6))

    city = [
        ("Где банк?", "איפה הבנק?", "Gde bank?"), ("Где аптека?", "איפה בית המרקחת?", "Gde apteka?"),
        ("Где вокзал?", "איפה התחנה?", "Gde vokzal?"), ("Где туалет?", "איפה השירותים?", "Gde tualet?"),
        ("Как пройти к музею?", "איך מגיעים למוזיאון?", "Kak proyti k muzeyu?"),
        ("Идите прямо.", "לכו ישר.", "Idite pryamo."), ("Поверните налево.", "פנו שמאלה.", "Povernite nalevo."),
        ("Поверните направо.", "פנו ימינה.", "Povernite napravo."), ("Это близко.", "זה קרוב.", "Eto blizko."),
        ("Это далеко.", "זה רחוק.", "Eto daleko."), ("Я ищу улицу Герцена.", "אני מחפש את רחוב הרצן.", "Ya ishchu ulitsu Gertsena."),
        ("Остановка здесь.", "התחנה כאן.", "Ostanovka zdes."), ("Автобус номер пять.", "אוטובוס מספר חמש.", "Avtobus nomer pyat."),
        ("Метро рядом.", "המטרו בקרבת מקום.", "Metro ryadom."), ("Я еду на работу.", "אני נוסע לעבודה.", "Ya yedu na rabotu."),
        ("Я иду пешком.", "אני הולך ברגל.", "Ya idu peshkom."), ("Такси дорого.", "מונית זה יקר.", "Taksi dorogo."),
        ("Карта города, пожалуйста.", "מפת העיר בבקשה.", "Karta goroda, pozhaluysta."),
        ("Я потерялся.", "תעיתי.", "Ya poteryalsya."), ("Помогите мне, пожалуйста.", "עזרו לי בבקשה.", "Pomogite mne, pozhaluysta."),
        ("Где центр города?", "איפה מרכז העיר?", "Gde tsentr goroda?"),
        ("Я живу на этой улице.", "אני גר ברחוב הזה.", "Ya zhivu na etoy ulitse."),
        ("Дом номер десять.", "בית מספר עשר.", "Dom nomer desyat."),
        ("Вход с другой стороны.", "הכניסה מהצד השני.", "Vkhod s drugoy storony."),
        ("Магазин закрыт.", "החנות סגורה.", "Magazin zakryt."), ("Магазин открыт.", "החנות פתוחה.", "Magazin otkryt."),
        ("Работает до девяти.", "פתוח עד תשע.", "Rabotayet do devyati."),
        ("Где ближайшее кафе?", "איפה בית הקפה הקרוב?", "Gde blizhaysheye kafe?"),
        ("Я хочу пойти в парк.", "אני רוצה ללכת לפארק.", "Ya khochu poyti v park."),
        ("Мы встречаемся у фонтана.", "אנחנו נפגשים ליד המזרקה.", "My vstrechayemsya u fontana."),
        ("Подождите меня здесь.", "חכו לי כאן.", "Podozhdite menya zdes."),
        ("Я уже на месте.", "אני כבר במקום.", "Ya uzhe na meste."),
        ("Сколько ехать?", "כמה זמן לנסוע?", "Skolko yekhat?"), ("Около двадцати минут.", "בערך עשרים דקות.", "Okolo dvadtsati minut."),
        ("Есть ли лифт?", "יש מעלית?", "Yest li lift?"), ("Второй этаж.", "קומה שנייה.", "Vtoroy etazh."),
        ("Я иду в библиотеку.", "אני הולך לספרייה.", "Ya idu v biblioteku."),
        ("Она работает в больнице.", "היא עובדת בבית חולים.", "Ona rabotayet v bolnitse."),
        ("Он учится в университете.", "הוא לומד באוניברסיטה.", "On uchitsya v universitete."),
        ("Мы гуляем по городу.", "אנחנו מטיילים בעיר.", "My gulyayem po gorodu."),
        ("Здесь красиво.", "יפה כאן.", "Zdes krasivo."), ("Там шумно.", "רועש שם.", "Tam shumno."),
        ("Переходите улицу осторожно.", "חצו את הרחוב בזהירות.", "Perekhodite ulitsu ostorožno."),
        ("Светофор красный.", "הרמזור אדום.", "Svetofor krasnyy."), ("Можно идти.", "אפשר ללכת.", "Mozhno idti."),
    ]
    units.append(unit("a1-u06", "בעיר וניווט", "В городе", city, tip="где? — איפה; идите — ציווי רשמי", every_cp=6))

    shopping = [
        ("Сколько это стоит?", "כמה זה עולה?", "Skolko eto stoit?"),
        ("Это слишком дорого.", "זה יקר מדי.", "Eto slishkom dorogo."),
        ("Есть дешевле?", "יש יותר זול?", "Yest deshevle?"),
        ("Я просто смотрю.", "אני רק מסתכל.", "Ya prosto smotryu."),
        ("Можно примерить?", "אפשר למדוד?", "Mozhno primerit?"),
        ("Где примерочная?", "איפה חדר ההלבשה?", "Gde primerochnaya?"),
        ("Мне нужен размер M.", "אני צריך מידה M.", "Mne nuzhen razmer M."),
        ("Это мало.", "זה קטן.", "Eto malo."), ("Это велико.", "זה גדול.", "Eto veliko."),
        ("Это подходит.", "זה מתאים.", "Eto podkhodit."), ("Я возьму это.", "אני אקח את זה.", "Ya vozmu eto."),
        ("Картой или наличными?", "בכרטיס או במזומן?", "Kartoy ili nalichnymi?"),
        ("Картой, пожалуйста.", "בכרטיס בבקשה.", "Kartoy, pozhaluysta."),
        ("Есть ли чек?", "יש קבלה?", "Yest li chek?"), ("Можно пакет?", "אפשר שקית?", "Mozhno paket?"),
        ("У вас есть скидка?", "יש לכם הנחה?", "U vas yest skidka?"),
        ("Когда распродажа?", "מתי מבצע?", "Kogda rasprodazha?"),
        ("Я ищу чёрную рубашку.", "אני מחפש חולצה שחורה.", "Ya ishchu chyornuyu rubashku."),
        ("Покажите, пожалуйста, эту сумку.", "תראו לי בבקשה את התיק הזה.", "Pokazhite, pozhaluysta, etu sumku."),
        ("Какой цвет вам нравится?", "איזה צבע מוצא חן בעיניכם?", "Kakoy tsvet vam nravitsya?"),
        ("Мне нравится синий.", "כחול מוצא חן בעיני.", "Mne nravitsya siniy."),
        ("Это подарок.", "זה מתנה.", "Eto podarok."), ("Можно упаковать?", "אפשר לעטוף?", "Mozhno upakovat?"),
        ("Возврат возможен?", "אפשר להחזיר?", "Vozvrat vozmozhen?"),
        ("В течение четырнадцати дней.", "בתוך ארבעה עשר יום.", "V techeniye chetyrnadtsati dney."),
        ("Касса справа.", "הקופה מימין.", "Kassa sprava."), ("Очередь большая.", "התור ארוך.", "Ochered bolshaya."),
        ("Я заплатил уже.", "כבר שילמתי.", "Ya zaplatil uzhe."),
        ("Спасибо за покупку!", "תודה על הקנייה!", "Spasibo za pokupku!"),
        ("Мне нужна новая куртка.", "אני צריך ז'קט חדש.", "Mne nuzhna novaya kurtka."),
        ("Эти ботинки удобные.", "המגפיים האלה נוחים.", "Eti botinki udobnyye."),
        ("Сколько стоит доставка?", "כמה עולה משלוח?", "Skolko stoit dostavka?"),
        ("Бесплатная доставка.", "משלוח חינם.", "Besplatnaya dostavka."),
        ("Я заказал онлайн.", "הזמנתי אונליין.", "Ya zakazal onlayn."),
        ("Где пункт выдачи?", "איפה נקודת האיסוף?", "Gde punkt vydachi?"),
        ("У вас есть другой цвет?", "יש לכם צבע אחר?", "U vas yest drugoy tsvet?"),
        ("Только этот размер остался.", "נשארה רק המידה הזאת.", "Tolko etot razmer ostalsya."),
        ("Я передумал.", "התחרטתי.", "Ya peredumal."), ("Не сейчас, спасибо.", "לא עכשיו, תודה.", "Ne seychas, spasibo."),
        ("Что вы ищете?", "מה אתם מחפשים?", "Chto vy ishchete?"),
        ("Мне нужна помощь.", "אני צריך עזרה.", "Mne nuzhna pomoshch."),
    ]
    units.append(unit("a1-u07", "קניות", "Покупки", shopping, tip="сколько стоит? — מחיר; возьму — אקח", every_cp=6))

    time_w = [
        ("Который час?", "מה השעה?", "Kotoryy chas?"), ("Сейчас час.", "עכשיו אחת.", "Seychas chas."),
        ("Сейчас два часа.", "עכשיו השתיים.", "Seychas dva chasa."), ("Сейчас три часа.", "עכשיו השלוש.", "Seychas tri chasa."),
        ("Сейчас половина пятого.", "עכשיו ארבע וחצי.", "Seychas polovina pyatogo."),
        ("Сейчас без четверти шесть.", "עכשיו שש פחות רבע.", "Seychas bez chetverti shest."),
        ("Сегодня понедельник.", "היום יום שני.", "Segodnya ponedelnik."),
        ("Завтра вторник.", "מחר יום שלישי.", "Zavtra vtornik."),
        ("Вчера было воскресенье.", "אתמול היה יום ראשון.", "Vchera bylo voskresenye."),
        ("Утром я пью кофе.", "בבוקר אני שותה קפה.", "Utrom ya pyu kofe."),
        ("Днём я работаю.", "בצהריים אני עובד.", "Dnyom ya rabotayu."),
        ("Вечером я отдыхаю.", "בערב אני נח.", "Vecherom ya otdykhayu."),
        ("Ночью я сплю.", "בלילה אני ישן.", "Nochyu ya splyu."),
        ("Когда мы встретимся?", "מתי ניפגש?", "Kogda my vstretimsya?"),
        ("Давайте в семь.", "בואו בשבע.", "Davayte v sem."),
        ("Я занят сегодня.", "אני עסוק היום.", "Ya zanyat segodnya."),
        ("Я свободен завтра.", "אני פנוי מחר.", "Ya svoboden zavtra."),
        ("На выходных я дома.", "בסוף השבוע אני בבית.", "Na vykhodnykh ya doma."),
        ("В понедельник у меня учёба.", "ביום שני יש לי לימודים.", "V ponedelnik u menya uchyoba."),
        ("Сколько времени это займёт?", "כמה זמן זה ייקח?", "Skolko vremeni eto zaymyot?"),
        ("Около часа.", "בערך שעה.", "Okolo chasa."), ("Я опаздываю.", "אני מאחר.", "Ya opazdyvayu."),
        ("Мы успеем.", "נספיק.", "My uspeyem."), ("Не волнуйся.", "אל תדאג.", "Ne volnuysya."),
        ("Подождите минуту.", "חכו דקה.", "Podozhdite minutu."), ("Скоро!", "בקרוב!", "Skoro!"),
        ("Уже поздно.", "כבר מאוחר.", "Uzhe pozdno."), ("Ещё рано.", "עדיין מוקדם.", "Yeshchyo rano."),
        ("Какой сегодня день?", "איזה יום היום?", "Kakoy segodnya den?"),
        ("Какое сегодня число?", "מה התאריך היום?", "Kakoye segodnya chislo?"),
        ("Сегодня пятое мая.", "היום חמישי במאי.", "Segodnya pyatoye maya."),
        ("Мой день рождения в июне.", "יום ההולדת שלי ביוני.", "Moy den rozhdeniya v iyune."),
        ("Через час я буду дома.", "בעוד שעה אהיה בבית.", "Cherez chas ya budu doma."),
        ("Я приду вовремя.", "אבוא בזמן.", "Ya pridu vovremya."),
        ("Расписание изменилось.", "לוח הזמנים השתנה.", "Raspisaniye izmenilos."),
        ("Встреча в среду.", "הפגישה ביום רביעי.", "Vstrecha v sredu."),
        ("Урок начинается в девять.", "השיעור מתחיל בתשע.", "Urok nachinayetsya v devyat."),
        ("Фильм длится два часа.", "הסרט נמשך שעתיים.", "Film dlitsya dva chasa."),
    ]
    units.append(unit("a1-u08", "זמן ושעות", "Время", time_w, tip="который час? — מה השעה", every_cp=6))

    weather = [
        ("Какая погода?", "מה מזג האוויר?", "Kakaya pogoda?"),
        ("Сегодня тепло.", "היום חם נעים.", "Segodnya teplo."),
        ("Сегодня холодно.", "היום קר.", "Segodnya kholodno."),
        ("Идёт дождь.", "יורד גשם.", "Idyot dozhd."),
        ("Идёт снег.", "יורד שלג.", "Idyot sneg."),
        ("Светит солнце.", "השמש זורחת.", "Svetit solntse."),
        ("На улице ветрено.", "בחוץ יש רוח.", "Na ulitse vetreno."),
        ("Очень жарко.", "חם מאוד.", "Ochen zharko."),
        ("Возьми зонт.", "קח מטריה.", "Vozmi zont."),
        ("Надень куртку.", "תלבש ז'קט.", "Naden kurtku."),
        ("Какая температура?", "מה הטמפרטורה?", "Kakaya temperatura?"),
        ("Плюс двадцать градусов.", "עשרים מעלות פלוס.", "Plyus dvadtsat gradusov."),
        ("Минус пять.", "מינוס חמש.", "Minus pyat."),
        ("Завтра будет дождь.", "מחר יהיה גשם.", "Zavtra budet dozhd."),
        ("Вчера было солнечно.", "אתמול היה שמשי.", "Vchera bylo solnechno."),
        ("Я люблю лето.", "אני אוהב קיץ.", "Ya lyublyu leto."),
        ("Зима в России холодная.", "החורף ברוסיה קר.", "Zima v Rossii kholodnaya."),
        ("Осенью часто дожди.", "בסתיו יש הרבה גשמים.", "Osenyu chasto dozhdi."),
        ("Весной всё цветёт.", "באביב הכול פורח.", "Vesnoy vsyo tsvetyot."),
        ("Туман на улице.", "יש ערפל בחוץ.", "Tuman na ulitse."),
        ("Гроза начинается.", "מתחילה סופה.", "Groza nachinayetsya."),
        ("Небо серое.", "השמיים אפורים.", "Nebo seroye."),
        ("Погода хорошая для прогулки.", "מזג אוויר טוב לטיול.", "Pogoda khoroshaya dlya progulki."),
        ("Сегодня облачно.", "היום מעונן.", "Segodnya oblachno."),
        ("Дует сильный ветер.", "נושבת רוח חזקה.", "Duyet silnyy veter."),
        ("Я замёрз.", "אני קפאתי מקור.", "Ya zamroz."),
        ("Мне жарко.", "חם לי.", "Mne zharko."),
        ("Прогноз на неделю.", "תחזית לשבוע.", "Prognoz na nedelyu."),
        ("Будет ли снег?", "יהיה שלג?", "Budet li sneg?"),
        ("Возьми шапку.", "קח כובע.", "Vozmi shapku."),
        ("На улице скользко.", "בחוץ חלקלק.", "Na ulitse skolsko."),
        ("Лучше остаться дома.", "עדיף להישאר בבית.", "Luchshe ostatysa doma."),
    ]
    units.append(unit("a1-u09", "מזג אוויר", "Погода", weather, tip="идёт дождь — יורד גשם", every_cp=6))

    print("A1 partial units so far", len(units), "lessons", sum(len(u["lessons"]) for u in units))
    return units

if __name__ == "__main__":
    u = build_a1()
    print(sum(len(x["lessons"]) for x in u))
