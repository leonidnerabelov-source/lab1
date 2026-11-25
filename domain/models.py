from dataclasses import dataclass
from abc import ABC, abstractmethod

@dataclass
class Owner:
    id: int
    full_name: str
    phone: str

@dataclass
class Species:
    id: int
    name: str
    breed: str

@dataclass
class Vaccination:
    id: int
    animal_id: int
    vaccine: str
    date: str

@dataclass
class Visit:
    id: int
    animal_id: int
    date: str
    reason: str

class Animal(ABC):

    def __init__(self, animal_id: int, name: str, age: int, owner: Owner, species: Species):
        self._id = animal_id
        self._name = name
        self._age = age
        self._owner = owner
        self._species = species

    @property
    def id(self) -> int:
        return self._id

    @property
    def name(self) -> str:
        return self._name

    @property
    def age(self) -> int:
        return self._age

    @property
    def owner(self) -> Owner:
        return self._owner

    @property
    def species(self) -> Species:
        return self._species

    @abstractmethod
    def speak(self) -> str:
        pass

class Dog(Animal):
    def speak(self) -> str:
        return "Гав!"

class Cat(Animal):
    def speak(self) -> str:
        return "Мяу!"

class Parrot(Animal):
    def speak(self) -> str:
        return "Кар-р!"