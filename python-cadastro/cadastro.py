"""
Sistema de Cadastro e Login (Python)
-------------------------------------
Projeto simples para praticar lógica de programação:
estruturas condicionais, laços de repetição, listas,
funções e match/case.

Funcionalidades:
- Cadastrar novo usuário (nome, e-mail e senha)
- Fazer login com e-mail e senha
- Listar usuários cadastrados
- Sair do sistema
"""

usuarios = []


def cadastrar_usuario():
    nome = input("Nome: ").strip()
    email = input("E-mail: ").strip().lower()

    if any(u["email"] == email for u in usuarios):
        print(">> Já existe um usuário cadastrado com esse e-mail.\n")
        return

    senha = input("Senha: ").strip()

    if len(senha) < 4:
        print(">> A senha precisa ter pelo menos 4 caracteres.\n")
        return

    usuarios.append({"nome": nome, "email": email, "senha": senha})
    print(f">> Usuário '{nome}' cadastrado com sucesso!\n")


def fazer_login():
    email = input("E-mail: ").strip().lower()
    senha = input("Senha: ").strip()

    for usuario in usuarios:
        if usuario["email"] == email and usuario["senha"] == senha:
            print(f">> Bem-vindo(a), {usuario['nome']}!\n")
            return

    print(">> E-mail ou senha inválidos.\n")


def listar_usuarios():
    if not usuarios:
        print(">> Nenhum usuário cadastrado ainda.\n")
        return

    print("\n--- Usuários cadastrados ---")
    for i, usuario in enumerate(usuarios, start=1):
        print(f"{i}. {usuario['nome']} ({usuario['email']})")
    print()


def exibir_menu():
    print("===== SISTEMA DE CADASTRO =====")
    print("1. Cadastrar usuário")
    print("2. Fazer login")
    print("3. Listar usuários")
    print("4. Sair")


def main():
    while True:
        exibir_menu()
        opcao = input("Escolha uma opção: ").strip()

        match opcao:
            case "1":
                cadastrar_usuario()
            case "2":
                fazer_login()
            case "3":
                listar_usuarios()
            case "4":
                print("Encerrando o sistema. Até logo!")
                break
            case _:
                print(">> Opção inválida. Tente novamente.\n")


if __name__ == "__main__":
    main()
