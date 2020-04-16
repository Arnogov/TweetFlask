#Import de fonctions depuis le Framework Flask
from flask import Flask
#Import d'une fonction pour convertir un template HTML en y injectant des variables Python
from flask import render_template
#Import de la variable request de Flask
from flask import request
from flask import redirect, url_for
from tweet import Tweet
import os

app = Flask(__name__)
tweets = []

tweets.append(Tweet("John", "Tweet n°1"))
tweets.append(Tweet("Jane", "Lorem ipsum"))
tweets.append(Tweet("John", "Dolores sit amet"))
tweets.append(Tweet("John", "Autre tweet"))
tweets.append(Tweet("John", "Dernier tweet"))

@app.route('/')
def hello_world():
    return 'Hello, World!'

@app.route('/tweets')
def display_tweets():
    return render_template('tweets.html', tweets=tweets)

@app.route('/tweets/<author>')
def display_author_tweets(author):
    authorTweets = [] #
    for tweet in tweets: # 
        if tweet.authorName == author :
            authorTweets.append(tweet)
    return render_template('tweets.html', tweets=authorTweets)

@app.route('/tweets/create', methods=['POST', 'GET'])
def display_create_tweet():
    if request.method == 'GET':
        return render_template('create_tweet.html')
    else:
        authorName = request.form['author']
        content = request.form['content']
        image = None
        f = request.files['image']
        if f.filename != '' :
            filepath = os.path.join(app.root_path, 'static', 'uploads', f.filename)
            f.save(filepath)
            image = url_for('static', filename='uploads/'+f.filename)
        tweet = Tweet(authorName, content, image)
        tweets.insert(0, tweet)
        return redirect(url_for('display_tweets'))

def find_tweet_by_id(tweet_id):
    for tweet in tweets :
        if tweet.id == tweet_id :
            return tweet
    return None

# /tweets/3/edit
@app.route('/tweets/<int:tweet_id>/edit', methods=['POST', 'GET'])
def edit_tweet(tweet_id):
    tweet = find_tweet_by_id(tweet_id)
    if request.method == 'GET':
        return render_template('edit_tweet.html', tweet=tweet)
    else:
        tweet.authorName = request.form['author']
        tweet.content = request.form['content']
        f = request.files['image']
        if f.filename != '' :
            filepath = os.path.join(app.root_path, 'static', 'uploads', f.filename)
            f.save(filepath)
            tweet.image = url_for('static', filename='uploads/'+f.filename)
        return redirect(url_for('display_tweets'))

# Ajouter une image à un tweet : 
# Modifier le modèle d'un Tweet (modifier la classe Tweet pour y ajouter une image.)
# Ajouter un input de type file dans le formulaire de création
# Modifier la méthode POST de création d'un tweet pour prendre en compte le fichier
# Afficher l'image d'un tweet (si il en a une) dans la liste des tweets
# 
# pour créer le chemin du fichier venant du formulaire :
# import os
# filename = os.path.join(app.instance_path, 'static', 'nom du fichier.jpg')