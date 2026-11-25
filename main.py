from pathlib import Path
from application.service import PetService
from infrastructure.json_repository import JsonPetRepository
from presentation.console import ConsoleApp


def main() -> None:
    repo_path = Path(__file__).parent / "pets.json"
    repository = JsonPetRepository(repo_path)

    service = PetService(repository)

    app = ConsoleApp(service)

    app.run()

if __name__ == "__main__":
    main()
#python -m unittest test.test_service