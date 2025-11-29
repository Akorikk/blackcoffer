# blackcoffer
# Blackcoffer_Assignment

** please delete the output.xlsx and run the main file blackcoffer_assignment.py but befor that activate the env name black conda activate black i have create with python 3.9

# Overview 
This project is an end-to-end Text Extraction and NLP Analysis Pipeline, built as part of the Blackcoffer Data Scientist assignment.
The objective of the project is to:
Extract article text from a list of URLs
Clean and preprocess the raw text
Compute 13 linguistic & sentiment metrics defined in the assignment
Generate the final structured output as Output.xlsx
The solution is implemented entirely in Python, using BeautifulSoup, pandas, and NLTK.

# WorkFlow 
The project executes in five major stages
1. Load Input and Dictionaries
2. Web Scraping
3. Text Cleaning & Preprocessing
4. NLP Metric Computation
5. Export Final Output

* Loading Input, Stopwords & Master Dictionary
* Web Scraping with BeautifulSoup
* Text Cleaning & Preprocessing
* NLP Metric Computation
 i compute 13 metrics as required by Blackcoffer assignment, Positive & Negative Score, Polarity Score, Subjectivity Score, Readability Metrics (Average Sentence Length), Complex Word Count & Percentage
* Generating Output.xlsx



This project demonstrates the full workflow required for Blackcoffer’s text analysis assignment—from data ingestion and extraction all the way to NLP-driven scoring and final reporting.
The implementation is efficient, scalable, and easy to extend.If needed, the codebase can be expanded to include Error loggingMulti-threaded scraping Pipeline automation Enhanced preprocessing