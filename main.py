import os
from typing import Dict, List

import openai
from dotenv import load_dotenv
from flask import Flask, render_template, request

app = Flask(__name__)

if not os.path.isfile(".env"):
    with open(".env", "w") as f:
        f.write("OPENAI_API_KEY=")

load_dotenv()


def create_images_from_prompt(form_data: Dict[str, str]) -> List[str]:
    prompt = form_data.get("text-prompt")
    size = form_data.get("image-size")
    quantity = int(form_data.get("image-quantity", 0))
    if not all([prompt, size, quantity]):
        return []
    try:
        openai.api_key = os.getenv("OPENAI_API_KEY")
        response = openai.Image.create(prompt=prompt, size=size, n=quantity)
        if "data" in response:
            return [img["url"] for img in response["data"]]
        elif "error" in response:
            return [response["error"]["message"]]
        else:
            return response
    except Exception as e:
        return [str(e)]


@app.route("/", methods=["GET", "POST"])
def home() -> str:
    images = []
    if request.method == "POST":
        images = create_images_from_prompt(request.form)
    return render_template("home.html", images=images)


if __name__ == "__main__":
    if not os.getenv("OPENAI_API_KEY"):
        raise ValueError("OPENAI_API_KEY is not set in environment variables")
    app.run()
