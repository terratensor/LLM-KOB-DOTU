# LLM-KOB-DOTU
Добавление LLM с книгами на svodd.ru


30.03.24  ver 0.1

На данный момент голая модель не обученая v1.0-pro (30к токенов), нет пока возможности через апи добавить 1.5-pro с количеством 1млн токенов, как только такая возможность появится, я сразу добавлю.
Для установки локально надо в консоли python прописать команду:

pip install -U -q google-generativeai

Так же требуется впн с локацией в сша.  Я использую PaladinVPN на виртуалке, можете на основной машине, это нужно что бы запустить код на локальной машине иначе будет выдавать ошибку и модель вам отвечать не будет

Для тестирования более новой модели на 1млн токенов, вам нужно перейти по этой ссылке -> https://aistudio.google.com/ включив предварительно впн(можно в браузере использовать VeePN или любой другой который поддерживает локацию сшп).


31.03.24  ver 0.2

Добавил возможность загружать файлы в формате .doc .pdf .docx, пока нет возможности загружать слишком большие файлы, так как есть лимит апи по количеству токенов

Добавил чат окно

Доюавил окно для ввода инструкции

Для получения API ключа перейдите по ссылку:

https://aistudio.google.com/app/apikey


31.03.24   ver 0.3

Добавил возможность сохранять историю переписки

Добавил возможность сохранять Итог для ИИ( Она создает итог согласно тому что происходило в чате и какую роль она получила)


Добавил возможность загружать Итог для ИИ( Что бы модель могла быстро вспомнить о чем шла речь)

Убрал (на сколько это возможно) цензуру


21.04.24 ver 0.4
Обновил LLM до версии 1.5, более корректно загружает файлы и извлекает информацию
