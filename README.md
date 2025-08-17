# GossipAI Backend

Backend API для приложения анализа эмоций и коммуникации GossipAI.

## Технологии

- **FastAPI** - веб-фреймворк для Python
- **Supabase** - база данных PostgreSQL и аутентификация
- **Google Vertex AI** - ИИ-модели (Gemini 2.5 Pro)
- **Google Cloud Vision API** - OCR для изображений
- **Google Speech-to-Text** - транскрипция аудио

## Деплой

Этот проект настроен для деплоя на Railway.

### Переменные окружения

Создайте файл `.env` или добавьте переменные в Railway:

```env
SUPABASE_URL=your_supabase_url
SUPABASE_ANON_KEY=your_supabase_anon_key
SUPABASE_SERVICE_ROLE_KEY=your_service_role_key
BACKEND_CORS_ORIGINS=["https://your-frontend-url.vercel.app"]
GOOGLE_APPLICATION_CREDENTIALS=path/to/service-account-key.json
VERTEX_AI_PROJECT=your_project_id
VERTEX_AI_LOCATION=us-central1
```

## API Endpoints

- `GET /` - Информация об API
- `GET /docs` - Swagger документация
- `POST /api/v1/auth/register` - Регистрация
- `POST /api/v1/auth/login` - Вход
- `POST /api/v1/analysis/text` - Анализ текста
- `POST /api/v1/analysis/upload` - Анализ файлов
- `GET /api/v1/presets/` - Получение пресетов
