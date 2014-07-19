import sys
import json
import re
import operator

locationData = {
        "AK":[61.3850,-152.2683],
        "AL":[32.7990,-86.8073],
        "AR":[34.9513,-92.3809],
        "AS":[14.2417,-170.7197],
        "AZ":[33.7712,-111.3877],
        "CA":[36.1700,-119.7462],
        "CO":[39.0646,-105.3272],
        "CT":[41.5834,-72.7622],
        "DC":[38.8964,-77.0262],
        "DE":[39.3498,-75.5148],
        "FL":[27.8333,-81.7170],
        "GA":[32.9866,-83.6487],
        "HI":[21.1098,-157.5311],
        "IA":[42.0046,-93.2140],
        "ID":[44.2394,-114.5103],
        "IL":[40.3363,-89.0022],
        "IN":[39.8647,-86.2604],
        "KS":[38.5111,-96.8005],
        "KY":[37.6690,-84.6514],
        "LA":[31.1801,-91.8749],
        "MA":[42.2373,-71.5314],
        "MD":[39.0724,-76.7902],
        "ME":[44.6074,-69.3977],
        "MI":[43.3504,-84.5603],
        "MN":[45.7326,-93.9196],
        "MO":[38.4623,-92.3020],
        "MP":[14.8058,145.5505],
        "MS":[32.7673,-89.6812],
        "MT":[46.9048,-110.3261],
        "NC":[35.6411,-79.8431],
        "ND":[47.5362,-99.7930],
        "NE":[41.1289,-98.2883],
        "NH":[43.4108,-71.5653],
        "NJ":[40.3140,-74.5089],
        "NM":[34.8375,-106.2371],
        "NV":[38.4199,-117.1219],
        "NY":[42.1497,-74.9384],
        "OH":[40.3736,-82.7755],
        "OK":[35.5376,-96.9247],
        "OR":[44.5672,-122.1269],
        "PA":[40.5773,-77.2640],
        "PR":[18.2766,-66.3350],
        "RI":[41.6772,-71.5101],
        "SC":[33.8191,-80.9066],
        "SD":[44.2853,-99.4632],
        "TN":[35.7449,-86.7489],
        "TX":[31.1060,-97.6475],
        "UT":[40.1135,-111.8535],
        "VA":[37.7680,-78.2057],
        "VI":[18.0001,-64.8199],
        "VT":[44.0407,-72.7093],
        "WA":[47.3917,-121.5708],
        "WI":[44.2563,-89.6385],
        "WV":[38.4680,-80.9696],
        "WY":[42.7475,-107.2085]
}

states = {
        'AK': 'Alaska',
        'AL': 'Alabama',
        'AR': 'Arkansas',
        'AS': 'American Samoa',
        'AZ': 'Arizona',
        'CA': 'California',
        'CO': 'Colorado',
        'CT': 'Connecticut',
        'DC': 'District of Columbia',
        'DE': 'Delaware',
        'FL': 'Florida',
        'GA': 'Georgia',
        'GU': 'Guam',
        'HI': 'Hawaii',
        'IA': 'Iowa',
        'ID': 'Idaho',
        'IL': 'Illinois',
        'IN': 'Indiana',
        'KS': 'Kansas',
        'KY': 'Kentucky',
        'LA': 'Louisiana',
        'MA': 'Massachusetts',
        'MD': 'Maryland',
        'ME': 'Maine',
        'MI': 'Michigan',
        'MN': 'Minnesota',
        'MO': 'Missouri',
        'MP': 'Northern Mariana Islands',
        'MS': 'Mississippi',
        'MT': 'Montana',
        'NA': 'National',
        'NC': 'North Carolina',
        'ND': 'North Dakota',
        'NE': 'Nebraska',
        'NH': 'New Hampshire',
        'NJ': 'New Jersey',
        'NM': 'New Mexico',
        'NV': 'Nevada',
        'NY': 'New York',
        'OH': 'Ohio',
        'OK': 'Oklahoma',
        'OR': 'Oregon',
        'PA': 'Pennsylvania',
        'PR': 'Puerto Rico',
        'RI': 'Rhode Island',
        'SC': 'South Carolina',
        'SD': 'South Dakota',
        'TN': 'Tennessee',
        'TX': 'Texas',
        'UT': 'Utah',
        'VA': 'Virginia',
        'VI': 'Virgin Islands',
        'VT': 'Vermont',
        'WA': 'Washington',
        'WI': 'Wisconsin',
        'WV': 'West Virginia',
        'WY': 'Wyoming'
}

def findStateFromCoordinates(lat, lon):
    flag = 0
    for loc in locationData:
        if flag == 0:
            spot = loc
            minDiff = abs(locationData[loc][0] - lat) + abs(locationData[loc][1] - lon)
            flag = 1
        else:
            diff = abs(locationData[loc][0] - lat) + abs(locationData[loc][1] - lon)
            if diff < minDiff:
                minDiff = diff
                spot = loc

    return spot

def getStateFromLocation(loc):
    searchObj = re.search( r'\w*', loc, flags=0)
    loc_present = searchObj.group()
    loc_present = loc_present.lower()

    for s in states:
        if loc_present.find(states[s].lower()):
            return s
    return 0

def getState(parsed_tweet):
    state = 0
    flag = 0
    # Working out the location with coordinates
    if parsed_tweet.has_key("coordinates"):
        coord = parsed_tweet["coordinates"]
        if coord != None:
            long_lat = coord["coordinates"]
            longitude = long_lat[0]
            latitude = long_lat[1]
            if latitude >= 14 and latitude <= 62:   # US location
                state = findStateFromCoordinates(latitude, longitude)
                flag = 1

    # Working out location with "user" tag
    if flag == 0 and parsed_tweet.has_key("user"):
        user_data = parsed_tweet["user"]
        if user_data != None:
            loc = user_data["location"]
            if loc != None:
                state = getStateFromLocation(loc)
    
    return state

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
    state_scores = {}

    for s in locationData:
        state_scores[s] = 0

    # Creating dictionary of words and their sentiment values
    sentiment_scores = {}
    for line in sent_file:
        word, score = line.split("\t")
        sentiment_scores[word] = int(score)


    for line in tweet_file:
        parsed_tweet = json.loads(line)
        if parsed_tweet.has_key("text"):
            tweet = parsed_tweet["text"]
            tweet_score = calculate_sentiment(tweet, sentiment_scores)
            state = getState(parsed_tweet)
            if state != 0:
                state_scores[state] = state_scores[state] + tweet_score

    happy_state = max(state_scores.iteritems(), key = operator.itemgetter(1))[0]
    print happy_state

if __name__ == '__main__':
    main()
