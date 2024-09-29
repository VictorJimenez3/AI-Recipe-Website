    function myFunction() {
        const ingredients = document.getElementById('ingredients').value;

        // Create sparkles
        createSparkles();

        fetch('/run-script', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ ingredients: ingredients })
        })
        .then(response => response.text()) // Get the response as text
        .then(data => {
            try {
                const jsonData = JSON.parse(data); // Parse the JSON data

                // Check for error in response data
                if (jsonData.data && jsonData.data.error === "invalid") {
                    alert("Error: Invalid request. Please provide valid ingredients.");
                } else {
                    displayRecipes(jsonData.data); // Pass the data object directly if no error
                }
            } catch (error) {
                console.error('Error parsing JSON:', error);
                alert("invalid input.");
            }
        })
        .catch(error => {
            console.error('Error:', error);
            alert("Failed to fetch the recipe. Please check your connection.");
        });
    }



            function createSparkles() {
                const button = document.querySelector('.button');
                const sparkleCount = 10; // Number of sparkles

                for (let i = 0; i < sparkleCount; i++) {
                    const sparkle = document.createElement('div');
                    sparkle.classList.add('sparkle');

                    // Position the sparkle randomly
                    sparkle.style.left = `${Math.random() * button.offsetWidth}px`;
                    sparkle.style.top = `${Math.random() * button.offsetHeight}px`;

                    button.appendChild(sparkle);

                    // Remove the sparkle after animation
                    setTimeout(() => {
                        sparkle.remove();
                    }, 600); // Match this to the duration of the animation
                }
            }

            function displayRecipes(data) {
                const recipesDiv = document.getElementById('recipes');
                recipesDiv.innerHTML = ''; // Clear previous recipes

                if (Array.isArray(data.recipes)) {
                    data.recipes.forEach(recipe => {
                        appendRecipe(recipesDiv, recipe);
                    });
                } else {
                    appendRecipe(recipesDiv, data);
                }
            }

            function appendRecipe(recipesDiv, recipe) {
                console.log("Appending recipe:", recipe); // Log each recipe
                const recipeElement = document.createElement('div');
                recipeElement.className = 'recipe';
            
                let calorieLabel = '';
                let calorieValue = '';
            
                if (recipe.calories) {
                    calorieLabel = 'Calories';
                    calorieValue = recipe.calories;
                } else {
                    calorieLabel = 'Calories';
                    calorieValue = 'Not available';
                }
            
                recipeElement.innerHTML = `
                    <h2>${recipe.title}</h2>
                    <p>${recipe.description}</p>
                    <h3>Ingredients:</h3>
                    <ul>
                        ${Array.isArray(recipe.ingredients) ? recipe.ingredients.map(ingredient => `<li>${ingredient}</li>`).join('') : '<li>No ingredients available</li>'}
                    </ul>
                    <h3>Allergen Information:</h3>
                    <p>${recipe.AllergenInformation || 'None'}</p>
                    <h4>${calorieLabel}:</h4>
                    <p>${calorieValue}</p>
                    <h3>Approximate Calorie Count:</h3>
                    <p>${recipe.ApproximateCalorieCount || 'None'}</p>
                    <h3>Instructions:</h3>
                    <p>${recipe.Instructions || 'None'}</p>
                `;
                
                recipesDiv.appendChild(recipeElement);
            }
            

            function saveRecipe(title, description, ingredients) {
                fetch('/save-recipe', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify({
                        title: title,
                        description: description,
                        ingredients: ingredients.split(',')
                    })
                })
                    .then(response => response.json())
                    .then(data => alert(data.message))
                    .catch(error => console.error('Error:', error));
            }

            function showSavedRecipes() {
                fetch('/show-saved-recipes', {
                    method: 'GET',
                    headers: {
                        'Content-Type': 'application/json',
                    }
                })
                .then(response => response.json())
                .then(data => {
                    console.log(data); // Log the response data to see its structure
                    displayRecipes(data);
                })
                .catch(error => console.error('Error:', error));
            }