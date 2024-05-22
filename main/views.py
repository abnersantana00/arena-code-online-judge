from django.shortcuts import render

# Create your views here.

from django.shortcuts import render
from django.http import HttpResponse
from .utils import extract_titles, generate_all_questions, generate_one_question
import json
import os
def home(request):

    return render(request, 'main/home.html')




# condicionais
def topic(request, topic_name ):

    if topic_name == 'conditional':
         titles_info = extract_titles('main/static/json-files/templates/conditional.json')
         context = {'topic' : 'Contitionals',
                    'titles_info': titles_info,}
         return render(request, 'main/topic.html', context)


def topic_detail(request, topic_name, title_name):
    # Construindo os caminhos dos arquivos com base no topic_name
    file1 = f'main/static/json-files/templates/{topic_name}.json'
    file2 = f'main/static/json-files/questions/{topic_name}-questions.json'

    # Lendo os arquivos JSON
    with open(file1, 'r', encoding='utf-8') as file:
        json_template = json.load(file)
    with open(file2, 'r', encoding='utf-8') as file:
        json_questions = json.load(file)

    all_questions = generate_all_questions(json_template,json_questions )
    one_question = generate_one_question(json_template, json_questions)
    print(one_question)

    context = {
        'title_name': title_name,
        'topic_name': topic_name,
        'all_questions': all_questions,
        'one_question' : one_question
    }


    return render(request, 'main/topic_detail.html', context)