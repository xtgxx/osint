import requests
import telebot

def handle_imei(bot, call, user_state):
    bot.send_message(call.message.chat.id, "📱 Send the IMEI number:")
    user_state[call.from_user.id] = "imei"

def handle_input(bot, msg, user_state):
    user_id = msg.from_user.id
    number = msg.text.strip()
    url = f"https://osintx.info/API/imei.php?key=EDWARD&term={requests.utils.quote(number)}"

    try:
        response = requests.get(url, timeout=10).json()
    except Exception as e:
        bot.send_message(msg.chat.id, f"❌ API Error: {e}")
        user_state.pop(user_id, None)
        return

    # ---------------- ESCAPE MARKDOWN CHARACTERS ----------------
    def escape_md(text):
        if not isinstance(text, str):
            text = str(text)
        escape_chars = r"_*[]()~`>#+-=|{}.!"
        for char in escape_chars:
            text = text.replace(char, f"\\{char}")
        return text

    formatted = ""
    for k, v in response.items():
        formatted += f"🔹 {escape_md(k.title())}: {escape_md(v)}\n"

    # ---------------- SEND WITHOUT PARSING ----------------
    bot.send_message(msg.chat.id, f"📱 IMEI Result\n\n{formatted}")
    user_state.pop(user_id, None)
