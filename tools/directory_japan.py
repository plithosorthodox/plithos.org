#!/usr/bin/env python3
"""The parish-scale Japan branch of the Churches directory.

The Church of Japan publishes each body in its official directory under one
of its three dioceses. Parish rows live one diocese to a file and are fetched
only when a reader needs that branch.

    python tools/directory_japan.py --check
    python tools/directory_japan.py --write
"""

import argparse
import json
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "data" / "directory"
CHECKED = "2026-11-14"
CLERGY_WORDS = (
    "司祭", "神父", "府主教", "主教", "大主教", "修道司祭",
    "伝教者", "伝教生", "教役者",
)


ROWS = json.loads(r'''{
  "jp-tokyo": [
    {
      "id": "jp-tokyo-resurrection-cathedral",
      "parent": "jp-tokyo",
      "kind": "parish",
      "rank": "Cathedral",
      "name": "Tokyo Resurrection Cathedral",
      "local": "東京復活大聖堂",
      "country": "JP",
      "address": [
        "〒101-0062",
        "東京都千代田区神田駿河台4-1-3"
      ],
      "services": [
        "・主日徹夜祷",
        "土曜日午後5時",
        "・主日聖体礼儀",
        "日曜日午前10時",
        "その他詳細は大聖堂ホームページをご覧ください"
      ],
      "founded": [
        "修復がはじまるまえの準備の期間を入れるとおよそ9年が費やされて、輝けるばかりの姿となった。"
      ],
      "site": "http://nikolaido.org/",
      "sources": [
        "https://www.orthodoxjapan.jp/area-tokyo.html",
        "https://www.orthodoxjapan.jp/annai/t-tokyo.html",
        "http://nikolaido.org/"
      ]
    },
    {
      "id": "jp-suka-parish",
      "parent": "jp-tokyo",
      "kind": "parish",
      "rank": "Parish",
      "name": "Suka Orthodox Church",
      "local": "須賀ハリストス正教会",
      "country": "JP",
      "dedication": "生神女福音聖堂",
      "address": [
        "〒289-2133",
        "千葉県匝瑳市蕪里628-7"
      ],
      "services": [
        "・聖体礼儀",
        "毎月第三日曜日 10時"
      ],
      "sources": [
        "https://www.orthodoxjapan.jp/area-tokyo.html",
        "https://www.orthodoxjapan.jp/annai/t-suka.html"
      ]
    },
    {
      "id": "jp-tega-parish",
      "parent": "jp-tokyo",
      "kind": "parish",
      "rank": "Parish",
      "name": "Tega Orthodox Church",
      "local": "手賀ハリストス正教会",
      "country": "JP",
      "dedication": "聖使徒神学者・福音記者イオアン聖堂",
      "address": [
        "〒270-1465",
        "千葉県柏市手賀422"
      ],
      "services": [
        "・聖体礼儀",
        "毎月第3土曜日 午前10時",
        "（ただし変更の場合がありますので、ご参祷をお考えの場合は事前にお問い合わせください。）"
      ],
      "founded": [
        "1974年（昭49年）10月に成聖され、信徒戸数は約10戸。",
        "柏駅から車で約30分。"
      ],
      "sources": [
        "https://www.orthodoxjapan.jp/area-tokyo.html",
        "https://www.orthodoxjapan.jp/annai/t-tega.html"
      ]
    },
    {
      "id": "jp-yamate-parish",
      "parent": "jp-tokyo",
      "kind": "parish",
      "rank": "Parish",
      "name": "Yamate Orthodox Church",
      "local": "山手ハリストス正教会",
      "country": "JP",
      "dedication": "東京至聖三者聖堂",
      "address": [
        "〒168-0081",
        "東京都杉並区宮前3-28-10"
      ],
      "services": [
        "・ 徹夜祷",
        "土曜日 午後5時",
        "・主日聖体礼儀",
        "毎週日曜日 午前10時",
        "（第3土・日を除く）"
      ],
      "founded": [
        "明治14年に麹町に始まり、その後、四谷洗礼聖堂として親しまれた。",
        "戦災により聖堂は焼失したが、1955年に現在地に移り、民家を改装して山手ハリストス正教会・主の降誕聖堂と呼んだ。"
      ],
      "site": "http://orthodox1yamate.web.fc2.com/index.html",
      "sources": [
        "https://www.orthodoxjapan.jp/area-tokyo.html",
        "https://www.orthodoxjapan.jp/annai/t-yamate.html",
        "http://orthodox1yamate.web.fc2.com/index.html"
      ]
    },
    {
      "id": "jp-maebashi-parish",
      "parent": "jp-tokyo",
      "kind": "parish",
      "rank": "Parish",
      "name": "Maebashi Orthodox Church",
      "local": "前橋ハリストス正教会",
      "country": "JP",
      "dedication": "亜使徒大主教聖ニコライ聖堂",
      "address": [
        "〒371-0022",
        "群馬県前橋市千代田町1-4-22"
      ],
      "services": [
        "第一日曜日 10：00 聖体礼儀",
        "前日土曜日 16：00 前晩祷",
        "第三日曜日 10：00 聖体礼儀",
        "前日土曜日 16：00 前晩祷"
      ],
      "founded": [
        "前橋への伝道は1875(明治8)年に始まり、3年後にはマトフエイ丹波を中心にした士族によって教会が設立された。"
      ],
      "site": "https://ocj-maebashi9s0t8k.wixsite.com/maebashi-new-page",
      "sources": [
        "https://www.orthodoxjapan.jp/area-tokyo.html",
        "https://www.orthodoxjapan.jp/annai/t-maebashi.html",
        "https://ocj-maebashi9s0t8k.wixsite.com/maebashi-new-page"
      ]
    },
    {
      "id": "jp-sukawa-parish",
      "parent": "jp-tokyo",
      "kind": "parish",
      "rank": "Parish",
      "name": "Sukawa Orthodox Church",
      "local": "須川ハリストス正教会",
      "country": "JP",
      "dedication": "聖パンテレイモン聖堂",
      "address": [
        "〒379-1418",
        "群馬県利根郡みなかみ町須川771"
      ],
      "services": [
        "第一土曜日",
        "(4月から10月) 6:30",
        "(11月から3月) 7:00 聖体礼儀",
        "※第一土曜日が1日の場合は第二。",
        "前日金曜日",
        "(4月から10月) 17:30",
        "(11月から3月) 17:00 前晩祷"
      ],
      "founded": [
        "明治15年に前橋でワルワラの聖名で洗礼を受けた本田マサが須川教会最初の信徒である。",
        "須川の教会は明治18年から始まった伝道活動の実りとしてマカリイ森下、ステファン森下、ワシリイ梅澤、グリゴリイ小池、アントニイ小室の諸兄が洗礼を受けたことから始まる。"
      ],
      "sources": [
        "https://www.orthodoxjapan.jp/area-tokyo.html",
        "https://www.orthodoxjapan.jp/annai/t-sukawa.html"
      ]
    },
    {
      "id": "jp-takasaki-parish",
      "parent": "jp-tokyo",
      "kind": "parish",
      "rank": "Parish",
      "name": "Takasaki Orthodox Church",
      "local": "高崎ハリストス正教会",
      "country": "JP",
      "dedication": "主の降誕聖堂",
      "address": [
        "〒370-0074",
        "群馬県高崎市下小鳥町726-5"
      ],
      "services": [
        "第二日曜日 10：00 聖体礼儀",
        "第四日曜日 10：00 聖体礼儀",
        "前日土曜日 16：00 前晩祷  (前晩祷は第二のみ)"
      ],
      "founded": [
        "大正3年、初代の聖堂が市内の柳川町に建てられた。",
        "現在の聖堂は1963(昭和38)年に現地へ移転、再建されたもの。"
      ],
      "sources": [
        "https://www.orthodoxjapan.jp/area-tokyo.html",
        "https://www.orthodoxjapan.jp/annai/t-takasaki.html"
      ]
    },
    {
      "id": "jp-yokohama-parish",
      "parent": "jp-tokyo",
      "kind": "parish",
      "rank": "Parish",
      "name": "Yokohama Orthodox Church",
      "local": "横浜ハリストス正教会",
      "country": "JP",
      "dedication": "生神女庇護聖堂",
      "address": [
        "〒221-0843",
        "神奈川県横浜市神奈川区松ヶ丘27-11"
      ],
      "services": [
        "原則毎月土日",
        "・主日前晩祷",
        "土曜 午後5時から",
        "・主日聖体礼儀",
        "日曜 午前10時から",
        "＊正教会暦に準拠した諸祭日については教会に直接お問合せください"
      ],
      "site": "http://www.orthodox-yokohama.jp/",
      "sources": [
        "https://www.orthodoxjapan.jp/area-tokyo.html",
        "https://www.orthodoxjapan.jp/annai/t-yokohama.html",
        "http://www.orthodox-yokohama.jp/"
      ]
    },
    {
      "id": "jp-ashikaga-parish",
      "parent": "jp-tokyo",
      "kind": "parish",
      "rank": "Parish",
      "name": "Ashikaga Orthodox Church",
      "local": "足利ハリストス正教会",
      "country": "JP",
      "dedication": "主の昇天聖堂",
      "address": [
        "〒326-0817",
        "栃木県足利市西宮町2855-2"
      ],
      "services": [
        "第一土曜日 10:00 聖体礼儀  (事前に要確認)"
      ],
      "founded": [
        "日本最古の大学、足利学校の所在地として有名な足利に正教の教えがもたらされたのは、明治11年のことであった。"
      ],
      "sources": [
        "https://www.orthodoxjapan.jp/area-tokyo.html",
        "https://www.orthodoxjapan.jp/annai/t-ashikaga.html"
      ]
    },
    {
      "id": "jp-kanuma-parish",
      "parent": "jp-tokyo",
      "kind": "parish",
      "rank": "Parish",
      "name": "Kanuma Orthodox Church",
      "local": "鹿沼ハリストス正教会",
      "country": "JP",
      "dedication": "聖使徒ペトル、パウェル会堂",
      "address": [
        "〒322-0065",
        "栃木県鹿沼市上材木町1732"
      ],
      "services": [
        "第4日曜日"
      ],
      "sources": [
        "https://www.orthodoxjapan.jp/area-tokyo.html",
        "https://www.orthodoxjapan.jp/annai/t-kanuma.html"
      ]
    },
    {
      "id": "jp-bato-parish",
      "parent": "jp-tokyo",
      "kind": "parish",
      "rank": "Parish",
      "name": "Bato Orthodox Church",
      "local": "馬頭ハリストス正教会",
      "country": "JP",
      "dedication": "顕栄聖堂",
      "address": [
        "〒324-0613",
        "栃木県那須郡那珂川町馬頭339"
      ],
      "services": [
        "毎月第三日曜日 10:00 聖体礼儀",
        "前日土曜日 17:00 前晩祷"
      ],
      "founded": [
        "馬頭に正教会の種が蒔かれたのは明治11(1878)年頃。"
      ],
      "sources": [
        "https://www.orthodoxjapan.jp/area-tokyo.html",
        "https://www.orthodoxjapan.jp/annai/t-batou.html"
      ]
    },
    {
      "id": "jp-utsunomiya-parish",
      "parent": "jp-tokyo",
      "kind": "parish",
      "rank": "Parish",
      "name": "Utsunomiya Orthodox Church",
      "local": "宇都宮ハリストス正教会",
      "country": "JP",
      "dedication": "亜使徒聖大帝コンスタンティン及び聖大后エレナ会堂",
      "address": [
        "〒320-0861",
        "栃木県宇都宮市西1-5-7"
      ],
      "services": [
        "奇数月第2金曜日午後4時～晩祷、土曜日午前10時～聖体礼儀",
        "偶数月第2土曜日午後4時～晩祷、日曜日午前10時～聖体礼儀"
      ],
      "founded": [
        "宇都宮ハリストス正教会沿革\n宇都宮ハリストス正教会は1877年（明治10年）に設立。",
        "宇都宮市中心部に位置し、長い間、古い家屋を利用して祈祷が行われていたが、2004（平成16）年6月に地元信徒の熱意により念願であった新会堂を建設、成聖された。"
      ],
      "sources": [
        "https://www.orthodoxjapan.jp/area-tokyo.html",
        "https://www.orthodoxjapan.jp/annai/t-utsunomiya.html"
      ]
    },
    {
      "id": "jp-akutsu-parish",
      "parent": "jp-tokyo",
      "kind": "parish",
      "rank": "Parish",
      "name": "Akutsu Orthodox Church",
      "local": "圷ハリストス正教会",
      "country": "JP",
      "dedication": "聖使徒パワェル会堂",
      "address": [
        "〒311-4323",
        "茨城県東茨城郡城里町上圷2329"
      ],
      "services": [
        "横浜教会にお問い合わせください"
      ],
      "founded": [
        "1889（明治22）年に趣のある二階建て会堂が建てられ、後に平屋に改築された。",
        "この会堂は2011(平成23)年の震災で損壊。"
      ],
      "sources": [
        "https://www.orthodoxjapan.jp/area-tokyo.html",
        "https://www.orthodoxjapan.jp/annai/t-akutsu.html"
      ]
    },
    {
      "id": "jp-odawara-parish",
      "parent": "jp-tokyo",
      "kind": "parish",
      "rank": "Parish",
      "name": "Odawara Orthodox Church",
      "local": "小田原ハリストス正教会",
      "country": "JP",
      "dedication": "聖神降臨聖堂",
      "address": [
        "〒250-0011",
        "神奈川県小田原市栄町4-4-1"
      ],
      "services": [
        "・晩祷",
        "毎月第1、第3、第4、",
        "(第5)土曜日 午後5時から",
        "・聖体礼儀",
        "毎月  第1、第3、第4、",
        "(第5)日曜日 午前10時から"
      ],
      "founded": [
        "二年後には、信徒たちのあいだに聖堂を建てたいという気持ちが起こり、自主的に募金活動が始まった。"
      ],
      "site": "http://odawara-orthodox.com/",
      "sources": [
        "https://www.orthodoxjapan.jp/area-tokyo.html",
        "https://www.orthodoxjapan.jp/annai/t-odawara.html",
        "http://odawara-orthodox.com/"
      ]
    },
    {
      "id": "jp-shizuoka-parish",
      "parent": "jp-tokyo",
      "kind": "parish",
      "rank": "Parish",
      "name": "Shizuoka Orthodox Church",
      "local": "静岡ハリストス正教会",
      "country": "JP",
      "dedication": "生神女庇護聖堂",
      "address": [
        "〒420-0823",
        "静岡県静岡市葵区春日3-9-5"
      ],
      "services": [
        "・主日前晩祷",
        "毎週土曜日 17：00",
        "・主日聖体礼儀",
        "毎週日曜日 10：00",
        "原則月最終日曜日を除く",
        "（時間は変更になることがあります。お問い合わせください。）"
      ],
      "founded": [
        "6年後、市内人宿町に最初の静岡教会会堂を新築、信徒は40人余りと記録されている。"
      ],
      "site": "https://www.ocj-shizuoka.org/",
      "sources": [
        "https://www.orthodoxjapan.jp/area-tokyo.html",
        "https://www.orthodoxjapan.jp/annai/t-shizuoka.html",
        "https://www.ocj-shizuoka.org/"
      ]
    },
    {
      "id": "jp-shuzenji-parish",
      "parent": "jp-tokyo",
      "kind": "parish",
      "rank": "Parish",
      "name": "Shuzenji Orthodox Church",
      "local": "修善寺ハリストス正教会",
      "country": "JP",
      "dedication": "顕栄聖堂",
      "address": [
        "〒410-2416",
        "静岡県伊豆市修善寺861"
      ],
      "services": [
        "・ 聖体礼儀",
        "毎月第2日曜日 午前10時から"
      ],
      "sources": [
        "https://www.orthodoxjapan.jp/area-tokyo.html",
        "https://www.orthodoxjapan.jp/annai/t-shuzesnji.html"
      ]
    },
    {
      "id": "jp-kashiwakubo-parish",
      "parent": "jp-tokyo",
      "kind": "parish",
      "rank": "Parish",
      "name": "Kashiwakubo Orthodox Church",
      "local": "柏久保ハリストス正教会",
      "country": "JP",
      "dedication": "主の降誕会堂",
      "address": [
        "〒410-2407",
        "静岡県伊豆市柏久保325"
      ],
      "services": [
        "・ 祈祷集会",
        "毎月第2土曜日 午前10時から"
      ],
      "founded": [
        "1880年（明13年）に最初の洗礼が行われる。",
        "伊豆の中心に位置する現在の会堂は、1909年（明42年）に建立された。"
      ],
      "sources": [
        "https://www.orthodoxjapan.jp/area-tokyo.html",
        "https://www.orthodoxjapan.jp/annai/t-kashiwakubo.html"
      ]
    },
    {
      "id": "jp-hamamatsu-parish",
      "parent": "jp-tokyo",
      "kind": "parish",
      "rank": "Parish",
      "name": "Hamamatsu Orthodox Church",
      "local": "浜松ハリストス正教会",
      "country": "JP",
      "dedication": "主の降誕会堂",
      "address": [
        "〒432-8014",
        "静岡県浜松市中区鹿谷町28-13"
      ],
      "services": [
        "毎月最終日曜日"
      ],
      "sources": [
        "https://www.orthodoxjapan.jp/area-tokyo.html",
        "https://www.orthodoxjapan.jp/annai/t-hamamatsu.html"
      ]
    }
  ],
  "jp-east": [
    {
      "id": "jp-sendai-parish",
      "parent": "jp-east",
      "kind": "parish",
      "rank": "Parish",
      "name": "Sendai Orthodox Church",
      "local": "仙台ハリストス正教会",
      "country": "JP",
      "dedication": "生神女福音聖堂",
      "address": [
        "〒980-0021",
        "宮城県仙台市青葉区中央3丁目4-20"
      ],
      "services": [
        "・毎日曜日午前10時",
        "・毎土曜日午後5時",
        "※どなたでも参祷出来ます。",
        "・教会の暦に従って復活大祭を中心に、救主イイスス・ハリストス（イエス・キリスト）や生神女マリヤと諸聖人を記憶する祭日が年間を通してあり、お祈りが行われます。"
      ],
      "founded": [
        "正教会初期の伝道は旧仙台藩士から始められた。",
        "1873年（明治6）には最初の公祈祷が行われた。"
      ],
      "site": "http://www.sendai-orthodox.com/",
      "sources": [
        "https://www.orthodoxjapan.jp/area-higashi.html",
        "https://www.orthodoxjapan.jp/annai/h-sendai.html",
        "http://www.sendai-orthodox.com/"
      ]
    },
    {
      "id": "jp-nakaniida-parish",
      "parent": "jp-east",
      "kind": "parish",
      "rank": "Parish",
      "name": "Nakaniida Orthodox Church",
      "local": "中新田ハリストス正教会",
      "country": "JP",
      "dedication": "前駆授洗イオアン聖堂",
      "address": [
        "〒981-4241",
        "宮城県加美郡加美町字南町173"
      ],
      "services": [
        "月1度司祭が巡回し、土曜日に晩祷、日曜日に聖体礼儀が行われている。"
      ],
      "founded": [
        "1884年(明治17)に最初の会堂が建立される。",
        "現聖堂は1967年(昭和42)建立。"
      ],
      "sources": [
        "https://www.orthodoxjapan.jp/area-higashi.html",
        "https://www.orthodoxjapan.jp/annai/h-nakaniida.html"
      ]
    },
    {
      "id": "jp-shirakawa-parish",
      "parent": "jp-east",
      "kind": "parish",
      "rank": "Parish",
      "name": "Shirakawa Orthodox Church",
      "local": "白河ハリストス正教会",
      "country": "JP",
      "dedication": "生神女進堂聖堂",
      "address": [
        "〒961-0942",
        "福島県白河市愛宕町50"
      ],
      "services": [
        "月に1度、巡回があり土曜日18：00～より晩祷、日曜日10：00～聖体礼儀が行われる。"
      ],
      "founded": [
        "1882年(明治15)に会堂が建てられ、今は集会所として現存。",
        "現聖堂は1915年(大正4)建立。"
      ],
      "sources": [
        "https://www.orthodoxjapan.jp/area-higashi.html",
        "https://www.orthodoxjapan.jp/annai/h-shirakawa.html"
      ]
    },
    {
      "id": "jp-ishinomaki-parish",
      "parent": "jp-east",
      "kind": "parish",
      "rank": "Parish",
      "name": "Ishinomaki Orthodox Church",
      "local": "石巻ハリストス正教会",
      "country": "JP",
      "dedication": "聖使徒イオアン聖堂",
      "address": [
        "〒986-0827",
        "宮城県石巻市千石町4-10"
      ],
      "services": [
        "・晩祷",
        "第1・3土曜日 午後6時",
        "・聖体礼儀",
        "第1・3日曜日 午前10時"
      ],
      "founded": [
        "1879年（明治12）に建立された初代聖堂は、国内最古の木造教会建築として石巻市中瀬公園に保存公開されていたが、2011年の東日本大震災で津波被害を受け、現在解体・再建が模索されている。"
      ],
      "sources": [
        "https://www.orthodoxjapan.jp/area-higashi.html",
        "https://www.orthodoxjapan.jp/annai/h-ishinomeki.html"
      ]
    },
    {
      "id": "jp-takashimizu-parish",
      "parent": "jp-east",
      "kind": "parish",
      "rank": "Parish",
      "name": "Takashimizu Orthodox Church",
      "local": "高清水ハリストス正教会",
      "country": "JP",
      "dedication": "主の顕栄聖堂",
      "address": [
        "〒987-2133",
        "宮城県栗原市高清水桜丁37"
      ],
      "services": [
        "・晩祷",
        "第4土曜日 午後6時30分",
        "・聖体礼儀",
        "第4日曜日 午後6時30分"
      ],
      "founded": [
        "1875年(明治8)に最初の洗礼が行われた後、この地の多くの青年が上京し、神品多数を輩出する。",
        "現会堂は1974年(昭和49)建立。"
      ],
      "sources": [
        "https://www.orthodoxjapan.jp/area-higashi.html",
        "https://www.orthodoxjapan.jp/annai/h-takashimizu.html"
      ]
    },
    {
      "id": "jp-sanuma-parish",
      "parent": "jp-east",
      "kind": "parish",
      "rank": "Parish",
      "name": "Sanuma Orthodox Church",
      "local": "佐沼ハリストス正教会",
      "country": "JP",
      "dedication": "主の顕栄聖堂",
      "address": [
        "〒987-0511",
        "宮城県登米市迫町佐沼西佐沼89"
      ],
      "founded": [
        "1896年に東北地方をおそった地震によって教会も破壊されて、試練の中におかれた。"
      ],
      "sources": [
        "https://www.orthodoxjapan.jp/area-higashi.html",
        "https://www.orthodoxjapan.jp/annai/h-sanuma.html"
      ]
    },
    {
      "id": "jp-jogetsutsumi-parish",
      "parent": "jp-east",
      "kind": "parish",
      "rank": "Parish",
      "name": "Jogetsutsumi Orthodox Church",
      "local": "上下堤ハリストス正教会",
      "country": "JP",
      "dedication": "生神女庇護聖堂",
      "address": [
        "〒981-0305",
        "宮城県東松島市上下堤字磯田沢78"
      ],
      "services": [
        "月1度、司祭が巡回し聖体礼儀が行われている。"
      ],
      "founded": [
        "最初の信徒は1877年(明治10)に仙台で受洗した一青年。",
        "2011年3月の東日本大震災で大きな被害を受けた会堂は、2013年6月2日に修復され成聖式が行われた。"
      ],
      "sources": [
        "https://www.orthodoxjapan.jp/area-higashi.html",
        "https://www.orthodoxjapan.jp/annai/h-jougedutsumi.html"
      ]
    },
    {
      "id": "jp-wakuya-parish",
      "parent": "jp-east",
      "kind": "parish",
      "rank": "Parish",
      "name": "Wakuya Orthodox Church",
      "local": "涌谷ハリストス正教会",
      "country": "JP",
      "dedication": "聖預言者イサイヤ聖堂",
      "address": [
        "〒987-0163",
        "宮城県遠田郡涌谷町立町14"
      ],
      "services": [
        "・晩祷",
        "第2土曜日 午後4時",
        "・聖体礼儀",
        "第2日曜日 午前9時30分"
      ],
      "founded": [
        "1882年（明治15）、聖ニコライがこの地を巡回し会堂建設を促すと、直ちに建築にかかり翌年完成させた。",
        "1958年（昭和33）に再建立されるが、2003年（平成15）の地震被害を被り、2004年（平成16）に新築された。"
      ],
      "sources": [
        "https://www.orthodoxjapan.jp/area-higashi.html",
        "https://www.orthodoxjapan.jp/annai/h-wakuya.html"
      ]
    },
    {
      "id": "jp-hakodate-parish",
      "parent": "jp-east",
      "kind": "parish",
      "rank": "Parish",
      "name": "Hakodate Orthodox Church",
      "local": "函館ハリストス正教会",
      "country": "JP",
      "address": [
        "〒040-0054",
        "北海道函館市元町3-13"
      ],
      "services": [
        "・晩祷",
        "毎週土曜日 午後5時",
        "・聖体礼儀（日曜礼拝）",
        "日曜日 午前10時",
        "※ 詳しくは教会までお問い合わせ下さい。 また、ハリストスの教え、聖書、正教会について学ばれたい方は教会にご連絡下さい。"
      ],
      "founded": [
        "1861年聖ニコライが来日した日本正教会発祥の地。"
      ],
      "site": "http://orthodox-hakodate.jp/",
      "sources": [
        "https://www.orthodoxjapan.jp/area-higashi.html",
        "https://www.orthodoxjapan.jp/annai/h-hakodate.html",
        "http://orthodox-hakodate.jp/"
      ]
    },
    {
      "id": "jp-kamiiso-parish",
      "parent": "jp-east",
      "kind": "parish",
      "rank": "Parish",
      "name": "Kamiiso Orthodox Church",
      "local": "上磯ハリストス正教会",
      "country": "JP",
      "dedication": "主の昇天聖堂",
      "address": [
        "〒049-0155",
        "北海道北斗市中野177"
      ],
      "services": [
        "・晩祷",
        "毎月第2土曜日",
        "・聖体礼儀",
        "日曜日",
        "※月によって変更あり"
      ],
      "founded": [
        "現在の聖堂は1987年(昭和62)に建立された。",
        "聖堂の沿革\n1884年（明治17）に初代の「有川昇天会堂」が、上磯町最初のキリスト教会堂として建立された。"
      ],
      "sources": [
        "https://www.orthodoxjapan.jp/area-higashi.html",
        "https://www.orthodoxjapan.jp/annai/h-kamiiso.html"
      ]
    },
    {
      "id": "jp-sapporo-parish",
      "parent": "jp-east",
      "kind": "parish",
      "rank": "Parish",
      "name": "Sapporo Orthodox Church",
      "local": "札幌ハリストス正教会",
      "country": "JP",
      "dedication": "主の顕栄聖堂",
      "address": [
        "〒062-0042",
        "北海道札幌市豊平区福住2条2丁目3-1"
      ],
      "services": [
        "・晩祷",
        "第2、第4土曜日 午後4時",
        "・聖体礼儀",
        "第2、第4日曜日 午前10時"
      ],
      "founded": [
        "6つのクーポルが特徴の聖堂は、静かな住宅地に溶け込んで美しい。",
        "1971年都市計画により札幌の中心地からここに移った。"
      ],
      "site": "https://sites.google.com/view/orthodox-sapporo",
      "sources": [
        "https://www.orthodoxjapan.jp/area-higashi.html",
        "https://www.orthodoxjapan.jp/annai/h-sapporo.html",
        "https://sites.google.com/view/orthodox-sapporo"
      ]
    },
    {
      "id": "jp-otaru-parish",
      "parent": "jp-east",
      "kind": "parish",
      "rank": "Parish",
      "name": "Otaru Orthodox Church",
      "local": "小樽ハリストス正教会",
      "country": "JP",
      "dedication": "主の復活聖堂",
      "address": [
        "〒047-0034",
        "北海道小樽市緑1丁目15-13"
      ],
      "services": [
        "・晩祷",
        "第3土曜日 午後4時",
        "・聖体礼儀",
        "第3日曜日 午前10時"
      ],
      "founded": [
        "小樽に正教が伝えられたのは1887年（明治20）頃で講義所が開かれ布教された。"
      ],
      "sources": [
        "https://www.orthodoxjapan.jp/area-higashi.html",
        "https://www.orthodoxjapan.jp/annai/h-otaru.html"
      ]
    },
    {
      "id": "jp-tomakomai-parish",
      "parent": "jp-east",
      "kind": "parish",
      "rank": "Parish",
      "name": "Tomakomai Orthodox Church",
      "local": "苫小牧ハリストス正教会",
      "country": "JP",
      "dedication": "主の降誕聖堂",
      "address": [
        "〒053-0851",
        "北海道苫小牧市山手町1丁目1-17"
      ],
      "services": [
        "・晩祷",
        "第1土曜日 午後4時",
        "・聖体礼儀",
        "第1日曜日 午前10時"
      ],
      "founded": [
        "現在の会堂は1975年（昭和50）に建立。",
        "1階聖堂、2階集会所の造りで、林に囲まれた住宅地にある。"
      ],
      "sources": [
        "https://www.orthodoxjapan.jp/area-higashi.html",
        "https://www.orthodoxjapan.jp/annai/h-tomakomai.html"
      ]
    },
    {
      "id": "jp-kushiro-parish",
      "parent": "jp-east",
      "kind": "parish",
      "rank": "Parish",
      "name": "Kushiro Orthodox Church",
      "local": "釧路ハリストス正教会",
      "country": "JP",
      "dedication": "聖神゜降臨聖堂",
      "address": [
        "〒085-0832",
        "北海道釧路市富士見2-1-35"
      ],
      "services": [
        "・聖体礼儀",
        "第1，3，5日曜日 午前10時",
        "・代式祈祷",
        "第2，4日曜日 午前10時",
        "（信徒による）"
      ],
      "founded": [
        "明治初頭、根室を拠点に現在の北海道東部、北方四島に正教は伝えられた。",
        "釧路には1902年(明治35)に会堂が建立される。"
      ],
      "site": "https://www.orthodoxjp.com/kushiro/index.htm",
      "sources": [
        "https://www.orthodoxjapan.jp/area-higashi.html",
        "https://www.orthodoxjapan.jp/annai/h-kushiro.html",
        "https://www.orthodoxjp.com/kushiro/index.htm"
      ]
    },
    {
      "id": "jp-kamimusa-parish",
      "parent": "jp-east",
      "kind": "parish",
      "rank": "Parish",
      "name": "Kamimusa Orthodox Church",
      "local": "上武佐ハリストス正教会",
      "country": "JP",
      "dedication": "生神女就寝聖堂",
      "address": [
        "〒086-1271",
        "北海道標津郡中標津町字武佐南9線西1番地"
      ],
      "services": [
        "・前晩祷",
        "第2土曜日 午後6時",
        "・聖体礼儀",
        "第2日曜日 午前10時"
      ],
      "founded": [
        "現会堂は1978年(昭和53)建立。",
        "山下りんの12大祭の聖像がある。"
      ],
      "sources": [
        "https://www.orthodoxjapan.jp/area-higashi.html",
        "https://www.orthodoxjapan.jp/annai/h-kamimusa.html"
      ]
    },
    {
      "id": "jp-shari-parish",
      "parent": "jp-east",
      "kind": "parish",
      "rank": "Parish",
      "name": "Shari Orthodox Church",
      "local": "斜里ハリストス正教会",
      "country": "JP",
      "dedication": "生神女福音聖堂",
      "address": [
        "〒099-4145",
        "北海道斜里郡斜里町字美咲60-9"
      ],
      "services": [
        "・晩祷",
        "第4土曜日 午後6時",
        "・聖体礼儀",
        "第4日曜日 午前10時"
      ],
      "founded": [
        "北海道十勝から移住した5戸の信徒の集会が教会の始まり。",
        "知床国立公園にも近い農村地帯に立つ現会堂は1979年(昭和54)に建立。"
      ],
      "sources": [
        "https://www.orthodoxjapan.jp/area-higashi.html",
        "https://www.orthodoxjapan.jp/annai/h-shari.html"
      ]
    },
    {
      "id": "jp-morioka-parish",
      "parent": "jp-east",
      "kind": "parish",
      "rank": "Parish",
      "name": "Morioka Orthodox Church",
      "local": "盛岡ハリストス正教会",
      "country": "JP",
      "dedication": "聖十字架挙栄聖堂",
      "address": [
        "〒020-0114",
        "岩手県盛岡市高松1-2-14"
      ],
      "services": [
        "・晩祷",
        "毎週土曜日 午後5時",
        "（ただし第2土曜はお休み）",
        "・聖体礼儀",
        "第2・4日曜日 午前10時",
        "※月によって変動あり。",
        "詳細は問い合わせてください。"
      ],
      "founded": [
        "盛岡市立公園「高松の池」に程近い高台にあり、国道4号線から大きな鐘楼とドームが見える。"
      ],
      "site": "https://www.ocjmorioka.com/",
      "sources": [
        "https://www.orthodoxjapan.jp/area-higashi.html",
        "https://www.orthodoxjapan.jp/annai/h-morioka.html",
        "https://www.ocjmorioka.com/"
      ]
    },
    {
      "id": "jp-hokushika-parish",
      "parent": "jp-east",
      "kind": "parish",
      "rank": "Parish",
      "name": "Hokushika Orthodox Church",
      "local": "北鹿ハリストス正教会",
      "country": "JP",
      "dedication": "生神女福音会堂",
      "address": [
        "〒018-5603",
        "秋田県大館市曲田80-1"
      ],
      "services": [
        "・聖体礼儀",
        "第2土曜日 午前10時",
        "（月1度、管轄司祭が巡回）"
      ],
      "founded": [
        "1892年（明治25）建立の木造の会堂は、今でも内外ともに美しさを保っている。"
      ],
      "sources": [
        "https://www.orthodoxjapan.jp/area-higashi.html",
        "https://www.orthodoxjapan.jp/annai/h-hokushika.html"
      ]
    },
    {
      "id": "jp-iwayado-parish",
      "parent": "jp-east",
      "kind": "parish",
      "rank": "Parish",
      "name": "Iwayado Orthodox Church",
      "local": "岩谷堂ハリストス正教会",
      "country": "JP",
      "dedication": "主の降誕聖堂",
      "address": [
        "〒023-1121",
        "岩手県奥州市江刺区男石1-4-3"
      ],
      "services": [
        "・聖体礼儀",
        "第5日曜日 午前10時",
        "（その他、土曜日に巡回もあり）"
      ],
      "sources": [
        "https://www.orthodoxjapan.jp/area-higashi.html",
        "https://www.orthodoxjapan.jp/annai/h-iwayadou.html"
      ]
    },
    {
      "id": "jp-yamada-parish",
      "parent": "jp-east",
      "kind": "parish",
      "rank": "Parish",
      "name": "Yamada Orthodox Church",
      "local": "山田ハリストス正教会",
      "country": "JP",
      "dedication": "主の復活会堂",
      "address": [
        "〒028-1341",
        "岩手県下閉伊郡山田町八幡町4-28"
      ],
      "services": [
        "・聖体礼儀",
        "第3日曜日 午前10時",
        "（月1度、管轄司祭が巡回）",
        "（前日の土曜日の夕方には晩課）"
      ],
      "founded": [
        "2011年3月の東日本大震災で山田町の市街地は津波と火災に被害を受け、会堂は焼失した。",
        "新会堂建設までの期間、仮会堂を設置して教会活動を行ってきたが、2018年12月2日、教団に寄せられた義援金により、「主の復活会堂」が建立され、成聖された。"
      ],
      "sources": [
        "https://www.orthodoxjapan.jp/area-higashi.html",
        "https://www.orthodoxjapan.jp/annai/h-yamada.html"
      ]
    },
    {
      "id": "jp-tono-parish",
      "parent": "jp-east",
      "kind": "parish",
      "rank": "Parish",
      "name": "Tono Orthodox Church",
      "local": "遠野正教会",
      "country": "JP",
      "dedication": "聖太祖アウラアム・サッラ会堂",
      "address": [
        "〒028-0555",
        "岩手県遠野市土淵町土淵10地割31-1"
      ],
      "services": [
        "・聖体礼儀",
        "第1日曜日 午前10時",
        "（月1度、管轄司祭が巡回）"
      ],
      "founded": [
        "長らく会堂が無かったが2013年地元信徒の努力により自力で建立した。"
      ],
      "sources": [
        "https://www.orthodoxjapan.jp/area-higashi.html",
        "https://www.orthodoxjapan.jp/annai/h-touno.html"
      ]
    },
    {
      "id": "jp-ichinoseki-parish",
      "parent": "jp-east",
      "kind": "parish",
      "rank": "Parish",
      "name": "Ichinoseki Orthodox Church",
      "local": "一関ハリストス正教会",
      "country": "JP",
      "dedication": "昇天聖堂",
      "address": [
        "〒021-0902",
        "岩手県一関市萩荘箱清水56-1"
      ],
      "services": [
        "・晩祷",
        "第1・4土曜日 午後5時",
        "・聖体礼儀（日曜礼拝）",
        "第1・4日曜日 午前10時"
      ],
      "founded": [
        "北上川交通の要所として栄えた一関はこの地方の伝道拠点で、1872年（明治5）には早くも布教が開始された。"
      ],
      "sources": [
        "https://www.orthodoxjapan.jp/area-higashi.html",
        "https://www.orthodoxjapan.jp/annai/h-ichinoseki.html"
      ]
    },
    {
      "id": "jp-kesennuma-parish",
      "parent": "jp-east",
      "kind": "parish",
      "rank": "Parish",
      "name": "Kesennuma Orthodox Church",
      "local": "気仙沼ハリストス正教会",
      "country": "JP",
      "dedication": "復活会堂",
      "address": [
        "〒988-0016",
        "宮城県気仙沼市沢田1-11"
      ],
      "services": [
        "月1度管轄司祭が巡回し、土曜日に聖体礼儀が行われている。"
      ],
      "founded": [
        "漁港として有名な同地では、1872年(明治5)には伝道が始まる。",
        "1889年(明治22)に建立された会堂は焼失したが再建された。"
      ],
      "sources": [
        "https://www.orthodoxjapan.jp/area-higashi.html",
        "https://www.orthodoxjapan.jp/annai/h-kesennuma.html"
      ]
    },
    {
      "id": "jp-kannari-parish",
      "parent": "jp-east",
      "kind": "parish",
      "rank": "Parish",
      "name": "Kannari Orthodox Church",
      "local": "金成ハリストス正教会",
      "country": "JP",
      "dedication": "聖使徒イオアン聖堂",
      "address": [
        "〒989-5155",
        "宮城県栗原市金成上町西裏60-1"
      ],
      "services": [
        "・晩祷",
        "第3土曜日 午後5時",
        "・聖体礼儀",
        "第3日曜日 午前10時"
      ],
      "founded": [
        "明治の初め迫害にあいながらも布教が行なわれ、この地方の各村々に教会が生まれた。",
        "現聖堂は川股松太郎の尽力によって1934年（昭和9）に建立。"
      ],
      "sources": [
        "https://www.orthodoxjapan.jp/area-higashi.html",
        "https://www.orthodoxjapan.jp/annai/h-kannari.html"
      ]
    },
    {
      "id": "jp-jumonji-parish",
      "parent": "jp-east",
      "kind": "parish",
      "rank": "Parish",
      "name": "Jumonji Orthodox Church",
      "local": "十文字ハリストス正教会",
      "country": "JP",
      "address": [
        "〒989-5501",
        "宮城県栗原市若柳川北十文字53"
      ],
      "services": [
        "・晩祷",
        "金曜日 午後6時",
        "・聖体礼儀",
        "土曜日 午前10時",
        "※月1度司祭巡回。"
      ],
      "founded": [
        "現会堂は1976年(昭和51)に建てられた。"
      ],
      "sources": [
        "https://www.orthodoxjapan.jp/area-higashi.html",
        "https://www.orthodoxjapan.jp/annai/h-jumonji.html"
      ]
    },
    {
      "id": "jp-sakari-parish",
      "parent": "jp-east",
      "kind": "parish",
      "rank": "Parish",
      "name": "Sakari Orthodox Church",
      "local": "盛ハリストス正教会",
      "country": "JP",
      "dedication": "昇天聖堂",
      "address": [
        "〒022-0003",
        "岩手県大船渡市盛町字町1-2"
      ],
      "services": [
        "・晩祷",
        "第2土曜日 午後5時",
        "・聖体礼儀（日曜礼拝）",
        "第2日曜日 午前10時"
      ],
      "sources": [
        "https://www.orthodoxjapan.jp/area-higashi.html",
        "https://www.orthodoxjapan.jp/annai/h-sakari.html"
      ]
    },
    {
      "id": "jp-okutama-parish",
      "parent": "jp-east",
      "kind": "parish",
      "rank": "Parish",
      "name": "Okutama Orthodox Church",
      "local": "奥玉ハリストス正教会",
      "country": "JP",
      "sources": [
        "https://www.orthodoxjapan.jp/area-higashi.html",
        "https://www.orthodoxjapan.jp/annai/h-okutama.html"
      ]
    },
    {
      "id": "jp-sogei-parish",
      "parent": "jp-east",
      "kind": "parish",
      "rank": "Parish",
      "name": "Sogei Orthodox Church",
      "local": "曾慶ハリストス正教会",
      "country": "JP",
      "founded": [
        "この地方への伝道は早く、1877年（明治10）には32人が受洗した。"
      ],
      "sources": [
        "https://www.orthodoxjapan.jp/area-higashi.html",
        "https://www.orthodoxjapan.jp/annai/h-sogei.html"
      ]
    },
    {
      "id": "jp-hikata-parish",
      "parent": "jp-east",
      "kind": "parish",
      "rank": "Parish",
      "name": "Hikata Orthodox Church",
      "local": "日形ハリストス正教会",
      "country": "JP",
      "founded": [
        "教会設立は1887年(明治20)で、会堂も建立したが現在は無い。"
      ],
      "sources": [
        "https://www.orthodoxjapan.jp/area-higashi.html",
        "https://www.orthodoxjapan.jp/annai/h-hikata.html"
      ]
    }
  ],
  "jp-west": [
    {
      "id": "jp-kyoto-parish",
      "parent": "jp-west",
      "kind": "parish",
      "rank": "Parish",
      "name": "Kyoto Orthodox Church",
      "local": "京都ハリストス正教会",
      "country": "JP",
      "dedication": "生神女福音聖堂",
      "address": [
        "〒604-0965",
        "京都府京都市中京区柳馬場通二条上る6丁目283"
      ],
      "founded": [
        "京都市内では、同22（1889）年に市の中心部「押小路通高倉西入る」に講義所を設立。"
      ],
      "site": "https://kyoto-orthodox.or.jp/",
      "sources": [
        "https://www.orthodoxjapan.jp/area-nishi.html",
        "https://www.orthodoxjapan.jp/annai/n-kyoto.html",
        "https://kyoto-orthodox.or.jp/"
      ]
    },
    {
      "id": "jp-nagoya-parish",
      "parent": "jp-west",
      "kind": "parish",
      "rank": "Parish",
      "name": "Nagoya Orthodox Church",
      "local": "名古屋ハリストス正教会",
      "country": "JP",
      "dedication": "神現聖堂",
      "address": [
        "〒466-0063",
        "愛知県名古屋市昭和区山脇町1-3-3"
      ],
      "founded": [
        "名古屋に正教がはじめて伝道されたのは明治7年である。",
        "最初に洗礼を受けたのは近藤瀬兵衛で、明治10年には市内に6カ所に講義所が開かれていた。"
      ],
      "site": "https://orthodoxnagoya.com/",
      "sources": [
        "https://www.orthodoxjapan.jp/area-nishi.html",
        "https://www.orthodoxjapan.jp/annai/n-nagoya.html",
        "https://orthodoxnagoya.com/"
      ]
    },
    {
      "id": "jp-toyohashi-parish",
      "parent": "jp-west",
      "kind": "parish",
      "rank": "Parish",
      "name": "Toyohashi Orthodox Church",
      "local": "豊橋ハリストス正教会",
      "country": "JP",
      "dedication": "聖使徒福音者マトフェイ聖堂",
      "address": [
        "〒440-0806",
        "愛知県豊橋市八町通3-15"
      ],
      "founded": [
        "1875年に布教が開始され、翌1876年に岡崎で3名が、また1877年には豊橋で17名が受洗。",
        "1879年、中八町に二階建ての木造教会「昇天会堂」を建設。"
      ],
      "site": "https://sites.google.com/view/orthodox-ths",
      "sources": [
        "https://www.orthodoxjapan.jp/area-nishi.html",
        "https://www.orthodoxjapan.jp/annai/n-toyohashi.html",
        "https://sites.google.com/view/orthodox-ths"
      ]
    },
    {
      "id": "jp-handa-parish",
      "parent": "jp-west",
      "kind": "parish",
      "rank": "Parish",
      "name": "Handa Orthodox Church",
      "local": "半田ハリストス正教会",
      "country": "JP",
      "dedication": "聖イオアン・ダマスキン聖堂",
      "address": [
        "〒475-0068",
        "愛知県半田市乙川西ノ宮町3-33"
      ],
      "founded": [
        "大正2年（1913年）にできた会堂が今も堅牢な姿で立っている。"
      ],
      "sources": [
        "https://www.orthodoxjapan.jp/area-nishi.html",
        "https://www.orthodoxjapan.jp/annai/n-handa.html"
      ]
    },
    {
      "id": "jp-osaka-parish",
      "parent": "jp-west",
      "kind": "parish",
      "rank": "Parish",
      "name": "Osaka Orthodox Church",
      "local": "大阪ハリストス正教会",
      "country": "JP",
      "dedication": "生神女庇護聖堂",
      "address": [
        "〒564-0073",
        "大阪府吹田市山手町1-8-15"
      ],
      "founded": [
        "1874（明治7）年に始まった大阪地方の伝道は、1878（明治11）年3月に実を結び、聴教者37名が領洗し、講義所を開設、大阪正教会が誕生した。",
        "1910（明治43）年7月、大阪天満橋に木造ビザンチン式の聖堂が建立されて、大阪生神女庇護聖堂と名付けられた。"
      ],
      "sources": [
        "https://www.orthodoxjapan.jp/area-nishi.html",
        "https://www.orthodoxjapan.jp/annai/n-osaka.html"
      ]
    },
    {
      "id": "jp-hiroshima-parish",
      "parent": "jp-west",
      "kind": "parish",
      "rank": "Parish",
      "name": "Hiroshima Orthodox Church",
      "local": "広島ハリストス正教会",
      "country": "JP",
      "sources": [
        "https://www.orthodoxjapan.jp/area-nishi.html",
        "https://www.orthodoxjapan.jp/annai/n-hiroshima.html"
      ]
    },
    {
      "id": "jp-kobe-parish",
      "parent": "jp-west",
      "kind": "parish",
      "rank": "Parish",
      "name": "Kobe Orthodox Church",
      "local": "神戸ハリストス正教会",
      "country": "JP",
      "address": [
        "〒650-0003",
        "兵庫県神戸市中央区山本通1-4-11"
      ],
      "services": [
        "・晩祷",
        "毎土曜日 午後５時",
        "・聖体礼儀",
        "毎月三回 日曜日 午前10時",
        "詳細は、上記の神戸正教会ホームページの予定表を参照下さい。"
      ],
      "founded": [
        "1913年神戸市平野祇園町に会堂。"
      ],
      "site": "https://kobeorthodox.jp/",
      "sources": [
        "https://www.orthodoxjapan.jp/area-nishi.html",
        "https://www.orthodoxjapan.jp/annai/n-koube.html",
        "https://kobeorthodox.jp/"
      ]
    },
    {
      "id": "jp-tokushima-parish",
      "parent": "jp-west",
      "kind": "parish",
      "rank": "Parish",
      "name": "Tokushima Orthodox Church",
      "local": "徳島ハリストス正教会",
      "country": "JP",
      "dedication": "聖神降臨聖堂",
      "address": [
        "〒770-8008",
        "徳島県徳島市西新浜町1-3-6"
      ],
      "founded": [
        "明治10年に中小路誠一郎が派遣された。"
      ],
      "sources": [
        "https://www.orthodoxjapan.jp/area-nishi.html",
        "https://www.orthodoxjapan.jp/annai/n-tokushima.html"
      ]
    },
    {
      "id": "jp-yanaihara-parish",
      "parent": "jp-west",
      "kind": "parish",
      "rank": "Parish",
      "name": "Yanaihara Orthodox Church",
      "local": "柳井原ハリストス正教会",
      "country": "JP",
      "address": [
        "〒710-0263",
        "岡山県倉敷市船穂町柳井原1883"
      ],
      "founded": [
        "明治22年に柳井原出身のコルニリイ浅野久吉が洗礼を受けた時から始まっている。"
      ],
      "sources": [
        "https://www.orthodoxjapan.jp/area-nishi.html",
        "https://www.orthodoxjapan.jp/annai/n-yanaihara.html"
      ]
    },
    {
      "id": "jp-wakayama-parish",
      "parent": "jp-west",
      "kind": "parish",
      "rank": "Parish",
      "name": "Wakayama Orthodox Church",
      "local": "和歌山ハリストス正教会",
      "country": "JP",
      "address": [
        "〒649-6338",
        "和歌山県和歌山市府中1011-160"
      ],
      "founded": [
        "1945年和歌山大空襲により、和歌山城近くにあった聖堂を焼失しました。",
        "このたび、戦火で失われた教会堂が、信徒たちの祈りと希望により、その復興へ向けた一歩を踏み出します。"
      ],
      "sources": [
        "https://www.orthodoxjapan.jp/area-nishi.html",
        "https://www.orthodoxjapan.jp/annai/n-wakayama.html"
      ]
    },
    {
      "id": "jp-hitoyoshi-parish",
      "parent": "jp-west",
      "kind": "parish",
      "rank": "Parish",
      "name": "Hitoyoshi Orthodox Church",
      "local": "人吉ハリストス正教会",
      "country": "JP",
      "dedication": "生神女庇護聖堂",
      "address": [
        "〒868-0022",
        "熊本県人吉市願成寺町287-1"
      ],
      "services": [
        "定例会",
        "毎月第3主日・第5主日（日曜日）"
      ],
      "founded": [
        "1932年（昭和7年）に現在のところに移転した。",
        "小高い丘のうえに建つ聖堂は、約400坪の敷地にある。"
      ],
      "sources": [
        "https://www.orthodoxjapan.jp/area-nishi.html",
        "https://www.orthodoxjapan.jp/annai/n-hitoyoshi.html"
      ]
    },
    {
      "id": "jp-kumamoto-mission",
      "parent": "jp-west",
      "kind": "parish",
      "rank": "Mission",
      "name": "Kumamoto Mission of Fukuoka Orthodox Church",
      "local": "福岡ハリストス正教会熊本伝道所",
      "country": "JP",
      "address": [
        "〒862-0975",
        "熊本県熊本市中央区新屋敷1-18-15"
      ],
      "services": [
        "定例会",
        "毎月第2主日（日曜日） 朝10時",
        "※これは原則です。変更することもありますので、必ず日時をご確認の上、 いらっしゃってください。"
      ],
      "founded": [
        "1962年に現在の敷地を購入して念願の会堂を建設した。"
      ],
      "sources": [
        "https://www.orthodoxjapan.jp/area-nishi.html",
        "https://www.orthodoxjapan.jp/annai/n-kumamoto.html"
      ]
    },
    {
      "id": "jp-kagoshima-parish",
      "parent": "jp-west",
      "kind": "parish",
      "rank": "Parish",
      "name": "Kagoshima Orthodox Church",
      "local": "鹿児島ハリストス正教会",
      "country": "JP",
      "dedication": "聖使徒イアコフ聖堂",
      "address": [
        "〒892-0848",
        "鹿児島県鹿児島市平之町12-39"
      ],
      "services": [
        "定例会",
        "毎月第4主日（日曜日）"
      ],
      "founded": [
        "明治時代に二度にわたって消失した聖堂は、その都度全信徒の努力によって再建された。",
        "第二次大戦末期には戦災にあって再度焼失した。"
      ],
      "sources": [
        "https://www.orthodoxjapan.jp/area-nishi.html",
        "https://www.orthodoxjapan.jp/annai/n-kagoshima.html"
      ]
    },
    {
      "id": "jp-fukuoka-parish",
      "parent": "jp-west",
      "kind": "parish",
      "rank": "Parish",
      "name": "Fukuoka Orthodox Church",
      "local": "福岡ハリストス正教会",
      "country": "JP",
      "address": [
        "〒811-2232",
        "福岡県糟屋郡志免町別府西 2-7-1"
      ],
      "sources": [
        "https://www.orthodoxjapan.jp/area-nishi.html",
        "https://www.orthodoxjapan.jp/annai/n-fukuoka.html"
      ]
    }
  ]
}''')


