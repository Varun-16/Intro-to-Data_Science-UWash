import sys
import json

word_count = {}

def find_total_count():
    total = 0
    for word in word_count:
        total = total + word_count[word]
    return total

def frequency():
    total_count = find_total_count()
    for word in word_count:
        print word, " ", "%.3f" % (word_count[word] / total_count)

def count(tweet):
    tweet = tweet.encode('utf-8')
    tweet = tweet.lower()
    tweet_words = tweet.split(" ")

    for word in tweet_words:
        word = word.strip()
        if not word_count.has_key(word):
            word_count[word] = 1
        else:
            word_count[word] = word_count[word] + 1

def main():
    tweet_file = open(sys.argv[1])
    for line in tweet_file:
        parsed_tweet = json.loads(line)
        if parsed_tweet.has_key('text'):
            tweet = parsed_tweet["text"]
            count(tweet)
    frequency()

if __name__ == '__main__':
    main()
