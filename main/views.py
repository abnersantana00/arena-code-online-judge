from django.shortcuts import render
from django.views.decorators.csrf import csrf_protect
from .utils import extract_titles, generate_all_questions, generate_one_question, run_test
import json
def home(request):
    return render(request, 'home.html')




# condicionais
def topic(request, topic):

    if topic == 'conditional':
         titles_info = extract_titles('main/static/json-files/templates/conditional.json')
         context = {
                    'titles_info': titles_info,
                    'topic': topic,
                    }



         return render(request, 'topic.html', context)


def topic_detail(request, topic, topic_name):

    file1 = f'main/static/json-files/templates/{topic}.json'
    file2 = f'main/static/json-files/questions/{topic}-questions.json'

    with open(file1, 'r', encoding='utf-8') as file:
        json_template = json.load(file)
    with open(file2, 'r', encoding='utf-8') as file:
        json_questions = json.load(file)

    all_questions = generate_all_questions(json_template,json_questions )
    one_question = generate_one_question(json_template, json_questions, "102024")
    problem_id = one_question['problem_id']

    context = {
        'topic': topic,
        'topic_name': topic_name,
        'all_questions': all_questions,
        'one_question' : one_question,
        'problem_id' : problem_id
    }


    return render(request, 'topic_detail.html', context)




def source_code(request, topic, topic_name, problem_id):
    if request.method == 'POST':
        code_submission = request.POST.get('code_submission')
        file2 = f'main/static/json-files/questions/{topic}-questions.json'
        with open(file2, 'r', encoding='utf-8') as file:
            json_questions = json.load(file)

        result = run_test(code_submission, json_questions,problem_id)
        print("RESULTADO DO JUIZ :", result)

        context = {
            'topic': topic,
            'topic_name': topic_name,
            'code_submission': code_submission,
            'result' : result,
        }

        return render(request, 'topic_source_code.html', context)

    return render(request, 'topic_source_code.html')




