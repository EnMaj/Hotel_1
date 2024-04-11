import ru_local
import random


class HotelRoom:

    def __init__(self, number, tp, capacity, comfort, food=0, busy=''):
        self.number = number
        self.tp = tp
        self.capacity = capacity
        self.comfort = comfort
        self.price = HotelRoom.cost(tp, comfort)
        self.food = food
        self.busy = busy

    @staticmethod
    def cost(sort, comfort):
        types = {
            ru_local.ONE_PERSON: 2900,
            ru_local.TWO_PERSONS: 2300,
            ru_local.JUNIOR_SUITE: 3200,
            ru_local.LUXE: 4100
        }

        ratios = {
            ru_local.STANDARD: 1,
            ru_local.STANDARD_PLUS: 1.2,
            ru_local.APARTMENT: 1.5
        }

        if sort in types and comfort in ratios:
            return types[sort] * ratios[comfort]

        return 'ERROR'


if __name__ == '__main__':
    hotel = []

    with open('fund.txt', 'r', encoding='utf8') as num_info:
        for ptr in num_info:
            hotel.append(HotelRoom(*ptr.split()))
    print(hotel[3].tp)
    print(hotel[2].price)

    with open('booking.txt', 'r', encoding='utf8') as book:
        for info in book:
            date, s_name, f_name, surname, num_people, go_in, days, max_money = info.split()

