# -*- coding: utf-8 -*-
"""
Created on Sat Dec 30 21:48:57 2023

@author: NASUS
"""

import sys
from pynput.mouse import Listener, Button
import pyautogui as pya
import pyperclip
import time
from PyQt5.QtWidgets import (
    QApplication,
    QWidget,
    QVBoxLayout,
    QListWidget,
    QPushButton,
    QLabel,
    QCheckBox,
)
from PyQt5.QtCore import Qt  # Import the Qt module
from threading import Thread

# from translate import Translator
from googletrans import Translator


class MyWidget(QWidget):
    def __init__(self):
        super().__init__()

        self.text_list = []
        self.listener_stop_flag = False  # Flag to stop the listener thread
        self.is_online = True  # Default is online mode
        self.error_label = QLabel(self)
        self.initUI()

    def initUI(self):
        layout = QVBoxLayout()

        # Add the error label to the interface
        layout.addWidget(self.error_label)

        # Add a checkbox for online/offline mode
        online_checkbox = QCheckBox("Online Mode", self)
        online_checkbox.setChecked(True)
        online_checkbox.stateChanged.connect(self.toggle_online_mode)
        layout.addWidget(online_checkbox)

        # Create a QListWidget and add items from text_list
        self.list_widget = QListWidget(self)
        self.list_widget.addItems(self.text_list)

        # Set the fixed size for self.list_widget
        self.list_widget.setFixedSize(300, 50)

        # Add the list to the interface
        layout.addWidget(self.list_widget)

        # Create a button named "Clear List"
        clear_button = QPushButton("Clear List", self)
        clear_button.clicked.connect(self.clearList)

        # Add the button to the interface
        layout.addWidget(clear_button)

        # Create a QLabel for displaying Turkish translation
        self.turkish_translation_label = QLabel(self)
        layout.addWidget(self.turkish_translation_label)

        # Apply the layout to the interface
        self.setLayout(layout)

        # Set the window title
        self.setWindowTitle("Text List Interface")

        # # Set the fixed size of the window
        # self.setFixedSize(310, 100)

        # Make the window stay on top of other windows
        self.setWindowFlags(self.windowFlags() | Qt.WindowStaysOnTopHint)

        # Close the application when the window is closed
        self.setAttribute(Qt.WA_QuitOnClose)

    def toggle_online_mode(self, state):
        self.is_online = state == Qt.Checked

        if not self.is_online:
            self.error_label.setText("")

    def check_word_in_file(self, word, file_path):
        with open(file_path, "r", encoding="utf-8") as file:
            words = file.read().split()
            return word in words

    def clearList(self):
        # Clear the list and update the interface
        self.text_list.clear()
        self.list_widget.clear()
        self.turkish_translation_label.clear()

    def closeEvent(self, event):
        self.listener_stop_flag = True  # İş parçacığını durdurmak için bayrağı ayarla
        if self.listener_thread_instance.is_alive():
            self.listener_thread_instance.join()  # İş parçacığının bitmesini bekle
        event.accept()  # Uygulamayı kapat


def copy_clipboard():
    pya.hotkey("ctrl", "c")
    time.sleep(0.1)
    return pyperclip.paste()


def double_click_and_copy():
    copied_text = copy_clipboard()
    return copied_text


def translate_to_turkish(word):
    translator = Translator()
    translation = translator.translate(word, src="en", dest="tr")
    return translation.text


def add_to_list(window):
    time.sleep(1)
    clicked_text = double_click_and_copy()

    if not clicked_text.strip():
        return
    try:
        window.error_label.setText("")
        turkish_translation = translate_to_turkish(clicked_text)

        # Clear previous items in the list and widget
        window.text_list.clear()
        window.list_widget.clear()

        # Add the last clicked word and translation to the list and widget
        window.text_list.append(clicked_text)
        window.list_widget.addItem(clicked_text)

        # Show the Turkish translation
        window.turkish_translation_label.setText(
            f"Turkish Translation: {turkish_translation}"
        )

        # Print the last clicked word and translation
        # print(clicked_text, "->", turkish_translation)

        pyperclip.copy("")

    except Exception as e:
        window.error_label.setText(f"An error occurred: {str(e)}")


