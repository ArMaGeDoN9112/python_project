# Эмоции.Текст

Благодаря нашей программе пользователь может транскрибировать аудио/видео с возможностью просмотра эмоционального окраса текста.

Кратко работу программы можно представить так:
загрузка файла -> преобразование в текст -> разбитие текста на кусочки -> анализ аудио-кусочков через нейросеть -> окрашивание кусочков текста в цвет соответствующий эмоции

Кратко про все файлы:

`analyze.py` - обработка входящего аудиопотока и преобразование его в отрезки из пяти слов с помощью библиотеки `vosk`. На каждый отрезок известно время начала произношения первого слова и конец последнего(пятого). Отрезки отправляются на сервер. А данные о начале и конца отрезка отправляются на обрезку в другую функцию.

`app.py` - "сервер" нашей программы. Здесь происходит обработка всех запросов.

С помощью определенных запросов можно: загрузить файл, начать анализ аудио/видео, зарендерить html страничку.

`encoder.pkl` и `scaler.pkl` - эти файлы содержат информацию о соотвествующих определенных python-объектах.

`fer.py` - скрипт с нейросетью, которая обрабатывает видео и показывает эмоции человека на данном видео.

Подробнее: на вход поступает видео, которое пользователь загрузил на сайте, далее видео обрабатывает нейросеть, которая поверх исходного видео накладывает прямоугольник вокруг лица, распознаваемого человека.

`haarcascade_frontalface_default.xml` - содержит информацию о конфигурации нейросети для распознавания лиц.

`model.keras` и `model.h5` - обученные модели с помощью машинного обучения.

`requirements.txt` - необходимые зависимости для работы программы.

`/templates/` - директория, в которой содержаться html-файлы.

`/static/` - директория, в которой содержатся файлы, необходимые для корректного отображения сайта.

`/audio/` - директория, в которую попадают временные файлы (отрезки аудио), который сразу же после обработки удаляются.

![Цветовая схема](цветовая_гамма.jpg)
