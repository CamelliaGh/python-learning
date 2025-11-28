'''
Planning:
Parent class PasswordGenerator with three children: RandomPasswordGenerator,
MemorablePasswordGenerator, PinCodeGenerator
methods: init + generate
'''
import random
import string
import nltk
from abc import ABC, abstractmethod


nltk.download('words')

class PasswordGenerator(ABC):
    """Abstract base class for password generators."""

    @abstractmethod
    def generate(self):
        """Generate and return a password string."""
        pass  # Implemented by subclasses


class RandomPasswordGenerator(PasswordGenerator):
    """Generates a random password from letters, and optionally digits and symbols."""

    def __init__(self, length: int, include_numbers: bool = True, include_symbols: bool = True):
        """Initialize the generator configuration.

        Args:
            length: Desired length of the generated password.
            include_numbers: If True, include digits 0-9.
            include_symbols: If True, include punctuation symbols.
        """
        self._length = length
        self.valid_characters = string.ascii_letters
        if include_numbers:
            self.valid_characters += string.digits
        if include_symbols:
            self.valid_characters += string.punctuation

    def generate(self):
        """Return a randomly generated password of configured length."""
        password_list = random.choices(self.valid_characters, k=self._length)
        return "".join(password_list)


class PinGenerator(PasswordGenerator):
    """Generates a numeric PIN with the specified length."""

    def __init__(self, length: int):
        """Initialize the PIN length.

        Args:
            length: Number of digits in the PIN.
        """
        self._lenght = length

    def generate(self):
        """Return a numeric PIN string of the configured length."""
        password_list = random.choices(string.digits, k=self._lenght)
        return "".join(password_list)


class MemorablePassword(PasswordGenerator):
    """Generates a 'memorable' password by combining random words."""

    def __init__(self, num_of_words: int = 4, separator: str = '-', capitalization: bool = False, vocabularies: list = None):
        """Initialize the memorable password configuration.

        Args:
            num_of_words: Number of words to combine.
            separator: Separator to use between words (not all strategies may use it).
            capitalization: If True, prefer uppercase words; otherwise lowercase. Strategy may vary.
            vocabularies: Optional custom list of words to sample from.
        """
        self._num_of_words = num_of_words
        self._separator = separator
        self._capitalization = capitalization
        self._vocabularies = vocabularies

        if vocabularies is None:
            self._vocabularies = nltk.corpus.words.words()#['Bobo', "Jack", "Kone", "Lala", "1986"]

    def generate(self):
        """Return a memorable password constructed from randomly chosen words."""
        password_words = random.choices(
            self._vocabularies, k=self._num_of_words)
        vocab_to_user = [word.upper() if random.choice(
            [True, False]) else word.lower() for word in password_words]
        return "".join(vocab_to_user)


if __name__ == '__main__':

    pin_generator = PinGenerator(8)
    print(f"This is a random pin: {pin_generator.generate()}")

    random_password_generator = RandomPasswordGenerator(8)
    print(f"This is a random password: {random_password_generator.generate()}")

    memoryable_password = MemorablePassword()
    print(f"This is a Memorable password: {memoryable_password.generate()}")
