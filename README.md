
# Reddit Post Scheduler

This project allows you to schedule posts to be made to Reddit subreddits at a specific time. Additionally, it uses the Groq API to generate content for these posts and comments on recent Reddit posts based on the provided topic.

## Features:
- Schedule posts to Reddit subreddits at a specific time.
- Automatically generate content for the posts using the Groq API.
- Generate and post thoughtful comments on recent Reddit posts.
- Use of Flask for the web interface and APScheduler for task scheduling.

## Prerequisites:

Before you begin, ensure you have met the following requirements:

- **Python** version 3.7 or higher
- **pip** (Python package installer) installed
- **Flask**, **APScheduler**, and other dependencies installed

## Setup Instructions:

### 1. Clone the Repository
First, clone this repository to your local machine:
```bash
git clone https://github.com/VARKALASAIVIGNESH/SYNKRIT-TASK.git
cd SYNKRIT-TASK
```

### 2. Create a Virtual Environment
It’s highly recommended to use a virtual environment to manage your Python packages. To create a virtual environment, run:

```bash
python -m venv venv
```

### 3. Activate the Virtual Environment
- On **Windows**, run:
```bash
.\venv\Scripts\activate
```
- On **Mac/Linux**, run:
```bash
source venv/bin/activate
```

### 4. Install the Required Dependencies
Install the necessary Python packages by running:
```bash
pip install -r requirements.txt
```

### 5. Set Up Environment Variables
You will need to set up environment variables for the Reddit API and Groq API credentials to interact with the APIs.

#### Create a `.env` file and add the following variables:
```bash
REDDIT_CLIENT_ID=your_reddit_client_id
REDDIT_CLIENT_SECRET=your_reddit_client_secret
REDDIT_USERNAME=your_reddit_username
REDDIT_PASSWORD=your_reddit_password
REDDIT_USER_AGENT=your_reddit_user_agent

GROQ_API_URL=your_groq_api_url
GROQ_API_KEY=your_groq_api_key
MODEL=your_model_name
```

### 6. Run the Application
Now that your environment is set up, you can run the Flask app using:
```bash
python app.py
```

The Flask server will start running on `http://127.0.0.1:5000/`.

### 7. Access the Web Interface
Open a web browser and navigate to `http://127.0.0.1:5000/`. You should see a simple form where you can:
- Enter the **topic** for your Reddit post.
- Enter the **subreddit** where you want to post.
- Choose the **time** when the post should be made.

### 8. Schedule a Post
Fill out the form with the necessary details and click **Schedule Post**. This will:
- Validate your input.
- Schedule the Reddit post using APScheduler.

### 9. View Logs and Debugging
You can view logs in the terminal to see the status of your scheduled posts, successful submissions to Reddit, and any errors encountered.

## Code Walkthrough

### `app.py`
This is the main entry point of the application. It runs the Flask web server and handles requests to schedule posts.
- **Flask Setup:** Configures routes for the web interface and form submission (`/generate_post`).
- **Job Scheduling:** Uses **APScheduler** to schedule tasks based on the user input (post time).
- **Groq API Integration:** Calls the Groq API to generate post content, removing any unwanted "Edit" section.

### `comment.py`
This script is responsible for generating comments for Reddit posts.
- **Post Comment Generation:** It uses the Groq API to generate thoughtful comments for recent Reddit posts.
- **Scheduler:** APScheduler is used to schedule comments on Reddit at specific times.
- **Reddit Interaction:** It uses the **PRAW** library to interact with Reddit, fetching recent posts and posting generated comments.

### `index1.html`
This file contains the front-end user interface:
- A simple HTML form where the user can input the **topic**, **subreddit**, and **post time**.
- The form submits data to the Flask backend, which processes the input and schedules the Reddit post.

### Dependencies

This project relies on the following libraries:

- **Flask** - For the web framework.
- **APScheduler** - For scheduling tasks (posting at a specific time).
- **PRA**W - For interacting with the Reddit API.
- **requests** - For making HTTP requests to the Groq API.

To install these dependencies, run the following:
```bash
pip install flask apscheduler praw requests
```

## Troubleshooting

If you encounter any issues:

- **Reddit API Errors:** Check your Reddit API credentials and ensure they are correctly set in the `.env` file.
- **Groq API Errors:** Make sure your Groq API key is valid and set in the `.env` file.
- **Invalid Date Format:** Ensure that the date format used for scheduling posts is correct (`YYYY-MM-DDTHH:MM`).

## Contributing

1. Fork the repository.
2. Create a new branch (`git checkout -b feature-branch`).
3. Commit your changes (`git commit -m 'Add feature'`).
4. Push to the branch (`git push origin feature-branch`).
5. Create a pull request.

##OUTPUTS

![WhatsApp Image 2025-01-17 at 14 23 41_9f18168f](https://github.com/user-attachments/assets/3790b577-26ec-4393-b55e-1a54dbb598be)


## License

This project is open-source and available under the [MIT License](LICENSE).

---

## Note:

Replace `your_reddit_*` and `your_groq_*` with your actual API credentials in the `.env` file. This is important for secure access to your Reddit and Groq accounts.

---

This README will provide others with a clear understanding of how to set up, run, and extend your Reddit Post Scheduler app. Let me know if you need any more details!
