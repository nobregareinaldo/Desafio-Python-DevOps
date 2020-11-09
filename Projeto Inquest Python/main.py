import pymysql
from app import app
from db_config import mysql
from flask import jsonify, request, Flask, redirect, url_for, render_template

@app.route("/")
def home():
    'Renderizar pagina inicial - HTML.'
    return render_template("index.html")

# __Pessoas__ - /pessoas (GET, POST)
@app.route('/pessoas')
def pessoas():
    'Listar todas as pessoas cadastradas.'
    try:
        conn = mysql.connect()
        cursor = conn.cursor(pymysql.cursors.DictCursor)
        cursor.execute("SELECT * FROM db_inquest.tb_pessoas")
        rows = cursor.fetchall()
        return render_template('/pessoas/pessoas.html', rows = rows)
    except Exception as e:
        print(e)
    finally:
        cursor.close()
        conn.close()

@app.route('/pessoas/cadastrar', methods=["POST", "GET"])
def incluir_pessoas():
    'Cadastrar pessoas no sistema.'
    if request.method == "POST":
        try:
            _nome		= request.form['pessoas_nome']
            _sobrenome	= request.form['pessoas_sobrenome']
            _cpf		= request.form['pessoas_cpf']
            _email		= request.form['pessoas_email']
            _end_com	= request.form['pessoas_end_com']
            _end_res	= request.form['pessoas_end_res']
            _cidade     = request.form['pessoas_cidade']
            _estado     = request.form['pessoas_estado']
            _pais		= request.form['pessoas_pais']
            _telefone	= request.form['pessoas_telefone']
            _celular	= request.form['pessoas_celular']
            
            if _nome and _sobrenome and _email:
                sql = "INSERT INTO db_inquest.tb_pessoas\
                    (\
                    pessoas_nome,\
                    pessoas_sobrenome,\
                    pessoas_cpf,\
                    pessoas_email,\
                    pessoas_end_com,\
                    pessoas_end_res,\
                    pessoas_cidade,\
                    pessoas_estado,\
                    pessoas_pais,\
                    pessoas_telefone,\
                    pessoas_celular\
                    )\
                    VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
                data = (_nome, _sobrenome, _cpf, _email, _end_com, _end_res, _cidade, _estado, _pais, _telefone, _celular)
                conn = mysql.connect()
                cursor = conn.cursor()
                cursor.execute(sql, data)
                conn.commit()
                return redirect(url_for("pessoas"))
            else:
                return not_found()
        except Exception as e:
                print(e)
        finally:
            cursor.close()
            conn.close()
    else:
        return render_template("/pessoas/pessoas_cadastrar.html")

@app.route("/pessoas/alterar", methods=["POST", "GET"])
def pessoas_alterar():
    'Consultar pessoas cadastradas pelo ID, função utlizada para fins de atualizacao.'
    if request.method == "POST":
        _id = request.form['pessoas_id']
        return redirect(url_for("update_pessoas", id=_id))
    else:
        return render_template("/pessoas/pessoas_buscar_id.html")

@app.route('/pessoas/update/<int:id>', methods=["POST", "GET"])
def update_pessoas(id):
    'Alterar cadastro de pessoa a partir do ID.'
    if request.method == "POST":
        try:
            _id         = id
            _nome		= request.form['pessoas_nome']
            _sobrenome	= request.form['pessoas_sobrenome']
            _cpf		= request.form['pessoas_cpf']
            _email		= request.form['pessoas_email']
            _end_com	= request.form['pessoas_end_com']
            _end_res	= request.form['pessoas_end_res']
            _cidade     = request.form['pessoas_cidade']
            _estado     = request.form['pessoas_estado']
            _pais		= request.form['pessoas_pais']
            _telefone	= request.form['pessoas_telefone']
            _celular	= request.form['pessoas_celular']
            
            if _nome and _sobrenome and _email:
                sql = "UPDATE db_inquest.tb_pessoas SET\
                    pessoas_nome=%s,\
                    pessoas_sobrenome=%s,\
                    pessoas_cpf=%s,\
                    pessoas_email=%s,\
                    pessoas_end_com=%s,\
                    pessoas_end_res=%s,\
                    pessoas_cidade=%s,\
                    pessoas_estado=%s,\
                    pessoas_pais=%s,\
                    pessoas_telefone=%s,\
                    pessoas_celular=%s\
                    WHERE pessoas_id=%s"
                data = (_nome, _sobrenome, _cpf, _email, _end_com, _end_res, _cidade, _estado, _pais, _telefone, _celular, _id)
                conn = mysql.connect()
                cursor = conn.cursor()
                cursor.execute(sql, data)
                conn.commit()
                return redirect(url_for("pessoas"))
            else:
                return not_found()
        except Exception as e:
                print(e)
        finally:
            cursor.close()
            conn.close()
    elif id == 0:
        return render_template("/pessoas/pessoas_buscar_id.html")
    else:
        try:
            _id = id
            conn = mysql.connect()
            cursor = conn.cursor(pymysql.cursors.DictCursor)
            cursor.execute("SELECT * FROM db_inquest.tb_pessoas WHERE pessoas_id = %s", id)
            rows = cursor.fetchall()
            return render_template('/pessoas/pessoas_alterar.html', rows = rows)
        except Exception as e:
            print(e)
        finally:
            cursor.close()
            conn.close()

