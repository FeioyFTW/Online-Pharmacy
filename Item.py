class Item:
    id = 0

    def __init__(self, name, price, have, bio, picture):
        Item.id += 1
        self.__item_id = Item.id
        self.__item_name = name
        self.__item_price = price
        self.__item_have = have
        self.__item_want = 0
        self.__item_bio = bio
        self.__item_picture = picture

    def get_item_id(self):
        return self.__item_id

    def set_item_id(self, id):
        self.__item_id = id

    def get_item_name(self):
        return self.__item_name

    def set_item_name(self, name):
        self.__item_name = name

    def get_item_price(self):
        return self.__item_price

    def set_item_price(self, price):
        self.__item_price = price

    def get_item_have(self):
        return self.__item_have

    def set_item_have(self, have):
        self.__item_have = have

    def get_item_want(self):
        return self.__item_want

    def set_item_want(self, want):
        if want <= self.get_item_have():
            self.__item_want = want
        else:
            print("We do not have enough stock at the moment! ")

    def get_item_bio(self):
        return self.__item_bio

    def set_item_bio(self, bio):
        self.__item_bio = bio

    def get_item_picture(self):
        return self.__item_picture

    def set_item_picture(self, picture):
        self.__item_picture = picture

    def get_total_price(self):
        return self.get_item_price() * self.get_item_want()

    def buy_item(self):
        s = self.get_item_have() - self.get_item_want()
        self.set_item_have(s)
        self.set_item_want(0)

    def __str__(self):
        s = "{} costs ${} with a bio {} and picture {}".format(self.get_item_name(), self.get_item_price(),
                                                               self.get_item_bio(), self.get_item_picture())
        return s


class Prescribed(Item):
    def __init__(self, name, price, bio, picture):
        super().__init__(name, price, bio, picture)
        self.__item_dosage = ""

    def get_item_dosage(self):
        return self.__item_dosage

    def set_item_dosage(self, dosage):
        self.__item_dosage = dosage
