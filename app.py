import pandas as pd
from flask import Flask, request, jsonify, render_template
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.preprocessing import MinMaxScaler

# Initialize Flask App
app = Flask(__name__)

# Load and preprocess dataset
data = pd.read_csv('C:\\Users\\Sunil\\OneDrive\\Desktop\\music-recommendation\\music_dataset\\Kannada_songs.csv')

# Define numerical features for similarity calculation
numerical_features = ['danceability', 'acousticness', 'energy', 'tempo', 'loudness', 'Valence']

# Normalize features
scaler = MinMaxScaler()
data[numerical_features] = scaler.fit_transform(data[numerical_features])

# Encode categorical features
data = pd.get_dummies(data, columns=['language'], drop_first=True)

# Create similarity matrix
features = numerical_features + list(data.filter(like='language_').columns)
similarity_matrix = cosine_similarity(data[features])

# Define recommendation function
def recommend_songs(song_name, num_recommendations=5):
    try:
        song_index = data[data['song_name'] == song_name].index[0]
        similarity_scores = list(enumerate(similarity_matrix[song_index]))
        sorted_scores = sorted(similarity_scores, key=lambda x: x[1], reverse=True)
        recommended_indexes = [index for index, score in sorted_scores[1:num_recommendations+1]]
        return data.iloc[recommended_indexes]['song_name'].tolist()
    except IndexError:
        return ["Song not found in the dataset. Please try another song."]

# Serve HTML page
@app.route('/')
def home():
    return render_template('index.html')

# Handle song recommendations
@app.route('/recommend', methods=['POST'])
def recommend():
    song_name = request.json.get('song_name', "")
    recommendations = recommend_songs(song_name)
    return jsonify({"recommendations": recommendations})

# Run Flask App
if __name__ == '__main__':
    app.run(debug=True)