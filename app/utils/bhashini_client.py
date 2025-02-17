import requests
import json
import base64
from app.config.llm_config import BHASHINI_CONFIG

class BhashiniClient:
    PIPELINE_CONFIG_ENDPOINT = BHASHINI_CONFIG["pipeline_config_endpoint"]
    INFERENCE_ENDPOINT = BHASHINI_CONFIG["inference_endpoint"]
    PIPELINE_ID = BHASHINI_CONFIG["pipeline_id"]

    def __init__(self, user_id, api_key, pipeline_id=PIPELINE_ID):
        self.user_id = user_id
        self.api_key = api_key
        self.pipeline_id = pipeline_id
        self.headers = {
            "Content-Type": "application/json",
            "userID": self.user_id,
            "ulcaApiKey": self.api_key
        }
        self.config = self._get_pipeline_config()
        self.pipeline_data = self._parse_pipeline_config(self.config)
        self.inference_api_key = self.pipeline_data['inferenceApiKey']

    def _get_pipeline_config(self):
        payload = {
            "pipelineTasks": [
                {"taskType": "asr"},
                {"taskType": "translation"},
                {"taskType": "tts"}
            ],
            "pipelineRequestConfig": {
                "pipelineId": self.pipeline_id
            }
        }
        response = requests.post(
            self.PIPELINE_CONFIG_ENDPOINT,
            headers=self.headers,
            data=json.dumps(payload)
        )
        response.raise_for_status()
        return response.json()

    def _parse_pipeline_config(self, config):
        inference_api_key = config['pipelineInferenceAPIEndPoint']['inferenceApiKey']['value']
        pipeline_data = {
            'asr': {},
            'tts': {},
            'translation': {},
            'inferenceApiKey': inference_api_key
        }

        for pipeline in config['pipelineResponseConfig']:
            task_type = pipeline['taskType']
            if task_type in ['asr', 'translation', 'tts']:
                for language_config in pipeline['config']:
                    source_language = language_config['language']['sourceLanguage']

                    if task_type != 'translation':
                        if source_language not in pipeline_data[task_type]:
                            pipeline_data[task_type][source_language] = []

                        language_info = {
                            'serviceId': language_config['serviceId'],
                            'sourceScriptCode': language_config['language'].get('sourceScriptCode')
                        }

                        if task_type == 'tts':
                            language_info['supportedVoices'] = language_config.get('supportedVoices', [])

                        pipeline_data[task_type][source_language].append(language_info)
                    else:
                        target_language = language_config['language']['targetLanguage']
                        if source_language not in pipeline_data[task_type]:
                            pipeline_data[task_type][source_language] = {}

                        if target_language not in pipeline_data[task_type][source_language]:
                            pipeline_data[task_type][source_language][target_language] = []

                        language_info = {
                            'serviceId': language_config['serviceId'],
                            'sourceScriptCode': language_config['language'].get('sourceScriptCode'),
                            'targetScriptCode': language_config['language'].get('targetScriptCode')
                        }

                        pipeline_data[task_type][source_language][target_language].append(language_info)

        return pipeline_data

    def detect_language(self, audio_content):
        # Placeholder for language detection logic
        return "kn"  # Replace with actual detection logic
    
    def asr(self, audio_content, audio_format='wav', sampling_rate=16000, source_language=None):
        # Use the provided source_language if available; otherwise, detect it
        if not source_language:
            source_language = self.detect_language(audio_content)

        if source_language not in self.pipeline_data['asr']:
            available_languages = ', '.join(self.pipeline_data['asr'].keys())
            raise ValueError(f"ASR not supported for language '{source_language}'. Available languages: {available_languages}")

        service_info = self.pipeline_data['asr'][source_language][0]
        service_id = service_info['serviceId']

        payload = {
            "pipelineTasks": [
                {
                    "taskType": "asr",
                    "config": {
                        "language": {"sourceLanguage": source_language},
                        "serviceId": service_id,
                        "audioFormat": audio_format,
                        "samplingRate": sampling_rate
                    }
                }
            ],
            "inputData": {
                "audio": [
                    {"audioContent": base64.b64encode(audio_content).decode('utf-8')}
                ]
            }
        }

        headers = {
            'Accept': '*/*',
            'Authorization': self.inference_api_key,
            'Content-Type': 'application/json'
        }

        response = requests.post(
            self.INFERENCE_ENDPOINT,
            headers=headers,
            data=json.dumps(payload)
        )

        response.raise_for_status()
        return response.json()['pipelineResponse'][0]['output'][0]['source']

    def tts(self, text, source_language, gender='female', sampling_rate=8000):
        if source_language not in self.pipeline_data['tts']:
            available_languages = ', '.join(self.pipeline_data['tts'].keys())
            raise ValueError(f"TTS not supported for language '{source_language}'. Available languages: {available_languages}")

        service_info = self.pipeline_data['tts'][source_language][0]
        service_id = service_info['serviceId']

        payload = {
            "pipelineTasks": [
                {
                    "taskType": "tts",
                    "config": {
                        "language": {"sourceLanguage": source_language},
                        "serviceId": service_id,
                        "gender": gender,
                        "samplingRate": sampling_rate
                    }
                }
            ],
            "inputData": {
                "input": [{"source": text}]
            }
        }

        headers = {
            'Accept': '*/*',
            'Authorization': self.inference_api_key,
            'Content-Type': 'application/json'
        }

        response = requests.post(
            self.INFERENCE_ENDPOINT,
            headers=headers,
            data=json.dumps(payload)
        )

        response.raise_for_status()
        audio_base64 = response.json()['pipelineResponse'][0]['audio'][0]['audioContent']
        return base64.b64decode(audio_base64)

    def translate(self, text: str, source_language: str, target_language: str) -> str:
        """
        Translate text using Bhashini's translation service.
        """
        if source_language not in self.pipeline_data['translation']:
            available_languages = ', '.join(self.pipeline_data['translation'].keys())
            raise ValueError(f"Translation not supported for source language '{source_language}'. Available languages: {available_languages}")

        if target_language not in self.pipeline_data['translation'][source_language]:
            available_targets = ', '.join(self.pipeline_data['translation'][source_language].keys())
            raise ValueError(f"Translation not supported for target language '{target_language}'. Available target languages: {available_targets}")

        service_info = self.pipeline_data['translation'][source_language][target_language][0]
        service_id = service_info['serviceId']

        payload = {
            "pipelineTasks": [
                {
                    "taskType": "translation",
                    "config": {
                        "language": {
                            "sourceLanguage": source_language,
                            "targetLanguage": target_language
                        },
                        "serviceId": service_id
                    }
                }
            ],
            "inputData": {
                "input": [{"source": text}]
            }
        }

        headers = {
            'Accept': '*/*',
            'Authorization': self.inference_api_key,
            'Content-Type': 'application/json'
        }

        response = requests.post(
            self.INFERENCE_ENDPOINT,
            headers=headers,
            data=json.dumps(payload)
        )

        response.raise_for_status()
        return response.json()['pipelineResponse'][0]['output'][0]['target']