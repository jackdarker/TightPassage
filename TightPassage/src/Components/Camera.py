class CameraUpdater(UpdatableObj):
    """Provides a class that updates the camera."""

    def __init__(self):
        super(CameraUpdater, self).__init__()

    def update(self, milliseconds, camera, desiredPan):
        pass


class SpringCameraUpdater(CameraUpdater):
    def __init__(self):
        super(SpringCameraUpdater, self).__init__()
        self.rest_length = 0.0
        self.damp = .05
        self.spring_stiffness = 1.75
        self.velocity = Vector2.zero()

    def update(self, milliseconds, camera):
        # Calculate and apply our spring equation to the camera.
        springVec = camera.desired_pan - camera.pan
        currentLength = springVec.length()
        displacement = currentLength - self.rest_length

        # Calculate the direction in which the spring should be moving.
        if displacement > 0:
            springDirection = springVec / displacement
        else:
            springDirection = Vector2.zero()

        force = springDirection * (displacement * self.spring_stiffness)
        self.velocity += force
        self.velocity *= self.damp
        camera.pan += self.velocity


class Camera(UpdatableObj):
    def __init__(self):
        super(Camera, self).__init__()

        # The center of the screen is the origin of the camera.
        self.world_center = Vector2(0, 0)
        self.pan = self.world_center
        self.desired_pan = self.pan
        self.previous_pos = self.pan

        # The extent to which the camera is allowed to move.
        # None indicates that there are no constraints.
        self.camera_bounds = None

        # The class that controls how the camera updates. Default is SpringCameraUpdater()
        self.update_handeler = SpringCameraUpdater()

        # Contains the visible portions of the camera.
        self.view_bounds = pygame.Rect(0, 0, 0, 0)
        self.update_order = 50000

    def get_world_pos(self):
        """Get the position of the camera in world coordinates."""
        return self.pan - self.world_center

    def get_movement_delta(self):
        """Get the amount the camera has moved since get_movement_delta was last called."""
        pos = self.pan - self.previous_pos
        self.previous_pos = Vector2(self.pan.X, self.pan.Y)
        return pos

    def Reset(self):
        """Reset the camera back to its defaults."""
        self.pan = self.world_center
        self.desired_pan = self.pos

    def check_bounds(self):
        """Make sure the camera is not outside if its legal range."""
        if not (self.camera_bounds == None):
            if self.__pan.X < self.camera_bounds.Left:
                self.__pan[0] = self.camera_bounds.Left

            if self.__pan.X > self.camera_bounds.Right:
                self.__pan[0] = self.camera_bounds.Right

            if self.__pan.Y < self.camera_bounds.Top:
                self.__pan[1] = self.camera_bounds.Top

            if self.__pan.Y > self.camera_bounds.Bottom:
                self.__pan[1] = self.camera_bounds.Bottom

    def get_cam_bounds(self):
        """Return the bounds of the camera in x, y, xMax, and yMax format."""
        world_pos = self.get_world_pos()
        screen_res = Ragnarok.get_world().get_backbuffer_size() * .5
        return (self.pan.X - screen_res.X), (self.pan.Y - screen_res.Y), (self.pan.X + screen_res.X), (
                self.pan.Y + screen_res.Y)

    def update_view_bounds(self):
        """Update the camera's view bounds."""
        self.view_bounds.left = self.pan.X - self.world_center.X
        self.view_bounds.top = self.pan.Y - self.world_center.Y
        self.view_bounds.width = self.world_center.X * 2
        self.view_bounds.height = self.world_center.Y * 2

    def update(self, milliseconds):
        self.update_handeler.update(milliseconds, self)
        self.check_bounds()
        self.update_view_bounds()
        super(Camera, self).update(milliseconds)

