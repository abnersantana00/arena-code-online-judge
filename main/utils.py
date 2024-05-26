import  json, random, subprocess, difflib, sys, time
def generate_all_questions(json_template, json_questions):
    questions = {}

    # Converte o json_template para um dicionário para facilitar a pesquisa
    template_dict = {item['topic_id']: item for item in json_template}

    for topic in json_questions:
        topic_name = topic['topic_name']

        topic_id = topic['topic_id']
        problems = topic['problems']
        if topic_id not in template_dict:
            continue

        template = template_dict[topic_id]
        stem_template = template['stem']
        variables = template['variable']

        for problem in problems:
            problem_id = problem['problem_id']
            variable_indices = problem['variable']
            title = problem.get('title', 'No Title')  # Obtém o título do problema
            filled_stem = stem_template

            for key, index in variable_indices.items():
                placeholder = "{{" + key + "}}"
                if key in variables and index < len(variables[key]):
                    value = variables[key][index]
                else:
                    value = "Índice fora do alcance"
                filled_stem = filled_stem.replace(placeholder, value)

            # Montando a questão com as informações adicionais
            questions[f"{problem_id}"] = {
                "topic_name": topic_name,
                "topic_id": topic_id,
                "problem_id": problem_id,
                "title": title,
                "stem": filled_stem,
            }

    return questions
# Template of Questions
def generate_one_question(json_template, json_questions, problem_id=None):
    # Gere todas as questões usando a função generate_all_questions
    all_questions = generate_all_questions(json_template, json_questions)

    # Se o problem_id for fornecido e existir nas questões, retorne a questão específica
    if problem_id is not None and problem_id in all_questions:
        return all_questions[problem_id]

    # Caso contrário, selecione uma questão de forma aleatória
    random_problem_id = random.choice(list(all_questions.keys()))
    random_question = all_questions[random_problem_id]

    return random_question
def extract_titles(json_file_path):
    with open(json_file_path, 'r') as file:
        data = json.load(file)

    titles_info = [{'topic_name': item['topic_name'], 'topic_id': item['topic_id']} for item in data]
    return titles_info
# Oline Judge Automatized Tests
import sys
import subprocess
import difflib
import time

def run_test(source_code, json_questions, problem_id):
    judge_code = {
        "runtime_error": None,
        "file_size": None,
        "file_size_max": None,
        "time_execution": None,
        "time_limit": None,
        "percentage": None,
        "actual_output": None,
        "output_expected": None,
        "base_code": None,
        "answer": None
    }

    if not source_code.strip():
        judge_code["runtime_error"] = "Erro por não digitar o código em branco"
        judge_code["answer"] = "Runtime error"
        return judge_code

    problem = None
    for item in json_questions:
        if problem_id in [p['problem_id'] for p in item.get('problems', [])]:
            problem = next(p for p in item['problems'] if p['problem_id'] == problem_id)
            break

    if problem is None:
        judge_code["runtime_error"] = "Erro: Problema não encontrado"
        judge_code["answer"] = "Runtime error"
        return judge_code

    judge_code["base_code"] = problem.get('base_code', None)
    input_data = problem['input_expected']
    output_expected = problem['output_expected']
    judge_code["output_expected"] = output_expected[0] if output_expected else None
    judge_code["time_limit"] = int(problem['time_limit'])

    try:
        # Utilizando o caminho absoluto do executável Python
        python_executable = sys.executable
        start_time = time.time()
        completed_process = subprocess.run(
            [python_executable, "-c", source_code],
            input='\n'.join(input_data).encode(),
            capture_output=True,
            text=True,
            timeout=judge_code["time_limit"]
        )
        end_time = time.time()
        judge_code["time_execution"] = round(end_time - start_time, 3)
        judge_code["actual_output"] = completed_process.stdout.strip()
    except subprocess.CalledProcessError as e:
        judge_code["runtime_error"] = f"Erro de execução: {e}"
        judge_code["answer"] = "Runtime error"
        return judge_code
    except subprocess.TimeoutExpired:
        judge_code["runtime_error"] = "Erro de execução: Tempo limite excedido"
        judge_code["answer"] = "Runtime error"
        return judge_code

    if completed_process.returncode != 0:
        judge_code["runtime_error"] = completed_process.stderr.strip()
        judge_code["answer"] = "Runtime error"
        return judge_code

    if judge_code["actual_output"] != judge_code["output_expected"]:
        judge_code["runtime_error"] = "Erro de saída"
        judge_code["answer"] = "Runtime error"
        return judge_code

    judge_code["percentage"] = 100
    judge_code["answer"] = "Success"
    return judge_code

    similarity = difflib.SequenceMatcher(None, judge_code["actual_output"], judge_code["output_expected"]).ratio()
    judge_code["percentage"] = int(similarity * 100)

    if 1 <= judge_code["percentage"] <= 99:
        judge_code["runtime_error"] = f"Resposta errada {judge_code['percentage']}%"
        judge_code["answer"] = f"wrong answer {judge_code['percentage']}%"

    return judge_code

def run_test_v0(source_code, json_questions, problem_id):
    if not source_code.strip():
        return "Erro por não digitar o código em branco"

    problem = None
    for item in json_questions:
        if problem_id in [p['problem_id'] for p in item.get('problems', [])]:
            problem = next(p for p in item['problems'] if p['problem_id'] == problem_id)
            break

    if problem is None:
        return "Erro: Problema não encontrado"

    input_data = problem['input_expected']
    output_expected = problem['output_expected']

    try:
        # Utilizando o caminho absoluto do executável Python
        python_executable = sys.executable
        completed_process = subprocess.run(
            [python_executable, "-c", source_code],
            input='\n'.join(input_data).encode(),
            capture_output=True,
            text=True,
            timeout=int(problem['time_limit'])
        )
        actual_output = completed_process.stdout.strip().split('\n')
    except subprocess.CalledProcessError:
        return "Erro de execução"
    except subprocess.TimeoutExpired:
        return "Erro de execução: Tempo limite excedido"

    if completed_process.returncode != 0:
        error_details = completed_process.stderr.strip()
        return f" Runtime Error :  {error_details}"

    if len(actual_output) != len(output_expected):
        return print("Erro de saída", actual_output, output_expected)

    correct_count = 0
    for actual, expected in zip(actual_output, output_expected):
        if actual == expected:
            correct_count += 1

    if correct_count == len(output_expected):
        return "Sucesso"

    similarity = sum([difflib.SequenceMatcher(None, actual, expected).ratio() for actual, expected in
                      zip(actual_output, output_expected)]) / len(output_expected)
    percentage = int(similarity * 100)

    if 1 <= percentage <= 99:
        return f"Resposta errada {percentage}%"

    return "Erro de saída"

