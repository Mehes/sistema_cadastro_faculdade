import json

# Arquivos utilizados
arquivo_estudantes = 'estudantes.json'
arquivo_professores = 'professores.json'
arquivo_disciplinas = 'disciplinas.json'
arquivo_turmas = 'turmas.json'
arquivo_matriculas = 'matriculas.json'


# Menu Principal
def menu_principal():
    while True:
        print("     MENU PRINCIPAL     ")
        print("1. Estudantes")
        print("2. Disciplinas")
        print("3. Professores")
        print("4. Turmas")
        print("5. Matrículas")
        print("6. Sair")
        escolha = input("Digite a opção desejada: ")
        if escolha == '1':
            menu_operacoes(arquivo_estudantes)
        elif escolha == '2':
            menu_operacoes(arquivo_disciplinas)
        elif escolha == '3':
            menu_operacoes(arquivo_professores)
        elif escolha == '4':
            menu_operacoes(arquivo_turmas)
        elif escolha == '5':
            menu_operacoes(arquivo_matriculas)
        elif escolha == '6':
            print("Você saiu.")                               # unico ponto que para o programa inteiro
            break
        else:
            print("Opção inválida. Tente novamente.")


# Menu de Operações
def menu_operacoes(nome_arquivo):
    while True:
        print("     MENU DE OPERAÇÕES     ")
        print("1. Incluir")
        print("2. Listar")
        print("3. Atualizar")
        print("4. Excluir")
        print("0. Voltar ao menu principal")
        escolha2 = input("Digite a opção desejada: ")
        if escolha2 == "1":
            incluir(nome_arquivo)
        elif escolha2 == "2":
            listar(nome_arquivo)
        elif escolha2 == "3":
            atualizar(nome_arquivo)
        elif escolha2 == "4":
            excluir(nome_arquivo)
        elif escolha2 == "0":                         # unica maneira de voltar ao menu principal
            break
        else:
            print("Opção inválida. Tente novamente.")


# Função incluir para todas as opções
def incluir(nome_arquivo):
    lista_qualquer = ler_arquivo(nome_arquivo)

    def codigo_existe(codigo, lista):   # Função usada sempre que um código é solicitado para averiguar se já existe ou não o mesmo valor
        return any(item["codigo"] == codigo for item in lista)

    try:
        if nome_arquivo in [arquivo_estudantes, arquivo_professores]:
            codigo = int(input("Digite o código: "))
            if codigo_existe(codigo, lista_qualquer):
                print("Já existe um cadastro com esse código.")
                return

            nome = input("Digite o nome: ")
            cpf = input("Digite o CPF: ")
            novo_registro = {
                "codigo": codigo,
                "nome": nome,
                "cpf": cpf
            }

        elif nome_arquivo == arquivo_disciplinas:
            codigo = int(input("Digite o código da disciplina: "))
            if codigo_existe(codigo, lista_qualquer):
                print("Já existe uma disciplina com esse código.")
                return

            nome = input("Digite o nome da disciplina: ")
            novo_registro = {
                "codigo": codigo,
                "nome": nome,
            }

        elif nome_arquivo == arquivo_turmas:
            codigo = int(input("Digite o código da turma: "))
            if codigo_existe(codigo, lista_qualquer):
                print("Já existe uma turma com esse código.")
                return
            codigo_professor = int(input("Digite o código do professor: "))
            professores = ler_arquivo(arquivo_disciplinas)
            if not codigo_existe(codigo_professor, professores):
                print("Código de professor inválido, este código já foi cadastrado.")


            codigo_disciplina = int(input("Digite o código da disciplina: "))
            disciplinas = ler_arquivo(arquivo_disciplinas)
            if not codigo_existe(codigo_disciplina, disciplinas):
                print("Código de disciplina inválido, este código já foi cadastrado.")
                return

            novo_registro = {
                "codigo": codigo,
                "codigo_professor": codigo_professor,
                "codigo_disciplina": codigo_disciplina
            }

        elif nome_arquivo == arquivo_matriculas:

            codigo_estudante = int(input("Digite o código do estudante: "))
            estudantes = ler_arquivo(arquivo_estudantes)
            if not codigo_existe(codigo_estudante, estudantes):
                print("Código de estudante inválido, o código já foi cadastrado.")
                return

            codigo_turma = int(input("Digite o código da turma: "))
            turmas = ler_arquivo(arquivo_turmas)
            if not codigo_existe(codigo_turma, turmas):
                print("Código de turma inválido, o código já foi cadastrado.")
                return

            novo_registro = {
                "codigo_estudante": codigo_estudante,
                "codigo_turma": codigo_turma
            }

        else:
            print("Tipo de cadastro inválido.")
            return

        lista_qualquer.append(novo_registro)
        salvar_arquivo(lista_qualquer, nome_arquivo)
        print("Cadastro incluído com sucesso!")

    except ValueError:
        print("Erro: valor inválido. Certifique-se de digitar números onde for necessário.")


