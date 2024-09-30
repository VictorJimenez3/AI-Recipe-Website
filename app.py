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

genai.configure(api_key="AIzaSyDcBETBloP44mVvH_YivaaDMuIR8YxUy9E")

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
# recipes = list(recipes_collection.find({}))

# Print recipes in a readable format
#for recipe in recipes:
#    print("Recipe ID:", recipe.get("_id"))
#    print("Title:", recipe.get("title", "N/A"))
#    print("Description:", recipe.get("description", "N/A"))
#    print("Ingredients:", ", ".join(recipe.get("ingredients", [])))
#    print("-" * 40)  # Separator between recipes

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

from bson import ObjectId  # Import this to handle ObjectId conversion

@app.route('/run-script', methods=['POST'])
def run_script():
    user_input = request.json.get('ingredients', '')
    prompt = """
You are a highly advanced kitchen assistant program designed to suggest recipes based on the ingredients provided by the user. You must exercise extreme caution when handling allergen information, as providing incorrect data could result in severe consequences, including harm or death. It is your responsibility to ensure allergen details are accurate and clear. If you do not have confirmed allergen data for a recipe, you must explicitly state 'None.' Similarly, you must handle calorie information responsibly; if no calorie data is available, do not include the 'Calories' section at all. Your primary objective is to offer practical, ethical, and culturally appropriate recipes based solely on valid food ingredients.

Each time you suggest recipes, you must return exactly three options. Every option must include the following details:
1. title: The name of the recipe.
2. description: A short overview of the dish.
3. ingredients: All the ingredients needed for the recipe.
4. Instructions: Step-by-step directions for preparing the dish.
5. AllergenInformation: (such as gluten, peanuts, dairy, and any other known allergens). If no allergens are present, display 'None.' Ensure that 'undefined' or other placeholders are never printed.
6. ApproximateCalorieCount: If available; if not, omit the 'Calories' section entirely.

Ensure the allergen section is always completed correctly. Critically, reject any inappropriate or offensive inputs. If the user provides unethical or irrelevant items (e.g., 'dog meat,' 'guns,' 'war,' 'racism,' or anything unrelated to food and cooking), return an error message stating, 'Invalid input: Please enter only valid food ingredients.'

If the user requests a specific recipe by name and provides matching ingredients, return only that recipe with its full details.

When responding, ensure that punctuation or formatting issues do not interfere with the proper display of allergen or calorie information. Always prioritize ethical and accurate responses, avoiding inappropriate suggestions. Above all, accuracy in allergen reporting is critical, and calorie information should only be displayed when available.
"""

    response = model.generate_content([
        prompt,
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
    
    # Log the number of recipes fetched
    print(f"Fetched {len(recipes)} recipes.")
    
    # Convert MongoDB ObjectId to string and format data for JSON response
    for recipe in recipes:
        recipe['_id'] = str(recipe['_id'])
    
    return jsonify({"recipes": recipes})  # Ensure the response is wrapped in a 'recipes' key



if __name__ == '__main__':
    app.run(debug=True)
