from abc import ABC, abstractmethod
from enum import Enum


class CurrencyType(Enum):
    FIAT = "fiat"
    VIRTUAL = "virtual"


class Country:
    pass


class USA(Country):
    pass


class Canada(Country):
    pass


class CurrencyFactory(ABC):
    @abstractmethod
    def get_currency(self, country) -> str:
        pass


class VirtualCurrencyFactory(CurrencyFactory):
    def get_currency(self, country) -> str:
        if isinstance(country, USA):
            return "Bitcoin"
        if isinstance(country, Canada):
            return "Etheriem"
        return "Dogecoing"


class FiatCurrencyFactory(CurrencyFactory):
    def get_currency(self, country) -> str:
        if isinstance(country, USA):
            return "USD"
        if isinstance(country, Canada):
            return "CAD"
        return "EURO"


class Currency:
    @staticmethod
    def get_currency_factory(type: str):
        if type == CurrencyType.FIAT:
            return FiatCurrencyFactory()
        else:
            return VirtualCurrencyFactory()


if __name__ == "__main__":
    print(Currency.get_currency_factory(CurrencyType.FIAT).get_currency(USA()))
    print(Currency.get_currency_factory(CurrencyType.FIAT).get_currency(Canada()))
    print(Currency.get_currency_factory(CurrencyType.VIRTUAL).get_currency(USA()))
