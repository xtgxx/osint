import requests
import telebot

def handle_pincode(bot, call, user_state):
    bot.send_message(call.message.chat.id, "📍 Send PINCODE:")
    user_state[call.from_user.id] = "pincode"

def handle_pincode_input(bot, msg, user_state):
    user_id = msg.from_user.id
    pincode = msg.text.strip()

    url = f"https://api.zippopotam.us/in/{requests.utils.quote(pincode)}"

    try:
        response = requests.get(url, timeout=10).json()
    except Exception as e:
        bot.send_message(msg.chat.id, f"❌ API Error: {e}")
        user_state.pop(user_id, None)
        return

    # ------------ CHECK INVALID ------------
    if "places" not in response:
        bot.send_message(msg.chat.id, "❌ Invalid PINCODE or No Data Found.")
        user_state.pop(user_id, None)
        return

    # ------------ ESCAPE MD ------------
    def escape_md(text):
        if not isinstance(text, str):
            text = str(text)
        escape_chars = r"_*[]()~`>#+-=|{}.!"
        for char in escape_chars:
            text = text.replace(char, f"\\{char}")
        return text

    final = f"📍 **PINCODE Result: {escape_md(pincode)}**\n\n"

    # API gives list of places
    for place in response["places"]:
        final += "----------------------\n"
        for k, v in place.items():
            key = k.replace("_", " ").title()
            final += f"🔹 {escape_md(key)}: {escape_md(v)}\n"

    # Add country details
    final += f"\n🌍 Country: {escape_md(response.get('country', 'Unknown'))}"

    bot.send_message(msg.chat.id, final, parse_mode="Markdown")
    user_state.pop(user_id, None)
