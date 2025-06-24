from fntypes.library.variative import Variative

u = Variative[int, str, float](1)

# Secluding Variative to the heading type in generic
print(u.only().unwrap())  # 1 (Variative contains int, we only it to int)

# Secluding Variative to the specified type
print(u.only(str).unwrap_or(None))  # None (Variative contains int, we tried secluding it to other type)

# Excluding the head type from Variative
print(u.detach().unwrap_or(None))  # None (Variative contains int and its head type is int so we can't detach it)

del u  # 💅


class Animal:
    def __repr__(self) -> str:
        return "instance of " + self.__class__.__name__


class Cat(Animal):
    pass


class Dog(Animal):
    pass


u = Variative[Cat, Dog, Animal](Cat())

print(u.only().unwrap())  # instance of Cat (Variative is of instance of Cat, it can be perfectly onlyd to the head type Cat)

print(u.only(Dog).unwrap_or(None))  # None (Variative contains Cat, it cannot be onlyd to Dog)

print(u.only(Animal).unwrap())  # instance of Cat (Cat is derived from Animal, so Animal can be perfectly used to only Cat into it)

print(
    u.detach().unwrap()
)  # Variative[Dog, Animal](instance of Cat) (Variative contains Cat, if we detach Cat from it its ok! because Cat is still an Animal which is not detachd)

print(u[Cat])  # Result[Cat, str]
print(u[Cat].unwrap_or_none())  # Cat()
print(u[Dog].unwrap_or_none()) # None
