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
    judge_code["output_expected"] = output_expected
    judge_code["time_limit"] = int(problem['time_limit'])

    total_tests = len(input_data)
    passed_tests = 0

    for idx, input_value in enumerate(input_data):
        if not input_value.strip():
            continue

        try:
            python_executable = sys.executable
            start_time = time.time()
            completed_process = subprocess.run(
                [python_executable, "-c", source_code],
                input=input_value,
                capture_output=True,
                text=True,
                timeout=judge_code["time_limit"]
            )
            end_time = time.time()
            judge_code["time_execution"] = round(end_time - start_time, 3)
            actual_output = completed_process.stdout.strip()
            judge_code["actual_output"] = actual_output
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

        expected_output = output_expected[idx]

        if actual_output == expected_output:
            passed_tests += 1
        else:
            judge_code["runtime_error"] = f"Erro de saída para entrada '{input_value}' - esperado: '{expected_output}', obtido: '{actual_output}'"
            judge_code["answer"] = "Runtime error"
            return judge_code

    judge_code["percentage"] = (passed_tests / total_tests) * 100
    judge_code["answer"] = "Success" if passed_tests == total_tests else f"Partial Success: {passed_tests}/{total_tests} tests passed"

    return judge_code
