from flask import Flask, render_template, request
import pandas as pd
import re

app = Flask(__name__)

# Define the route for the homepage
@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        # Check if a file was uploaded
        if 'file' not in request.files:
            return render_template('index.html', error='No file part')

        file = request.files['file']

        # Check if the file name is empty
        if file.filename == '':
            return render_template('index.html', error='No selected file')

        # Check if the file is in CSV format
        if file and file.filename.endswith('.csv'):
            # Read the CSV file into a DataFrame
            df = pd.read_csv(file)

            # Create a dictionary to store ingredient counts
            ingredient_counts = {}

            # Iterate over each row in the DataFrame
            for index, row in df.iterrows():
                ingredients = row['Ingredients'].split('\n')
                for item in ingredients:
                    # Extracting ingredient name and quantity
                    matches = re.findall(r'([a-zA-Z\s]+)\s*-\s*([\d\.]+)\s*(?:g|gm)?', item)
                    for match in matches:
                        item_name, item_quantity = match
                        item_name = item_name.strip()  # Remove extra spaces
                        item_quantity = float(item_quantity)  # Convert quantity to float

                        # Update ingredient count in the dictionary
                        if item_name in ingredient_counts:
                            ingredient_counts[item_name] += item_quantity
                        else:
                            ingredient_counts[item_name] = item_quantity

            # Return the ingredient counts
            return render_template('index.html', ingredient_counts=ingredient_counts)

    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
