import sys
import json

def calculate_sentiment(tweet, scores):
    tweet = tweet.encode('utf-8')
    words_in_tweet = tweet.split(" ")
    sentiment_score = 0
    for word in words_in_tweet:
        if scores.has_key(word):
            sentiment_score = sentiment_score + scores[word]

    return sentiment_score

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
            print calculate_sentiment(tweet, sentiment_scores)

if __name__ == '__main__':
    main()
