import sys

from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QLineEdit, QPushButton, QVBoxLayout, QHBoxLayout, \
    QFormLayout, QMessageBox
from pyrebase import pyrebase

firebaseConfig = {
  "apiKey": "AIzaSyBeRevWSM3ggFnAnyIoJgi39PhjysZKpTA",
  "authDomain": "of7-e4325.firebaseapp.com",
  "databaseURL": "https://of7-e4325-default-rtdb.firebaseio.com/",
  "projectId": "of7-e4325",
  "storageBucket": "of7-e4325.appspot.com",
  "messagingSenderId": "123824909124",
  "appId": "1:123824909124:web:0eef61a355b198335f4511",
  "measurementId": "G-5J2785FQ8T"}

firebase = pyrebase.initialize_app(firebaseConfig)
db = firebase.database()
class Formulario(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        # Crear layouts
        form_layout = QFormLayout()
        btn_layout = QHBoxLayout()
        main_layout = QVBoxLayout()

        # Crear campos de texto
        self.nombre_herramienta_input = QLineEdit()
        self.plano_input = QLineEdit()
        self.certificado_input = QLineEdit()
        self.mc_input = QLineEdit()

        # Crear etiquetas
        nombre_herramienta_label = QLabel('Nombre de la Herramienta:')
        plano_label = QLabel('Plano:')
        certificado_label = QLabel('Certificado Algo:')
        mc_label = QLabel('MC:')

        # Añadir campos de texto y etiquetas al form layout
        form_layout.addRow(nombre_herramienta_label, self.nombre_herramienta_input)
        form_layout.addRow(plano_label, self.plano_input)
        form_layout.addRow(certificado_label, self.certificado_input)
        form_layout.addRow(mc_label, self.mc_input)

        # Crear botón
        self.agregar_btn = QPushButton('Agregar')
        self.agregar_btn.clicked.connect(self.agregar_datos)

        # Añadir botón al horizontal layout
        btn_layout.addWidget(self.agregar_btn)

        # Añadir layouts al layout principal
        main_layout.addLayout(form_layout)
        main_layout.addLayout(btn_layout)

        self.button = QPushButton("Test", self)
        self.button.setIcon(QIcon("img/qr-code.png"))

        self.show()
        # Configurar el layout principal en el QWidget
        self.setLayout(main_layout)

        # Configurar título de la ventana
        self.setWindowTitle('Formulario de Herramientas')

        # Mostrar la ventana
        self.show()

    def agregar_datos(self):
        # Aquí deberías añadir la lógica para manejar los datos ingresados
        nombre_herramienta = self.nombre_herramienta_input.text()
        plano = self.plano_input.text()
        certificado = self.certificado_input.text()
        mc= self.mc_input.text()

        datos = {
            "nombre_herramienta": nombre_herramienta,
            "plano": plano,
            "certificado_despacho": certificado,
            "mc": mc
        }

        # Enviar datos a Firebase
        db.child("herramientas").push(datos)

        # Opcional: Limpiar campos de entrada después de guardar
        self.nombre_herramienta_input.clear()
        self.plano_input.clear()
        self.certificado_input.clear()
        self.mc_input.clear()

        # Opcional: Mostrar mensaje de confirmación
        QMessageBox.information(self, "Guardado", "Datos guardados exitosamente en Firebase.")

        # Aquí podrías, por ejemplo, enviar los datos a una base de datos o realizar alguna otra acción

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Formulario()
    sys.exit(app.exec_())
