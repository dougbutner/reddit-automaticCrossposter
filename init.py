import praw
import random
import time
from praw.exceptions import APIException
from keys import keys
from config import config

# REST API connection for two accounts
reddit = praw.Reddit(client_id=keys['client_id'],
                     client_secret=keys['client_secret'],
                     user_agent=keys['user_agent'],
                     username=keys['username'],
                     password=keys['password'])

reddit2 = praw.Reddit(client_id=keys['client_id2'],
                      client_secret=keys['client_secret2'],
                      user_agent=keys['user_agent'],
                      username=keys['username2'],
                      password=keys['password2'])

f = open('copiedPostIds.txt', 'r')
postedIds = f.read().lower().splitlines()
f.close()

def crosspost_submission(submission, subreddit_list, reddit_instance):
    for subreddit in subreddit_list:
        try:
            submission.crosspost(subreddit, title=submission.title, send_replies=True)
            print(f"Crossposted to {subreddit} using {reddit_instance.user.me()} \n\t" + submission.title)
        except APIException as e:
            if "CROSSPOST" in str(e):
                print(f"Guda, remove the subreddit: {subreddit}")
            else:
                print(f"Failed to crosspost to {subreddit} due to {e}")
        sleep_time = random.randint(5, 12)
        print(f"Sleeping for {sleep_time} seconds")
        time.sleep(sleep_time)

for submission in reddit.subreddit(config['fromSub']).stream.submissions():
    if submission.id not in postedIds:
        matched_subs = []
        for key, subreddits in config['matchSubreddits'].items():
            if key in submission.title:
                matched_subs = subreddits
                break
        if not matched_subs:
            matched_subs = config["matchSubreddits"]["default"]
        
        f = open('copiedPostIds.txt', 'a+')
        f.write(str(submission.id) + '\n')
        f.close()
        postedIds.append(str(submission.id))
        
        reddit_accounts = [reddit2, reddit2] # TODO CHANGE THIS BACK 
        random.shuffle(reddit_accounts)
        
        for chosen_account in reddit_accounts:
            crosspost_submission(submission, matched_subs, chosen_account)
            break
        
        break
