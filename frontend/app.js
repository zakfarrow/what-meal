document.addEventListener("DOMContentLoaded", () => {
    const form = document.querySelector("#recipe-form");
    const recipeList = document.querySelector("#recipe-list");

    form.addEventListener("submit", async (event) => {
        event.preventDefault();
        
        const ingredients = form.elements["ingredients"].value;
        const encodedIngredients = encodeURIComponent(ingredients);
        const response = await fetch(`http://localhost:5000/backend/get_recipes?ingredients=${encodedIngredients}`);

        const recipes = await response.json();

        // Display recipe suggestions
        recipeList.innerHTML = "";
        recipes.forEach(recipe => {
            const recipeDiv = document.createElement("div");
            recipeDiv.textContent = recipe.name;
            recipeList.appendChild(recipeDiv);
        });
    });
});
