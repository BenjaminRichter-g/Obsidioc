class FileNode:
    def __init__(self ,parent ,type="file", name="unnamed"):
        self.type = type #or folder
        self.children = LinkedList()
        self.leaf = True
        self.name = name
        self.parent = parent

    def add_child(self, child):
        self.children.insert_beginning(child)
        self.leaf = False


    def remove_child(self, child_name):
        self.children.delete_node_by_name(child_name)
        if self.children.get_size() == 0:
            self.leaf = True


class LinkedListNode:
    def __init__(self, node):
        self.node = node
        self.next = None

class LinkedList:
    def __init__(self):
        self.head = None

    def insert_beginning(self, new_node):
        new_node = LinkedListNode(new_node)
        if self.head == None:
            self.head = new_node
            return
        else:
            new_node.next = self.head 
            self.head = new_node

    def delete_beginning(self):

        if self.head == None:
            return
        
        self.head = self.head.next

    
    def delete_node_by_name(self, node_name):
        
        current_node = self.head
        if current_node == None:
            return
        if current_node.node.name == node_name:
            self.delete_beginning()
            return
            
        while current_node.next != None and current_node.next.node.name != node_name:
            current_node = current_node.next

        if current_node == None:
            print("Node not found for deletion")
            return
        else:
            current_node.next = current_node.next.next 

    def get_size(self):
        size = 0 
        if self.head:
            current_node = self.head
            while current_node:
                size+=1
                current_node = current_node.next
        return size






        



