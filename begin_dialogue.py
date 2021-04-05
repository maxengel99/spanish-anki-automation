'''Starts the textbox conversation'''
import os
import easygui
from anki_request import AnkiRequest
from concurrent.futures import ThreadPoolExecutor, as_completed
import requests
from github_handler import GithubHandler
import json
import csv


def get_text_file():
    '''Read in textfile from user and returns content'''

    vocab_file_name = easygui.fileopenbox(
        "Please upload a csv file of the new vocabulary")

    with open(vocab_file_name, newline='', encoding='utf8', errors='ignore') as f:
        reader = csv.reader(f)
        return list(reader)

def create_audio(word):
    '''creates the audio file'''
    url = "https://translate.google.com/translate_tts?ie=UTF-8&tl=es&client=tw-ob&q=" + word

    doc = requests.get(url)
    filename = 'mp3/{}.mp3'.format(word)

    with open(filename, "wb") as file:
        print('Writing file {}'.format(filename))
        file.write(doc.content)
        print("File writing completed for " + word)


def create_and_save_info(vocab_info):
    '''Create and saves audio files to ./mp3'''

    github_handler = GithubHandler()
    processes = []

    with ThreadPoolExecutor(max_workers=10) as executor:
        for cur_word in vocab_info:
            kanji_word = cur_word[0]

            if not os.path.isfile('mp3/{}.mp3'.format(kanji_word)):
                print('Adding audio for {}'.format(kanji_word))
                processes.append(executor.submit(
                    create_audio, kanji_word))
            else:
                print('Skipping word - {}'.format(kanji_word))

    for task in as_completed(processes):
        print(task.result())

    commit_message = easygui.enterbox()
    github_handler.add_to_github(commit_message)


def add_vocab_to_anki(vocab_info):
    '''Adds vocab and audio to anki deck, must have anki open'''

    anki_request = AnkiRequest()

    for cur_word in vocab_info:
        anki_arg = anki_request.generate_json(cur_word)
        response = anki_request.invoke(anki_arg)
        print(response)

    print("Completed adding vocab to anki")


def begin():
    '''Starts the textbox conversation'''

    print("Beginning dialogue")

    vocab_file_content = get_text_file()

    print('Creating audio')

    create_and_save_info(vocab_file_content)

    print('Adding to Anki deck')

    add_vocab_to_anki(vocab_file_content)

    user_continue = easygui.ynbox(
        "Would you like to perform another command?", choices=("Yes", "No"))

    if user_continue:
        begin()
    else:
        exit()


if __name__ == '__main__':
    begin()
