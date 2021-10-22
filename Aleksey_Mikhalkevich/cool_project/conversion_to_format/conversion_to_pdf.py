from pathlib import Path

from fpdf import FPDF


class PDF(FPDF):

    def body(self, data):
        if not self.is_list(data[0]):
            data = [data]

        for feed in data:
            self.cell(0, 5, f'Channel title: {feed[0]["channel_title"]}', align="C", ln=1)
            self.cell(0, 5, f'Source: {feed[0]["source"]}', align="C", ln=1)
            for news in feed[1:]:
                self.cell(0, 5, f"{'-' * 125}", align="C", ln=1)

                if news["title"]:
                    self.multi_cell(0, 5, f"Title: {news['title']}")
                    self.ln()
                if news["date"]:
                    self.multi_cell(0, 5, f"date of publication: {news['date']}")
                    self.ln()
                if news["link"]:
                    self.multi_cell(0, 5, f"Link: {news['link']}")
                    self.ln()
                if news["author"]:
                    self.multi_cell(0, 5, f"Author: {news['author']}")
                    self.ln()

                if news["category"]:
                    if self.is_list(news["category"]):
                        for category in news["category"]:
                            self.cell(0, 5, "Categories: ", ln=1)
                            self.multi_cell(0, 5, f"{' ' * 5}{category}")
                    else:
                        self.multi_cell(0, 5, f"Category: {news['category']}")
                    self.ln("10")

                if news["description"]:
                    self.multi_cell(0, 5, f"Description: {news['description']}")
                    self.ln("10")
                if news["more_description"]:
                    self.multi_cell(0, 5, f"More description: {news['more_description']}")
                    self.ln("10")
                if news["comments"]:
                    self.multi_cell(0, 5, f"Comments: {news['comments']}")
                    self.ln()

                if news["media_object"]:
                    if self.is_list(news["media_object"]):
                        for media in news["media_object"]:
                            self.cell(0, 5, "Media objects: ", ln=1)
                            self.multi_cell(0, 5, f"{' ' * 5}{media}")
                    else:
                        self.multi_cell(0, 5, f"Media object: {news['media_object']}")
                    self.ln()

                if news["extra_links"]:
                    if self.is_list(news["extra_links"]):
                        for extra_link in news["extra_links"]:
                            self.cell(0, 5, "Extra links: ", ln=1)
                            self.multi_cell(0, 5, f"{' ' * 5}{extra_link}")
                    else:
                        self.multi_cell(0, 5, f"Extra link: {news['extra_links']}")
                    self.ln()

                if news["source_feed"]:
                    if self.is_list(news["source_feed"]):
                        for source in news["source_feed"]:
                            self.cell(0, 5, "Sources: ", ln=1)
                            self.multi_cell(0, 5, f"{' ' * 5}{source}")
                    else:
                        self.multi_cell(0, 5, f"Source: {news['source_feed']}")

                self.cell(0, 5, f"{'-' * 125}", align="C")
                self.ln("20")

    def footer(self):
        self.set_y(-10)
        self.set_font("DejaVu", "", 15)
        self.cell(0, 5, f"Page {str(self.page_no())}", 0, 0, "C")

    @staticmethod
    def is_list(obj):
        return isinstance(obj, list)


def convertor_to_pdf(data, path, verbose):
    pdf = PDF()
    pdf.alias_nb_pages()
    pdf.add_page()
    path_to_ttf = Path(Path(__file__).parent, "files_for_pdf", "DejaVuSansCondensed.ttf")
    pdf.add_font("DejaVu", "", path_to_ttf, uni=True)
    pdf.set_font("DejaVu", "", 14)
    pdf.set_auto_page_break(True, 10)
    pdf.body(data)
    pdf.output("feed.pdf", "F")


