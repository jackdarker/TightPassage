import numbers
from math import hypot
#from math import radians
#from math import degrees
from math import sin
from math import cos
from math import acos
from math import pi
from math import atan2

EPSILON = 1e-9
PI_DIV_180 = pi / 180.0

def sign(value):
    """
    Signum function. Computes the sign of a value.

    :Parameters:
        value : numerical
            Any number.

    :rtype: numerical

    :Returns:
        -1 if value was negative,
        1 if value was positive,
        0 if value was equal zero
    """
    assert isinstance(value, int) or isinstance(value, float)
    if 0 < value:
        return 1
    elif 0 > value:
        return -1
    else:
        return 0

class Vector2(object):
    def __init__(self, x=0.0, y=0.0):
        if(isinstance(x, numbers.Number)):
            self.x = x
            self.y = y
        else:#maybe a tuple?
            self.x=x[0]
            self.y=x[1]

    def __add__(self, other):
        if isinstance(other, Vector2):
            new_vec = Vector2()
            new_vec.x = self.x + other.x
            new_vec.y = self.y + other.y
            return new_vec
        else:
            raise TypeError("other must be of type Vector2")

    def __radd__(self, other):
        return self.__add__(other)

    def __sub__(self, other):
        if isinstance(other, Vector2):
            new_vec = Vector2()
            new_vec.x = self.x - other.x
            new_vec.y = self.y - other.y
            return new_vec
        else:
            raise TypeError("other must be of type Vector2")

    def __rsub__(self, other):
        return self.__sub__(other)

    def __mul__(self, value):
        if isinstance(value, numbers.Number):
            new_vec = self.copy()
            new_vec.x = new_vec.x * value
            new_vec.y = new_vec.y * value
            return new_vec
        else:
            raise TypeError("value must be a number.")

    def __rmul__(self, value):
        return self.__mul__(value)

    def __truediv__(self, value):
        if isinstance(value, numbers.Number):
            if value:
                new_vec = self.copy()
                new_vec.x /= value
                new_vec.y /= value
                return new_vec
            else:
                raise ZeroDivisionError("Cannot divide by zero.")
        else:
            raise TypeError("value must be a number.")

    def __floordiv__(self, value):
        if isinstance(value, numbers.Number):
            if value:
                new_vec = self.copy()
                new_vec.x = new_vec.x // value
                new_vec.y = new_vec.y // value
                return new_vec
            else:
                raise ZeroDivisionError("Cannot divide by zero.")
        else:
            raise TypeError("value must be a number.")

    def __rtruediv__(self, value):
        return self.__truediv__(value)

    def __rfloordiv__(self, value):
        return self.__floordiv__(value)

    def __eq__(self, other):
        """Check to see if two Vector2 objects are equal"""
        if isinstance(other, Vector2):
            if self.x == other.x and self.y == other.y:
                return True
        else:
            raise TypeError("other must be of type Vector2")

        return False

    def __neg__(self):
        return Vector2(-self.x, -self.y)

    def __getitem__(self, index):
        if index > 1:
            raise IndexError("Index must be less than 2")

        if index == 0:
            return self.x
        else:
            return self.y

    def __setitem__(self, index, value):
        if index > 1:
            raise IndexError("Index must be less than 2")

        if index == 0:
            self.x = value
        else:
            self.y = value

    def __str__(self):
        return "<Vector2> [ " + str(self.x) + ", " + str(self.y) + " ]"

    def __len__(self):
        return 2

    def zero(self):
        self.x = 0.0
        self.y = 0.0

    def is_zero(self):
        return self.x * self.x + self.y * self.y < EPSILON

    def as_xy_tuple(self):
        """returns tuple (x, y), z is supressed"""
        return self.x, self.y

    # Define our properties
    @staticmethod
    def zero():
        """Returns a Vector2 with all attributes set to 0"""
        return Vector2(0, 0)

    @staticmethod
    def one():
        """Returns a Vector2 with all attribures set to 1"""
        return Vector2(1, 1)

    def copy(self):
        """Create a copy of this Vector"""
        new_vec = Vector2()
        new_vec.x = self.x
        new_vec.y = self.y
        return new_vec

    def _length(self):
        """
        Calculates the length of the vector and returns it.
        """
        return hypot(self.x, self.y)

    def _set_length(self, value):
        """Scale the vector to have a given length"""
        self *= (value / self.length)

    length = property(_length, _set_length, doc="""
    returns length and change the length if set::

        v = Vec2(x, y)
        length = v.length
        v.length = 10 # vectors is scaled so length is 10 now

    """)

    def _length_sq(self):
        """
        Calculates the squared length of the vector and returns it.
        """
        return self.x * self.x + self.y * self.y
    length_sq = property(_length_sq, doc="""returns length squared""")

    def _normalized(self):
        """
        Returns a new vector with unit length.
        """
        leng = self.length
        if leng:
            return self.__class__(self.x / leng, self.y / leng)
        else:
            return self.__class__(0, 0)
    normalized = property(_normalized,
                                doc="""returns new vector with unit length""")
    def normalize(self):
        """modifys to normalized Vector"""
        length = self.length
        if length > 0:
            self.x /= length
            self.y /= length
        else:
            print("Length 0, cannot normalize.")

    def normalize_copy(self):
        """Create a copy of this Vector, normalize it, and return it."""
        vec = self.copy()
        vec.normalize()
        return vec

    def _normal_left(self):
        """returns the right normal (perpendicular), not unit length"""
        return self.__class__(-self.y, self.x)
    normal_left = property(_normal_left)

    def _normal_right(self):
        """returns the left normal (perpendicular), not unit length"""
        return self.__class__(self.y, -self.x)
    normal_right = property(_normal_right)

    perp = normal_left
    def truncate(self, scalar):
        if self.length_sq > scalar * scalar:
            self.length = scalar

    def wrap_around(self, size):
        x_max, y_max = size
        if self.x > x_max:
            self.x = 0
        elif self.x < 0.0:
            self.x = x_max
        if self.y > y_max:
            self.y = 0
        elif self.y < 0.0:
            self.y = y_max

    def round(self, n_digits=3):
        """
        Round values to n_digits.

        :Parameters:
            n_digits : int
                Number of digits after the point.
        """
        self.x = round(self.x, n_digits)
        self.y = round(self.y, n_digits)

    def rounded(self, n_digits=3):
        """
        Get a rounded vector.

        :Parameters:
            n_digits : int
                Number of digits after the point.

        :rtype: `Vec2`
        :Returns: `Vec2` rounded to n_digits
        """
        return self.__class__(round(self.x, n_digits), round(self.y, n_digits))
    def cross(self, other):
        """
        Cross product.

        :Parameters:
            other : `Vec2`
                The second vector for the cross product.

        :rtype: float
        :Returns: z value of the cross product (since x and y would be 0).
        :Note: a.cross(b) == - b.cross(a)
        """
        assert isinstance(other, self.__class__)
        return self.x * other.y - self.y * other.x

    def project_onto(self, other):
        """
        Project this vector onto another one.

        :Parameters:
            other : `Vec2`
                The other vector to project onto.

        :rtype: `Vec2`
        :Returns: The projected vector.
        """
        assert isinstance(other, self.__class__)
        return self.dot(other) / other.length_sq * other

    def reflect(self, normal):
        """normal should be normalized unitlength"""
        assert isinstance(normal, self.__class__)
        return self - 2 * self.dot(normal) * normal

    def reflect_tangent(self, tangent):
        """tangent should be normalized, unitlength"""
        assert isinstance(tangent, self.__class__)
        return 2 * tangent.dot(self) * tangent - self

    def rotate(self, degrees):
        """Rotates the vector bout the angle (degrees), + clockwise, - ccw"""
        rad = degrees * PI_DIV_180
        sin_val = sin(rad)
        cos_val = cos(rad)
        xcoord = self.x
        self.x = cos_val * xcoord - sin_val * self.y
        self.y = sin_val * xcoord + cos_val * self.y

    def rotated(self, degrees):
        """
        Returns a new vector, rotated about angle (degrees), + clockwise, - ccw
        """
        rad = degrees * PI_DIV_180
        sin_val = sin(rad)
        cos_val = cos(rad)
        return self.__class__(cos_val * self.x - sin_val * self.y,
                              sin_val * self.x + cos_val * self.y)

    def scaled(self, scale):
        """
        Returns a vector scaled to given length.

        :Returns: `Vec2` with lange scale
        """
        scale = scale / self.length
        return self.__class__(scale * self.x, scale * self.y)

    def rotate_to(self, angle_degrees):
        """rotates the vector to the given angle (degrees)."""
        self.rotate(angle_degrees - self.angle)

    def get_angle_between(self, other):
        """Returns the angle between the vectors."""
        assert isinstance(other, self.__class__)
        length = self.length
        olen = other.length
        if length and olen:
            return  acos(self.dot(other) / (length * olen)) / PI_DIV_180
        return 0

    @staticmethod
    def distance(vec1, vec2):
        """Calculate the distance between two Vectors"""
        if isinstance(vec1, Vector2) \
                and isinstance(vec2, Vector2):
            dist_vec = vec2 - vec1
            return dist_vec.length()
        else:
            raise TypeError("vec1 and vec2 must be Vector2's")

    @staticmethod
    def dot(vec1, vec2):
        """Calculate the dot product between two Vectors"""
        if isinstance(vec1, Vector2) \
                and isinstance(vec2, Vector2):
            return ((vec1.x * vec2.x) + (vec1.y * vec2.y))
        else:
            raise TypeError("vec1 and vec2 must be Vector2's")

    @staticmethod
    def angle(vec1, vec2):
        """Calculate the angle between two Vector2's"""
        dotp = Vector2.dot(vec1, vec2)
        mag1 = vec1.length()
        mag2 = vec2.length()
        result = dotp / (mag1 * mag2)
        return math.acos(result)

    @staticmethod
    def lerp(vec1, vec2, time):
        """Lerp between vec1 to vec2 based on time. Time is clamped between 0 and 1."""
        if isinstance(vec1, Vector2) \
                and isinstance(vec2, Vector2):
            # Clamp the time value into the 0-1 range.
            if time < 0:
                time = 0
            elif time > 1:
                time = 1

            x_lerp = vec1[0] + time * (vec2[0] - vec1[0])
            y_lerp = vec1[1] + time * (vec2[1] - vec1[1])
            return Vector2(x_lerp, y_lerp)
        else:
            raise TypeError("Objects must be of type Vector2")

    @staticmethod
    def from_polar(degrees, magnitude):
        """Convert polar coordinates to Carteasian Coordinates"""
        vec = Vector2()
        vec.x = math.cos(math.radians(degrees)) * magnitude

        # Negate because y in screen coordinates points down, oppisite from what is
        # expected in traditional mathematics.
        vec.y = -math.sin(math.radians(degrees)) * magnitude
        return vec

    @staticmethod
    def component_mul(vec1, vec2):
        """Multiply the components of the vectors and return the result."""
        new_vec = Vector2()
        new_vec.x = vec1.x * vec2.x
        new_vec.y = vec1.y * vec2.y
        return new_vec

    @staticmethod
    def component_div(vec1, vec2):
        """Divide the components of the vectors and return the result."""
        new_vec = Vector2()
        new_vec.x = vec1.x / vec2.x
        new_vec.y = vec1.y / vec2.y
        return new_vec


