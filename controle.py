from PyQt5 import  uic,QtWidgets
import mysql.connector
from reportlab.pdfgen import canvas

numero_id = 0

#CONECTANDO AO BANCO DE DADOS
banco = mysql.connector.connect(
    host="localhost",
    user="root",
    passwd="",
    database="cadastro_produtos"
)


#PEGA OS DADOS, MOSTRA NO TERMINAL E ENVIA PARA O BANCO
def funcao_principal():
    #PEGANDO OS DADOS
    codigo = formulario.le_codigo.text()
    descricao = formulario.le_descricao.text()
    preco = formulario.le_preco.text()
    categoria = ''

    #PRINTA A CATEGORIA NO TERMINAL
    if formulario.rb_eletronicos.isChecked() :
        print("Categoria Eletronicos selecionada")
        categoria = 'Eletrônicos'
    elif formulario.rb_informatica.isChecked() :
        print("Categoria Informatica selecionada")
        categoria = 'Informática'
    else :
        print("Categoria Alimentos selecionada")
        categoria = 'Alimentos'

    print("Código:",codigo)
    print("Descricao:",descricao)
    print("Preco",preco)
    
    #ENVIA OS DADOS PARA O BANCO VIA SQL
    cursor = banco.cursor()
    comando_SQL = "INSERT INTO produtos (codigo,descricao,preco,categoria) VALUES (%s,%s,%s,%s)"
    dados = (str(codigo),str(descricao),str(preco),categoria)
    cursor.execute(comando_SQL,dados)
    banco.commit()

    #LIMPA OS CAMPOS APOS O ENVIO DOS DADOS
    formulario.le_codigo.setText("")
    formulario.le_descricao.setText("")
    formulario.le_preco.setText("")

#FUNÇÃO PARA LISTAR OS DADOS
def chama_tela_listar():
    segunda_tela.show()

    cursor = banco.cursor()
    comando_SQL = "SELECT * FROM produtos"
    cursor.execute(comando_SQL)
    dados_lidos = cursor.fetchall()
    
    segunda_tela.tb_listar.setRowCount(len(dados_lidos))
    segunda_tela.tb_listar.setColumnCount(5)

    for i in range(0, len(dados_lidos)):
        for j in range(0, 5):
           segunda_tela.tb_listar.setItem(i,j,QtWidgets.QTableWidgetItem(str(dados_lidos[i][j])))

def chama_tela_cadastro():
    segunda_tela.close()


#EXCLUINDO DADOS
def excluir_dados():
    linha = segunda_tela.tb_listar.currentRow()
    segunda_tela.tb_listar.removeRow(linha)

    cursor = banco.cursor()
    cursor.execute("SELECT id FROM produtos")
    dados_lidos = cursor.fetchall()
    valor_id = dados_lidos[linha][0]
    print(valor_id)
    cursor.execute("DELETE FROM produtos WHERE id="+ str(valor_id))

#EXCLUINDO DADOS
def editar_dados():
    global numero_id
    linha = segunda_tela.tb_listar.currentRow()

    cursor = banco.cursor()
    cursor.execute("SELECT id FROM produtos")
    dados_lidos = cursor.fetchall()
    valor_id = dados_lidos[linha][0]
    cursor.execute("SELECT * FROM produtos WHERE id="+ str(valor_id))
    produto =  cursor.fetchall()
    terceira_tela.show()

    numero_id = valor_id

    terceira_tela.le_editar_id.setText(str(produto[0][0]))
    terceira_tela.le_editar_codigo.setText(str(produto[0][1]))
    terceira_tela.le_editar_produto.setText(str(produto[0][2]))
    terceira_tela.le_editar_preco.setText(str(produto[0][3]))
    terceira_tela.le_editar_categoria.setText(str(produto[0][4]))

def salvar_dados_editados():
    #PEGA O NUMERO DO ID UTILIZANDO UMA VARIAVEL GLOBAL
    global numero_id
    
    #DADOS DO LINE EDIT
    codigo = terceira_tela.le_editar_codigo.text()
    descricao = terceira_tela.le_editar_produto.text()
    preco =  terceira_tela.le_editar_preco.text()
    categoria = terceira_tela.le_editar_categoria.text()
    
    #ATUALIZAR NO BANCO
    cursor = banco.cursor()
    cursor.execute("UPDATE produtos SET codigo = '{}',descricao = '{}',preco = '{}', categoria = '{}' WHERE id = {}".format(codigo,descricao,preco,categoria,numero_id))

    #ATUALIZAR NA TELA
    terceira_tela.close()
    segunda_tela.close()
    chama_tela_listar()


#FUNÇÃO PARA GERAR UM PDF
def chama_gerar_pdf():
    #PEGA OS DADOS DO BANCO
    cursor = banco.cursor()
    comando_SQL = "SELECT * FROM produtos"
    cursor.execute(comando_SQL)
    dados_lidos = cursor.fetchall()
    y = 0

    #INSERE NO CAMINHO ESPECIFICADO
    pdf = canvas.Canvas("cadastro_produtos.pdf")
    pdf.setFont("Times-Bold", 25)
    pdf.drawString(200,800, "Produtos cadastrados:")
    pdf.setFont("Times-Bold", 18)

    pdf.drawString(10,750, "ID")
    pdf.drawString(110,750, "CODIGO")
    pdf.drawString(210,750, "PRODUTO")
    pdf.drawString(310,750, "PREÇO")
    pdf.drawString(410,750, "CATEGORIA")

    #PERCORRE OS DADOS LIDOS
    for i in range(0, len(dados_lidos)):
        y = y + 50
        pdf.drawString(10,750 - y, str(dados_lidos[i][0]))
        pdf.drawString(110,750 - y, str(dados_lidos[i][1]))
        pdf.drawString(210,750 - y, str(dados_lidos[i][2]))
        pdf.drawString(310,750 - y, str(dados_lidos[i][3]))
        pdf.drawString(410,750 - y, str(dados_lidos[i][4]))

    pdf.save()
    print("PDF FOI GERADO COM SUCESSO!")



app=QtWidgets.QApplication([])
formulario=uic.loadUi("cadastro.ui")
segunda_tela=uic.loadUi("listar_dados.ui")
terceira_tela=uic.loadUi("editar_dados.ui")
formulario.pb_enviar.clicked.connect(funcao_principal)
formulario.pb_listar.clicked.connect(chama_tela_listar)
segunda_tela.pb_lista_voltar.clicked.connect(chama_tela_cadastro)
segunda_tela.pb_lista_pdf.clicked.connect(chama_gerar_pdf)
segunda_tela.pb_lista_excluir.clicked.connect(excluir_dados)
segunda_tela.pb_lista_editar.clicked.connect(editar_dados)
terceira_tela.pb_edit_salvar.clicked.connect(salvar_dados_editados)

formulario.show()
app.exec()