def check_word_in_file(clicked_text):
    clicked_text = clicked_text.lower()  # Kelimeyi küçük harflere dönüştür
    window.error_label.setText("")
    # Offline kelime listesi
    offline_words = [
        "ability:yetenek",
        "able:hünerli",
        "about:hakkında",
        "above:üstünde",
        "accept:kabuletmek",
        "according:binaen",
        "account:hesap",
        "across:karşısında",
        "act:davranmak",
        "action:aksiyon",
        "activity:aktivite",
        "actually:Aslında",
        "add:eklemek",
        "address:adres",
        "administration:yönetim",
        "admit:itirafetmek",
        "adult:yetişkin",
        "affect:etkilemek",
        "after:sonrasında",
        "again:Tekrar",
        "against:aykırı",
        "age:yaş",
        "agency:Ajans",
        "agent:ajan",
        "ago:evvel",
        "agree:kabuletmek",
        "agreement:anlaşma",
        "ahead:ilerde",
        "air:hava",
        "all:Tümü",
        "allow:izinvermek",
        "almost:neredeyse",
        "alone:yalnız",
        "along:birlikte",
        "already:çoktan",
        "also:Ayrıca",
        "although:rağmen",
        "always:Herzaman",
        "American:Amerikan",
        "among:arasında",
        "amount:miktar",
        "analysis:analiz",
        "and:Ve",
        "animal:hayvan",
        "another:birdiğer",
        "answer:cevap",
        "any:herhangi",
        "anyone:herhangibiri",
        "anything:herhangibirşey",
        "appear:belliolmak",
        "apply:uygula",
        "approach:yaklaşmak",
        "area:alan",
        "argue:tartışmak",
        "arm:kol",
        "around:etrafında",
        "arrive:varmak",
        "art:sanat",
        "article:madde",
        "artist:sanatçı",
        "as:gibi",
        "ask:sormak",
        "assume:farzetmek",
        "at:-den",
        "attack:saldırı",
        "attention:dikkat",
        "attorney:avukat",
        "audience:kitle",
        "author:yazar",
        "authority:yetki",
        "available:mevcut",
        "avoid:kaçınmak",
        "away:uzak",
        "baby:Bebek",
        "back:geri",
        "bad:kötü",
        "bag:çanta",
        "ball:top",
        "bank:banka",
        "bar:çubuk",
        "base:temel",
        "be:olmak",
        "beat:vurmak",
        "beautiful:Güzel",
        "because:Çünkü",
        "become:halinegelmek",
        "bed:yatak",
        "before:önce",
        "begin:başlamak",
        "behavior:davranış",
        "behind:arka",
        "believe:inanmak",
        "benefit:fayda",
        "best:eniyi",
        "better:dahaiyi",
        "between:arasında",
        "beyond:öte",
        "big:büyük",
        "bill:fatura",
        "billion:milyar",
        "bit:biraz",
        "black:siyah",
        "blood:kan",
        "blue:mavi",
        "board:pano",
        "body:vücut",
        "book:kitap",
        "born:doğmak",
        "both:ikisibirden",
        "box:kutu",
        "boy:erkekçocuk",
        "break:kırmak",
        "bring:getirmek",
        "brother:Erkekkardeş",
        "budget:bütçe",
        "build:inşaetmek",
        "building:bina",
        "business:işletme",
        "but:Ancak",
        "buy:satınalmak",
        "by:ile",
        "call:Arama",
        "camera:kamera",
        "campaign:kampanya",
        "can:olabilmek",
        "cancer:kanser",
        "candidate:aday",
        "capital:başkent",
        "car:araba",
        "card:kart",
        "care:bakım",
        "career:kariyer",
        "carry:taşımak",
        "case:dava",
        "catch:yakalamak",
        "cause:neden",
        "cell:hücre",
        "center:merkez",
        "central:merkezi",
        "century:yüzyıl",
        "certain:kesin",
        "certainly:kesinlikle",
        "chair:sandalye",
        "challenge:meydanokumak",
        "chance:şans",
        "change:değiştirmek",
        "character:karakter",
        "charge:şarj",
        "check:kontroletmek",
        "child:çocuk",
        "choice:seçenek",
        "choose:seçmek",
        "church:kilise",
        "citizen:vatandaş",
        "city:şehir",
        "civil:sivil",
        "claim:iddia",
        "class:sınıf",
        "clear:temizlemek",
        "clearly:Açıkça",
        "close:kapalı",
        "coach:koç",
        "cold:soğuk",
        "collection:Toplamak",
        "college:kolej",
        "color:renk",
        "come:Gelmek",
        "commercial:reklam",
        "common:yaygın",
        "community:toplum",
        "company:şirket",
        "compare:karşılaştırmak",
        "computer:bilgisayar",
        "concern:kaygı",
        "condition:durum",
        "conference:konferans",
        "Congress:Kongre",
        "consider:dikkatealmak",
        "consumer:tüketici",
        "contain:içermek",
        "continue:devametmek",
        "control:kontrol",
        "cost:maliyet",
        "could:abilir",
        "country:ülke",
        "couple:çift",
        "course:kurs",
        "court:mahkeme",
        "cover:kapak",
        "create:yaratmak",
        "crime:suç",
        "cultural:kültürel",
        "culture:kültür",
        "cup:bardak",
        "current:akım",
        "customer:müşteri",
        "cut:kesmek",
        "dark:karanlık",
        "data:veri",
        "daughter:kızçocuğu",
        "day:gün",
        "dead:ölü",
        "deal:anlaşmak",
        "death:ölüm",
        "debate:çekişme",
        "decade:onyıl",
        "decide:kararvermek",
        "decision:karar",
        "deep:derin",
        "defense:savunma",
        "degree:derece",
        "Democrat:Demokrat",
        "democratic:demokratik",
        "describe:betimlemek",
        "design:tasarım",
        "despite:aksine",
        "detail:detay",
        "determine:belirlemek",
        "develop:geliştirmek",
        "development:gelişim",
        "die:ölmek",
        "difference:fark",
        "different:farklı",
        "difficult:zor",
        "dinner:akşamyemeği",
        "direction:yön",
        "director:müdür",
        "discover:keşfetmek",
        "discuss:tartışmak",
        "discussion:tartışma",
        "disease:hastalık",
        "do:Yapmak",
        "doctor:doktor",
        "dog:köpek",
        "door:kapı",
        "down:aşağı",
        "draw:çizmek",
        "dream:rüya",
        "drive:sürmek",
        "drop:düşürmek",
        "drug:ilaç",
        "during:sırasında",
        "each:herbiri",
        "early:erken",
        "east:doğu",
        "easy:kolay",
        "eat:yemekyemek",
        "economic:ekonomik",
        "economy:ekonomi",
        "edge:kenar",
        "education:eğitim",
        "effect:etki",
        "effort:çaba",
        "eight:sekiz",
        "either:herhangibiri",
        "election:seçim",
        "else:başka",
        "employee:çalışan",
        "end:son",
        "energy:enerji",
        "enjoy:Eğlence",
        "enough:yeterli",
        "enter:girmek",
        "entire:bütün",
        "environment:çevre",
        "environmental:çevre",
        "especially:özellikle",
        "establish:kurmak",
        "even:eşit",
        "evening:akşam",
        "event:etkinlik",
        "ever:durmadan",
        "every:Her",
        "everybody:herkes",
        "everyone:herkes",
        "everything:herşey",
        "evidence:kanıt",
        "exactly:Kesinlikle",
        "example:örnek",
        "executive:yönetici",
        "exist:varolmak",
        "expect:beklemek",
        "experience:deneyim",
        "expert:uzman",
        "explain:açıklamak",
        "eye:göz",
        "face:yüz",
        "fact:hakikat",
        "factor:faktör",
        "fail:hata",
        "fall:düşmek",
        "family:aile",
        "far:uzak",
        "fast:hızlı",
        "father:baba",
        "fear:korku",
        "federal:federal",
        "feel:hissetmek",
        "feeling:his",
        "few:birkaç",
        "field:alan",
        "fight:kavga",
        "figure:figür",
        "fill:doldurmak",
        "film:film",
        "final:son",
        "finally:Sonunda",
        "financial:parasal",
        "find:bulmak",
        "fine:iyi",
        "finger:parmak",
        "finish:sonaermek",
        "fire:ateş",
        "firm:firma",
        "first:Birinci",
        "fish:balık",
        "five:beş",
        "floor:zemin",
        "fly:uçmak",
        "focus:odak",
        "follow:takipetmek",
        "food:yiyecek",
        "foot:ayak",
        "for:için",
        "force:güç",
        "foreign:yabancı",
        "forget:unutmak",
        "form:biçim",
        "former:önceki",
        "forward:ileri",
        "four:dört",
        "free:özgür",
        "friend:arkadaş",
        "from:itibaren",
        "front:ön",
        "full:tamdolu",
        "fund:fon,sermaye",
        "future:gelecek",
        "game:oyun",
        "garden:bahçe",
        "gas:gaz",
        "general:genel",
        "generation:nesil",
        "get:eldeetmek",
        "girl:kız",
        "give:vermek",
        "glass:bardak",
        "go:Gitmek",
        "goal:amaç",
        "good:iyi",
        "government:devlet",
        "great:Harika",
        "green:yeşil",
        "ground:zemin",
        "group:grup",
        "grow:büyümek",
        "growth:büyüme",
        "guess:tahminetmek",
        "gun:silah",
        "guy:adam",
        "hair:saç",
        "half:yarım",
        "hand:el",
        "hang:asmak",
        "happen:olmak",
        "happy:mutlu",
        "hard:zor",
        "have:sahipolmak",
        "he:O",
        "head:KAFA",
        "health:sağlık",
        "hear:duymak",
        "heart:kalp",
        "heat:sıcaklık",
        "heavy:ağır",
        "help:yardım",
        "her:o",
        "here:Burada",
        "herself:kendini",
        "high:yüksek",
        "him:o",
        "himself:kendisi",
        "his:onun",
        "history:tarih",
        "hit:vurmak",
        "hold:tutmak",
        "home:Ev",
        "hope:umut",
        "hospital:hastane",
        "hot:sıcak",
        "hotel:otel",
        "hour:saat",
        "house:ev",
        "how:Nasıl",
        "however:Yinede",
        "huge:büyük",
        "human:insan",
        "hundred:yüz",
        "husband:koca",
        "I:BEN",
        "idea:fikir",
        "identify:tanımlamak",
        "if:eğer",
        "image:imaj",
        "imagine:hayaletmek",
        "impact:darbe",
        "important:önemli",
        "improve:geliştirmek",
        "in:içinde",
        "include:katmak",
        "including:içermek",
        "increase:arttırmak",
        "indeed:Aslında",
        "indicate:belirtmek",
        "individual:bireysel",
        "industry:sanayi",
        "information:bilgi",
        "inside:içeri",
        "instead:yerine",
        "institution:kurum",
        "interest:faiz",
        "interesting:ilginç",
        "international:uluslararası",
        "interview:röportaj",
        "into:içine",
        "investment:yatırım",
        "involve:içermek",
        "issue:sorun",
        "it:BT",
        "item:öğe",
        "its:onun",
        "itself:kendisi",
        "job:iş",
        "join:katılmak",
        "just:Sadece",
        "keep:kale",
        "key:anahtar",
        "kid:çocuk",
        "kill:öldürmek",
        "kind:tür",
        "kitchen:mutfak",
        "know:Bilmek",
        "knowledge:bilgi",
        "land:kara",
        "language:dil",
        "large:büyük",
        "last:son",
        "late:geç",
        "later:Dahasonra",
        "laugh:gülmek",
        "law:kanun",
        "lawyer:avukat",
        "lay:sermek",
        "lead:yolgöstermek",
        "leader:Önder",
        "learn:öğrenmek",
        "least:enaz",
        "leave:ayrılmak",
        "left:sol",
        "leg:bacak",
        "legal:yasal",
        "less:az",
        "let:izinvermek",
        "letter:mektup",
        "level:seviyesi",
        "lie:yalan",
        "life:hayat",
        "light:ışık",
        "like:beğenmek",
        "likely:büyükihtimalle",
        "line:astar",
        "list:liste",
        "listen:Dinlemek",
        "little:biraz",
        "live:canlı",
        "local:yerel",
        "long:uzun",
        "look:Bakmak",
        "lose:kaybetmek",
        "loss:kayıp",
        "lot:pay",
        "love:Aşk",
        "low:Düşük",
        "machine:makine",
        "magazine:dergi",
        "main:ana",
        "maintain:sürdürmek",
        "major:ana",
        "majority:çoğunluk",
        "make:yapmak",
        "man:Adam",
        "manage:üstesindengelmek",
        "management:yönetmek",
        "manager:müdür",
        "many:birçok",
        "market:pazar",
        "marriage:evlilik",
        "material:malzeme",
        "matter:konu",
        "may:mayıs",
        "maybe:Belki",
        "me:Ben",
        "mean:Anlam",
        "measure:ölçüm",
        "media:medya",
        "medical:tıbbi",
        "meet:tanışmak",
        "meeting:toplantı",
        "member:üye",
        "memory:hafıza",
        "mention:değinmek",
        "message:İleti",
        "method:yöntem",
        "middle:orta",
        "might:belki",
        "military:askeri",
        "million:milyon",
        "mind:akıl",
        "minute:dakika",
        "miss:kayıp",
        "mission:misyon",
        "model:model",
        "modern:modern",
        "moment:an",
        "money:para",
        "month:ay",
        "more:Daha",
        "morning:Sabah",
        "most:en",
        "mother:anne",
        "mouth:ağız",
        "move:taşınmak",
        "movement:hareket",
        "movie:film",
        "Mr:Bay",
        "Mrs:Bayan",
        "much:fazla",
        "music:müzik",
        "must:mutlak",
        "my:Benim",
        "myself:kendim",
        "name:isim",
        "nation:ulus",
        "national:ulusal",
        "natural:doğal",
        "nature:doğa",
        "nasuhcan:Harika bir mühendis",
        "near:yakın",
        "nearly:neredeyse",
        "necessary:gerekli",
        "need:ihtiyaç",
        "network:ağ",
        "never:Asla",
        "new:yeni",
        "news:haberler",
        "newspaper:gazete",
        "next:Sonraki",
        "nice:Güzel",
        "night:gece",
        "no:HAYIR",
        "none:hiçbiri",
        "nor:ne",
        "north:kuzey",
        "not:Olumsuz",
        "note:Not",
        "nothing:Hiçbirşey",
        "notice:farketme",
        "now:Şimdi",
        "n't:değil",
        "number:sayı",
        "occur:meydanagelmek",
        "of:ileilgili",
        "off:kapalı",
        "offer:teklif",
        "office:ofis",
        "officer:subay",
        "official:resmi",
        "often:sıklıkla",
        "oh:ah",
        "oil:yağ",
        "ok:Tamam",
        "old:eskimiş",
        "on:Açık",
        "once:birkere",
        "one:bir",
        "only:sadece",
        "onto:üzerine",
        "open:açık",
        "operation:operasyon",
        "opportunity:fırsat",
        "option:seçenek",
        "or:veya",
        "order:emir",
        "organization:organizasyon",
        "other:diğer",
        "others:diğerleri",
        "our:bizim",
        "out:dışarı",
        "outside:dıştan",
        "over:üzerinde",
        "own:sahipolmak",
        "owner:malsahibi",
        "page:sayfa",
        "pain:ağrı",
        "painting:tablo",
        "paper:kağıt",
        "parent:ebeveyn",
        "part:parça",
        "participant:katılımcı",
        "particular:özel",
        "particularly:özellikle",
        "partner:ortak",
        "party:Parti",
        "pass:geçmek",
        "past:geçmiş",
        "patient:hasta",
        "pattern:model",
        "pay:ödemek",
        "peace:barış",
        "people:insanlar",
        "per:başına",
        "perform:rolyapmak",
        "performance:verim",
        "perhaps:belki",
        "period:dönem",
        "person:kişi",
        "personal:kişisel",
        "phone:telefon",
        "physical:fiziksel",
        "pick:seçmek",
        "picture:resim",
        "piece:parça",
        "place:yer",
        "plan:plan",
        "plant:bitki",
        "play:oynamak",
        "player:oyuncu",
        "PM:ÖĞLEDENSONRA",
        "point:nokta",
        "police:polis",
        "policy:politika",
        "political:siyasi",
        "politics:siyaset",
        "poor:fakir",
        "popular:popüler",
        "population:nüfus",
        "position:konum",
        "positive:pozitif",
        "possible:olası",
        "power:güç",
        "practice:pratik",
        "prepare:hazırlanmak",
        "present:Sunmak",
        "president:başkan",
        "pressure:basınç",
        "pretty:tatlı",
        "prevent:önlemek",
        "price:fiyat",
        "private:özel",
        "probably:muhtemelen",
        "problem:sorun",
        "process:işlem",
        "produce:üretmek",
        "product:ürün",
        "production:üretme",
        "professional:profesyonel",
        "professor:profesör",
        "program:program",
        "project:proje",
        "property:mülk",
        "protect:korumak",
        "prove:kanıtlamak",
        "provide:sağlamak",
        "public:halk",
        "pull:çekmek",
        "purpose:amaç",
        "push:itmek",
        "put:koymak",
        "quality:kalite",
        "question:soru",
        "quickly:hızlıca",
        "quite:epeyce",
        "race:ırk",
        "radio:radyo",
        "raise:artırmak",
        "range:menzil",
        "rate:oran",
        "rather:yerine",
        "reach:ulaşmak",
        "read:Okumak",
        "ready:hazır",
        "real:gerçek",
        "reality:gerçeklik",
        "realize:farketmek",
        "really:Gerçekten",
        "reason:sebep",
        "receive:almak",
        "recent:son",
        "recently:sonzamanlarda",
        "recognize:tanımak",
        "record:kayıt",
        "red:kırmızı",
        "reduce:azaltmak",
        "reflect:yansıtmak",
        "region:bölge",
        "relate:ilgiliolmak",
        "relationship:ilişki",
        "religious:din",
        "remain:geriyekalmak",
        "remember:Unutma",
        "remove:kaldırmak",
        "report:rapor",
        "represent:temsiletmek",
        "Republican:Cumhuriyetçi",
        "require:gerekmek",
        "research:araştırma",
        "resource:kaynak",
        "respond:yanıtlamak",
        "response:cevap",
        "responsibility:sorumluluk",
        "rest:dinlenmek",
        "result:sonuç",
        "return:geridönmek",
        "reveal:ortayaçıkarmak",
        "rich:zengin",
        "right:Sağ",
        "rise:yükselmek",
        "risk:risk",
        "road:yol",
        "rock:kaynak",
        "role:rol",
        "room:oda",
        "rule:kural",
        "run:koşmak",
        "safe:güvenli",
        "same:Aynı",
        "save:kaydetmek",
        "say:söylemek",
        "scene:sahne",
        "school:okul",
        "science:bilim",
        "scientist:bilimadamı",
        "score:Gol",
        "sea:deniz",
        "season:mevsim",
        "seat:koltuk",
        "second:ikinci",
        "section:bölüm",
        "security:güvenlik",
        "see:Görmek",
        "seek:aramak",
        "seem:gözükmek",
        "sell:satmak",
        "send:Göndermek",
        "senior:kıdemli",
        "sense:algı",
        "series:seri",
        "serious:cidden",
        "serve:sert",
        "service:hizmet",
        "set:ayarlamak",
        "seven:Yedi",
        "several:birçok",
        "sex:seks",
        "sexual:cinsel",
        "shake:sallamak",
        "share:paylaşmak",
        "she:o",
        "shoot:filmçekmek",
        "short:kısa",
        "shot:atış",
        "should:meli",
        "shoulder:omuz",
        "show:göstermek",
        "side:taraf",
        "sign:imza",
        "significant:önemli",
        "similar:benzer",
        "simple:basit",
        "simply:basitçe",
        "since:ozamandanberi",
        "sing:şarkısöylemek",
        "single:Bekar",
        "sister:kızkardeş",
        "sit:oturmak",
        "site:alan",
        "situation:durum",
        "six:altı",
        "size:boyut",
        "skill:yetenek",
        "skin:deri",
        "small:küçük",
        "smile:gülümsemek",
        "so:Buyüzden",
        "social:sosyal",
        "society:toplum",
        "soldier:asker",
        "some:bazı",
        "somebody:biri",
        "someone:birisi",
        "something:birşey",
        "sometimes:Bazen",
        "son:oğul",
        "song:şarkı",
        "soon:yakında",
        "sort:düzenlemek",
        "sound:ses",
        "source:kaynak",
        "south:güney",
        "southern:güney",
        "space:uzay",
        "speak:konuşmak",
        "special:özel",
        "specific:özel",
        "speech:konuşma",
        "spend:harcamak",
        "sport:spor",
        "spring:bahar",
        "staff:kadro",
        "stage:sahne",
        "stand:durmak",
        "standard:standart",
        "star:yıldız",
        "window:pencere",
        "word:kelime",
        "words:kelimeler",
        "file:dosya",
        "self:kendikendine",
        "hello:selam",
        "hi:selam",
    ]  

    for item in offline_words:
        eng, tr = item.split(":")
        if eng == clicked_text:
            window.list_widget.clear()
            window.turkish_translation_label.clear()
            window.turkish_translation_label.setText(f"Turkish Translation: {tr}")
            return tr

    return False


