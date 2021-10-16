Package description
===
This package contains modules which implement serializers process

##serializers.py
This module contains function where happened serializers process. 
Input XML data type serialize to Python data type. 

For example:

    <item>
        <title>
            <![CDATA[ Стварыла бюсты Касцюшкі, Горкага, Чайкоўскага і ратавала яўрэяў у Кобрыне. Гісторыя скульптаркі Бальбіны Світыч-Відацкай ]]>
        </title>
        <link>https://people.onliner.by/2021/10/16/stvaryla-byusty-kascyushki-horkaha-chajkouskaha</link>
        <pubDate>Sat, 16 Oct 2021 10:45:08 +0300</pubDate>
        <dc:creator>Onliner</dc:creator>
        <category>
            <![CDATA[ Социум ]]>
        </category>
        <guid isPermaLink="false">https://people.onliner.by/2021/10/16/stvaryla-byusty-kascyushki-horkaha-chajkouskaha</guid>
        <description>
            <![CDATA[ <p><a href="https://people.onliner.by/2021/10/16/stvaryla-byusty-kascyushki-horkaha-chajkouskaha"><img src="https://content.onliner.by/news/thumbnail/fa3015d720d358b025455c9ea7720961.jpeg" alt="" /></a></p><p>Наша гісторыя захоўвае мноства таямніц і імёнаў таленавітых суайчыннікаў, чые біяграфіі яшчэ дэталёва не вывучылі, не прааналізавалі для шырокіх колаў аўдыторыі. Сярод іх, напрыклад, даволі цікавая скульптарка Бальбіна Світыч-Відацкая. Яна даволі доўга жыла ў савецкай Беларусі, стварала мастацкія творы для філармоніі, драматычнага тэатра ў Брэсце, але ў пэўны момант была вымушана з’ехаць за мяжу. Што цікава, за кардонам яна таксама не разгубілася і працягвала ствараць, пакінуўшы пасля сябе змястоўную спадчыну. Хто такая Світыч-Відацкая і чым ейная гісторыя звязана з Магілёвам, расказвае мастацтвазнаўца Сяргей Харэўскі.</p><p><a href="https://people.onliner.by/2021/10/16/stvaryla-byusty-kascyushki-horkaha-chajkouskaha">Читать далее…</a></p> ]]>
        </description>
        <media:thumbnail url="https://content.onliner.by/news/thumbnail/fa3015d720d358b025455c9ea7720961.jpeg"/>
    </item>

serialize to:

    {
        "title": "Стварыла бюсты Касцюшкі, Горкага, Чайкоўскага і ратавала яўрэяў у Кобрыне. Гісторыя скульптаркі Бальбіны Світыч-Відацкай",
        "date": "Sat, 16 Oct 2021 10:45:08 +0300",
        "link": "https://people.onliner.by/2021/10/16/stvaryla-byusty-kascyushki-horkaha-chajkouskaha",
        "author": None,
        "category": [
            "Социум"
        ],
        "description": "Наша гісторыя захоўвае мноства таямніц і імёнаў таленавітых суайчыннікаў, чые біяграфіі яшчэ дэталёва не вывучылі, не прааналізавалі для шырокіх колаў аўдыторыі. Сярод іх, напрыклад, даволі цікавая скульптарка Б
        альбіна Світыч-Відацкая. Яна даволі доўга жыла ў савецкай Беларусі, стварала мастацкія творы для філармоніі, драматычнага тэатра ў Брэсце, але ў пэўны момант была вымушана з’ехаць за мяжу. Што цікава, за кардонам яна таксама не разгубі
        лася і працягвала ствараць, пакінуўшы пасля сябе змястоўную спадчыну. Хто такая Світыч-Відацкая і чым ейная гісторыя звязана з Магілёвам, расказвае мастацтвазнаўца Сяргей Харэўскі.Читать далее…",
        "more_description": None,
        "comments": None,
        "media_object":  [
            "https://content.onliner.by/news/thumbnail/fd77370a5d8bbd92140bef72b64038ba.jpeg"
        ],
        "extra_links": "https://people.onliner.by/2021/10/16/stvaryla-byusty-kascyushki-horkaha-chajkouskaha",
        "source_feed": None
    }

