#import sys #import innecesario

#Clase nodo
class Node:
    def __init__(self, value):
        self.value = value
        self.left = None
        self.right = None
        self.height = 1 

#FUNCIONES AUXILIARES
#Funcion para calcular la altura del nodo
def getHeight(node):
    if not node:
        return 0
    return node.height

#Funcion para calcular el factor de balance del nodo
def getBalance(node):
    if not node:
        return 0
    return getHeight(node.left) - getHeight(node.right)

#Funcion para actualizar la altura del nodo
def updateHeight(node):
    if node:
        node.height = 1 + max(getHeight(node.left), getHeight(node.right))

#ROTACIONES
#Rotacion a la derecha
def rotate_right(y):
    x = y.left
    T2 = x.right

    x.right = y
    y.left = T2

    updateHeight(y)
    updateHeight(x)

    return x

#Rotacion a la izquierda
def rotate_left(x):
    y = x.right
    T2 = y.left

    y.left = x
    x.right = T2

    updateHeight(x)
    updateHeight(y)

    return y

class AVLTree:
    def __init__(self):
        self.root = None

    #Insercion
    def insert(self, value):
        self.root = self._insert_recursive(self.root, value)

    def _insert_recursive(self, node, value):
        if not node:
            return Node(value)

        if value < node.value:
            node.left = self._insert_recursive(node.left, value)
        elif value > node.value:
            node.right = self._insert_recursive(node.right, value)
        else:
            return node 
        
        updateHeight(node)
        
        balance = getBalance(node)

        if balance > 1 and getBalance(node.left) >= 0:
             return rotate_right(node) #Falta el return para que el nodo actual se actualice con el resultado de la rotacion 
        elif balance > 1 and getBalance(node.left) < 0:
            node.left = rotate_left(node.left)
            return rotate_right(node) #Falta el return para que el nodo actual se actualice con el resultado de la rotacion 
        elif balance < -1 and getBalance(node.right) <= 0:
            return rotate_left(node)#Falta el return para que el nodo actual se actualice con el resultado de la rotacion 
        elif balance < -1 and getBalance(node.right) > 0:
            node.right = rotate_right(node.right)
            return rotate_left(node) #Falta el return para que el nodo actual se actualice con el resultado de la rotacion 
        
        return node 

    #Eliminacion
    def delete(self, value):
        self.root = self._delete_recursive(self.root, value)

    def _delete_recursive(self, node, value):
        if not node:
            return node

        if value < node.value:
            node.left = self._delete_recursive(node.left, value)
        elif value > node.value:
            node.right = self._delete_recursive(node.right, value)
        else:
            # Cuando el Nodo tiene un solo hijo o no tiene
            if not node.left:
                return node.right
            elif not node.right:
                return node.left

            # Cuando el Nodo tiene dos hijos
            min_larger_node = self._get_min_value_node(node.right)
            node.value = min_larger_node.value  # Copiar el valor del sucesor inorden
            node.right = self._delete_recursive(node.right, min_larger_node.value)  # Eliminar el sucesor

        # Actualizacion de la altura y rebalanceo del árbol
        updateHeight(node)
        balance = getBalance(node)

        if balance > 1 and getBalance(node.left) >= 0:
            return rotate_right(node)
        if balance > 1 and getBalance(node.left) < 0:
            node.left = rotate_left(node.left)
            return rotate_right(node)
        if balance < -1 and getBalance(node.right) <= 0:
            return rotate_left(node)
        if balance < -1 and getBalance(node.right) > 0:
            node.right = rotate_right(node.right)
            return rotate_left(node)

        return node

    def _get_min_value_node(self, node):
        temporal = node
        while temporal.left:
            temporal = temporal.left
        return temporal

    #Recorrido in-order
    def in_order(self, node):
        if node:
            self.in_order(node.left)
            print(node.value, end=' ')
            self.in_order(node.right)

    #Visualizacion
    def mostrar(self):
        self._mostrar(self.root)

    def _mostrar(self, nodo):
        if nodo is None:
            return
        print(f"Valor: {nodo.value}, Altura: {nodo.height}, Balance: {getBalance(nodo)}")
        self._mostrar(nodo.left)
        self._mostrar(nodo.right)


avl = AVLTree()
values_to_insert = [10, 20, 30, 40, 50, 25]

print("Insertando valores:", values_to_insert)
for val in values_to_insert:
    avl.insert(val)

print("\n--- Después de inserciones ---")
print("Recorrido in-orden :")
avl.in_order(avl.root)

avl.delete(30)  # Eliminar el valor 30

print("\n--- Después de eliminar 30 ---")
print("Recorrido in-orden :")
avl.in_order(avl.root)

print("\n--- Estructura del árbol ---")
avl.mostrar()
