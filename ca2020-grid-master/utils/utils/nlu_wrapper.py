import requests


class NLUWrapper(object):
    def __init__(self, host='localhost', port=5001, **kwargs):
        self.host, self.port = host, port

    def annotate(self, in_utterance, modules=()):
        try:
            response = requests.post('http://{}:{}/annotate'.format(self.host, self.port),
                                     json={'state': {'utterance': in_utterance},
                                           'modules': modules},
                                     timeout=5)
        except requests.Timeout:
            return {}
        assert response.status_code == 200, 'Error calling the NLU service'
        return response.json()

    def annotate_sentiment(self, in_utterance):
        response = self.annotate(in_utterance, modules=['Preprocessor', 'VaderNLTK'])
        return response['annotations']['sentiment']

    def annotate_ner(self, in_utterance):
        response = self.annotate(in_utterance, modules=['Preprocessor', 'StanfordNER'])
        return response['annotations'].get('ner', {})

    def annotate_pos(self, in_utterance):
        response = self.annotate(in_utterance, modules=['Preprocessor', 'MorphoTagger'])
        return response['annotations'].get('postag', [])

    def annotate_abuse(self, in_utterance):
        response = self.annotate(in_utterance, modules=['Preprocessor', 'AlanaAbuseDetector'])
        return response['annotations'].get('abuse', {})
