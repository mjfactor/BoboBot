import json
from difflib import get_close_matches
import os


def loadBrain(filename: str) -> dict:
    if not os.path.exists(filename):
        with open(filename, 'w') as f:
            json.dump({"question": []}, f, indent=2)
    with open(filename, 'r') as f:
        return json.load(f)


def save_to_brain(filename: str, data: dict):
    with open(filename, 'w') as f:
        json.dump(data, f, indent=2)


def find_best_matches(user_question: str, question: list[str]) -> list | None:
    best_matches = get_close_matches(user_question, question, n=1, cutoff=0.6)
    return best_matches[0] if best_matches else None


def get_answer_for_question(brain: dict, user_question: str) -> str:
    for q in brain['question']:
        if q['question'] == user_question:
            return q['answer']


def clean_brain(filename: str):
    with open(filename, 'w') as f:
        json.dump({"question": []}, f, indent=2)


def chat_bot():
    brain = loadBrain('brain.json')
    while True:
        user_question = input('You: ')
        if user_question.lower() in ['exit', 'quit', 'bye']:
            break
        elif user_question.lower() == 'clean':
            clean_brain('brain.json')
            print('BoboBot has been cleaned!')
            print("Teach Me, run me again!")
            break
        best_match: str | None = find_best_matches(user_question, [q['question'] for q in brain['question']])
        if best_match:
            print(f'Bot: {get_answer_for_question(brain, best_match)}')
        else:
            print('Bot: I do not understand your question. Can you teach me?')
            new_answer = input("Type the answer or 'skip' for the question: ")
            if new_answer.lower() != 'skip':
                brain['question'].append({'question': user_question, 'answer': new_answer})
                save_to_brain('brain.json', brain)
                print('BoBo: Thanks for teaching me!')


