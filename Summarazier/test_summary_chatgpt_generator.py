import unittest
from unittest.mock import Mock, patch
from summarizer.summary_chatgpt_api_generator import SummaryChatGPTAPIGenerator
import json

class TestSummaryChatGPTAPIGenerator(unittest.TestCase):
    def setUp(self) -> None:
        self.summary_chatgpt_api_generator = SummaryChatGPTAPIGenerator(config_file='./config.ini')

    @patch('summarizer.summary_chatgpt_api_generator.requests.post')
    def test_get_summary_request_result(self, mock_post):
        ''' Test requst results from chatGPT for content "Say Hello"'''
        mock_json = {'choices': [{'message' : {'content' : 'Hello'}}]}
        mock_post.return_value = Mock(status_code=200, json=lambda: mock_json)

        response = self.summary_chatgpt_api_generator.get_summary_request_result(content=None, model='gpt-3.5-turbo', temperature=0.5)
        
        self.assertEqual(response, mock_json)

        data = {
            'model': 'gpt-3.5-turbo',
            'messages': [{'role': 'user', 'content': 'Say Hello'}],
            'temperature': 0.5
        }

        mock_post.assert_called_with(f"{SummaryChatGPTAPIGenerator.BASE_URL}/chat/completions",
            headers=self.summary_chatgpt_api_generator.headers,
            data=json.dumps(data)
        )


    @patch('summarizer.summary_chatgpt_api_generator.SummaryChatGPTAPIGenerator.get_summary')
    def test_get_summary(self, mock_get_post):
        ''' Check results from chatGPT for sending message "Say Hello"'''
        mock_post = 'Hello'
        mock_get_post.return_value = mock_post

        post = self.summary_chatgpt_api_generator.get_summary(content=None)

        self.assertEqual(post, mock_post)


    def test_is_valid_summary(self):
        '''Get valid result from ChatGPT
           Test require internet connection'''
        result = self.summary_chatgpt_api_generator.get_summary(content='MySQL future is fantastic', model='gpt-3.5-turbo', temperature=0.5)
        
        self.assertIsNotNone(result)


if __name__ == "__main__":
    unittest.main()