class Vector3(object):
    """Provides basic 3D Vector operations"""

    def __init__(self, x=0.0, y=0.0, z=0.0):
        """Constructs a Vector3 object with the default position of the object."""
        # Check for potential problems while converting the values.
        try:
            self.x = float(x)
            self.y = float(y)
            self.z = float(z)
        except (TypeError):
            raise TypeError("x, y, and z must be a numerical type.")

    def __len__(self):
        """Returns the number of attributes contained in this class."""
        return 3

    def __str__(self):
        """Builds a string representation of this object."""
        return "<Vector3>: { " + str(self.x) + ", " + str(self.y) + ", " + str(self.z) + " }"

    # Provide our operator overloaded methods
    def __eq__(self, other):
        """Check to see if two Vector3 instances are equal"""
        if not isinstance(other, Vector3):
            raise TypeError("other must be of type Vector3")

        if self.x == other.x \
                and self.y == other.y \
                and self.z == other.z:
            return True
        else:
            return False

    def __ne__(self, other):
        """Check to see if two Vector3 instances are not equal"""
        if not isinstance(other, Vector3):
            raise TypeError("other must be of type Vector3")

        if not (self.x == other.x) \
                or not (self.y == other.y) \
                or not (self.z == other.z):
            # True, the objects are not equal to each other.
            return True
        else:
            # False, the objects are equal to each other
            return False

    def __add__(self, other):
        """Adds two Vector3 objects, or a single float to the x, y, and z attributes."""
        if isinstance(other, Vector3):
            vec3 = Vector3()
            vec3.x = self.x + other.x
            vec3.y = self.y + other.y
            vec3.z = self.z + other.z
            return vec3
        else:
            # The object isn't of a correct type, return self to prevent errors.
            raise TypeError("other must be of type Vector3")

    def __radd__(self, other):
        return self.__add__(other)

    def __sub__(self, other):
        """Subtract two Vector3 objects, or a single float from the x, y, and z attributes"""
        if isinstance(other, Vector3):
            vec3 = Vector3()
            vec3.x = self.x - other.x
            vec3.y = self.y - other.y
            vec3.z = self.z - other.z
            return vec3
        else:
            raise TypeError("other must be of type Vector3")

    def __rsub__(self, other):
        return self.__sub__(other)

    def __mul__(self, other):
        """Multiply a Vector3 and a scalar."""
        if isinstance(other, numbers.Number):
            vec3 = Vector3()
            vec3.x = self.x * other
            vec3.y = self.y * other
            vec3.z = self.z * other
            return vec3
        else:
            raise TypeError("other must be a single number")

    def __rmul__(self, other):
        return self.__mul__(other)

    def __floordiv__(self, other):
        """Divide a Vector3 and a scalar."""
        if operator.isNumberType(other):
            vec3 = Vector3()
            vec3.x = self.x // other
            vec3.y = self.y // other
            vec3.z = self.z // other
            return vec3
        else:
            raise TypeError("other must be a single number")

    def __rfloordiv__(self, other):
        return self.__floordiv__(other)

    def __truediv__(self, other):
        """Divide a Vector3 and a scalar."""
        if operator.isNumberType(other):
            vec3 = Vector3()
            vec3.x = self.x / other
            vec3.y = self.y / other
            vec3.z = self.z / other
            return vec3
        else:
            raise TypeError("other must be a single number")

    def __rtruediv__(self, other):
        return self.__truediv__(other)

    def __neg__(self):
        """Negate the Vector"""
        neg_vec = Vector3()
        neg_vec.x = -self.x
        neg_vec.y = -self.y
        neg_vec.z = -self.z
        return neg_vec

    def __setitem__(self, index, value):
        """Set an internal value."""
        if index > 2:
            raise IndexError("index must be between 0 and 2 inclusive.")

        try:
            if index == 0:
                self.x = value
            elif index == 1:
                self.y = value
            else:
                self.z = value
        except (TypeError):
            raise TypeError("value must be a numerical type.")

    def __getitem__(self, index):
        """Get an internal value."""
        if index > 2:
            raise IndexError("index must be between 0 and 2 inclusive.")

        if index == 0:
            return self.x
        elif index == 1:
            return self.y
        else:
            return self.z

    # Define our methods
    def copy(self):
        """Create a copy of the Vector"""
        cpy_vec = Vector3()
        cpy_vec.x = self.x
        cpy_vec.y = self.y
        cpy_vec.z = self.z
        return cpy_vec

    def to_vec4(self, isPoint):
        """Converts this vector3 into a vector4 instance."""
        vec4 = Vector4()
        vec4.x = self.x
        vec4.y = self.y
        vec4.z = self.z
        if isPoint:
            vec4.w = 1
        else:
            vec4.w = 0

        return vec4

    def length(self):
        """Gets the length of the Vector"""
        return math.sqrt((self.x * self.x) + (self.y * self.y) + (self.z * self.z))

    def normalize(self):
        """Normalizes this Vector"""
        vlength = self.length()

        # Make sure the length isn't 0
        if vlength > 0:
            self.x /= vlength
            self.y /= vlength
            self.z /= vlength
        else:
            return Vector3(0, 0, 0)

    def normalize_copy(self):
        """Creates and returns a new Vector3 that is a normalized version of this Vector"""
        newVec = self.copy()
        newVec.normalize()
        return newVec

    def clamp(self, clampVal):
        """Clamps all the components in the vector to the specified clampVal."""
        if self.x > clampVal:
            self.x = clampVal
        if self.y > clampVal:
            self.y = clampVal
        if self.z > clampVal:
            self.z = clampVal

    # Define our static methods
    @staticmethod
    def up():
        """Return a Vector that points in the up direction."""
        return Vector3(0, 1, 0)

    @staticmethod
    def tuple_as_vec(xyz):
        """
        Generates a Vector3 from a tuple or list.
        """
        vec = Vector3()
        vec[0] = xyz[0]
        vec[1] = xyz[1]
        vec[2] = xyz[2]
        return vec

    @staticmethod
    def cross(vec1, vec2):
        """Returns the cross product of two Vectors"""
        if isinstance(vec1, Vector3) and isinstance(vec2, Vector3):
            vec3 = Vector3()
            vec3.x = (vec1.y * vec2.z) - (vec1.z * vec2.y)
            vec3.y = (vec1.z * vec2.x) - (vec1.x * vec2.z)
            vec3.z = (vec1.x * vec2.y) - (vec1.y * vec2.x)
            return vec3
        else:
            raise TypeError("vec1 and vec2 must be Vector3's")


