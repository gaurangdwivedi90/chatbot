import os
import sqlite3
from IPython.display import display, Markdown
from langchain.schema import HumanMessage
from langchain_google_genai import ChatGoogleGenerativeAI
import matplotlib.pyplot as plt
import matplotlib.image as mpimg



def fashion_recommendation(input_user):
    # Configure Gemini API
    os.environ["GOOGLE_API_KEY"] = "AIzaSyACu6v_NNeij7lik28ia05U8-NEF2k-kr0"
    
    # Initialize the model
    model = ChatGoogleGenerativeAI(
        model="models/gemini-1.0-pro-latest",
        temperature=0.7,  # Controls randomness
        top_p=0.8  # Controls nucleus sampling
    )
    
    # Function to connect to the database
    def connect_db():
        connection = sqlite3.connect('apparel.db')  # Path to your local database
        print('Database connected.')
        return connection
    
    # Function to retrieve images based on the recommendation from Gemini
    def get_image_from_db(apparel_name):
        if apparel_name is None:
            print("Apparel name is None. Cannot proceed with fetching an image.")
            return None
    
        conn = connect_db()
        cursor = conn.cursor()
        # Query the database to get the image path for the recommended apparel
        query = "SELECT image_path FROM apparel WHERE name LIKE ?"
        cursor.execute(query, ('%' + apparel_name + '%',))
        result = cursor.fetchone()
        conn.close()
        
        if result:
            print('Image found.')
            return result[0]  # Return image path or URL
        else:
            print('Image not found.')
            return None  # If no match is found
    
    # Function to get suggestions from Gemini AI
    def get_gemini_suggestions(context):
        # Call Gemini model for recommendations
        response = model(context)
        display(Markdown(response.content))  # Display the chatbot response
        
        return response.content  # Get the text content of the response
    
    # Function to extract apparel name from the recommendation_text
    def extract_apparel_name(recommendation_text):
        conn = sqlite3.connect('apparel.db')  # Connect to your SQLite database
        cursor = conn.cursor()
        
        # Execute a query to select all product names from the apparel table
        cursor.execute("SELECT name FROM apparel")
        
        products = [row[1] for row in cursor.fetchall()]
        
        conn.close()  # Close the database connection
        
        # Define a list of known product names
        available_products = products
        
        # Find the product names in the recommendation text
        found_products = []
        for product in available_products:
            if product.lower() in recommendation_text.lower():  # Case-insensitive search
                found_products.append(product)
        
        if found_products:
            return found_products  # Return all found product names
        else:
            return None
    
    # Function to fetch product names from the database
    def fetch_product_names():
        conn = sqlite3.connect('apparel.db')  # Connect to your SQLite database
        cursor = conn.cursor()
        
        # Execute a query to select all product names from the apparel table
        cursor.execute("SELECT name FROM apparel")
        
        # Fetch all results and extract product names into a list
        products = [row[0] for row in cursor.fetchall()]
        
        conn.close()  # Close the database connection
        return products
    
    # Fetch the product names from the database
    product_names = fetch_product_names()
    
    
    # Function to send context and user input
    def send_context_and_input():
        # Step 1: Define the context for the AI (Gemini) processing system
        context = {
            "role": "style consultant",
            "name": "Anna",
            "description": (
            "You are an AI-powered virtual stylist integrated into a fashion brand's website. "
            "Your primary task is to help users discover outfits that match their preferences. "
            "You offer personalized suggestions based on the user's selected products and preferences. "
            f"Only recommend products from the brand’s available catalog, which consists of {', '.join(product_names)}. "
            "Do not suggest other products and make sure . Provide suggestions in a friendly, helpful, and confident tone."
            )
        }
    
        # Example user input
        user_input = input_user
        
    
        # Combine context and user input
        conversation_context = [
            HumanMessage(content=context['description']),
            HumanMessage(content=user_input)
        ]
    
        return conversation_context
    
    # Fetch suggestions based on the combined context and input
    conversation_context = send_context_and_input()
    
    # Get apparel suggestions from Gemini
    recommendation_text = get_gemini_suggestions(conversation_context)
    
    # Print recommendation text for debugging
    print("Recommendation text:", recommendation_text)
    
    # Extract the suggested apparel names from the recommendation_text
    suggested_apparel_names = extract_apparel_name(recommendation_text)
    
    if suggested_apparel_names:
        print(f"Extracted apparel names: {suggested_apparel_names}")
        
        # Fetch and display images for each extracted product
        for apparel_name in suggested_apparel_names:
            image_path = get_image_from_db(apparel_name)
            
            if image_path:
                # Read and display the image
                img = mpimg.imread(image_path)
                plt.imshow(img)
                plt.axis('off')  # Hide axes
                plt.show()
            else:
                print(f"Sorry, no image found for the item: {apparel_name}")
    else:
        print("Could not extract any apparel names from the recommendation.")
        
    #return recommendation_text