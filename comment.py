import praw
import requests
from apscheduler.schedulers.background import BackgroundScheduler
import logging
import datetime
import time

# Logging setup
logging.basicConfig(level=logging.INFO)

# Reddit API credentials
REDDIT_CLIENT_ID = ''
REDDIT_CLIENT_SECRET = ''
REDDIT_USERNAME = ''
REDDIT_PASSWORD = ''
REDDIT_USER_AGENT = ''

# Groq API credentials
GROQ_API_URL = 'https://api.groq.com/openai/v1/chat/completions'
GROQ_API_KEY = ''
MODEL = 'llama3-8b-8192'

# Reddit API initialization
reddit = praw.Reddit(
    client_id=REDDIT_CLIENT_ID,
    client_secret=REDDIT_CLIENT_SECRET,
    username=REDDIT_USERNAME,
    password=REDDIT_PASSWORD,
    user_agent=REDDIT_USER_AGENT
)

# Background scheduler setup
scheduler = BackgroundScheduler()
scheduler.start()

def generate_comment(post_content):
    """
    Generates a comment using the Groq API based on the Reddit post content.
    """
    headers = {
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {GROQ_API_KEY}'
    }

    # Modify the prompt to generate the comment directly without unnecessary prefixes
    prompt = f"Please write a thoughtful and relevant comment on the following Reddit post:\n{post_content}"

    payload = {
        'model': MODEL,
        'messages': [{'role': 'user', 'content': prompt}]
    }

    try:
        response = requests.post(GROQ_API_URL, json=payload, headers=headers)
        response.raise_for_status()  # Raise exception for bad responses (4xx, 5xx)
        
        data = response.json()
        
        # Extract the generated comment from the response
        comment = data.get('choices', [{}])[0].get('message', {}).get('content', '').strip()
        
        if not comment:  # If comment is empty or invalid
            logging.warning("Generated comment is empty or invalid.")
            return None
        
        logging.info(f"Generated comment: {comment}")
        return comment
    except requests.exceptions.RequestException as e:
        logging.error(f"Error generating comment from Groq: {e}")
        return None

def comment_on_posts(subreddit_name):
    """
    Fetches recent posts from a specified subreddit and comments on them.
    """
    try:
        # Fetch posts from subreddit
        subreddit = reddit.subreddit(subreddit_name)
        posts = subreddit.new(limit=2)  # Fetch the 2 latest posts
        
        for post in posts:
            logging.info(f"Found post: {post.title} (ID: {post.id})")
            
            # Generate a comment for each post
            comment = generate_comment(post.title + " " + post.selftext)
            
            if comment:
                # Post the comment to the post
                post.reply(comment)
                logging.info(f"Posted comment: {comment} to post: {post.title}")
                
    except praw.exceptions.APIException as e:
        logging.error(f"Error commenting on posts: {e}")

def schedule_commenting(subreddit_name, post_time):
    """
    Schedules a comment job for a subreddit at the specified time.
    """
    try:
        # Convert post_time to datetime
        post_time = datetime.datetime.strptime(post_time, '%Y-%m-%dT%H:%M')
        
        scheduler.add_job(
            comment_on_posts,
            'date',
            run_date=post_time,
            args=[subreddit_name]  # Pass subreddit name
        )
        
        logging.info(f"Commenting job scheduled for {post_time.strftime('%Y-%m-%d %H:%M')} in r/{subreddit_name}")
    except ValueError:
        logging.error(f"Invalid date format: {post_time}")
        return

# Keep the script running and allow the scheduler to keep working
if __name__ == '__main__':
    try:
        # Example: Schedule commenting for 'technology' subreddit at a specified time
        schedule_commenting('technology', '2025-01-17T15:03')  # Set the time and subreddit
        
        # Run the scheduler in the background and keep the main thread alive
        logging.info("Scheduler is running. Press Ctrl+C to stop.")
        
        # Instead of using while True, use time.sleep to keep the process alive
        while True:
            time.sleep(10)  # Sleep for 10 seconds to keep the script running and responsive to scheduled jobs
        
    except KeyboardInterrupt:
        # Gracefully shutdown scheduler on interrupt
        scheduler.shutdown()
        logging.info("Scheduler shut down.")