class Vector4(object):
    """Provides basic 3D Vector operations"""

    def __init__(self, x=0.0, y=0.0, z=0.0, w=0.0):
        """Constructs a Vector4 object with the default position of the object."""
        # Check for potential problems while converting the values.
        try:
            self.x = float(x)
            self.y = float(y)
            self.z = float(z)
            self.w = float(w)
        except (TypeError):
            raise TypeError("x, y, z, and w must be a numerical type.")

    def __len__(self):
        """Returns the number of attributes contained in this class."""
        return 4

    def __str__(self):
        """Builds a string representation of this object."""
        return "<Vector4>: { " + str(self.x) + ", " + str(self.y) + ", " + str(self.z) + ", " + str(self.w) + " }"

    # Provide our operator overloaded methods
    def __eq__(self, other):
        """Check to see if two Vector4 instances are equal"""
        if not isinstance(other, Vector4):
            return False

        if self.x == other.x \
                and self.y == other.y \
                and self.z == other.z \
                and self.w == other.w:
            return True
        else:
            return False

    def __ne__(self, other):
        """Check to see if two Vector4 instances are not equal"""
        if not isinstance(other, Vector4):
            raise TypeError("other must be of type Vector4")

        if not (self.x == other.x) \
                or not (self.y == other.y) \
                or not (self.z == other.z) \
                or not (self.w == other.w):
            # True, the objects are not equal to each other.
            return True
        else:
            # False, the objects are equal to each other
            return False

    def __add__(self, other):
        """Adds two Vector4 objects."""
        if isinstance(other, Vector4):
            vec4 = Vector4()
            vec4.x = self.x + other.x
            vec4.y = self.y + other.y
            vec4.z = self.z + other.z
            vec4.w = self.w + other.w
            return vec4
        else:
            # The object isn't of a correct type, return self to prevent errors.
            raise TypeError("other must be of type Vector3")

    def __radd__(self, other):
        return self.__add__(other)

    def __sub__(self, other):
        """Subtract two Vector4 objects."""
        if isinstance(other, Vector4):
            vec4 = Vector4()
            vec4.x = self.x - other.x
            vec4.y = self.y - other.y
            vec4.z = self.z - other.z
            vec4.w = self.w - other.w
            return vec4
        else:
            raise TypeError("other must be of type Vector4")

    def __rsub__(self, other):
        return self.__sub__(other)

    def __mul__(self, other):
        """Multiply a Vector4 and a scalar."""
        if isinstance(other, numbers.Number):
            vec4 = Vector4()
            vec4.x = self.x * other
            vec4.y = self.y * other
            vec4.z = self.z * other
            vec4.w = self.w * other
            return vec4
        else:
            raise TypeError("other must be a single number")

    def __rmul__(self, other):
        return self.__mul__(other)

    def __div__(self, other):
        """Divide a Vector4 and a scalar."""
        if operator.isNumberType(other):
            vec4 = Vector4()
            vec4.x = self.x / other
            vec4.y = self.y / other
            vec4.z = self.z / other
            vec4.w = self.w / other
            return vec4
        else:
            raise TypeError("other must be a single number")

    def __rdiv__(self, other):
        return self.__div__(other)

    def __neg__(self):
        """Negate the Vector"""
        neg_vec = Vector4()
        neg_vec.x = -self.x
        neg_vec.y = -self.y
        neg_vec.z = -self.z
        neg_vec.w = -self.w
        return neg_vec

    def __setitem__(self, index, value):
        """Set an internal value."""
        if index > 3:
            raise IndexError("index must be between 0 and 3 inclusive.")

        try:
            if index == 0:
                self.x = value
            elif index == 1:
                self.y = value
            elif index == 2:
                self.z = value
            else:
                self.w = value
        except (TypeError):
            raise TypeError("value must be a numerical type.")

    def __getitem__(self, index):
        """Get an internal value."""
        if index > 3:
            raise IndexError("index must be between 0 and 3 inclusive.")

        if index == 0:
            return self.x
        elif index == 1:
            return self.y
        elif index == 2:
            return self.z
        else:
            return self.w

    # Define our methods
    def copy(self):
        """Create a copy of the Vector"""
        cpy_vec = Vector4()
        cpy_vec.x = self.x
        cpy_vec.y = self.y
        cpy_vec.z = self.z
        cpy_vec.w = self.w
        return cpy_vec

    def to_vec3(self):
        """Convert this vector4 instance into a vector3 instance."""
        vec3 = Vector3()
        vec3.x = self.x
        vec3.y = self.y
        vec3.z = self.z

        if self.w != 0:
            vec3 /= self.w

        return vec3

    def length(self):
        """Gets the length of the Vector"""
        return math.sqrt((self.x * self.x) + (self.y * self.y) + (self.z * self.z) + (self.w * self.w))

    def normalize(self):
        """Normalizes this Vector"""
        vlength = self.length()

        # Make sure the length isn't 0
        if vlength > 0:
            self.x /= vlength
            self.y /= vlength
            self.z /= vlength
            self.w /= vlength
        else:
            return Vector4(0, 0, 0, 0)

    def normalize_copy(self):
        """Creates and returns a new Vector3 that is a normalized version of this Vector"""
        newVec = self.copy()
        newVec.normalize()
        return newVec

    def clamp(self, clampVal):
        """Clamps all the components in the vector to the specified clampVal."""
        if self.x > clampVal:
            self.x = clampVal
        if self.y > clampVal:
            self.y = clampVal
        if self.z > clampVal:
            self.z = clampVal
        if self.w > clampVal:
            self.w = clampVal

    # Define our static methods
    @staticmethod
    def up():
        """Return a Vector that points in the up direction."""
        return Vector4(0, 1, 0, 0)

    @staticmethod
    def tuple_as_vec(xyzw):
        """
        Generates a Vector4 from a tuple or list.
        """
        vec = Vector4()
        vec[0] = xyzw[0]
        vec[1] = xyzw[1]
        vec[2] = xyzw[2]
        vec[3] = xyzw[3]
        return vec


