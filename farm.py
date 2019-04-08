import time
from collections import defaultdict


class Vegetable:
    growtime = None

    def __init__(self):
        self.creation_time = time.time()
        self._adult = False

    def is_adult(self):
        if self._adult:
            return True
        elif time.time() - self.creation_time > self.growtime:
            self._adult = True
            return True
        else:
            return False


class Tomato(Vegetable):
    growtime = 10
    price = 2


class Cucumber(Vegetable):
    growtime = 15
    price = 5


class Farm:
    veggie_by_name = {
        "tomato": Tomato,
        "cucumber": Cucumber
    }

    def __init__(self):
        self._veggies = []
        self.money = 0

    def grow(self, type):
        veg_cls = self.veggie_by_name.get(type)

        if veg_cls is None:
            raise ValueError('Bad vegetable type')

        self._veggies.append(veg_cls())

    def watch(self):
        stat = {veg_key: dict(adults=0, kids=0) for veg_key in self.veggie_by_name}

        for veg in self._veggies:
            veg_key = next(key for key, veg_cls in self.veggie_by_name.items() if isinstance(veg, veg_cls))
            stat[veg_key]["adults" if veg.is_adult() else "kids"] += 1

        return dict(stat, money=self.money)

    def sell(self, type, number):
        veg_cls = self.veggie_by_name.get(type)

        if veg_cls is None:
            raise ValueError('Bad vegetable type')

        if type in self.veggie_by_name:
            total = len([
                veg for veg in self._veggies
                if isinstance(veg, veg_cls) and veg.is_adult()
            ])
            if total < number:
                raise ValueError('You have not enough {}s!!'.format(type))
            else:
                new_veggies = []
                dropped = 0
                for veg in self._veggies:
                    if isinstance(veg, veg_cls) and dropped < number:
                        self.money += veg.price
                        dropped += 1
                    else:
                        new_veggies.append(veg)

                self._veggies = new_veggies
