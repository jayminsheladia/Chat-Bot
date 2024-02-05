# Imports
from newspaper import Article
import random
import string
import nltk
import os
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity

nltk_data_path = os.path.join(os.path.dirname(__file__), 'nltk_data')
nltk.data.path.append(os.path.abspath(nltk_data_path))

# Download the punkt package
nltk.download('punkt', quiet=True)

# Function to get and parse articles
def get_parsed_articles(urls):
    corpus = ''
    for url in urls:
        article = Article(url)
        article.download()
        article.parse()
        article.nlp()
        corpus += article.text + ' '
    return corpus

# Function for greeting response
def greet_response(text):
    text = text.lower()
    bot_greet = ['hello', 'hi', 'hey', 'wassup']
    user_greet = ['hi', 'hello', 'helo', 'hiii', 'wassup', 'hey']
    for word in text.split():
        if word in user_greet:
            return random.choice(bot_greet)

# Function to sort indices based on values
def index_sort(list_var):
    length = len(list_var)
    list_index = list(range(length))
    x = list_var
    for i in range(length):
        for j in range(length):
            if x[list_index[i]] > x[list_index[j]]:
                temp = list_index[i]
                list_index[i] = list_index[j]
                list_index[j] = temp
    return list_index

# Function for bot response to queries
def bot_response(user_input):
    user_input = user_input.lower()
    sentence_list.append(user_input)
    bot_res = ''
    cm = CountVectorizer().fit_transform(sentence_list)
    similarity_score = cosine_similarity(cm[-1], cm)
    similarity_score_list = similarity_score.flatten()
    index = index_sort(similarity_score_list)
    index = index[1:]
    response_flag = 0
    j = 0
    for i in range(len(index)):
        if similarity_score_list[index[i]] > 0.001:
            bot_res = bot_res + ' ' + sentence_list[index[i]]
            response_flag = 1
            j += 1
        if j > 2:
            break
    if response_flag == 0:
        bot_res = bot_res + 'I apologize, I have not understood your meaning.'
    sentence_list.remove(user_input)
    return bot_res

# Start the chat
print("Covid Helpline: I am here to help you with information regarding the Covid virus. If you want to exit, type bye or exit.")
exit_list = ['bye', 'exit', 'byee', 'break', 'quit']

# URLs for articles
article_urls = ['https://en.wikipedia.org/wiki/Coronavirus', 'https://en.wikipedia.org/wiki/BTS']
corpus = get_parsed_articles(article_urls)
sentence_list = nltk.sent_tokenize(corpus)

while True:
    user_input = input()
    if user_input.lower() in exit_list:
        print("Bot: Thank you for connecting with us. See you later.")
        break
    else:
        if greet_response(user_input) is not None:
            print('Bot: ' + greet_response(user_input))
        else:
            print('Bot: ' + bot_response(user_input))
