import pymorphy2
from bs4 import BeautifulSoup
import random

from django.db.models import Q
from pages.models import Pages, PagesBlockGrammeme, PagesBlock, Block
from django.core.management.base import BaseCommand

morph = pymorphy2.MorphAnalyzer()


def get_gramm(page, gramm_choice):
    gramm = PagesBlockGrammeme.objects.filter(page=page, block_type=gramm_choice).first()
    if not gramm:
        gramm = PagesBlockGrammeme.objects.filter(page=page.parent, block_type=gramm_choice).first()
    return gramm


def get_phrase(page, gramm):
    phrase = page.name
    if gramm and gramm.active:
        phrase = getattr(morph.parse(page.name)[gramm.number or 0].inflect(
            set((g.gramm for g in gramm.gramms.all()))
        ), 'word', page.name).lower()
        if gramm.transform == 1:
            phrase = phrase.capitalize()
        if gramm.transform == 2:
            phrase = phrase.upper()
    return phrase


def get_name(page1, page2):
    """ Phrase for menu """
    gramm1 = get_gramm(page1, 3)
    gramm2 = get_gramm(page2, 3)
    phrase = []
    phrase1 = get_phrase(page1, gramm1)
    phrase2 = get_phrase(page2, gramm2)
    phrase.insert(0, phrase1) if gramm1 and gramm1.prepend else phrase.append(phrase1)
    phrase.insert(0, phrase2) if gramm2 and gramm2.prepend else phrase.append(phrase2)
    phrase[0] = phrase[0].capitalize()
    return ' '.join(phrase)

def get_h1(page1, page2):
    """ Phrase for menu """
    gramm1 = get_gramm(page1, 3)
    gramm2 = get_gramm(page2, 3)
    phrase = ['натяжные потолки']
    phrase1 = get_phrase(page1, gramm1)
    phrase2 = get_phrase(page2, gramm2)
    phrase.insert(0, phrase1) if gramm1 and gramm1.prepend else phrase.append(phrase1)
    phrase.insert(0, phrase2) if gramm2 and gramm2.prepend else phrase.append(phrase2)
    phrase[0] = phrase[0].capitalize()
    return ' '.join(phrase)


def get_gallery(page1, page2):
    """ Phrase for gallery """
    gramm1 = get_gramm(page1, 4)
    gramm2 = get_gramm(page2, 4)
    phrase = ['натяжных потолков']
    phrase1 = get_phrase(page1, gramm1)
    phrase2 = get_phrase(page2, gramm2)
    phrase.insert(0, phrase1) if gramm1 and gramm1.prepend else phrase.append(phrase1)
    phrase.insert(0, phrase2) if gramm2 and gramm2.prepend else phrase.append(phrase2)
    phrase.insert(0, 'Галерея')
    return ' '.join(phrase)


def get_price(page1, page2):
    """ Phrase for gallery """
    gramm1 = get_gramm(page1, 3)
    gramm2 = get_gramm(page2, 3)
    phrase = ['натяжныe потолки']
    phrase1 = get_phrase(page1, gramm1)
    phrase2 = get_phrase(page2, gramm2)
    phrase.insert(0, phrase1) if gramm1 and gramm1.prepend else phrase.append(phrase1)
    phrase.insert(0, phrase2) if gramm2 and gramm2.prepend else phrase.append(phrase2)
    phrase.insert(0, 'Цены на')
    return ' '.join(phrase)


def get_title(page1, page2):
    """ Phrase for title """
    gramm1 = get_gramm(page1, 3)
    gramm2 = get_gramm(page2, 3)
    phrase = ['натяжныe потолки']
    phrase1 = get_phrase(page1, gramm1)
    phrase2 = get_phrase(page2, gramm2)
    phrase.insert(0, phrase1) if gramm1 and gramm1.prepend else phrase.append(phrase1)
    phrase.insert(0, phrase2) if gramm2 and gramm2.prepend else phrase.append(phrase2)
    phrase.append(' - цена за 1м2 / Купить')
    phrase[0] = phrase[0].capitalize()
    # Add second phrase
    sphrase = ['натяжной потолок']
    gramm1 = get_gramm(page1, 0)
    gramm2 = get_gramm(page2, 0)
    phrase1 = get_phrase(page1, gramm1)
    phrase2 = get_phrase(page2, gramm2)
    sphrase.insert(0, phrase1) if gramm1 and gramm1.prepend else sphrase.append(phrase1)
    sphrase.insert(0, phrase2) if gramm2 and gramm2.prepend else sphrase.append(phrase2)
    phrase.append(' '.join(sphrase))
    return ' '.join(phrase)