def dot(vec1, vec2):
    """Returns the dot product of two Vectors"""
    if isinstance(vec1, Vector3) and isinstance(vec2, Vector3):
        return (vec1.x * vec2.x) + (vec1.y * vec2.y) + (vec1.z * vec2.z)
    elif isinstance(vec1, Vector4) and isinstance(vec2, Vector4):
        return (vec1.x * vec2.x) + (vec1.y * vec2.y) + (vec1.z * vec2.z) + (vec1.w * vec2.w)
    else:
        raise TypeError("vec1 and vec2 must a Vector type")


def distance(vec1, vec2):
    """Returns the distance between two Vectors"""
    vec3 = vec2 - vec1
    return vec3.length


def angle(vec1, vec2):
    """Returns the angle between two vectors"""
    dot_vec = dot(vec1, vec2)
    mag1 = vec1.length()
    mag2 = vec2.length()
    result = dot_vec / (mag1 * mag2)
    return math.acos(result)


def project(vec1, vec2):
    """Project vector1 onto vector2."""
    if isinstance(vec1, Vector3) and isinstance(vec2, Vector3) \
            or isinstance(vec1, Vector4) and isinstance(vec2, Vector4):
        return dot(vec1, vec2) / vec2.length() * vec2.normalize_copy()
    else:
        raise ValueError("vec1 and vec2 must be Vector3 or Vector4 objects.")