@app.route("/pessoas/excluir", methods=["POST", "GET"])
def pessoas_excluir():
    'Consultar pessoas cadastradas pelo ID, função utlizada para fins de delecao.'
    if request.method == "POST":
        _id = request.form['pessoas_id']
        return redirect(url_for("delete_pessoas", id=_id))
    else:
        return render_template("/pessoas/pessoas_buscar_id.html")

@app.route('/pessoas/delete/<int:id>', methods=["POST", "GET"])
def delete_pessoas(id):
    'Excluir cadastro de pessoa a partir do ID.'
    if request.method == "POST":
        try:
            _id = id
            
            if _id:
                sql = "DELETE FROM db_inquest.tb_pessoas WHERE pessoas_id=%s"
                data = (_id)
                conn = mysql.connect()
                cursor = conn.cursor()
                cursor.execute(sql, data)
                conn.commit()
                return redirect(url_for("pessoas"))
            else:
                return not_found()
        except Exception as e:
                print(e)
        finally:
            cursor.close()
            conn.close()
    elif id == 0:
        return render_template("/pessoas/pessoas_buscar_id.html")
    else:
        try:
            _id = id
            conn = mysql.connect()
            cursor = conn.cursor(pymysql.cursors.DictCursor)
            cursor.execute("SELECT * FROM db_inquest.tb_pessoas WHERE pessoas_id = %s", id)
            rows = cursor.fetchall()
            return render_template('/pessoas/pessoas_excluir.html', rows = rows)
        except Exception as e:
            print(e)
        finally:
            cursor.close()
            conn.close()

@app.route("/pessoas/buscar", methods=["POST", "GET"])
def pessoas_buscar():
    'Consultar pessoas cadastradas pelo ID - renderização de HTML.'
    if request.method == "POST":
        _id = request.form['pessoas_id']
        return redirect(url_for("pessoas_por_id", id=_id))
    else:
        return render_template("/pessoas/pessoas_buscar_id.html")

@app.route('/pessoas/<int:id>')
def pessoas_por_id(id):
    'Consultar pessoas cadastradas pelo ID.'
    try:
        _id = id

        conn = mysql.connect()
        cursor = conn.cursor(pymysql.cursors.DictCursor)
        cursor.execute("SELECT * FROM db_inquest.tb_pessoas WHERE pessoas_id = %s", id)
        rows = cursor.fetchall()
        return render_template('/pessoas/pessoas.html', rows = rows)
    except Exception as e:
        print(e)
    finally:
        cursor.close()
        conn.close()

# __Empresas__ - /empresas (GET, POST)
@app.route('/empresas')
def empresas():
    'Listar todas as empresas cadastradas.'
    try:
        conn = mysql.connect()
        cursor = conn.cursor(pymysql.cursors.DictCursor)
        cursor.execute("SELECT * FROM db_inquest.tb_empresas")
        rows = cursor.fetchall()
        return render_template('/empresas/empresas.html', rows = rows)
    except Exception as e:
        print(e)
    finally:
        cursor.close()
        conn.close()

@app.route('/empresas/cadastrar', methods=["POST", "GET"])
def incluir_empresas():
    'Cadastrar empresas no sistema.'
    if request.method == "POST":
        try:
            _razao		= request.form['empresas_razao']
            _fantasia	= request.form['empresas_fantasia']
            _cnpj		= request.form['empresas_cnpj']
            _email		= request.form['empresas_email']
            _end_com	= request.form['empresas_end_com']
            _end_cobr	= request.form['empresas_end_cobr']
            _cidade		= request.form['empresas_cidade']
            _estado		= request.form['empresas_estado']
            _pais		= request.form['empresas_pais']
            _telefone	= request.form['empresas_telefone']
            _celular	= request.form['empresas_celular']
            
            if _razao and _fantasia and _cnpj:
                sql = "INSERT INTO db_inquest.tb_empresas\
                    (\
                    empresas_razao,\
					empresas_fantasia,\
					empresas_cnpj,\
					empresas_email,\
					empresas_end_com,\
					empresas_end_cobr,\
					empresas_cidade,\
					empresas_estado,\
					empresas_pais,\
					empresas_telefone,\
					empresas_celular\
                    )\
                    VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
                data = (_razao, _fantasia, _cnpj, _email, _end_com, _end_cobr, _cidade, _estado, _pais, _telefone, _celular)
                conn = mysql.connect()
                cursor = conn.cursor()
                cursor.execute(sql, data)
                conn.commit()
                return redirect(url_for("empresas"))
            else:
                return not_found()
        except Exception as e:
                print(e)
        finally:
            cursor.close()
            conn.close()
    else:
        return render_template("/empresas/empresas_cadastrar.html")

@app.route("/empresas/alterar", methods=["POST", "GET"])
def empresas_alterar():
    'Consultar empresas cadastradas pelo ID, função utlizada para fins de atualizacao.'
    if request.method == "POST":
        _id = request.form['empresas_id']
        return redirect(url_for("update_empresas", id=_id))
    else:
        return render_template("/empresas/empresas_buscar_id.html")

