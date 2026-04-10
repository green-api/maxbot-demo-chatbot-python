import asyncio
from maxbot_api_client_python.types import models
from maxbot_api_client_python import utils
from utils.yml_reader import t

class MainMenuScene:
    async def start(self, app):
        pass

    async def execute(self, n):
        if n.type() == "message_callback":
            await n.answer_callback("")

        state_data = n.state_manager.get_state_data(n.state_id)
        lang = state_data.get("lang", "ru") if state_data else "ru"

        await self.send_main_menu(n, lang)

    async def send_main_menu(self, n, lang: str):
        from scenes.endpoints import EndpointsScene 

        n.state_manager.update_state_data(n.state_id, {"lang": lang})
        
        try:
            sender_name = n.sender_name()
        except ValueError:
            sender_name = "User"

        await asyncio.sleep(0.5)

        image_source = "https://drive.google.com/uc?export=download&id=1gi2bPCQVgldRZolRH7gxevs1GIMnxmi2"
        image_attachment = models.Attachment(
            type="image",
            payload={"url": image_source}
        )

        btn_labels = {
            "ru": ["Текст 📩", "Файл 📋", "Картинка 🖼", "Аудио 🎵", "Видео 📽", "Контакт 📱", "Геолокация 🌎", "О боте 🦎", "Стоп"],
            "en": ["Text 📩", "File 📋", "Image 🖼", "Audio 🎵", "Video 📽", "Contact 📱", "Location 🌎", "About 🦎", "Stop"],
        }
        l = btn_labels.get(lang, btn_labels["en"])

        keyboard_attachment = utils.attach_keyboard([
            [{"type": "callback", "text": l[0], "payload": "/message"}, {"type": "callback", "text": l[1], "payload": "/file"}],
            [{"type": "callback", "text": l[2], "payload": "/image"}, {"type": "callback", "text": l[3], "payload": "/audio"}],
            [{"type": "callback", "text": l[4], "payload": "/video"}, {"type": "callback", "text": l[5], "payload": "/contact"}],
            [{"type": "callback", "text": l[6], "payload": "/location"}, {"type": "callback", "text": l[7], "payload": "/about"}],
            [{"type": "callback", "text": l[8], "payload": "/stop"}],
        ])

        await n.reply_with_attachments(
            f"{t(lang, 'welcome_message')}**{sender_name}**!{t(lang, 'menu')}",
            "markdown",
            [image_attachment, keyboard_attachment]
        )

        n.activate_next_scene(EndpointsScene())