def component_add(vec1, vec2):
    """Add each of the components of vec1 and vec2 together and return a new vector."""
    if isinstance(vec1, Vector3) and isinstance(vec2, Vector3):
        addVec = Vector3()
        addVec.x = vec1.x + vec2.x
        addVec.y = vec1.y + vec2.y
        addVec.z = vec1.z + vec2.z
        return addVec

    if isinstance(vec1, Vector4) and isinstance(vec2, Vector4):
        addVec = Vector4()
        addVec.x = vec1.x + vec2.x
        addVec.y = vec1.y + vec2.y
        addVec.z = vec1.z + vec2.z
        addVec.w = vec1.w + vec2.w
        return addVec


def reflect(vec1, vec2):
    """Take vec1 and reflect it about vec2."""
    if isinstance(vec1, Vector3) and isinstance(vec2, Vector3) \
            or isinstance(vec1, Vector4) and isinstance(vec2, Vector4):
        return 2 * dot(vec1, vec2) * vec2 - vec2
    else:
        raise ValueError("vec1 and vec2 must both be a Vector type")


def sign(val):
    """Returns the sign of a number."""
    if val > 0:
        return 1
    elif val < 0:
        return -1

    return 0


class Ray(object):
    def __init__(self, origin=Vector3(0, 0, 0), direction=Vector3(0, 0, 0)):
        self.origin = origin
        self.direction = direction
        # Normalize our Vector
        self.direction.normalize()

    def get_point(self, scalar_val):
        """Get a point along the ray."""
        return scalar_val * self.direction + self.origin