@app.route('/empresas/update/<int:id>', methods=["POST", "GET"])
def update_empresas(id):
    'Alterar cadastro de empresa a partir do ID.'
    if request.method == "POST":
        try:
            _id         = id
            _razao		= request.form['empresas_razao']
            _fantasia	= request.form['empresas_fantasia']
            _cnpj		= request.form['empresas_cnpj']
            _email		= request.form['empresas_email']
            _end_com	= request.form['empresas_end_com']
            _end_cobr	= request.form['empresas_end_cobr']
            _cidade		= request.form['empresas_cidade']
            _estado		= request.form['empresas_estado']
            _pais		= request.form['empresas_pais']
            _telefone	= request.form['empresas_telefone']
            _celular	= request.form['empresas_celular']
            
            if _id and _razao and _fantasia and _cnpj:
                sql = "UPDATE db_inquest.tb_empresas SET\
					empresas_razao=%s,\
					empresas_fantasia=%s,\
					empresas_cnpj=%s,\
					empresas_email=%s,\
					empresas_end_com=%s,\
					empresas_end_cobr=%s,\
					empresas_cidade=%s,\
					empresas_estado=%s,\
					empresas_pais=%s,\
					empresas_telefone=%s,\
					empresas_celular=%s\
                    WHERE empresas_id=%s"
                data = (_razao, _fantasia, _cnpj, _email, _end_com, _end_cobr, _cidade, _estado, _pais, _telefone, _celular, _id)
                conn = mysql.connect()
                cursor = conn.cursor()
                cursor.execute(sql, data)
                conn.commit()
                return redirect(url_for("empresas"))
            else:
                return not_found()
        except Exception as e:
                print(e)
        finally:
            cursor.close()
            conn.close()
    elif id == 0:
        return render_template("/empresas/empresas_buscar_id.html")
    else:
        try:
            _id = id

            conn = mysql.connect()
            cursor = conn.cursor(pymysql.cursors.DictCursor)
            cursor.execute("SELECT * FROM db_inquest.tb_empresas WHERE empresas_id = %s", id)
            rows = cursor.fetchall()
            return render_template('/empresas/empresas_alterar.html', rows = rows)
        except Exception as e:
            print(e)
        finally:
            cursor.close()
            conn.close()

@app.route("/empresas/excluir", methods=["POST", "GET"])
def empresas_excluir():
    'Consultar empresas cadastradas pelo ID, função utlizada para fins de delecao.'
    if request.method == "POST":
        _id = request.form['empresas_id']
        return redirect(url_for("delete_empresas", id=_id))
    else:
        return render_template("/empresas/empresas_buscar_id.html")

@app.route('/empresas/delete/<int:id>', methods=["POST", "GET"])
def delete_empresas(id):
    'Excluir cadastro de empresa a partir do ID.'
    if request.method == "POST":
        try:
            _id = id
            
            if _id:
                sql = "DELETE FROM db_inquest.tb_empresas WHERE empresas_id=%s"
                data = (_id)
                conn = mysql.connect()
                cursor = conn.cursor()
                cursor.execute(sql, data)
                conn.commit()
                return redirect(url_for("empresas"))
            else:
                return not_found()
        except Exception as e:
                print(e)
        finally:
            cursor.close()
            conn.close()
    elif id == 0:
        return render_template("/empresas/empresas_buscar_id.html")
    else:
        try:
            _id = id

            conn = mysql.connect()
            cursor = conn.cursor(pymysql.cursors.DictCursor)
            cursor.execute("SELECT * FROM db_inquest.tb_empresas WHERE empresas_id = %s", id)
            rows = cursor.fetchall()
            return render_template('/empresas/empresas_excluir.html', rows = rows)
        except Exception as e:
            print(e)
        finally:
            cursor.close()
            conn.close()

@app.route("/empresas/buscar", methods=["POST", "GET"])
def empresas_buscar():
    'Consultar empresas cadastradas pelo ID - renderização de HTML.'
    if request.method == "POST":
        _id = request.form['empresas_id']
        return redirect(url_for("empresas_por_id", id=_id))
    else:
        return render_template("/empresas/empresas_buscar_id.html")

@app.route('/empresas/<int:id>')
def empresas_por_id(id):
    'Consultar empresas cadastradas pelo ID.'
    try:
        _id = id

        conn = mysql.connect()
        cursor = conn.cursor(pymysql.cursors.DictCursor)
        cursor.execute("SELECT * FROM db_inquest.tb_empresas WHERE empresas_id = %s", id)
        rows = cursor.fetchall()
        return render_template('/empresas/empresas.html', rows = rows)
    except Exception as e:
        print(e)
    finally:
        cursor.close()
        conn.close()

# __Bens__ - /bens (GET, POST)
@app.route('/bens')
def bens():
    'Listar todos os bens cadastrados.'
    try:
        conn = mysql.connect()
        cursor = conn.cursor(pymysql.cursors.DictCursor)
        cursor.execute("SELECT * FROM db_inquest.tb_bens")
        rows = cursor.fetchall()
        return render_template('/bens/bens.html', rows = rows)
    except Exception as e:
        print(e)
    finally:
        cursor.close()
        conn.close()

