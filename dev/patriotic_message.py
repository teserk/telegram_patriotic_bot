from globals import bot


def patriotic_message(message):
    answer = 'РОССИЯ!!! РОССИЯ!! РОССИЯ!!! РОССИЯ!!!\n' \
             " 🤍🤍🤍🤍🤍🤍🤍🤍🤍🤍🤍🤍🤍🤍🤍🤍\n" \
             " 🤍🤍🤍🤍🤍🤍🤍🤍🤍🤍🤍🤍🤍🤍🤍🤍\n" \
             " 🤍🤍🤍🤍🤍🤍🤍🤍🤍🤍🤍🤍🤍🤍🤍🤍\n" \
             " 💙💙💙💙💙💙💙💙💙💙💙💙💙💙💙💙\n" \
             " 💙💙💙💙💙💙💙💙💙💙💙💙💙💙💙💙\n" \
             " 💙💙💙💙💙💙💙💙💙💙💙💙💙💙💙💙\n" \
             " ❤️❤️❤️❤️❤️❤️❤️❤️❤️❤️❤️❤️❤️❤️❤️❤️\n" \
             " ❤️❤️❤️❤️❤️❤️❤️❤️️❤️❤️❤️❤️❤️❤️❤️❤️\n" \
             " ❤️❤️❤️❤️❤️❤️❤️❤️️❤️❤️❤️❤️❤️❤️❤️❤"
    bot.send_message(message.chat.id, answer)
