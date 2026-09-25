from database import criar_tabela
from estoque import (
    atualizar_produto,
    buscar_por_id,
    buscar_por_nome,
    cadastrar_produto,
    excluir_produto,
    listar_produtos,
    produtos_com_estoque_baixo,
    registrar_entrada,
    registrar_saida,
)


def ler_inteiro(mensagem, minimo=None):
    while True:
        try:
            valor = int(input(mensagem))
            if minimo is not None and valor < minimo:
                print(f"Digite um valor maior ou igual a {minimo}.")
                continue
            return valor
        except ValueError:
            print("Digite um número inteiro válido.")


def ler_decimal(mensagem, minimo=None):
    while True:
        try:
            valor = float(input(mensagem).replace(",", "."))
            if minimo is not None and valor < minimo:
                print(f"Digite um valor maior ou igual a {minimo}.")
                continue
            return valor
        except ValueError:
            print("Digite um número válido.")


def mostrar_produto(produto):
    print(
        f'ID: {produto["id"]} | Nome: {produto["nome"]} | '
        f'Preço: R$ {produto["preco"]:.2f} | Quantidade: {produto["quantidade"]} | '
        f'Categoria: {produto["categoria"]}'
    )


def cadastrar():
    print("\n--- Cadastrar produto ---")
    nome = input("Nome: ").strip()
    preco = ler_decimal("Preço: R$ ", 0)
    quantidade = ler_inteiro("Quantidade inicial: ", 0)
    categoria = input("Categoria: ").strip()

    try:
        produto_id = cadastrar_produto(nome, preco, quantidade, categoria)
        print(f"Produto cadastrado com sucesso. ID: {produto_id}")
    except ValueError as erro:
        print(f"Erro: {erro}")


def listar():
    print("\n--- Produtos cadastrados ---")
    produtos = listar_produtos()
    if not produtos:
        print("Nenhum produto cadastrado.")
        return
    for produto in produtos:
        mostrar_produto(produto)


def buscar():
    print("\n1 - Buscar por ID")
    print("2 - Buscar por nome")
    opcao = input("Escolha: ").strip()

    if opcao == "1":
        produto = buscar_por_id(ler_inteiro("ID: ", 1))
        if produto:
            mostrar_produto(produto)
        else:
            print("Produto não encontrado.")
    elif opcao == "2":
        produtos = buscar_por_nome(input("Digite parte do nome: "))
        if not produtos:
            print("Produto não encontrado.")
        else:
            for produto in produtos:
                mostrar_produto(produto)
    else:
        print("Opção inválida.")


def atualizar():
    print("\n--- Atualizar produto ---")
    produto_id = ler_inteiro("ID do produto: ", 1)
    produto = buscar_por_id(produto_id)
    if produto is None:
        print("Produto não encontrado.")
        return

    mostrar_produto(produto)
    nome = input(f'Novo nome [{produto["nome"]}]: ').strip() or produto["nome"]
    preco_texto = input(f'Novo preço [{produto["preco"]:.2f}]: ').strip()
    qtd_texto = input(f'Nova quantidade [{produto["quantidade"]}]: ').strip()
    categoria = input(f'Nova categoria [{produto["categoria"]}]: ').strip() or produto["categoria"]

    try:
        preco = float(preco_texto.replace(",", ".")) if preco_texto else produto["preco"]
        quantidade = int(qtd_texto) if qtd_texto else produto["quantidade"]
        atualizar_produto(produto_id, nome, preco, quantidade, categoria)
        print("Produto atualizado com sucesso.")
    except ValueError as erro:
        print(f"Erro: {erro}")


def excluir():
    print("\n--- Excluir produto ---")
    produto_id = ler_inteiro("ID do produto: ", 1)
    if excluir_produto(produto_id):
        print("Produto excluído com sucesso.")
    else:
        print("Produto não encontrado.")


def entrada():
    produto_id = ler_inteiro("ID do produto: ", 1)
    quantidade = ler_inteiro("Quantidade de entrada: ", 1)
    if registrar_entrada(produto_id, quantidade):
        print("Entrada registrada com sucesso.")
    else:
        print("Produto não encontrado.")


def saida():
    produto_id = ler_inteiro("ID do produto: ", 1)
    quantidade = ler_inteiro("Quantidade de saída: ", 1)
    resultado = registrar_saida(produto_id, quantidade)
    if resultado == "ok":
        print("Saída registrada com sucesso.")
    elif resultado == "estoque_insuficiente":
        print("Estoque insuficiente para essa saída.")
    else:
        print("Produto não encontrado.")


def estoque_baixo():
    print("\n--- Produtos com estoque baixo ---")
    produtos = produtos_com_estoque_baixo()
    if not produtos:
        print("Nenhum produto com estoque baixo.")
        return
    for produto in produtos:
        mostrar_produto(produto)


def menu():
    criar_tabela()

    while True:
        print("\n=== SISTEMA DE GERENCIAMENTO DE ESTOQUE ===")
        print("1 - Cadastrar produto")
        print("2 - Listar produtos")
        print("3 - Buscar produto")
        print("4 - Atualizar produto")
        print("5 - Excluir produto")
        print("6 - Registrar entrada")
        print("7 - Registrar saída")
        print("8 - Ver estoque baixo")
        print("0 - Sair")

        opcao = input("Escolha uma opção: ").strip()

        if opcao == "1":
            cadastrar()
        elif opcao == "2":
            listar()
        elif opcao == "3":
            buscar()
        elif opcao == "4":
            atualizar()
        elif opcao == "5":
            excluir()
        elif opcao == "6":
            entrada()
        elif opcao == "7":
            saida()
        elif opcao == "8":
            estoque_baixo()
        elif opcao == "0":
            print("Programa encerrado.")
            break
        else:
            print("Opção inválida.")


if __name__ == "__main__":
    menu()