@app.route('/bens/cadastrar', methods=["POST", "GET"])
def incluir_bens():
    'Cadastrar bens no sistema.'
    if request.method == "POST":
        try:
            _descricao = request.form['bens_descricao']
            _situacao  = request.form['bens_situacao']
            
            if _descricao and _situacao:
                sql = "INSERT INTO db_inquest.tb_bens\
                    (\
					bens_descricao,\
					bens_situacao\
                    )\
                    VALUES(%s, %s)"
                data = (_descricao, _situacao)
                conn = mysql.connect()
                cursor = conn.cursor()
                cursor.execute(sql, data)
                conn.commit()
                return redirect(url_for("bens"))
            else:
                return not_found()
        except Exception as e:
                print(e)
        finally:
            cursor.close()
            conn.close()
    else:
        return render_template("/bens/bens_cadastrar.html")

@app.route("/bens/alterar", methods=["POST", "GET"])
def bens_alterar():
    'Consultar bens cadastrados pelo ID, função utlizada para fins de atualizacao.'
    if request.method == "POST":
        _id = request.form['bens_id']
        return redirect(url_for("update_bens", id=_id))
    else:
        return render_template("/bens/bens_buscar_id.html")

@app.route('/bens/update/<int:id>', methods=["POST", "GET"])
def update_bens(id):
    'Alterar cadastro de bem a partir do ID.'
    if request.method == "POST":
        try:
            _id        = id
            _descricao = request.form['bens_descricao']
            _situacao  = request.form['bens_situacao']
            
            if _id and _descricao and _situacao:
                sql = "UPDATE db_inquest.tb_bens SET\
                    bens_descricao=%s,\
                    bens_situacao=%s\
                    WHERE bens_id=%s"
                data = (_descricao, _situacao, _id)
                conn = mysql.connect()
                cursor = conn.cursor()
                cursor.execute(sql, data)
                conn.commit()
                return redirect(url_for("bens"))
            else:
                return not_found()
        except Exception as e:
                print(e)
        finally:
            cursor.close()
            conn.close()
    elif id == 0:
        return render_template("/bens/bens_buscar_id.html")
    else:
        try:
            _id = id

            conn = mysql.connect()
            cursor = conn.cursor(pymysql.cursors.DictCursor)
            cursor.execute("SELECT * FROM db_inquest.tb_bens WHERE bens_id = %s", id)
            rows = cursor.fetchall()
            return render_template('/bens/bens_alterar.html', rows = rows)
        except Exception as e:
            print(e)
        finally:
            cursor.close()
            conn.close()

@app.route("/bens/excluir", methods=["POST", "GET"])
def bens_excluir():
    'Consultar bens cadastrados pelo ID, função utlizada para fins de delecao.'
    if request.method == "POST":
        _id = request.form['bens_id']
        return redirect(url_for("delete_bens", id=_id))
    else:
        return render_template("/bens/bens_buscar_id.html")

@app.route('/bens/delete/<int:id>', methods=["POST", "GET"])
def delete_bens(id):
    'Excluir cadastro de bem a partir do ID.'
    if request.method == "POST":
        try:
            _id = id
            
            if _id:
                sql = "DELETE FROM db_inquest.tb_bens WHERE bens_id=%s"
                data = (_id)
                conn = mysql.connect()
                cursor = conn.cursor()
                cursor.execute(sql, data)
                conn.commit()
                return redirect(url_for("bens"))
            else:
                return not_found()
        except Exception as e:
                print(e)
        finally:
            cursor.close()
            conn.close()
    elif id == 0:
        return render_template("/bens/bens_buscar_id.html")
    else:
        try:
            _id = id

            conn = mysql.connect()
            cursor = conn.cursor(pymysql.cursors.DictCursor)
            cursor.execute("SELECT * FROM db_inquest.tb_bens WHERE bens_id = %s", id)
            rows = cursor.fetchall()
            return render_template('/bens/bens_excluir.html', rows = rows)
        except Exception as e:
            print(e)
        finally:
            cursor.close()
            conn.close()

@app.route("/bens/buscar", methods=["POST", "GET"])
def bens_buscar():
    'Consultar bens cadastrados pelo ID - renderização de HTML.'
    if request.method == "POST":
        _id = request.form['bens_id']
        return redirect(url_for("bens_por_id", id=_id))
    else:
        return render_template("/bens/bens_buscar_id.html")

@app.route('/bens/<int:id>')
def bens_por_id(id):
    'Consultar bens cadastrados pelo ID.'
    try:
        _id = id

        conn = mysql.connect()
        cursor = conn.cursor(pymysql.cursors.DictCursor)
        cursor.execute("SELECT * FROM db_inquest.tb_bens WHERE bens_id = %s", id)
        rows = cursor.fetchall()
        return render_template('/bens/bens.html', rows = rows)
    except Exception as e:
        print(e)
    finally:
        cursor.close()
        conn.close()

