Лабораторная работа №4
Нигаматулина Дарина

СУБД: Microsoft SQL Server Express

Запуск:
```powershell
.\venv\Scripts\activate
python seed.py
uvicorn main:app --reload
```

API Документация:
Swagger UI: http://127.0.0.1:8000/docs
ReDoc: http://127.0.0.1:8000/redoc

Примеры cURL:
bash# Зарегистрированные пассажиры
curl http://127.0.0.1:8000/passengers/registered

Доступные рейсы
curl http://127.0.0.1:8000/flights/available

Создать пассажира
curl -X POST http://127.0.0.1:8000/passengers \
  -H "Content-Type: application/json" \
  -d '{
    "full_name": "Сидоров Петр",
    "passport_data": "EF123456",
    "contact_info": "sidorov@mail.ru",
    "status": "registered"
  }'
