# 🚀 Быстрый запуск Twitch AutoPoster

## ⚡ 5 минут до первого поста

### 1. Установка зависимостей
```bash
pip install -r requirements.txt
```

### 2. Настройка конфигурации
1. Скопируйте `env_example.txt` в `.env`
2. Заполните данные в `.env` файле

### 3. Тестирование
```bash
python test_config.py
```

**Если есть ошибки с Telegram:**
```bash
python debug_telegram.py
```

**Если проблема с chat_id:**
```bash
python fix_chat_id.py
```

**Если проблема с правами:**
```bash
python check_permissions.py
```

### 4. Запуск
```bash
python main.py
```

## 🔑 Что нужно получить:

### Twitch API:
- [Twitch Developer Console](https://dev.twitch.tv/console)
- Client ID + Client Secret

### Telegram Bot:
- [@BotFather](https://t.me/botfather)
- Bot Token + Channel ID

### VK API (опционально):
- [VK Developers](https://vk.com/dev)
- Group ID + Access Token

## 📱 Результат:
Автоматические посты в Telegram и VK при каждом запуске стрима!

---
**Подробная документация:** [README.md](README.md)
