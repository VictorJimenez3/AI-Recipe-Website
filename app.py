from flask import Flask, jsonify, request, render_template
from pymongo import MongoClient
from pymongo.server_api import ServerApi
import json
import google.generativeai as genai

#Victor's Notes on inputs
# - when the output ends in punctuation, the calories and allergens do not show.
# When you ask it for a specific reciple while you also give igredients, it doesnt give that specific recipies, it gives random stuff from the ingredients.
#when there are no alergens it says undefined, change this to none
#also, sometimes it gives recipes with none of the igredients listed, its weird.

# MongoDB connection
uri = "mongodb+srv://vmj:RuEIzEBBBpqoWj13@cluster0.eulfz.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0&tls=true"
client = MongoClient(uri, server_api=ServerApi('1'))
db = client['ai_recipe_generator']
recipes_collection = db['recipes']

genai.configure(api_key="AIzaSyBqgBuWyNOy9qrEABYmgK1aJBR2FJ8CRSw")

# Create the model
generation_config = {
    "temperature": 1,
    "top_p": 0.95,
    "top_k": 64,
    "max_output_tokens": 8192,
    "response_mime_type": "application/json",
}

model = genai.GenerativeModel(
    model_name="gemini-1.5-flash",
    generation_config=generation_config,
)

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

from bson import ObjectId  # Import this to handle ObjectId conversion

@app.route('/run-script', methods=['POST'])
def run_script():
    user_input = request.json.get('ingredients', '')
    
    response = model.generate_content([
        "You are a kitchen assistant program that suggests recipes based on the ingredients provided by the user. Follow these rules: Only provide responses related to the kitchen, cooking, or recipes. For any off-topic conversations, return 'invalid request.' When suggesting recipes, always provide three options, each including the title, a brief description, a list of ingredients, allergen information (display 'None' if no allergens are present), and an approximate calorie count (skip this if unknown). If the user asks for one specific recipe while providing ingredients, ensure you return only that requested recipe with its details. Do not provide unrelated or random recipes based on ingredients not provided. If the output ends with punctuation, ensure allergen and calorie information is still displayed properly.",
        "output: ",
        user_input
    ])

    text_content = response._result.candidates[0].content.parts[0].text
    
    try:
        # Try parsing the response as JSON
        recipe_data = json.loads(text_content)
    except json.JSONDecodeError:
        # If parsing fails, return the text content for debugging
        return jsonify({
            "message": "Failed to parse response as JSON.",
            "raw_response": text_content
        }), 400

    # Send a valid JSON response if parsing succeeds
    return jsonify({
        "message": "Recipe generated and saved successfully!",
        "data": recipe_data,
        "ingredients": user_input.split(',')  # Return the ingredients as a list
    })


    # Save the recipe to MongoDB and capture the insert result

    #insert_result = recipes_collection.insert_one(recipe_data)

    # Convert ObjectId to a string and include it in the response
    #recipe_data['_id'] = str(insert_result.inserted_id)

    # Prepare a response message
    return jsonify({
        "message": "Recipe generated and saved successfully!",
        "data": recipe_data,
        "ingredients": user_input.split(',')  # Return the ingredients as a list
    })


if __name__ == '__main__':
    app.run(debug=True)