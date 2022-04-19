import pickle
import pandas as pd

def recommend(username):
    df_sentiment = pd.read_csv('./data/df_sentiment.csv')
    product_review = pd.read_csv('./data/sample30.csv')
    user_recommendation = open('./data/user_recommendation.pkl', 'rb')
    user_recommendation_table = pickle.load(user_recommendation)
    tfidf_vectorizer = open('./data/tfidf_vectorizer.pkl', 'rb')
    tfidf_vector = pickle.load(tfidf_vectorizer)
    sentiment_model = open('./data/Sentiment_model.pkl', 'rb')
    sentiment_model_load = pickle.load(sentiment_model)
    list_final = [[]]

    if username in user_recommendation_table.index:
        top20_product_ids = user_recommendation_table.loc[username].sort_values(ascending=False)[:20]
        product_mapping = pd.DataFrame(product_review[['id', 'name']]).drop_duplicates()
        top20_products = pd.merge(top20_product_ids, product_mapping, on='name')

        product_review_mapping = pd.DataFrame(
            df_sentiment[['name', 'reviews_full_text', 'user_sentiment']]).drop_duplicates()
        product_review_data = pd.merge(top20_products, product_review_mapping, on='name')

        test_data = tfidf_vector.transform(product_review_data['reviews_full_text'])

        product_review_data['predicted_sentiment'] = sentiment_model_load.predict(test_data)
        product_review_data['predicted_sentiment_score'] = product_review_data['predicted_sentiment'].replace(['negative', 'positive'], [0, 1])
        product_pivot = product_review_data.reset_index().pivot_table(values='predicted_sentiment_score', index='name',aggfunc='mean')
        product_pivot.sort_values(by='predicted_sentiment_score', inplace=True, ascending=False)
        list_final = [[index, out] for index, out in enumerate(product_pivot.head(5).index, 1)]
        text_info = "Hello \"" + username + "\", Below are the top 5 recommendations for you"
    else:
        text_info = "Please enter a valid user!!!"

    return text_info, list_final