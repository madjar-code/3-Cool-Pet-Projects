from django.db import models
from common.mixins.models import BaseModel
from users.models import User


class TextBlock(BaseModel):
    text = models.TextField(max_length=1048)
    author = models.ForeignKey(
        to=User, on_delete=models.SET_NULL, blank=True, null=True)

    class Meta:
        verbose_name = 'Text block'
        verbose_name = 'Text blocls'

    def __str__(self) -> str:
        if self.author:
            return f'Text of {self.author}'
        return f'Text of unknown user'
