# Contenido para src/domain/system.py

"""
Este módulo contiene la lógica de negocio pura (Dominio) para obtener el estado
base del sistema.

Es la capa más interna y NO debe importar librerías de infraestructura como FastAPI,
Pydantic o bases de datos.
"""


def build_status_message(project_name: str, environment: str) -> dict:
    """
    Construye el mensaje de estado del sistema.

    Args:
        project_name: El nombre del proyecto.
        environment: El ambiente actual.

    Returns:
        Un diccionario con el estado y el mensaje generado.
    """
    message = (
        f"¡Hola Mundo! Proyecto '{project_name}' [ENV: {environment}]. "
        "El servicio está en línea. Lógica de Dominio Pura."
    )
    return {"status": "ok", "message": message}
