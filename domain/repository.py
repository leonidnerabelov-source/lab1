from abc import ABC, abstractmethod
from domain.models import Animal, Vaccination, Visit

class PetRepository(ABC):

    @abstractmethod
    def get_animals(self) -> list[Animal]:
        pass

    @abstractmethod
    def save_animals(self, animals: list[Animal]) -> None:
        pass

    @abstractmethod
    def get_vaccinations(self) -> list[Vaccination]:
        pass

    @abstractmethod
    def save_vaccinations(self, items: list[Vaccination]) -> None:
        pass

    @abstractmethod
    def get_visits(self) -> list[Visit]:
        pass

    @abstractmethod
    def save_visits(self, items: list[Visit]) -> None:
        pass