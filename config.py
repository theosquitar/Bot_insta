from instabot import Bot

# Configurar el bot de Instagram
bot = Bot()

# Iniciar sesión con una cuenta ya creada manualmente
bot.login(username="axhiogb4867", password="BhPtoIXkEc")

# Seguir la cuenta objetivo
target_account = "mauriciopalominoayala"
bot.follow(target_account)

print(f"Has seguido a {target_account}")
