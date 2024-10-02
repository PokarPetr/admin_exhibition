# admin_exibition

## Клонирование репозитория
Скопируйте репозиторий из GitHub:
```bash
git clone https://github.com/PokarPetr/admin_exhibition.git
cd admin_exhibition
```

## Установка
Создайте виртуальное окружение:
```bash
python -m venv venv
```

Активируйте виртуальное окружение:

Windows:
```bash
venv\Scripts\activate
```
MacOS/Linux:
```bash
source venv/bin/activate
```

Установите зависимости:
```bash
pip install -r requirements.txt
```

## Запуск сервера
Для запуска сервера:
```bash
uvicorn app:app --reload
```

## Документация
После запуска приложения, документация в формате Swagger будет доступна по адресу:
http://127.0.0.1:8000/docs
