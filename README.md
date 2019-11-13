# Fantasy Football Player Predictions

This is my capstone project for the Udacity Machine Learning Engineer Nanodegree. We will attempt to predict fantasy point output for Tom Brady and LeSean McCoy during the 2012 NFL season using data from their 2010 and 2011 seasons.

Specifically, we have two goals:

1. Build an LSTM RNN using football, betting, and weather data that significantly improves upon performance attained from a simple moving-average approach.
2. Prove the value of Twitter volume and sentiment features by incorporating them into the LSTM model and improving performance.

We start with raw data on player performance, game location and conditions, and defensive performance. To this, we add a dataset obtained from Sinha, et. al. of NFL-related tweets sent during the 2010, 2011 and 2012 seasons. These tweets do not contain text, per Twitter's terms of service, so we include here a script to retrieve the text. 

Further, we use Stanford Core NLP to perform sentiment analysis on the tweets. See setup instructions below.

## Setup
#### Environment
To install required packages, simply create a Python 3 virtual environment and run the notebook 00_install_requirements.ipynb in the modeling_notebooks folder.

#### Twitter API
To retrieve Twitter data (notebook 01_pull_data.ipynb) you will need Twitter API credentials. Go to [Twitter's developer page](https://developer.twitter.com/) and apply for API access. Once you are granted access, save your API key, API secret, access token, and access token secret as environment variables respectively named TWITTER_API_KEY, TWITTER_API_SECRET, TWITTER_API_ACCESS_TOKEN, and TWITTER_API_ACCESS_SECRET

#### Stanford Core NLP
You must set up a Core NLP server on the machine you plan to run the scripts on in order to perform sentiment analysis of the tweets (notebook 05_sentiment_analysis). To do so, first download the English version [on Core NLP's GitHub page](https://stanfordnlp.github.io/CoreNLP/). Unzip the file, navigate to the resultant folder in a Terminal window, and run the command: 

`!java -mx5g -cp "*" edu.stanford.nlp.pipeline.StanfordCoreNLPServer -timeout 10000`

to start the server.

## Structure

#### modeling_notebooks
This is the main folder containing the full machine learning workflow. Notebooks are meant to be run sequentially to reproduce my results.

#### data_compilation
Contains two scripts: one to retrieve defensive stats using the sportsreference Python package and one to retrieve tweet text from IDs. We call both of them in modeling_notebooks/01_pull_data.ipynb.

#### data
Contains four folders:

- data_raw: contains all raw data gathered for project before cleaning or aggregation.
- data_modified: contains all cleaned data, written in modeling_notebooks 02 - 05.
- data_final: contains all features, produced by notebook 07.
- appendix_2018_naive: contains data to apply naive moving-average approach to 2018 season, for reference.
- predictions_output: contains pickled files with predictions and metrics from various models. Produced in notebooks 10 - 14.

#### plots
- Contains an exploratory visualization for the Twitter data and correlation plots for all features versus the target.

#### sentiment_analysis_validation
- Contains two notebooks exploring the efficacy of sentiment analysis by TextBlob and Stanford Core NLP.

Note: for these notebooks to work, the user will need to manually create a set of tweets with hand-labeled sentiment. File not included to comply with Twitter terms of service.







