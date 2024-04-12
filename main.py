import ru_local
import random


class HotelRoom:

    def __init__(self, number, tp, capacity, comfort, food=0):
        self.number = number
        self.tp = tp
        self.capacity = capacity
        self.comfort = comfort
        self.price = HotelRoom.cost(tp, comfort)
        self.food = food
        self.busy = []

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

    @staticmethod
    def dietary(food_cost):
        diets = {
            "half_board": 1000,
            "breakfast": 280,
            "no_diet": 0
        }
        for tp, price in diets.items():
            if price <= food_cost:
                return price

    def booking(self, busy_date:str, days):
        date = int(busy_date[:2])
        self.busy.append([date, date + days])


if __name__ == '__main__':
    hotel = []

    with open('fund.txt', 'r', encoding='utf8') as num_info:
        for ptr in num_info:
            hotel.append(HotelRoom(*ptr.split()))
    for i in range(len(hotel) - 1):
        for j in range(len(hotel) - 1 - i):
            if hotel[j].cost(hotel[j].tp, hotel[j].comfort) > hotel[j + 1].cost(hotel[j].tp, hotel[j].comfort):
                hotel[j], hotel[j + 1] = hotel[j + 1], hotel[j]

    with open('booking.txt', 'r', encoding='utf8') as book:
        for info in book:
            booking_date, s_name, f_name, surname, num_people, busy_date, days, max_money = info.split()
            print(info)
            if int(num_people) > 6:
                continue
            force_major = random.randint(0, 3)
            if force_major == 0:
                continue

            for apartment in hotel:
                busy_flag = False
                food_cost = 0
                if apartment.number == int(num_people):
                    for element in apartment.busy:
                        if element[0] < busy_date < element[1]:
                            busy_flag = True
                    if not busy_flag:
                        apartment.booking(busy_date, days)
                        food_cost = max_money - apartment.cost(apartment.tp, apartment.comfort)
                        food_price = apartment.dietary(food_cost)
                if not busy_flag:
                    if apartment.number == int(num_people) + 1:
                        for element in apartment.busy:
                            if element[0] < busy_date < element[1]:
                                busy_flag = True
                        if not busy_flag:
                            apartment.booking(busy_date, days)
                            food_cost = max_money - apartment.cost(apartment.tp, apartment.comfort)
                            food_price = apartment.dietary(food_cost)