# __Socios__ - /socios (GET, POST)
@app.route('/socios')
def socios():
    'Listar todos os socios cadastrados.'
    try:
        conn = mysql.connect()
        cursor = conn.cursor(pymysql.cursors.DictCursor)
        cursor.execute(
            "SELECT \
                t1.socios_id AS socios_id,\
                t2.pessoas_nome AS pessoas_nome,\
                t2.pessoas_sobrenome AS pessoas_sobrenome,\
                t3.empresas_razao AS empresas_razao\
                FROM db_inquest.tb_socios AS t1\
                INNER JOIN db_inquest.tb_pessoas AS t2 ON t1.socios_pessoas_id = t2.pessoas_id\
                INNER JOIN db_inquest.tb_empresas AS t3 ON t1.socios_empresas_id = t3.empresas_id"
        )
        rows = cursor.fetchall()
        return render_template('/socios/socios.html', rows = rows)
    except Exception as e:
        print(e)
    finally:
        cursor.close()
        conn.close()

@app.route('/socios/cadastrar', methods=["POST", "GET"])
def incluir_socios():
    'Cadastrar socios no sistema.'
    if request.method == "POST":
        try:
            _pessoas_id  = request.form['socios_pessoas_id']
            _empresas_id = request.form['socios_empresas_id']
            
            if _pessoas_id and _empresas_id:
                sql = "INSERT INTO db_inquest.tb_socios\
                    (\
					socios_pessoas_id,\
					socios_empresas_id\
                    )\
                    VALUES(%s, %s)"
                data = (_pessoas_id, _empresas_id)
                conn = mysql.connect()
                cursor = conn.cursor()
                cursor.execute(sql, data)
                conn.commit()
                return redirect(url_for("socios"))
            else:
                return not_found()
        except Exception as e:
                print(e)
        finally:
            cursor.close()
            conn.close()
    else:
        combo_pessoas = listar_combo_pessoas()
        combo_empresas = listar_combo_empresas()

        return render_template("/socios/socios_cadastrar.html", pessoas=combo_pessoas, empresas=combo_empresas)

@app.route("/socios/alterar", methods=["POST", "GET"])
def socios_alterar():
    'Consultar socios cadastrados pelo ID, função utlizada para fins de atualizacao.'
    if request.method == "POST":
        _id = request.form['socios_id']
        return redirect(url_for("update_socios", id=_id))
    else:
        return render_template("/socios/socios_buscar_id.html")

@app.route('/socios/update/<int:id>', methods=["POST", "GET"])
def update_socios(id):
    'Alterar cadastro de socio a partir do ID.'
    if request.method == "POST":
        try:
            _id          = id
            _pessoas_id  = request.form['socios_pessoas_id']
            _empresas_id = request.form['socios_empresas_id']
            
            if _id and _pessoas_id and _empresas_id:
                sql = "UPDATE db_inquest.tb_socios SET\
                    socios_pessoas_id=%s,\
                    socios_empresas_id=%s\
                    WHERE socios_id=%s"
                data = (_pessoas_id, _empresas_id, _id)
                conn = mysql.connect()
                cursor = conn.cursor()
                cursor.execute(sql, data)
                conn.commit()
                return redirect(url_for("socios"))
            else:
                return not_found()
        except Exception as e:
                print(e)
        finally:
            cursor.close()
            conn.close()
    elif id == 0:
        return render_template("/socios/socios_buscar_id.html")
    else:
        try:
            _id = id

            conn = mysql.connect()
            cursor = conn.cursor(pymysql.cursors.DictCursor)
            cursor.execute(
                "SELECT \
                    t1.socios_id AS socios_id,\
                    t1.socios_pessoas_id AS socios_pessoas_id,\
                    t1.socios_empresas_id AS socios_empresas_id,\
                    IFNULL(t2.pessoas_nome, '---') AS pessoas_nome,\
                    IFNULL(t2.pessoas_sobrenome, '') AS pessoas_sobrenome,\
                    IFNULL(t3.empresas_razao, '---') AS empresas_razao\
                FROM db_inquest.tb_socios AS t1\
                LEFT JOIN db_inquest.tb_pessoas AS t2 ON t1.socios_pessoas_id = t2.pessoas_id\
                LEFT JOIN db_inquest.tb_empresas AS t3 ON t1.socios_empresas_id = t3.empresas_id\
                    WHERE socios_id = %s", id
            )
            rows = cursor.fetchall()

            combo_pessoas = listar_combo_pessoas()
            combo_empresas = listar_combo_empresas()
            return render_template('/socios/socios_alterar.html', rows = rows, pessoas=combo_pessoas, empresas=combo_empresas)
        except Exception as e:
            print(e)
        finally:
            cursor.close()
            conn.close()

@app.route("/socios/excluir", methods=["POST", "GET"])
def socios_excluir():
    'Consultar socios cadastrados pelo ID, função utlizada para fins de delecao.'
    if request.method == "POST":
        _id = request.form['socios_id']
        return redirect(url_for("delete_socios", id=_id))
    else:
        return render_template("/socios/socios_buscar_id.html")

