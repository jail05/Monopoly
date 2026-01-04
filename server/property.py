class Property:
    ID=0
    def __init__(self, name, color):
        Property.ID +=1
        self.ID = Property.ID
        self.name = name
        self.color_group = color
        self.purchase_price = 20
        self.base_rent = 25
        self.house_count =0
        self.has_hotel = False
        self.mortgaged = False
        self.owner_id = None



    def has_owner(self):
        if self.owner_id==None:
            return False
        else:
            return True

    def is_mortgaged(self):
        return self.is_mortgaged

    def current_rent(self):
        if self.is_mortgaged():
            return 0
        elif self.has_hotel:
            return 5*self.base_rent
        else:
            return (self.house_count+1)*self.base_rent

    def can_build_house(self):
        return (not(self.has_hotel) and
                not(self.is_mortgaged) and
                self.house_count < 4)

    def can_build_hotel(self):
        return not(self.has_hotel) and not(self.mortgaged) and self.house_count == 3

    def mortgage(self):
        self.mortgaged = True

    def unmortgage(self):
        self.mortgaged = False

    def house_counter(self):
        self.house_count += 1

    def has_hotel(self):
        return self.has_hotel







