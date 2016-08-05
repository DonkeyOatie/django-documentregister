from __future__ import unicode_literals

from django.db import models
from django.utils.translation import ugettext_lazy as _


class DocumentType(models.Model):

    """
    Define the document type
    """

    class Meta:
        verbose_name = _('Document Type')
        verbose_name_plural = _('Document Types')

    def __str__(self):
        return '{} - {}'.format(self.document_type_short, self.document_type_long)

    document_type_short = models.CharField(
        _('Document Type Short'),
        max_length=5,
        null=False,
        blank=False,
        unique=True,
        db_index=True
    )

    document_type_long = models.CharField(
        _('Document Type Long'),
        max_length=50,
        null=False,
        blank=False
    )

    description = models.TextField(
        _('Document Type Description'),
        null=False,
        blank=False
    )


class Document(models.Model):

    """
    Represents an instance of a registered document
    """

    class Meta:
        verbose_name = _('Document')
        verbose_name_plural = _('Documents')

    document_type = models.ForeignKey(
        DocumentType
    )

    title = models.CharField(
        _('Title'),
        max_length=256,
        null=False,
        blank=False,
        db_index=True
    )

    description = models.TextField(
        _('Description'),
        null=False,
        blank=False
    )

    link = models.URLField(
        _('Document Link'),
        null=False,
        blank=False
    )

    author_name = models.CharField(
        _('Author Name'),
        max_length=100,
        null=False,
        blank=False,
        db_index=True
    )

    author_email = models.EmailField(
        _('Author Email Address'),
        db_index=True
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
        db_index=True
    )

    @property
    def tag(self):
        return self.document_type.document_type_short + str(self.pk).zfill(5)

    @property
    def full_title(self):
        return '{} {}'.format(self.tag, self.title)
