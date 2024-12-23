import praw
from keys import keys

def test_reddit_instance(instance_name, reddit):
    try:
        user = reddit.user.me()
        print(f"{instance_name} authentication successful!")
        print(f"Logged in as: {user.name}")
        return True
    except Exception as e:
        print(f"{instance_name} authentication failed!")
        print(f"Error: {str(e)}")
        return False

# Test first account
reddit = praw.Reddit(
    client_id=keys['client_id'],
    client_secret=keys['client_secret'],
    user_agent="TestScript/1.0",  # Use a simple user agent for testing
    username=keys['username'],
    password=keys['password']
)

# Test authentication
test_reddit_instance("First account", reddit)

# Test second account if needed
reddit2 = praw.Reddit(
    client_id=keys['client_id2'],
    client_secret=keys['client_secret2'],
    user_agent="TestScript/1.0",  # Use a simple user agent for testing
    username=keys['username2'],
    password=keys['password2']
)

test_reddit_instance("Second account", reddit2)