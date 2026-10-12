from PyQt5.QtWidgets import QPushButton

class SkillIconButton(QPushButton):
    """Квадратная кнопка-иконка навыка."""
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