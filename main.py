from src.services.telegram_service import bot

# app = Flask(__name__)
# app.register_blueprint(diecast, url_prefix='/diecast')


if __name__ == "__main__":
    # app.run(debug=False, port=5000)
    bot.infinity_polling()
