const { MongoClient } = require('mongodb');
const { Configuration, OpenAIApi } = require('openai');

// MongoDB connection
const uri = "mongodb+srv://vmj:RuEIzEBBBpqoWj13@cluster0.eulfz.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0";
const client = new MongoClient(uri);
const dbName = 'ai_recipe_generator';
const collectionName = 'recipes';



async function main() {
    try {
        // Connect to MongoDB
        await client.connect();
        const db = client.db(dbName);
        const recipesCollection = db.collection(collectionName);

        // Configure Google Generative AI
        const configuration = new Configuration({
            apiKey: "AIzaSyBqgBuWyNOy9qrEABYmgK1aJBR2FJ8CRSw",
        });
        const openai = new OpenAIApi(configuration);

        // Create the model configuration
        const generationConfig = {
            temperature: 1,
            top_p: 0.95,
            top_k: 64,
            max_output_tokens: 8192,
            response_mime_type: "application/json",
        };

        const input = prompt('Input: '); // Assuming input from the user
        const response = await openai.createChatCompletion({
            model: "gemini-1.5-flash",
            messages: [
                {
                    role: "user",
                    content: "You are a program that will provide the user with recipes and stuff about the kitchen in general. You will take user input and suggest recipes from the ingredients they have provided. You will not provide any response or help or recipes on off-topic conversations outside of the kitchen. You will only respond as {invalid} and nothing else. If the user is looking for suggestions, you will provide 3 recipe suggestions, each with a title, description, and ingredients. If they are specifically looking for one recipe, you will only provide one."
                },
                { role: "user", content: input },
            ],
            ...generationConfig,
        });

        // Navigate to the content
        const textContent = response.data.choices[0].message.content;

        // Load the JSON data
        const recipeData = JSON.parse(textContent);

        // Extract and print the ingredients
        const ingredients = recipeData.ingredients || [];

        if (ingredients.length > 0) {
            ingredients.forEach(ingredient => {
                console.log(`- ${ingredient}`);
            });
        } else if (recipeData.recipes) {
            // Displaying the ingredients for each recipe
            recipeData.recipes.forEach(recipe => {
                console.log(`Recipe: ${recipe.title}`);
                console.log(`Description: ${recipe.description}`);
                console.log("Ingredients:");
                recipe.ingredients.forEach(ingredient => {
                    console.log(`- ${ingredient}`);
                });
                console.log();  // Add a blank line between recipes
            });
        } else {
            console.log("The key 'recipes' does not exist in the provided data.");
        }

        // Insert the recipe data into MongoDB
        const result = await recipesCollection.insertOne(recipeData);
        console.log(`New document inserted with id: ${result.insertedId}`);
        
    } catch (error) {
        console.error("Error:", error);
    } finally {
        // Close the MongoDB connection
        await client.close();
    }
}

function myFunction() {
    main();
}


    


  