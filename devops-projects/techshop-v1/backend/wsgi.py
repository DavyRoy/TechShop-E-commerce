from app import create_app

# Создать приложение
app = create_app()

# Запустить если файл запущен напрямую
if __name__ == '__main__':
    app.run(
        host='0.0.0.0',
        port=5000,
        debug=True
    )