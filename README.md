# LineBot

一個用 **Django** 寫的 LINE Bot。以 LINE 私訊 / 群聊指令觸發功能，例如查天氣、簽到賺石頭、抽正妹圖（PTT Beauty）、翻譯、查匯率、看新番、AI 對話等。

本專案可**本地用 Docker 部屬**，資料庫用 **MySQL**，快取用 **Redis**。MySQL 對外開 3306 port，可用 DBeaver 等工具從其他電腦連線。

## 功能指令

| 指令 | 說明 |
| --- | --- |
| `!指令` | 列出所有指令 |
| `!白貓` | 查白貓 Wiki |
| `!天氣` | 查今日天氣 |
| `!簽到` | 每日簽到 +50 石頭 |
| `!石頭` | 看目前石頭數 |
| `!正妹` / `!抽女朋友` / `!十連抽` | 花石頭抽 PTT Beauty 圖（`!正妹:名字` 可指定） |
| `!北捷` / `!中捷` / `!高捷` | 各捷運路線圖 |
| `!yt 關鍵字` | 查 YouTube 影片 |
| `!gif 關鍵字` | 回傳 Tenor GIF |
| `@中 / @英 / @日 / @韓 文字` | 翻譯 |
| `!遊戲 甲 乙 丙 ...` 再 `!抽` | 隨機抽選 |
| `!ai 問題` | Gemini AI 對話（可先傳一張圖） |
| `!新番 yyyy年x季` | 查當季新番 |
| `xx美金 / xx美 / xxUSD ...` | 匯率換算成台幣 |

## 技術棧

- Python **3.10+**（用到 `match` 語法，不可低於 3.10）
- Django 4.1
- LINE Messaging API SDK（`line-bot-sdk`）
- **MySQL 8**（資料庫）
- **Redis**（快取，存放暫存圖片 / 電影訂票旗標）
- Docker / docker-compose

## 專案結構

```
LineBot/
├── LineBot/            # Django 專案設定（settings.py / urls.py ...）
├── BotTest/            # LINE Bot 的 app
│   ├── views.py        # webhook 與各指令的處理
│   ├── models.py       # LineUser / Photo / DailyAttendance
│   └── services/       # 天氣、AI、匯率、正妹圖等邏輯
├── docker-compose.yml  # mysql + redis + line_bot
├── Dockerfile
└── requirements.txt
```

## 快速開始（使用 Docker）

### 1. 準備環境變數

```bash
cp .env.example .env
```

編輯 `.env`，填入你的金鑰。**LINE 的兩個金鑰是必填**，bot 才連得上；其他 API 金鑰沒用到可以留空，但該功能會失效。

另外 **MySQL 的 root 密碼 `MYSQL_ROOT_PASSWORD` 一定要改**（DBeaver 連線用同一組），`MYSQL_DATABASE` 預設 `LineBot` 即可：

```
MYSQL_ROOT_PASSWORD=強密碼
MYSQL_DATABASE=LineBot
```

