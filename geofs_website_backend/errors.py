class IntegrityError(Exception):
    def __init__(self, *args):
        Exception.__init__(self, *args)


class EnvVariableError(Exception):
    def __init__(self, *args):
        Exception(self, *args)


class GitError(Exception):
    def __init__(self, *args):
        Exception(self, *args)
