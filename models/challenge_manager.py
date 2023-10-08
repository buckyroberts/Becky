import os

from config.settings import CHALLENGES_DIR
from models.challenge import Challenge
from utils.files import get_subdirectories, read_file


class ChallengeManager:

    def __init__(self):
        self.challenges = self.get_challenges()

    @staticmethod
    def get_challenges():
        results = []
        points_directories = get_subdirectories(CHALLENGES_DIR)

        for points_directory in points_directories:
            points_str = os.path.basename(os.path.normpath(points_directory))
            points = int(points_str)
            challenge_directories = get_subdirectories(points_directory)

            for challenge_directory in challenge_directories:
                name = os.path.basename(os.path.normpath(challenge_directory))

                # File content
                instructions = read_file(challenge_directory / 'instructions.md')
                output = read_file(challenge_directory / 'output.py')
                source_code = read_file(challenge_directory / 'source_code.py')

                challenge = Challenge(
                    instructions=instructions,
                    name=name,
                    output=output,
                    points=points,
                    source_code=source_code
                )
                results.append(challenge)

        return results
