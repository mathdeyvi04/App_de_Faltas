from tkinter import *
from FuncoesGerais import criando_janela, verificador_nomes
from tkinter import ttk
from tkinter import messagebox
from os import listdir, getcwd


# Vamos construir o sanha de novo.

def faltante():
    # Vamos importar os alunos e ordenados
    def importando() -> list:
        # Obtendo
        al = []

        # Devemos apresentar um treeview perguntando de qual base ele quer os alunos
        subjanela = criando_janela(
            "Pegando Alunos",
            200,
            300
        )

        colunas = ['Arquivos De Nomes']

        tv = ttk.Treeview(
            subjanela,
            show='headings',
            columns=colunas
        )

        for coluna in colunas:
            tv.heading(coluna, text='Nomes dos Grupos', anchor="center")
            tv.column(coluna, minwidth=50, anchor="center")

        for arq in listdir(getcwd()):
            if arq.endswith(".txt"):
                tv.insert("", 'end', values=[arq])

        # Por último, vamos colocar a opção de criar um novo
        tv.insert("", 'end', values=['Criar um novo grupo'])

        tv.pack()

        Label(subjanela, text="Clique duas vezes para executar", bg='#dde').pack()

        # Vamos bindar

        def abrindo():

            item = tv.item(tv.selection()[0])["values"][0]

            if item == "Criar um novo grupo":
                subjanela.destroy()

                # Caso não exista esse arquivo, devemos ter o Sanha de montá-lo
                # Para tanto, vamos bradar:

                def Turmando() -> None:
                    pelotao = criando_janela('Criando Turma', 380, 200)
                    turma = []

                    def adicionar(event):
                        nome = nome_.get()
                        turma.append(nome)
                        nome_.delete(0, 'end')

                    Label(pelotao, text='Insira o nome de um aluno, tenha certeza que esteja correto.',
                          bg='#dde').place(
                        x=10, y=10)
                    nome_ = Entry(pelotao)
                    nome_.place(x=10, y=40)
                    nome_.bind('<Return>', adicionar)
                    Label(pelotao, text='Press Enter para adicionar', bg='#dde').place(x=10, y=70)

                    ja_tem_um_label = BooleanVar(pelotao)
                    ja_tem_um_label.set(False)

                    def finalizar():
                        if len(turma) == 0:
                            return messagebox.showwarning(
                                'ERROR',
                                "Nenhum adicionado."
                            )

                        if ja_tem_um_label.get():
                            return None
                        else:
                            ja_tem_um_label.set(True)

                        def desetar():
                            if nome_dado.get() == frase:
                                nome_dado.delete(0, 'end')
                                nome_dado.config(fg="black")

                                ajuda.set(frase_ajuda)

                        def setar():
                            if nome_dado.get() == "":
                                nome_dado.insert(0, frase)
                                nome_dado.config(fg="gray")

                                ajuda.set("")

                        # Devemos criar o nome do arquivo.
                        frase = "Insira o nome da turma/pelotão"
                        frase_ajuda = "Press Enter Para Encerrar"
                        ajuda = StringVar(pelotao)
                        ajuda.set("")

                        Label(pelotao, textvariable=ajuda, bg="#dde").place(x=210, y=105)
                        nome_dado = Entry(pelotao)
                        nome_dado.config(fg="gray")
                        nome_dado.insert(0, frase)
                        nome_dado.place(x=80, y=105)

                        nome_dado.bind("<Return>", lambda event: concluir())
                        nome_dado.bind("<FocusIn>", lambda event: desetar())
                        nome_dado.bind("<FocusOut>", lambda event: setar())

                        # Vamos colocar todos no arquivo

                        def concluir():

                            # Primeiro, criar.

                            p = open(nome_dado.get() + ".txt", 'x', encoding='utf-8')
                            p.close()

                            primeira = True
                            with open(r"Alunos.txt", 'w', encoding='utf-8') as base1:
                                for aluno in turma:
                                    if primeira:
                                        base1.write(aluno)
                                        primeira = False

                                    else:
                                        base1.write(f'\n{aluno}')

                            pelotao.destroy()
                            faltante()

                    Button(pelotao, text='Terminar', command=finalizar).place(x=10, y=100)

                    pelotao.mainloop()

                Turmando()

            with open(item, 'r', encoding='utf-8') as base:
                for linha in base:
                    if '\n' in linha:
                        linha = linha.replace('\n', '')

                    al.append(linha)

            subjanela.destroy()

        tv.bind("<Double-1>", lambda event: abrindo())

        subjanela.mainloop()

        # Ordenando, isso aqui é sanhudo.
        al.sort()

        return al

    #  Vamos guardar os alunos aqui
    alunos = importando()

    if len(alunos) == 0:
        messagebox.showerror('ERROR',
                             'Não há nenhum aluno no arquivo base, sugiro apagar o arquivo.')
        exit(0)

    # Vamos guardar os alunos que chegam por aqui
    safos = []

    # Primeiro, a interface inicial que vai decidir o que fazer

    App = criando_janela("App", 200, 200)

    def check():
        # Vamos criar a aplicação de checkbuttons.
        App.destroy()

        def pegando_tamanho(lista):
            # As variáveis que representam o total.
            wid = 0
            hei = 0

            # Iniciamos o algoritmo para o tamanho total.
            Max = 0
            i = 0
            while True:

                # Para definirmos a altura final
                if hei > Max:
                    Max = hei

                if i == len(lista):
                    break

                if i % 10 == 0:
                    # Vamos a próxima coluna.
                    wid += 115
                    hei = 0

                hei += 40

                i += 1

            return wid, hei

        # Vamos obter o tamanho estimado do Sanha, pois deve o acompanhar.
        comp, larg = pegando_tamanho(alunos)

        # Vamos criar o Sanha desde já
        pegando_check = criando_janela('App de Faltas', comp, larg)

        # Devemos preparar o Sanha que ficará em loop, literalmente colocando por cima.
        def gerando_os_checkbuttons():
            # Vamos fazê-los com o frame por cima
            principal = Frame(pegando_check, bg="#dde")
            principal.place(x=0, y=0, width=comp, height=larg)

            # Como já temos o frame, devemos fazer surgir todos os nomes de todos os alunos
            # Vamos criar um checkbutton para cada nome que ainda não chegou

            # Criando Estilo
            style = ttk.Style()
            style.configure("Custom.TCheckbutton", font=("Helvetica", 10), background='#dde')

            # Vamos criar a função responsável de registrar chegada de alguém
            def adicionando_safo(nome):
                safos.append(nome)
                principal.destroy()
                gerando_os_checkbuttons()

            # Criando os checksbutton
            posx = 10
            posy = 10
            i = 1
            for aluno in alunos:
                if aluno not in safos:
                    # As variáveis de posição

                    # Se ele ainda não tiver chegado, vamos acrescentar o sanhudo
                    cb = ttk.Checkbutton(principal, text=aluno, onvalue=1, offvalue=0,
                                         style="Custom.TCheckbutton")
                    cb['command'] = lambda pessoa=aluno: adicionando_safo(pessoa)

                    cb.place(x=posx, y=posy)

                    posy += 30

                    if i % 10 == 0:
                        posx += 110
                        posy = 10

                    i += 1

            Label(principal, text=f'Há {len(safos)} em forma.', bg='yellow').place(x=posx, y=posy)
            Label(principal, text=f'Faltam {len(alunos) - len(safos)}.').place(x=posx, y=posy + 30)

        gerando_os_checkbuttons()

        pegando_check.mainloop()

    Button(App, text='Check Button', command=check).place(x=0, y=0, width=200, height=100)

    def tw():

        App.destroy()

        # Só vamos precisar montar um treeview monstruoso.

        janela = criando_janela('App de Faltas', 300, 400)

        # Devemos criar um treeview
        def criando_treeview():
            tv = ttk.Treeview(janela,
                              columns=['Aluno Anti-Safo'],
                              show='headings')

            # Colocando as colunas do treeview
            tv.column('Aluno Anti-Safo', minwidth=0, width=200, anchor='center')
            tv.heading('Aluno Anti-Safo', text='Aluno Anti-Safo', anchor='center')

            tv.place(x=10, y=10, width=200, height=320)

            # Observe bem como fazemos as customizações
            tv.tag_configure("even_row", background="lightgray")

            # Aplicando as informações no TreeView
            for aluno in alunos:
                if aluno not in safos:
                    tv.insert("", "end", values=[aluno], tags=('even_row',))

            Label(janela, text=f'Há {len(safos)} em forma.', bg='yellow').place(x=10, y=370)
            Label(janela, text=f'Faltam {len(alunos) - len(safos)}.').place(x=150, y=370)

        criando_treeview()

        def adicionar(evento):
            nome = nome_carteado.get()
            nome_carteado.delete(0, 'end')

            for aluno in alunos:
                if verificador_nomes(nome, aluno):
                    # Achamos o sanhudo
                    if aluno in safos:
                        # Ele já está presente.
                        return messagebox.showwarning(message='Este aluno já chegou.')
                    else:
                        safos.append(aluno)
                        return criando_treeview()

            # Se chegamos aqui, não achamos o cara
            return messagebox.showerror(message='Aluno não existe')

        # Agora, vamos criar os outros Sanhas.
        nome_carteado = Entry(janela)
        nome_carteado.place(x=10, y=340)
        Label(janela, text='Pressione Enter', bg='#dde').place(x=150, y=340)
        nome_carteado.bind('<Return>', adicionar)

        janela.mainloop()

    Button(App, text='TreeView', command=tw).place(x=0, y=100, width=200, height=100)

    App.mainloop()


if __name__ == '__main__':
    faltante()
