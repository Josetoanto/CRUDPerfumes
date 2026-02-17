# app/modules/perfumes/exceptions.py

class PerfumeNotFound(Exception):
    """Se lanza cuando un perfume no existe para el usuario dado."""
    def __init__(self, message: str = "Perfume no encontrado"):
        super().__init__(message)


class PerfumeIntegrityError(Exception):
    """Se lanza cuando ocurre un error de integridad en la base de datos."""
    def __init__(self, message: str = "Error de integridad al crear/actualizar perfume"):
        super().__init__(message)
