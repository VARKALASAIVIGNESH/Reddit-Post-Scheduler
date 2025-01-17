from flask import Flask, render_template, request, jsonify
import requests
import praw
from apscheduler.schedulers.background import BackgroundScheduler
import datetime
import logging

# Flask app setup
app = Flask(__name__)

# Logging setup
logging.basicConfig(level=logging.INFO)

# Reddit API credentials
REDDIT_CLIENT_ID = 'nj1BLntGQjbUs8z4U-cTrg'
REDDIT_CLIENT_SECRET = '2B5qe6hR2rPsC4XYTflZQIV29OkIag'
REDDIT_USERNAME = 'Feisty-Shelter9567'
REDDIT_PASSWORD = '55724@28'
REDDIT_USER_AGENT = 'Reddit AI Bot by Feisty-Shelter9567'

# Groq API credentials
GROQ_API_URL = 'https://api.groq.com/openai/v1/chat/completions'
GROQ_API_KEY = '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'
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

# Flask Routes
@app.route('/')
def index():
    return render_template('index1.html')

@app.route('/generate_post', methods=['POST'])
def generate_post():
    # Get form data
    user_input = request.form.get('topic')
    subreddit = request.form.get('subreddit')
    post_time = request.form.get('post_time')

    # Log received data for debugging
    logging.info(f"Received data: topic={user_input}, subreddit={subreddit}, post_time={post_time}")

    # Check if any field is missing
    if not user_input or not subreddit or not post_time:
        logging.error("Missing data: topic, subreddit, or post_time is empty")
        return jsonify({'error': 'All fields are required.'}), 400

    try:
        # Convert post_time from string to datetime object
        post_time = datetime.datetime.strptime(post_time, '%Y-%m-%dT%H:%M')
    except ValueError:
        logging.error(f"Invalid date format: {post_time}")
        return jsonify({'error': 'Invalid date format. Use YYYY-MM-DDTHH:MM.'}), 400

    # Schedule post
    scheduler.add_job(
        post_to_reddit,
        'date',
        run_date=post_time,
        args=[user_input, subreddit]  # Pass both topic and subreddit
    )

    return jsonify({'message': f'Post scheduled successfully for {post_time.strftime("%Y-%m-%d %H:%M")}!'})

def post_to_reddit(topic, subreddit):
    logging.info(f"Generating content for topic: {topic}")
    headers = {
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {GROQ_API_KEY}'
    }

    payload = {
        'model': MODEL,
        'messages': [{'role': 'user', 'content': f"Generate a Reddit post about {topic}."}]
    }

    try:
        # Generate content using Groq API
        response = requests.post(GROQ_API_URL, json=payload, headers=headers)
        response.raise_for_status()

        data = response.json()
        content = data['choices'][0]['message']['content']
        logging.info(f"Generated content: {content}")

        # Clean up content (if needed) to remove "Edit" section
        # Check for "Edit" in content and remove if it exists
        if "Edit:" in content:
            content = content.split("Edit:")[0].strip()
            logging.info("Removed 'Edit' section from content.")

        # Submit post to subreddit
        subreddit_instance = reddit.subreddit(subreddit)

        # Check subreddit rules
        submission_type = subreddit_instance.submission_type
        logging.info(f"Subreddit r/{subreddit} allows: {submission_type}")

        if submission_type in ['self', 'any']:
            # Submit as a text post (self-post)
            submission = subreddit_instance.submit(title=f"Discussion about {topic}", selftext=content)
            logging.info(f"Text post successfully submitted to r/{subreddit}")

            # Handle flair if required
            try:
                flairs = list(subreddit_instance.flair.link_templates)
                if flairs:
                    default_flair = flairs[0]  # Select the first available flair
                    submission.flair.select(default_flair['id'])
                    logging.info(f"Flair applied: {default_flair['text']}")
                else:
                    logging.info("No available flairs for the subreddit.")
            except praw.exceptions.APIException as flair_error:
                logging.warning(f"Flair selection error: {flair_error}")
        else:
            logging.error(f"Subreddit r/{subreddit} does not allow posts.")
            return

    except requests.exceptions.RequestException as e:
        logging.error(f"Error generating content from Groq: {e}")
    except praw.exceptions.APIException as e:
        logging.error(f"Error posting to Reddit: {e}")

if __name__ == '__main__':
    try:
        app.run(debug=True)
    except KeyboardInterrupt:
        scheduler.shutdown()
        logging.info("Scheduler shut down.")
