from faker import Faker
from typing import Any

class DataGenerator:
    def __init__(self):
        self.fake = Faker()

    def generate(self, function: str, *args: str) -> Any:
        # Vérifie si la fonction demandée existe dans Faker
        if hasattr(self.fake, function) and callable(getattr(self.fake, function)):
            # Obtient la fonction demandée
            faker_function = getattr(self.fake, function)

            try:
                # Appelle la fonction avec les arguments fournis
                result = faker_function(*args)
                return result
            except Exception as e:
                print(f"Erreur lors de l'appel de la fonction {function}: {e}")
                return None
        else:
            print(f"La fonction {function} n'existe pas dans le module faker.")
            return None

# Exemple d'utilisation
generator = DataGenerator()
result = generator.generate("name")
print(result)  # Output: Un nom généré aléatoirement
fake = Faker()
print(fake.phone_number())  # Output: Un nom généré aléatoirement
