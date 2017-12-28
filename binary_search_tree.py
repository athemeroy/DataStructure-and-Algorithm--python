class Node():
    def __init__(self, key):
        self.key = key
        self.right = None
        self.left = None
    def __repr__(self):
        return f'<Node key: {self.key} left: {self.left} right: {self.right} \n>'

            
            
class BinarySearchTree():
    def __init__(self):
        self.root = None
    def _insert_node(self, node, new_node):
        if node.key > new_node.key:
            if node.left == None:
                node.left = new_node
            else:
                self._insert_node(node.left, new_node)
        else:
            if node.right == None:
                node.right = new_node
            else:
                self._insert_node(node.right, new_node)
                
    def insert(self, key):
        if hasattr(key, '__iter__'):
            for i in key:
                self.insert(i)
        else:
            new_node = Node(key)
            if self.root == None:
                self.root = new_node
            else:
                self._insert_node(self.root, new_node)
            

    def __repr__(self):
        return self.root.__repr__()
    
    def _in_order_traverse_node(self, node, callback):
        if node != None:
            self._in_order_traverse_node(node.left, callback)
            callback(node.key)
            self._in_order_traverse_node(node.right, callback)
            
    
    def in_order_traverse(self, callback):
        return self._in_order_traverse_node(self.root, callback)
    
    def show(self):
        return self.in_order_traverse(print)


    def _pre_order_traverse_node(self, node, callback):
        if node != None:
            callback(node.key)
            self._pre_order_traverse_node(node.left, callback)
            self._pre_order_traverse_node(node.right, callback)
            
    
    def pre_order_traverse(self, callback):
        return self._pre_order_traverse_node(self.root, callback)


    def _post_order_traverse_node(self, node, callback):
        if node != None:
            self._post_order_traverse_node(node.left, callback)
            self._post_order_traverse_node(node.right, callback)
            callback(node.key)
    
    def post_order_traverse(self, callback):
        return self._post_order_traverse_node(self.root, callback)
    
    def _min_node(self, node):
        if node:
            while (node and node.left != None):
                node = node.left
            return node
    
    
#    def _find_min_node(self):
        
        
    @property
    def min(self):
        return self._min_node(self.root).key
    
    def _max_node(self, node):
        if node:
            while (node and node.right != None):
                node = node.right
            return node
        
    @property
    def max(self):
        return self._max_node(self.root).key
    
    def _search_node(self, node, key):
        if node == None:
            return False
        if key < node.key:
            return self._search_node(node.left, key)
        elif key > node.key:
            return self._search_node(node.right, key)
        else:
            return True
    
    def search(self, key):
        return self._search_node(self.root, key)
    
    def _remove_node(self, node, key):
        if node == None:
            return None
        if key < node.key:
            node.left = self._remove_node(node.left, key)
            return node
        elif key > node.key:
            node.right = self._remove_node(node.right, key)
            return node
        # 如果这个节点的值和key相等
        else:
            # 第一种情况：这是一个叶子节点
            if node.left == None and node.right == None:
                return None
            # 第二种情况：只有一个子节点
            if node.left == None:
                return node.right
            elif node.right == None:
                return node.left
            # 第三种情况： 这个节点有两个子节点
            else:
                # 找到这个节点的最小的后代
                aux = self._min_node(node.right)
#                print(f'aux is now{aux}\n\n')
                # 用这个后代的key代替这个节点的key
                node.key = aux.key
                # 在它的后代（只有可能在右支）中移除这个节点
                node.right = self._remove_node(node.right, aux.key)
#                print(f'{node}.right is {node.right}')
                return node
            
    
    def remove(self, key):
        self.root = self._remove_node(self.root, key)
    
    
if __name__ == '__main__':
    bst = BinarySearchTree()
    bst.insert([11, 7, 15, 5, 9, 13, 20, 3, 6, 8, 10, 12, 14, 18, 25])

                    