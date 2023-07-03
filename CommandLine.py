from pyvis.network import Network
import networkx as nx
from IPython.display import display, HTML
import pandas as pd

df = pd.read_excel('data.xlsx')

# Tabela de interaçõesa
tabela_interacoes = {}
for index, row in df.iterrows():
    name = row['Name']
    interacoes = row['Interacoes'].split(', ')
    tabela_interacoes[name] = interacoes


# Mapeamento de nós para links, cores, descrições e tipos
mapeamento_links_cores = {}
for index, row in df.iterrows():
    name = row['Name']
    link = row['Link']
    cor = row['Cor']
    descricao = row['Descrição']
    tipo = row['Tipo']
    mapeamento_links_cores[name] = {'link': link, 'cor': cor, 'descrição': descricao, 'tipo': tipo}


# Criação do grafo
grafo = nx.DiGraph()

# Adiciona as arestas ao grafo
for elemento, interacoes in tabela_interacoes.items():
    for interacao in interacoes:
        grafo.add_edge(elemento, interacao)

# Criação da visualização do grafo
nt = Network(notebook=True)

for node in grafo.nodes:
    # Verificar se o nó tem um link, cor, descrição e tipo associados
    if node in mapeamento_links_cores:
        info = mapeamento_links_cores[node]
        link = info['link']
        cor = info['cor']
        descricao = info['descrição']
        tipo = info['tipo']
        nt.add_node(node, label=node, shape="dot", color=cor, title=node, url=link, descricao=descricao, tipo=tipo)
    else:
        nt.add_node(node, label=node, shape="dot")

nt.from_nx(grafo)

# Exibir o gráfico interativo
nt.show_buttons(filter_=['physics'])
nt.show('grafo_interativo.html')

# Criar um campo de pesquisa e adicionar o evento de busca
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

    <div class="config" id="config"></div>   
    
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
                    var descricao = node.options.descricao;
                    var tipo = node.options.tipo;

                    var infoHTML = '<h3>' + label + '</h3>';
                    infoHTML += '<p><strong>Cor:</strong> ' + color + '</p>';
                    infoHTML += '<p><strong>Descrição:</strong> ' + descricao + '</p>';
                    infoHTML += '<p><strong>Tipo:</strong> ' + tipo + '</p>';
                    infoHTML += '<p><strong>Interações:</strong></p>';
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

# Incorporar o campo de pesquisa no arquivo HTML
with open('grafo_interativo.html', 'a') as file:
    file.write(html_code)

# Baixar o arquivo HTML
nt.save_graph('../grafo_interativo.html')