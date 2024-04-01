import sys
from PyQt5.QtWidgets import (QApplication, QMainWindow, QTextEdit, QLineEdit, QPushButton,
                             QVBoxLayout, QWidget, QFileDialog, QHBoxLayout, QGroupBox)

import google.generativeai as genai
from PyPDF2 import PdfReader  
import docx  
import win32com.client  

# Апи ключ
API_KEY = 'API ключ сюда вводить'
generation_config = {
    "temperature": 0.9,
    "top_p": 1,
    "top_k": 1,
    "max_output_tokens": 4096,
}

safety_settings = [
    {
        "category": "HARM_CATEGORY_HARASSMENT",
        "threshold": "BLOCK_NONE",
    },
    {
        "category": "HARM_CATEGORY_HATE_SPEECH",
        "threshold": "BLOCK_NONE",
    },
    {
        "category": "HARM_CATEGORY_SEXUALLY_EXPLICIT",
        "threshold": "BLOCK_NONE",
    },
    {
        "category": "HARM_CATEGORY_DANGEROUS_CONTENT",
        "threshold": "BLOCK_NONE",
    },
]

#Инициализация

genai.configure(api_key=API_KEY)

gemini = genai.GenerativeModel(model_name="gemini-1.0-pro",
                               generation_config=generation_config,
                               safety_settings=safety_settings)
chat = gemini.start_chat()


class ChatWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.chat_history = []
        self.initUI()

    def set_prompt(self):
        try:
            prompt = self.prompt_field.text()
            instruction = f"Отныне {prompt}. Пожалуйста, отвечай на вопросы и веди себя в соответствии с этой ролью." #Инструкция для ИИ
            chat.send_message(instruction)
            self.prompt_field.clear()
        except Exception as e:
            self.chat_display.append(f"Ошибка при установке подсказки: {e}\n")
          
#Загрузка файла суммирования в .txt формате
    def load_summary_file(self):
        options = QFileDialog.Options()
        file_path, _ = QFileDialog.getOpenFileName(self, "Загрузить файл суммирования", "",
                                                   "Text Files (*.txt)", options=options)
        if file_path:
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    summary_text = f.read()
                chat.send_message(summary_text)  # Send summary text to the model
            except Exception as e:
                self.chat_display.append(f"Ошибка при загрузке файла суммирования: {e}\n")
              
#Сохранение истории
    def save_history(self):
        try:
            options = QFileDialog.Options()
            file_path, _ = QFileDialog.getSaveFileName(self, "Сохранить историю", "",
                                                       "Text Files (*.txt)", options=options)
            if file_path:
                with open(file_path, 'w', encoding='utf-8') as f:
                    for sender, message in self.chat_history:
                        f.write(f"{sender}: {message}\n")
        except Exception as e:
            self.chat_display.append(f"Ошибка при сохранении истории: {e}\n")
          
#Сохранение суммирования, суммирует информацию которую получил в чате и сохраняет в .txt формате
    def summarize_knowledge(self):
        try:
            summary_prompt = "Пожалуйста, суммируй полученные знания из предыдущего разговора, что бы после их загрузки ты смог вспомнить о чем шла речь"
            response = chat.send_message(summary_prompt)

            options = QFileDialog.Options()
            file_path, _ = QFileDialog.getSaveFileName(self, "Сохранить знания", "",
                                                       "Text Files (*.txt)", options=options)
            if file_path:
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(response.text)
        except Exception as e:
            self.chat_display.append(f"Ошибка при суммировании знаний: {e}\n")
#UI
    def initUI(self):
        self.chat_display = QTextEdit(self)
        self.chat_display.setReadOnly(True)

        self.input_field = QLineEdit(self)
        # button_layout = QHBoxLayout()

        ai_group = QGroupBox("Работа с ИИ", self)
        ai_group_layout = QVBoxLayout()

        # Ввод и вывод 
        self.prompt_field = QLineEdit(self)
        prompt_button = QPushButton('Инструкция ИИ', self)
        prompt_button.clicked.connect(self.set_prompt)
        ai_group_layout.addWidget(self.prompt_field)
        ai_group_layout.addWidget(prompt_button)

        # Итог
        summarize_button = QPushButton('Подытожить', self)
        summarize_button.clicked.connect(self.summarize_knowledge)
        ai_group_layout.addWidget(summarize_button)

        #Загрузка Суммирования
        load_summary_button = QPushButton('Загрузить файл суммирования', self)
        load_summary_button.clicked.connect(self.load_summary_file)
        ai_group_layout.addWidget(load_summary_button)

        ai_group.setLayout(ai_group_layout)

        button_layout = QHBoxLayout()

        send_button = QPushButton('Отправить', self)
        send_button.clicked.connect(self.send_message)
        button_layout.addWidget(send_button)

        load_file_button = QPushButton('Загрузить файл', self)
        load_file_button.clicked.connect(self.load_file)
        button_layout.addWidget(load_file_button)

        save_history_button = QPushButton('Сохранить историю', self)
        save_history_button.clicked.connect(self.save_history)
        button_layout.addWidget(save_history_button)

        #Слои
        layout = QVBoxLayout()
        layout.addWidget(ai_group)  # Add AI group at the top left
        layout.addWidget(self.chat_display)
        layout.addWidget(self.input_field)
        layout.addLayout(button_layout)

        central_widget = QWidget()
        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)

        self.setGeometry(300, 300, 600, 400)
        self.setWindowTitle('Мини-чат с языковой моделью')
        self.show()
#Отправка сообщения
    def send_message(self):
        user_input = self.input_field.text()
        self.chat_display.append("Вы: " + user_input + "\n")
        self.input_field.clear()

        if user_input == "/sum":
            self.summarize_knowledge()
        else:
            #Отправка сообщения ИИ на user_input
            response = chat.send_message(user_input)

        # Ответ ИИ
        self.chat_display.append("Модель: " + response.text + "\n")
        # Сохранения истории чата
        self.chat_history.append(("Вы", user_input))
        self.chat_history.append(("Модель", response.text))
#Загрузка файлов .PDF .docx .doc
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


#Запуск
def main():
    try:
        app = QApplication(sys.argv)
        ex = ChatWindow()
        sys.exit(app.exec_())
    except Exception as e:
        print(f"Критическая ошибка: {e}")


if __name__ == '__main__':
    main()
