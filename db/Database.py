import mysql.connector
from mysql.connector import Error
from models.PessoaFisica import PessoaFisica
from models.PessoaJuridica import PessoaJuridica
from models.Aluguel import Aluguel
from models.Veiculo import Veiculo

class Database:
    def __init__(self, host, user, password, database):
        self.host = "localhost"
        self.user = "root"
        self.password = "senha"
        self.database = "locadora"
        self.connection = None

    
    def connect(self):
        try:
            self.connection = mysql.connector.connect(
                host=self.host,
                user=self.user,
                password=self.password,
                database=self.database
            )
            if self.connection.is_connected():
                print("Conexão ao banco de dados estabelecida.")
        except Error as e:
            print(f"Erro ao conectar ao MySQL: {e}")

    
    def close(self):
        if self.connection.is_connected():
            self.connection.close()
            print("Conexão ao banco de dados fechada.")

    
    def inserir_pessoa(self, pessoa):
        cursor = self.connection.cursor()
        if isinstance(pessoa, PessoaFisica):
            tipo = 'Fisica'
            cpf = pessoa._cpf
            cnpj = None
        else:
            tipo = 'Juridica'
            cnpj = pessoa._cnpj
            cpf = None

        sql = """
        INSERT INTO Pessoa (nome, endereco, tipo, cpf, cnpj)
        VALUES (%s, %s, %s, %s, %s)
        """
        values = (pessoa._nome, pessoa._endereco, tipo, cpf, cnpj)

        try:
            cursor.execute(sql, values)
            self.connection.commit()
            print(f"Pessoa cadastrada com sucesso: {pessoa}")
        except Error as err:
            print(f"Erro: {err}")
        finally:
            cursor.close()

    
    def inserir_veiculo(self, veiculo):
        cursor = self.connection.cursor()
        sql = """
        INSERT INTO Veiculo (modelo, marca, ano, tipo)
        VALUES (%s, %s, %s, %s)
        """
        values = (veiculo._modelo, veiculo._marca, veiculo._ano, veiculo._tipo.name)

        try:
            cursor.execute(sql, values)
            self.connection.commit()
            print(f"Veículo cadastrado com sucesso: {veiculo}")
        except Error as err:
            print(f"Erro ao cadastrar veículo: {err}")
        finally:
            cursor.close()

    
    def inserir_aluguel(self, aluguel):
        cursor = self.connection.cursor()
        sql = """
        INSERT INTO Aluguel (pessoa_id, veiculo_id, dias, valor)
        VALUES (%s, %s, %s, %s)
        """
        values = (aluguel._pessoa_id, aluguel._veiculo_id, aluguel._dias, aluguel.calcular_valor())

        try:
            cursor.execute(sql, values)
            self.connection.commit()
            print("Aluguel cadastrado com sucesso!")
        except Error as err:
            print(f"Erro: {err}")
        finally:
            cursor.close()

    
    def listar_carros_alugados(self):
        cursor = self.connection.cursor(dictionary=True)
        sql = """
        SELECT Aluguel.id, Pessoa.nome AS pessoa_nome, Veiculo.modelo AS veiculo_modelo,
               Veiculo.marca, Veiculo.ano, Aluguel.dias, Aluguel.valor
        FROM Aluguel
        JOIN Pessoa ON Aluguel.pessoa_id = Pessoa.id
        JOIN Veiculo ON Aluguel.veiculo_id = Veiculo.id
        """
        try:
            cursor.execute(sql)
            return cursor.fetchall()
        except Error as err:
            print(f"Erro ao listar carros alugados: {err}")
            return []
        finally:
            cursor.close()

    
    def listar_pessoas(self):
        cursor = self.connection.cursor(dictionary=True)
        sql = """
        SELECT id, nome, endereco, tipo,
           COALESCE(cpf, '') AS cpf,
           COALESCE(cnpj, '') AS cnpj
        FROM Pessoa
        """
        try:
            cursor.execute(sql)
            return cursor.fetchall()
        except Error as err:
            print(f"Erro ao listar pessoas: {err}")
            return []
        finally:
            cursor.close()


    def listar_veiculos(self):
        cursor = self.connection.cursor(dictionary=True)
        try:
            cursor.execute("SELECT * FROM Veiculo")
            return cursor.fetchall()
        except Error as err:
            print(f"Erro ao listar veículos: {err}")
            return []
        finally:
            cursor.close()
