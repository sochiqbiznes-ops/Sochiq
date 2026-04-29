def calc(client):
    total = client[2] * client[3]
    debt = total - client[4]
    return total, debt