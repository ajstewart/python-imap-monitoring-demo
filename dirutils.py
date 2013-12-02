import os
def ensure_dir(dirname):
    """Ensure directory exists, or raise exception if file of same name exists."""
    if not os.path.exists(dirname):
        os.makedirs(dirname)
    elif not os.path.isdir(dirname):
        raise RuntimeError("Path exists but is not directory: \n" + dirname)

def ensure_parent_dir(filename):
    """Ensure parent directory exists, so you can write to `filename`."""
    d = os.path.dirname(filename)
    if not os.path.exists(d):
        print "Making directory", d
        os.makedirs(d)

