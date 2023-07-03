from pyvis.network import Network
import networkx as nx
import pandas as pd
import tkinter as tk
from tkinter import filedialog, messagebox

def selecionar_arquivo():
    arquivo = filedialog.askopenfilename(filetypes=[("Arquivos XLSX e CSV", "*.xlsx;*.csv")])
    entry_arquivo.delete(0, tk.END)
    entry_arquivo.insert(tk.END, arquivo)

def selecionar_saida():
    caminho_saida = filedialog.asksaveasfilename(defaultextension=".html", filetypes=[("Arquivo HTML", "*.html")])
    entry_saida.delete(0, tk.END)
    entry_saida.insert(tk.END, caminho_saida)

def gerar_grafo():
    arquivo = entry_arquivo.get()
    caminho_saida = entry_saida.get()

    if arquivo and caminho_saida:
        if arquivo.endswith('.xlsx'):
            df = pd.read_excel(arquivo)
        elif arquivo.endswith('.csv'):
            df = pd.read_csv(arquivo)
        else:
            messagebox.showerror("Erro", "Formato de arquivo inválido. Apenas arquivos XLSX e CSV são suportados.")
            return

        # Tabela de interações
        tabela_interacoes = {}
        for index, row in df.iterrows():
            name = row['name']
            interactions = row['interactions'].split(', ')
            tabela_interacoes[name] = interactions

        # Mapeamento de nós para links, cores, descrições e tipos
        mapeamento_links_cores = {}
        for index, row in df.iterrows():
            name = row['name']
            link = row['link']
            color = row['color']
            description = row['description']
            type = row['type']
            mapeamento_links_cores[name] = {'link': link, 'color': color, 'description': description, 'type': type}

        # Criação do grafo
        grafo = nx.DiGraph()

        # Adiciona as arestas ao grafo
        for elemento, interactions in tabela_interacoes.items():
            for interacao in interactions:
                grafo.add_edge(elemento, interacao)

        # Criação da visualização do grafo
        nt = Network(notebook=True)

        for node in grafo.nodes:
            # Verificar se o nó tem um link, color, description e type associados
            if node in mapeamento_links_cores:
                info = mapeamento_links_cores[node]
                link = info['link']
                color = info['color']
                description = info['description']
                type = info['type']
                nt.add_node(node, label=node, shape="dot", color=color, title=node, url=link, description=description, type=type)
            else:
                nt.add_node(node, label=node, shape="dot")

        nt.from_nx(grafo)

        # Exibir o gráfico interativo
        nt.show_buttons(filter_=['physics'])
        nt.save_graph(caminho_saida)

        # Incorporar o campo de pesquisa no arquivo HTML
        html_code = '''
        <style>
            .container {
                display: flex;
                flex-direction: row;
                align-items: center;
            }

            .container-componentes{
                display: flex;
                flex-direction: column;
                align-items: center;
                justify-content: flex-start;
            }

            .search-input {
                margin: 10px;
            }

            .mynetwork {
                margin: 10px;
            }

            .config {
                margin: 10px;
            }

            .node-info {
                margin: 10px;
            }
        </style>

        <div class="container">
            
            <div class="container-componentes">
                <div class="search-input">
                    <input type="text" id="search-input" placeholder="Buscar" style="padding: 5px; font-size: 14px;"></input>
                </div>

                <div class="node-info" id="node-info"></div>
            </div>         

            <script type="text/javascript">
                var nodes = network.body.data.nodes.get();
                var searchInput = document.getElementById("search-input");
                var nodeInfoDiv = document.getElementById("node-info");
                var selectedNodeId = null;

                searchInput.addEventListener('input', function() {
                    var searchTerm = this.value.toLowerCase().trim();
                    var foundNodeIds = [];

                    if (searchTerm !== '') {
                        for (var i = 0; i < nodes.length; i++) {
                            var node = nodes[i];
                            var label = node.label.toLowerCase();

                            if (label.includes(searchTerm)) {
                                foundNodeIds.push(node.id);
                            }
                        }
                    }

                    if (foundNodeIds.length > 0) {
                        network.selectNodes(foundNodeIds);
                        network.fit({
                            nodes: foundNodeIds
                        });
                    } else {
                        network.unselectAll();
                    }
                });

                network.on("click", function(params) {
                    if (params.nodes.length > 0) {
                        var nodeId = params.nodes[0];
                        if (selectedNodeId === nodeId) {
                            nodeInfoDiv.innerHTML = '';
                            selectedNodeId = null;
                        } else {
                            selectedNodeId = nodeId;
                            var node = network.body.nodes[selectedNodeId];
                            var label = node.options.label;
                            var color = node.options.color.background;
                            var title = node.options.title;
                            var url = node.options.url;
                            var description = node.options.description;
                            var type = node.options.type;

                            var infoHTML = '<h3>' + label + '</h3>';
                            infoHTML += '<p><strong>color:</strong> ' + color + '</p>';
                            infoHTML += '<p><strong>description:</strong> ' + description + '</p>';
                            infoHTML += '<p><strong>type:</strong> ' + type + '</p>';
                            infoHTML += '<p><strong>interactions:</strong></p>';
                            infoHTML += '<ul>';
                            var neighbors = network.getConnectedNodes(selectedNodeId);
                            neighbors.forEach(function(neighbor) {
                                var neighborNode = network.body.nodes[neighbor];
                                var neighborLabel = neighborNode.options.label;
                                infoHTML += '<li>' + neighborLabel + '</li>';
                            });
                            infoHTML += '</ul>';
                            infoHTML += '<p><strong>Hiperlink:</strong> <a href="' + url + '" target="_blank">' + url + '</a></p>';

                            nodeInfoDiv.innerHTML = infoHTML;
                        }
                    }
                });
            </script>
        </div>
        '''

        with open(caminho_saida, 'a') as file:
            file.write(html_code)
        
        messagebox.showinfo("Sucesso", "O grafo foi gerado e o arquivo HTML foi salvo.")

# Criação da janela principal
root = tk.Tk()
root.title("Gerador de Grafo de arquitetura")
root.geometry("600x120")

# Label e Campo de texto para exibir o caminho do arquivo selecionado
label_arquivo = tk.Label(root, text="Arquivo (.xlsx ou .csv):")
label_arquivo.grid(row=0, column=0, padx=5, pady=5, sticky=tk.E)
entry_arquivo = tk.Entry(root, width=50)
entry_arquivo.grid(row=0, column=1, columnspan=2, padx=5, pady=5, sticky=tk.W)
button_arquivo = tk.Button(root, text="Selecionar", command=selecionar_arquivo, bg="blue", fg="white")
button_arquivo.grid(row=0, column=3, padx=5, pady=5, sticky=tk.W)

# Label e Campo de texto para exibir o caminho de saída do arquivo HTML
label_saida = tk.Label(root, text="Saída (Pasta para salvar .html):")
label_saida.grid(row=1, column=0, padx=5, pady=5, sticky=tk.E)
entry_saida = tk.Entry(root, width=50)
entry_saida.grid(row=1, column=1, columnspan=2, padx=5, pady=5, sticky=tk.W)
button_saida = tk.Button(root, text="Selecionar", command=selecionar_saida, bg="blue", fg="white")
button_saida.grid(row=1, column=3, padx=5, pady=5, sticky=tk.W)

# Botão para gerar o grafo
button_gerar = tk.Button(root, text="Gerar Grafo", command=gerar_grafo, bg="green", fg="white")
button_gerar.grid(row=2, column=0, columnspan=4, padx=5, pady=10)

root.mainloop()