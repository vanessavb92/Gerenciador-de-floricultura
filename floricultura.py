import tkinter as tk
from tkinter import messagebox
from tkinter import simpledialog
import json
import os

# Caminho do arquivo JSON para armazenar os dados
ARQUIVO_DADOS = "dados_floricultura.json"

# Classe Floricultura
class Floricultura:
    def __init__(self, nome):
        self.nome = nome
        self.estoque = {}
        self.fluxo_caixa = 0
        self.entregas = []
        self.carregar_dados()

    def carregar_dados(self):
        """Carrega os dados de um arquivo JSON"""
        if os.path.exists(ARQUIVO_DADOS):
            with open(ARQUIVO_DADOS, "r") as arquivo:
                dados = json.load(arquivo)
                self.estoque = dados.get("estoque", {})
                self.fluxo_caixa = dados.get("fluxo_caixa", 0)
                self.entregas = dados.get("entregas", [])
        else:
            # Se o arquivo não existir, inicializa com dados padrão
            self.salvar_dados()

    def salvar_dados(self):
        """Salva os dados no arquivo JSON"""
        dados = {
            "estoque": self.estoque,
            "fluxo_caixa": self.fluxo_caixa,
            "entregas": self.entregas
        }
        with open(ARQUIVO_DADOS, "w") as arquivo:
            json.dump(dados, arquivo, indent=4)

    def adicionar_produto(self, produto, quantidade, preco):
        if produto in self.estoque:
            self.estoque[produto]['quantidade'] += quantidade
        else:
            self.estoque[produto] = {'quantidade': quantidade, 'preco': preco}
        self.salvar_dados()
    
    def remover_produto(self, produto, quantidade):
        if produto in self.estoque and self.estoque[produto]['quantidade'] >= quantidade:
            self.estoque[produto]['quantidade'] -= quantidade
            if self.estoque[produto]['quantidade'] == 0:
                del self.estoque[produto]  # Remove o produto caso a quantidade chegue a zero
            self.salvar_dados()
            return f"{quantidade} unidade(s) de {produto} removida(s) com sucesso!"
        else:
            return "Estoque insuficiente ou produto não encontrado."
    
    def vender_produto(self, produto, quantidade):
        if produto in self.estoque and self.estoque[produto]['quantidade'] >= quantidade:
            self.estoque[produto]['quantidade'] -= quantidade
            valor_venda = self.estoque[produto]['preco'] * quantidade
            self.fluxo_caixa += valor_venda
            self.salvar_dados()
            return f"Venda de {quantidade} unidades de {produto} realizada com sucesso!"
        else:
            return "Estoque insuficiente ou produto não encontrado."
    
    def registrar_entrega(self, pedido):
        self.entregas.append(pedido)
        self.salvar_dados()
        return f"Entrega do pedido '{pedido}' registrada com sucesso!"

# Função para atualizar a interface com o estoque
def atualizar_estoque_display():
    estoque_texto.delete(1.0, tk.END)  # Limpa a área de texto do estoque
    for produto, info in floricultura.estoque.items():
        estoque_texto.insert(tk.END, f"{produto} - Quantidade: {info['quantidade']} - Preço: R${info['preco']:.2f}\n")

# Função para adicionar produto
def adicionar_produto():
    dialog = tk.Toplevel(root)
    dialog.title("Adicionar Produto")
    dialog.geometry("400x300")  # Tamanho da janela de diálogo

    def salvar_produto():
        produto = produto_entry.get()
        try:
            quantidade = int(quantidade_entry.get())
            preco = float(preco_entry.get())
            floricultura.adicionar_produto(produto, quantidade, preco)
            atualizar_estoque_display()
            messagebox.showinfo("Sucesso", f"Produto {produto} adicionado com sucesso!")
            dialog.destroy()
        except ValueError:
            messagebox.showerror("Erro", "Preencha todos os campos corretamente.")

    produto_label = tk.Label(dialog, text="Nome do Produto:")
    produto_label.pack(pady=10)
    produto_entry = tk.Entry(dialog, width=30)
    produto_entry.pack(pady=10)

    quantidade_label = tk.Label(dialog, text="Quantidade:")
    quantidade_label.pack(pady=10)
    quantidade_entry = tk.Entry(dialog, width=30)
    quantidade_entry.pack(pady=10)

    preco_label = tk.Label(dialog, text="Preço Unitário:")
    preco_label.pack(pady=10)
    preco_entry = tk.Entry(dialog, width=30)
    preco_entry.pack(pady=10)

    salvar_button = tk.Button(dialog, text="Adicionar Produto", command=salvar_produto, bg="#4B0082", fg="white")
    salvar_button.pack(pady=10)

    # Função de arrastar a janela
    def arrastar_janela(event):
        dialog.geometry(f"+{event.x_root}+{event.y_root}")

    dialog.bind("<B1-Motion>", arrastar_janela)
    dialog.transient(root)
    dialog.grab_set()

# Função para remover produto
def remover_produto():
    dialog = tk.Toplevel(root)
    dialog.title("Remover Produto")
    dialog.geometry("400x300")  # Tamanho da janela de diálogo

    def salvar_remocao():
        produto = produto_entry.get()
        try:
            quantidade = int(quantidade_entry.get())
            mensagem = floricultura.remover_produto(produto, quantidade)
            messagebox.showinfo("Resultado da Remoção", mensagem)
            atualizar_estoque_display()
            dialog.destroy()
        except ValueError:
            messagebox.showerror("Erro", "Preencha todos os campos corretamente.")

    produto_label = tk.Label(dialog, text="Nome do Produto:")
    produto_label.pack(pady=10)
    produto_entry = tk.Entry(dialog, width=30)
    produto_entry.pack(pady=10)

    quantidade_label = tk.Label(dialog, text="Quantidade a Remover:")
    quantidade_label.pack(pady=10)
    quantidade_entry = tk.Entry(dialog, width=30)
    quantidade_entry.pack(pady=10)

    remover_button = tk.Button(dialog, text="Remover Produto", command=salvar_remocao, bg="#4B0082", fg="white")
    remover_button.pack(pady=10)

    # Função de arrastar a janela
    def arrastar_janela(event):
        dialog.geometry(f"+{event.x_root}+{event.y_root}")

    dialog.bind("<B1-Motion>", arrastar_janela)
    dialog.transient(root)
    dialog.grab_set()

