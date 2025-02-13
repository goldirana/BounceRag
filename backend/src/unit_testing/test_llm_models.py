import unittest
from unittest.mock import patch, MagicMock
from backend.src.llm_models import get_openai_model

class TestGetOpenAIModel(unittest.TestCase):

    @patch('backend.src.llm_models.config_params')
    @patch('backend.src.llm_models.ChatOpenAI')
    def test_get_openai_model(self, mock_chat_openai, mock_config_params):
        # Arrange
        mock_config_params.model.chat_model = 'gpt-3.5-turbo'
        mock_config_params.model.temperature = 0.7
        mock_model_instance = MagicMock()
        mock_chat_openai.return_value = mock_model_instance

        # Act
        model = get_openai_model()

        # Assert
        mock_chat_openai.assert_called_once_with(temperature=0.7, model_name='gpt-3.5-turbo')
        self.assertEqual(model, mock_model_instance)

if __name__ == '__main__':
    unittest.main()