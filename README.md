<a name="readme-top"></a>
<h3 align="center">Security Tracking Bot for Telegram</h3>

<div align="center">
<img src="https://www.python.org/static/community_logos/python-powered-w.svg" hspace="20" align="center" height="100"> 
<img src="https://opencv1.b-cdn.net/wp-content/uploads/2020/07/OpenCV_logo_no_text-1.svg" hspace="20" align="center"  height="100">
<img src="https://docs.aiogram.dev/en/dev-3.x/_static/logo.png" hspace="20"  alt="Aiogram" align="center"  height="100"><br><br>
</div><br><br>



<h2 align="center"> Телеграм-бот для распознавания и оповещения об объектах в кадре.</h2><br><br>



### О проекте
Проект по распознаванию объектов на видео с использованием Python и OpenCV, создан для удобного оповещения 
о новых объектах посредством Telegram. Инструментом распознавания объектов служит легковесная модель SSD MobileNet v3
в паре с COCO-dataset, запущенная стандартными средствами библиотеки OpenCV (cv2.dnn.DetectionModel).
Роль пользовательского интерфейса выполняет библиотека Aiogram v3. 

<p align="right">(<a href="#readme-top">back to top</a>)</p>
  


### Создано при помощи

* ![Python 3.10](https://img.shields.io/badge/python-3.10-blue.svg)
* ![OpenCV 4.8.1](https://img.shields.io/badge/opencv--python-4.8.1-python.svg)
* ![Aiogram 3.1.1](https://img.shields.io/badge/aiogram-3.1.1-python)

<p align="right">(<a href="#readme-top">back to top</a>)</p>



### Установка

#### Ручная установка (для локального использования)

1. Создайте бота и получите токен в Telegram при помощи ` https://t.me/BotFather `
2. Скопируйте репозиторий
   ```sh
   git clone https://github.com/Cntrfct/security_tracking_tg_bot.git
   ``` 
3. Установите необходимые библиотеки `pip install -r requirements.txt`
4. Переименуйте файл `.env.example` в `.env` и отредактируйте его
5. Запустите `python main.py`


#### Установка через docker-compose(на сервере)

1. Создайте бота и получите токен в Telegram при помощи ` https://t.me/BotFather `
2. Скопируйте репозиторий(ветку server)
   ```sh
   git clone --branch=server https://github.com/Cntrfct/security_tracking_tg_bot.git
   ``` 
3. Переименуйте файл `.env.example` в `.env` и отредактируйте его
4. Создайте и разверните контейнер `docker compose up -d --build`
   

<p align="right">(<a href="#readme-top">back to top</a>)</p>



### Применение
Бот отлично справляется с функцией распознавания. В качестве источника нужно ввести ссылку любого действующего 
видеопотока. Автоматически бот присылает уведомления с кадром и описанием объекта каждые 10 секунд, при условии, что в кадре обнаружен какой-то объект.
Управление осуществляется командами, через кнопку "Меню".
- /start - Начало работы бота. Запуск бота и вывод приветственного сообщения.
- /stream - Запуск видеопотока. На этом этапе нужно ввести корректную ссылку на видеопоток, иначе будет получено сообщение об ошибке.
- /getframe - Получить кадр. Если видеопоток был запущен удачно, при помощи данной команды можно получить кадр в любой момент.
- /stop - Остановка видеопотока. Команда останавливает текущий видеопоток.

<p align="right">(<a href="#readme-top">back to top</a>)</p>



### Контакты
https://t.me/C0NTRAfact

<p align="right">(<a href="#readme-top">back to top</a>)</p>



### Пример
https://t.me/sectrack_bot

<p align="right">(<a href="#readme-top">back to top</a>)</p>