LINE 金鑰在 [LINE Developers Console](https://developers.line.biz/) 的你的專案裡：

```
LINE_CHANNEL_ACCESS_TOKEN=...
LINE_CHANNEL_SECRET=...
```

### 2. 啟動

```bash
docker compose up -d --build
```

啟動時會自動 `migrate`（建立 MySQL 資料表），之後服務跑在：

- LINE Bot / Django：http://localhost:8000
- MySQL：localhost:3306（DBeaver 也連這個）
- Redis：localhost:6379

看 log：

```bash
docker compose logs -f line_bot
```

### 3. 設定 LINE Webhook

到 LINE Developers Console 把 Webhook URL 設為你的公網網址的 `/callback`。本機要收 LINE 的 request，通常需要把 8000 port 做 [ngrok](https://ngrok.com/) 或網頁伺服器反代到公網。

```
https://你的網域/callback
```

### 4. 停止 / 重啟

```bash
docker compose down          # 停止（資料會保留在 mysql 與 redis volume）
docker compose down -v       # 停止並刪除掉 mysql / redis 的資料（會從頭初始化）
docker compose up -d         # 再次啟動
```

### 用 DBeaver 從另一台電腦連 MySQL

MySQL 已對外開放 3306 port。在同一個區網內的電腦就能連：

1. 查這台主機在區網的 IP（例如 `192.168.x.x`）：
   ```bash
   ipconfig getifaddr en0     # macOS
   ip addr                    # Linux
   ipconfig                   # Windows（查 IPv4 位址）
   ```
2. DBeaver 新增連線 **MySQL**，填入：
   - Host：`主機IP`（例如 `192.168.137.198`）
   - Port：`3306`
   - Database：`LineBot`
   - Username：`root`
   - Password：`.env` 裡的 `MYSQL_ROOT_PASSWORD`

> 需在同一區網才能連；若跨網段要另外開防火牆 / VPN。root 已開放可從任何 host 連線（`root@%`）。
> 如果 DBeaver 報 `caching_sha2_password` 驗證失敗，可在 MySQL 內改成舊驗證方式：
> ```bash
> docker compose exec mysql mysql -uroot -p -e \
>   "ALTER USER 'root'@'%' IDENTIFIED WITH mysql_native_password BY '<MYSQL_ROOT_PASSWORD>'; FLUSH PRIVILEGES;"
> ```

## 本地開發（不裝 Docker）

需要 Python 3.10+、Redis，以及一台 MySQL（可指到 docker 起的 MySQL，或本機自己裝）。

```bash
python3.12 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt

cp .env.example .env             # 編輯填上金鑰與 MYSQL_ROOT_PASSWORD
export DB_ENGINE=mysql
export REDIS_LOCATION=redis://localhost:6379/0
# 連 docker 的 MySQL 就先用 docker compose up -d mysql；否則改用本機的 MySQL 連線資訊
export MYSQL_HOST=localhost
export MYSQL_USER=root
export MYSQL_PASSWORD=<MYSQL_ROOT_PASSWORD>
export MYSQL_NAME=LineBot
redis-server &                   # 本機要有 Redis

python manage.py migrate
python manage.py runserver 0.0.0.0:8000
```

## 常用 Django 指令

```bash
# 在 docker 內執行
docker compose exec line_bot python manage.py migrate
docker compose exec line_bot python manage.py createsuperuser   # 建 admin 帳號
docker compose exec line_bot python manage.py runscript create_photos --chdir BotTest   # 更新 PTT 正妹圖
```

Admin 後台：http://localhost:8000/admin

## 常見問題

**Q：一直連不到 Redis？**
確認 `.env` / compose 的 `REDIS_LOCATION` 正確（docker 內為 `redis://redis:6379/0`），並用 `docker compose ps` 確認 redis 有起來。

**Q：`!天氣` 沒反應？**
需要在 `.env` 填 `WEATHER_API_KEY`（中央氣象局 Open Data 金鑰，免費申請）。

**Q：想清空資料庫重新開始？**
刪掉 MySQL volume 後重建（資料會全部重置）：
```bash
docker compose down -v
docker compose up -d --build
```

**Q：port 8000 被占用？**
改 `docker-compose.yml` 的 `ports: "8000:8000"` 為你要的 host port（例如 `"9000:8000"`）。

**Q：改程式碼後要重新 build 嗎？**

`line_bot` 已掛載本機專案到 `/home/app`（見 `docker-compose.yml` 的 `volumes: .:/home/app`），
所以**改 Python 程式碼通常即時生效**：`runserver` 會自動 reload，存檔就生效，不需重 build / 重啟。

| 改動 | 需要的指令 |
| --- | --- |
| 改 Python 檔（`views.py`、`settings.py` 等） | 不用，存檔即 auto-reload |
| 改 `requirements.txt`、`Dockerfile`（裝新套件） | `docker compose up -d --build`（掛載不會重裝套件） |
| 只改 `.env` 的變數（密碼、金鑰） | `docker compose up -d`（recreate 吃到新值，不用 build） |
| 只改 `docker-compose.yml`（環境變數、port 等） | `docker compose up -d`（會 recreate，不必 build） |
| 只改 MySQL 資料 | 不用重建，`docker compose exec mysql mysql ...` 直接改 |

> 若某次改動後 auto-reload 沒生效，可 `docker compose restart line_bot`；加了新 Python 套件則必須 `--build`（掛載只同步檔案、不會重裝套件）。
> 改到 model 時記得跑 `python manage.py makemigrations` / `migrate`。

## 授權 / 備註

- 資料庫使用 MySQL，會自動建立資料庫（`MYSQL_DATABASE`）並對外開 3306。
- `LineBot/settings.py` 的資料庫設定用 `DB_ENGINE` 切換（`mysql` / `sqlite`），預設 `mysql`。
- API 金鑰都放在 `.env`（已 gitignore，不會被 commit）。
