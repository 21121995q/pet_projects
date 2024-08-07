![image](https://github.com/21121995q/pet_projects/assets/141146413/a0212c20-bb13-464c-8350-a519b743491f)

This project explores the capabilities of large language models (LLMs) for code generation, focusing on sentiment analysis of YouTube comments. By integrating various sentiment analysis models and the YouTube Data API, this web application analyzes the most liked comments on YouTube videos related to a user-specified topic.

During development, I experimented with several LLMs to assist in writing code and found Gpt's Code Copilot to be the most responsive and effective for generating substantial code snippets. This project demonstrates the potential of using LLMs to streamline development processes and achieve robust results.

In this project, an ensemble of models is employed for semantic analysis of the most relevant YouTube comments on a chosen topic, aiming to study the representation that can be formed based on the most popular comments.

The final prompt is attached in the file 'prompt.txt'.

# Key Features

1.User-Friendly Interface:
- A web page with a central search window where users can input their topic of interest.
- Displays video titles, the number of likes, top 5 relevant comments, the number of likes for each comment, and the sentiment analysis results (Positive, Neutral, Negative) from three different models.

2.YouTube API Integration:
- Fetches the most popular videos related to the specified topic using the YouTube Data API v3.
- Extracts the top 5 most relevant comments for each video.
- Handles potential issues gracefully by skipping videos if comments or likes cannot be retrieved.
  
3.Advanced Sentiment Analysis:
- Utilizes three sentiment analysis models for robust evaluation:
        cardiffnlp/twitter-roberta-base-sentiment
        siebert/sentiment-roberta-large-english
        sbcBI/sentiment_analysis_model
- Displays the sentiment evaluation and scores from each model under each comment.
  
Technology Stack
Frontend: HTML, CSS, JavaScript
Backend: Python, Flask
APIs: YouTube Data API v3
Libraries: Hugging Face transformers for sentiment analysis

# Getting Started

insert your YouTube Data API key into the app.py file.
