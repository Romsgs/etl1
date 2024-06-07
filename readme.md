# APS Data Viz

## Instruções de Configuração

Siga estes passos para configurar o ambiente virtual e instalar as dependências.

### Criando e Ativando o Ambiente Virtual

#### No Windows

1. Create a virtual environment:

```bash
python -m venv venv
```

2. Activate the virtual environment:

```bash
./venv/Scripts/activate
```

### Installing Dependencies

Instale todas as dependências necessárias executando:

```bash
pip install -r requirements.txt
```

## Para executar:

para o programa que busca pelos arquivos json direto na APS
`streamlit run app.py`
para o programa que transforma os jsons obtidos com o script anterior em arquivos excel (markup e checklist) com um sufixo para melhor localização
`streamlit run inputETL.py`

caso o terminal não encontre o comando streamlit, o mesmo se encontra na pasta /venv/scripts/streamlit.cmd executando da seguinte maneira
`/venv/scripts/streamlit.cmd run arquivo`

##### o aplicativo roda automaticamente em uma nova janela do browser padrão

### detalhes da busca

no arquivo go.py / selected functions/ folder.py ta a logica do regex pra bsucar apenas por arquivos ED-MOD ou PR-MOD bem como a extensao dos arquivos

# Aplicativo para Criar Arquivos Excel (XLSX) a partir de JSON de Resposta APS

Este aplicativo converte respostas JSON do APS em arquivos Excel (XLSX).

```bash
streamlit run inputETL.py
```

## File Management

- **pasta input**: os arquivos JSON destinados à conversão serão baixados na pasta input.
- **pasta output**: O aplicativo salvará os arquivos Excel convertidos na pasta output.
