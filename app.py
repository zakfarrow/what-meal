from flask import Flask, request, jsonify
import os
from dotenv import load_dotenv
import mysql.connector

# Load environment variables from .env file
load_dotenv()

# Get database credentials from environment variables
db_host = os.environ.get("DB_HOST")
db_user = os.environ.get("DB_USER")
db_password = os.environ.get("DB_PASSWORD")
db_name = os.environ.get("DB_NAME")

# Set up the database connection
db_connection = mysql.connector.connect(
    host=db_host,
    user=db_user,
    password=db_password,
    database=db_name
)


#create a cursor to execute queries
cursor = db_connection.cursor()


app = Flask(__name__)

@app.route('/recipes', methods=['GET'])
def get_recipes():

    # Get user inputs from request
    ingredients = request.args.get('ingredients')

    # Split ingredients into a list
    ingredient_list = ingredients.split(',')

    # Construct the SQL query
    query = "SELECT * FROM recipes WHERE INSTR(ingredients, %s) > 0"

    # Execute the query with the provided ingredients
    cursor.execute(query, (', '.join(ingredient_list),))

    # Fetch the matching recipes
    matching_recipes = cursor.fetchall()


    # Process the results
    recipes = []
    for recipe in matching_recipes:
        recipe_data = {
            'id': recipe[0],
            'name': recipe[1],
            'ingredients': recipe[2]
        }
        recipes.append(recipe_data)



    cursor.close()
    db_connection.close()
    
    return jsonify(recipes)

if __name__ == '__main__':
    app.run(debug=True)