import secrets
from typing import List
from django.conf import settings
from django.core.cache import cache
from texts.models import TextBlock


HASH_ALPHABET: str = settings.HASH_ALPHABET
DEFAULT_HASH_LENGTH: int = settings.DEFAULT_HASH_LENGTH
MAX_ATTEMPTS = 1000
CACHE_KEY = 'hash_generator_cache_key'


class MaxAttemptsError(Exception):
    pass


class HashGenerator:
    def _create_hash(self) -> str:
        random_hash: str = ''.join(secrets.choice(HASH_ALPHABET)
                              for _ in range(DEFAULT_HASH_LENGTH))
        return random_hash

    def generate_hashes(self, num_hashes: int = 20) -> None:
        hashes: List[str] = []
        for _ in range(num_hashes):
            hash_value = self.create_unique_hash()
            hashes.append(hash_value)
        cache.set(CACHE_KEY, hashes)
            
    def create_unique_hash(self, attempt_number: int = 0) -> str:
        if attempt_number >= MAX_ATTEMPTS:
            raise MaxAttemptsError(
                'Too many attempts to create a unique'
                'hash. You may have run out of free hashes')
        random_hash: str = self._create_hash()

        if TextBlock.objects.filter(hash=random_hash).exists():
            return self.create_unique_hash()
        return random_hash
