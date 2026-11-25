import unittest
import tempfile
from pathlib import Path

from application.service import PetService
from domain.exceptions import PetValidationError
from domain.models import Cat, Dog, Owner, Parrot, Species
from domain.repository import PetRepository
from infrastructure.json_repository import JsonPetRepository


class InMemoryPetRepository(PetRepository):
    def __init__(self):
        self.animals = []
        self.vaccinations = []
        self.visits = []

    def get_animals(self):
        return list(self.animals)

    def save_animals(self, animals):
        self.animals = list(animals)

    def get_vaccinations(self):
        return list(self.vaccinations)

    def save_vaccinations(self, items):
        self.vaccinations = list(items)

    def get_visits(self):
        return list(self.visits)

    def save_visits(self, items):
        self.visits = list(items)


class PetServiceTests(unittest.TestCase):
    def setUp(self):
        self.repo = InMemoryPetRepository()
        self.service = PetService(self.repo)

    def test_add_animal(self):
        dog = self.service.add_animal("dog", "Рекс", 3, "Иван Иванов")
        self.assertEqual(dog.id, 1)
        self.assertIsInstance(dog, Dog)
        self.assertEqual(dog.speak(), "Гав!")

    def test_add_cat_and_parrot(self):
        cat = self.service.add_animal("cat", "Мурка", 2, "Анна")
        parrot = self.service.add_animal("parrot", "Кеша", 1, "Олег")
        self.assertIsInstance(cat, Cat)
        self.assertEqual(cat.speak(), "Мяу!")
        self.assertIsInstance(parrot, Parrot)
        self.assertEqual(parrot.speak(), "Кар-р!")

    def test_empty_name_is_rejected(self):
        with self.assertRaises(PetValidationError):
            self.service.add_animal("dog", "  ", 2, "Иван")

    def test_negative_age_is_rejected(self):
        with self.assertRaises(PetValidationError):
            self.service.add_animal("dog", "Рекс", -1, "Иван")

    def test_unknown_type_is_rejected(self):
        with self.assertRaises(PetValidationError):
            self.service.add_animal("hamster", "Хома", 1, "Иван")

    def test_update_animal(self):
        dog = self.service.add_animal("dog", "Рекс", 3, "Иван")
        self.service.update_animal(dog.id, "Рекс 2", 4)
        updated = self.service.list_animals()[0]
        self.assertEqual(updated.name, "Рекс 2")
        self.assertEqual(updated.age, 4)

    def test_update_missing_animal(self):
        with self.assertRaises(PetValidationError):
            self.service.update_animal(42, "Имя", 1)

    def test_delete_animal(self):
        dog = self.service.add_animal("dog", "Удалить меня", 3, "Иван")
        self.service.add_vaccination(dog.id, "Бешенство", "2026-01-10")
        self.service.add_visit(dog.id, "10.01.2026", "Осмотр")

        self.service.delete_animal(dog.id)
        self.assertEqual(self.service.list_animals(), [])
        self.assertEqual(self.repo.vaccinations, [])
        self.assertEqual(self.repo.visits, [])

    def test_delete_missing_animal(self):
        with self.assertRaises(PetValidationError):
            self.service.delete_animal(42)

    def test_add_and_list_vaccinations(self):
        dog = self.service.add_animal("dog", "Рекс", 3, "Иван")
        rec = self.service.add_vaccination(dog.id, "Вакцина", "2026-05-01")
        self.assertEqual(rec.id, 1)
        self.assertEqual(len(self.service.list_vaccinations(dog.id)), 1)

    def test_vaccination_for_missing_animal(self):
        with self.assertRaises(PetValidationError):
            self.service.add_vaccination(42, "Вакцина", "2026-05-01")

    def test_add_and_list_visits(self):
        dog = self.service.add_animal("dog", "Рекс", 3, "Иван")
        visit = self.service.add_visit(dog.id, "01.05.2026", "Осмотр")
        self.assertEqual(visit.id, 1)
        self.assertEqual(len(self.service.list_visits(dog.id)), 1)

    def test_visit_for_missing_animal(self):
        with self.assertRaises(PetValidationError):
            self.service.add_visit(42, "01.05.2026", "Осмотр")

    def test_save_and_load_animals(self):
        with tempfile.TemporaryDirectory() as tmp_dir:
            repo = JsonPetRepository(Path(tmp_dir) / "pets.json")
            owner = Owner(1, "Иван Иванов", "+79990000000")
            species = Species(1, "Собака", "Корги")
            dog = Dog(1, "Чеддар", 2, owner, species)

            repo.save_animals([dog])
            loaded = repo.get_animals()

            self.assertEqual(len(loaded), 1)
            self.assertIsInstance(loaded[0], Dog)
            self.assertEqual(loaded[0].name, "Чеддар")


if __name__ == "main":
    unittest.main()