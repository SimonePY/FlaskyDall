from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def home():
    try:
        # render the home page template
        return render_template('home.html')
    except Exception as e:
        # log the error and display a custom error page
        app.logger.error(str(e))
        return render_template('', error=str(e)), 500

if __name__ == "__main__":
    try:
        app.run(port=5000)
    except Exception as e:
        print(f"An error occurred: {e}")
