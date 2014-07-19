import sys
import json

unknown_words_scores = {}   # Sentiment scores of each unknown word
unknown_words_count = {}    # Number of tweets in which the unknown words occur 

def calculate_sentiment(tweet, scores):
    tweet = tweet.encode('utf-8')
    words_in_tweet = tweet.split(" ")
    sentiment_score = 0
    to_be_added = []
    for word in words_in_tweet:
        if scores.has_key(word):
            sentiment_score = sentiment_score + scores[word]
        else:
            if to_be_added.count(word) == 0:    # If the same word is present more than once in a tweet
                to_be_added.append(word)
            if not unknown_words_scores.has_key(word):  # If the word is not already found in previous tweets
                unknown_words_scores[word] = 0
                unknown_words_count[word] = 0

    # Updating the sentiment scores of each unknown word
    for word in to_be_added:
        unknown_words_scores[word] = unknown_words_scores[word] + sentiment_score
        unknown_words_count[word] = unknown_words_count[word] + 1
    

def main():
    sent_file = open(sys.argv[1])
    tweet_file = open(sys.argv[2])

    # Creating dictionary of words and their sentiment values
    sentiment_scores = {}
    for line in sent_file:
        word, score = line.split("\t")
        sentiment_scores[word] = int(score)


    for line in tweet_file:
        parsed_tweet = json.loads(line)
        if parsed_tweet.has_key("text"):
            tweet = parsed_tweet["text"]
            calculate_sentiment(tweet, sentiment_scores)
            
    for unknown_word in unknown_words_scores:
        print unknown_word, " ", float(unknown_words_scores[unknown_word] / unknown_words_count[unknown_word])

if __name__ == '__main__':
    main()
