from summarizer.summary_chatgpt_api_generator import SummaryChatGPTAPIGenerator
from connector.db_connector import Database
import logging
import datetime
import time

def store_summaries_to_db():
    db = Database()
    db.connect()

    # prepare for logging
    logging.basicConfig(level=logging.ERROR)
    logger = logging.getLogger(__name__)

    # prepare only three articles without summary
    # for generating summaries with minute pause
    # reason: GPT sent "429 error" after more than 3 articles per minute for free account
    articles = get_articles_without_summary(db, logger, 3)
        
    while len(articles) > 0:
        generate_and_store_articles(db, articles, logger)
        time.sleep(60)
        articles = get_articles_without_summary(db, logger, 3)
    
    db.close()   

def get_articles_without_summary(db, logger, limit=0):
      
    ''' 
    Calculate list of articles for summary generation 
    :param db: database
    :param logger: logger to save exceptions catching
    :param limit: limitation for loading in a reason of chatGPT limitations for free account (limit=0 - without limitations)
    :return: list of articles for summarization
    '''

    if limit == 0:
        sql = f'''SELECT DISTINCT Articles.id, content
            FROM Articles
            LEFT JOIN Summaries ON Articles.id = Summaries.article_id 
            WHERE summary IS NULL OR NOT EXISTS
            (SELECT is_bad
            FROM Summaries
            WHERE is_bad IS NULL AND Articles.id = Summaries.article_id)'''
    else:
        sql = f'''SELECT DISTINCT Articles.id, content
            FROM Articles
            LEFT JOIN Summaries ON Articles.id = Summaries.article_id 
            WHERE summary IS NULL OR NOT EXISTS
            (SELECT is_bad
            FROM Summaries
            WHERE is_bad IS NULL AND Articles.id = Summaries.article_id)
            LIMIT {limit}'''

    try:
        return db.select(sql)
    except Exception as e:
        logger.error(f"Error select Articles without summary: {e}")
        
def generate_and_store_articles(db, articles, logger):
    '''
    Generate summaries for all articles from list
    :param db: database
    :param articles: list of articles to summarize
    :param logger: logger to save exceptions catching
    '''
    generator = SummaryChatGPTAPIGenerator()

    for article in articles:
        article_id = article.get('id', '')
        content = article.get('content', '')
        summary = generator.get_summary(content)

        # Save summary to database
        try:
            db.query('INSERT Summaries (article_id, summary, generated_date) VALUES (%s, %s, %s)', (article_id, summary, datetime.datetime.now()))
            db.commit()
        except Exception as e:
            logger.error(f"Error insert Summary to Database: {e}")   