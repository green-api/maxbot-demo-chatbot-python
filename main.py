import os, sys, time, logging, asyncio
from dotenv import load_dotenv

from maxbot_chatbot_python.bot import Bot
from maxbot_api_client_python import API, Config
from maxbot_chatbot_python.state import MapStateManager
from scenes.start import StartScene

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logging.getLogger("httpx").setLevel(logging.WARNING)
logger = logging.getLogger(__name__)

sys.dont_write_bytecode = True

async def main():
    if not load_dotenv():
        logger.warning("Warning: Error loading .env file or it does not exist")

    try:
        api_client = API(Config(
            base_url=os.getenv("BASE_URL"),
            token=os.getenv("TOKEN"),
            global_rps=25,
            timeout=30
        ))
        app_bot = Bot(api_client)
    except Exception as e:
        logger.fatal(f"Bot initialization error: {e}")
        return

    start_scene = StartScene()
    app_bot.state_manager = MapStateManager({})
    app_bot.state_manager.set_start_scene(start_scene)

    start_time = time.time()

    @app_bot.router.register("message_created")
    @app_bot.router.register("message_callback")

    async def scene_handler(n):
        if n.update and getattr(n.update, 'timestamp', 0) < start_time:
            return
        
        n.create_state_id()

        if not app_bot.state_manager.get(n.state_id):
            app_bot.state_manager.create(n.state_id)

        current_scene = n.get_current_scene()
        if not current_scene:
            current_scene = start_scene
            n.activate_next_scene(current_scene)

        if hasattr(current_scene, 'execute'):
            await current_scene.execute(n)
        else:
            logger.error("Current scene does not implement 'execute' method")

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