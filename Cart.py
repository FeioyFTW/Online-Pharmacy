class Cart:
    def __init__(self, item):
        self.__item = item

    def get_item(self):
        return self.__item

    def set_item(self, item):
        self.__item = item

    def total(self):
        total = 0
        for i in self.__item:
            total += i.get_total_price()

        return total

    def paid(self):
        for i in self.__item:
            i.set_have(i.get_have() - i.get_want())
