import itertools
class FPNode(object):
    def __init__(self, name, count, parent):
        self.name = name
        self.count = count
        self.parent = parent
        self.link = None
        self.children = []
    def has_child(self, name):
        for node in self.children:
            if node.name == name:
                return True
        return False
    def get_child(self, name):
        for node in self.children:
            if node.name == name:
                return node
        return None
    def add_child(self, value):
        child = FPNode(value, 1, self)
        self.children.append(child)
        return child


class FPTree(object):
    def __init__(self, data, min_sup, root_name, root_count):
        self.frequent = self.find_fre_1_item(data, min_sup)
        self.headers = self.build_header_table(self.frequent)
        self.root = self.build_fptree(
            data, root_name,
            root_count, self.frequent, self.headers)
    @staticmethod
    def find_fre_1_item(data, min_sup):
        items = {}
        for data in data:
            for item in data:
                if item in items:
                    items[item] += 1
                else:
                    items[item] = 1
        for key in list(items.keys()):
            if items[key] < min_sup:
                del items[key]
        return items
    @staticmethod
    def build_header_table(frequent):
        headers = {}
        for key in frequent.keys():
            headers[key] = None
        return headers
    def build_fptree(self, data, root_name,
                     root_count, frequent, headers):
        root = FPNode(root_name, root_count, None)

        for transaction in data:
            sorted_items = [x for x in transaction if x in frequent]
            sorted_items.sort(key=lambda x: frequent[x], reverse=True)
            if len(sorted_items) > 0:
                self.insert_tree(sorted_items, root, headers)
        return root
    def insert_tree(self, sorted_items, node, headers):
        first = sorted_items[0]
        child = node.get_child(first)
        if child is not None:
            child.count += 1
        else:
            child = node.add_child(first)
            if headers[first] is None:
                headers[first] = child
            else:
                current = headers[first]
                while current.link is not None:
                    current = current.link
                current.link = child
        next_items = sorted_items[1:]
        if len(next_items) > 0:
            self.insert_tree(next_items, child, headers)
    def has_single_path(self, node):#
        num_children = len(node.children)
        if num_children > 1:
            return False
        elif num_children == 0:
            return True
        else:
            return True and self.has_single_path(node.children[0])
    def mine_patterns(self, min_sup):
        if self.has_single_path(self.root):
            return self.generate_pattern_list()
        else:
            return self.zip_patterns(self.mine_sub_trees(min_sup))
    def zip_patterns(self, patterns):
        suffix = self.root.name
        if suffix is not None:
            new_patterns = {}
            for key in patterns.keys():
                new_patterns[tuple(sorted(list(key) + [suffix]))] = patterns[key]
            return new_patterns
        return patterns
    def generate_pattern_list(self):
        patterns = {}
        items = self.frequent.keys()
        if self.root.name is None:
            suffix_value = []
        else:
            suffix_value = [self.root.name]
            patterns[tuple(suffix_value)] = self.root.count
        for i in range(1, len(items) + 1):
            for subset in itertools.combinations(items, i):
                pattern = tuple(sorted(list(subset) + suffix_value))
                patterns[pattern] = min([self.frequent[x] for x in subset])
        return patterns

    def mine_sub_trees(self, min_sup):
        patterns = {}
        mining_order = sorted(self.frequent.keys(),key=lambda x: self.frequent[x])
        for item in mining_order:
            suffixes = []
            conditional_tree_input = []
            node = self.headers[item]
            while node is not None:
                suffixes.append(node)
                node = node.link
            for suffix in suffixes:
                frequency = suffix.count
                path = []
                parent = suffix.parent
                while parent.parent is not None:
                    path.append(parent.name)
                    parent = parent.parent
                for i in range(frequency):
                    conditional_tree_input.append(path)
            subtree = FPTree(conditional_tree_input, min_sup,item, self.frequent[item])
            subtree_patterns = subtree.mine_patterns(min_sup)
            for pattern in subtree_patterns.keys():
                if pattern in patterns:
                    patterns[pattern] += subtree_patterns[pattern]
                else:
                    patterns[pattern] = subtree_patterns[pattern]
        return patterns
def find_frequent_patterns(data, min_sup):
    tree = FPTree(data, min_sup, None, None)
    return tree.mine_patterns(min_sup)

def printf(frequent):
    for i in frequent:
        if len(i)>1:
            print(i,':',frequent[i])
def load_data():#inputdata
    '''
    data from text book
    '''
    data = [['l1', 'l2', 'l5'], ['l2', 'l4'], ['l2', 'l3'],
            ['l1', 'l2', 'l4'], ['l1', 'l3'], ['l2', 'l3'],
            ['l1', 'l3'], ['l1', 'l2', 'l3', 'l5'], ['l1', 'l2', 'l3']]

    return data
if __name__ == "__main__":
    min_sup = 2 #最小支持數
    data = load_data()
    frequent = find_frequent_patterns(data, min_sup)
    printf(frequent)
