# AGENTS.md

本文件提供給 AI agent / 協作者快速上手這個 LINE Bot 專案。改程式碼前請先讀這裡。

## 專案概要

一個用 **Django 4.1** 寫的 LINE Bot（私訊/群聊指令觸發功能：天氣、簽到、石頭、PTT 正妹圖、翻譯、匯率、新番、AI 對話等）。以 **Docker Compose** 本地部屬，資料庫用 **MySQL 8**，快取用 **Redis**。

## 關鍵指令（改完程式碼必看）

- `line_bot` container 已掛載本機專案到 `/home/app`（`volumes: .:/home/app`），所以**改 Python 程式碼存檔即 auto-reload 生效，不需 rebuild**。
- 只有「改 `requirements.txt` / `Dockerfile`（裝新套件）」才需要 `docker compose up -d --build`。
- 只改 `.env` / `docker-compose.yml` 用 `docker compose up -d`。
- 看 log：`docker compose logs -f line_bot`

## 啟動 / 停止

```bash
cp .env.example .env        # 首次：先填 LINE 金鑰與 MYSQL_ROOT_PASSWORD
docker compose up -d --build
docker compose logs -f line_bot
docker compose down         # 停止（資料保留在 volume）
```

`line_bot` 開機會自動 `migrate` 再跑 `runserver 0.0.0.0:8000`。

## 環境變數（.env，已 gitignore）

- **LINE_CHANNEL_ACCESS_TOKEN / LINE_CHANNEL_SECRET** — 必填（LINE Developers Console）
- **MYSQL_ROOT_PASSWORD / MYSQL_DATABASE** — MySQL root 密碼 與 資料庫名（預設 LineBot），DBeaver 也用同一組密碼
- `YOUTUBE_API_KEY` / `WEATHER_API_KEY` / `OPEN_AI_API_KEY` / `GIPHY_API_KEY` / `GEMINI_API_KEY` — 選填，沒填該功能失效
- `RENDER_EXTERNAL_HOSTNAME` — settings 裡無 default 的 env，缺失時 app 無法啟動；本地需在 `.env` 提供（例如 `*`）

所有從 `.env` 讀取的變數都在 `LineBot/settings.py`，用 `os.environ.get(..., default=env(...))` 讀取。

## 資料庫

- **MySQL 8**（docker `mysql` service，port 3306）。Also 可用 DBeaver 從其他電腦連（Host=本機 IP, Database=LineBot, User=root, Password=$MYSQL_ROOT_PASSWORD）。
- `LineBot/settings.py` 用 `DB_ENGINE` 切換 `mysql` / `sqlite`（預設 `mysql`）。`mysql` 分支從 `MYSQL_HOST/PORT/USER/PASSWORD/NAME` 讀，都有 default。
- Django atoms：
  - `BotTest.LineUser`：`line_id`（LINE 使用者 ID）、`money`（石頭數）
  - `BotTest.Photo`：`image_src`、`name`（PTT 文章標題）、`url`（PTT 文章連結）— 由 PTT Beauty 腳本填充
  - `BotTest.DailyAttendance`：`time`（`auto_now_add`）、`line_user`（FK → LineUser）

## 架構 / 檔案

- `LineBot/` — Django 專案設定（`settings.py`、`urls.py`、`wsgi.py`）
- `BotTest/views.py` — webhook `/callback` 與所有指令處理（`match message_type:`，文字指令用 `!指令` 前綴）
- `BotTest/models.py` — 三張資料表
- `BotTest/services/` — 各功能邏輯：`weather.py`、`gemini.py`、`open_ai.py`、`giphy.py`、`anime.py`、`ptt_beauty.py`、`whitecat_wiki.py`、`user_money.py`、`line_bot.py`、`redis_service.py`
- `BotTest/scripts/create_photos.py` — 抓 PTT Beauty 正妹圖灌入 `Photo`（用 `runscript create_photos`）

## 指令對照（views.py 內）

`!指令` 可列全部。常見：`!天氣`、`!簽到`、`!石頭`、`!正妹` / `!抽女朋友` / `!十連抽`、`!北捷/中捷/高捷`、`!yt`、`!gif`、`@中/英/日/韓`（翻譯）、`!ai`、`!新番`、匯率（`xx美金` 等）。sign 到 LINE Webhook URL：`你的網域/callback`。

## 常用指令（docker 內）

```bash
docker compose exec line_bot python manage.py migrate
docker compose exec line_bot python manage.py createsuperuser
docker compose exec line_bot python manage.py runscript create_photos --chdir BotTest   # 更新 PTT 正妹圖
docker compose exec line_bot python manage.py shell
```

Admin 後台：http://localhost:8000/admin

## 其他注意事項

- **Python 3.10+**：`views.py` 用到 `match` 語法，不可低於 3.10（Docker 用 python:3.10-alpine）。
- `get_web_page`（`create_photos.py`）已加 User-Agent + timeout + 3 次重試，處理 PTT 偶發斷線，不要移除。
- 改到 model 記得 `makemigrations` + `migrate`。
- DEBUG 預設從 `.env` 讀，正式環境請關閉。
