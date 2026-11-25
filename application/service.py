from domain.models import Animal, Dog, Cat, Parrot, Owner, Species, Vaccination, Visit
from domain.repository import PetRepository
from domain.exceptions import PetValidationError


class PetService:

    def __init__(self, repository: PetRepository):
        self._repo = repository

    def add_animal(
            self, animal_type: str, name: str, age: int, owner_name: str
    ) -> Animal:
        if not name.strip():
            raise PetValidationError("Имя питомца не может быть пустым", "name")
        if age < 0:
            raise PetValidationError("Возраст не может быть отрицательным", "age")

        animals = self._repo.get_animals()
        new_id = max((a.id for a in animals), default=0) + 1

        owner = Owner(id=new_id, full_name=owner_name, phone="Не указан")
        species = Species(id=1, name="Неизвестно", breed="Неизвестно")

        if animal_type.lower() == "dog":
            animal = Dog(new_id, name, age, owner, species)
        elif animal_type.lower() == "cat":
            animal = Cat(new_id, name, age, owner, species)
        elif animal_type.lower() == "parrot":
            animal = Parrot(new_id, name, age, owner, species)
        else:
            raise PetValidationError("Неизвестный тип животного", "animal_type")

        animals.append(animal)
        self._repo.save_animals(animals)
        return animal

    def list_animals(self) -> list[Animal]:
        return self._repo.get_animals()

    def update_animal(self, animal_id: int, new_name: str, new_age: int) -> None:
        if not new_name.strip():
            raise PetValidationError("Имя не может быть пустым", "name")
        if new_age < 0:
            raise PetValidationError("Возраст не может быть отрицательным", "age")

        animals = self._repo.get_animals()
        for animal in animals:
            if animal.id == animal_id:
                animal._name = new_name
                animal._age = new_age

                self._repo.save_animals(animals)
                return

        raise PetValidationError(f"Питомец с ID {animal_id} не найден", "id")

    def delete_animal(self, animal_id: int) -> None:
        animals = self._repo.get_animals()
        remaining = [a for a in animals if a.id != animal_id]

        if len(remaining) == len(animals):
            raise PetValidationError(f"Питомец с ID {animal_id} не найден", "id")

        self._repo.save_animals(remaining)

        all_vaccinations = self._repo.get_vaccinations()
        remaining_vaccinations = [v for v in all_vaccinations if v.animal_id != animal_id]
        self._repo.save_vaccinations(remaining_vaccinations)

        all_visits = self._repo.get_visits()
        remaining_visits = [v for v in all_visits if v.animal_id != animal_id]
        self._repo.save_visits(remaining_visits)

    def add_vaccination(self, animal_id: int, vaccine: str, date: str) -> Vaccination:
        animals = self._repo.get_animals()
        if all(a.id != animal_id for a in animals):
            raise PetValidationError(f"Питомец с ID {animal_id} не найден", "animal_id")

        items = self._repo.get_vaccinations()
        new_id = max((v.id for v in items), default=0) + 1
        record = Vaccination(new_id, animal_id, vaccine, date)
        items.append(record)
        self._repo.save_vaccinations(items)
        return record

    def list_vaccinations(self, animal_id: int) -> list[Vaccination]:
        if all(a.id != animal_id for a in self._repo.get_animals()):
            raise PetValidationError(f"Питомец с ID {animal_id} не найден", "animal_id")

        all_vaccinations = self._repo.get_vaccinations()
        return [v for v in all_vaccinations if v.animal_id == animal_id]

    def add_visit(self, animal_id: int, date: str, reason: str) -> Visit:
        if all(a.id != animal_id for a in self._repo.get_animals()):
            raise PetValidationError(f"Питомец с ID {animal_id} не найден", "animal_id")

        items = self._repo.get_visits()
        new_id = max((v.id for v in items), default=0) + 1
        record = Visit(new_id, animal_id, date, reason)
        items.append(record)
        self._repo.save_visits(items)
        return record

    def list_visits(self, animal_id: int) -> list[Visit]:
        if all(a.id != animal_id for a in self._repo.get_animals()):
            raise PetValidationError(f"Питомец с ID {animal_id} не найден", "animal_id")

        all_visits = self._repo.get_visits()
        return [v for v in all_visits if v.animal_id == animal_id]