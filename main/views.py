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



    context = {
        'topic': topic,
        'topic_name': topic_name,
    }


    return render(request, 'topic_detail.html', context)




def source_code(request, code_submission, problem_id):
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