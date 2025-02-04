from flask import Flask, jsonify, request
from main import app, con

@app.route('/livro',methods=['GET'])
def livro():
    cur = con.cursor()
    cur.execute("select id_livro, titulo, autor, ano_publicacao from livros")
    livros = cur.fetchall()
    livros_dic = []
    for livro in livros:
        livros_dic.append({
            'id_livro': livro[0],
            'titulo': livro[1],
            'autor': livro[2],
            'ano_publicacao': livro[3]
        })
    return jsonify(mensagem='listas de livros', livros=livros_dic)


@app.route('/livro',  methods=['POST'])
def livro_post():
    data = request.get_json()
    titulo = data.get('titulo')
    autor = data.get('autor')
    ano_publicacao = data.get('ano_publicacao')

    cursor = con.cursor()
    cursor.execute("SELECT 1 FROM LIVROS WHERE TITULO = ?", (titulo,))

    if cursor.fetchone():
        return jsonify({'error': 'Livro já existente'}), 400

    cursor.execute("INSERT INTO LIVROS(TITULO, AUTOR, ANO_PUBLICACAO) VALUES  (?, ?, ?)", (titulo, autor, ano_publicacao))
    con.commit()
    cursor.close()

    return jsonify({
         'message': "Livro criado com sucesso",
         'livro': {
             'titulo': titulo,
             'autor': autor,
             'ano_publicacao': ano_publicacao
        }
    })

@app.route('/livro/<int:id>', methods = ['PUT'])
def livros_put(id):
    cursor = con.cursor()
    cursor.execute("SELECT id_livro FROM livros WHERE id_livro = ?", (id,))
    livro_data = cursor.fetchone()

    if not livro_data:
        cursor.close()
        return jsonify({"error": "livro não foi encontrado"}), 404

    data = request.get_json()
    titulo = data.get('titulo')
    autor = data.get('autor')
    ano_publicacao = data.get('ano_publicacao')

    cursor.execute("UPDATE livros SET titulo = ?, autor = ?, ano_publicacao = ? WHERE id_livro = ?", (titulo, autor, ano_publicacao, id))

    con.commit()
    cursor.close()

    return jsonify({
        'message': "Livro atualizado com sucesso!",
        'livro': {
            'titulo': titulo,
            'autor': autor,
            'ano_publicacao': ano_publicacao
        }
    })

