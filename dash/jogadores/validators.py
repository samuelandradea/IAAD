# Arquivo: validators.py

def tratar_dados_jogador(nome_bruto, selecao_bruta, camisa_bruta):
    """
    Age como um 'trigger' ou 'middleware' para limpar e validar
    """
    #tratando o texto
    nome_formatado = nome_bruto.strip().title()
    selecao_limpa = selecao_bruta.strip()
    
    
    try:
        camisa_formatada = int(camisa_bruta)
    except ValueError:
        camisa_formatada = 0 #Valor padrão caso venha um texto por engano
        
    # Retorna os dados prontos e limpos
    return nome_formatado, selecao_limpa, camisa_formatada