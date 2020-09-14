class Pool(object):
    """
    Create a pool of reusable objects.
    Reduces memory allocations due to new objects being constantly generated
    (such as in bullets being fired, etc.)
    """

    def __init__(self, object_count=0, init_function=None):
        """
        object_count is the number of objects we want to store in our pool.
        init_function is an optional delegate that specifies how the object should be inited.
            init_function should return the type of object that we want to use.
        """
        # A list containing all of our objects.
        self.queue = []

        # The number of objects left in the pool.
        self.objects_in_pool = 0

        # The number of ojects the user has checked out and not returned.
        self.active_objects = 0

        # The function used to init our objects.
        self.init_function = init_function

        # Generate our pool.
        for i in range(object_count):
            self.__init_object()

    def __init_object(self):
        """Create a new object for the pool."""
        # Check to see if the user created a specific initalization function for this object.
        if self.init_function is not None:
            new_obj = self.init_function()
            self.__enqueue(new_obj)
        else:
            raise TypeError("The Pool must have a non None function to fill the pool.")

    def __dequeue(self):
        """Pull an object from the list."""
        self.objects_in_pool -= 1
        return self.queue.pop()

    def __enqueue(self, item):
        """Add an object to the list."""
        self.objects_in_pool += 1
        self.queue.append(item)

    def request_object(self):
        """Grab an object from the pool. If the pool is empty, a new object will be generated and returned."""
        obj_to_return = None
        if len(self.queue) > 0:
            obj_to_return = self.__dequeue()
        else:
            # The queue is empty, generate a new item.
            self.__init_object()
            object_to_return = self.__dequeue()
        self.active_objects += 1
        return obj_to_return

    def return_object(self, obj):
        """Return a checked out object back into the queue."""
        self.__enqueue(obj)
        self.active_objects -= 1
