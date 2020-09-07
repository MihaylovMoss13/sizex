import re

from django.urls import reverse
from django.db import models
from django.conf import settings

from mptt.models import MPTTModel, TreeForeignKey
from ckeditor_uploader.fields import RichTextUploadingField
from django.utils.translation import ugettext as _
from django.utils.safestring import mark_safe

from .changer import changer

PROTOCOL_CHOICES = (
    ('http://', 'http'),
    ('https://', 'https')
)


class Domain(models.Model):
    protocol = models.CharField(
        verbose_name=_('Протокол'),
        max_length=255,
        blank=True,
        default='http://',
        choices=PROTOCOL_CHOICES
    )
    domain = models.CharField(verbose_name=_('Домен'), max_length=255, blank=True)
    scripts = models.TextField(verbose_name=_('Доп. скрипты'), blank=True, null=True)
    name = models.CharField(verbose_name=_('Название региона'), max_length=255, blank=True)

    def __str__(self):
        return self.domain

    class Meta:
        verbose_name = _('Домен')
        verbose_name_plural = _('Домены')


class PagesManager(models.Manager):
    def get_queryset(self):
        return super(PagesManager, self).get_queryset().select_related('domain')


class Pages(MPTTModel):
    # Base parameters
    name = models.CharField(verbose_name=_('Название страницы'), max_length=255)
    h1 = models.CharField(verbose_name=_('h1 страницы'), max_length=255, blank=True, null=True)
    alias = models.CharField(verbose_name=_('Ссылка на страницу'), max_length=255, blank=True)
    replace = models.BooleanField(verbose_name=_('Не подменять пустой alias'), default=False)
    parent = TreeForeignKey(
        'self',
        null=True,
        blank=True,
        related_name='children',
        verbose_name='Родитель',
        on_delete=models.CASCADE
    )
    text = RichTextUploadingField(verbose_name=_('Текст страницы'), blank=True, null=True)
    domain = models.ForeignKey(Domain, verbose_name=_('Домен'), on_delete=models.CASCADE, default=1)

    # Meta parameters
    title = models.CharField(verbose_name=_('Заголовок страницы'), max_length=1000, blank=True)
    meta_d = models.CharField(verbose_name=_('Ключевое описание'), max_length=1000, blank=True)

    # Active
    status = models.BooleanField(verbose_name=_('Вкл?'), default=True)
    is_link = models.BooleanField(verbose_name=_('Проставлять ссылку?'), default=True)
    template = models.CharField(verbose_name=_('Кастомный шаблон для поддоменов'), max_length=255, blank=True)
    ymap = models.TextField(verbose_name=_('Карта'), blank=True, null=True)
    address = models.CharField(verbose_name=_(u'Адрес офиса'), max_length=255, blank=True)

    created_at = models.DateTimeField(verbose_name=_('Дата и время создания'), auto_now_add=True)
    update_at = models.DateTimeField(verbose_name=_('Дата и время последнего обновления'), auto_now=True)

    objects = PagesManager()

    @mark_safe
    def clear_cache(self):
        return '<a href="%s"><span class="icon-refresh"></span></a>' % reverse(
            'clear_cache',
            kwargs={'pk': self.id}
        )

    clear_cache.short_description = _('Кэш')


    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = _('Страницы сайта')
        ordering = ['lft']

    def get_children(self):
        return Pages.objects.filter(parent=self).filter(status=True)

    def get_unique_alias(self, alias, num=0):
        num += 1
        pages = Pages.objects.filter(alias=alias)
        if len(pages) != 0:
            if len(pages) == 1 and pages[0].id == self.id:
                return alias

            alias = alias + '-' + str(num)
            return self.get_unique_alias(alias, num)
        return alias

    def get_prealias(self, alias, obj):
        if obj.parent:
            if obj.parent.alias not in ['verhnee_meny', 'levoe_meny']:
                alias = obj.parent.alias + '/' + self.alias
                self.get_prealias(alias, obj.parent)
        return alias

    def change_alias(self):
        alias = self.get_prealias('', self)

        for item in self.name.lower():
            if item in changer:
                alias += changer[item]
            else:
                alias += item
        alias = re.sub('[^A-Za-z0-9-/_\s]+', '', alias)
        alias = re.sub('-{2,10}', '-', alias)
        self.alias = self.get_unique_alias(alias)

    def save(self, *args, **kwargs):
        if not self.title:
            self.title = self.name

        if not self.h1:
            self.h1 = self.name

        if self.alias == '' and not self.replace:
            self.change_alias()

        if hasattr(self, 'title_en'):
            if not self.title_en:
                self.title_en = self.name_en

            if not self.h1_en:
                self.h1_en = self.name_en

        super(Pages, self).save(*args, **kwargs)

    def get_absolute_url(self):
        alias = reverse('page', kwargs={'slug': self.alias}) if self.alias else ''
        return self.domain.protocol + self.domain.domain + alias

    def get_host_url(self):
        if self.alias:
            return self.domain.protocol + self.domain.domain + reverse('page', kwargs={'slug': self.alias})
        else:
            return self.domain.protocol + self.domain.domain


