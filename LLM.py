import sys
from PyQt5.QtWidgets import (QApplication, QMainWindow, QTextEdit, QLineEdit, QPushButton,
                             QVBoxLayout, QWidget, QAction, QFileDialog)

import google.generativeai as genai 
from PyPDF2 import PdfReader  # Для чтения PDF
import docx  # Для чтения DOCX
import win32com.client  # Для DOC файлов

# Апи ключ
API_KEY = 'API_KEY'

model = 'gemini-1.0-pro'

#Инициализация 

genai.configure(api_key=API_KEY)
gemini = genai.GenerativeModel(model_name=model)
chat = gemini.start_chat()


class ChatWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()

    def set_prompt(self):
        prompt = self.prompt_field.text()

        # Инструкция
        instruction = f"Отныне ты {prompt}. Пожалуйста, отвечай на вопросы и веди себя в соответствии с этой ролью."

        chat.send_message(instruction)  # Отправка инструкции модели
        self.prompt_field.clear()  

    def initUI(self):
        self.chat_display = QTextEdit(self)
        self.chat_display.setReadOnly(True)

        self.input_field = QLineEdit(self)

        send_button = QPushButton('Отправить', self)
        send_button.clicked.connect(self.send_message)

        load_button = QPushButton('Загрузить файл', self)
        load_button.clicked.connect(self.load_file)

        self.prompt_field = QLineEdit(self)
        prompt_button = QPushButton('Инструкция ИИ', self)
        prompt_button.clicked.connect(self.set_prompt)

        layout = QVBoxLayout()
        layout.addWidget(self.chat_display)
        layout.addWidget(self.input_field)
        layout.addWidget(send_button)
        layout.addWidget(load_button)
        layout.addWidget(self.prompt_field)  # Add prompt field
        layout.addWidget(prompt_button)  # Add prompt button

        central_widget = QWidget()
        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)

        self.setGeometry(300, 300, 600, 400)
        self.setWindowTitle('Чат')
        self.show()

    def send_message(self):
        user_input = self.input_field.text()
        self.chat_display.append("Вы: " + user_input + "\n")
        self.input_field.clear()

        # Отправка и получение ответа
        response = chat.send_message(user_input)

        # Ответ модели в чате
        self.chat_display.append("Модель: " + response.text + "\n")

    def load_file(self):
        options = QFileDialog.Options()
        file_path, _ = QFileDialog.getOpenFileName(self, "Загрузить файл", "",
                                                   "All Files (*);;PDF Files (*.pdf);;Text Files (*.txt);;Docx Files (*.docx)",
                                                   options=options)
        if file_path:
            try:
                if file_path.endswith(".pdf"):
                    with open(file_path, 'rb') as f:
                        reader = PdfReader(f)
                        text = ""
                        for page in reader.pages:
                            text += page.extract_text()

                elif file_path.endswith(".docx"):
                    doc = docx.Document(file_path)
                    text = "\n".join([paragraph.text for paragraph in doc.paragraphs])

                elif file_path.endswith(".doc"):
                    word = win32com.client.Dispatch("Word.Application")
                    doc = word.Documents.Open(file_path)
                    text = doc.Content.Text
                    doc.Close()
                    word.Quit()
                else:
                    raise ValueError("Неподдерживаемый тип")

                chat.send_message(f"Загружено из файла: {file_path}")
                chat.send_message(text)  # Send text to the model

            except Exception as e:
                self.chat_display.append(f"Ошибка загрузки файла: {e}\n")


def main():
    app = QApplication(sys.argv)
    ex = ChatWindow()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
