import os
from typing import List
from dotenv import load_dotenv
from flask import Flask, render_template, request
import openai as oa

app: Flask = Flask(__name__)


def check_env_file() -> None:
    if not os.path.isfile(".env"):
        with open(".env", "w") as f:
            f.write("OPENAI_API_KEY=")


def create_images_from_prompt(prompt: str, size: str, quantity: int) -> List[str]:
    try:
        response = oa.Image.create(prompt=prompt, size=size, n=quantity)
        return [img["url"] for img in response["data"]]
    except Exception as e:
        return [str(e)]


@app.before_first_request
def cache_api_key() -> None:
    app.api_key = os.getenv("OPENAI_API_KEY")
    if not app.api_key:
        raise ValueError("OPENAI_API_KEY is not set in environment variables")


@app.route("/", methods=["GET", "POST"])
def home() -> str:
    images: List[str] = []
    if request.method == "POST":
        prompt_text: str = request.form["prompt"]
        image_size: str = request.form["size"]
        image_quantity: int = int(request.form["quantity"])
        images = create_images_from_prompt(prompt_text, image_size, image_quantity)
    return render_template("home.html", images=images)


if __name__ == "__main__":
    check_env_file()
    load_dotenv()
    app.run(port=5000, debug=True)