# Função listar para todas as opções
def listar(nome_arquivo):
    lista_qualquer = ler_arquivo(nome_arquivo)
    if not lista_qualquer:
        print("Não há cadastros.")
    else:
        print("Lista de Cadastros:")
        for item in lista_qualquer:
            for chave, valor in item.items():
                print(f"{chave}: {valor}")
            print("----------------")


# Função atualizar para todas as opções
def atualizar(nome_arquivo):
    lista_qualquer = ler_arquivo(nome_arquivo)
    if not lista_qualquer:
        print("Não há cadastros para atualizar.")
        return

    for item in lista_qualquer:
        print(f"Código: {item.get('codigo')}, Nome: {item.get('nome', item.get('descricao', '---'))}")

    try:
        codigo_atualizar = int(input("Digite o código que deseja atualizar: "))
    except ValueError:
        print("Código inválido. Digite um número inteiro.")
        return

    for item in lista_qualquer:
        if item["codigo"] == codigo_atualizar:
            print("Campos disponíveis para atualização:")
            for chave in item:
                print(f"- {chave}")
            campo = input("Digite o campo que deseja alterar: ").strip()

            if campo in item:
                novo_valor = input(f"Digite o novo valor para {campo}: ")

                # separando campos inteiros e strings para atualização
                campos_inteiros = [
                    "codigo", "codigo_disciplina", "codigo_professor",
                    "codigo_matricula", "codigo_estudante", "codigo_turma"
                ]

                if campo in campos_inteiros:
                    try:
                        novo_valor = int(novo_valor)
                    except ValueError:
                        print("Valor inválido! Deve ser um número inteiro.")
                        return

                item[campo] = novo_valor
                salvar_arquivo(lista_qualquer, nome_arquivo)
                print(f"{campo} atualizado com sucesso!")
            else:
                print("Campo inválido.")
            break
    else:
        print("Código não encontrado.")



# Função excluir para todas as opções
def excluir(nome_arquivo):
    lista_qualquer = ler_arquivo(nome_arquivo)
    if not lista_qualquer:
        print("Não há cadastros para excluir.")
        return

    codigo_excluir = int(input("Digite o código do registro que deseja excluir: "))
    item_excluido = None

    for item in lista_qualquer:
        if item["codigo"] == codigo_excluir:
            item_excluido = item
            break

    if item_excluido:
        lista_qualquer.remove(item_excluido)
        salvar_arquivo(lista_qualquer, nome_arquivo)
        print("Cadastro excluído com sucesso!")
    else:
        print(f"O registro com código {codigo_excluir} não foi encontrado.")


# Salvar dados no arquivo
def salvar_arquivo(lista_qualquer, nome_arquivo):
    with open(nome_arquivo, "w", encoding="utf-8") as arquivo:
        json.dump(lista_qualquer, arquivo, ensure_ascii=False)


# Ler dados do arquivo
def ler_arquivo(nome_arquivo):
    try:
        with open(nome_arquivo, 'r', encoding="utf-8") as arquivo:
            conteudo = arquivo.read().strip()
            if not conteudo:
                return []
            return json.loads(conteudo)
    except FileNotFoundError:
        return []

# Start do programa
menu_principal()
