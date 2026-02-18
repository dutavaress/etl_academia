# %%
import pandas as pd
import json
import sqlite3

with open('alunos.json', 'r') as f:
    dados_alunos = json.load(f)

df_alunos = pd.DataFrame(dados_alunos)

with open('checkins.json', 'r') as f:
    dados_checkins = json.load(f)

df_checkins = pd.DataFrame(dados_checkins)



#%%
print(df_alunos.head())
print(df_alunos.info())


# %%
#Tratamento de dados alunos.json
df_alunos['data_cadastro'] = pd.to_datetime(df_alunos['data_cadastro'], errors='coerce')
df_alunos['mensalidade'] = df_alunos['mensalidade'].str.replace('$', '').str.replace(',', '.').astype(float)
df_alunos['cpf'] = df_alunos['cpf'].str.replace('-', '')
df_alunos['status'] = df_alunos['status'].str.replace('ativo', 'Ativo')

#Colunas data, status e cpf tratadas e padronizadas.


# %%
#Verificação de possíveis inconsistências em alunos.json

print(df_alunos['status'].unique())
counts_cpf = df_alunos['cpf'].value_counts()
print(counts_cpf[counts_cpf > 1])
#Não há cpfs duplicados e status está consistente.

counts_name = df_alunos['nome'].value_counts()
print(counts_name[counts_name > 1]) 
#Não há nomes duplicados


# %%
#View da base checkins.json
print(df_checkins.head())
print(df_checkins.info())



# %%
#Tratamento de dados checkins.json
df_checkins['data_hora'] = pd.to_datetime(df_checkins['data_hora'], errors='coerce')



# %%
#Resultado final das bases após o tratamento de dados
print(df_checkins.head())
print('--------------------------------')
print(df_alunos.head())   



# %%
#Verificando se há alunos fantasmas (id's de check-in que não existem na base alunos)
ids_alunos = set(df_alunos['id'].unique())
ids_checkins = set(df_checkins['id_aluno'].unique())

# Alunos fantasmas (IDs que estão no checkin mas não no cadastro)
fantasmas = ids_checkins - ids_alunos

if len(fantasmas) > 0:
    print(f"Há {len(fantasmas)} check-ins de alunos inexistentes!")
    print(f"IDs inconsistentes: {list(fantasmas)[:5]}...")
    
    # Decisão de Engenharia: Vamos remover esses check-ins sujos
    df_checkins = df_checkins[df_checkins['id_aluno'].isin(ids_alunos)]
    print("Checkins incorretos removidos")
else:
    print("Não há check-ins de alunos inexistentes.")



# %%

#Criando conexão com um arquivo de banco de dados
conn = sqlite3.connect('fluxbody.db')

#Salvando os df's como tabelas SQL
df_alunos.to_sql('alunos', conn, if_exists='replace', index=False)
df_checkins.to_sql('checkins', conn, if_exists='replace', index=False)



#%% 
#Testando consulta para verificar se a consulta SQL direto no python funcionou.
query = """
SELECT 
    a.nome,
    COUNT(c.id_aluno) as total_checkins
FROM alunos a
LEFT JOIN checkins c ON a.id = c.id_aluno
GROUP BY a.nome
ORDER BY total_checkins DESC
LIMIT 5
"""

df_top_alunos = pd.read_sql(query, conn)
print("\nTop 5 alunos mais frequentes:")
print(df_top_alunos)

conn.close()

# %%