@app.route('/socios/delete/<int:id>', methods=["POST", "GET"])
def delete_socios(id):
    'Excluir cadastro de socio a partir do ID.'
    if request.method == "POST":
        try:
            _id = id
            
            if _id:
                sql = "DELETE FROM db_inquest.tb_socios WHERE socios_id=%s"
                data = (_id)
                conn = mysql.connect()
                cursor = conn.cursor()
                cursor.execute(sql, data)
                conn.commit()
                return redirect(url_for("socios"))
            else:
                return not_found()
        except Exception as e:
                print(e)
        finally:
            cursor.close()
            conn.close()
    elif id == 0:
        return render_template("/socios/socios_buscar_id.html")
    else:
        try:
            _id = id

            conn = mysql.connect()
            cursor = conn.cursor(pymysql.cursors.DictCursor)
            cursor.execute(
                "SELECT \
                    t1.socios_id AS socios_id,\
                    t1.socios_pessoas_id AS socios_pessoas_id,\
                    t1.socios_empresas_id AS socios_empresas_id,\
                    IFNULL(t2.pessoas_nome, '---') AS pessoas_nome,\
                    IFNULL(t2.pessoas_sobrenome, '') AS pessoas_sobrenome,\
                    IFNULL(t2.pessoas_cpf, '') AS pessoas_cpf,\
                    IFNULL(t3.empresas_razao, '---') AS empresas_razao,\
                    IFNULL(t3.empresas_cnpj, '---') AS empresas_cnpj\
                FROM db_inquest.tb_socios AS t1\
                LEFT JOIN db_inquest.tb_pessoas AS t2 ON t1.socios_pessoas_id = t2.pessoas_id\
                LEFT JOIN db_inquest.tb_empresas AS t3 ON t1.socios_empresas_id = t3.empresas_id\
                    WHERE socios_id = %s", id
            )
            rows = cursor.fetchall()
            return render_template('/socios/socios_excluir.html', rows = rows)
        except Exception as e:
            print(e)
        finally:
            cursor.close()
            conn.close()

@app.route("/socios/buscar", methods=["POST", "GET"])
def socios_buscar():
    'Consultar socios cadastrados pelo ID - renderização de HTML.'
    if request.method == "POST":
        _id = request.form['socios_id']
        return redirect(url_for("socios_por_id", id=_id))
    else:
        return render_template("/socios/socios_buscar_id.html")

@app.route('/socios/<int:id>')
def socios_por_id(id):
    'Consultar socios cadastrados pelo ID.'
    try:
        _id = id

        conn = mysql.connect()
        cursor = conn.cursor(pymysql.cursors.DictCursor)
        cursor.execute(
            "SELECT \
                t1.socios_id AS socios_id,\
                t2.pessoas_nome AS pessoas_nome,\
                t2.pessoas_sobrenome AS pessoas_sobrenome,\
                t3.empresas_razao AS empresas_razao\
                FROM db_inquest.tb_socios AS t1\
                INNER JOIN db_inquest.tb_pessoas AS t2 ON t1.socios_pessoas_id = t2.pessoas_id\
                INNER JOIN db_inquest.tb_empresas AS t3 ON t1.socios_empresas_id = t3.empresas_id\
                WHERE socios_id = %s", id)
        rows = cursor.fetchall()
        return render_template('/socios/socios.html', rows = rows)
    except Exception as e:
        print(e)
    finally:
        cursor.close()
        conn.close()

# __Patrimonio__ - /patrimonio (GET, POST)
@app.route('/patrimonio')
def patrimonios():
    'Listar todos os patrimonios cadastrados.'
    try:
        conn = mysql.connect()
        cursor = conn.cursor(pymysql.cursors.DictCursor)
        cursor.execute(
            "SELECT \
                t1.patr_id AS patr_id,\
                IFNULL(t2.pessoas_nome, '---') AS pessoas_nome,\
                IFNULL(t2.pessoas_sobrenome, '') AS pessoas_sobrenome,\
                IFNULL(t3.empresas_razao, '---') AS empresas_razao,\
                t4.bens_descricao as bens_descricao\
                FROM db_inquest.tb_patrimonio AS t1\
                LEFT JOIN db_inquest.tb_pessoas AS t2 ON t1.patr_pessoas_id = t2.pessoas_id\
                LEFT JOIN db_inquest.tb_empresas AS t3 ON t1.patr_empresas_id = t3.empresas_id\
                INNER JOIN db_inquest.tb_bens AS t4 ON t1.patr_bens_id = t4.bens_id"
        )
        rows = cursor.fetchall()
        return render_template('/patrimonio/patrimonios.html', rows = rows)
    except Exception as e:
        print(e)
    finally:
        cursor.close()
        conn.close()

