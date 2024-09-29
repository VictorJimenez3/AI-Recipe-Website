from flask import Flask, jsonify, request, render_template
from pymongo import MongoClient
from pymongo.server_api import ServerApi
import json
import google.generativeai as genai
from bson import json_util  # For MongoDB JSON serialization

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

# Fetch saved recipes from MongoDB
recipes = list(recipes_collection.find({}))

# Print recipes in a readable format
for recipe in recipes:
    print("Recipe ID:", recipe.get("_id"))
    print("Title:", recipe.get("title", "N/A"))
    print("Description:", recipe.get("description", "N/A"))
    print("Ingredients:", ", ".join(recipe.get("ingredients", [])))
    print("-" * 40)  # Separator between recipes

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

from bson import ObjectId  # Import this to handle ObjectId conversion

@app.route('/run-script', methods=['POST'])
def run_script():
    user_input = request.json.get('ingredients', '')
    
    response = model.generate_content([
        "You are a kitchen assistant program that suggests recipes based on the ingredients provided by the user. Follow these rules:Only provide responses related to the kitchen, cooking, or recipes.For any off-topic conversations, return data as error: invalid.DO NOT RETURN ANYTHING ELSE. If the user asks for recipe suggestions, provide 3 recipes, each with: -TitleBrief -descriptionList of ingredients.If the user specifically requests one recipe, provide only one.Include the following for each recipe:Allergen information, Approximate calorie count. If these are not applicaple or unknown,",
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

    insert_result = recipes_collection.insert_one(recipe_data)

    # Convert ObjectId to a string and include it in the response
    recipe_data['_id'] = str(insert_result.inserted_id)

    # Prepare a response message
    return jsonify({
        "message": "Recipe generated and saved successfully!",
        "data": recipe_data,
        "ingredients": user_input.split(',')  # Return the ingredients as a list
    })

@app.route('/save-recipe', methods=['POST'])
def save_recipe():
    data = request.json
    recipe_data = {
        "title": data.get('title'),
        "description": data.get('description'),
        "ingredients": data.get('ingredients')
    }

    # Insert the recipe into MongoDB
    insert_result = recipes_collection.insert_one(recipe_data)

    return jsonify({
        "message": "Recipe saved successfully!",
        "recipe_id": str(insert_result.inserted_id)
    })

@app.route('/show-saved-recipes', methods=['GET'])
def show_saved_recipes():
    # Fetch all saved recipes from MongoDB
    recipes = list(recipes_collection.find({}))
    
    # Convert MongoDB ObjectId to string and format data for JSON response
    for recipe in recipes:
        recipe['_id'] = str(recipe['_id'])
    
    return jsonify(recipes)

if __name__ == '__main__':
    app.run(debug=True)