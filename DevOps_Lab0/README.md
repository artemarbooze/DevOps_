# Лабораторная работа 0 — свой сервис

## Что это

Небольшое веб-приложение «Заметки». Фронтенд отправляет новую заметку в Flask-бэкенд. Бэкенд записывает заметку в PostgreSQL и читает сохранённые заметки для отображения на странице.

## Состав проекта

- `frontend/` — веб-страница с формой и списком заметок;
- `backend/` — Flask-бэкенд с API (`GET` и `POST /api/notes`);
- `notes-db` — отдельный контейнер PostgreSQL, запускается командой `docker run`.

## Запуск

1. В терминале перейти в папку лабораторной:

   ```bash
   cd DevOps_Lab0
   ```

2. Запустить базу данных:

   ```bash
   docker run -d --name notes-db \
     -e POSTGRES_USER=notes -e POSTGRES_PASSWORD=notes -e POSTGRES_DB=notes \
     -p 5432:5432 -v notes-data:/var/lib/postgresql/data postgres:16-alpine
   ```

   При повторных запусках контейнер уже создан, достаточно `docker start notes-db`.

3. Установить зависимости бэкенда:

   ```bash
   python3 -m venv .venv
   .venv/bin/pip install -r backend/requirements.txt
   ```

4. Запустить бэкенд:

   ```bash
   .venv/bin/python backend/app.py
   ```

5. Открыть в браузере <http://localhost:8000>.
6. Ввести заметку, нажать «Добавить» и обновить страницу. Заметка останется в списке, так как она сохранена в PostgreSQL.

## Остановка

В окне терминала с бэкендом нажать `Ctrl + C`, затем остановить базу данных:

```bash
docker stop notes-db
```

Данные PostgreSQL сохраняются в Docker volume `notes-data`. Чтобы удалить и контейнер, и данные, выполнить:

```bash
docker rm -f notes-db
docker volume rm notes-data
```
