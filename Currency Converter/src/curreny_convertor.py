import currency_service 


class CurrencyConvertor:
    """Currency converter that uses exchange rate API."""
    
    def __init__(self):
        pass

    def convert(self, amount: float, from_currency: str, to_currency: str) -> float:
        """Convert amount from one currency to another. Returns -1 on error."""
        try:
            rate = currency_service.get_exchange_rate(
                from_currency, to_currency)
            print(f"Found rate {rate}")
            if rate is not None:
                return rate * amount
            else:
                raise Exception("Currency not found")
        except Exception as e:
            print(f"An error occuring while converting the currency\n: {e}")
            return -1


if __name__ == '__main__':
    # Test conversion
    currency_convertor = CurrencyConvertor()
    print(currency_convertor.convert(1000, "USD", "IRR"))