def clean(row):
    out = {key: value for key, value in row.items()
           if value not in (None, "", [])}
    if out.get("founded"):
        founded = [value for value in out["founded"]
                   if not any(word in value for word in CLERGY_WORDS)]
        if founded:
            out["founded"] = founded
        else:
            out.pop("founded")
    out.setdefault("checked", CHECKED)
    sources = list(out.get("sources") or [])
    if not sources or len(sources) > 3:
        raise ValueError("%s must cite one to three sources" % out.get("id"))
    if not all(str(url).startswith("http") for url in sources):
        raise ValueError("%s carries a non-URL source" % out.get("id"))
    out["sources"] = sources
    out["cite"] = list(sources)
    for field in ("address", "languages", "services", "founded"):
        if out.get(field) and (not isinstance(out[field], list) or
                               not all(isinstance(value, str)
                                       for value in out[field])):
            raise ValueError("%s has invalid %s" % (out.get("id"), field))
    return out


def build():
    payloads = {}
    seen = set(ROWS)
    allowed_kinds = {"parish", "monastery"}
    for parent, source_rows in ROWS.items():
        rows = []
        branch_seen = {parent}
        for source in source_rows:
            row = clean(source)
            work_id = row.get("id")
            if not work_id or work_id in seen:
                raise ValueError("duplicate or missing id: %s" % work_id)
            if row.get("parent") not in branch_seen:
                raise ValueError("%s hangs off an unknown branch parent: %s" %
                                 (work_id, row.get("parent")))
            if row.get("kind") not in allowed_kinds:
                raise ValueError("%s has unsupported kind: %s" %
                                 (work_id, row.get("kind")))
            if row.get("kind") == "parish" and not row.get("local"):
                raise ValueError("%s is a parish without its own name" %
                                 work_id)
            if row.get("country") != "JP":
                raise ValueError("%s is outside Japan" % work_id)
            if not row.get("name") or not row.get("local"):
                raise ValueError("%s lacks a name" % work_id)
            if row.get("site") and not row["site"].startswith("http"):
                raise ValueError("%s carries a non-URL site" % work_id)
            seen.add(work_id)
            branch_seen.add(work_id)
            rows.append(row)
        payloads[parent] = {
            "v": 1,
            "parent": parent,
            "country": "JP",
            "rows": rows,
        }
    expected = {"jp-tokyo": 18, "jp-east": 29, "jp-west": 14}
    actual = {parent: len(payload["rows"])
              for parent, payload in payloads.items()}
    if actual != expected:
        raise ValueError("Japan branch counts changed: %s" % actual)
    return payloads


