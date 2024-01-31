from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QPushButton, QGridLayout, \
        QMessageBox, QLineEdit, QFileDialog, QHBoxLayout, QTableWidget, \
        QTableWidgetItem, QDateEdit, QHeaderView, QComboBox
from PyQt5.QtCore import Qt, QDate, QTimer, QPropertyAnimation, QEasingCurve
from PyQt5.QtGui import QFont, QIcon, QPixmap
import qrcode
import pyrebase
from datetime import datetime
import sys
import os
import webbrowser

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
firebase_storage = firebase.storage()

class Herramientas(QWidget):
        def __init__(self):
            super(Herramientas, self).__init__()
            self.initialize()
            self.ruta_pdf_temporal = None
            self.nombre_pdf_temporal = None
            self.table_widget.cellClicked.connect(self.abrir_pdf)
            self.label_subida_exitosa = QLabel('', self)
            self.label_subida_exitosa.setGeometry(500, 100, 200, 50)  # Ajusta la posición según necesidad
            self.btn_generar_qr.hide()

            self.timer_ocultar_mensaje = QTimer(self)
            self.timer_ocultar_mensaje.timeout.connect(self.ocultarMensaje)
        def initialize(self):
            self.setWindowTitle('Herramientas')
            self.setWindowIcon(QIcon('img/logosolologo.png'))
            self.setGeometry(600, 100, 700, 600)


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
            layout = QGridLayout(self)
            titulo_layout = QHBoxLayout()
            search_layout = QHBoxLayout()

            # Añadir la barra de búsqueda y el combo box al QHBoxLayout

            # Imagen izquierda

            label_imagen_izquierda = QLabel(self)
            pixmap_izquierda = QPixmap("img/logosolologo.png")
            tamaño_ampliado = 40
            label_imagen_izquierda.setPixmap(pixmap_izquierda.scaled(tamaño_ampliado, tamaño_ampliado, Qt.IgnoreAspectRatio))
            label_imagen_izquierda.setAlignment(Qt.AlignRight)

            # Titulo
            label_titulo = QLabel("Gestión de Herramientas", self)
            label_titulo.setFont(QFont("Franklin Gothic", 22))
            label_titulo.setAlignment(Qt.AlignCenter)

            #imagen derecha
            label_imagen_derecha = QLabel(self)
            pixmap_derecha = QPixmap("img/Herramientas.png")
            label_imagen_derecha.setPixmap(pixmap_derecha.scaled(30, 30, Qt.KeepAspectRatio))

            titulo_layout.addWidget(label_imagen_izquierda)
            titulo_layout.addWidget(label_titulo)
            titulo_layout.addWidget(label_imagen_derecha)

            label_nherramienta = QLabel('Nombre Herramienta:', self)
            label_plano = QLabel('Plano:', self)
            label_end = QLabel('Certificados:', self)
            label_certificado = QLabel('Orden de compra:', self)
            label_mc = QLabel('Control Dimencional:', self)

            # Botones
            self.btnagregar = QPushButton('Agregar')
            self.btn_modificar = QPushButton('Modificar')
            self.btn_eliminar = QPushButton('Eliminar')
            self.btn_subir_pdf = QPushButton('Subir PDF')

            # Configuraciones adicionales para botones y campos de texto
            self.btnagregar.setFixedSize(120, 40)
            self.btn_modificar.setFixedSize(120, 40)
            self.btn_eliminar.setFixedSize(120, 40)
            self.btn_subir_pdf.setFixedSize(120, 40)

            self.btn_actualizar = QPushButton('')
            self.btn_actualizar.setIcon(QIcon("img/update.png"))
            self.btn_actualizar.setFixedSize(50, 40)

            self.btn_limpiar = QPushButton('', self)
            self.btn_limpiar.setFixedSize(50, 40)
            self.btn_limpiar.setIcon(QIcon("img/limpiar.png"))

            self.btn_limpiar.clicked.connect(self.limpiar_todo)

            buttons_update_clear_layout = QHBoxLayout()
            buttons_update_clear_layout.addWidget(self.btn_actualizar)
            buttons_update_clear_layout.addWidget(self.btn_limpiar)

            # Campos de entrada
            self.nherramienta_input = QLineEdit()
            self.plano_input = QLineEdit()
            self.nombre_pdf_input = QLineEdit(self)
            self.certificado_despacho_input = QLineEdit()
            self.mc_input = QLineEdit()
            buttons_layout = QHBoxLayout()

            # fecha cuando llego
            entrega_lbl = QLabel('Fecha de ingreso', self)
            self.date_edit = QDateEdit(self)
            self.date_edit.setDate(QDate.currentDate())  # Establecer la fecha actual
            self.date_edit.setCalendarPopup(True)

          # Espaciador para empujar los botones hacia el centro
            buttons_layout = QHBoxLayout()
            buttons_layout.addWidget(self.btnagregar)
            buttons_layout.addWidget(self.btn_modificar)
            buttons_layout.addWidget(self.btn_eliminar)
            # Agregar el botón al layout


            buttons_container = QWidget()
            buttons_container.setLayout(buttons_layout)
            #creacion de vista de la BD
            self.table_widget = QTableWidget(self)
            self.table_widget.setColumnCount(6)  # Número de columnas
            self.table_widget.setHorizontalHeaderLabels(["Nombre Herramienta", "Plano", "O. de Compra", "Control dimencional","fecha de ingreso","Certificado END"])

            self.table_widget.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)  # Hace que las columnas se estiren

            self.table_widget.cellClicked.connect(self.cargar_datos_fila or self.fila_seleccionada)

            #QTableWidget permita la selección de filas
            self.table_widget.setSelectionBehavior(QTableWidget.SelectRows)
            self.table_widget.setSelectionMode(QTableWidget.SingleSelection)
            self.table_widget.itemSelectionChanged.connect(self.verificar_seleccion)
            self.cargar_datos()


            #label que dice si el pdf esta cargado y subido
            self.label_subida_exitosa = QLabel('', self)
            label_x = self.btn_subir_pdf.x()
            label_y = self.btn_subir_pdf.y() - 30  # 30 píxeles por encima del botón
            self.label_subida_exitosa.setGeometry(label_x, label_y, 200, 25)

            self.timer_ocultar_mensaje = QTimer(self)
            self.timer_ocultar_mensaje.timeout.connect(self.ocultarMensaje)

            # Conectar señales a funciones
            self.btnagregar.clicked.connect(self.guardar_datos)
            self.btn_modificar.clicked.connect(self.modificar_datos)
            self.btn_actualizar.clicked.connect(self.cargar_datos)
            self.btn_eliminar.clicked.connect(self.eliminar_datos)
            self.btn_subir_pdf.clicked.connect(self.subir_pdf_firebase)
            #QR generator
            self.btn_generar_qr = QPushButton('Generar', self)
            self.btn_generar_qr.setIcon(QIcon("img/qr-code.png"))
            self.btn_generar_qr.clicked.connect(self.generar_qr)

            #barra de busqueda

            self.search_bar = QLineEdit(self)
            self.search_bar.setPlaceholderText("Buscar...")
            self.search_bar.textChanged.connect(self.filter_table)

            self.filter_options = QComboBox(self)
            self.filter_options.addItems(["Nombre herramienta", "CD","Plano", "Fecha"])

            search_layout.addWidget(self.search_bar)
            search_layout.addWidget(self.filter_options)

            # Agregar widgets al diseño
            layout.addLayout(titulo_layout, 0, 0, 1, 5)


            layout.addWidget(label_nherramienta, 1, 0)
            layout.addWidget(self.nherramienta_input, 1, 1)

            layout.addWidget(label_plano, 2, 0)
            layout.addWidget(self.plano_input, 2, 1)

            layout.addWidget(label_end, 1, 2)
            layout.addWidget(self.nombre_pdf_input, 1, 3)
            layout.addWidget(self.btn_subir_pdf, 1, 4)

            layout.addWidget(label_certificado, 2, 2)
            layout.addWidget(self.certificado_despacho_input, 2, 3)
            layout.addWidget(entrega_lbl, 3, 2)
            layout.addWidget(self.date_edit, 3, 3)

            layout.addWidget(label_mc, 3, 0)
            layout.addWidget(self.mc_input, 3, 1)
            layout.addWidget(buttons_container, 4, 0, 1, -1)
            layout.addWidget(self.btn_generar_qr, 5, 4,1,2)
            layout.addLayout(buttons_update_clear_layout, 5, 0) 

            layout.addLayout(search_layout, 5, 1, 1, 3)
            # Asumiendo que quieres que esté en la fila 4
            layout.setRowStretch(6, 2)  # Añade estiramiento a la fila anterior a los botones para empujar los botones hacia abajo y centrarlos verticalmente.
            layout.setRowStretch(5, 1)  # Añade estiramiento a la fila después de los botones para mantener el equilibrio.

            # Para centrar el contenedor de botones horizontalmente en la cuadrícula
            layout.setColumnStretch(0, 1)  # Añade estiramiento a la columna antes del contenedor de botones
            layout.setColumnStretch(1, 1)

            # Agregar el QTableWidget al layout
            layout.addWidget(self.table_widget, 6, 0, 1, 5)  # Ajusta los números de fila y columna según sea necesario

        def limpiar_todo(self):
            # Llamar a la función que borra los contenidos de los campos de entrada
            self.limpiar_campos()

            # Deseleccionar cualquier selección en la tabla
            self.table_widget.clearSelection()
        def obtener_clave_firebase_de_fila(self, fila):
            item = self.table_widget.item(fila, 0)  # Puedes usar cualquier columna aquí
            if item:
                clave_firebase = item.data(Qt.UserRole)
                print(f"Clave obtenida para fila {fila}: {clave_firebase}")  # Imprimir la clave obtenida
                return item.data(Qt.UserRole)
            return None

        def verificar_seleccion(self):
            # Verifica si hay una fila seleccionada y muestra/oculta el botón según corresponda
            if self.table_widget.selectionModel().hasSelection():
                self.btn_generar_qr.show()
            else:
                self.btn_generar_qr.hide()
        def fila_seleccionada(self, row, column):
            # Mostrar el botón cuando se selecciona una fila
            self.btn_generar_qr.show()
        def filter_table(self):
            search_text = self.search_bar.text().lower()
            filter_option = self.filter_options.currentText()  # Obtiene la opción de filtro seleccionada

            # Mapeo de opciones a columnas del QTableWidget
            column_map = {
                "Nombre herramienta": 0,  # Asume que "Plano" está en la columna 0
                "MC": 3,
                "Plano": 1,# Asume que "Certificado" está en la columna 1
                "Fecha": 4
            }

            column_to_filter = column_map.get(filter_option, 0)  # Por defecto, filtra en la columna 0

            for row in range(self.table_widget.rowCount()):
                item = self.table_widget.item(row, column_to_filter)
                if item and search_text in item.text().lower():
                    self.table_widget.setRowHidden(row, False)
                else:
                    self.table_widget.setRowHidden(row, True)
        def deseleccionar_y_borrar(self):
            # Deseleccionar cualquier selección en la tabla
            self.table_widget.clearSelection()

            # Llamar a la función que borra los contenidos de los labels
            self.limpiar_campos()
        def get_fecha(self):
            # Obtener la fecha del QDateEdit
            fecha = self.date_edit.date()
            return fecha.toString("dd-MM-yyyy")
        def abrir_pdf(self, row, column):
            if column == 5:
                nombre_pdf = self.table_widget.item(row, column).text()
                pdfs = db.child("herramientas").child("certificados").get()
                for pdf in pdfs.each():
                    if pdf.val()['nombre_archivo'] == nombre_pdf:
                        pdf_url = pdf.val()['url']
                        webbrowser.open(pdf_url)
                        break

        def subir_pdf_firebase(self):
            options = QFileDialog.Options()
            options |= QFileDialog.DontUseNativeDialog
            file_dialog = QFileDialog()
            file_dialog.setOptions(options)
            file_dialog.setNameFilter("Archivos PDF (*.pdf)")
            file_dialog.setDefaultSuffix("pdf")

            file_path, _ = QFileDialog.getOpenFileName(self, "Seleccionar PDF", "", "Archivos PDF (*.pdf)")
            if file_path:
                self.ruta_pdf_temporal = file_path
                self.nombre_pdf_temporal = self.nombre_pdf_input.text()# Usar el texto del QLineEdit como nombre del PDF
                print(f"Ruta temporal del PDF: {self.ruta_pdf_temporal}")
                print(f"Nombre temporal del PDF: {self.nombre_pdf_temporal}")

                label_x = self.btn_subir_pdf.x() - 30
                label_y = self.btn_subir_pdf.y() - 15  # 30 píxeles por encima del botón
                self.label_subida_exitosa.setGeometry(label_x, label_y, 200, 25)
                self.label_subida_exitosa.setText( os.path.basename(file_path) + 'cargado')
                self.label_subida_exitosa.show()
                self.timer_ocultar_mensaje.start(3000)

                if not self.nombre_pdf_temporal:
                    QMessageBox.information(self, "Error", "Por favor, ingrese un nombre para el PDF.")

        def ocultarMensaje(self):
            # Crear animación para desvanecer el mensaje
            self.animacion = QPropertyAnimation(self.label_subida_exitosa, b"opacity")
            self.animacion.setDuration(1000)  # Duración de la animación en ms
            self.animacion.setStartValue(1)  # Opacidad inicial (1 = totalmente visible)
            self.animacion.setEndValue(0)  # Opacidad final (0 = invisible)
            self.animacion.setEasingCurve(QEasingCurve.InOutQuad)
            self.animacion.start()
            self.label_subida_exitosa.clear()
            self.timer_ocultar_mensaje.stop()

            # Detener el temporizador
        def generar_qr(self):
            selected = self.table_widget.currentRow()
            if selected >= 0:
                nombre_pdf = self.table_widget.item(selected, 5).text()
                certificados = db.child("herramientas").child("certificados").get()
                for certificado in certificados.each():
                    if certificado.val()['nombre_archivo'] == nombre_pdf:
                        pdf_url = certificado.val()['url']

                        # Generar el código QR
                        qr = qrcode.QRCode(
                            version=1,
                            error_correction=qrcode.constants.ERROR_CORRECT_L,
                            box_size=10,
                            border=4,
                        )
                        qr.add_data(pdf_url)
                        qr.make(fit=True)
                        img = qr.make_image(fill_color="black", back_color="white")

                        # Mostrar el código QR en una nueva ventana o como prefieras
                        img.show()
                        break
                else:
                    QMessageBox.information(self, "Error", "No se encontró el PDF asociado.")
            else:
                QMessageBox.information(self, "Error", "Por favor, seleccione una fila primero.")
        def cargar_datos_fila(self, row, column):
                # Suponiendo que el orden de las columnas en QTableWidget es el mismo que el orden de los campos de entrada
            self.nherramienta_input.setText(self.table_widget.item(row, 0).text())
            self.plano_input.setText(self.table_widget.item(row, 1).text())
            self.certificado_despacho_input.setText(self.table_widget.item(row, 2).text())
            self.mc_input.setText(self.table_widget.item(row, 3).text())

                # Para el QDateEdit, necesitas convertir el texto a una fecha
            fecha_str = self.table_widget.item(row, 4).text()
            fecha = QDate.fromString(fecha_str, "dd-MM-yyyy")
            if fecha.isValid():
                self.date_edit.setDate(fecha)

                # Suponiendo que la columna 5 tiene el nombre del PDF
            self.nombre_pdf_input.setText(self.table_widget.item(row, 5).text())
        def guardar_datos(self):
            nombre_herramienta = self.nherramienta_input.text()
            plano = self.plano_input.text()
            certificado = self.certificado_despacho_input.text()
            END = self.nombre_pdf_input.text()  # Corregido para usar .text()
            mc = self.mc_input.text()
            fecha_seleccionada = self.get_fecha()

            # Validación: Asegurarse de que el campo del certificado END no esté vacío
            if not self.nombre_pdf_input.text().strip():
                QMessageBox.warning(self, "Advertencia", "Por favor, ingrese el nombre del Certificado END.")
                return
            # Guardar los datos de la herramienta
            datos_herramienta = {
                "nombre_herramienta": nombre_herramienta,
                "plano": plano,
                "certificado": certificado,
                "C_END": END,
                "mc": mc,
                "fecha": fecha_seleccionada
            }
            db.child("herramientas").child("lista_herramientas").push(datos_herramienta)

            # Si hay un PDF seleccionado, subirlo y guardar en "certificados"
            if self.ruta_pdf_temporal:
                ruta_en_storage = f"pdf/{self.nombre_pdf_temporal}.pdf"
                print(f"Ruta de almacenamiento en Firebase: {ruta_en_storage}")
                firebase_storage.child(ruta_en_storage).put(self.ruta_pdf_temporal)
                pdf_url = firebase_storage.child(ruta_en_storage).get_url(None)

                datos_certificado = {
                    "nombre_archivo": self.nombre_pdf_temporal,
                    "url": pdf_url}
                db.child("herramientas").child("certificados").push(datos_certificado)

                nueva_fila = self.table_widget.rowCount()
                self.table_widget.insertRow(nueva_fila)

                self.table_widget.setItem(nueva_fila, 0, QTableWidgetItem(nombre_herramienta))
                self.table_widget.setItem(nueva_fila, 1, QTableWidgetItem(plano))
                self.table_widget.setItem(nueva_fila, 2, QTableWidgetItem(certificado))
                self.table_widget.setItem(nueva_fila, 3, QTableWidgetItem(mc))
                self.table_widget.setItem(nueva_fila, 4, QTableWidgetItem(fecha_seleccionada))
                self.table_widget.setItem(nueva_fila, 5, QTableWidgetItem(self.nombre_pdf_temporal))

                # Resetear las variables temporales del PDF
                self.ruta_pdf_temporal = None
                self.nombre_pdf_temporal = None

                # Limpiar campos y recargar datos
            self.limpiar_campos()
            self.cargar_datos()

        def limpiar_campos(self):
            self.nherramienta_input.clear()
            self.plano_input.clear()
            self.certificado_despacho_input.clear()  # Asegúrate de que esto no tenga paréntesis adicionales
            self.mc_input.clear()
            self.date_edit.setDate(QDate.currentDate())
            if hasattr(self, 'nombre_pdf_input'):
                self.nombre_pdf_input.clear()  # Solo si existe este campo en tu clase

        def subir_actualizar_pdf(self, clave_firebase, nombre_pdf):
            # Subir el nuevo PDF a Firebase Storage
            ruta_en_storage = f"pdf/{self.nombre_pdf_temporal}.pdf"
            firebase_storage.child(ruta_en_storage).put(self.ruta_pdf_temporal)
            nueva_url_pdf = firebase_storage.child(ruta_en_storage).get_url(None)

            certificados = db.child("herramientas").child("certificados").get()
            clave_certificado = None
            for certificado in certificados.each():
                # Verificar si 'nombre_archivo' existe en el certificado
                if certificado.val().get('nombre_archivo') == nombre_pdf:
                    clave_certificado = certificado.key()
                    break

            if clave_certificado:
                # Actualizar la base de datos con el nuevo nombre y la nueva URL del PDF
                db.child("herramientas").child("certificados").child(clave_firebase).update({
                    "nombre_archivo": self.nombre_pdf_temporal,
                    "url": nueva_url_pdf
                })
            else:
                db.child("herramientas").child("certificados").push({
                    "nombre_archivo": nombre_pdf,
                    "url": nueva_url_pdf
                })

            # Resetear la ruta PDF temporal
            self.ruta_pdf_temporal = None
            return self.nombre_pdf_temporal  # Devolver el nuevo nombre del PDF para actualizarlo en la tabla
        def actualizar_tabla(self, fila, datos):
            # Actualiza la fila en la tabla
            self.table_widget.item(fila, 0).setText(datos["nombre_herramienta"])
            self.table_widget.item(fila, 1).setText(datos["plano"])
            self.table_widget.item(fila, 2).setText(datos["certificado"])
            self.table_widget.item(fila, 3).setText(datos["mc"])
            self.table_widget.item(fila, 4).setText(datos["fecha"])
            if "C_end" in datos:
                self.table_widget.item(fila, 5).setText(datos["C_end"])
        def modificar_datos(self):
            selected = self.table_widget.currentRow()
            if selected >= 0:
                clave_firebase = self.obtener_clave_firebase_de_fila(selected)
                print(f"Clave de Firebase seleccionada: {clave_firebase}")  # Imprimir la clave obtenida
                if clave_firebase:
                    # Obtén los datos actualizados de los campos de entrada
                    nombre_herramienta_actualizado = self.nherramienta_input.text()
                    plano_actualizado = self.plano_input.text()
                    CertificadoDactualizado = self.certificado_despacho_input.text()
                    mcactualizado = self.mc_input.text()
                    fechaactualizada = self.date_edit.date().toString("dd-MM-yyyy")



                    clave_firebase = self.obtener_clave_firebase_de_fila(selected)
                    print(clave_firebase)
                    # Actualiza los datos en Firebase
                    datos_actualizados = {"nombre_herramienta": nombre_herramienta_actualizado,
                                          "plano": plano_actualizado,
                                          "certificado": CertificadoDactualizado,
                                          "fecha": fechaactualizada,
                                          "mc": mcactualizado,
                                          "plano":plano_actualizado
                                          }
                    nombre_pdf = self.nombre_pdf_temporal if self.ruta_pdf_temporal else self.table_widget.item(
                        selected, 5).text()

                    if nombre_pdf:
                        self.subir_actualizar_pdf(clave_firebase, nombre_pdf)

                    if self.ruta_pdf_temporal:
                        nombre_pdf_actualizado = self.subir_actualizar_pdf(clave_firebase)
                        datos_actualizados["C_end"] = nombre_pdf_actualizado

                    db.child("herramientas").child("lista_herramientas").child(clave_firebase).update(datos_actualizados)

                    self.actualizar_tabla(selected, datos_actualizados)
                    QMessageBox.information(self, "Actualización", "Datos actualizados con éxito.")



                else:
                    QMessageBox.information(self, "Error", "No se pudo obtener la clave de Firebase.")

            else:
                QMessageBox.information(self, "Error", "Por favor, seleccione una fila para actualizar.")

        def eliminar_pdf_firebase(self, nombre_pdf):
            ruta_pdf = f"pdf/{nombre_pdf}.pdf"
            try:
                firebase_storage.child(ruta_pdf).delete(ruta_pdf,None)
            except Exception as e:
                print(f"Error al eliminar el archivo PDF: {e}")
        def eliminar_datos(self):
            selected = self.table_widget.currentRow()
            if selected >= 0:
                clave_herramienta = self.obtener_clave_firebase_de_fila(selected)
                nombre_pdf = self.table_widget.item(selected,5).text()
                respuesta = QMessageBox.question(self, "Eliminar", "¿Está seguro de que desea eliminar este elemento?",
                                                 QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
                if respuesta == QMessageBox.Yes:
                    clave_herramienta = self.obtener_clave_firebase_de_fila(selected)
                    nombre_pdf = self.table_widget.item(selected, 5).text()
                  # Asumiendo que el nombre del PDF está en la columna 5
                    if clave_herramienta and nombre_pdf:

                        self.eliminar_certificado_relacionado(nombre_pdf)

                    # Eliminar la herramienta de la base de datos
                        db.child("herramientas").child("lista_herramientas").child(clave_herramienta).remove()

                    # Eliminar la fila de la tabla
                        self.table_widget.removeRow(selected)

                        QMessageBox.information(self, "Éxito", "Herramienta y PDF asociado eliminados correctamente.")

                        self.limpiar_campos()


            else:
                QMessageBox.warning(self, "Error", "Por favor, seleccione una fila para eliminar.")

        def eliminar_certificado_relacionado(self, nombre_pdf):
            certificados = db.child("herramientas").child("certificados").get()
            print(f"Nombre del PDF a eliminar: {nombre_pdf}")
            for certificado in certificados.each():
                if certificado.val().get("nombre_archivo") == nombre_pdf:
                    try:
                        ruta_pdf = f"pdf/{nombre_pdf}.pdf"
                        print(f"Ruta del PDF a eliminar: {ruta_pdf}")
                        firebase_storage.child(ruta_pdf).delete(ruta_pdf,token= None)
                        print(f"Archivo PDF eliminado: {ruta_pdf}")

                    except Exception as e:
                        print(f"Error al eliminar el archivo PDF: {e}")
                    # Eliminar la entrada del certificado en la base de datos
                    db.child("herramientas").child("certificados").child(certificado.key()).remove()
                    break

        def cargar_datos(self):

            self.table_widget.setRowCount(0)
            herramientas = db.child("herramientas").child("lista_herramientas").get()
            certificados = db.child("herramientas").child("certificados").get()
            if herramientas.val():
                herramientas_lista = [herramienta.val() for herramienta in herramientas.each()]
                clave_herramientas = [herramienta.key() for herramienta in herramientas.each()]

                # Ordenar los datos por fecha (Asegúrate de que el formato de fecha aquí coincida con el formato usado en tus datos)
                herramientas_lista.sort(key=lambda x: datetime.strptime(x['fecha'], "%d-%m-%Y"), reverse=True)

                self.table_widget.setRowCount(len(herramientas_lista))
                for index, herramienta in enumerate(herramientas_lista):
                    key = clave_herramientas[index]  # Asumiendo que el orden de las claves no cambió
                    self.table_widget.setItem(index, 0, QTableWidgetItem(herramienta['nombre_herramienta']))
                    self.table_widget.setItem(index, 1, QTableWidgetItem(herramienta['plano']))
                    self.table_widget.setItem(index, 2, QTableWidgetItem(herramienta['certificado']))
                    self.table_widget.setItem(index, 3, QTableWidgetItem(herramienta['mc']))
                    self.table_widget.setItem(index, 4, QTableWidgetItem(herramienta['fecha']))
                    # Busca el nombre del PDF correspondiente en los certificados
                    nombre_pdf = ""
                    if certificados.val():
                        for certificado in certificados.each():
                            if certificado.val().get("nombre_archivo") == herramienta.get("C_END"):
                                nombre_pdf = certificado.val().get("nombre_archivo", "")
                                break
                    self.table_widget.setItem(index, 5, QTableWidgetItem(nombre_pdf))

                    for col in range(self.table_widget.columnCount()):
                        item = self.table_widget.item(index, col)
                        if item is not None:
                            item.setData(Qt.UserRole, key)
                            print(f"Fila {index}, Columna {col}, Clave Firebase: {key}")  # Imprimir la clave
            else:
                QMessageBox.information(self, "Información", "No hay datos en Firebase.")

        # Cierre de ventana
        def closeEvent(self, event):
            Cuadro = QMessageBox.warning(self, "CERRAR", "¿Está seguro de cerrar la ventana?", QMessageBox.Yes | QMessageBox.No,
                                         QMessageBox.Yes)
            if Cuadro == QMessageBox.Yes:
                event.accept()
            elif Cuadro == QMessageBox.No:
                 event.ignore()


if __name__ == "__main__":
        app = QApplication(sys.argv)
        window = Herramientas()
        window.show()
        sys.exit(app.exec_())