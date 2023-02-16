from textblob import TextBlob

#this program takes a string and returns support
#oppose, or neutral depending on its sentiment

#def sentimentAnalysis(text):

text = """I oppose the proposed Section 301 action imposing new tariffs.  American families and small businesses are still struggling to make ends meet, and we cant afford new tariffs taxes and higher prices.
"""

data = TextBlob(text)
polarity = data.sentiment.polarity
print("polarity: ", polarity)
