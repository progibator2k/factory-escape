"""Мини текстовая игра «Побег с завода»."""

ROOMS = {
    "цех": {
        "desc": "Вы в тёмном цеху. Вокруг молчат станки. На выходе — коридор (север), справа — склад (восток).",
        "exits": {"север": "коридор", "восток": "склад"},
        "items": ["фонарик"],
    },
    "склад": {
        "desc": "Склад, заставленный ящиками. Выход обратно в цех — на западе.",
        "exits": {"запад": "цех"},
        "items": ["лом"],
    },
    "коридор": {
        "desc": "Длинный коридор. На юге — цех, на востоке — офис, на севере — стальная дверь на проходную.",
        "exits": {"юг": "цех", "восток": "офис", "север": "проходная"},
        "items": [],
    },
    "офис": {
        "desc": "Тёмный офис начальника смены. В углу стоит запертый металлический шкафчик. Выход — на западе.",
        "exits": {"запад": "коридор"},
        "items": [],
    },
    "проходная": {
        "desc": "Проходная. Свобода!",
        "exits": {},
        "items": [],
    },
}

HELP_TEXT = (
    "Команды:\n"
    "  осмотреться           — описание комнаты и предметов\n"
    "  идти <направление>    — север / юг / запад / восток\n"
    "  взять <предмет>       — поднять предмет\n"
    "  использовать <предмет>— применить предмет\n"
    "  инвентарь             — что у вас с собой\n"
    "  помощь                — эта справка\n"
    "  выход                 — выйти из игры"
)


class Game:
    def __init__(self):
        self.room = "цех"
        self.inventory = []
        self.items = {name: list(room["items"]) for name, room in ROOMS.items()}
        self.locker_open = False
        self.finished = False
        self.moves = 0

    def describe(self):
        text = ROOMS[self.room]["desc"]
        items = self.items[self.room]
        if items:
            text += "\nВы видите: " + ", ".join(items) + "."
        return text

    def go(self, direction):
        dest = ROOMS[self.room]["exits"].get(direction)
        if dest is None:
            return "Туда пройти нельзя."
        if dest == "офис" and "фонарик" not in self.inventory:
            return "В офисе слишком темно. Нужен фонарик."
        if dest == "проходная" and "ключ-карта" not in self.inventory:
            return "Дверь заперта электронным замком. Нужна ключ-карта."
        self.room = dest
        self.moves += 1
        if dest == "проходная":
            self.finished = True
            return f"Вы прикладываете карту, дверь открывается... Вы сбежали с завода за {self.moves} ходов! ПОБЕДА!"
        return self.describe()

    def take(self, item):
        if item not in self.items[self.room]:
            return "Здесь нет такого предмета."
        self.items[self.room].remove(item)
        self.inventory.append(item)
        return f"Вы взяли: {item}."

    def use(self, item):
        if item not in self.inventory:
            return "У вас нет такого предмета."
        if item == "лом":
            if self.room == "офис" and not self.locker_open:
                self.locker_open = True
                self.items["офис"].append("ключ-карта")
                return "Вы взломали шкафчик ломом. Внутри лежит ключ-карта!"
            return "Здесь лом не пригодится."
        return "Ничего не происходит."

    def show_inventory(self):
        if not self.inventory:
            return "Ваши карманы пусты."
        return "У вас с собой: " + ", ".join(self.inventory) + "."

    def handle(self, command):
        """Обрабатывает команду игрока и возвращает текст ответа."""
        parts = command.strip().lower().split(maxsplit=1)
        if not parts:
            return "Введите команду. Напишите «помощь»."
        action = parts[0]
        arg = parts[1] if len(parts) > 1 else ""

        if action in ("осмотреться", "осмотр"):
            return self.describe()
        if action in ("идти", "иди"):
            return self.go(arg)
        if action in ("взять", "возьми"):
            return self.take(arg)
        if action in ("использовать", "используй"):
            return self.use(arg)
        if action == "инвентарь":
            return self.show_inventory()
        if action == "помощь":
            return HELP_TEXT
        return "Непонятная команда. Напишите «помощь»."


def main():
    game = Game()
    print("=== ПОБЕГ С ЗАВОДА ===")
    print("Вы заперты на заводе. Найдите способ выбраться!\n")
    print(HELP_TEXT + "\n")
    print(game.describe())
    while not game.finished:
        command = input("\n> ")
        if command.strip().lower() == "выход":
            print("Игра окончена.")
            break
        print(game.handle(command))


if __name__ == "__main__":
    main()