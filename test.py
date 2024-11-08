import sqlite3

def get_image_from_db(apparel_name):
    conn = sqlite3.connect('apparel.db')
    cursor = conn.cursor()

    # Query to fetch the image path for the apparel
    query = "SELECT image_path FROM apparel WHERE name LIKE ?"
    cursor.execute(query, ('%' + apparel_name + '%',))
    result = cursor.fetchone()

    conn.close()

    if result:
        return result[0]  # Return the image path
    else:
        return None  # No image found

# Example: Retrieve the image for "Blue Shirt"
image_path = get_image_from_db("red hoodie")
if image_path:
    print(f"Image path: {image_path}")
else:
    print("No image found.")
    
    
from IPython.display import Image, display

# Display the image using the path
if image_path:
    display(Image(image_path))
else:
    print("No image found.")
