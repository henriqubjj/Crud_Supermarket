import sqlite3

class Estoque:
    def __init__(self, id, nome, quantidade, preco_unit):
        self.id = id
        self.nome = nome
        self.quantidade = quantidade
        self.preco_unit = preco_unit

class Cliente:
    def __init__(self, id, nome, telefone, endereco):
        self.id = id
        self.nome = nome
        self.telefone = telefone
        self.endereco = endereco

class GerenciadorCRUD:
    def __init__(self, db_file):
        self.conn = sqlite3.connect(db_file)
        self.c = self.conn.cursor()
        self.c.execute('''CREATE TABLE IF NOT EXISTS estoque
                         (id INTEGER PRIMARY KEY, nome TEXT, quantidade INTEGER, preco_unit REAL)''')
        self.c.execute('''CREATE TABLE IF NOT EXISTS clientes
                         (id INTEGER PRIMARY KEY, nome TEXT, telefone TEXT, endereco TEXT)''')
        self.c.execute('''CREATE TABLE IF NOT EXISTS vendas
                         (id INTEGER PRIMARY KEY, cliente_id INTEGER, item_id INTEGER, quantidade INTEGER, total REAL)''')
        self.conn.commit()

    def inserir_estoque(self, nome, quantidade, preco_unit):
        self.c.execute("INSERT INTO estoque (nome, quantidade, preco_unit) VALUES (?, ?, ?)",
                       (nome, quantidade, preco_unit))
        self.conn.commit()
        print("Item inserido com sucesso.")

    def alterar_estoque(self, id, nome, quantidade, preco_unit):
        self.c.execute("UPDATE estoque SET nome=?, quantidade=?, preco_unit=? WHERE id=?",
                       (nome, quantidade, preco_unit, id))
        self.conn.commit()
        print("Item alterado com sucesso.")

    def pesquisar_estoque_por_nome(self, nome):
        self.c.execute("SELECT * FROM estoque WHERE nome LIKE ?", ('%' + nome + '%',))
        itens = self.c.fetchall()
        if itens:
            for item in itens:
                print("ID:", item[0])
                print("Nome:", item[1])
                print("Quantidade:", item[2])
                print("Preço Unitário:", item[3])
                print("--------------------------")
        else:
            print("Nenhum item encontrado com esse nome.")

    def remover_estoque(self, id):
        self.c.execute("DELETE FROM estoque WHERE id=?", (id,))
        self.conn.commit()
        print("Item removido com sucesso.")

    def remover_todos_estoque(self):
        self.c.execute("DELETE FROM estoque")
        self.conn.commit()
        print("Todos os itens do estoque foram removidos.")

    def listar_todos_estoque(self):
        self.c.execute("SELECT * FROM estoque")
        itens = self.c.fetchall()
        if itens:
            for item in itens:
                print("ID:", item[0])
                print("Nome:", item[1])
                print("Quantidade:", item[2])
                print("Preço Unitário:", item[3])
                print("--------------------------")
        else:
            print("Nenhum item encontrado.")

    def exibir_um_estoque(self, id):
        self.c.execute("SELECT * FROM estoque WHERE id=?", (id,))
        item = self.c.fetchone()
        if item:
            print("ID:", item[0])
            print("Nome:", item[1])
            print("Quantidade:", item[2])
            print("Preço Unitário:", item[3])
        else:
            print("Item não encontrado.")
        

    def inserir_cliente(self, nome, telefone, endereco):
        self.c.execute("INSERT INTO clientes (nome, telefone, endereco) VALUES (?, ?, ?)",
                       (nome, telefone, endereco))
        self.conn.commit()
        print("Cliente inserido com sucesso.")

    def alterar_cliente(self, id, nome, telefone, endereco):
        self.c.execute("UPDATE clientes SET nome=?, telefone=?, endereco=? WHERE id=?",
                       (nome, telefone, endereco, id))
        self.conn.commit()
        print("Cliente alterado com sucesso.")

    def pesquisar_cliente_por_nome(self, nome):
        self.c.execute("SELECT * FROM clientes WHERE nome LIKE ?", ('%' + nome + '%',))
        clientes = self.c.fetchall()
        if clientes:
            for cliente in clientes:
                print("ID:", cliente[0])
                print("Nome:", cliente[1])
                print("Telefone:", cliente[2])
                print("Endereço:", cliente[3])
                print("--------------------------")
        else:
            print("Nenhum cliente encontrado com esse nome.")

    def remover_cliente(self, id):
        self.c.execute("DELETE FROM clientes WHERE id=?", (id,))
        self.conn.commit()
        print("Cliente removido com sucesso.")

    def remover_todos_clientes(self):
        self.c.execute("DELETE FROM clientes")
        self.conn.commit()
        print("Todos os clientes foram removidos.")

    def listar_todos_clientes(self):
        self.c.execute("SELECT * FROM clientes")
        clientes = self.c.fetchall()
        if clientes:
            for cliente in clientes:
                print("ID:", cliente[0])
                print("Nome:", cliente[1])
                print("Telefone:", cliente[2])
                print("Endereço:", cliente[3])
                print("--------------------------")
        else:
            print("Nenhum cliente encontrado.")

    def exibir_um_cliente(self, id):
        self.c.execute("SELECT * FROM clientes WHERE id=?", (id,))
        cliente = self.c.fetchone()
        if cliente:
            print("ID:", cliente[0])
            print("Nome:", cliente[1])
            print("Telefone:", cliente[2])
            print("Endereço:", cliente[3])
        else:
            print("Cliente não encontrado.")

    def registrar_venda(self, cliente_id, item_id, quantidade):
        # Obter o preço unitário do item
        self.c.execute("SELECT preco_unit, quantidade FROM estoque WHERE id=?", (item_id,))
        resultado = self.c.fetchone()
        if resultado:
            preco_unit, estoque_atual = resultado
            if estoque_atual >= quantidade:
                total = quantidade * preco_unit

                # Solicita a confirmação do usuário
                confirmacao = input(f"Total da compra: R${total:.2f}. Deseja confirmar a compra? (S/N): ").upper()
                if confirmacao == 'S':
                    # Registra a venda no banco de dados
                    self.c.execute("INSERT INTO vendas (cliente_id, item_id, quantidade, total) VALUES (?, ?, ?, ?)",
                                   (cliente_id, item_id, quantidade, total))
                    # Atualiza a quantidade de itens no estoque
                    estoque_atual -= quantidade
                    self.c.execute("UPDATE estoque SET quantidade=? WHERE id=?", (estoque_atual, item_id))
                    self.conn.commit()
                    print("Venda registrada com sucesso.")
                    return total
                else:
                    print("Compra cancelada.")
                    return 0
            else:
                print("Quantidade insuficiente em estoque.")
                return 0
        else:
            print("Item não encontrado.")
            return 0

    def gerar_relatorio_vendas(self):
        self.c.execute("SELECT COUNT(*), SUM(quantidade), SUM(total) FROM vendas")
        relatorio = self.c.fetchone()
        print("Total de vendas:", relatorio[0])
        print("Total de itens vendidos:", relatorio[1])
        print("Valor total de vendas:", relatorio[2])
        
            
    def gerar_relatorio_estoque(self):
        self.c.execute("SELECT COUNT(*), SUM(quantidade), SUM(quantidade*preco_unit) FROM estoque")
        relatorio = self.c.fetchone()
        print("Total de itens:",relatorio[0])
        print("Quantidade total de estoque:",relatorio[1])
        print("Valor total em estoque:",relatorio[2])

    def gerar_relatorio_clientes(self):
        self.c.execute("SELECT COUNT(*) FROM clientes")
        total_clientes = self.c.fetchone()[0]
        print("Total de clientes:", total_clientes)

    def fechar_conexao(self):
        self.conn.close()