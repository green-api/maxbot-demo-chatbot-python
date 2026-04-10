from utils.yml_reader import t
from scenes.start import StartScene
from scenes.main_menu import MainMenuScene

class EndpointsScene:
    async def start(self, app):
        pass

    async def execute(self, n):
        if n.type() == "message_callback":
            await n.answer_callback("")

        try:
            text = n.text()
        except ValueError:
            text = None

        state_data = n.state_manager.get_state_data(n.state_id)
        lang = state_data.get("lang", "ru") if state_data else "ru"

        try:
            sender_id = n.sender_id()
            sender_name = n.sender_name()
        except ValueError:
            sender_id, sender_name = 0, "User"

        text_lower = text.lower() if text else ""

        match text_lower:
            case "1" | "/message":
                await n.show_action("typing_on")
                await n.reply_with_keyboard(
                    t(lang, "send_text_message") + t(lang, "links.send_text_documentation"),
                    "markdown",
                    self.get_control_buttons(lang)
                )

            case "2" | "/file":
                await n.show_action("sending_file")
                await n.reply_with_media(
                    t(lang, "send_file_message") + t(lang, "links.send_file_documentation"),
                    "markdown",
                    "https://storage.yandexcloud.net/sw-prod-03-test/ChatBot/corgi.pdf",
                    self.get_control_buttons(lang)
                )

            case "3" | "/image":
                await n.show_action("sending_photo")
                await n.reply_with_media(
                    t(lang, "send_image_message") + t(lang, "links.send_file_documentation"),
                    "markdown",
                    "https://storage.yandexcloud.net/sw-prod-03-test/ChatBot/corgi.jpg",
                    self.get_control_buttons(lang)
                )

            case "4" | "/audio":
                await n.show_action("sending_audio")
                audio_url = "https://storage.yandexcloud.net/sw-prod-03-test/ChatBot/Audio_bot_eng.mp3"
                if lang == "ru":
                    audio_url = "https://storage.yandexcloud.net/sw-prod-03-test/ChatBot/Audio_bot.mp3"
                
                await n.reply_with_media(
                    t(lang, "send_audio_message") + t(lang, "links.send_file_documentation"),
                    "markdown",
                    audio_url,
                    self.get_control_buttons(lang)
                )

            case "5" | "/video":
                await n.show_action("sending_video")
                video_url = "https://storage.yandexcloud.net/sw-prod-03-test/ChatBot/Video_bot_eng.mp4"
                if lang == "ru":
                    video_url = "https://storage.yandexcloud.net/sw-prod-03-test/ChatBot/Video_bot_ru.mp4"
                
                await n.reply_with_media(
                    t(lang, "send_video_message") + t(lang, "links.send_file_documentation"),
                    "markdown",
                    video_url,
                    self.get_control_buttons(lang)
                )

            case "6" | "/contact":
                await n.reply_with_keyboard(
                    t(lang, "send_contact_message") + t(lang, "links.send_contact_documentation"),
                    "markdown",
                    self.get_control_buttons(lang)
                )
                await n.reply_with_contact(sender_name, "", sender_id)

            case "7" | "/location":
                await n.reply_with_keyboard(
                    t(lang, "send_location_message") + t(lang, "links.send_location_documentation"),
                    "markdown",
                    self.get_control_buttons(lang)
                )
                await n.reply_with_location(35.888171, 14.440230)

            case "8" | "/about":
                about_msg = (t(lang, "about_chatbot") +
                             t(lang, "link_to_max") +
                             t(lang, "link_to_docs") +
                             t(lang, "link_to_source_code"))
                
                await n.reply_with_keyboard(
                    about_msg,
                    "markdown",
                    self.get_control_buttons(lang)
                )

            case "стоп" | "stop" | "0" | "/stop":
                await n.reply(
                    f"{t(lang, 'stop_message')}{sender_name}!",
                    "markdown"
                )
                n.activate_next_scene(StartScene())

            case "menu" | "меню" | "/menu":
                s_menu = MainMenuScene()
                n.activate_next_scene(s_menu)
                await s_menu.send_main_menu(n, lang)

            case _:
                await n.reply(t(lang, "not_recognized_message"), "markdown")

    def get_control_buttons(self, lang: str):
        m_text, s_text = ("Menu", "Stop") if lang == "en" else ("Меню", "Стоп")
        return [
            [
                {"type": "callback", "text": m_text, "payload": "/menu"},
                {"type": "callback", "text": s_text, "payload": "/stop"}
            ]
        ]