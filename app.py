from flask import Flask, render_template, request
import google.generativeai as genai

genai.configure(api_key="Your-API-Key")

# Set up the model
generation_config = {
  "temperature": 1,
  "top_p": 0.95,
  "top_k": 0,
  "max_output_tokens": 8192,
}

safety_settings = [
  {
    "category": "HARM_CATEGORY_HARASSMENT",
    "threshold": "BLOCK_MEDIUM_AND_ABOVE"
  },
  {
    "category": "HARM_CATEGORY_HATE_SPEECH",
    "threshold": "BLOCK_MEDIUM_AND_ABOVE"
  },
  {
    "category": "HARM_CATEGORY_SEXUALLY_EXPLICIT",
    "threshold": "BLOCK_MEDIUM_AND_ABOVE"
  },
  {
    "category": "HARM_CATEGORY_DANGEROUS_CONTENT",
    "threshold": "BLOCK_MEDIUM_AND_ABOVE"
  },
]

model = genai.GenerativeModel(model_name="gemini-1.5-pro-latest",
                              generation_config=generation_config,
                              safety_settings=safety_settings)


def get_ai_response(user_input):
  convo = model.start_chat(history=[])  
  convo.send_message(user_input)
  return convo.last.text

app = Flask(__name__)

app.config['STATIC_FOLDER'] = 'static'

@app.route('/', methods=['GET', 'POST'])
def index():
  response = None
  image_url = None  

  if request.method == 'POST':
    user_input = request.form['user_input']
    response = get_ai_response(user_input)

  return render_template('index.html', response=response, image_url=image_url)

if __name__ == '__main__':
  app.run(debug=True)