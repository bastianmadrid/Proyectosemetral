from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QPushButton

from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap, QFont, QIcon, QLinearGradient, QColor, QPalette, QBrush
from Cotizaciones import Cotizaciones
from Herramientas import Herramientas
import sys

class VentanaPrincipal(QWidget):

    def __init__(self):
        super(VentanaPrincipal, self).__init__()
        self.initialize()


    def initialize(self):
        self.setGeometry(480,150,500,500)
        self.setWindowTitle("OF7")
        self.display_widgets()
        self.setWindowIcon(QIcon('img/logosolologo.png'))
        gradient = QLinearGradient(0, 0, self.width(), self.height())
        gradient.setColorAt(0.0, QColor("#c32b30"))
        gradient.setColorAt(0.5, QColor("#4c544c"))
        gradient.setColorAt(1.0, QColor("#403f3e"))

        p = QPalette()
        p.setBrush(QPalette.Window, QBrush(gradient))
        self.setPalette(p)

    def display_widgets(self):
        color_primario = "#c32b30"  # Rojo
        color_fondo = "#f6f2ed"  # Crema

        color_texto = "#f6f2ed"  # Casi negro
        color_secundario = "#4b4b4c"
        color_destacado = "#e48c9c"
        color_terciario = "#403f3e"

        self.setStyleSheet(f"""
    QPushButton {{
        background-color: {color_primario};  # Color rojo para el fondo del botón
        color: #f6f2ed;  # Color casi negro para el texto
        border: none;
        padding: 10px;
        margin: 5px;
        border-radius: 5px;
    }}
    QPushButton:hover {{
        background-color: {color_secundario};  # Color para el fondo del botón al pasar el mouse
        color: {color_destacado};  # Color para el texto al pasar el mouse
    }}
    QLineEdit {{
        border: 1px solid {color_terciario};
        padding: 5px;
    }}
    QLabel {{
        color: {color_texto};
    }}
""")

        logo_img = "img/logosolologo.png"
        try:
                with open(logo_img):

                    etiqueta_logo = QLabel(self)
                    pixmap = QPixmap(logo_img)
                    etiqueta_logo.setPixmap( pixmap)
                    etiqueta_logo.move(135,70)
        except FileNotFoundError:
                print("no se encontro el logo")

        etiqueta_titulo = QLabel("OF7",self)
        etiqueta_titulo.move(0,-100)
        etiqueta_titulo.setFont(QFont("Franklin Gothic",26))
        etiqueta_titulo.resize(500,300)
        etiqueta_titulo.setAlignment(Qt.AlignCenter)

        self.debajo_logo = QLabel("Software de escritorio",self)
        self.debajo_logo.setFont(QFont("Franklin Gothic", 26))
        self.debajo_logo.setAlignment(Qt.AlignCenter)

        self.debajo_logo.move(80,300)


        #botones
        #Cotizaciones

        self.botton_cotizaciones = QPushButton("G. Cotizaciones",self)
        self.botton_cotizaciones.resize(150,30)
        self.botton_cotizaciones.move(30,400)

        #Herramientas
        self.botton_herramientas = QPushButton("G. Herramientas", self)
        self.botton_herramientas.resize(150, 30)
        self.botton_herramientas.move(320, 400)
        #Direcciones botones

        self.botton_cotizaciones.clicked.connect(self.ir_aC)
        self.botton_herramientas.clicked.connect(self.ir_aH)


    def ir_aC(self):
        self.ir_cotizaciones = Cotizaciones()
        self.ir_cotizaciones.show()

    def ir_aH(self):
        self.ir_herramientas = Herramientas()
        self.ir_herramientas.show()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = VentanaPrincipal()
    window.show()
    sys.exit(app.exec_())

