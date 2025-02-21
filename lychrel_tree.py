import matplotlib.pyplot as plt

def is_palindrome(n: int) -> bool:
    return str(n) == str(n)[::-1]

def reverse_num(n: int) -> int:
    return int(str(n)[::-1])

def lychrel_chain(n: int, max_iter: int = 200):
    """
    Generate the chain of 'reverse-and-add' starting from n.
    Returns:
        - chain: the list of numbers encountered (including n).
        - found_pal: bool indicating if a palindrome was found before max_iter.
    """
    chain = [n]
    current = n
    for _ in range(max_iter):
        r = reverse_num(current)
        next_val = current + r
        chain.append(next_val)
        if is_palindrome(next_val):
            return chain, True
        current = next_val
    # If no palindrome is found within max_iter steps, treat as a Lychrel candidate
    return chain, False

def build_lychrel_graph(start: int, end: int, max_iter: int = 200):
    """
    Builds adjacency relationships (edges) for the reverse-and-add graph
    for numbers in [start, end]. Also identifies any "Lychrel seeds."

    Returns:
        - adjacency: dict { node: set_of_next_nodes }
        - level_of: dict { node: (minimum) level in the chain layering }
        - lychrel_seeds: set of numbers that did not produce a palindrome
                         within max_iter steps.
    """
    adjacency = {}
    level_of = {}
    lychrel_seeds = set()

    def add_edge(u, v):
        """Utility to add an edge u -> v to adjacency."""
        if u not in adjacency:
            adjacency[u] = set()
        adjacency[u].add(v)

    for n in range(start, end + 1):
        chain, found_pal = lychrel_chain(n, max_iter)

        # If no palindrome found, mark n as a Lychrel candidate
        if not found_pal:
            lychrel_seeds.add(n)

        # Add edges for each step in the chain
        for i, node in enumerate(chain):
            # Set level if not already set (or keep min level if conflict)
            if node not in level_of:
                level_of[node] = i
            else:
                level_of[node] = min(level_of[node], i)

            # Edge: chain[i] -> chain[i+1], if not at the end
            if i < len(chain) - 1:
                nxt = chain[i + 1]
                add_edge(node, nxt)
                # Update level for the next node
                if nxt not in level_of:
                    level_of[nxt] = i + 1
                else:
                    level_of[nxt] = min(level_of[nxt], i + 1)

    return adjacency, level_of, lychrel_seeds

def plot_lychrel_graph(adjacency, level_of, lychrel_seeds, filename='lychrel_tree.png'):
    """
    Plot the Lychrel graph in layers, auto-scaling the axes to fit all nodes,
    and then save the figure to a file.

    Parameters:
        adjacency: Dictionary { node -> set(next_nodes) }
        level_of: Dictionary { node -> layer_index }
        lychrel_seeds: Set of nodes that did not produce a palindrome within max_iter
        filename: Name of the file to save the figure (e.g., 'lychrel_tree.png')
    """
    from collections import defaultdict
    nodes_by_level = defaultdict(list)
    for node, lvl in level_of.items():
        nodes_by_level[lvl].append(node)

    all_levels = sorted(nodes_by_level.keys())

    # Assign (x, y) positions to each node
    pos = {}

    # Track min/max x,y to set plot bounds
    min_x = float('inf')
    max_x = float('-inf')
    min_y = float('inf')
    max_y = float('-inf')

    for lvl in all_levels:
        row_nodes = nodes_by_level[lvl]
        row_nodes.sort()
        count = len(row_nodes)
        for i, node in enumerate(row_nodes):
            # Center the nodes around x=0
            x = i - count / 2
            # Place them on row y = -lvl
            y = -lvl
            pos[node] = (x, y)

            # Track bounding box
            node_radius = 0.2
            min_x = min(min_x, x - node_radius)
            max_x = max(max_x, x + node_radius)
            min_y = min(min_y, y - node_radius)
            max_y = max(max_y, y + node_radius)

    plt.figure(figsize=(12, 10))
    ax = plt.gca()
    ax.set_aspect('equal', adjustable='datalim')

    # Draw edges
    for u, next_nodes in adjacency.items():
        (x_u, y_u) = pos[u]
        for v in next_nodes:
            (x_v, y_v) = pos[v]
            ax.annotate(
                "",
                xy=(x_v, y_v),
                xytext=(x_u, y_u),
                arrowprops=dict(
                    arrowstyle="->",
                    color="gray",
                    shrinkA=5,
                    shrinkB=5,
                    lw=0.5
                )
            )

    # Draw nodes
    for node, (x, y) in pos.items():
        color = "red" if node in lychrel_seeds else "skyblue"
        circ = plt.Circle((x, y), 0.2, color=color, ec="black", zorder=2)
        ax.add_patch(circ)
        ax.text(x, y, str(node), ha='center', va='center', fontsize=6, zorder=3)

    # Set axis limits to ensure every node is fully visible
    margin = 0.5
    plt.xlim(min_x - margin, max_x + margin)
    plt.ylim(min_y - margin, max_y + margin)

    plt.title("Lychrel Tree (Reverse-and-Add) [Auto-Scaled]", fontsize=14)
    plt.axis('off')

    # Save the figure before showing
    plt.savefig(filename, dpi=300, bbox_inches='tight')
    print(f"Saved Lychrel tree to: {filename}")

    # Now show the plot
    plt.show()

def main():
    START = 1
    END = 200
    MAX_ITER = 50

    adjacency, level_of, lychrel_seeds = build_lychrel_graph(START, END, MAX_ITER)

    # You can change 'lychrel_tree.png' to any desired path or filename
    plot_lychrel_graph(adjacency, level_of, lychrel_seeds, filename='lychrel_tree.png')

if __name__ == "__main__":
    main()
