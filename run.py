from application import create_app


CONFIG_NAME="development"
app = create_app(CONFIG_NAME)
# method to run the flask app
if __name__ == '__main__':
    app.run()