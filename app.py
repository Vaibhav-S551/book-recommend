from flask import Flask, render_template, request
import pandas as pd
import pickle
import numpy as np

# Load data
popular_df = pickle.load(open('popular.pk1', 'rb'))
pt = pickle.load(open('pt.pkl', 'rb'))
books = pickle.load(open('books.pkl', 'rb'))
similarity_score = pickle.load(open('similarity_scores.pkl', 'rb'))

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index1.html',
                           book_name=list(popular_df['Book-Title'].values),
                           Author=list(popular_df['Book-Author'].values),
                           image=list(popular_df['Image-URL-M'].values),
                           rating=list(popular_df['avg_rating'].values)
    )

@app.route('/recommend')
def recommend_ui():
    return render_template('recommend.html')

@app.route('/contact')
def contact_us():
    return render_template('contact.html')
@app.route('/get_recommendations', methods=['POST'])
def recommend():
    user_input = request.form.get('user_input').strip()  # Trim whitespace

    # Check if user_input exists in the index
    if user_input not in pt.index:
        return f"Book '{user_input}' not found in the index.", 404

    # Get the index of the book
    index = np.where(pt.index == user_input)[0][0]
    print(f"User input index: {index}")  # Debugging output

    # Get similar items
    similar_items = sorted(
        list(enumerate(similarity_score[index])),
        key=lambda x: x[1],
        reverse=True
    )[1:9]  # Skip the first item (itself)

    print(f"Similar items indices: {[i[0] for i in similar_items]}")  # Debugging output

    data = []
    for i in similar_items:
        temp_df = books[books['Book-Title'] == pt.index[i[0]]]
        
        if not temp_df.empty:
            item = [
                temp_df['Book-Title'].values[0],  # Book Title
                temp_df['Book-Author'].values[0],  # Book Author
                temp_df['Image-URL-M'].values[0]   # Image URL
            ]
            data.append(item)

    print(f"Recommendations data: {data}")
   # print(data)
    #   # Debugging output
    return render_template('recommend.html', data=data)

if __name__ == '__main__':
    app.run(debug=True)
