import json
import random
import openai


def generate_questions(template_path, question_path, qtd_itens=None, select_one=False):
    with open(template_path, 'r', encoding='utf-8') as template_file:
        template_data = json.load(template_file)

    with open(question_path, 'r', encoding='utf-8') as questoes_file:
        questoes_data = json.load(questoes_file)

    # Comparar o cod-template dos dois arquivos
    if template_data["cod-template"] == questoes_data["cod-template"]:
        total_questoes = len(questoes_data["questoes"])

        # Ajustar qtd_itens para não exceder o total de questões disponíveis
        if qtd_itens is None or qtd_itens > total_questoes:
            qtd_itens = total_questoes

        stem_variables = template_data["stem-var"]

        questions = []

        for n in range(qtd_itens):
            questao = questoes_data["questoes"][n]

            # Processar layers dinamicamente
            stem_principal = template_data["stem"]
            if "layer-1" in template_data and "layer-1-var" in questao:
                layer_name = template_data["layer-1"]["layer-nome"]  # Nome do layer dinâmico
                layer_1_stem = template_data["layer-1"]["stem"]

                for layer_var_name, layer_var_value in questao["layer-1-var"].items():
                    index = int(layer_var_value)
                    if layer_var_name in template_data["layer-1"]["layer-1-var"]:
                        variable_list = template_data["layer-1"]["layer-1-var"][layer_var_name]
                        if 0 <= index < len(variable_list):  # Verifica índice válido
                            variable_insert = variable_list[index]
                        else:
                            variable_insert = ""  # Valor vazio para índice inválido
                        # Substitui o placeholder no layer-1
                        layer_1_stem = layer_1_stem.replace(f"{{{{{layer_var_name}}}}}", variable_insert)

                # Substituir o layer-nome dinamicamente no stem principal
                stem_principal = stem_principal.replace(f"{{{{{layer_name}}}}}", layer_1_stem)

            # Substituição de variáveis do stem principal
            for stem_var_name, stem_var_value in questao["stem-var"].items():
                index = int(stem_var_value)
                variable_insert = stem_variables[stem_var_name][index]
                stem_principal = stem_principal.replace(f"{{{{{stem_var_name}}}}}", variable_insert)

            # Adicionar questão gerada
            questions.append(stem_principal)

        if select_one:
            return [random.choice(questions)]

        return questions

    else:
        raise ValueError("Erro: O template e a lista de geração têm códigos diferentes")

def get_feedback(question, code_submission, api_key):
    from openai import OpenAI

    # Criando o cliente diretamente com a chave API
    client = OpenAI(api_key=api_key)

    # Mensagens para o modelo
    message = [
        {"role": "system", "content": "Você é um assistente especializado em revisar código e dar feedback."}
    ]

    # Adicionando a questão e a submissão ao contexto
    feedback_prompt = (
        f"Questão: {question}\n"
        f"Código submetido:\n{code_submission}\n\n"
        f"Se minha resposta estiver errada diga exatamente onde errei. Baseado na questão e no código submetido, corrija a resposta e dê um feedback detalhado. "
    )

    # Adicionando o prompt como mensagem do usuário
    message.append({"role": "user", "content": feedback_prompt})

    try:
        # Chamada à API
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            temperature=1,
            max_tokens=1000,
            messages=message,
        )
        # Retornando o conteúdo da resposta
        return response.choices[0].message.content
    except Exception as e:
        # Tratamento de erro
        return f"Erro ao obter o feedback: {e}"