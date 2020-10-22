import pygame



def is_numeric(s):
    """trys to parse the string as int or float"""
    try:
        x = int(s)
    except:
        try:
            x = float(s)
        except:
            x = None
    return x

def get_images(sheet, frame_indices, size):
    """Get desired images from a sprite sheet image."""
    frames = []
    for cell in frame_indices:
        frame_rect = ((size[0]*cell[0],size[1]*cell[1]), size)
        frames.append(sheet.subsurface(frame_rect))
    return frames

def get_allImages(sheet,size):
    """Get images from a sprite sheet image.
    returns a list of tiles from top left to bottom right
    """
    frames = []
    maxx = sheet.get_width() // size[0]
    maxy = sheet.get_height() // size[1]
    for x in range(0, maxx):
        for y in range(0, maxy):
            frame_rect = ((size[0]*x,size[1]*y), size)
            frames.append(sheet.subsurface(frame_rect))
    return frames

def get_allImagesInDirectory(sheet,size):
    """Get images from a sprite sheet image.
    returns a list of tiles from top left to bottom right
    """
    #todo
    frames = []
    maxx = sheet.get_width() // size[0]
    maxy = sheet.get_height() // size[1]
    for x in range(0, maxx):
        for y in range(0, maxy):
            frame_rect = ((size[0]*x,size[1]*y), size)
            frames.append(sheet.subsurface(frame_rect))
    return frames


def get_class(fully_qualified_path, module_name, class_name, *instantiation):
    """
    Returns an instantiated class for the given string descriptors
    :param fully_qualified_path: The path to the module eg("Utilities.Printer")
    :param module_name: The module name eg("Printer")
    :param class_name: The class name eg("ScreenPrinter")
    :param instantiation: Any fields required to instantiate the class
    :return: An instance of the class
    """

    #todo: thats not working ! Maybe use this:
    #import importlib
    #def str_to_class(module_name, class_name):
    #    """Return a class instance from a string reference"""
    #    try:
    #        module_ = importlib.import_module(module_name)
    #        try:
    #            class_ = getattr(module_, class_name)()
    #        except AttributeError:
    #            logging.error('Class does not exist')
    #    except ImportError:
    #        logging.error('Module does not exist')
    #    return class_ or None

    p = __import__(fully_qualified_path)
    m = getattr(p, module_name)
    c = getattr(m, class_name)
    instance = c(*instantiation)
    return instance