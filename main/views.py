from django.shortcuts import render
from django.views.decorators.csrf import csrf_protect
from .utils import *
import json, random
def home(request):
    return render(request, 'home.html')




# condicionais
def topic(request, topic):

    json_template = f'main/static/json-files/templates/{topic}.json'
    json_questions = f'main/static/json-files/questions/{topic}-questoes.json'
    all_questions = generate_questions(json_template, json_questions)
    one_question = generate_questions(json_template, json_questions, select_one=True)
    context = {

        'all_questions': all_questions,
        'one_question': one_question,
    }
    if request.method == 'POST':
        code_submission = request.POST.get('code_submission')
        question = request.POST.get('question')
        print(code_submission)
        print(question)
        context = {

            'code_submission': code_submission,
            'question': question,
            'all_questions': all_questions,
            'one_question': one_question,
        }

        return render(request, 'topic_detail.html', context)





    return render(request, 'topic.html', context)

# descondiderar este topic detail
def topic_detail(request, topic, topic_name):

    file1 = f'main/static/json-files/templates/{topic}.json'
    file2 = f'main/static/json-files/questions/{topic}-questions.json'

    with open(file1, 'r', encoding='utf-8') as file:
        json_template = json.load(file)
    with open(file2, 'r', encoding='utf-8') as file:
        json_questions = json.load(file)

    all_questions = generate_all_questions(json_template,json_questions )
    one_question = generate_one_question(json_template, json_questions)
    problem_id = one_question['problem_id']

    combined_list = list(zip(one_question['input_expected'], one_question['output_expected']))
    expected = combined_list if len(combined_list) < 3 else random.sample(combined_list, 3)

    context = {
        'topic': topic,
        'topic_name': topic_name,
        'all_questions': all_questions,
        'one_question' : one_question,
        'problem_id' : problem_id,
        'expected' : expected
    }


    return render(request, 'topic_detail.html', context)




def source_code(request, code_submission, question, problem_id):
    if request.method == 'POST':
        print(code_submission)

        code_submission = request.POST.get('code_submission')
        file2 = f'main/static/json-files/questions/{topic}-questions.json'
        with open(file2, 'r', encoding='utf-8') as file:
            json_questions = json.load(file)
        print("Code submission:", code_submission, type(code_submission))
        result = run_test(code_submission, json_questions,problem_id)
        print("RESULTADO DO JUIZ :", result)

        context = {
            'topic': topic,
            #'topic_name': topic_name,
            'problem_id' : problem_id,
            'code_submission': code_submission,
            'result' : result,
        }

        return render(request, 'topic_source_code.html', context)

    return render(request, 'topic_source_code.html')