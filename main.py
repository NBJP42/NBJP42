import sys
from abc import ABC, abstractmethod
from datetime import datetime
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QPushButton, QLabel, 
    QWidget, QGridLayout, QHBoxLayout, QVBoxLayout
)
from PyQt5.QtCore import Qt

# --- 1. Абстрактный класс и кастомный Map ---

class BaseSkill(ABC):
    @abstractmethod
    def activate(self):
        pass

class SkillMap:
    """Кастомный Map на списках (запрещено использовать стандартный dict)."""
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


# --- 3. Кастомный UI компонент и генерация объектов ---

class SkillIconButton(QPushButton):
    """Кастомная квадратная кнопка-иконка навыка."""
    def __init__(self, skill_obj, parent=None):
        super().__init__(parent)
        self.skill = skill_obj
        self.setFixedSize(85, 85)
        self.setText(f"{self.skill.name}\n\nур. {self.skill.level}")
        self.setStyleSheet("""
            background-color: #2c3e50; 
            color: #fff; 
            font-size: 11px; 
            border-radius: 8px;
            font-weight: bold;
        """)

    def update_text(self):
        self.setText(f"{self.skill.name}\n\nур. {self.skill.level}")

def create_initial_skills():
    """Создание коллекции из 10+ объектов пользовательского класса."""
    names = [
        "Фаербол", "Ледяной шип", "Щит", "Молния", 
        "Хил", "Тень", "Яд", "Берсерк", "Волна", "Метеор"
    ]
    return [Skill(name, level=i + 1) for i, name in enumerate(names)]


# --- 4. Главное окно и сохранение отчета ---

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("RPG Skill Manager — Персонаж и Навыки")
        self.resize(550, 650)

        self.time_in = datetime.now()
        self.skills = create_initial_skills()

        self.skill_map = SkillMap()
        for skill in self.skills:
            self.skill_map.put(skill.name, skill)

        central_widget = QWidget()
        main_layout = QVBoxLayout()

        # --- БЛОК ПЕРСОНАЖА СЛЕВА И АКТИВНЫЙ НАВЫК ---
        hero_panel = QWidget()
        hero_panel.setStyleSheet("background-color: #ecf0f1; border-radius: 10px; padding: 10px;")
        hero_layout = QHBoxLayout()

        # «Человечек» (иконка/аватар персонажа)
        self.hero_avatar = QLabel("🕵")
        self.hero_avatar.setStyleSheet("font-size: 40px; background-color: #bdc3c7; border-radius: 25px; padding: 5px;")
        self.hero_avatar.setAlignment(Qt.AlignCenter)
        self.hero_avatar.setFixedSize(60, 60)

        # Текст слева от человечка: какой скилл активирован
        hero_info_layout = QVBoxLayout()
        hero_title = QLabel("Герой")
        hero_title.setStyleSheet("font-weight: bold; font-size: 12px; color: #7f8c8d;")
        
        self.active_skill_label = QLabel("Активный навык: Не выбран")
        self.active_skill_label.setStyleSheet("font-weight: bold; font-size: 14px; color: #2c3e50;")

        hero_info_layout.addWidget(hero_title)
        hero_info_layout.addWidget(self.active_skill_label)

        hero_layout.addWidget(self.hero_avatar)
        hero_layout.addLayout(hero_info_layout)
        hero_layout.addStretch()
        hero_panel.setLayout(hero_layout)

        main_layout.addWidget(hero_panel)

        # Заголовок для сетки скиллов
        self.title_label = QLabel("Дерево навыков (выберите навык или измените уровень):")
        self.title_label.setStyleSheet("font-weight: bold; font-size: 13px; margin-top: 10px;")
        main_layout.addWidget(self.title_label)

        # --- СЕТКА КВАДРАТНЫХ ИКОНОК СО СТРЕЛОЧКАМИ ---
        grid_layout = QGridLayout()
        
        for i, skill in enumerate(self.skills):
            row = i // 2  # 2 столбца
            col = i % 2   

            cell_widget = QWidget()
            cell_layout = QHBoxLayout()
            cell_layout.setContentsMargins(0, 0, 0, 0)

            # Квадратная иконка навыка
            icon_btn = SkillIconButton(skill)
            icon_btn.clicked.connect(lambda checked, s=skill: self.on_skill_clicked(s))

            # Кнопки управления уровнем (▲ и ▼)
            btn_layout = QVBoxLayout()
            btn_layout.setSpacing(2)
            
            up_btn = QPushButton("▲")
            up_btn.setFixedSize(30, 40)
            up_btn.setStyleSheet("font-size: 11px; font-weight: bold;")
            
            down_btn = QPushButton("▼")
            down_btn.setFixedSize(30, 40)
            down_btn.setStyleSheet("font-size: 11px; font-weight: bold;")

            up_btn.clicked.connect(lambda checked, s=skill, btn=icon_btn: self.change_level(s, btn, 1))
            down_btn.clicked.connect(lambda checked, s=skill, btn=icon_btn: self.change_level(s, btn, -1))

            btn_layout.addWidget(up_btn)
            btn_layout.addWidget(down_btn)

            cell_layout.addWidget(icon_btn)
            cell_layout.addLayout(btn_layout)
            cell_widget.setLayout(cell_layout)

            grid_layout.addWidget(cell_widget, row, col)

        main_layout.addLayout(grid_layout)

        central_widget.setLayout(main_layout)
        self.setCentralWidget(central_widget)

    def on_skill_clicked(self, skill):
        # При клике на иконку обновляем надпись возле человечка
        self.active_skill_label.setText(skill.activate())

    def change_level(self, skill, icon_btn, delta):
        # Изменяем уровень через сеттер с защитой данных
        skill.level = skill.level + delta
        icon_btn.update_text()
        # Если изменен текущий навык, обновляем текст у человечка тоже
        if f"ур. {skill.level - delta}" in self.active_skill_label.text() or skill.name in self.active_skill_label.text():
            self.active_skill_label.setText(skill.activate())

    def closeEvent(self, event):
        """Сохранение отчета в файл при закрытии приложения."""
        time_out = datetime.now()
        
        with open("report.txt", "w", encoding="utf-8") as f:
            f.write("+---------------------------------------------------+\n")
            f.write("|   login    |      time_in      |     time_out     |\n")
            f.write("|------------|-------------------|------------------|\n")
            
            t_in_str = self.time_in.strftime("%d.%m.%Y %H:%M:%S")
            t_out_str = time_out.strftime("%d.%m.%Y %H:%M:%S")
            
            f.write(f"| Student    | {t_in_str} | {t_out_str} |\n")
            f.write("+---------------------------------------------------+\n")
            
        event.accept()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())