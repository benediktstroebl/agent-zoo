import os 
import pandas as pd
import sys 
import matplotlib.pyplot as plt
import seaborn as sns
import json
import logging
import networkx as nx

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

WORKSPACE_DIR = 'saved_workspaces/'

def load_logs(run_name, agent_dir):
    # Construct full path
    logs_path = os.path.join(WORKSPACE_DIR, run_name, agent_dir, 'logs/logs.json')
    
    # Check if path exists
    if not os.path.exists(logs_path):
        logger.error(f"Logs file not found at: {logs_path}")
        logger.info(f"Current working directory: {os.getcwd()}")
        logger.info(f"Checking if directory exists: {os.path.exists(os.path.dirname(logs_path))}")
        raise FileNotFoundError(f"Logs file not found at: {logs_path}")
        
    try:
        with open(logs_path, 'r') as f:
            logs = json.load(f)
        return logs
    except json.JSONDecodeError as e:
        logger.error(f"Error decoding JSON from {logs_path}: {e}")
        raise

def plot_logs(logs, animal, run_name):
    if not logs:
        logger.warning("No logs data to plot")
        return
        
    types = []
    for log in logs:
        types.append(log['type'])
    
    plt.figure(figsize=(10, 6))
    sns.countplot(x=types)
    
    # Create visuals directory if it doesn't exist
    os.makedirs(f'visuals/{run_name}', exist_ok=True)
    
    plt.savefig(os.path.join('visuals', f'log_types_{animal}.png'))
    plt.close()

def plot_tool_calls(logs, animal, run_name):
    tool_calls = []
    for log in logs:
        try: 
            if (log['type'] == 'action'):
                if log['start_time'] is None:
                    continue
                tool_calls.append(log['tool_call']['name'])
        except Exception as e:
            print(e)

    plt.figure(figsize=(10, 6))
    sns.countplot(x=tool_calls)
    plt.xticks(rotation=45)
    plt.savefig(os.path.join('visuals', f'{run_name}', f'tool_calls_{animal}.png'), bbox_inches='tight', dpi=300)
    plt.close()



def create_computation_graph(tools):
    """
    Create a sequential computation graph based on an ordered list of tools.
    Each tool used before will have a directed edge to every tool used after.
    
    Args:
        tools (list): A list of tuples where each tuple contains 
                      (tool_name, start_time, end_time).
                      Example: [("ToolA", "08:00", "09:00"), 
                                ("ToolB", "09:00", "10:00")]
                      
    Returns:
        graph (networkx.DiGraph): A fully sequential directed graph.
    """
    # Create a directed graph
    graph = nx.DiGraph()
    
    # Maintain a counter for each tool to handle repeated usage
    tool_counter = {}
    
    # Create unique nodes for each tool instance
    nodes = []
    for tool, start_time, end_time in tools:
        if tool not in tool_counter:
            tool_counter[tool] = 0
        tool_counter[tool] += 1
        node_name = f"{tool}_{tool_counter[tool]}"
        graph.add_node(node_name, tool=tool, start_time=start_time, end_time=end_time)
        nodes.append(node_name)
    
    # Add edges: Each node connects to all subsequent nodes
    for i in range(len(nodes)-1):
        graph.add_edge(nodes[i], nodes[i+1])
    
    return graph

def visualize_graph(graph, run_name, animal):
    """
    Visualize the computation graph using matplotlib.
    
    Args:
        graph (networkx.DiGraph): A directed acyclic graph.
    """
    # Use hierarchical layout to separate nodes vertically
    pos = nx.kamada_kawai_layout(graph)  # Better separation than spring_layout
    plt.figure(figsize=(20, 12))
    
    # Get first and last nodes
    nodes = list(graph.nodes())
    first_node = nodes[0]
    last_node = nodes[-1]
    
    # Create color map for nodes
    node_colors = ['lightgreen' if node == first_node else 'red' if node == last_node 
                  else 'lightblue' for node in graph.nodes()]
    
    # Draw the nodes and edges with increased spacing
    nx.draw(graph, pos, with_labels=True, node_color=node_colors,
            edge_color='gray', node_size=2000, font_size=10,
            width=2, arrows=True, arrowsize=20,
            node_shape='o',  # Circular nodes
            alpha=0.9,       # Slight transparency
            min_target_margin=30,  # Minimum margin between nodes
            min_source_margin=30)
    
    # Draw edge labels (optional: include start and end times as labels)
    # edge_labels = {(u, v): f"{graph.nodes[v]['start_time']} → {graph.nodes[v]['end_time']}" 
    #                for u, v in graph.edges()}
    # nx.draw_networkx_edge_labels(graph, pos, font_size=8)
    
    plt.title("Ordered Computation Graph")
    plt.savefig(os.path.join('visuals', f'{run_name}', f'{animal}_computation_graph.png'), bbox_inches='tight', dpi=300)
    plt.close()

def return_tuples(logs):
    tools = []
    for log in logs:
        try:    
            if log['type'] == 'action':
                if log['start_time'] is None:
                    continue
                tools.append((log['tool_call']['name'], log['start_time'], log['end_time']))
        except Exception as e:
            print(e)
    return tools

if __name__ == '__main__':
    animals = ['giraffe', 'monkey']
    for run_name in ['humor_2_agents_claude_4', 'humor_2_agents_4o_2', 'humor_2_agents_4o_3', 'humor_2_agents_4o_1']:
        for animal in animals:
            logs = load_logs(run_name, animal)
            plot_logs(logs, animal, run_name)
            plot_tool_calls(logs, animal, run_name)
            tools = return_tuples(logs)
            graph = create_computation_graph(tools)
            visualize_graph(graph, run_name, animal)
