from fntypes import Variative, Option, Some
import dataclasses
import typing

@typing.runtime_checkable
class CanSpeak(typing.Protocol):
    def sound(self) -> str:
        ...

@dataclasses.dataclass
class Cat(CanSpeak):
    name: str
    kittens: list["Cat"]

    def sound(self) -> str:
        return "Meow-meow"

@dataclasses.dataclass
class Dog(CanSpeak):
    name: str

    def sound(self) -> str:
        return "Woof-woof"


@dataclasses.dataclass
class Lizard:
    name: str


@dataclasses.dataclass
class PetLover:
    name: str
    age: int
    pet: Option[Variative[Cat, Dog, Lizard]]


pet_lover = PetLover("Nikolay", 20, Some(Variative(Cat("Lusya", []))))

print(f"- Hey, {pet_lover.name}. Are you a pet lover?")

match pet_lover.pet:
    case Some(pet):
        print(f"- Yea! .. {pet.value.name.upper()}!!!! COME HERE")
        print(f"  Hey, {pet.value.name}, say something")
        if isinstance(pet.value, CanSpeak):
            print(f"- {pet.value.sound()}")
        else:
            print("- ...")
            print("- Oh.. I forgot they can't speak")
        
        if cat := pet.only(Cat).unwrap_or(None):
            print("- I love cats!! Does she have kittens?")
            if not cat.kittens:
                print("- Not really")
            else:
                print("- Yeahh..", ",".join([kitten.name for kitten in cat.kittens]))

    case _:
        print("- Nope ......")
