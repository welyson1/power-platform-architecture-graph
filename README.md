
# Power Platform Architecture Graph Builder

This application allows you to build an architecture graph for Power Platform based on interactions between SharePoint lists, Power Automate, Power BI, and Power Apps. You can use an input file in either .xlsx or .csv format to define the interactions and visualize them in an interactive graph.

## Features

- Select an input file in .xlsx or .csv format that contains the interaction data.
- Specify the output path for the generated HTML file.
- Generate a graph representing the architecture based on the provided data.
- Visualize the graph using the Pyvis library.
- Nodes in the graph can have associated links, colors, descriptions, and types.
- Search for nodes by their labels.
- Click on a node to view additional information about it, including its color, description, type, interactions, and associated hyperlink.


## Screenshots

![demo.gif](https://raw.githubusercontent.com/welyson1/power-platform-architecture-graph/development/demo.gif)

![software.png](https://raw.githubusercontent.com/welyson1/power-platform-architecture-graph/development/software.png)

![html_generated.png](https://raw.githubusercontent.com/welyson1/power-platform-architecture-graph/development/html_generated.png)

![graph.png](https://raw.githubusercontent.com/welyson1/power-platform-architecture-graph/development/graph.png)


## Files
```bash
├── root
    │ CommandLine.py 
    │ Interface.py
    │ data.csv
    │ data.xlsx
```

The code of the `CommandLine.py` file does not have a graphical interface, you must adjust the location of your `.xlsx` file, in this version support for `.csv` files is not yet implemented.

The code in the `Interface.py` file has an interface and you don't need to configure file paths. Download the latest executable version [here](https://pip.pypa.io/en/stable/).

I put sample files supported by the code. Your documentation data must respect the following header.

|name |	link |	color	 | description |	type |	interactions |
| --- | ---- | --------- | ------------| ------- | ------------- |
| Projects |  https://link1.com |  lightgreen |  description description |  Sharepoint list |  Team, Cost, Send email, Report cost | 
| Team |  https://link2.com | lightgreen  |  description description |  Sharepoint list |  Report cost, Send email | 
| Cost |  https://link3.com |  lightgreen |  description description |  Sharepoint list |  Report cost, Insert cost | 
| Send email |  https://link4.com |  lightblue |  description description |  Power Automation |  Projects, Team |
| Insert cost |  https://link5.com |  lightpink |  description description |  Power Apps |  Cost |
| Report cost |  https://link6.com | lightyellow |  description description |  Power BI |  Projects, Team, Cost |


## Installation
1. Clone this repository

2. Type the commands below in the terminal to install the necessary libraries

`pyvis` is a Python library that provides an interface for creating interactive graph visualizations using the Vis.js JavaScript library. In the provided code, `pyvis` is used to create and manipulate the graph view.
```bash
pip install pyvis
```

You need this library
```bash
pip install openpyxl
```

`networkx` is a Python library that allows the creation, manipulation and study of structures, dynamics and functions of complex networks. In the provided code, `networkx` is used to create and manipulate the underlying graph.
```bash
pip install networkx
```

`pandas` is a widely used Python library for data analysis and manipulation. It provides efficient data structures and data analysis tools, allowing reading, writing and data manipulation of XLSX and CSV files. In the provided code, `pandas` is used to read the data from the XLSX or CSV file and process it before creating the graph.
```bash
pip install pandas
```

`tkinter` is a Python graphical user interface (GUI) library that lets you easily and interactively create windows, buttons, text fields, and other interface components. In the provided code, `tkinter` is used to create the application's graphical interface, where users can select files, define the output path and interact with the buttons to generate the graph.
```bash
pip install tkinter
```
**it will only be necessary if you are going to use the code with a graphical interface*

3. run the code with the command below

```bash
python Interface.py
```
or the command below to run without graphical interface. You will have to change the path of the files 
```bash
python CommandLine.py
```
## Contributing

Feel free to contribute to this project by submitting bug reports, feature requests, or pull requests.


## Licença

[MIT](https://choosealicense.com/licenses/mit/)