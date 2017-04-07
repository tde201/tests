""" Implement the Heap data structure; where the heap structure and perfectly
    balanced binary tree are maintained.

    We shall consider a min-heap, the heap property maintained is that every
    node key is less than or equal to every child key.

    Methods include:
      Add an element.
      Deleting an element.
      Extract-Min.
      TODO: Implement heapify.
"""
#===============================================================================
class Heap:
    """ The min-Heap class.

        This creates the initial min heap, and has methods to extract-min,
        delte nodes, insert nodes.

        The Heap property is always maintained. In a min-Heap this is that each
        node key is less than or equal to each child key. A perfectly balanced
        binary tree is also maintained.
    """

    def __init__(self, inputArray):
        self.heap     = inputArray  # Assumption: this is already a heap.
        self.heapSize = len(inputArray)
        self.heapify()


    def parent(self, iNode):
        """ Return parent node of node iNode in the heap list. """

        # Assumption that we have a perfectly balanced binary tree, root
        # indexed as zero.

        if iNode == 0:
            # root
            return iNode
        elif iNode % 2 == 0:
            # iNode even
            return (iNode - 1) // 2
        else:
            # iNode odd
            return iNode // 2


    def child(self, iNode):
        """ Return child nodes of node iNode from the heap list. """

        if iNode >= self.heapSize // 2:
            return []  # i.e. no child nodes
        elif 2 * iNode + 2 >= self.heapSize:
            return [2 * iNode + 1]  # i.e. only 1 child node
        else:
            return [2 * iNode + 1, 2 * (iNode + 1)]


    def bubbleUp(self, childNode, childKey):
        """ Bubble-up child node until Heap property restored.

            Args:
              childNode: The array index of the node to examine.
              childKey:  The key value of the node to examine.
        """

        parentNode = self.parent(childNode)
        parentKey  = self.heap[parentNode]
        
        if parentKey > childKey:
            # Heap property violated, swap parent and child keys
            self.heap[parentNode] = childKey
            self.heap[childNode]  = parentKey
            self.bubbleUp(parentNode, childKey)


    def bubbleDown(self, parentNode, parentKey):
        """ Bubble-down parent node until Heap property restored.

            Args:
              parentNode: The parent node.
              parentKey:  The parent key.
        """

        childNodes    = self.child(parentNode)
        numChildNodes = len(childNodes)
        childKeys     = []

        if numChildNodes > 0:

            minChildKey  = None
            minChildNode = None
            
            for iVal in range(numChildNodes):

                childLeaf = childNodes[iVal]
                childKey  = self.heap[childLeaf]
                
                if (minChildKey == None or
                    childKey < minChildKey):
                    minChildKey  = childKey
                    minChildNode = childLeaf
            
            if parentKey > minChildKey:
                # Swap parent with the child with smallest key, if the Heap
                # property is violated
                self.heap[parentNode]   = minChildKey
                self.heap[minChildNode] = parentKey
                self.bubbleDown(minChildNode, parentKey)


    def heapify(self):
        """ Heapify an unheaped array. """

        # Starting from the first entry, bubble-down node until the Heap
        # property is respected. When the n-1th level is complete can go onto
        # the next level. TODO: check that the level is respects the Heap
        # property. Does not work at the moment.
        for iNode in range(self.heapSize - 1, -1, -1):
            self.bubbleDown(iNode, self.heap[iNode])
                

    def insert(self, kKey):
        """ Insert a node with key value kKey. """

        # Insert to end of list
        self.heap.append(kKey)
        iNode = self.heapSize  # i.e. heap index of kKey
        self.heapSize += 1

        # Bubble up until Heap property restored i.e. key of kKey's parent is
        # less than or equal to kKey.
        self.bubbleUp(iNode, kKey)


    def extractMin(self):
        """ Extract the root node.

            Returns:
              root: Key of root node.
        """

        if self.heapSize == 0:
            root = None
            print 'Heap empty!'
        else:
            # Replace root with last leaf, delete last leaf.
            root = self.heap[0]
            self.heap[0] = self.heap[-1]
            del self.heap[-1]
            self.heapSize -= 1

            # Bubble-down new root until Heap property restored.
            if self.heapSize > 0:
                self.bubbleDown(0, self.heap[0])

        return root


    def delete(self, kKey):
        """ Delete a node from middle of the heap.

            Args:
              kKey: Key value to delete.
        """
        
        if kKey not in self.heap:

            print 'Key not in Heap.'

        else:

            kNode = self.heap.index(kKey)  # First index of kKey in Heap

            # Replace kNode with last leaf, delete last leaf
            replaceKey = self.heap[-1]
            self.heap[kNode] = replaceKey
            del self.heap[-1]
            self.heapSize -= 1

            if self.heapSize > 0:
                # Bubble-up; if the node needs to be bubbled down, only 1 recurse is
                # performed before bubble-down executed.
                self.bubbleUp(kNode, replaceKey)
                self.bubbleDown(kNode, replaceKey)


#===============================================================================
def main():
    A = [13, 11, 9, 12, 4, 9, 8, 4, 4]
    print Heap(A).heap

#===============================================================================
if __name__ == "__main__":
    main()
