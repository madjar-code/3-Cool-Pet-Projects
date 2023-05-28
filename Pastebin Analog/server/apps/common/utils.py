import random
from django.conf import settings
from django.db.models import Model


def _generate_code(letters: str = settings.SLUG_ALPHABET,
                  length: int = settings.DEFAULT_SLUG_LENGTH) -> str:
    random_code: str = ''.join(random.choice(letters)\
                               for _ in range(length))
    return random_code


def generate_unique_slug(prefix: str, model_class: Model) -> str:
    code: str = _generate_code() 

    slug = prefix + '-' + code
    if model_class.objects.filter(slug=slug).exists():
        return generate_unique_slug(prefix, model_class)
    return slug
