import numpy as np

""" vec.py contains these 'classes' (actually more like namespaces)
        Vec3
        Vec2
"""

class Vec3(object):
    """
    A helper class for 3d points, just to hide obscure numpy syntax

    >>> vec = [1,2,3]
    >>> len = Vec3.length(vec)
    >>> np.allclose(len, 3.7416573)
    True
    >>> nlen = Vec3.normalize(Vec3.asVec3(vec))
    >>> np.allclose(nlen, len)
    True
    """

    @staticmethod
    def length(vec3):
        return np.linalg.norm(vec3, 2, -1)
    
    @staticmethod
    def asVec3(vec3):
        assert len(vec3) == 3 
        return np.array(vec3, dtype=np.float64, copy=False)

    @staticmethod
    def normalize(vec3):
        """ nb: this wont overwrite vec3 unless it's an np.array """
        len = np.linalg.norm(vec3, 2, -1)
        vec3 /= len
        return len

class Vec2(object):
    """
    A helper class for 2d points, just to hide obscure numpy syntax

    >>> vec = [1,1]
    >>> len = Vec2.length(vec)
    >>> np.allclose(len, 1.4142135623730951)
    True
    >>> nlen = Vec2.normalize(Vec2.asVec2(vec))
    >>> np.allclose(nlen, len)
    True
    """

    @staticmethod
    def length(vec2):
        return np.linalg.norm(vec2, 2, -1)
    
    @staticmethod
    def asVec2(vec2):
        assert len(vec2) == 2 
        return np.array(vec2, dtype=np.float64, copy=False)

    @staticmethod
    def normalize(vec2):
        """ nb: this wont overwrite vec3 unless it's an np.array """
        len = np.linalg.norm(vec2, 2, -1)
        vec2 /= len
        return len

if __name__ == "__main__":
    import doctest
    doctest.testmod()
