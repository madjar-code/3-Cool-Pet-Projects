import abc
import hashlib
import secrets
from django.conf import settings
from texts.models import TextBlock


HASH_ALPHABET: str = settings.HASH_ALPHABET
DEFAULT_HASH_LENGTH: int = settings.DEFAULT_HASH_LENGTH
MAX_ATTEMPTS = 1000


class MaxAttemptsError(Exception):
    pass


class BaseHashGenerator(abc.ABC):
    @abc.abstractmethod
    def _create_hash(self) -> str:
        pass

    def create_unique_hash(self, attempt_number: int = 0) -> str:
        if attempt_number >= MAX_ATTEMPTS:
            raise MaxAttemptsError(
                'Too many attempts to create a unique'
                'hash. You may have run out of free hashes')
        random_hash: str = self._create_hash()

        if TextBlock.objects.filter(hash=random_hash).exists():
            return self.create_unique_hash(attempt_number + 1)
        return random_hash


def hash_factory(type: str = 'random') -> BaseHashGenerator:
    if type == 'sha':
        return HashGeneratorSHA()
    else:
        return HashGeneratorRandom()


class HashGeneratorRandom(BaseHashGenerator):
    def _create_hash(self) -> str:
        random_hash: str = ''.join(secrets.choice(HASH_ALPHABET)
                              for _ in range(DEFAULT_HASH_LENGTH))
        return random_hash

    def create_unique_hash(self, attempt_number: int = 0) -> str:
        return super().create_unique_hash(attempt_number)


class HashGeneratorSHA(BaseHashGenerator):
    def _create_hash(self) -> str:
        random_bytes: bytes = secrets.token_bytes()
        hash_value: str = hashlib.sha256(random_bytes).hexdigest()
        return hash_value[:DEFAULT_HASH_LENGTH]

    def create_unique_hash(self, attempt_number: int = 0) -> str:
        return super().create_unique_hash(attempt_number)