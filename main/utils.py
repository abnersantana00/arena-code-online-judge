import  json, random, subprocess, difflib, sys
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
    expected_output = problem['output_expected']

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
        return f"Erro de execução com código de retorno {completed_process.returncode}"

    if len(actual_output) != len(expected_output):
        return "Erro de saída"

    correct_count = 0
    for actual, expected in zip(actual_output, expected_output):
        if actual == expected:
            correct_count += 1

    if correct_count == len(expected_output):
        return "Sucesso"

    similarity = sum([difflib.SequenceMatcher(None, actual, expected).ratio() for actual, expected in
                      zip(actual_output, expected_output)]) / len(expected_output)
    percentage = int(similarity * 100)

    if 1 <= percentage <= 99:
        return f"Resposta errada {percentage}%"

    return "Erro de saída"

# 