# Função para vender produto
def vender_produto():
    produto = simpledialog.askstring("Vender Produto", "Nome do produto:")
    quantidade = simpledialog.askinteger("Vender Produto", "Quantidade de produto a ser vendida:")
    mensagem = floricultura.vender_produto(produto, quantidade)
    messagebox.showinfo("Resultado da Venda", mensagem)
    atualizar_estoque_display()

# Função para registrar entrega
def registrar_entrega():
    pedido = simpledialog.askstring("Registrar Entrega", "Nome do pedido a ser entregue:")
    mensagem = floricultura.registrar_entrega(pedido)
    messagebox.showinfo("Entrega Registrada", mensagem)

# Função para mostrar fluxo de caixa
def mostrar_fluxo_caixa():
    messagebox.showinfo("Fluxo de Caixa", f"Fluxo de Caixa Atual: R${floricultura.fluxo_caixa:.2f}")

# Função para mostrar entregas
def mostrar_entregas():
    entregas_texto.delete(1.0, tk.END)
    for entrega in floricultura.entregas:
        entregas_texto.insert(tk.END, f"Pedido: {entrega}\n")

# Configuração da interface gráfica
root = tk.Tk()
root.title("Flores & Encantos - Gerenciador de Floricultura")

# Estilizando a janela
root.config(bg="#FAF0E6")
root.geometry("1024x768")  # Tamanho inicial maior
root.minsize(800, 600)  # Tamanho mínimo para redimensionamento
root.resizable(True, True)  # Permite redimensionar a janela

# Criação da instância da floricultura e carregamento dos dados
floricultura = Floricultura("Flores & Encantos")

# Título
titulo = tk.Label(root, text="Bem-vindo ao sistema da Floricultura", font=("Helvetica", 20, "bold"), bg="#FAF0E6", fg="#4B0082")
titulo.pack(pady=20)

# Botões principais
botao_frame = tk.Frame(root, bg="#FAF0E6")
botao_frame.pack(pady=10, fill="x")

botao_adicionar_produto = tk.Button(botao_frame, text="Adicionar Produto", command=adicionar_produto, bg="#4B0082", fg="white", font=("Helvetica", 12, "bold"), relief="flat")
botao_adicionar_produto.pack(side="left", padx=10, pady=5, fill="x", expand=True)

botao_remover_produto = tk.Button(botao_frame, text="Remover Produto", command=remover_produto, bg="#4B0082", fg="white", font=("Helvetica", 12, "bold"), relief="flat")
botao_remover_produto.pack(side="left", padx=10, pady=5, fill="x", expand=True)

botao_vender_produto = tk.Button(botao_frame, text="Vender Produto", command=vender_produto, bg="#4B0082", fg="white", font=("Helvetica", 12, "bold"), relief="flat")
botao_vender_produto.pack(side="left", padx=10, pady=5, fill="x", expand=True)

botao_registrar_entrega = tk.Button(botao_frame, text="Registrar Entrega", command=registrar_entrega, bg="#4B0082", fg="white", font=("Helvetica", 12, "bold"), relief="flat")
botao_registrar_entrega.pack(side="left", padx=10, pady=5, fill="x", expand=True)

botao_fluxo_caixa = tk.Button(botao_frame, text="Ver Fluxo de Caixa", command=mostrar_fluxo_caixa, bg="#4B0082", fg="white", font=("Helvetica", 12, "bold"), relief="flat")
botao_fluxo_caixa.pack(side="left", padx=10, pady=5, fill="x", expand=True)

botao_mostrar_entregas = tk.Button(botao_frame, text="Ver Entregas Registradas", command=mostrar_entregas, bg="#4B0082", fg="white", font=("Helvetica", 12, "bold"), relief="flat")
botao_mostrar_entregas.pack(side="left", padx=10, pady=5, fill="x", expand=True)

# Exibição de estoque
estoque_frame = tk.LabelFrame(root, text="Estoque de Produtos", font=("Helvetica", 12), bg="#FAF0E6", fg="#4B0082", relief="solid")
estoque_frame.pack(pady=10, fill="both", expand=True)

estoque_texto = tk.Text(estoque_frame, height=20, width=80, font=("Helvetica", 12), bd=2, wrap=tk.WORD, bg="#FFF0F5", fg="#4B0082")
estoque_texto.pack(padx=10, pady=10)

# Exibição de entregas
entregas_frame = tk.LabelFrame(root, text="Entregas Registradas", font=("Helvetica", 12), bg="#FAF0E6", fg="#4B0082", relief="solid")
entregas_frame.pack(pady=10, fill="both", expand=True)

entregas_texto = tk.Text(entregas_frame, height=10, width=80, font=("Helvetica", 12), bd=2, wrap=tk.WORD, bg="#FFF0F5", fg="#4B0082")
entregas_texto.pack(padx=10, pady=10)

# Atualiza o estoque na interface ao carregar os dados
atualizar_estoque_display()

# Iniciar a interface gráfica
root.mainloop()
