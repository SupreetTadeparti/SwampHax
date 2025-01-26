from flask import Flask, request, send_from_directory
from manim_model import ManimModel
import os
import openai
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

SYSTEM_PROMPT = (
    "You are a code assistant that exclusively writes Python scripts using the Manim library. "
    "Your task is to create animations that explain mathematical concepts based on the given prompt. "
    "You must use the `manim_voiceover` library for adding voiceovers to the animations. "
    "Import `GTTSService` explicitly using `from manim_voiceover.services.gtts import GTTSService`. "
    "Use the `VoiceoverScene` class, and ensure that all voiceovers are synchronized with the animations. "
    "Your output must only include the complete Python script, formatted for Python syntax. "
    "Do not include any explanations, comments, backticks, or additional text. DO NOT WRAP THE CODE IN BACKTICKS UNDER ANY CIRCUMSTANCES. "
)

client = OpenAI()
client.api_key = os.getenv("OPENAI_API_KEY")
manim_model = ManimModel()

app = Flask(__name__)

@app.route('/')
def home():
    return "Hello, Flask!"

@app.route('/video/<path:filename>')
def serve_media(filename):
    return send_from_directory('.', filename)

@app.route('/generate_animation_openai')
def generate_animation_openai():
    prompt = request.args.get('prompt')
    if not prompt:
        return {"error": "No prompt provided."}, 400

    completion = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": prompt}
        ],
        max_tokens=1024,
        temperature=0.3,
    )

    try: 
        script = completion.choices[0].message.content
        filename = manim_model.generate_unique_filename()
        video_path = manim_model.execute_animation(script, filename)
        if video_path and os.path.exists(video_path):
            return {"video_path": video_path}
        else:
            return {"error": "Failed to generate animation"}, 500
    except Exception as e:
        return {"error": str(e)}, 500

@app.route('/generate_animation_finetuned')
def generate_animation():
    prompt = request.args.get('prompt')
    if not prompt:
        return {"error": "No prompt provided."}, 400
    
    try:
        script = manim_model.generate_script(f"I would like to create an animation that {prompt}")
        filename = manim_model.generate_unique_filename()
        video_path = manim_model.execute_animation(script, filename)
        
        if video_path and os.path.exists(video_path):
            return {"video_path": video_path}
        else:
            return {"error": "Failed to generate animation"}, 500
    except Exception as e:
        return {"error": str(e)}, 500

if __name__ == '__main__':
    app.run(debug=True, use_reloader=False, host='0.0.0.0')