import json


def generate_questions(template_path, question_path, qtd_itens=None):
    with open(template_path, 'r') as template_file:
        template_data = json.load(template_file)

    with open(question_path, 'r') as questoes_file:
        questoes_data = json.load(questoes_file)

    # Comparar o cod-template dos dois arquivos
    if template_data["cod-template"] == questoes_data["cod-template"]:
        total_questoes = len(questoes_data["questoes"])

        # Ajustar qtd_itens para não exceder o total de questões disponíveis
        if qtd_itens is None or qtd_itens > total_questoes:
            qtd_itens = total_questoes

        stem_variables = template_data["stem-var"]

        for n in range(qtd_itens):
            questao = questoes_data["questoes"][n]

            # Montar o layer-1 (condição) - Se aplicável
            layer_1_stem = ""
            if "layer-1" in template_data and "layer-1-var" in questao:
                layer_1_stem = template_data["layer-1"]["stem"]
                for layer_var_name, layer_var_value in questao["layer-1-var"].items():
                    index = int(layer_var_value)
                    if layer_var_name in template_data["layer-1"]["layer-1-var"]:
                        variable_insert = template_data["layer-1"]["layer-1-var"][layer_var_name][index]
                        layer_1_stem = layer_1_stem.replace(f"{{{{{layer_var_name}}}}}", variable_insert)

            # Montar o layer-2 (se aplicável)
            layer_2_stem = ""
            if "layer-2" in template_data:
                layer_2_stem = template_data["layer-2"]["stem"]
                for layer_var_name, layer_var_value in questao["layer-2-var"].items():
                    index = int(layer_var_value)
                    variable_insert = template_data["layer-2"]["layer-2-var"][layer_var_name][index]
                    layer_2_stem = layer_2_stem.replace(f"{{{{{layer_var_name}}}}}", variable_insert)

            # Montar o layer-3 (se aplicável)
            layer_3_stem = ""
            if "layer-3" in template_data:
                layer_3_stem = template_data["layer-3"]["stem"]
                for layer_var_name, layer_var_value in questao["layer-3-var"].items():
                    index = int(layer_var_value)
                    variable_insert = template_data["layer-3"]["layer-3-var"][layer_var_name][index]
                    layer_3_stem = layer_3_stem.replace(f"{{{{{layer_var_name}}}}}", variable_insert)

            # Montar o stem principal e substituir as variáveis do stem
            stem_principal = template_data["stem"]
            for stem_var_name, stem_var_value in questao["stem-var"].items():
                index = int(stem_var_value)
                variable_insert = stem_variables[stem_var_name][index]
                stem_principal = stem_principal.replace(f"{{{{{stem_var_name}}}}}", variable_insert)

            # Substituir os layers no stem principal
            stem_principal = stem_principal.replace("{{{condicao}}}", layer_1_stem)
            stem_principal = stem_principal.replace("{{{layer-2}}}", layer_2_stem)
            stem_principal = stem_principal.replace("{{{layer-3}}}", layer_3_stem)

            print(f"### Questão {n + 1} ###")
            print(stem_principal)
            print()

    else:
        print("Erro: O template e a lista de geração têm códigos diferentes")