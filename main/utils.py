import  json, random

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


def generate_one_question(json_template,json_questions ):

    # Gere todas as questões usando a função generate_all_questions
    all_questions = generate_all_questions(json_template, json_questions)

    # Selecione uma questão de forma aleatória
    random_problem_id = random.choice(list(all_questions.keys()))
    random_question = all_questions[random_problem_id]

    return random_question
def generate_especific_question(json_template,json_questions, problem_id):
    ...


def extract_titles(json_file_path):
    with open(json_file_path, 'r') as file:
        data = json.load(file)

    titles_info = [(item['topic_name'], item['topic_id']) for item in data]
    return titles_info