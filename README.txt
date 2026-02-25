# 🏋️ FluxBody Analytics (FluxBody Fitness) - End-to-End BI & Data Pipeline

## 📖 Visão Geral do Projeto
Este projeto é uma simulação ponta a ponta do ambiente de dados de uma rede de academias fictícia (FluxBody Fitness). O objetivo foi atuar como um **Analista de BI Full-Stack / Analytics Engineer**, resolvendo problemas desde a extração de dados sujos de uma API simulada até a entrega de painéis executivos com insights acionáveis para a diretoria.

## 🎯 O Problema de Negócio
A FluxBody Fitness enfrentava desafios comuns no setor de assinaturas, além dos gestores se sentirem perdidos na tomada de decisão:

* Falta de visibilidade sobre o **MRR (Receita Recorrente Mensal)** e o impacto da inadimplência.
* Dificuldade em prever e evitar o **Churn (Cancelamento)**.
* Dados descentralizados e "sujos" vindos de sistemas legados de catraca e pagamentos.
* Necessidade de otimizar a escala de funcionários baseado no fluxo real de alunos nas filiais.

## 🛠️ Stack Tecnológica Utilizada
* **Linguagem:** Python (Pandas, JSON)
* **Banco de Dados:** SQLite e SQL (Data Warehouse local)
* **Visualização e Modelagem:** Power BI, DAX e Power Query
* **Engenharia de Dados:** Geração de dados (Faker/Mock), ETL (Extração, Tratamento e Load), Modelagem Dimensional (Star Schema)

---

## ⚙️ Arquitetura e Pipeline de Dados
O projeto foi dividido em 4 etapas principais:

### 1. Geração de Dados (Simulando o Caos)
Para simular um ambiente real e desafiador, criei scripts para gerar bases em formato JSON (`alunos.json` e `checkins.json`) repletos de inconsistências propositais:
* Datas em múltiplos formatos (ex: `MM/DD/YYYY` vs `YYYY-MM-DD`).
* Valores financeiros tipados como *String* e contendo símbolos (`$186.81`).
* Caracteres especiais em documentos (CPFs com pontuação).
* Status inconsistentes (`Ativo` vs `ativo`).

### 2. Processamento e Limpeza (ETL com Python)
Utilizando `Pandas`, desenvolvi um script de limpeza robusto para:
* Padronizar as tipagens de datas (`pd.to_datetime`).
* Limpar strings financeiras e converter para `Float`.
* Padronizar categorias textuais e remover caracteres especiais.
* **Integridade Referencial:** Implementei um "Sanity Check" via código para identificar e remover "Alunos Fantasmas" (IDs presentes na catraca, mas inexistentes no banco de cadastros).

### 3. Armazenamento (Data Warehouse com SQLite)
Após a limpeza, os DataFrames foram carregados via engine do `sqlite3` para um banco de dados relacional (`fluxbody.db`), facilitando consultas SQL analíticas e simulando o ambiente de um DW corporativo.

### 4. Modelagem e BI (Power BI & DAX)
No Power BI, os dados foram conectados e estruturados:
* Criação de uma `d_Calendario` dinâmica via DAX, respeitando os limites temporais das tabelas Fato.
* Relacionamentos `1:*` (Um para Muitos) entre Cadastro e Check-ins.
* Criação de tabela dimensão geográfica (`d_Estados`) para precisão absoluta no visual de Mapas.

---

## 💡 Insights Extraídos e Ações de Negócio
O painel foi dividido em duas visões estratégicas para atender a diferentes áreas da empresa:

### 💰 Relatório Financeiro

1. **A Hemorragia da Inadimplência:** O painel revelou uma taxa de inadimplência de 29%, representando $1.444 em risco.
   * *Ação Proposta:* Congelar campanhas de atração temporariamente e focar o time de atendimento em renegociação e recuperação de crédito, o que trará fluxo de caixa imediato.
2. **Receita Garantida vs. Churn:** A receita perdida (cancelados) representa mais da metade do MRR atual. Isso é um problema gravíssimo.
   * *Ação Proposta:* Reestruturação da área de *Customer Success* da academia para focar no engajamento dos alunos nos primeiros 3 meses.
3. **Padrão de Matrículas:** Quartas e segundas-feiras são os dias de maior pico de conversão.
   * *Ação Proposta:* Direcionar o orçamento do tráfego pago e colocar os melhores consultores de vendas nas unidades nestes dias específicos.

### ⚙️ Relatório Operacional

1. **Painel de Ação Anti-Churn (Dias sem treinar):** Uma tabela dinâmica isola alunos Ativos que não frequentam a academia há mais de 30 dias.
   * *Ação Proposta:* Ferramenta de uso diário para a recepção realizar ligações preventivas, oferecendo avaliações físicas para resgatar o aluno antes que ele cancele o plano.
2. **Dimensionamento de rede (Top Unidades):** O Mapa de Formas revela alta concentração de acessos em estados como o Texas e Califórnia.
   * *Ação Proposta:* Priorizar manutenções preventivas de maquinário nas unidades dessas regiões devido ao alto desgaste, enquanto o Marketing foca nas regiões de baixo tráfego.
3. **Embaixadores da marca (Top 10 engajados):** Identificação dos heavy-users.
   * *Ação Proposta:* Oferecer a estes 10 alunos o programa "indique um amigo" com isenção de mensalidade, usando-os como promotores orgânicos da marca.
