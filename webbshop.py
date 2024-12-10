"""
__author__  = "Artem Tsvietkov"
__version__ = "1.0.0"
__email__   = "artem.tsvietkov@elev.ga.ntig.se"

webbshop.py : Webbshop-Programm med enkelt gränsnitt
"""
import csv
import os

# Представление продукта
class Product:
    def __init__(self, product_id, name, desc, price, quantity):
        self.id = product_id
        self.name = name
        self.desc = desc
        self.price = price
        self.quantity = quantity

    def __str__(self):
        # Усечение длинных названий и описаний
        name = self.name if len(self.name) <= 13 else self.name[:13] + "..."
        desc = self.desc if len(self.desc) <= 23 else self.desc[:23] + "..."
        price = f"${self.price:,.2f}"

        # Форматируем строки с отступами, чтобы все было красиво выровнено
        return f"{self.id:<4}  {name:<15}   {desc:<30}   {price:<15}   {self.quantity:<10}"

    def full_description(self):
        """Возвращает полное описание продукта"""
        return f"ID: {self.id}\nName: {self.name}\nDescription: {self.desc}\nPrice: ${self.price:,.2f}\nQuantity: {self.quantity}"

# Управление инвентарем
class Inventory:
    def __init__(self):
        self.products = []

    def load_data(self, filename):
        """Загружает данные о продуктах из CSV-файла"""
        if not os.path.exists(filename):
            return
        with open(filename, 'r') as file:
            reader = csv.DictReader(file)
            for row in reader:
                product = Product(
                    product_id=int(row['id']),
                    name=row['name'],
                    desc=row['desc'],
                    price=float(row['price']),
                    quantity=int(row['quantity'])
                )
                self.products.append(product)

    def save_data(self, filename):
        """Сохраняет данные о продуктах в CSV-файл"""
        fieldnames = ['id', 'name', 'desc', 'price', 'quantity']
        with open(filename, 'w', newline='') as file:
            writer = csv.DictWriter(file, fieldnames=fieldnames)
            writer.writeheader()
            for product in self.products:
                writer.writerow({
                    'id': product.id,
                    'name': product.name,
                    'desc': product.desc,
                    'price': product.price,
                    'quantity': product.quantity
                })

    def get_next_id(self):
        """Возвращает следующий доступный ID для нового продукта"""
        if not self.products:
            return 1
        return max(product.id for product in self.products) + 1

    def get_product_by_id(self, product_id):
        """Получить продукт по ID"""
        for product in self.products:
            if product.id == product_id:
                return product
        return None

    def remove_product(self, product_id):
        """Удалить продукт по ID и пересчитать ID"""
        self.products = [product for product in self.products if product.id != product_id]
        # Переназначаем ID, чтобы не было пропусков
        for i, product in enumerate(self.products):
            product.id = i + 1  # Сдвигаем ID на 1

    def update_product(self, product_id, field, new_value):
        """Обновить информацию о продукте"""
        product = self.get_product_by_id(product_id)
        if product:
            if field == 'name':
                product.name = new_value
            elif field == 'desc':
                product.desc = new_value
            elif field == 'price':
                product.price = float(new_value)
            elif field == 'quantity':
                product.quantity = int(new_value)

    def add_product(self, product):
        """Добавить новый продукт в инвентарь"""
        self.products.append(product)

    def get_products(self):
        """Получить строковое представление всех продуктов"""
        return "\n".join(str(product) for product in self.products)

# Отображение списка продуктов
def display_products(inventory):
    """Отображает все продукты в виде таблицы"""
    os.system('cls' if os.name == 'nt' else 'clear')
    # Печатаем заголовок таблицы с отступами
    print(f"{'ID':<4}  {'Name':<15}   {'Description':<30}   {'Price':<15}   {'Quantity':<10}")
    print("=" * 80)  # Линия-разделитель
    # Печатаем список продуктов с отступами
    print(inventory.get_products())
    print("=" * 80)

def main():
    """Главная функция для взаимодействия с пользователем и управления инвентарем"""
    inventory = Inventory()
    inventory.load_data('db_products.csv')

    while True:
        display_products(inventory)
        print("\nActions: 'add' - Add product | 'exit' - Exit program | 'view' - View product by ID | 'update' - Update product | 'delete' - Delete product")
        action = input("Enter action: ").lower()

        if action == 'exit':
            inventory.save_data('db_products.csv')
            print("Exiting the program...")
            break

        elif action == 'add':
            # Добавляем новый продукт
            new_id = inventory.get_next_id()
            name = input("Enter product name: ")
            desc = input("Enter product description: ")
            price = input("Enter product price: ")
            quantity = input("Enter product quantity: ")

            product = Product(new_id, name, desc, float(price), int(quantity))
            inventory.add_product(product)
            print("\nProduct added successfully.")

        elif action == 'view':
            # Просмотр продукта по ID
            try:
                product_id = int(input("Enter product ID: "))
                product = inventory.get_product_by_id(product_id)
                if product:
                    print("\nProduct Details:")
                    print(product.full_description())
                    input("\nPress Enter to go back.")
                else:
                    print("\nProduct not found.")
            except ValueError:
                print("Invalid input. Please enter a valid product ID.")

        elif action == 'update':
            # Обновление информации о продукте
            try:
                product_id = int(input("Enter product ID to update: "))
                product = inventory.get_product_by_id(product_id)
                if product:
                    print("\nCurrent Product Details:")
                    print(product.full_description())
                    field = input("Which field do you want to update? (name, desc, price, quantity): ").lower()
                    new_value = input(f"Enter new value for {field}: ")

                    inventory.update_product(product_id, field, new_value)
                    print(f"\nProduct {field} updated successfully.")
                else:
                    print("\nProduct not found.")
            except ValueError:
                print("Invalid input. Please enter a valid product ID.")

        elif action == 'delete':
            # Удаление продукта
            try:
                product_id = int(input("Enter product ID to delete: "))
                product = inventory.get_product_by_id(product_id)
                if product:
                    inventory.remove_product(product_id)
                    print(f"\nProduct with ID {product_id} deleted successfully.")
                else:
                    print("\nProduct not found.")
            except ValueError:
                print("Invalid input. Please enter a valid product ID.")
        else:
            print("Invalid action. Please try again.")

if __name__ == "__main__":
    main()
