import maxbot_api_client_python.utils as utils
from scenes.main_menu import MainMenuScene

class StartScene:
    async def start(self, app):
        pass

    async def execute(self, n):
        if n.type == "message_callback":
            await n.answer_callback("")

        try:
            text = n.text()
        except ValueError:
            text = None

        if not text or text == "/start":
            await self.ask_language(n)
            return

        if text in ["1", "/english"]:
            await self.proceed_to_main_menu(n, "en")
        elif text in ["2", "/russian"]:
            await self.proceed_to_main_menu(n, "ru")
        else:
            await self.ask_language(n)

    async def ask_language(self, n):
        buttons = [
            [
                {"type": "callback", "text": "English", "payload": "/english"},
                {"type": "callback", "text": "Русский", "payload": "/russian"}
            ]
        ]
        keyboard_attachment = utils.attach_keyboard(buttons)
        await n.reply_with_attachments(
            "Please select your language: \nПожалуйста, выберите язык: ",
            "",
            [keyboard_attachment]
        )

    async def proceed_to_main_menu(self, n, lang: str):
        next_scene = MainMenuScene()
        n.state_manager.update_state_data(n.state_id, {"lang": lang})
        n.activate_next_scene(next_scene)
        await next_scene.send_main_menu(n, lang)