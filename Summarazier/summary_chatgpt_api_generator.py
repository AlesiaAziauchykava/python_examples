import requests
import configparser
import json

class SummaryChatGPTAPIGenerator:
    BASE_URL = 'https://api.openai.com/v1'
    
    def __init__(self, config_file='./config.ini'):
        config = configparser.ConfigParser()
        config.read(config_file)

        secret_key = config.get('chatgpt', 'secret_key')

        self.headers = {
            'Authorization': f'Bearer {secret_key}',
            'Content-Type': 'application/json'
        }
      
    
    def get_summary_request_result(self, content, model='gpt-3.5-turbo', temperature=0.5):
        '''
        Fetch post for requested receiver from ChatGPT API
        
        :param content: content of article
        :param model: model of CharGPT - 'gpt-3.5-turbo' or 'gpt-4' or ...
        :param temperature: temperature for chatGPT API request 0 - 1

        :return: return request result from chatGPT API 
        '''

        # generate request prompt for ChatGPT for selected receiver (LinkedIn or Twitter)
        if content:
            prompt = 'Summarize: ' + content
        else: 
            prompt = 'Say Hello'
        
        # prepare data for ChatGPT API POST request
        data = {
            'model': model,
            'messages': [{'role': 'user', 'content': prompt}],
            'temperature': temperature
        }

        # send POST request to ChatGPT API
        response = requests.post(
            f'{self.BASE_URL}/chat/completions', 
            headers=self.headers, data=json.dumps(data))
        
        response.raise_for_status()
        return response.json()
    

    def get_summary(self, content, model='gpt-3.5-turbo', temperature=0.5):
        '''
        Get post text from response

        :param content: content of article
        :param model: model of CharGPT - 'gpt-3.5-turbo' or 'gpt-4' or ...
        :param temperature: temperature for chatGPT API request 0 - 1

        :return: return post content 
        '''
        result = self.get_summary_request_result(content, model, temperature)
        return result.get('choices', [])[0].get('message', {}).get('content',None)