class Matrix4(object):
    def __init__(self, *args):
        """
        *args defines a function that can accept a variable number of parameters.
        This allows us to be a bit more flexible in how we can create a Matrix,
        as the user can define all four rows, or only one or two rows upon init.
        """
        # A list of four Vector4's
        self.dta = []

        # Find the number of arguments the user passed to us.
        argLen = len(args)

        # Make sure we don't accept more than 4 lists.
        if argLen > 4:
            raise ValueError("*args should not contain more than four lists.")

        # Create an identity matrix if the user isn't filling all the rows with data.
        if argLen != 4:
            self.dta = Matrix4.identity().dta

        # Take each arg and append it to our dta list.
        for index, arg in enumerate(args):
            if isinstance(arg, Vector4) \
                    or isinstance(arg, tuple) \
                    or isinstance(arg, list):
                if len(arg) == 4:
                    self.dta.append(Vector4(arg[0], arg[1], arg[2], arg[3]))
                else:
                    raise ValueError("Each argument must contain four values or be a Vector4.")
            else:
                raise ValueError("Each argument must contain four values or be a Vector4.")

    def __getitem__(self, index):
        """Get a row from the matrix."""
        return self.get_row(index)

    def get_row(self, row):
        if row > -1 and row < 4:
            return self.dta[row].copy()

    def set_row(self, row, vec4):
        if row > -1 and row < 4:
            self.dta[row] = vec4.copy()

    def get_col(self, col):
        if col > -1 and col < 4:
            return Vector4(self.dta[0][col],
                           self.dta[1][col],
                           self.dta[2][col],
                           self.dta[3][col])

    def set_col(self, col, vec4):
        if col > -1 and col < 4:
            self.dta[col][0] = vec4.x,
            self.dta[col][1] = vec4.y,
            self.dta[col][2] = vec4.z,
            self.dta[col][3] = vec4.w

    def __mul__(self, other):
        if isinstance(other, Matrix4):
            return Matrix4((dot(self.get_row(0), other.get_col(0)),
                            dot(self.get_row(0), other.get_col(1)),
                            dot(self.get_row(0), other.get_col(2)),
                            dot(self.get_row(0), other.get_col(3))),

                           (dot(self.get_row(1), other.get_col(0)),
                            dot(self.get_row(1), other.get_col(1)),
                            dot(self.get_row(1), other.get_col(2)),
                            dot(self.get_row(1), other.get_col(3))),

                           (dot(self.get_row(2), other.get_col(0)),
                            dot(self.get_row(2), other.get_col(1)),
                            dot(self.get_row(2), other.get_col(2)),
                            dot(self.get_row(2), other.get_col(3))),

                           (dot(self.get_row(3), other.get_col(0)),
                            dot(self.get_row(3), other.get_col(1)),
                            dot(self.get_row(3), other.get_col(2)),
                            dot(self.get_row(3), other.get_col(3)))
                           )

        if isinstance(other, Vector4):
            vec = Vector4(dot(self.get_row(0), other),
                          dot(self.get_row(1), other),
                          dot(self.get_row(2), other),
                          dot(self.get_row(3), other))
            return vec

        if isinstance(other, numbers.Number):
            return Matrix4(self.dta[0] * other,
                           self.dta[1] * other,
                           self.dta[2] * other,
                           self.dta[3] * other)

        raise TypeError("other must be of type Matrix4, Vector4, or number")

    def __rmul__(self, other):
        return self.__mul__(other)

    def __str__(self):
        string = ""
        for vec in self.dta:
            string += "[ " + str(vec.x) + " " + str(vec.y) + " " + str(vec.z) + " " + str(vec.w) + " ]\n"
        return string

    def transpose(self):
        """Create a transpose of this matrix."""
        ma4 = Matrix4(self.get_col(0),
                      self.get_col(1),
                      self.get_col(2),
                      self.get_col(3))
        return ma4

    def is_identity(self):
        """Check to see if this matrix is an identity matrix."""
        for index, row in enumerate(self.dta):
            if row[index] == 1:
                for num, element in enumerate(row):
                    if num != index:
                        if element != 0:
                            return False
            else:
                return False

        return True

    def is_orthogonal(self):
        """Check to see if this matrix is orthogonal."""
        return (self * self.transpose()).is_identity()

    def inverse_as_orghogonal(self):
        """Get the inverse of this matrix, assuming this matrix is orthogonal."""
        return self.transpose()

    @staticmethod
    def identity():
        """Create and return an identity matrix."""
        ma4 = Matrix4((1, 0, 0, 0),
                      (0, 1, 0, 0),
                      (0, 0, 1, 0),
                      (0, 0, 0, 1))
        return ma4

    @staticmethod
    def translate(translationAmt):
        """Create a translation matrix."""
        if not isinstance(translationAmt, Vector3):
            raise ValueError("translationAmt must be a Vector3")

        ma4 = Matrix4((1, 0, 0, translationAmt.x),
                      (0, 1, 0, translationAmt.y),
                      (0, 0, 1, translationAmt.z),
                      (0, 0, 0, 1))
        return ma4

    @staticmethod
    def scale(scaleAmt):
        """
        Create a scale matrix.
        scaleAmt is a Vector3 defining the x, y, and z scale values.
        """
        if not isinstance(scaleAmt, Vector3):
            raise ValueError("scaleAmt must be a Vector3")

        ma4 = Matrix4((scaleAmt.x, 0, 0, 0),
                      (0, scaleAmt.y, 0, 0),
                      (0, 0, scaleAmt.z, 0),
                      (0, 0, 0, 1))
        return ma4

    @staticmethod
    def z_rotate(rotationAmt):
        """Create a matrix that rotates around the z axis."""
        ma4 = Matrix4((math.cos(rotationAmt), -math.sin(rotationAmt), 0, 0),
                      (math.sin(rotationAmt), math.cos(rotationAmt), 0, 0),
                      (0, 0, 1, 0),
                      (0, 0, 0, 1))

        return ma4

    @staticmethod
    def y_rotate(rotationAmt):
        """Create a matrix that rotates around the y axis."""
        ma4 = Matrix4((math.cos(rotationAmt), 0, math.sin(rotationAmt), 0),
                      (0, 1, 0, 0),
                      (-math.sin(rotationAmt), 0, math.cos(rotationAmt), 0),
                      (0, 0, 0, 1))
        return ma4

    @staticmethod
    def x_rotate(rotationAmt):
        """Create a matrix that rotates around the x axis."""
        ma4 = Matrix4((1, 0, 0, 0),
                      (0, math.cos(rotationAmt), -math.sin(rotationAmt), 0),
                      (0, math.sin(rotationAmt), math.cos(rotationAmt), 0),
                      (0, 0, 0, 1))

        return ma4

    @staticmethod
    def build_rotation(vec3):
        """
        Build a rotation matrix.
        vec3 is a Vector3 defining the axis about which to rotate the object.
        """
        if not isinstance(vec3, Vector3):
            raise ValueError("rotAmt must be a Vector3")
        return Matrix4.x_rotate(vec3.x) * Matrix4.y_rotate(vec3.y) * Matrix4.z_rotate(vec3.z)

