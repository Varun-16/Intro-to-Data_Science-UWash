import sys
import json
import operator

def main():
    hashtags_list = {}
    tweet_file = open(sys.argv[1])

    for line in tweet_file:
        
        parsed_tweet = json.loads(line)
        if parsed_tweet.has_key("entities"):
            ent = parsed_tweet["entities"]
            hashtags = ent["hashtags"]
            
            if len(hashtags) != 0:
                hash_text = hashtags[0]["text"]
                hash_text = hash_text.encode('utf-8')
                hash_text = hash_text.lower()
                if hashtags_list.has_key(hash_text):
                    hashtags_list[hash_text] = hashtags_list[hash_text] + 1
                else:
                    hashtags_list[hash_text] = 1

    for i in range(0, 10):
        max_hashtag = max(hashtags_list.iteritems(), key = operator.itemgetter(1))[0]
        print max_hashtag, " ", hashtags_list[max_hashtag]
        hashtags_list.pop(max_hashtag, None)
if __name__ == '__main__':
    main()
