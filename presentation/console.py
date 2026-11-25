from application.service import PetService
from domain.exceptions import PetValidationError


class ConsoleApp:
    def __init__(self, service: PetService):
        self.service = service

    def run(self) -> None:
        while True:
            print("\n=== МЕНЕДЖЕР ДОМАШНИХ ЖИВОТНЫХ ===")
            print("1. Показать всех питомцев")
            print("2. Добавить питомца")
            print("3. Удалить питомца")
            print("4. Изменить данные питомца")
            print("5. Добавить вакцинацию")
            print("6. Показать вакцинации питомца")
            print("7. Добавить визит к ветеринару")
            print("8. Показать визиты питомца")
            print("0. Выход")
            choice = input("Выберите действие: ").strip()

            try:
                if choice == "1":
                    self._show_animals()
                elif choice == "2":
                    self._add_animal()
                elif choice == "3":
                    self._delete_animal()
                elif choice == "4":
                    self._update_animal()
                elif choice == "5":
                    self._add_vaccination()
                elif choice == "6":
                    self._show_vaccinations()
                elif choice == "7":
                    self._add_visit()
                elif choice == "8":
                    self._show_visits()
                elif choice == "0":
                    print("До свидания!")
                    return
                else:
                    print("Неизвестная команда")

            except PetValidationError as error:
                print(f"Ошибка валидации: {error}")
            except ValueError as error:
                print(f"Ошибка ввода: {error}")
            except (EOFError, KeyboardInterrupt):
                print("\nВыход")
                return

    def _show_animals(self) -> None:
        animals = self.service.list_animals()
        if not animals:
            print("Питомцев пока нет.")
            return
        for animal in animals:
            print(f"[{animal.id}] {animal.name} ({type(animal).__name__}), "
                  f"возраст: {animal.age}, говорит: {animal.speak()}, "
                  f"владелец: {animal.owner.full_name}")

    def _add_animal(self) -> None:
        animal_type = input("Тип (dog/cat/parrot): ").strip()
        name = input("Кличка: ").strip()
        age = int(input("Возраст: "))
        owner_name = input("ФИО владельца: ").strip()

        animal = self.service.add_animal(animal_type, name, age, owner_name)
        print(f"Добавлен питомец #{animal.id}")

    def _delete_animal(self) -> None:
        animal_id = int(input("ID питомца для удаления: "))
        self.service.delete_animal(animal_id)
        print("Питомец удален.")

    def _update_animal(self) -> None:
        animal_id = int(input("ID питомца: "))
        new_name = input("Новая кличка: ").strip()
        new_age = int(input("Новый возраст: "))
        self.service.update_animal(animal_id, new_name, new_age)
        print("Данные обновлены.")

    def _add_vaccination(self) -> None:
        animal_id = int(input("ID питомца: "))
        vaccine = input("Название вакцины: ").strip()
        date = input("Дата (ГГГГ-ММ-ДД): ").strip()
        self.service.add_vaccination(animal_id, vaccine, date)
        print("Вакцинация добавлена.")

    def _show_vaccinations(self) -> None:
        animal_id = int(input("ID питомца: "))
        vaccinations = self.service.list_vaccinations(animal_id)

        if not vaccinations:
            print("У этого питомца нет вакцинаций.")
            return

        print(f"\nВакцинации питомца #{animal_id}:")
        for v in vaccinations:
            print(f"  - {v.date}: {v.vaccine}")

    def _add_visit(self) -> None:
        # Вот здесь теперь только одно объявление функции!
        try:
            animal_id = int(input("ID питомца: "))
            date = input("Дата визита (ДД.ММ.ГГГГ): ").strip()

            if not date.replace(".", "").isdigit():
                raise ValueError("Дата должна состоять только из цифр и точек (например, 12.05.2024)")

            reason = input("Причина визита: ").strip()
            if not reason:
                raise ValueError("Причина визита не может быть пустой")

            self.service.add_visit(animal_id, date, reason)
            print("Визит успешно добавлен.")

        except ValueError as error:
            print(f"Ошибка ввода: {error}")

    def _show_visits(self) -> None:
        animal_id = int(input("ID питомца: "))
        visits = self.service.list_visits(animal_id)

        if not visits:
            print("У этого питомца нет визитов.")
            return

        print(f"\nВизиты питомца #{animal_id}:")
        for v in visits:
            print(f"  - {v.date}: {v.reason}")