from db.models.order import Order


def filter_washers(washers: list):
    result = list()

    for washer in washers:
        if washer and washer not in result:
            result.append(washer)

    return result


def washers_profit(orders):
    orders_profit_for_washers = 0

    for order in orders:
        order: Order

        washers_rate = sum([washer.stake for washer in order.washers])
        order_profit_for_washers = washers_rate * 0.01 * order.price

        orders_profit_for_washers += order_profit_for_washers

    return orders_profit_for_washers
