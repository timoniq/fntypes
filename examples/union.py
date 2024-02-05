from fntypes import Union

u = Union[int, str, float](1)

# Secluding union to the heading type in generic
print(u.only().unwrap()) # 1 (union contains int, we only it to int)

# Secluding union to the specified type
print(u.only(str).unwrap_or(None)) # None (union contains int, we tried secluding it to other type)

# Excluding the head type from union
print(u.detach().unwrap_or(None)) # None (union contains int and its head type is int so we can't detach it)

del u  # 💅


class Animal:
    def __repr__(self) -> str:
        return "instance of " + self.__class__.__name__

class Cat(Animal):
    pass

class Dog(Animal):
    pass


u = Union[Cat, Dog, Animal](Cat())

print(u.only().unwrap()) # instance of Cat (union is of instance of Cat, it can be perfectly onlyd to the head type Cat)

print(u.only(Dog).unwrap_or(None)) # None (union contains Cat, it cannot be onlyd to Dog)

print(u.only(Animal).unwrap()) # instance of Cat (Cat is derived from Animal, so Animal can be perfectly used to only Cat into it)

print(u.detach().unwrap()) # Union[Dog, Animal](instance of Cat) (union contains Cat, if we detach Cat from it its ok! because Cat is still an Animal which is not detachd)
