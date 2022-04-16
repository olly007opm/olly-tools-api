from fastapi import APIRouter, Response
import requests

router = APIRouter(
    prefix="/convert",
    tags=["convert"],
)


@router.get("/base-n", summary="Convert numbers across bases")
def demo(number: str, origin_base: int, target_base: int, response: Response):
    # Convert number to base 10
    try:
        num = int(number, origin_base)
    except ValueError:
        # Invalid origin base
        response.status_code = 400
        return {"error": "Invalid origin base"}

    # Convert number to target base
    if target_base == 10:
        return {"result": num}
    elif target_base == 2:
        return {"result": bin(num)[2:]}
    elif target_base == 8:
        return {"result": oct(num)[2:]}
    elif target_base == 16:
        return {"result": hex(num)[2:]}
    else:
        response.status_code = 400
        return {"error": "Invalid target base"}


@router.get("/currency", summary="Convert an amount between currencies")
def currency(amount: int, origin: str, target: str, response: Response):
    """
    # Supported currencies
    ```
    - 1INCH   - BRL     - DOGE    - HKD     - KYD     - MYR     - SEK     - USD
    - ADA     - BSD     - DOP     - HNL     - KZT     - MZN     - SGD     - USDC
    - AED     - BTC     - DOT     - HRK     - LAK     - NAD     - SHIB    - USDT
    - AFN     - BTN     - DZD     - HTG     - LBP     - NGN     - SHP     - UYU
    - ALGO    - BUSD    - EGLD    - HUF     - LINK    - NIO     - SLL     - UZS
    - ALL     - BWP     - EGP     - ICP     - LKR     - NOK     - SOL     - VEF
    - AMD     - BYN     - ENJ     - IDR     - LRD     - NPR     - SOS     - VET
    - ANG     - BYR     - ERN     - ILS     - LSL     - NZD     - SRD     - VND
    - AOA     - BZD     - ETB     - IMP     - LTC     - OMR     - STD     - VUV
    - ARS     - CAD     - ETC     - INJ     - LTL     - ONE     - SVC     - WBTC
    - ATOM    - CDF     - ETH     - INR     - LUNA    - PAB     - SYP     - WST
    - AUD     - CHF     - EUR     - IQD     - LVL     - PEN     - SZL     - XAF
    - AVAX    - CHZ     - FIL     - IRR     - LYD     - PGK     - THB     - XAG
    - AWG     - CLF     - FJD     - ISK     - MAD     - PHP     - THETA   - XAU
    - AZN     - CLP     - FKP     - JEP     - MATIC   - PKR     - TJS     - XCD
    - BAM     - CNY     - FTT     - JMD     - MDL     - PLN     - TMT     - XDR
    - BBD     - COP     - GBP     - JOD     - MGA     - PYG     - TND     - XLM
    - BCH     - CRC     - GEL     - JPY     - MKD     - QAR     - TOP     - XMR
    - BDT     - CRO     - GGP     - KES     - MMK     - RON     - TRX     - XOF
    - BGN     - CUC     - GHS     - KGS     - MNT     - RSD     - TRY     - XPF
    - BHD     - CUP     - GIP     - KHR     - MOP     - RUB     - TTD     - XRP
    - BIF     - CVE     - GMD     - KMF     - MRO     - RWF     - TWD     - YER
    - BMD     - CZK     - GNF     - KPW     - MUR     - SAR     - TZS     - ZAR
    - BNB     - DAI     - GRT     - KRW     - MVR     - SBD     - UAH     - ZMK
    - BND     - DJF     - GTQ     - KSM     - MWK     - SCR     - UGX     - ZMW
    - BOB     - DKK     - GYD     - KWD     - MXN     - SDG     - UNI     - ZWL
    ```
    """
    # Get exchange rates
    rate = requests.get(
        f"https://cdn.jsdelivr.net/gh/fawazahmed0/currency-api@1/latest/currencies/{origin}/{target}.json")
    if rate.status_code != 200:
        # Invalid currency
        response.status_code = 400
        return {"error": "Invalid currency"}
    else:
        # Convert currency
        rate = rate.json()[target]
        return {"result": round(amount * rate, 2)}


@router.get("/to-roman", summary="Convert to roman numerals")
def to_roman(number: int, response: Response):
    if number < 1 or number > 3999:
        # Invalid number
        response.status_code = 400
        return {"error": "Invalid number"}
    else:
        # Convert number to roman numerals
        thousands = number // 1000
        hundreds = (number % 1000) // 100
        tens = (number % 100) // 10
        ones = number % 10

        roman = ""
        # Calculate thousands
        if thousands > 0:
            roman += "M" * thousands

        # Calculate hundreds
        if hundreds == 9:
            roman += "CM"
            hundreds = 0
        if hundreds >= 5:
            roman += "D"
            hundreds -= 5
        if hundreds == 4:
            roman += "CD"
            hundreds = 0
        if hundreds > 0:
            roman += "C" * hundreds

        # Calculate tens
        if tens == 9:
            roman += "XC"
            tens = 0
        if tens >= 5:
            roman += "L"
            tens -= 5
        if tens == 4:
            roman += "XL"
            tens = 0
        if tens > 0:
            roman += "X" * tens

        # Calculate ones
        if ones == 9:
            roman += "IX"
            ones = 0
        if ones >= 5:
            roman += "V"
            ones -= 5
        if ones == 4:
            roman += "IV"
            ones = 0
        if ones > 0:
            roman += "I" * ones

        return {"result": roman}


@router.get("/from-roman", summary="Convert from roman numerals")
def from_roman(number: str, response: Response):
    value = 0
    # Convert number to roman numerals
    for i in range(len(number)):
        current = number[i]
        next = number[i + 1] if i < len(number) - 1 else None

        def get_val(char):
            romanvalues = {"I": 1, "V": 5, "X": 10, "L": 50, "C": 100, "D": 500, "M": 1000}
            if char in romanvalues:
                return romanvalues[char]
            else:
                return 0

        if get_val(current) < get_val(next):
            value -= get_val(current)
        else:
            value += get_val(current)

    return {"result": value}
