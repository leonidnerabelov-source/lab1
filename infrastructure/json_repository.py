import json
from pathlib import Path

from domain.repository import PetRepository
from domain.models import Animal, Dog, Cat, Parrot, Owner, Species, Vaccination, Visit

class JsonPetRepository(PetRepository):
    def __init__(self, path: Path):
        self.path = path

    def _read_data(self) -> dict:
        if not self.path.exists():
            return {"animals": [], "vaccinations": []}
        try:
            text = self.path.read_text(encoding="utf-8")
            return json.loads(text)
        except json.JSONDecodeError:
            raise RuntimeError("Файл поврежден или содержит неверный JSON")

    def _write_data(self, data: dict) -> None:
        self.path.parent.mkdir(parents=True, exist_ok=True)
        text = json.dumps(data, ensure_ascii=False, indent=4)
        self.path.write_text(text, encoding="utf-8")

    def get_animals(self) -> list[Animal]:
        data = self._read_data()
        animals = []

        for item in data.get("animals", []):
            owner = Owner(**item["owner"])
            species = Species(**item["species"])
            animal_type = item["type"]
            if animal_type == "dog":
                animal = Dog(item["id"], item["name"], item["age"], owner, species)
            elif animal_type == "cat":
                animal = Cat(item["id"], item["name"], item["age"], owner, species)
            elif animal_type == "parrot":
                animal = Parrot(item["id"], item["name"], item["age"], owner, species)
            else:
                continue

            animals.append(animal)

        return animals

    def save_animals(self, animals: list[Animal]) -> None:
        data = self._read_data()
        animals_data = []

        for animal in animals:
            animal_dict = {
                "type": type(animal).__name__.lower(),
                "id": animal.id,
                "name": animal.name,
                "age": animal.age,
                "owner": {
                    "id": animal.owner.id,
                    "full_name": animal.owner.full_name,
                    "phone": animal.owner.phone
                },
                "species": {
                    "id": animal.species.id,
                    "name": animal.species.name,
                    "breed": animal.species.breed
                }
            }
            animals_data.append(animal_dict)

        data["animals"] = animals_data
        self._write_data(data)
    def get_vaccinations(self) -> list[Vaccination]:
        data = self._read_data()
        return [Vaccination(**item) for item in data.get("vaccinations", [])]

    def save_vaccinations(self, items: list[Vaccination]) -> None:
        data = self._read_data()
        data["vaccinations"] = [
            {
                "id": v.id,
                "animal_id": v.animal_id,
                "vaccine": v.vaccine,
                "date": v.date
            } for v in items
        ]
        self._write_data(data)
    def get_visits(self) -> list[Visit]:
        data = self._read_data()
        return [Visit(**item) for item in data.get("visits", [])]

    def save_visits(self, items: list[Visit]) -> None:
        data = self._read_data()
        data["visits"] = [
            {
                "id": v.id,
                "animal_id": v.animal_id,
                "date": v.date,
                "reason": v.reason
            } for v in items
        ]
        self._write_data(data)