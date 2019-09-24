def createFolder(self, directory):
    try:
        if not os.path.exists(directory):
            os.makedirs(directory)
    except OSError:
        print('Error: Creating directory. ' + directory)


def to_str(self, var):
    return str(list(np.reshape(np.asarray(var), (1, np.size(var)))[0]))[1:-1]

