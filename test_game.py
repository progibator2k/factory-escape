from game import Game


def test_start_room():
    game = Game()
    assert game.room == "цех"
    assert game.inventory == []


def test_take_item():
    game = Game()
    game.handle("взять фонарик")
    assert "фонарик" in game.inventory


def test_cannot_take_missing_item():
    game = Game()
    assert "нет такого" in game.handle("взять лом")


def test_cannot_go_wrong_direction():
    game = Game()
    assert "нельзя" in game.handle("идти запад")


def test_office_requires_flashlight():
    game = Game()
    game.handle("идти север")
    result = game.handle("идти восток")
    assert "темно" in result
    assert game.room == "коридор"


def test_gate_requires_keycard():
    game = Game()
    game.handle("идти север")
    result = game.handle("идти север")
    assert "заперта" in result
    assert not game.finished


def test_full_walkthrough_wins():
    game = Game()
    commands = [
        "взять фонарик",
        "идти восток",
        "взять лом",
        "идти запад",
        "идти север",
        "идти восток",
        "использовать лом",
        "взять ключ-карта",
        "идти запад",
        "идти север",
    ]
    for cmd in commands:
        game.handle(cmd)
    assert game.finished
    assert game.room == "проходная"

def test_moves_counter():
    game = Game()
    game.handle("идти север")
    game.handle("идти юг")
    assert game.moves == 2