# admin_exibition

## Клонирование репозитория
Скопируйте репозиторий из GitHub:
git clone https://github.com/PokarPetr/admin_exhibition.git
cd admin_exhibition

## Установка
Создайте виртуальное окружение:
python -m venv venv

Активируйте виртуальное окружение:
Windows:
venv\Scripts\activate
MacOS/Linux:
source venv/bin/activate

Установите зависимости:
pip install -r requirements.txt

## Запуск сервура
Для запуска сервера:
uvicorn app:app --reload

## Документация
После запуска приложения, документация в формате Swagger будет доступна по адресу:
http://127.0.0.1:8000/docs