def get_desc(page1, page2):
    """ Phrase for description """
    gramm1 = get_gramm(page1, 0)
    gramm2 = get_gramm(page2, 0)
    phrase = ['натяжной потолок']
    phrase1 = get_phrase(page1, gramm1)
    phrase2 = get_phrase(page2, gramm2)
    phrase.insert(0, phrase1) if gramm1 and gramm1.prepend else phrase.append(phrase1)
    phrase.insert(0, phrase2) if gramm2 and gramm2.prepend else phrase.append(phrase2)
    phrase.append('по лучшей цене с установкой в Москве.')
    phrase.insert(0, 'Заказать')
    return ' '.join(phrase)


def get_text(page1, page2):
    number = random.randint(0, 4)
    if number == 0:
        text = """
        <p>
        Интерьеры квартир в Москве и Московской области требуют оригинальных современных решений.
        {phrase} - это один из самых интересных вариантов.
        Цена за 1 м2 такого изделия разная, зависит от многих параметров.
        Специалисты нашей компании могут подобрать идеальный вариант для вас,
        создав эстетически привлекательную, ровную поверхность.
        </p>
        """
        gramm1 = get_gramm(page1, 0)
        gramm2 = get_gramm(page2, 0)
        phrase = ['натяжной потолок']
        phrase1 = get_phrase(page1, gramm1)
        phrase2 = get_phrase(page2, gramm2)
        phrase.insert(0, phrase1) if gramm1 and gramm1.prepend else phrase.append(phrase1)
        phrase.insert(0, phrase2) if gramm2 and gramm2.prepend else phrase.append(phrase2)
        phrase[0] = phrase[0].capitalize()
        return text.format(phrase=' '.join(phrase))

    if number == 1:
        text = """
        <p>
        Эксклюзивный ремонт — мечта многих, однако добиться неповторимого внешнего вида в помещении с помощью одних только стен, мебели и декора зачастую невозможно.
        С этой целью стоит заказать в квартиру {phrase} из каталога нашей компании.
        </p>
        """
        gramm1 = get_gramm(page1, 3)
        gramm2 = get_gramm(page2, 3)
        phrase = ['натяжные потолоки']
        phrase1 = get_phrase(page1, gramm1)
        phrase2 = get_phrase(page2, gramm2)
        phrase.insert(0, phrase1) if gramm1 and gramm1.prepend else phrase.append(phrase1)
        phrase.insert(0, phrase2) if gramm2 and gramm2.prepend else phrase.append(phrase2)
        return text.format(phrase=' '.join(phrase))

    if number == 2:
        return """
        <p>
        Широкое разнообразие цветов, фактур, рисунков и других вариантов дизайна и монтажа позволяет подобрать оптимальный натяжной потолок для интерьера любого ресторана, бара или кафе.
        В ассортименте компании «Сайзекс» найдется подходящее решение независимо от направленности заведения, площади и ценовых предпочтений.
        </p>
        """

    if number == 3:
        text = """
        <p>
        Мы привыкли видеть красивые обои или плитку у себя под ногами.
        А между тем не менее экстравагантно и богато смотрятся и {phrase}, заказать монтаж которых можно по фиксированной цене за м2 у нас.
        </p>
        """
        gramm1 = get_gramm(page1, 3)
        gramm2 = get_gramm(page2, 3)
        phrase = ['натяжные потолоки']
        phrase1 = get_phrase(page1, gramm1)
        phrase2 = get_phrase(page2, gramm2)
        phrase.insert(0, phrase1) if gramm1 and gramm1.prepend else phrase.append(phrase1)
        phrase.insert(0, phrase2) if gramm2 and gramm2.prepend else phrase.append(phrase2)
        return text.format(phrase=' '.join(phrase))

    if number == 4:
        text = """
        <p>
        Все чаще при оформлении интерьеров дизайнеры отдают предпочтение современному стилю с плавным очертанием предметов и отсутствием четких границ.
        Очень гармонично в нем смотрятся и {phrase}, заказать которые можно по приемлемой цене за м2 в каталогах ведущих производителей.
        </p>
        """
        gramm1 = get_gramm(page1, 3)
        gramm2 = get_gramm(page2, 3)
        phrase = ['натяжные потолоки']
        phrase1 = get_phrase(page1, gramm1)
        phrase2 = get_phrase(page2, gramm2)
        phrase.insert(0, phrase1) if gramm1 and gramm1.prepend else phrase.append(phrase1)
        phrase.insert(0, phrase2) if gramm2 and gramm2.prepend else phrase.append(phrase2)
        return text.format(phrase=' '.join(phrase))


