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

#debug print statement
print("Connecting to the database...")

# Set up the database connection
db_connection = mysql.connector.connect(
    host=db_host,
    user=db_user,
    password=db_password,
    database=db_name
)

#debug print statement
print("Connected to the database!")

#create a cursor to execute queries
cursor = db_connection.cursor()


app = Flask(__name__)

@app.route('/get_recipes', methods=['GET'])
def get_recipes():

    print("Received a request for recipes")
    # Get user inputs from request
    ingredients = request.args.get('ingredients')

    # Split ingredients into a list
    ingredient_list = ingredients.split(',')

    # Construct dynamic SQL query
    query = "SELECT name FROM recipes WHERE "
    conditions = []

    for ingredient in ingredient_list:
        conditions.append("ingredients LIKE '%{}%'".format(ingredient.strip()))
    
    query += " OR ".join(conditions)

    # Execute the query with the provided ingredients
    cursor.execute(query)

    # Fetch the matching recipes
    matching_recipes = cursor.fetchall()

    #debug print statement
    print("Fetched recipes:", matching_recipes)
    # Process the results
    # recipes = []
    # for recipe in matching_recipes:
    #     recipe_data = {
    #         'id': recipe[0],
    #         'name': recipe[1],
    #         'ingredients': recipe[2]
    #     }
    #     recipes.append(recipe_data)



    cursor.close()
    db_connection.close()
    
    return jsonify(matching_recipes)


if __name__ == '__main__':
    app.run(debug=True)
