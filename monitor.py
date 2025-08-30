#!/usr/bin/env python3
"""
Скрипт для мониторинга Twitch AutoPoster с логированием
"""

import time
import logging
from datetime import datetime
from main import TwitchAutoPoster

# Настройка логирования
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('autoposter.log', encoding='utf-8'),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger(__name__)

class MonitoredAutoPoster(TwitchAutoPoster):
    """Расширенная версия AutoPoster с логированием"""
    
    def __init__(self):
        super().__init__()
        logger.info("🚀 Инициализация Twitch AutoPoster с мониторингом")
    
    def get_twitch_token(self):
        """Получение токена с логированием"""
        logger.info("🔑 Получение токена Twitch...")
        result = super().get_twitch_token()
        if result:
            logger.info("✅ Токен Twitch получен успешно")
        else:
            logger.error("❌ Не удалось получить токен Twitch")
        return result
    
    def check_stream_status(self):
        """Проверка статуса стрима с логированием"""
        logger.debug("🔍 Проверка статуса стрима...")
        result = super().check_stream_status()
        return result
    
    def post_to_socials(self, stream_info):
        """Постинг в соцсети с логированием"""
        logger.info(f"📝 Постинг информации о стриме: {stream_info.get('title', 'Без названия')}")
        super().post_to_socials(stream_info)
    
    def post_to_telegram(self, message):
        """Постинг в Telegram с логированием"""
        logger.info("📱 Отправка поста в Telegram...")
        super().post_to_telegram(message)
    
    def post_to_vk(self, message):
        """Постинг в VK с логированием"""
        logger.info("🌐 Отправка поста в VK...")
        super().post_to_vk(message)
    
    def run(self):
        """Основной цикл с расширенным логированием"""
        logger.info("🚀 Запуск Twitch AutoPoster с мониторингом...")
        logger.info(f"📺 Мониторинг канала: {TWITCH_STREAMER_LOGIN}")
        logger.info(f"📱 Telegram канал: {TELEGRAM_CHANNEL_ID}")
        logger.info(f"🌐 VK группа: {VK_GROUP_ID if VK_GROUP_ID else 'Не настроена'}")
        logger.info("=" * 50)
        
        start_time = datetime.now()
        check_count = 0
        
        while True:
            try:
                check_count += 1
                current_time = datetime.now()
                uptime = current_time - start_time
                
                logger.info(f"🔍 Проверка #{check_count} (Uptime: {uptime})")
                
                self.check_stream_status()
                
                # Логируем статистику каждые 10 проверок
                if check_count % 10 == 0:
                    logger.info(f"📊 Статистика: {check_count} проверок, Uptime: {uptime}")
                
                time.sleep(60)  # Проверяем каждую минуту
                
            except KeyboardInterrupt:
                logger.info("🛑 Остановка программы по запросу пользователя...")
                break
            except Exception as e:
                logger.error(f"❌ Неожиданная ошибка: {e}", exc_info=True)
                time.sleep(60)
        
        logger.info(f"🏁 Программа остановлена. Всего проверок: {check_count}")

def main():
    """Главная функция"""
    try:
        poster = MonitoredAutoPoster()
        poster.run()
    except Exception as e:
        logger.error(f"💥 Критическая ошибка: {e}", exc_info=True)
        raise

if __name__ == "__main__":
    main()
