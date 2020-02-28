# redditbot
Reddit bot for searching subreddits and returning information on relevant posts.

## Installation

Create a Reddit script application [here](https://www.reddit.com/prefs/apps) and copy your login information to the *praw.ini* file stored in the project directory (this is what the Reddit API will use to authenticate your account).
```bash
[DEFAULT]
client_id = CLIENT_ID
client_secret = CLIENT_SECRET
user_agent = USER_AGENT
username = USERNAME
password = PASSWORD
```

Use Git to clone repository & run script from working directory:
```bash
git clone https://github.com/colin-gall/redditbot

cd redditbot

python3 redditbot.py
```

## Usage

Run the script from the command line and choose your subreddit of choice:
```bash
python3 redditbot -s worldnews
```

Additionally, change the number of posts to return or add keyword filters:
```bash
python3 redditbot -s worldnews -l 500 -k politics
```