def manifest(payloads=None):
    payloads = payloads or build()
    return {
        parent: {
            "url": "/data/directory/%s.v1.json" % parent,
            "count": len(payload["rows"]),
            "country": payload["country"],
        }
        for parent, payload in sorted(payloads.items())
    }


def encoded(payload):
    return json.dumps(payload, ensure_ascii=False,
                      separators=(",", ":")).encode("utf-8")


def output_path(parent):
    return OUT / ("%s.v1.json" % parent)


def write(payloads):
    OUT.mkdir(parents=True, exist_ok=True)
    for parent, payload in sorted(payloads.items()):
        path = output_path(parent)
        path.write_bytes(encoded(payload))
        print("wrote %s (%d rows)" %
              (path.relative_to(ROOT), len(payload["rows"])))


def problems(payloads):
    errors = []
    expected = set()
    for parent, payload in sorted(payloads.items()):
        path = output_path(parent)
        expected.add(path.name)
        if not path.exists():
            errors.append("missing %s" % path.relative_to(ROOT))
        elif path.read_bytes().replace(b"\r\n", b"\n") != encoded(payload):
            errors.append("stale %s" % path.relative_to(ROOT))
    if OUT.exists():
        for path in OUT.glob("jp-*.v1.json"):
            if path.name not in expected:
                errors.append("unexpected %s" % path.relative_to(ROOT))
    return errors


def main():
    parser = argparse.ArgumentParser()
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument("--write", action="store_true")
    mode.add_argument("--check", action="store_true")
    args = parser.parse_args()
    try:
        payloads = build()
        if args.write:
            write(payloads)
        errors = problems(payloads)
    except (OSError, ValueError) as exc:
        print("directory Japan: %s" % exc, file=sys.stderr)
        return 1
    if errors:
        for error in errors:
            print(error, file=sys.stderr)
        return 1
    print("Japan branches: 3 dioceses, 61 parishes and missions")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
