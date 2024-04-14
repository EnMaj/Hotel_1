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
            return float(types[sort] * ratios[comfort])

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

    def booking(self, busy_date: str, days):
        date = int(busy_date[:2])
        self.busy.append([date, date + days - 1])


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
        date_now = 1
        busy_room_number = 0
        categories_busy = {
            ru_local.ONE_PERSON: 0,
            ru_local.TWO_PERSONS: 0,
            ru_local.JUNIOR_SUITE: 0,
            ru_local.LUXE: 0
        }
        profit = 0
        missed_profit = 0
        for info in book:
            booking_date, s_name, f_name, surname, num_people, busy_date, days, max_money = info.split()
            num_people = float(num_people)
            days = float(days)
            max_money = float(max_money)

            if int(booking_date[:2]) != date_now:
                for room in hotel:
                    # print(room.busy)
                    for date in room.busy:
                        if date[0] <= date_now <= date[1]:
                            busy_room_number += 1
                            categories_busy[room.tp] += 1
                date_now = int(booking_date[:2])
                print(f'{ru_local.NUMBER_BUSY_ROOM} {busy_room_number}\n'
                      f'{ru_local.NUMBER_FREE_ROOM} {len(hotel) - busy_room_number}\n'
                      f'{ru_local.NUMBER_ONE_PERSON} {round(categories_busy[ru_local.ONE_PERSON] * 100 / 9, 2)}\n'
                      f'{ru_local.NUMBER_TWO_PERSONS} {round(categories_busy[ru_local.TWO_PERSONS] * 100 / 6, 2)}\n'
                      f'{ru_local.NUMBER_JUNIOR_SUITE} {round(categories_busy[ru_local.JUNIOR_SUITE] * 100 / 5, 2)}\n'
                      f'{ru_local.NUMBER_LUXE} {round(categories_busy[ru_local.LUXE] * 100 / 4, 2)}\n'
                      f'{ru_local.HOTEL_BUSY} {round(busy_room_number * 100 / len(hotel), 2)}\n'
                      f'{ru_local.PROFIT} {profit}\n'
                      f'{ru_local.MISSED_PROFIT} {missed_profit}\n')
                busy_room_number = 0
                categories_busy = {
                    ru_local.ONE_PERSON: 0,
                    ru_local.TWO_PERSONS: 0,
                    ru_local.JUNIOR_SUITE: 0,
                    ru_local.LUXE: 0
                }
                profit = 0
                missed_profit = 0

            if int(num_people) > 6:
                continue
            force_major = random.randint(0, 3)
            booking_flag = False
            for apartment in hotel:
                busy_flag = False
                food_cost = 0
                if int(apartment.capacity) == int(num_people) \
                        and max_money >= apartment.cost(apartment.tp, apartment.comfort):
                    for element in apartment.busy:
                        if element[0] <= float(busy_date[:2]) <= element[1]:
                            busy_flag = True
                    if not busy_flag:
                        food_cost = max_money - apartment.cost(apartment.tp, apartment.comfort)
                        food_price = apartment.dietary(food_cost)
                        final_price = (apartment.cost(apartment.tp, apartment.comfort)
                                       + food_price) * num_people
                        if force_major == 0:
                            missed_profit += final_price
                            break
                        apartment.booking(busy_date, days)
                        profit += final_price
                        booking_flag = True
                        break
            if not booking_flag:
                for apartment in hotel:
                    busy_flag = False
                    food_cost = 0
                    if apartment.capacity == num_people + 1 \
                            and max_money >= 0.7 * apartment.cost(apartment.tp, apartment.comfort):
                        for element in apartment.busy:
                            if element[0] <= float(busy_date[:2]) <= element[1]:
                                busy_flag = True
                        if not busy_flag:
                            food_cost = max_money - 0.7 * apartment.cost(apartment.tp, apartment.comfort)
                            food_price = apartment.dietary(food_cost)
                            final_price = (0.7 * apartment.cost(apartment.tp, apartment.comfort)
                                           + food_price) * num_people
                            if force_major == 0:
                                missed_profit += final_price
                                break
                            apartment.booking(busy_date, days)
                            profit += final_price
                            break