last_click_time = 0


def on_click(x, y, button, pressed, window):
    global last_click_time
    if window.listener_stop_flag:
        return  # Stop the listener if the flag is set
    if button == Button.left and pressed:
        current_time = time.time()
        if current_time - last_click_time <= 0.5:
            if not window.is_online:
                time.sleep(1)
                clicked_text = double_click_and_copy()
                if check_word_in_file(clicked_text):
                    # print(f"Word found offline: {clicked_text}")
                    window.list_widget.clear()
                    window.list_widget.addItem(f"Word found offline: {clicked_text}")
                else:
                    # print("Word not found offline")
                    window.list_widget.clear()
                    window.turkish_translation_label.clear()
                    window.list_widget.addItem("Word not found offline")
            else:
                add_to_list(window)
        last_click_time = current_time


def listener_thread(window):
    with Listener(
        on_click=lambda x, y, button, pressed: on_click(x, y, button, pressed, window)
    ) as listener:
        listener.join()


if __name__ == "__main__":
    app = QApplication([])

    # Create the PyQt5 window
    window = MyWidget()

    # Start the listener in a separate thread
    listener_thread_instance = Thread(target=listener_thread, args=(window,))
    listener_thread_instance.start()

    window.show()

    # Close the application when the window is closed
    sys.exit(app.exec_())
