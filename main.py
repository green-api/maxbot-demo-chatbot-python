import asyncio, logging, os, time
from dotenv import load_dotenv

from maxbot_chatbot_python import Bot, MapStateManager
from maxbot_api_client_python import API, Config
from scenes.start import StartScene

logger = logging.getLogger(__name__)

async def main():
    if not load_dotenv():
        logger.warning("Error loading .env file or it does not exist")

    cfg = Config(
        base_url=os.getenv("BASE_URL"),
        token=os.getenv("TOKEN"),
        ratelimiter=25,
        timeout=30
    )

    async with API(cfg) as api_client:
        app_bot = Bot(api_client)
        
        start_scene = StartScene()
        app_bot.state_manager = MapStateManager(init_data={})
        app_bot.state_manager.set_start_scene(start_scene)

        start_time = time.time()

        @app_bot.router.register("message_created")
        @app_bot.router.register("message_callback")
        async def scene_handler(notification):
            if notification.update and getattr(notification.update, 'timestamp', 0) < (start_time * 1000):
                return
            
            notification.create_state_id()

            if not app_bot.state_manager.get(notification.state_id):
                app_bot.state_manager.create(notification.state_id)

            current_scene = notification.get_current_scene()
            if not current_scene:
                current_scene = start_scene
                notification.activate_next_scene(current_scene)

            if hasattr(current_scene, 'execute'):
                await current_scene.execute(notification)
            else:
                logger.error(f"Current scene {type(current_scene).__name__} does not implement 'execute'")

        try:
            logger.info("Bot is polling...")
            await app_bot.start_polling()
        except asyncio.CancelledError:
            logger.info("The bot has been stopped")

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logger.info("The bot has been stopped by user")