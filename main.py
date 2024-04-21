import ru_local
import random


class HotelRoom:

    def __init__(self, number, tp, capacity, comfort, food=0):
        self.number = number
        self.tp = tp
        self.capacity = int(capacity)
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
            "half_board": 1000.0,
            "breakfast": 280.0,
            "no_diet": 0
        }
        for tp, price in diets.items():
            if price <= food_cost:
                return price

    def booking(self, busy_date: str, days):
        date = int(busy_date[:2])
        self.busy.append([date, date + days - 1])


def calculate_profits(is_sell, missed_profit, profit, num_people, max_money, hotel, booking_flag):
    for apartment in hotel:
        busy_flag = False
        coefficient = 0.7 if is_sell == True else 1
        food_cost = 0
        final_price = 0.0

        if (apartment.capacity == num_people + 1 if is_sell == True else 0) \
                and max_money >= coefficient * apartment.cost(apartment.tp, apartment.comfort):

            for element in apartment.busy:
                if element[0] <= float(busy_date[:2]) <= element[1]:
                    busy_flag = True
                    break

            if not busy_flag:
                food_cost = max_money - coefficient * apartment.cost(apartment.tp, apartment.comfort)
                food_price = float(apartment.dietary(food_cost))
                final_price = num_people * coefficient * (apartment.cost(apartment.tp, apartment.comfort) + food_price)

                if force_major == 0:
                    missed_profit += final_price
                    break

                apartment.booking(busy_date, days)
                profit += final_price
                booking_flag = True
                break

    return missed_profit, profit, booking_flag, hotel


if __name__ == '__main__':
    hotel = []

    with open('fund.txt', 'r', encoding='utf8') as num_info:
        for ptr in num_info:
            hotel.append(HotelRoom(*ptr.split()))

    hotel = sorted(hotel, key=lambda x: x.cost(x.tp, x.comfort), reverse=True)

    with (open('booking.txt', 'r', encoding='utf8') as book):
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
            booking_date, last_name, first_name, patronymic, num_people, busy_date, days, max_money = info.split()
            num_people = int(num_people)
            days = int(days)
            max_money = float(max_money)

            if int(booking_date[:2]) != date_now:
                for room in hotel:
                    for date in room.busy:
                        if date[0] <= date_now <= date[1]:
                            busy_room_number += 1
                            categories_busy[room.tp] += 1
                            break

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

            missed_profit, profit, booking_flag, hotel = calculate_profits(False, missed_profit, profit, num_people,
                                                                           max_money, hotel, booking_flag)

            if not booking_flag:
                missed_profit, profit, booking_flag, hotel = calculate_profits(True, missed_profit, profit, num_people,
                                                                               max_money,
                                                                               hotel, booking_flag)