CODE_CHOICES = (
    ('0', 301),
    ('1', 302),
)

class Redirect(models.Model):
    fr = models.CharField(verbose_name=_('Откуда'), max_length=1023)
    to = models.CharField(verbose_name=_('Куда'), max_length=1023)
    code = models.CharField(verbose_name=_('Код'), max_length=255, choices=CODE_CHOICES, default='0')
    domain = models.ForeignKey(Domain, verbose_name=_('Домен'), on_delete=models.CASCADE)

    def __str__(self):
        return str(self.id)

    class Meta:
        verbose_name = _('Редирект')
        verbose_name_plural = _('Редиректы')



class Feedback(models.Model):
    name = models.CharField(verbose_name=_('Имя'), max_length=255)
    email = models.CharField(verbose_name=_('Электронная почта'), max_length=255, blank=True)
    phone = models.CharField(verbose_name=_('Телефон'), max_length=255)
    comment = models.TextField(verbose_name=_('Комментарий'), blank=True, null=True)

    created_at = models.DateTimeField(verbose_name=_('Дата и время создания'), auto_now_add=True)
    update_at = models.DateTimeField(verbose_name=_('Дата и время последнего обновления'), auto_now=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _('Заявка')
        verbose_name_plural = _('Заявки')


class Block(models.Model):
    name = models.CharField(verbose_name=_('Название блока'), max_length=255, blank=True)
    html = RichTextUploadingField(verbose_name=_('Html блока'), blank=True, null=True)
    html_mobile = RichTextUploadingField(verbose_name=_('Html мобильного блока'), blank=True, null=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _('Html блок')
        verbose_name_plural = _('Html блоки')


class IndexBlock(models.Model):
    name = models.CharField(verbose_name=_('Название'), max_length=255, blank=True)
    link = models.CharField(verbose_name=_('Ссылка'), max_length=255, blank=True)
    image = models.ImageField(upload_to='gallery', verbose_name=_('Картинка'))
    status = models.BooleanField(verbose_name=_(u'Вкл?'), default=True)
    order = models.PositiveIntegerField(default=0, verbose_name=_('Очередность'), blank=False, null=False)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _(u'Блок на главную')
        verbose_name_plural = _(u'Блоки для главной')
        ordering = ('order',)


class PagesBlock(models.Model):
    page = models.ForeignKey(Pages, verbose_name=_('Страница'), on_delete=models.CASCADE)
    block = models.ForeignKey(Block, verbose_name=_('Блок'), on_delete=models.CASCADE)
    html = RichTextUploadingField(
        verbose_name=_('Переопределяющий HTML для блока'),
        blank=True,
        null=True,
        config_name='inline'
    )

    html_mobile = RichTextUploadingField(
        verbose_name=_('Переопределяющий Html мобильного блока'),
        blank=True,
        null=True,
        config_name='inline'
    )

    order = models.PositiveIntegerField(verbose_name=_('Очередность'), blank=True, null=True, default=0)

    class Meta:
        verbose_name = _('Соотношение блока и страницы')
        verbose_name_plural = _('Соотношение блоков и страниц')
        ordering = ('order',)

BLOCK_TYPE_CHOICES = (
    (0, 'title'),
    (1, 'desc'),
    (3, 'Название в меню'),
    (4, 'Галерея'),
    (5, 'Цены'),
)


class Grammeme(models.Model):
    name = models.CharField(verbose_name=_('Название граммемы'), max_length=255, blank=True)
    gramm = models.CharField(verbose_name=_('Граммема'), max_length=255)

    def __str__(self):
        return self.name


TRANSFORM_CHOICES = (
    (0, 'Маленькими буквами'),
    (1, 'С большой буквы'),
    (2, 'Большими буквами'),
)

PREPEND_CHOICES = (
    (True, 'В начало'),
    (False, 'В конец'),
)

ACTIVE_CHOICES = (
    (True, 'Подменять'),
    (False, 'Не подменять')
)


class PagesBlockGrammeme(models.Model):
    page = models.ForeignKey(Pages, verbose_name=_('Страница'), blank=True, null=True, on_delete=models.CASCADE)
    block_type = models.SmallIntegerField(verbose_name=_('Тип блока'), blank=True, choices=BLOCK_TYPE_CHOICES)
    active = models.BooleanField(verbose_name=_('Использовать граммему?'), default=True, choices=ACTIVE_CHOICES)
    gramms = models.ManyToManyField(Grammeme, verbose_name=_('Граммемы'))
    number = models.IntegerField(verbose_name=_('Номер граммемы'), blank=True, null=True)
    prepend = models.BooleanField(verbose_name=_('Куда?'), default=False, choices=PREPEND_CHOICES)
    transform = models.IntegerField(verbose_name=_('Трансформация текста'), default=0, choices=TRANSFORM_CHOICES)

    @mark_safe
    def show_gramms(self):
        return ', '.join([g.name for g in self.gramms.all()])

    class Meta:
        verbose_name = _('Граммема')
        verbose_name_plural = _('Граммемы')
