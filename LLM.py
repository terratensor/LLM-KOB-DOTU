
import tkinter as tk
from tkinter import scrolledtext
import base64
import json

import google.generativeai as genai
# Апи ключ введите сюда свой ключ который получите вот тут https://aistudio.google.com/app/apikey
API_KEY = 'API_KEY'

model = 'gemini-1.0-pro'

# Инициализация

genai.configure(api_key=API_KEY)
gemini = genai.GenerativeModel(model_name=model)
chat = gemini.start_chat()

# Функции 

def send_message():
    user_input = entry_field.get()
    entry_field.delete(0, tk.END)

    # Добавить сообщение пользователя в чат
    chat_box.configure(state='normal')
    chat_box.insert(tk.END, "Вы: " + user_input + "\n")
    chat_box.configure(state='disabled')

    # Отправить сообщение модели и получить ответ
    response = chat.send_message(user_input)

    # Добавить ответ модели в чат
    chat_box.configure(state='normal')
    chat_box.insert(tk.END, "Модель: " + response.text + "\n")
    chat_box.configure(state='disabled')

    # Прокрутить чат вниз
    chat_box.yview(tk.END)
# Создание графического интерфейса (пока для удобства, можно будет под сайт переделать)

window = tk.Tk()
window.title("ДОТУ-КОБ-ЛЛМ")

# Стили 

font_style = ("Arial", 12)
bg_color = "#f0f0f0"
entry_bg = "#ffffff"

# Виджеты 

# Поле чата
chat_box = scrolledtext.ScrolledText(window, wrap=tk.WORD, font=font_style, bg=bg_color)
chat_box.pack(expand=True, fill='both', padx=10, pady=10)
chat_box.configure(state='disabled')

# Поле ввода
entry_field = tk.Entry(window, font=font_style, bg=entry_bg)
entry_field.pack(fill='x', padx=10, pady=5)
entry_field.bind("<Return>", lambda event: send_message())

# Кнопка отправки
send_button = tk.Button(window, text="Отправить", command=send_message)
send_button.pack(pady=5)

# Дополнительный промпт 

prompt_label = tk.Label(window, text="Вводный промпт:")
prompt_label.pack()

prompt_entry = tk.Entry(window, font=font_style, bg=entry_bg)
prompt_entry.pack(fill='x', padx=10, pady=5)
prompt_entry.insert(0, " ")  # Пример промпта

def set_prompt():
    prompt = prompt_entry.get()
    chat.send_message(prompt)  # Отправить промпт модели
    prompt_entry.delete(0, tk.END)  # Очистить поле промпта

prompt_button = tk.Button(window, text="Установить промпт", command=set_prompt)
prompt_button.pack(pady=5)

# Запуск 

window.mainloop()
