# InicialUI.py
from models.PessoaFisica import PessoaFisica
from models.PessoaJuridica import PessoaJuridica
from models.Veiculo import Veiculo
from models.Aluguel import Aluguel

class InicialUI:
    def __init__(self, db):
        self.db = db

    def menu(self):
        print("\n--- Menu Locadora de Veículos ---")
        print("1. Cadastrar Pessoa")
        print("2. Cadastrar Veículo")
        print("3. Realizar Aluguel")
        print("4. Listar Carros Alugados")
        print("5. Listar Pessoas Cadastradas")
        print("6. Listar Veículos Cadastrados")
        print("7. Sair")

    def cadastrar_pessoa(self):
        tipo = input("Digite o tipo de pessoa (1 para Física, 2 para Jurídica): ")
        nome = input("Nome: ")
        endereco = input("Endereço: ")
        
        if tipo == "1":
            cpf = input("CPF: ")
            pessoa = PessoaFisica(nome, endereco, cpf)
        elif tipo == "2":
            cnpj = input("CNPJ: ")
            pessoa = PessoaJuridica(nome, endereco, cnpj)
        else:
            print("Tipo inválido! A pessoa não será cadastrada.")
            return
        
        self.db.inserir_pessoa(pessoa)

    def cadastrar_veiculo(self):
        modelo = input("Modelo: ")
        marca = input("Marca: ")
        ano = int(input("Ano: "))
        
        print("Tipos de Veículo: 1. Carro, 2. Moto, 3. Caminhão")
        tipo_input = int(input("Escolha o tipo de veículo: "))

        tipo = None
        if tipo_input == 1:
            tipo = Veiculo.TipoVeiculo.CARRO
        elif tipo_input == 2:
            tipo = Veiculo.TipoVeiculo.MOTO
        elif tipo_input == 3:
            tipo = Veiculo.TipoVeiculo.CAMINHAO
        else:
            print("Tipo inválido! O veículo não será cadastrado.")
            return

        try:
            veiculo = Veiculo(modelo, marca, ano, tipo)
            self.db.inserir_veiculo(veiculo)
        except ValueError as e:
            print(f"Erro ao cadastrar veículo: {e}")

    def realizar_aluguel(self):
        try:
            pessoa_id = int(input("ID da pessoa: "))
            veiculo_id = int(input("ID do veículo: "))
            dias = int(input("Quantidade de dias: "))
            
            aluguel = Aluguel(pessoa_id, veiculo_id, dias)
            self.db.inserir_aluguel(aluguel)
        except ValueError:
            print("Erro: Por favor, insira valores válidos para IDs e dias.")

    def listar_carros_alugados(self):
        alugueis = self.db.listar_carros_alugados()
        print("\n--- Carros Alugados ---")
        if alugueis:
            print(f"{'ID':<5}{'Pessoa':<20}{'Veículo':<20}{'Marca':<15}{'Ano':<6}{'Dias':<6}{'Valor':<10}")
            for aluguel in alugueis:
                print(f"{aluguel['id']:<5}{aluguel['pessoa_nome']:<20}{aluguel['veiculo_modelo']:<20}{aluguel['marca']:<15}{aluguel['ano']:<6}{aluguel['dias']:<6}{aluguel['valor']:<10.2f}")
        else:
            print("Nenhum carro alugado encontrado.")

    def listar_pessoas(self):
        pessoas = self.db.listar_pessoas()
        print("\n--- Pessoas Cadastradas ---")
        if pessoas:
            print(f"{'ID':<5}{'Nome':<20}{'Endereço':<30}{'Tipo':<10}{'CPF':<15}{'CNPJ':<15}")
            for pessoa in pessoas:
                print(f"{pessoa['id']:<5}{pessoa['nome']:<20}{pessoa['endereco']:<30}{pessoa['tipo']:<10}{pessoa.get('cpf', ''):<15}{pessoa.get('cnpj', ''):<15}")
        else:
            print("Nenhuma pessoa cadastrada.")

    def listar_veiculos(self):
        veiculos = self.db.listar_veiculos()
        print("\n--- Veículos Cadastrados ---")
        if veiculos:
            print(f"{'ID':<5}{'Modelo':<20}{'Marca':<15}{'Ano':<6}{'Tipo':<10}")
            for veiculo in veiculos:
                print(f"{veiculo['id']:<5}{veiculo['modelo']:<20}{veiculo['marca']:<15}{veiculo['ano']:<6}{veiculo['tipo']:<10}")
        else:
            print("Nenhum veículo cadastrado.")
