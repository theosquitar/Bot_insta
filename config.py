from instabot import Bot

# Configurar el bot de Instagram
bot = Bot()

# Iniciar sesión con una cuenta ya creada manualmente
bot.login(username="ghmivcv1640", password="AIXXPNobqn")

# Seguir la cuenta objetivo
target_account = "mauriciopalominoayala"
bot.follow(target_account)

print(f"Has seguido a {target_account}")
