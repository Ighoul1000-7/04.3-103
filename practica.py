from fastapi import FastAPI, Form
from textblob import TextBlob
from fastapi.responses import HTMLResponse
from translate import Translator

app = FastAPI()

html_form = """
<div>
    <form method="post" style='max-width: 600px;margin: 50px auto;background-color: #fff;padding: 20px;border-radius: 8px;box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);'>
        <input type="text" name="text" placeholder="Введите текст">
        <button type="submit">Анализировать</button>
    </form>
</div>
"""

# Функция перевода
def translate_text(text):
    translator = Translator(from_lang="ru", to_lang="en")
    translation = translator.translate(text)
    return translation

# Главная страница
@app.get("/", response_class=HTMLResponse)
async def read_form():
    return html_form

# Событие на нажатия кнопки
@app.post("/", response_class=HTMLResponse)
async def process_form(text: str = Form(...)):
    # Перевод текста
    translated_text = translate_text(text)
    blob = TextBlob(translated_text)

    # Анализ тональности текста
    sentiment_score = blob.sentiment.polarity

    # Определение тональности
    if sentiment_score > 0:
        sentiment = "позитивный"
    elif sentiment_score < 0:
        sentiment = "негативный"
    else:
        sentiment = "нейтральный"

    # Отображение результата
    result_html = f"""
    <p>Ваш текст: <strong>{text}</strong></p>
    <p>Тональность: <strong>{sentiment}</strong></p>
    <p>Оценка тональности: <strong>{sentiment_score}</strong></p>
    {html_form}
    """
    return result_html