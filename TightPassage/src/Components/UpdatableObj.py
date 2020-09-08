class UpdatableObj():
    """
    The base class of our game engine.
    Represents an object that can be updated.
    """
    # The number of objects that have existed so far. Used to create a unique object id.
    __total_id = 0

    def __init__(self, update_order=0):
        # The order in which this object should update relative to the other objects.
        self.update_order = update_order

        # Represents the unique identifer for this object.
        self.obj_id = self.__total_id

        # Keeps track of the total number of object created since game start.
        UpdatableObj.__total_id += 1

        # Is the object allowed to update druing the update loop?
        self.is_enabled = True

        # Does the object stay in one place even if the camera is moving?
        self.is_static = True

        # Represents the location of the object in world space.
        self.coords = Vector2()

        # Allows the user to define the object as they want.
        self.tag = ""

    def __str__(self):
        return "{ \nUpdateableObj: \t Update Order: " + str(self.update_order) + "\t Object ID: " \
               + str(self.obj_id) + "\t Is Enabled: " + str(self.is_enabled) + "\n}"

    def update(self, milliseconds):
        # Update the object.
        pass
