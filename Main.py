from ui.InicialUI import InicialUI
from db.Database import Database  

class Main:
    def __init__(self):
        self.db = Database(host="localhost", user="seu_usuario", password="sua_senha", database="nome_do_banco")
        self.db.connect()
        self.ui = InicialUI(self.db)  # Cria uma instância da classe InicialUI
        self.run()

    def run(self):
        while True:
            self.ui.menu()
            opcao = input("Escolha uma opção: ")
            match opcao:
                case "1":
                    self.ui.cadastrar_pessoa()
                case "2":
                    self.ui.cadastrar_veiculo()
                case "3":
                    self.ui.realizar_aluguel()
                case "4":
                    self.ui.listar_carros_alugados()
                case "5":
                    self.ui.listar_pessoas()
                case "6":
                    self.ui.listar_veiculos()
                case "7":
                    print("Saindo...")
                    self.db.close()
                    break
                case _:
                    print("Opção inválida. Tente novamente.")

if __name__ == "__main__":
    Main()
