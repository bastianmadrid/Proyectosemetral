from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QPushButton, QGridLayout, \
    QMessageBox, QLineEdit, QRadioButton, QButtonGroup, QHBoxLayout, QDateEdit, \
    QTableWidget, QTableWidgetItem, QComboBox
from PyQt5.QtCore import Qt, QDate
from pyrebase import pyrebase
from PyQt5.QtGui import QPixmap, QFont, QIcon, QColor, QBrush
import sys

firebaseConfig = {
  "apiKey": "AIzaSyBeRevWSM3ggFnAnyIoJgi39PhjysZKpTA",
  "authDomain": "of7-e4325.firebaseapp.com",
  "databaseURL": "https://of7-e4325-default-rtdb.firebaseio.com/",
  "projectId": "of7-e4325",
  "storageBucket": "of7-e4325.appspot.com",
  "messagingSenderId": "123824909124",
  "appId": "1:123824909124:web:0eef61a355b198335f4511",
  "measurementId": "G-5J2785FQ8T"}

conección = pyrebase.initialize_app(firebaseConfig)
db = conección.database()
class Cotizaciones(QWidget):
    def __init__(self):
        super(Cotizaciones, self).__init__()
        self.claves_firebase = {}
        self.initialize()


    def initialize(self):
        self.setWindowTitle('Cotizaciones')
        self.setWindowIcon(QIcon('img/logosolologo.png'))
        self.setGeometry(100, 100, 680, 600)

        self.display_widget()
    def display_widget(self):
        color_primario = "#c32b30"  # Rojo
        color_fondo = "#f6f2ed"  # Crema
        color_texto = "#1d1d1c"  # Casi negro
        color_secundario = "#4b4b4c"  # Gris oscuro
        color_terciario = "#403f3e"  # Gris más oscuro
        color_acentuado = "#4c544c"  # Verde oscuro
        color_contraste = "#333334"  # Gris casi negro
        color_destacado = "#e48c9c"  # Rosa

        # Aplicar estilos con los colores de la empresa
        self.setStyleSheet(f"""
                          QWidget {{
    background-color: {color_fondo};
    color: {color_texto};
}}
QPushButton {{
    background-color: {color_primario};
    color: {color_fondo};
    border: none;
    padding: 10px;
    margin: 5px;
    border-radius: 5px;
}}
QPushButton:hover {{
    background-color: {color_secundario};
    color: {color_destacado};
}}
QLineEdit {{
    border: 1px solid {color_terciario};
    padding: 5px;
}}
QLabel {{
    color: {color_texto};
}}
""")
        estilo_deshabilitado = "QLineEdit:disabled, QDateEdit:disabled { background-color: #CDCDCD; color: #717D7E }"

        self.setStyleSheet(self.styleSheet() + estilo_deshabilitado)

        layout = QGridLayout(self)
        titulo_layout = QHBoxLayout()

        # Crear y configurar la primera imagen
        label_imagen_izquierda = QLabel(self)
        pixmap_izquierda = QPixmap("img/logosolologo.png")
        label_imagen_izquierda.setPixmap(pixmap_izquierda.scaled(40,40, Qt.KeepAspectRatio))

        # titulo
        label_titulo = QLabel("Gestión de Cotizaciones",self)
        label_titulo.setFont(QFont("Franklin Gothic",22))
        label_titulo.setAlignment(Qt.AlignCenter)

        # Crear y configurar la segunda imagen
        label_imagen_derecha = QLabel(self)
        pixmap_derecha = QPixmap("img/cotización.png")
        label_imagen_derecha.setPixmap(pixmap_derecha.scaled(30, 30, Qt.KeepAspectRatio))



        label_cotizaciones = QLabel('N° de Cotización:', self)
        label_cliente = QLabel('Cliente:', self)
        label_respuesta = QLabel('Respuesta:', self)
        label_orden_compra = QLabel('Orden de Compra:', self)
        label_Fecha = QLabel('Fecha', self)
        label_facturado = QLabel('Facturado:', self)
        label_descripcion = QLabel('Descripción:', self)

        label_cliente.setAlignment(Qt.AlignRight | Qt.AlignVCenter )
        label_orden_compra.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        label_facturado.setAlignment(Qt.AlignRight | Qt.AlignVCenter)

        # Grupo de botones de tipo RRadioButton para opciones de respuesta (Sí/No/pendiente)
        respuesta_layout = QHBoxLayout()
        self.respuesta_radiobutton_si = QRadioButton('Si', self)
        self.respuesta_radiobutton_no = QRadioButton('No', self)
        self.respuesta_radiobutton_pendiente = QRadioButton('Pendiente', self)
        self.respuesta_group = QButtonGroup(self)
        self.respuesta_group.addButton(self.respuesta_radiobutton_si)
        self.respuesta_group.addButton(self.respuesta_radiobutton_no)
        self.respuesta_group.addButton(self.respuesta_radiobutton_pendiente)

        self.respuesta_radiobutton_si.toggled.connect(self.on_respuesta_toggled)
        self.respuesta_radiobutton_no.toggled.connect(self.on_respuesta_toggled)
        self.respuesta_radiobutton_pendiente.toggled.connect(self.on_respuesta_toggled)

        respuesta_layout.addWidget(self.respuesta_radiobutton_si)
        respuesta_layout.addWidget(self.respuesta_radiobutton_no)
        respuesta_layout.addWidget(self.respuesta_radiobutton_pendiente)

        self.search_bar = QLineEdit(self)
        self.search_bar.setPlaceholderText("Buscar...")
        self.search_bar.textChanged.connect(self.realizar_busqueda)

        self.filter_options = QComboBox(self)
        self.filter_options.addItems(["Número de Cotización", "Cliente", "Fecha", "Respuesta", "Orden de compra", "Factura"])



        # Botones
        self.btn_agregar = QPushButton('Agregar', self)
        self.btn_modificar = QPushButton('Modificar', self)
        self.btn_eliminar = QPushButton('Eliminar', self)
        self.btn_agregar.setFixedSize(70, 47)

        self.btn_actualizar = QPushButton('')
        self.btn_actualizar.setIcon(QIcon("img/update.png"))
        self.btn_actualizar.setFixedSize(50, 40)

        self.btn_limpiar = QPushButton('', self)
        self.btn_limpiar.setIcon(QIcon("img/limpiar.png"))
        self.btn_limpiar.setFixedSize(50, 40)

        buttons_layout = QHBoxLayout()

        buttons_layout.addWidget(self.btn_agregar)
        buttons_layout.addWidget(self.btn_modificar)
        buttons_layout.addWidget(self.btn_eliminar)



        # Puedes agregar un poco de espacio entre los botones si lo deseas
        buttons_layout.addStretch()

        self.table_widget = QTableWidget(self)
        self.table_widget.setColumnCount(6)
        self.table_widget.setHorizontalHeaderLabels(["Número de Cotización", "Cliente", "Fecha", "Respuesta", "Orden de compra", "Factura"])
        # Permitir selección de filas en QTableWidget
        self.table_widget.setSelectionBehavior(QTableWidget.SelectRows)
        self.table_widget.setSelectionMode(QTableWidget.SingleSelection)
        self.table_widget.cellClicked.connect(self.cargar_datos_para_modificar)
        self.table_widget.itemSelectionChanged.connect(self.verificar_seleccion)


        self.table_widget.cellDoubleClicked.connect(self.mostrar_descripcion)
        # Campos de entrada
        self.cotizaciones_input = QLineEdit(self)
        self.cliente_input = QLineEdit(self)
        self.orden_compra_input = QLineEdit(self)
        self.facturado_input = QLineEdit(self)
        self.descripcion_input = QLineEdit(self)

        self.fecha_input = QDateEdit(self)
        self.fecha_input.setCalendarPopup(True)
        self.fecha_input.setDate(QDate.currentDate())

        # Conectar señales a funciones
        self.btn_agregar.clicked.connect(self.guardar_datos)
        self.btn_modificar.clicked.connect(self.modificar_datos)
        self.btn_eliminar.clicked.connect(self.eliminar_datos)
        self.btn_limpiar.clicked.connect(self.limpiar_campos)
        self.btn_actualizar.clicked.connect(self.visualizar_datos)

        titulo_layout.addWidget(label_imagen_izquierda)
        titulo_layout.addWidget(label_titulo)
        titulo_layout.addWidget(label_imagen_derecha)

        # Agregar widgets al diseño
        layout.addLayout(titulo_layout, 0, 0, 1, 4)  # Asegúrate de ajustar los parámetros según la disposición deseada
        # Asegúrate de que el título abarque todas las columnas
        layout.addWidget(label_cotizaciones, 1, 0)
        layout.addWidget(self.cotizaciones_input, 1, 1)

        layout.addWidget(label_cliente, 1, 2)
        layout.addWidget(self.cliente_input, 1, 3)

        layout.addWidget(label_respuesta, 3, 0)
        layout.addLayout(respuesta_layout, 3, 1)

        layout.addWidget(label_orden_compra, 3, 2)
        layout.addWidget(self.orden_compra_input, 3, 3)

        layout.addWidget(label_Fecha, 4, 0)
        layout.addWidget(self.fecha_input, 4, 1)

        layout.addWidget(label_facturado, 4, 2)
        layout.addWidget(self.facturado_input, 4, 3)

        layout.addWidget(label_descripcion, 5, 0)  # Ajusta la fila y la columna según sea necesario
        layout.addWidget(self.descripcion_input, 5, 1, 1, 3)

        layout.addWidget(self.search_bar, 7, 2)  # Asegúrate de usar las coordenadas correctas
        layout.addWidget(self.filter_options, 7, 3)

        layout.addLayout(buttons_layout, 6, 1, 1, 4)
        layout.addWidget(self.btn_actualizar, 6, 0)
        layout.addWidget(self.btn_limpiar, 6, 3)
        layout.addWidget(self.table_widget, 8, 0, 1, 4)



        self.habilitar_campos(False)

        self.visualizar_datos()



    def on_respuesta_toggled(self):
        # Habilita o deshabilita los campos dependiendo del estado del botón de radio "Sí"
        respuesta_si = self.respuesta_radiobutton_si.isChecked()
        respuesta_pendiente = self.respuesta_radiobutton_pendiente.isChecked()
        self.habilitar_campos(respuesta_si or respuesta_pendiente)

    def todos_los_campos_llenos(self, datos):
        # Verifica si todos los campos en el diccionario 'datos' no están vacíos
        return all(datos.get(campo) for campo in
                   ["Numero_cotizacion", "Cliente", "Fecha", "Fespuesta", "Orden_compra", "Facturado"])

    def realizar_busqueda(self):
        search_text = self.search_bar.text().lower()
        filter_option = self.filter_options.currentText()

        column_map = {
            "Número de Cotización": 0,
            "Cliente": 1,
            "Fecha": 2,
            "Respuesta": 3,
            "Orden de compra": 4,
            "Factura": 5
        }

        column_to_filter = column_map.get(filter_option, 0)

        for row in range(self.table_widget.rowCount()):
            item = self.table_widget.item(row, column_to_filter)
            if item and search_text in item.text().lower():
                self.table_widget.setRowHidden(row, False)
            else:
                self.table_widget.setRowHidden(row, True)


    def habilitar_campos(self, habilitar):
        # Habilita o deshabilita los campos
        self.orden_compra_input.setEnabled(habilitar)
        self.fecha_input.setEnabled(habilitar)
        self.facturado_input.setEnabled(habilitar)

    def verificar_seleccion(self):
        # Verificar si hay una fila seleccionada en la tabla
        hay_fila_seleccionada = len(self.table_widget.selectedItems()) > 0
        if hay_fila_seleccionada:
            self.btn_agregar.setDisabled(True)
            self.btn_agregar.setText("X︎")
            self.btn_agregar.setStyleSheet("color: black ;font-size: 16px;")  # Cambiar el color del texto a rojo
        else:
            self.btn_agregar.setEnabled(True)
            self.btn_agregar.setText("Agregar")
            self.btn_agregar.setStyleSheet("")

    def visualizar_datos(self):
        # Limpiar la tabla antes de cargar nuevos datos
        self.table_widget.setRowCount(0)
        self.claves_firebase.clear()

        # Obtener datos de Firebase y cargarlos en la tabla
        try:
            cotizaciones = db.child("Cotizaciones").get()
            if cotizaciones.each() is not None:
                for cotizacion in cotizaciones.each():
                    datos = cotizacion.val()
                    fila_actual = self.table_widget.rowCount()
                    self.table_widget.insertRow(fila_actual)

                    # Almacenar la clave de Firebase en el diccionario
                    self.claves_firebase[fila_actual] = cotizacion.key()

                    # Si hay un término de búsqueda y una categoría seleccionada, filtrar los resultados


                # Crear QTableWidgetItem para cada campo
                    self.table_widget.setItem(fila_actual, 0, QTableWidgetItem(datos.get("Numero_cotizacion", "")))
                    self.table_widget.setItem(fila_actual, 1, QTableWidgetItem(datos.get("Cliente", "")))
                    self.table_widget.setItem(fila_actual, 2, QTableWidgetItem(datos.get("Fecha", "")))
                    self.table_widget.setItem(fila_actual, 3, QTableWidgetItem(datos.get("Fespuesta", "")))
                    self.table_widget.setItem(fila_actual, 4, QTableWidgetItem(datos.get("Orden_compra", "")))
                    self.table_widget.setItem(fila_actual, 5, QTableWidgetItem(datos.get("Facturado", "")))

                    # Aquí aplicarías las condiciones para cambiar el color de las filas
                    respuesta = datos.get("Fespuesta", "")
                    orden_compra = datos.get("Orden_compra", "")
                    facturado = datos.get("Facturado", "")

                    # Condición para cambiar el color de la fila
                    if respuesta == "Si" and orden_compra and facturado:
                        color = QColor(158, 255, 130)  # Verde
                        for columna in range(self.table_widget.columnCount()):
                            item = self.table_widget.item(fila_actual, columna)
                            if item is not None:
                                item.setBackground(QBrush(color))
                    elif respuesta == "No":
                        color = QColor(255, 145, 145)  # Rojo
                        for columna in range(self.table_widget.columnCount()):
                            item = self.table_widget.item(fila_actual, columna)
                            if item is not None:
                                item.setBackground(QBrush(color))
                    elif respuesta == "Pendiente":
                        color = QColor(255, 217, 151)  # Naranja
                        for columna in range(self.table_widget.columnCount()):
                            item = self.table_widget.item(fila_actual, columna)
                            if item is not None:
                                item.setBackground(QBrush(color))
                    else:
                        color = QColor(255, 217, 151)  # Naranja
                        for columna in range(self.table_widget.columnCount()):
                            item = self.table_widget.item(fila_actual, columna)
                            if item is not None:
                                item.setBackground(QBrush(color))
                else:

                    print("No hay datos para mostrar.")
            else:
             print("No hay datos para mostrar.")

        except Exception as e:
            print(f"Error al obtener datos: {e}")

    def cargar_datos_para_modificar(self, row, column):
        # Cargar datos de la fila seleccionada en los campos de entrada
        self.cotizaciones_input.setText(self.table_widget.item(row, 0).text())
        self.cliente_input.setText(self.table_widget.item(row, 1).text())
        fecha_texto = self.table_widget.item(row, 2).text()
        #fecha proceso
        fecha = QDate.fromString(fecha_texto, "dd-MM-yyyy")
        if fecha.isValid():
            self.fecha_input.setDate(fecha)
        else:
            print("Formato de fecha inválido o fecha no disponible.")
        #respuesta proceso
        respuesta_texto = self.table_widget.item(row, 3).text()
        # Establecer el botón de radio correspondiente
        if respuesta_texto == "Si":
            self.respuesta_radiobutton_si.setChecked(True)
        elif respuesta_texto == "No":
            self.respuesta_radiobutton_no.setChecked(True)
        elif respuesta_texto == "Pendiente":
            self.respuesta_radiobutton_pendiente.setChecked(True)
        else:
            print("Valor de respuesta desconocido o no disponible.")

        self.orden_compra_input.setText(self.table_widget.item(row, 4).text())
        item_facturado = self.table_widget.item(row, 5)  # Asegúrate de que el índice de la columna sea correcto
        if item_facturado is not None:
                 self.facturado_input.setText(item_facturado.text())
        else:
                 print("No hay datos en la columna 'Facturado' para esta fila.")


    def mostrar_descripcion(self, row, column):
        # Asegurarse de que se hizo doble clic en la columna del número de cotización
        if column == 0:  # Cambia '0' por el índice de la columna del número de cotización
            numero_cotizacion = self.table_widget.item(row, column).text()

            # Obtener la descripción de Firebase usando el número de cotización
            try:
                cotizaciones = db.child("Cotizaciones").get()
                for cotizacion in cotizaciones.each():
                    if cotizacion.val()["Numero_cotizacion"] == numero_cotizacion:
                        descripcion = cotizacion.val().get("Descripción", "No hay descripción disponible.")
                        QMessageBox.information(self, f"Descripción de {numero_cotizacion}", descripcion)
                        break
            except Exception as e:
                QMessageBox.warning(self, "Error", f"No se pudo obtener la descripción: {e}")

    def guardar_datos(self):
        # Obtener los valores de los campos de entrada
        numero_cotizacion = self.cotizaciones_input.text()
        cliente = self.cliente_input.text()
        descripcion = self.descripcion_input.text()
        if self.respuesta_radiobutton_si.isChecked():
            respuesta = "Si"
        elif self.respuesta_radiobutton_no.isChecked():
            respuesta = "No"
        elif self.respuesta_radiobutton_pendiente.isChecked():
            respuesta = "Pendiente"

        # Verificar que los campos obligatorios estén completos
        if not numero_cotizacion or not cliente or not respuesta:
            QMessageBox.warning(self, "Error",
                                "Por favor, complete los campos de número de cotización, cliente y respuesta.")
            return

        # Establecer "Orden de Compra" y "Facturado" como "No válido" si la respuesta es "No"
        orden_compra = "No válido" if respuesta == "No" else self.orden_compra_input.text()
        facturado = "No válido" if respuesta == "No" else self.facturado_input.text()
        fecha = self.fecha_input.date().toString("dd-MM-yyyy")


        # Crear un diccionario con los datos
        datos_cotizacion = {
            "Numero_cotizacion": numero_cotizacion,
            "Cliente": cliente,
            "Descripción": descripcion,
            "Orden_compra": orden_compra,
            "Fecha": fecha,
            "Facturado": facturado,
            "Fespuesta": respuesta

        }

        # Enviar los datos a Firebase
        try:
            db.child("Cotizaciones").push(datos_cotizacion)
            QMessageBox.information(self, "Éxito", "Datos guardados correctamente.")
        except Exception as e:
            QMessageBox.warning(self, "Error", f"Error al guardar datos: {e}")

        self.limpiar_campos()

    def modificar_datos(self):
        fila_seleccionada = self.table_widget.currentRow()
        if fila_seleccionada == -1:
            QMessageBox.warning(self, "Advertencia", "Seleccione una fila para modificar.")
            return

        # Obtener la clave de Firebase de la fila seleccionada
        clave_firebase = self.claves_firebase.get(fila_seleccionada)
        if not clave_firebase:
            QMessageBox.warning(self, "Error", "No se pudo obtener la clave de Firebase.")
            return

        # Recoger los datos de los campos de entrada
        datos_actualizados = {
            "Numero_cotizacion": self.cotizaciones_input.text(),
            "Cliente": self.cliente_input.text(),
            "Descripción": self.descripcion_input.text(),
            "Orden_compra": self.orden_compra_input.text(),
            "Fecha": self.fecha_input.date().toString("dd-MM-yyyy"),
            "Facturado": self.facturado_input.text(),
            "Fespuesta": "Si" if self.respuesta_radiobutton_si.isChecked() else "No" if self.respuesta_radiobutton_no.isChecked() else "Pendiente"
        }

        # Verificar que los campos obligatorios estén completos
        if not datos_actualizados["Numero_cotizacion"] or not datos_actualizados["Cliente"]:
            QMessageBox.warning(self, "Error", "Por favor, complete los campos obligatorios.")
            return

        # Enviar los datos actualizados a Firebase
        try:
            db.child("Cotizaciones").child(clave_firebase).update(datos_actualizados)
            QMessageBox.information(self, "Éxito", "Datos actualizados correctamente.")
            self.visualizar_datos()  # Actualizar la tabla
        except Exception as e:
            QMessageBox.warning(self, "Error", f"Error al actualizar datos: {e}")

    def eliminar_datos(self):
        selected_items = self.table_widget.selectedItems()
        if selected_items:
            row = selected_items[0].row()  # Obtén la fila seleccionada
            firebase_key = self.claves_firebase.get(row)  # Obtén la clave de Firebase

            if firebase_key:
                # Eliminar de Firebase
                try:
                    db.child("Cotizaciones").child(firebase_key).remove()
                    QMessageBox.information(self, "Éxito", "Cotización eliminada correctamente.")

                    # Actualizar la tabla
                    self.table_widget.removeRow(row)
                    del self.claves_firebase[row]  # Elimina la clave del diccionario

                except Exception as e:
                    QMessageBox.warning(self, "Error", f"No se pudo eliminar la cotización: {e}")
            else:
                QMessageBox.warning(self, "Error", "No se encontró la clave de Firebase para la fila seleccionada.")
        else:
            QMessageBox.warning(self, "Error", "Por favor, seleccione una fila para eliminar.")


    def limpiar_campos(self):
        self.cotizaciones_input.clear()
        self.descripcion_input.clear()
        self.cliente_input.clear()
        self.orden_compra_input.clear()
        self.facturado_input.clear()
        self.fecha_input.setDate(QDate.currentDate())

        self.table_widget.clearSelection()

        self.respuesta_group.setExclusive(False)
        self.respuesta_radiobutton_si.setChecked(False)
        self.respuesta_radiobutton_no.setChecked(False)
        self.respuesta_radiobutton_pendiente.setChecked(False)
        self.respuesta_group.setExclusive(True)

    # Cierre de ventana
    def closeEvent(self, event):
        Cuadro = QMessageBox.warning(self, "CERRAR", "¿Está seguro de cerrar la ventana?", QMessageBox.Yes | QMessageBox.No, QMessageBox.Yes)
        if Cuadro == QMessageBox.Yes:
            event.accept()
        elif Cuadro == QMessageBox.No:
            event.ignore()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = Cotizaciones()
    window.show()
    sys.exit(app.exec_())