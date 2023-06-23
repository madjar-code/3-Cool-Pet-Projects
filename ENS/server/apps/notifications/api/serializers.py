import re
from typing import List
from spellchecker import SpellChecker
from rest_framework import serializers
from rest_framework.serializers import (
    ModelSerializer,
    ValidationError,
)
from notifications.models import NotificationTemplate


class CreateNTSerializer(ModelSerializer):
    ignore_typos = serializers.BooleanField(default=False)
    class Meta:
        model = NotificationTemplate
        fields = (
            'id',
            'send_time',
            'title',
            'text',
            'created_at',
            'ignore_typos',
        )
        read_only_fields = (
            'id',
            'created_at',
        )
        write_only_fields = (
            'ignore_typos',
        )

    def check_spelling(self, text: str) -> List[str]:
        words = re.findall(r'\w+', text)
        spell_checker = SpellChecker()
        misspelled_words = spell_checker.unknown(words)
        return list(misspelled_words)

    def validate_title(self, title: str) -> str:
        ignore_typos = self.initial_data.get('ignore_typos', False)
        if not ignore_typos:
            misspelled_words = self.check_spelling(title)
            if misspelled_words:
                misspeled_words_string = ", ".join(misspelled_words)
                raise ValidationError('There are misspelled words: {}'.\
                                        format(misspeled_words_string))
        return title

    def validate_text(self, text: str) -> str:
        ignore_typos = self.initial_data.get('ignore_typos', False)
        if not ignore_typos:
            misspelled_words = self.check_spelling(text)
            if misspelled_words:
                misspeled_words_string = ", ".join(misspelled_words)
                raise ValidationError('There are misspelled words: {}'.\
                                        format(misspeled_words_string))
        return text
