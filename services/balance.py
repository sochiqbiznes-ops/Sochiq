def calc_paid_units(paid_money: int, price: int) -> int:
    return paid_money // price


def calc_balance(received: int, paid_money: int, price: int) -> dict:
    paid_units = calc_paid_units(paid_money, price)
    balance_units = paid_units - received
    balance_money = balance_units * price

    return {
        "paid_units": paid_units,
        "balance_units": balance_units,
        "balance_money": balance_money
    }