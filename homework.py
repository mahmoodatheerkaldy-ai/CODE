#Q1

#--------------------------
#Q2
class vehicle:
    def __init__(self, brand, year):
        self.brand = brand
        self.year = year

    def move(self):
        print(f"the vehicle is moving")

class car(vehicle):
    def __init__(self, brand, year):
        super().__init__(brand, year)
    def move(self):
        print(f"the car is driving on the road")
    
class plan(vehicle):
    def __init__(self, brand, year):
        super().__init__(brand, year)
    def move(self):
        print(f"the plan is fling in the are")

c1 = car("supra", "200")
p1 = plan("f12", "2007")
lst = [c1, p1]
for x in lst:
    x.move()

#------------------
#Q3
class matrix:
    def __init__(self, lst):
        self.n = len(lst)
        self.m = len(lst[0])
        self.lst = lst
    def __mul__(self, other):
        new_lst = [[]]
        def transorm(lst):
            lost = [j for i, j in lst]
            return lost
        self.lst = transorm(self.lst)
        other.lst = transorm(other.lst)

        for i in range(len(self.lst)):
            for j in range(len(self.lst)):
                new_lst.append(self.lst[i][j] * other.lst[i][j])
        return new_lst
    
n = matrix([[1, 2, 3],[4, 5, 6]]) 
m = matrix([[7, 8],[9, 10],[11, 12]])

lst = n * m
print(lst)