class Command(BaseCommand):
    help = "Create pages"
    def add_arguments(self, parser):
        parser.add_argument('--counter', type=int, required=True, help='Number of pages which will create.')

    def handle(self, *args, **kwargs):
        catalog = Pages.objects.filter(name='Каталог').first()
        parents = catalog.get_children()
        counter = 0

        for parent in parents:
            parents2 = [p for p in parents if p != parent]
            for page1 in parent.get_children():
                for parent2 in parents2:
                    for page2 in parent2.get_children():
                        counter += 1
                        if counter > kwargs.get('counter'):
                            exit()
                        name = get_name(page1, page2)
                        h1 = get_h1(page1, page2)
                        gallery = get_gallery(page1, page2)
                        price = get_price(page1, page2)
                        title = get_title(page1, page2)
                        desc = get_desc(page1, page2)
                        text = get_text(page1, page2)
                        newpage, crtd = Pages.objects.get_or_create(
                            parent=page1,
                            h1=name,
                            name=name,
                            title=title,
                            meta_d=desc,
                        )
                        if crtd:
                            newpage.status = False
                        newpage.alias.replace('//', '/')
                        newpage.alias += '/' if newpage.alias[-1] != '/' else ''
                        newpage.save()
                        empty_block = Block.objects.filter(name='Empty Block').first()
                        ready_block = Block.objects.filter(name='Калькулятор + готовый рассчет').first()
                        price_block = Block.objects.filter(name='Таблица с ценами').first()
                        feedback_block = Block.objects.filter(name=random.choice([
                            'Вызвать замерщика(первый тип)',
                            'Вызвать замерщика(второй тип)',
                            'Вызвать замерщика(третий тип)'
                        ])).first()
                        excellent_block = Block.objects.filter(name='Наши преимущества').first()
                        hot_block = Block.objects.filter(name='Горячие предложения').first()
                        gallery_block = PagesBlock.objects.filter(Q(page=page1) | Q(page=page2)).filter(html__icontains='Галерея').first()
                        if PagesBlock.objects.filter(page=newpage).count() == 0:
                            html = '<div class="uk-container content"><h1>' + h1 + '</h1>' + text + '</div>'
                            pb = PagesBlock.objects.create(
                                block=empty_block,
                                page=newpage,
                                html=html,
                                order=1,
                                html_mobile=html
                            )
                            if ready_block:
                                pb = PagesBlock.objects.create(
                                    block=ready_block,
                                    order=2,
                                    page=newpage
                                )
                            if price_block:
                                html = '<div class="uk-container content"><div class="h2">' + price + '</div></div>'
                                pb = PagesBlock.objects.create(
                                    block=empty_block,
                                    page=newpage,
                                    html=html,
                                    order=3,
                                    html_mobile=html
                                )
                                pb = PagesBlock.objects.create(
                                    block=price_block,
                                    order=4,
                                    page=newpage
                                )
                            if feedback_block:
                                pb = PagesBlock.objects.create(
                                    block=feedback_block,
                                    order=5,
                                    page=newpage
                                )
                            if gallery_block:
                                soup = BeautifulSoup(gallery_block.html, "html.parser")
                                soup.find(class_='h2').contents[0].replace_with(gallery)
                                soup_mobile = BeautifulSoup(gallery_block.html_mobile, "html.parser")
                                soup_mobile.find(class_='h2').contents[0].replace_with(gallery)
                                pb = PagesBlock.objects.create(
                                    block=empty_block,
                                    page=newpage,
                                    order=6,
                                    html=str(soup),
                                    html_mobile=str(soup_mobile)
                                )
                            if excellent_block:
                                pb = PagesBlock.objects.create(
                                    order=7,
                                    block=excellent_block,
                                    page=newpage
                                )
                            if hot_block:
                                pb = PagesBlock.objects.create(
                                    order=8,
                                    block=hot_block,
                                    page=newpage
                                )
