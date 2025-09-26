from loguru import logger

# Archivo de log rotativo
logger.add(
    "runtime.log",       # Nombre del archivo de salida
    rotation="5 MB",     # Se rota al llegar a 5 MB
    retention=5,         # Mantener 5 archivos antiguos
    level="INFO",        # Nivel de log (DEBUG, INFO, WARNING, ERROR)
    backtrace=True,      # Mostrar traceback detallado en errores
    diagnose=True        # Info adicional en excepciones
)

__all__ = ["logger"]