"""line-intersection code from dr0id-book_programming_game_ai_by_example"""
def line_intersection_2d(A, B, C, D):
    rTop = (A.y - C.y) * (D.x - C.x) - (A.x - C.x) * (D.y - C.y)
    rBot = (B.x - A.x) * (D.y - C.y) - (B.y - A.y) * (D.x - C.x)

    sTop = (A.y - C.y) * (B.x - A.x) - (A.x - C.x) * (B.y - A.y)
    #sBot = (B.x - A.x) * (D.y - C.y) - (B.y - A.y) * (D.x - C.x)

    if (rBot == 0): #or (sBot == 0):
        # lines are parallel
        return False, None, None

    r = rTop / rBot
    s = sTop / rBot

    if (r > 0) and (r < 1) and (s > 0) and (s < 1):
        dist = distance(A,B) * r
        point = A + r * (B - A)
        return True, dist, point
    else:
        return False, 0, None


def line_intersection_point_2d(a, b, c, d):
    r_top = (a.y - c.y) * (d.x - c.x) - (a.x - c.x) * (d.y - c.y)
    r_bot = (b.x - a.x) * (d.y - c.y) - (b.y - a.y) * (d.x - c.x)
    s_top = (a.y - c.y) * (b.x - a.x) - (a.x - c.x) * (b.y - a.y)
    s_bot = (b.x - a.x) * (d.y - c.y) - (b.y - a.y) * (d.x - c.x)

    if r_bot == 0 or s_bot == 0:  # //parallel
        return False, None, None

    r = r_top / r_bot
    s = s_top / s_bot

    if (r > 0) and (r < 1) and (s > 0) and (s < 1):
        # lines intersect

        _dist = a.get_distance(b) * r
        _point = a + r * (b - a)
        return True, _point, _dist

    # lines do not intersect
    return False, None, None