@app.route('/patrimonio/cadastrar', methods=["POST", "GET"])
def incluir_patr():
    'Cadastrar patrimonios no sistema.'
    if request.method == "POST":
        try:
            _pessoas_id  = request.form['patr_pessoas_id']
            _empresas_id = request.form['patr_empresas_id']
            _bens_id     = request.form['patr_bens_id']

            if not _pessoas_id: _pessoas_id = 0
            if not _empresas_id: _empresas_id = 0
            
            if _bens_id:
                sql = "INSERT INTO db_inquest.tb_patrimonio\
                    (\
					patr_pessoas_id,\
					patr_empresas_id,\
                    patr_bens_id\
                    )\
                    VALUES(%s, %s, %s)"
                data = (_pessoas_id, _empresas_id, _bens_id)
                conn = mysql.connect()
                cursor = conn.cursor()
                cursor.execute(sql, data)
                conn.commit()
                return redirect(url_for("patrimonios"))
            else:
                return not_found()
        except Exception as e:
                print(e)
        finally:
            cursor.close()
            conn.close()
    else:
        combo_pessoas = listar_combo_pessoas()
        combo_empresas = listar_combo_empresas()
        combo_bens = listar_combo_bens()
        return render_template("/patrimonio/patrimonios_cadastrar.html", bens=combo_bens, pessoas=combo_pessoas, empresas=combo_empresas)

@app.route("/patrimonio/alterar", methods=["POST", "GET"])
def patr_alterar():
    'Consultar patrimonios cadastrados pelo ID, função utlizada para fins de atualizacao.'
    if request.method == "POST":
        _id = request.form['patr_id']
        return redirect(url_for("update_patr", id=_id))
    else:
        return render_template("/patrimonio/patrimonios_buscar_id.html")

@app.route('/patrimonio/update/<int:id>', methods=["POST", "GET"])
def update_patr(id):
    'Alterar cadastro de patrimonio a partir do ID.'
    if request.method == "POST":
        try:
            _id          = id
            _pessoas_id  = request.form['patr_pessoas_id']
            _empresas_id = request.form['patr_empresas_id']
            _bens_id     = request.form['patr_bens_id']

            if _id and _pessoas_id and _empresas_id and _bens_id:
                sql = "UPDATE db_inquest.tb_patrimonio SET\
                    patr_pessoas_id=%s,\
                    patr_empresas_id=%s,\
                    patr_bens_id=%s\
                    WHERE patr_id=%s"
                data = (_pessoas_id, _empresas_id, _bens_id, _id)
                conn = mysql.connect()
                cursor = conn.cursor()
                cursor.execute(sql, data)
                conn.commit()
                return redirect(url_for("patrimonios"))
            else:
                return not_found()
        except Exception as e:
                print(e)
        finally:
            cursor.close()
            conn.close()
    elif id == 0:
        return render_template("/patrimonio/patrimonios_buscar_id.html")
    else:
        try:
            _id = id

            conn = mysql.connect()
            cursor = conn.cursor(pymysql.cursors.DictCursor)
            cursor.execute(
                "SELECT \
                    t1.patr_id AS patr_id,\
                    t1.patr_pessoas_id AS patr_pessoas_id,\
                    t1.patr_empresas_id AS patr_empresas_id,\
                    t1.patr_bens_id AS patr_bens_id,\
                    IFNULL(t2.pessoas_nome, '---') AS pessoas_nome,\
                    IFNULL(t2.pessoas_sobrenome, '') AS pessoas_sobrenome,\
                    IFNULL(t3.empresas_razao, '---') AS empresas_razao,\
                    t4.bens_descricao as bens_descricao\
                FROM db_inquest.tb_patrimonio AS t1\
                LEFT JOIN db_inquest.tb_pessoas AS t2 ON t1.patr_pessoas_id = t2.pessoas_id\
                LEFT JOIN db_inquest.tb_empresas AS t3 ON t1.patr_empresas_id = t3.empresas_id\
                INNER JOIN db_inquest.tb_bens AS t4 ON t1.patr_bens_id = t4.bens_id\
                    WHERE patr_id = %s", id
            )
            rows = cursor.fetchall()

            combo_bens = listar_combo_bens()
            combo_pessoas = listar_combo_pessoas()
            combo_empresas = listar_combo_empresas()
            return render_template('/patrimonio/patrimonios_alterar.html', rows = rows, bens=combo_bens, pessoas=combo_pessoas, empresas=combo_empresas)
        except Exception as e:
            print(e)
        finally:
            cursor.close()
            conn.close()

@app.route("/patrimonio/excluir", methods=["POST", "GET"])
def patr_excluir():
    'Consultar patrimonios cadastrados pelo ID, função utlizada para fins de delecao.'
    if request.method == "POST":
        _id = request.form['patr_id']
        return redirect(url_for("delete_patr", id=_id))
    else:
        return render_template("/patrimonio/patrimonios_buscar_id.html")

