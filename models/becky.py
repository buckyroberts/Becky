import os

import promptlayer

from models.challenge_manager import ChallengeManager
from utils.strings import remove_whitespace

openai = promptlayer.openai
openai.api_key = os.getenv('OPENAI_API_KEY')
promptlayer.api_key = os.environ.get('PROMPTLAYER_API_KEY')


class Becky:

    def __init__(self, prompt_template_name):
        self.prompt_template_name = prompt_template_name
        prompt_template = promptlayer.prompts.get(self.prompt_template_name)
        self.system_content = prompt_template['messages'][0]['prompt']['template']
        self.user_content_template = prompt_template['messages'][1]['prompt']['template']

    def calculate_score(self):
        score = 0
        challenge_manager = ChallengeManager()

        for challenge in challenge_manager.challenges:
            variables = {
                'instructions': challenge.instructions,
                'source_code': challenge.source_code
            }

            response, pl_request_id = openai.ChatCompletion.create(
                model='gpt-3.5-turbo',
                messages=[
                    {
                        'role': 'system',
                        'content': self.system_content
                    },
                    {
                        'role': 'user',
                        'content': self.user_content_template.format(**variables)
                    },
                ],
                temperature=0.5,
                max_tokens=1024,
                return_pl_id=True
            )

            promptlayer.track.prompt(
                request_id=pl_request_id,
                prompt_name=self.prompt_template_name,
                prompt_input_variables=variables
            )

            trimmed_output = remove_whitespace(challenge.output)
            trimmed_response_content = remove_whitespace(response.choices[0].message.content)
            passed_challenge = trimmed_output == trimmed_response_content

            if passed_challenge:
                score += challenge.points
                print(f'Passed {challenge.name} | {challenge.points}/{challenge.points}')
            else:
                print(f'Failed {challenge.name} | 0/{challenge.points}')

        print(f'\nTotal Score: {score}')
