""" Graph type object that can be used for representing dependencies between
nodes.
"""
class DepGraph(object):
    """ Dependency graph class, each node holds two lists of requirements:
    the dependencies(needed by current node) and the dependants (need current node).
    """
    def __init__(self):
        self.graph = {}

    def add_node(self, label):
        """ Insert node into graph without any dependencies.
        TODO: try to add warning message of ops that are not errorneous but might hint at a problem.
        https://docs.python.org/3.6/library/warnings.html
        """
        # print("added node: ", label)
        if label not in self.graph.keys():
            self.graph[label] = {'internal': [], 'external': []}

    def add_dependency(self, label=None, dependencies=None, create=False):
        """ Add edges to the graph. If create is true then the edges
        will also add missing nodes.
        """
        if not label and create:
            self.graph[label] = []
        elif not label:
            raise TreeNodeError("Label can't be empty")
        if dependencies:
            for dep in dependencies:
                if dep in self.graph.keys():
                    self.graph[label]['external'].append(dep)
                    self.graph[dep]['internal'].append(label)
                elif create:
                    self.add_node(dep)
                    self.graph[label]['external'].append(dep)
                    self.graph[dep]['internal'].append(label)
                elif not create:
                    raise TreeNodeError("Dependency does not exist")
        else:
            raise TreeNodeError("Dependencies can't be empty")

    def __remove_node(self, label):
        """ Remove node from graph and all its edges.
        """
        # does it matter if I don't rise exception if key does not exist?
        # assert(label in self.graph.keys())
        if label:
            for edge in self.graph[label]:
                self.graph[edge].remove(label)
            del self.graph[label]
        else:
            raise TreeNodeError("Label can't be empty")

    def shortest_path(self, first, second):
        """ Return shortest path between two nodes.
        """
        pass

    def depend_on(self, label):
        """ Return a list of nodes that depend on input node.
        """
        if label not in self.graph.keys():
            raise TreeNodeError('Node does not exist')
        else:
            return self.graph[label]['external']

    def dependencies_of(self, label):
        """ Return a list of nodes that the input node depends on.
        """
        if label not in self.graph.keys():
            raise TreeNodeError('Node does not exist')
        else:
            return self.graph[label]['internal']

    def get_graph(self):
        """ Returns the current internal representation of the graph.
        """
        return self.graph

    def get_requirements(self):
        return self.graph.keys()

    def __str__(self):
        ret_str = ""
        for label, node in self.graph.items():
            tmp = str(label) + \
            "\n\t\tInternal: " + str(node['internal']) + "\n\t\tExternal: "\
            + str(node['external']) + '\n'
            ret_str += tmp
        return ret_str

class TreeNodeError(Exception):
    def __init__(self, message = "Dependency tree node error"):
        self.message = message
