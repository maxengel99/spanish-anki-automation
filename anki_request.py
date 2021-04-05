'''Handles interaction with anki'''
import json
import urllib.request


class AnkiRequest:
    """Handles interaction with anki"""

    def generate_json(self, cur_word):
        """Create json for anki"""
        fields = {'Spanish': cur_word[0], 'English': cur_word[1]}

        audio_json = {'url': 'https://raw.githubusercontent.com/maxengel99/spanish-anki-automation/master/mp3/{}.mp3'.format(cur_word[0]), 'filename': '{}.mp3'.format(cur_word[0]),
                      'fields': ['Audio']}
        deck_name = 'Spanish - Practical'
        model_name = 'Spanish - Front and Back'
        json_args = {'deckName': deck_name, 'modelName': model_name,
                     'fields': fields, 'options': {'allowDuplicate': False},
                     'tags': [], 'audio': audio_json}
        return {'action': 'addNote', 'params': {'note': json_args},
                'version': 6}

    def invoke(self, params):
        """Makes request to add anki card"""
        print(params)
        response = json.load(urllib.request.urlopen(
            'http://localhost:8765', json.dumps(params).encode('utf-8')))
        return response
