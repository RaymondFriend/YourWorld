from newsapi import NewsApiClient

# Init
newsapi = NewsApiClient(api_key="e2f29d109cf04ff987e713b82d7539c8")

# /v2/top-headlines
# top_headlines = newsapi.get_top_headlines(q='bitcoin',
#                                           category='business',
#                                           language='en')

# print("Top Headlines about Bitcoin in Business")
# for headline in top_headlines:
#     print(f"next headline: {headline}")


# /v2/everything
all_articles = newsapi.get_everything(q='United States',
                                      sources='bbc-news',
                                      domains='bbc.co.uk',
                                      from_param='2023-12-07',
                                      to='2024-01-06',
                                      language='en',
                                      sort_by='relevancy',
                                      page=2)

print(f"all_articles keys {all_articles.keys()}")
print(f"all_articles status {all_articles['status']}")
print(f"all_articles totalResults {all_articles['totalResults']}")
print(f"all_articles.articles length {len(all_articles['articles'])}")
# print(f"all_articles articles {all_articles['articles']}")

i = 0
for article in all_articles['articles']:
    if(i < 10):
        print(f"article type {type(article)}")
        print(f"article keys {article.keys()}")
        print(article['title'], "-", article['url'])
    else:
        break
    i += 1
    

# print("All articles in the last month about bitcoin from certain sources.")
# for article in all_articles:
#     print(f"next article: {article}")

# # /v2/top-headlines/sources
# sources = newsapi.get_sources()

# for source in sources:
#     print(f"next source {source}")

def unpack_article(article):

    return ""