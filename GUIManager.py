import sys
from PyQt6.QtWidgets import QApplication, QWidget

app = QApplication([sys.argv])

window = QWidget()

window.show()

sys.exit(app.exec())