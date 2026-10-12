from abc import ABC, abstractmethod

# --- 1. Абстрактный класс и кастомный Map ---

class BaseSkill(ABC):
    @abstractmethod
    def activate(self):
        pass

class SkillMap:
    """Кастомный Map на списках."""
    def __init__(self):
        self._data = []

    def put(self, key, value):
        for item in self._data:
            if item[0] == key:
                item[1] = value
                return
        self._data.append([key, value])

    def get(self, key):
        for item in self._data:
            if item[0] == key:
                return item[1]
        return None


# --- 2. Класс навыка (ООП, геттеры/сеттеры, спец. методы) ---

class Skill(BaseSkill):
    def __init__(self, name: str, level: int):
        self._name = name
        self._level = level

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, value):
        if value:
            self._name = value

    @property
    def level(self):
        return self._level

    @level.setter
    def level(self, value):
        if 1 <= value <= 100:
            self._level = value

    def activate(self):
        return f"Активный навык: {self._name} (ур. {self._level})"

    def __str__(self):
        return f"Skill: {self._name} (Lvl {self._level})"

    def __repr__(self):
        return f"Skill(name='{self._name}', level={self._level})"

    def __eq__(self, other):
        return isinstance(other, Skill) and self._name == other._name

    def __lt__(self, other):
        return self._level < other._level