def dist_to_line_segment_sq(a, b, p):
    """
    given a line segment AB and a point P, this function calculates the
    perpendicular distance between them.
    Avoiding sqrt.
    """
    # if the angle is obtuse between pa and ab is obtuse then the closest vertex must be A
    dot_a = (p.x - a.x) * (b.x - a.x) + (p.y - a.y) * (b.y - a.y)

    if dot_a <= 0:
        return a.get_distance_sq(p)

    # if the angle is obtuse between pb and ab is obtuse then the closest vertex must be B
    dot_b = (p.x - b.x) * (a.x - b.x) + (p.y - b.y) * (a.y - b.y)

    if dot_b <= 0:
        return b.get_distance_sq(p)

    # calculate the point along AB that is the closest to p
    point = a + ((b - a) * dot_a) / (dot_a + dot_b)

    # calculate the distance p-point
    return p.get_distance_sq(point)


def line_segment_circle_intersection(a, b, p, r):
    """
    returns true if the line segemnt AB intersects with a circle at
    position P with radius radius
    """
    # first determine the distance from the center o the circle to
    # the line segment (working in distance squared space)
    dist_to_line_sq = dist_to_line_segment_sq(a, b, p)

    if dist_to_line_sq < r * r:
        return True
    else:
        return False


def do_lines_intersect_circle(walls, cur_pos, radius):
    # test against the walls
    for wall in walls:
        # do a line segment intersection test
        # if line_segment_circle_intersection(wall.start, wall.end, cur_pos, radius):
        #     return True
        # optimized by inlining method 'line_segment_circle_intersection'
        dist_to_line_sq = dist_to_line_segment_sq(wall.start, wall.end, cur_pos)

        if dist_to_line_sq < radius * radius:
            return True
        # else:
        #     return False

    return False


def find_closest_point_of_intersection_with_walls(a, b, walls):
    distance = sys.maxsize
    this_impact_point = None
    for wall in walls:
        is_intersecting, impact_point, dist = line_intersection_point_2d(a, b, wall.start, wall.end)
        if is_intersecting:
            if dist < distance:
                distance = dist
                this_impact_point = impact_point

    if distance < sys.maxsize:
        return True, this_impact_point, distance

    return False, this_impact_point, distance