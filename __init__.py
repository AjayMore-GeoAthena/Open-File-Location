def classFactory(iface):
    from .OpenFileLocationPlugin import OpenFileLocationPlugin
    return OpenFileLocationPlugin(iface)