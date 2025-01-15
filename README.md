# Telegram-бот для расчёта нормы воды, калорий и трекинга активности (HealthBuddyAPI-TG-Bot)

## 📋 Описание проекта

Я разработал Telegram-бота, который помогает пользователям рассчитывать дневные нормы воды и калорий, а также отслеживать тренировки и питание. Бот реализует множество функций, включая настройку профиля, логирование активности и предоставление графического отчета о прогрессе. Все данные сохраняются даже при перезапуске сервера.

## 🛠 Реализованные функции

### 1. Настройка профиля пользователя
- **Команда `/set_profile`** запрашивает параметры пользователя:
  - Вес, рост, возраст.
  - Уровень активности (минуты в день).
  - Город (используется для определения температуры через OpenWeatherMap API).
  - Цель по калориям рассчитывается автоматически, но может быть задана вручную.

### 2. Расчёт норм воды и калорий
- **Норма воды** рассчитывается на основе:
  - Формулы: Вес × 30 мл/кг + 500 мл (на 30 минут активности) + до 1000 мл при жаре (> 25°C).
- **Норма калорий**:
  - Используется формула: `10 × Вес + 6.25 × Рост - 5 × Возраст + активность (200-400 ккал)`.

### 3. Логирование воды
- **Команда `/log_water <количество>`**:
  - Записывает количество выпитой воды и показывает остаток до выполнения дневной нормы.

### 4. Логирование еды
- **Команда `/log_food <название продукта>`**:
  - Бот использует OpenFoodFacts API для получения информации о калорийности продуктов.
  - Сохраняет данные о потреблённых калориях.

### 5. Логирование тренировок
- **Команда `/log_workout <тип тренировки> <время>`**:
  - Учитывает сожжённые калории и дополнительную норму воды, зависящую от типа тренировки.

### 6. Прогресс пользователя
- **Команда `/check_progress`**:
  - Показывает текущий прогресс по воде и калориям.
  - Дополнительно генерируется график прогресса, отправляемый пользователю.

### 7. Дополнительные возможности
- **Кнопки** для всех основных команд.
- **Сохранение состояния**: Данные сохраняются в файл, чтобы они были доступны даже после перезапуска сервера.
- **Графики**: Прогресс отображается визуально с помощью графиков.
- **Деплой**: Бот задеплоен на [Render.com](https://render.com).

---

## 📂 Структура проекта

1. **`api/`**
   - `api.py` — Работа с OpenWeatherMap и OpenFoodFacts API.
2. **`app/`**
   - `handlers.py` — Основная логика обработки команд.
   - `keyboards.py` — Определение кнопок.
   - `middleware.py` — Логирование всех сообщений.
   - `storage.py` — Сохранение и загрузка данных пользователей.
   - `utils.py` — Вспомогательные функции (расчёты и т.д.).
3. **`data/`**
   - `recommendations.py` — Список рекомендаций по еде и тренировкам.
   - `users_data.json` — Файл для хранения данных пользователей.
4. **`logs/`**
   - `bot.log` — Логи работы бота.
5. **`.env`**
   - Конфигурация токенов (BOT_TOKEN, WEATHER_TOKEN).
6. **`Dockerfile`**
   - Конфигурация для деплоя.
7. **`README.md`**
   - Описание проекта.
8. **`requirements.txt`**
   - Зависимости проекта.
9. **`bot.py`**
   - Точка входа для запуска бота.

---

## 📷 Примеры работы

### Скриншоты работы в Telegram:
1. **Настройка профиля**  
   Заполнение данных пользователя: вес, рост, возраст, активность и город.  
   ![Настройка профиля](https://github.com/user-attachments/assets/8395ee4f-81a8-4d76-b952-a8b2259852bb)

2. **Логирование воды**  
   Добавление количества выпитой воды с расчетом оставшейся нормы.  
   ![Логирование воды](https://github.com/user-attachments/assets/b6cac052-456a-4d92-aa11-673792d737d2)

3. **Логирование еды**  
   Добавление информации о съеденной пище и калорийности.  
   ![Логирование еды](https://github.com/user-attachments/assets/66c13035-ebbc-4d9f-8d2c-d2829ddda48d)

4. **Логирование тренировок**  
   Фиксация тренировки с расчетом сожженных калорий и дополнительной нормы воды.  
   ![Логирование тренировок](https://github.com/user-attachments/assets/e03aaf93-10a3-41f7-a976-228932e21476)

5. **Прогресс пользователя**  
   Просмотр прогресса по воде и калориям с расчетом оставшегося.  
   ![Прогресс пользователя](https://github.com/user-attachments/assets/9677a5fd-8a63-4da1-852b-45ca4916c42e)

6. **Графики прогресса**  
   Визуализация прогресса пользователя по воде и калориям в виде графиков.  
   ![Графики прогресса](https://github.com/user-attachments/assets/a28192b4-9491-4858-aab7-a2718316976e)

7. **Кнопки навигации**  
   Удобные кнопки для вызова всех основных функций бота.  
   ![Кнопки навигации](https://github.com/user-attachments/assets/18ef87d4-26d3-4485-848b-4570140178ea)

8. **Общий пример работы бота**  
   Демонстрация нескольких функций бота: настройки, логирования и прогресса.  
   ![Общий пример работы](https://github.com/user-attachments/assets/dad466b7-095c-456b-a4ae-142c3c95a569)






### Скриншоты успешного деплоя:
- Успешный деплой и логи (в отдельной файле):

![Деплой](https://github.com/user-attachments/assets/10c8a36e-ac42-4dbb-ae0f-138b3f927f36)
![Логи](https://github.com/user-attachments/assets/4a44aadb-f321-41be-93ce-b7dbb9477336)


---

## 🌐 Как запустить проект локально

1. **Клонируйте репозиторий:**
   ```bash
   git clone https://github.com/username/healthbuddyapi-tg-bot.git
   cd healthbuddyapi-tg-bot
   ```

2. **Установите зависимости:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Создайте файл `.env` и добавьте API-ключи:**
   ```env
   BOT_TOKEN=<ваш_токен>
   WEATHER_TOKEN=<ваш_ключ_погоды>
   ```

4. **Запустите бота:**
   ```bash
   python main.py
   ```

---

## 🌐 Как задеплоить на Render.com

1. **Создайте Dockerfile** (уже есть в проекте).
2. **Добавьте репозиторий на GitHub.**
3. **Свяжите с Render.com:**
   - Выберите "New Web Service".
   - Укажите Dockerfile и переменные окружения (BOT_TOKEN, WEATHER_TOKEN).
4. **Разверните приложение.**

---

## 🏆 Выполенные задачи

1. Реализован полный функционал из задания.
2. Добавлены графики для визуализации прогресса.
3. Реализован деплой на Render.com.
4. Удобные кнопки для всех основных команд.
5. Состояние сохраняется между перезапусками сервера.

