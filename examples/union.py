from monading import Union

u = Union[int, str, float](1)

# Secluding union to the heading type in generic
print(u.seclude()) # 1 (union contains int, we seclude it to int)

# Secluding union to the specified type
print(u.seclude(str, raise_error=False)) # None (union contains int, we tried secluding it to other type)

# Excluding the head type from union
print(u.exclude(raise_error=False)) # None (union contains int and its head type is int so we can't exclude it)

del u  # 💅


class Animal:
    def __repr__(self) -> str:
        return "instance of " + self.__class__.__name__

class Cat(Animal):
    pass

class Dog(Animal):
    pass


u = Union[Cat, Dog, Animal](Cat())

print(u.seclude()) # instance of Cat (union is of instance of Cat, it can be perfectly secluded to the head type Cat)

print(u.seclude(Dog, raise_error=False)) # None (union contains Cat, it cannot be secluded to Dog)

print(u.seclude(Animal)) # instance of Cat (Cat is derived from Animal, so Animal can be perfectly used to seclude Cat into it)

print(u.exclude()) # Union[Dog, Animal](instance of Cat) (union contains Cat, if we exclude Cat from it its ok! because Cat is still an Animal which is not excluded)