@app.route('/patrimonio/delete/<int:id>', methods=["POST", "GET"])
def delete_patr(id):
    'Excluir cadastro de patrimonio a partir do ID.'
    if request.method == "POST":
        try:
            _id = id
            
            if _id:
                sql = "DELETE FROM db_inquest.tb_patrimonio WHERE patr_id=%s"
                data = (_id)
                conn = mysql.connect()
                cursor = conn.cursor()
                cursor.execute(sql, data)
                conn.commit()
                return redirect(url_for("patrimonios"))
            else:
                return not_found()
        except Exception as e:
                print(e)
        finally:
            cursor.close()
            conn.close()
    elif id == 0:
        return render_template("/patrimonio/patrimonios_buscar_id.html")
    else:
        try:
            _id = id

            conn = mysql.connect()
            cursor = conn.cursor(pymysql.cursors.DictCursor)
            cursor.execute(
                "SELECT \
                    t1.patr_id AS patr_id,\
                    t1.patr_pessoas_id AS patr_pessoas_id,\
                    t1.patr_empresas_id AS patr_empresas_id,\
                    t1.patr_bens_id AS patr_bens_id,\
                    IFNULL(t2.pessoas_nome, '---') AS pessoas_nome,\
                    IFNULL(t2.pessoas_sobrenome, '') AS pessoas_sobrenome,\
                    IFNULL(t2.pessoas_cpf, '') AS pessoas_cpf,\
                    IFNULL(t3.empresas_razao, '---') AS empresas_razao,\
                    IFNULL(t3.empresas_cnpj, '---') AS empresas_cnpj,\
                    t4.bens_descricao as bens_descricao\
                FROM db_inquest.tb_patrimonio AS t1\
                LEFT JOIN db_inquest.tb_pessoas AS t2 ON t1.patr_pessoas_id = t2.pessoas_id\
                LEFT JOIN db_inquest.tb_empresas AS t3 ON t1.patr_empresas_id = t3.empresas_id\
                INNER JOIN db_inquest.tb_bens AS t4 ON t1.patr_bens_id = t4.bens_id\
                    WHERE patr_id = %s", id
            )
            rows = cursor.fetchall()
            return render_template('/patrimonio/patrimonios_excluir.html', rows = rows)
        except Exception as e:
            print(e)
        finally:
            cursor.close()
            conn.close()

@app.route("/patrimonio/buscar", methods=["POST", "GET"])
def patr_buscar():
    'Consultar patrimonios cadastrados pelo ID - renderização de HTML.'
    if request.method == "POST":
        _id = request.form['patr_id']
        return redirect(url_for("patr_por_id", id=_id))
    else:
        return render_template("/patrimonio/patrimonios_buscar_id.html")

@app.route('/patrimonio/<int:id>')
def patr_por_id(id):
    'Consultar patrimonios cadastrados pelo ID.'
    try:
        _id = id

        conn = mysql.connect()
        cursor = conn.cursor(pymysql.cursors.DictCursor)
        cursor.execute(
            "SELECT \
                t1.patr_id AS patr_id,\
                IFNULL(t2.pessoas_nome, '---') AS pessoas_nome,\
                IFNULL(t2.pessoas_sobrenome, '') AS pessoas_sobrenome,\
                IFNULL(t3.empresas_razao, '---') AS empresas_razao,\
                t4.bens_descricao as bens_descricao\
                FROM db_inquest.tb_patrimonio AS t1\
                LEFT JOIN db_inquest.tb_pessoas AS t2 ON t1.patr_pessoas_id = t2.pessoas_id\
                LEFT JOIN db_inquest.tb_empresas AS t3 ON t1.patr_empresas_id = t3.empresas_id\
                INNER JOIN db_inquest.tb_bens AS t4 ON t1.patr_bens_id = t4.bens_id\
                WHERE patr_id = %s", id
        )
        rows = cursor.fetchall()
        return render_template('/patrimonio/patrimonios.html', rows = rows)
    except Exception as e:
        print(e)
    finally:
        cursor.close()
        conn.close()

def listar_combo_pessoas():
    'Listar todas as pessoas cadastradas no sistema para alimentar um combo.'
    try:
        conn = mysql.connect()
        cursor = conn.cursor(pymysql.cursors.DictCursor)
        cursor.execute("SELECT pessoas_id, pessoas_nome, pessoas_sobrenome, pessoas_cpf FROM db_inquest.tb_pessoas")
        pessoas = cursor.fetchall()

        return pessoas
    except Exception as e:
        print(e)
    finally:
        cursor.close()
        conn.close()

def listar_combo_empresas():
    'Listar todas as empresas cadastradas no sistema para alimentar um combo.'
    try:
        conn = mysql.connect()
        cursor = conn.cursor(pymysql.cursors.DictCursor)
        cursor.execute("SELECT empresas_id, empresas_razao, empresas_cnpj FROM db_inquest.tb_empresas")
        empresas = cursor.fetchall()

        return empresas
    except Exception as e:
        print(e)
    finally:
        cursor.close()
        conn.close()

def listar_combo_bens():
    'Listar todos os bens cadastrados no sistema para alimentar um combo.'
    try:
        conn = mysql.connect()
        cursor = conn.cursor(pymysql.cursors.DictCursor)
        cursor.execute("SELECT bens_id, bens_descricao, bens_situacao FROM db_inquest.tb_bens")
        bens = cursor.fetchall()

        return bens
    except Exception as e:
        print(e)
    finally:
        cursor.close()
        conn.close()

@app.errorhandler(404)
def not_found(error=None):
    'Renderizar pagina "nao encontrada" - HTML.'
    return render_template("nao_econtrada.html", pagina=request.url)

if __name__ == "__main__":
    app.run()