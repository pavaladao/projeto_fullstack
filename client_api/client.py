from flask import Flask, request, jsonify, render_template
import requests

app = Flask(__name__)


@app.route('/')
def home():
    return render_template('home.html')


@app.route('/aluguel', methods=['GET', 'POST'])
def aluguel():
    resultados_aluguel = None

    if request.method == 'GET':
        id_aluguel = request.args.get('aluguel')

        if id_aluguel:
            url_aluguel = 'http://127.0.0.1:3001/alugueis/{}'.format(
                id_aluguel)
            # Faz uma requisição GET para a API
            response = requests.get(url_aluguel)

            # Verifica se a requisição foi bem-sucedida
            if response.status_code == 200:
                # Retorna os dados da API como JSON
                resultados_aluguel = response.json()
            else:
                # Retorna None se a requisição falhar
                resultados_aluguel = None

        # Renderiza o template HTML com os resultados da pesquisa
        return render_template('aluguel.html', resultados_aluguel=resultados_aluguel)

    # Renderiza o formulário HTML para input da pesquisa
    return render_template('aluguel.html')


@app.route('/pessoa', methods=['GET', 'POST'])
def pessoa():
    resultados_pessoa = None

    if request.method == 'GET':
        cpf_pessoa = request.args.get('pessoa')

        if cpf_pessoa:
            # Define a URL da API a ser consumida
            url_pessoa = 'http://127.0.0.1:3000/pessoas/{}'.format(cpf_pessoa)

            # Faz uma requisição GET para a API
            response = requests.get(url_pessoa)

            # Verifica se a requisição foi bem-sucedida
            if response.status_code == 200:
                # Retorna os dados da API como JSON
                resultados_pessoa = response.json()
            else:
                # Retorna None se a requisição falhar
                resultados_pessoa = None

        # Renderiza o template HTML com os resultados da pesquisa
        return render_template('pessoa.html', resultados_pessoa=resultados_pessoa)

    # Renderiza o formulário HTML para input da pesquisa
    return render_template('pessoa.html')


if __name__ == '__main__':
    app.run(debug=True, port=5000)
