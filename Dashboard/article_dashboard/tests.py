from django.test import TestCase
from article_dashboard.models import Summaries, Articles
import sqlite3
import hashlib
import os
from dashboards.settings import PROJECT_ROOT


class ArticleDashboardTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        '''
        Preopare "test" database for testing
        '''
        cls.create_test_database()
        cls.fill_test_database()


    @classmethod   
    def create_test_database(cls):
        con = sqlite3.connect("test.db")
        print(con)
        cur = con.cursor()
        print(cur)
        print(cur.execute('''CREATE TABLE IF NOT EXISTS Articles (
            id VARCHAR(255) PRIMARY KEY,
            title TEXT NOT NULL,
            content TEXT,
            published_date DATETIME,
            author VARCHAR(255),
            url TEXT NOT NULL,
            source VARCHAR(255)
            );'''))
        
        cur.execute('''CREATE TABLE IF NOT EXISTS ArticleMetadata (
            id INT AUTO_INCREMENT PRIMARY KEY,
            article_id VARCHAR(255),
            categories TEXT,
            image_url TEXT,
            engagement_data TEXT,
            FOREIGN KEY (article_id) REFERENCES Articles(id)
            );''')
        
        cur.execute('''CREATE TABLE IF NOT EXISTS Summaries (
            id INT AUTO_INCREMENT PRIMARY KEY,
            article_id VARCHAR(255),
            summary TEXT,
            is_bad TINYINT(1),
            generated_date DATETIME,
            FOREIGN KEY (article_id) REFERENCES Articles(id)
            );''')
        
        con.close()

    @classmethod
    def fill_test_database(cls):

        # 1st - article and summary
        title = 'This is my life!'
        hash_object = hashlib.md5(title.encode())
        article_id = str(hash_object.hexdigest())
        article = Articles.objects.create(id=article_id, 
            title=title, 
            content='I like music, dance and working as a developer', 
            published_date='2023-10-30', 
            author='Alesia Aziauchykava',
            url='https://www.youtube.com/watch?v=fUYHqrgJAt0',
            source='Audio')
        
        Summaries.objects.create(id=1, article=article, summary='My life', is_bad=0, generated_date='2023-10-30')

        # 2nd - article and summary
        title = 'Halloween party'
        hash_object = hashlib.md5(title.encode())
        article_id = str(hash_object.hexdigest())
        article = Articles.objects.create(id=article_id, 
            title=title, 
            content='We spent time by playing halloween games', 
            published_date='2023-11-01', 
            author='Alesia Aziauchykava',
            url='https://en.wikipedia.org/wiki/Halloween',
            source='Text')
        
        Summaries.objects.create(id=2, article=article, summary='Helloween', is_bad=0, generated_date='2023-11-01')

        # 3d - article and summary
        title = 'The weather is fine today!'
        hash_object = hashlib.md5(title.encode())
        article_id = str(hash_object.hexdigest())
        article = Articles.objects.create(id=article_id, 
            title=title, 
            content='There are good mushrooms in October forest!', 
            published_date='2023-10-31', 
            author='Alesia Aziauchykava',
            url='https://medium.com/snap-shots/its-all-about-the-mushroom-4d88b76e31b8',
            source='Text')
        
        Summaries.objects.create(id=3, article=article, summary='Mushrooms', is_bad=0, generated_date='2023-10-31')


    '''
    Check models for Articles and Summaries
    '''
    def test_article_title_label(self):
        article = Articles.objects.first()
        field_label = article._meta.get_field('title').verbose_name
        self.assertEqual(field_label, 'title')


    def test_article_content_label(self):
        article = Articles.objects.first()
        field_label = article._meta.get_field('content').verbose_name
        self.assertEqual(field_label, 'content')


    def test_article_published_date_label(self):
        article = Articles.objects.first()
        field_label = article._meta.get_field('published_date').verbose_name
        self.assertEqual(field_label, 'published date')


    def test_article_author_label(self):
        article = Articles.objects.first()
        field_label = article._meta.get_field('author').verbose_name
        self.assertEqual(field_label, 'author')


    def test_article_url_label(self):
        article = Articles.objects.first()
        field_label = article._meta.get_field('url').verbose_name
        self.assertEqual(field_label, 'url')


    def test_article_source_label(self):
        article = Articles.objects.first()
        field_label = article._meta.get_field('source').verbose_name
        self.assertEqual(field_label, 'source')


    def test_summary_summary_label(self):
        summary = Summaries.objects.first()
        field_label = summary._meta.get_field('summary').verbose_name
        self.assertEqual(field_label, 'summary')


    def test_summary_is_bad_label(self):
        summary = Summaries.objects.first()
        field_label = summary._meta.get_field('is_bad').verbose_name
        self.assertEqual(field_label, 'is bad')


    def test_summary_generated_date_label(self):
        summary = Summaries.objects.first()
        field_label = summary._meta.get_field('generated_date').verbose_name
        self.assertEqual(field_label, 'generated date')
    
    
    '''
    Check views
    '''
    def test_articles_ordered_by_published_date(self):
        '''
        Check order of articles in on the main page: should be descending
        '''
        response = self.client.get('/articles_list')
        last_date = 0
        for article in response.context['articles']:
            if last_date == 0:
                last_date = article.published_date
            else:
                self.assertTrue(last_date >= article.published_date)
                last_date = article.published_date


    def test_show(self):
        '''
        Check response and template for the view "show"
        '''
        response = self.client.get('/articles_list')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'articles_list.html')

   
    def test_show_woth_parameters(self):
        '''
        Check response and template for the view "show" with parameters:
        date_form and date_to
        '''
        response = self.client.get('/articles_list?date_from=2023-10-10&date_to=2023-11-20')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'articles_list.html')


    def test_summary_edit(self):
        '''
        Check response and template for the view "summary_edit" 
        '''
        summary = Summaries.objects.first()
        response = self.client.get('/summary_edit/' + str(summary.id))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'summary_edit.html')


    def test_summary_update(self):
        '''
        Check response and template for the view "summary_update" 
        '''
        summary = Summaries.objects.first()
        response = self.client.post('/summary_update/' + str(summary.id), 
            {'article': summary.article.id,
            'summary': summary.summary, 
            'is_bad' : summary.is_bad, 
            'generated_date' : summary.generated_date})
        
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, '/articles_list')


    def test_summary_update_article_not_found(self):
        '''
        Check response and template for the view "summary_update" with incorrect Article
        '''
        summary = Summaries.objects.first()
        response = self.client.post('/summary_update/' + str(summary.id), 
            {'article': '123',
            'summary': summary.summary, 
            'is_bad' : summary.is_bad, 
            'generated_date' : summary.generated_date})
        
        self.assertEqual(response.status_code, 404)
