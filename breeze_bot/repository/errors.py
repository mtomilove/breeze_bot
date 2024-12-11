class RepositoryError(Exception):
    pass


class NotFoundError(RepositoryError):
    pass