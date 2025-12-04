# Convert a number to its word representation
units = ["", "one", "two", "three", "four",
         "five", "six", "seven", "eight", "nine"]
teens = ["ten", "eleven", "twelve", "thirteen", "fourteen",
         "fifteen", "sixteen", "seventeen", "eighteen", "nineteen"]
tens = ["", "", "twenty", "thirty", "forty",
        "fifty", "sixty", "seventy", "eighty", "ninety"]
multiples = ["", "thousand", "million", "billion", "trillion", "quadrillion", "quintillion", "sextillion", "septillion", "octillion", "nonillion", "decillion",
             "undecillion", "duodecillion", "tredecillion", "quattuordecillion", "quindecillion", "sexdecillion", "septendecillion", "octodecillion", "novemdecillion", "vigintillion"]


def number_to_word(n: int) -> str:
    res = ""
    group = 0
    
    # Process number in groups of 1000s
    while n > 0:
        if n % 1000 != 0:
            value = n % 1000
            temp = ""
            # Handle hundreds place
            if value >= 100:
                temp += units[value//100] + " hundred "
                value %= 100
            # Handle tens place (20+)
            if value >= 20:
                temp += tens[value//10] + " "
                value %= 10
            # Handle units place
            if value > 0:
                temp += units[value] + " "
            # Add group suffix (thousand, million, etc.)
            if group > 0:
                temp += multiples[group] + " "

            res = temp + res

        n = n // 1000
        group += 1

    return res.strip()


print(number_to_word(4123))
