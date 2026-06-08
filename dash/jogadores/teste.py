import mysql.connector
import random

# 1. Configuração da Conexão (com a senha correta)
def obter_conexao():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="Matheusdev#2026",
        database="Copa do Mundo de Futebol"
    )

# 2. Função de Cadastro com ID Aleatório
def cadastrar_jogador_db(nome, posicao, camisa, data_nascimento, id_selecao):
    conn = obter_conexao()
    cursor = conn.cursor()

    try:
        # Gera o ID aleatório
        id_aleatorio = random.randint(10000, 999999)

        sql = """
            INSERT INTO Jogadores 
            (id_jogador, nome_jogador, posicao, numero_camisa, data_nascimento, Selecoes_id_selecoes) 
            VALUES (%s, %s, %s, %s, %s, %s)
        """
        valores = (id_aleatorio, nome, posicao, camisa, data_nascimento, id_selecao)
        
        cursor.execute(sql, valores)
        conn.commit() # Confirma a inserção no banco
        
        return True, f"Sucesso! {nome} cadastrado com o ID {id_aleatorio}."
        
    except mysql.connector.Error as err:
        return False, f"Erro no MySQL: {err.msg}"
        
    finally:
        cursor.close()
        conn.close()

# 3. Execução do Teste no Terminal
if __name__ == '__main__':
    print("🚀 Iniciando teste de conexão e cadastro...")
    
    # Dados de teste (Usando ID de seleção = 1 que corresponde ao Brasil no seu script)
    sucesso, mensagem = cadastrar_jogador_db(
        nome="Jogador Teste Terminal",
        posicao="Atacante",
        camisa=99,
        data_nascimento="2000-01-01",
        id_selecao=1
    )
    
    print("-" * 50)
    print(mensagem)
    print("-" * 50)