# 🍺 Projeto AB InBev – Pipeline de Dados - Cervejarias

## 👩‍💻 Autora

Daniella Viana  
[github.com/DaniellaViana](https://github.com/DaniellaViana) 

## 📌 Objetivo
Este projeto implementa um pipeline de dados ETL (Extract, Transform, Load), utilizando o **Apache Airflow** para orquestração, e **Pandas** para processamento de dados. A arquitetura segue o modelo **Lakehouse**, com as camadas Bronze, Silver e Gold, permitindo fácil rastreabilidade e modularidade.

## 📁 Estrutura do Projeto

A estrutura do repositório está organizada da seguinte forma:

Projeto-Bees/ <br>│ ├── dags/ # Código principal
<br>│    └── brewery_pipeline.py
<br>│ ├── data/ # Camadas do Lakehouse
<br>│ ├── bronze/ # Dados brutos extraídos 
<br>│ ├── silver/ # Dados limpos/tratados
<br>│ └── gold/ # Dados agregados para análise 
<br>│ ├── tests/ # Testes de extração e transformação
<br>│ ├── extract_test.py
<br>│ └── transform_test.py 
<br>│ ├── docker-compose.yml # Configuração do Docker para o Airflow 
<br>└── .gitignore # Arquivo de configuração do Git
 
## ▶️ Execução

### 1. Clone o repositório em seu ambiente local:
   
```git clone https://github.com/DaniellaViana/Projeto-Bees.git```
<br><br>cd Projeto-Bees

### 2. Subir o ambiente com Airflow

Este projeto já vem com um docker-compose.yml pronto para rodar o Airflow localmente:

**Execute o comando abaixo:**

```docker-compose up --build```

Acesse a interface do Airflow em:
👉 http://localhost:8080

**Login:**

Usuário: admin
<br>Senha: admin

### 3. Executar o pipeline
Na interface do Airflow, ative a DAG **brewery_data_pipeline** (se não estiver ativa). Você pode executá-la manualmente ou aguardar o agendamento automático (Todos os dias às 22h).

### 4. Resultado da execução
Após a execução, os arquivos de dados transformados estarão disponíveis nas seguintes localizações:

**data/silver/breweries.parquet**

**data/gold/brewery_summary.parquet**

## ⚙️ Tecnologias e Arquitetura

**Apache Airflow:** Orquestração das tarefas de ETL, proporcionando monitoramento e escalabilidade futura.

**Pandas:** Processamento de dados tabulares, ideal para trabalhar com grandes volumes de dados em Python.

**Arquitetura Lakehouse:** A separação dos dados em Bronze, Silver e Gold facilita a rastreabilidade, modularidade e governança de dados.

**Bronze:** Dados brutos extraídos de fontes externas.

**Silver:** Dados limpos e tratados, prontos para análise.

**Gold:** Dados agregados para visualizações e insights.

O pipeline foi modularizado, com funções específicas para cada etapa:

Extração de dados.
Transformação dos dados (limpeza, formatação, etc).
Agregação para análise e visualização.

# 🔄 Trade-offs
**Uso do LocalExecutor com PostgreSQL:** o projeto utiliza o Airflow com LocalExecutor e PostgreSQL como metadatabase, o que oferece maior robustez e paralelismo local. Ainda assim, o LocalExecutor não oferece a mesma escalabilidade que opções como KubernetesExecutor.

**Processamento em memória com Pandas:** ideal para datasets pequenos e prototipagem rápida. 

**Fonte de dados externa:** a ingestão de dados é feita via requisição GET a uma API externa, o que simula com fidelidade um cenário real de extração dinâmica.

**Orquestração baseada em tempo:** a DAG é executada com base em agendamento temporal. Está agendada para executar todos os dias às 22h.

# 🛠️ Testes
O projeto inclui testes automatizados para garantir que as etapas de extração e transformação estejam funcionando corretamente:

**Testes de extração:** Localizados em tests/extract_test.py.

**Testes de transformação:** Localizados em tests/transform_test.py.

Executar:

```docker exec -it projetobees-airflow-webserver-1 /bin/bash```

Instalar o PYTEST

```pip install pytest```

Executar os testes:

```pytest tests/extract_test.py```

```pytest tests/transform_test.py```

# ⚠️ Monitoramento/Alertas

**Foram incluídos os seguintes monitoramentos:**

Logs detalhados nas tasks (extract, transform, aggregate) usando logging do Python para registrar o que foi feito em cada etapa.

Retries e timeout configurados em cada tarefa da DAG, para evitar falhas silenciosas.

Alertas automáticos por e-mail em caso de falha de qualquer tarefa no Airflow:

Exemplo:

```
default_args = {
    'owner': 'airflow',
    'retries': 2,
    'retry_delay': timedelta(minutes=5),
    'email_on_failure': True,
    'email': ['colocar o email aqui'],
}
```