DATA = [{'channel_title': 'Люди Onlíner', 'source': 'https://people.onliner.by/feed'},
        {'title': 'За сутки от коронавируса умерли 16 человек. Данные от Минздрава',
         'date': 'Fri, 22 Oct 2021 15:54:48 +0300',
         'link': 'https://people.onliner.by/2021/10/22/za-sutki-ot-koronavirusa-umerli', 'author': None,
         'category': ['Коронавирус в Беларуси'],
         'description': 'Минздрав опубликовал новую сводку по ситуации с коронавирусом. По официальным данным, за очередные сутки зарегистрированы 2082 пациента с COVID-19. Выписаны 2034. Умерли 16.Читать далее…',
         'more_description': None, 'comments': None,
         'media_object': ['https://content.onliner.by/news/thumbnail/f36804945f613170d4e24f09da9a2697.jpeg'],
         'extra_links': 'https://people.onliner.by/2021/10/22/za-sutki-ot-koronavirusa-umerli', 'source_feed': None},
        {'title': 'Обязательное ношение масок отменено. Но Минздрав рекомендует\xa0(дополнено)',
         'date': 'Fri, 22 Oct 2021 14:17:49 +0300',
         'link': 'https://people.onliner.by/2021/10/22/maski-uzhe-ne-vezde-obyazatelny', 'author': None,
         'category': ['Коронавирус в Беларуси'],
         'description': 'Минздрав сегодня немного путано\xa0объявил\xa0про новую тактику санитарно-противоэпидемических мероприятий в\xa0отношении COVID-19. Из сообщения следует, в частности, что отменяется требование об\xa0обязательном использовании средств индивидуальной защиты при посещении некоторых (не\xa0всех) объектов и\xa0организаций, транспорта. Возможно, это отзвук недавнего большого совещания по ковиду — исполняют и\xa0«актуализируют».Читать далее…',
         'more_description': None, 'comments': None,
         'media_object': ['https://content.onliner.by/news/thumbnail/a3713e5fe17a16f7f46eb678cbca4c49.jpeg'],
         'extra_links': 'https://people.onliner.by/2021/10/22/maski-uzhe-ne-vezde-obyazatelny', 'source_feed': None},
        {'title': 'Челлендж. Наши читатели показали, как убрали рабочие столы',
         'date': 'Fri, 22 Oct 2021 14:11:00 +0300',
         'link': 'https://people.onliner.by/2021/10/22/chellendzh-nashi-chitateli-pokazali-kak-ubrali-rabochie-stoly',
         'author': None, 'category': ['Социум'],
         'description': 'В четверг мы запустили очередную серию челленджа «Хорошие белорусы». Идея была следующая. Усердная работа нередко превращает наши рабочие столы в завалы из книг, мусора, бумаги, документов и прочих вещей. И в разгар буднего дня мы попросили читателей провести у себя на рабочем месте косметическую уборку. Чем закончился очередной челлендж, смотрите ниже.Читать далее…',
         'more_description': None, 'comments': None,
         'media_object': ['https://content.onliner.by/news/thumbnail/0200e7bfb17fb4c5f084eb12aedc788a.jpeg'],
         'extra_links': 'https://people.onliner.by/2021/10/22/chellendzh-nashi-chitateli-pokazali-kak-ubrali-rabochie-stoly',
         'source_feed': None}, {
            'title': '5 тонн продукции неизвестного происхождения пытались ввезти в РФ из Беларуси. Рыбу сожгли, мясо закопали',
            'date': 'Fri, 22 Oct 2021 12:30:20 +0300',
            'link': 'https://people.onliner.by/2021/10/22/vvezennuyu-iz-belarusi-rybu-i', 'author': None,
            'category': ['Происшествия'],
            'description': 'В Смоленской области уничтожено более 3 тонн европейской рыбной продукции, которую пытались нелегально ввезти из Беларуси, а также 2,5 тонны мяса без документов, сообщили\xa0агентству «Интерфакс-Запад» в Россельхознадзоре. Ввозили продукцию на двух машинах в объезд официальных ветеринарных постов. Рыбу и говядину спрятали за ящиками с чипсами, но это не помогло: рыбу сожгли, мясо закопали.Читать далее…',
            'more_description': None, 'comments': None,
            'media_object': ['https://content.onliner.by/news/thumbnail/4815335422bd8d0ae75c959d2ac58413.jpeg'],
            'extra_links': 'https://people.onliner.by/2021/10/22/vvezennuyu-iz-belarusi-rybu-i', 'source_feed': None},
        {'title': 'Десять историй хитроумных афер — какая из них правдивая? Тест\xa0(спецпроект)',
         'date': 'Fri, 22 Oct 2021 11:00:32 +0300',
         'link': 'https://people.onliner.by/2021/10/22/desyat-istorij-afer-test', 'author': None,
         'category': ['Без рубрики'],
         'description': 'История насчитывает столько случаев хитроумных афер, ограблений и прочих незаконных (но очень уж впечатляющих) махинаций, что хватит еще на сотни голливудских сценариев. Иногда бывает сложно поверить, что это не выдуманный кем-то случай, а настоящий результат эксперимента по смешиванию человеческой изобретательности и жажды наживы. В новом тесте, который мы сделали вместе с Parimatch, предлагаем вам почитать десять коротких историй афер и понять, какие из них правдивые, а какие нет. И в который раз убедиться, что жизнь интереснее вымысла.Читать далее…',
         'more_description': None, 'comments': None,
         'media_object': ['https://content.onliner.by/news/thumbnail/43bda77cb3bcf10cfd00faaf6ac278d0.jpeg'],
         'extra_links': 'https://people.onliner.by/2021/10/22/desyat-istorij-afer-test', 'source_feed': None},
        {'title': 'Буря в пустыне: как Полесье зарастает барханами \xa0(видео)',
         'date': 'Fri, 22 Oct 2021 09:49:46 +0300',
         'link': 'https://people.onliner.by/2021/10/22/kak-polese-zarastaet-barxanami', 'author': None,
         'category': ['Социум'],
         'description': 'Это Столинский район, недалеко от границы с Житковичским: небольшие барханы и песчаная буря. Верблюдов пока не видели, но тоже скоро заведутся. В последние лет десять-пятнадцать это красивое зрелище становится все более обычным для нашей страны. Страдает в том числе Полесье, которое когда-то славилось болотами и плодородными (если осушить) торфяниками. На снимках как раз эти самые благодатные торфяники\xa0— то, во что мы их превратили.Читать далее…',
         'more_description': None, 'comments': None,
         'media_object': ['https://content.onliner.by/news/thumbnail/2e57fd13726f020260d9f516fd137a64.jpeg'],
         'extra_links': 'https://people.onliner.by/2021/10/22/kak-polese-zarastaet-barxanami', 'source_feed': None},
        {'title': 'В Украине на Сергея Михалка завели уголовное дело за драку со зрителем',
         'date': 'Thu, 21 Oct 2021 23:37:17 +0300',
         'link': 'https://people.onliner.by/2021/10/21/na-sergeya-mixolka-zaveli-delo', 'author': None,
         'category': ['Культура'],
         'description': 'На недавнем концерте группы «Ляпис 98» в Полтаве произошел инцидент: Сергей Михалок прямо во время выступления повздорил с одним из зрителей, вышедшим с гитарой на сцену. Зачем — до сих пор неизвестно. Конфликт начался со словесной перепалки: артист требовал, чтобы человек показал свой входной билет. В какой-то момент происходящее вылилось в драку: Михалок ударил оппонентаголовой. Видео случившегося опубликовал украинский телеграм-канал МВД.Читать далее…',
         'more_description': None, 'comments': None,
         'media_object': ['https://content.onliner.by/news/thumbnail/1bd96705316b7fa835e41de7908c1aa7.jpeg'],
         'extra_links': 'https://people.onliner.by/2021/10/21/na-sergeya-mixolka-zaveli-delo', 'source_feed': None},
        {'title': '«В ноябре расслабляться не стоит». Врач-инфекционист о распространении ковида в Беларуси',
         'date': 'Thu, 21 Oct 2021 22:22:59 +0300', 'link': 'https://people.onliner.by/2021/10/21/vrach-infekcionist',
         'author': None, 'category': ['Здоровье'],
         'description': 'Делать долгосрочные прогнозы нельзя, но в ноябре невозможно дать людям повод для радости и для того, чтобы расслабиться и забыть об этой инфекции. Об этом рассказал на телеканале ОНТ ректор Гомельского государственного медицинского университета, врач-инфекционист, доктор медицинских наук Игорь Стома.Читать далее…',
         'more_description': None, 'comments': None,
         'media_object': ['https://content.onliner.by/news/thumbnail/b6ac3a8e6fd14e447032fa6da6e78bb8.jpeg'],
         'extra_links': 'https://people.onliner.by/2021/10/21/vrach-infekcionist', 'source_feed': None},
        {'title': 'В Национальный календарь прививок внесена вакцинация от коронавируса',
         'date': 'Thu, 21 Oct 2021 19:19:58 +0300', 'link': 'https://people.onliner.by/2021/10/21/kalendar-privivok',
         'author': None, 'category': ['Здоровье'],
         'description': 'Вакцинацию от СOVID-19 внесли в Национальный календарь прививок, сообщает пресс-служба Министерства здравоохранения.Читать далее…',
         'more_description': None, 'comments': None,
         'media_object': ['https://content.onliner.by/news/thumbnail/3aec52ed0c77a0ef8bb4f1728bbf69b0.jpeg'],
         'extra_links': 'https://people.onliner.by/2021/10/21/kalendar-privivok', 'source_feed': None}, {
            'title': 'Может ли коронавирус привести к бесплодию? Говорим со специалистом о влиянии COVID-19 на фертильность',
            'date': 'Thu, 21 Oct 2021 17:00:10 +0300',
            'link': 'https://people.onliner.by/2021/10/21/govorim-s-medikom-o', 'author': None,
            'category': ['Здоровье'],
            'description': 'В начале октября с наплывом новой волны коронавируса Минздрав разрешил вакцинацию беременным женщинам. И это все неспроста, дело в том, что невакцинированные беременные очень часто переносят болезнь в тяжелой форме,\xa0пишет\xa0The Guardian. Мы поговорили со специалистом и узнали, может ли коронавирус привести к бесплодию и безопасна ли вакцинация беременных.Читать далее…',
            'more_description': None, 'comments': None,
            'media_object': ['https://content.onliner.by/news/thumbnail/199587603d4709c86d8ff9f38bda040c.jpeg'],
            'extra_links': 'https://people.onliner.by/2021/10/21/govorim-s-medikom-o', 'source_feed': None}]

if __name__ == '__main__':
    convertor_to_pdf(DATA, "", None)
