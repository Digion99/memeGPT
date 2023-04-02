from io import BytesIO
from base64 import b64encode
from PIL import Image, ImageDraw, ImageFont
from flask import Flask, render_template, request

app = Flask(__name__)

class MemeGenerator:
    def __init__(self, img):
        self.image = img
        self.draw = ImageDraw.Draw(self.image)
        self.font = ImageFont.truetype("arial.ttf", 50)
        self.generated_image = None
    
    def generate_meme(self, text_top, text_bottom):
        width, height = self.image.size
        x_top, y_top = width/2, 10
        x_bottom, y_bottom = width/2, height-60
        
        self.draw_text(text_top, x_top, y_top)
        self.draw_text(text_bottom, x_bottom, y_bottom)
        
        self.generated_image = self.image
    
    def draw_text(self, text, x, y):
        text_width, text_height = self.draw.textsize(text, font=self.font)
        x -= text_width / 2
        self.draw.text((x, y), text, font=self.font, fill=(255, 255, 255))

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/generate_meme', methods=['POST'])
def generate_meme():
    # Get the uploaded image, top text, and bottom text from the form data
    image = request.files['image']
    text_top = request.form['text_top']
    text_bottom = request.form['text_bottom']

    # Open the image using the PIL module
    img = Image.open(image)

    # Create an instance of the MemeGenerator class
    meme = MemeGenerator(img)

    # Generate the meme
    meme.generate_meme(text_top, text_bottom)

    # Convert the generated image to a data URI
    buffer = BytesIO()
    meme.generated_image.save(buffer, format='PNG')
    image_data = buffer.getvalue()
    image_url = f"data:image/png;base64,{b64encode(image_data).decode()}"

    # Render the result.html template with the image URL
    return render_template('result.html', image_url=image_url)

if __name__ == '__main__':
    app.run(debug=True)
