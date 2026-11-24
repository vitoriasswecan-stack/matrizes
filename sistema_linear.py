import tkinter as tk
from tkinter import ttk, messagebox


class SistemaLinearApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Sistema Linear | Calculadora")
        self.root.geometry("600x650")
        self.root.minsize(500, 600)
        self.root.configure(bg="#111827")

        self.quantidade = tk.IntVar(value=2)
        self.campos = []

        self.criar_interface()

    def criar_interface(self):
        # Título
        titulo = tk.Label(
            self.root,
            text="SISTEMAS LINEARES",
            font=("Segoe UI", 22, "bold"),
            bg="#111827",
            fg="#60A5FA"
        )
        titulo.pack(pady=(25, 5))

        subtitulo = tk.Label(
            self.root,
            text="Calculadora de sistemas 2x2 e 3x3",
            font=("Segoe UI", 11),
            bg="#111827",
            fg="#D1D5DB"
        )
        subtitulo.pack(pady=(0, 20))

        # Seleção do tipo de sistema
        selecao_frame = tk.Frame(self.root, bg="#111827")
        selecao_frame.pack(pady=10)

        tk.Label(
            selecao_frame,
            text="Quantidade de incógnitas:",
            font=("Segoe UI", 11),
            bg="#111827",
            fg="white"
        ).pack(side="left", padx=10)

        seletor = ttk.Combobox(
            selecao_frame,
            values=["2x2", "3x3"],
            state="readonly",
            width=10
        )
        seletor.set("2x2")
        seletor.pack(side="left")
        seletor.bind("<<ComboboxSelected>>", self.alterar_sistema)

        # Área das equações
        self.equacoes_frame = tk.Frame(
            self.root,
            bg="#1F2937",
            padx=20,
            pady=20
        )
        self.equacoes_frame.pack(padx=30, pady=20, fill="x")

        # Resultado
        self.resultado = tk.Label(
            self.root,
            text="Digite os coeficientes do sistema.",
            font=("Segoe UI", 12),
            bg="#111827",
            fg="#D1D5DB",
            justify="center",
            wraplength=500
        )
        self.resultado.pack(pady=20)

        # Botões
        botoes_frame = tk.Frame(self.root, bg="#111827")
        botoes_frame.pack(pady=15)

        btn_resolver = tk.Button(
            botoes_frame,
            text="RESOLVER",
            command=self.resolver,
            font=("Segoe UI", 11, "bold"),
            bg="#2563EB",
            fg="white",
            activebackground="#1D4ED8",
            activeforeground="white",
            relief="flat",
            padx=25,
            pady=12,
            cursor="hand2"
        )
        btn_resolver.pack(side="left", padx=10)

        btn_limpar = tk.Button(
            botoes_frame,
            text="LIMPAR",
            command=self.limpar,
            font=("Segoe UI", 11, "bold"),
            bg="#374151",
            fg="white",
            activebackground="#4B5563",
            activeforeground="white",
            relief="flat",
            padx=25,
            pady=12,
            cursor="hand2"
        )
        btn_limpar.pack(side="left", padx=10)

        rodape = tk.Label(
            self.root,
            text="Desenvolvido em Python",
            font=("Segoe UI", 9),
            bg="#111827",
            fg="#6B7280"
        )
        rodape.pack(side="bottom", pady=15)

        self.montar_campos(2)

    def alterar_sistema(self, event):
        seletor = event.widget
        quantidade = 2 if seletor.get() == "2x2" else 3
        self.montar_campos(quantidade)

    def montar_campos(self, quantidade):
        self.quantidade = quantidade
        self.campos = []

        for widget in self.equacoes_frame.winfo_children():
            widget.destroy()

        variaveis = ["x", "y", "z"]

        for i in range(quantidade):
            linha = tk.Frame(self.equacoes_frame, bg="#1F2937")
            linha.pack(pady=10)

            campos_linha = []

            for j in range(quantidade):
                entrada = tk.Entry(
                    linha,
                    width=7,
                    font=("Segoe UI", 12),
                    justify="center"
                )
                entrada.pack(side="left", padx=5)

                entrada.insert(0, "1")
                campos_linha.append(entrada)

                label = tk.Label(
                    linha,
                    text=variaveis[j],
                    font=("Segoe UI", 12),
                    bg="#1F2937",
                    fg="white"
                )
                label.pack(side="left", padx=(0, 8))

                if j < quantidade - 1:
                    tk.Label(
                        linha,
                        text="+",
                        font=("Segoe UI", 12),
                        bg="#1F2937",
                        fg="white"
                    ).pack(side="left", padx=5)

            tk.Label(
                linha,
                text="=",
                font=("Segoe UI", 12),
                bg="#1F2937",
                fg="white"
            ).pack(side="left", padx=5)

            entrada_resultado = tk.Entry(
                linha,
                width=7,
                font=("Segoe UI", 12),
                justify="center"
            )
            entrada_resultado.pack(side="left", padx=5)
            entrada_resultado.insert(0, "0")

            campos_linha.append(entrada_resultado)
            self.campos.append(campos_linha)

        self.resultado.config(
            text="Digite os coeficientes do sistema."
        )

    def resolver(self):
        try:
            n = self.quantidade
            matriz = []

            for linha in self.campos:
                valores = [float(campo.get()) for campo in linha]
                matriz.append(valores)

        except ValueError:
            messagebox.showerror(
                "Erro",
                "Preencha todos os campos com números válidos."
            )
            return

        resultado = self.gauss(matriz, n)

        self.resultado.config(
            text=resultado,
            fg="#34D399" if "Resultado" in resultado else "#FBBF24"
        )

    def gauss(self, matriz, n):
        # Eliminação de Gauss com pivotamento
        for coluna in range(n):
            pivo = max(
                range(coluna, n),
                key=lambda linha: abs(matriz[linha][coluna])
            )

            if abs(matriz[pivo][coluna]) < 1e-10:
                continue

            matriz[coluna], matriz[pivo] = (
                matriz[pivo],
                matriz[coluna]
            )

            valor_pivo = matriz[coluna][coluna]

            for j in range(coluna, n + 1):
                matriz[coluna][j] /= valor_pivo

            for linha in range(n):
                if linha != coluna:
                    fator = matriz[linha][coluna]

                    for j in range(coluna, n + 1):
                        matriz[linha][j] -= (
                            fator * matriz[coluna][j]
                        )

        # Verificação de inconsistência
        for linha in range(n):
            if all(
                abs(matriz[linha][coluna]) < 1e-10
                for coluna in range(n)
            ) and abs(matriz[linha][n]) > 1e-10:
                return "Sistema impossível: não possui solução."

        # Verificação de infinitas soluções
        for linha in range(n):
            if all(
                abs(matriz[linha][coluna]) < 1e-10
                for coluna in range(n)
            ):
                return "Sistema indeterminado: possui infinitas soluções."

        # Extração dos resultados
        solucoes = [0] * n

        for linha in range(n):
            pivo = next(
                (
                    coluna for coluna in range(n)
                    if abs(matriz[linha][coluna]) > 1e-10
                ),
                None
            )

            if pivo is not None:
                solucoes[pivo] = matriz[linha][n]

        variaveis = ["x", "y", "z"]
        texto = "Resultado:\n\n"

        for i in range(n):
            texto += f"{variaveis[i]} = {solucoes[i]:.6f}\n"

        return texto

    def limpar(self):
        for linha in self.campos:
            for campo in linha:
                campo.delete(0, tk.END)

        self.resultado.config(
            text="Digite os coeficientes do sistema.",
            fg="#D1D5DB"
        )


if __name__ == "__main__":
    janela = tk.Tk()
    app = SistemaLinearApp(janela)
    janela.mainloop()
