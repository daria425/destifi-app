search_instructions="""Given the following stock, use the bing tool to provide a summary of the latest sentiment analysis, key financial news, and potential market-moving events. 
- Ensure insights are clear, concise, and useful for investors. 
- Use the bing tool to ensure information is up to date.
- Provide as much detail as possible on sentiment and reasons for the sentiment,
- include a sentiment score of -1 to 1 and sentiment category (Bullish, Neutral, Bearish), 
 -include key financial news topics, and news volume (specific number of mentions in articles or social media)."""

extract_instructions="""Analyze the following stock sentiment paragraph and extract structured information, 
        including the stock symbol, overall sentiment score (-1 to 1), sentiment category (Bullish, Neutral, Bearish), key financial news topics, news volume (number of mentions in articles or social media). 
        Ensure the extracted data is well-structured and suitable for quantitative analysis."""