from django.shortcuts import render

# Create your views here.

from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_protect
from .utils import extract_titles, generate_all_questions, generate_one_question, run_test
import json
import os
def home(request):

    return render(request, 'home.html')




# condicionais
def topic(request, topic_name):

    if topic_name == 'conditional':
         titles_info = extract_titles('main/static/json-files/templates/conditional.json')
         context = {'topic' : 'Contitionals',
                    'titles_info': titles_info,}
         print("titles_info =", titles_info)
         return render(request, 'topic.html', context)


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
    one_question = generate_one_question(json_template, json_questions, "102024")
    print(one_question)

    context = {
        'title_name': title_name,
        'topic_name': topic_name,
        'all_questions': all_questions,
        'one_question' : one_question
    }


    return render(request, 'main/topic_detail.html', context)



@csrf_protect
def source_code(request, topic_name, title_name):
    if request.method == 'POST':
        source_code = request.POST.get('source_code')
        topic_id = request.POST.get('topic_id')
        problem_id = request.POST.get('problem_id')

        file2 = f'main/static/json-files/questions/{topic_name}-questions.json'
        with open(file2, 'r', encoding='utf-8') as file:
            json_questions = json.load(file)

        result = run_test(source_code, json_questions,problem_id)
        print("RESULTADO DO JUIZ :", result)

        # Aqui você pode processar o código-fonte enviado e o objeto one_question
        # Por exemplo, salvar em um banco de dados, executar testes, etc.
        # Para simplicidade, vamos apenas passar esses dados para o contexto
        print("run_test :", type(source_code), source_code, type(json_questions), type(problem_id), problem_id)
        context = {
            'topic_name': topic_name,
            'title_name': title_name,
            'source_code': source_code,
            'topic_id': topic_id,
            'problem_id': problem_id,
            'result' : result,
        }

        return render(request, 'main/topic_source_code.html', context)

    return render(request, 'main/topic_source_code.html')