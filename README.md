# AI Recipe Generator

## Overview
The **AI Recipe Generator** is a web-based application designed to help users create personalized recipes based on the ingredients they have available. The app generates easy-to-follow recipes and includes allergen information and calorie counts. Users can also save their favorite recipes for future reference.

## Functionality
- **Ingredient-based Recipe Generation**: Input available ingredients to generate personalized recipes.
- **Allergen and Nutritional Information**: Provides allergen details and calorie counts for each recipe.
- **Save Favorite Recipes**: Allows users to save and revisit their favorite recipes.
- **Planned Features**:
  - **Pantry Feature**: Upload a PDF of pantry items to generate recipes based on current stock.
  - **Meal Planning**: Plan meals for a specific period based on available ingredients.
  - **Grocery List Generator**: Generate a shopping list from selected recipes or meal plans.

## Technologies Used
- **Backend**: Flask (Python)
- **Database**: MongoDB
- **Frontend**: HTML, CSS, JavaScript, Bootstrap
- **AI Integration**: Google Gemini
- **Data Format**: JSON

## Installation

1. **Clone the repository**:
   ```bash
   git clone https://github.com/yourusername/AI-Recipe-Generator.git
   cd AI-Recipe-Generator
   ```

2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up MongoDB**:
   - Ensure MongoDB is installed and running locally or through a cloud service (e.g., MongoDB Atlas).
   - Update the MongoDB connection string in `config.py` with your database credentials.

4. **Run the application**:
   ```bash
   flask run
   ```

5. **Access the web app**:
   Open your browser and navigate to `http://localhost:5000` to use the AI Recipe Generator.

## Usage
1. **Input Ingredients**: Enter your available ingredients in the input field.
2. **Generate Recipes**: Click "Generate Recipe" to get personalized suggestions.
3. **Save Favorite Recipes**: Save recipes to your favorites for future use.
