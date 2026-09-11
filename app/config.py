"""
Configuración centralizada de la aplicación.

Este módulo proporciona variables de configuración para desarrollo,
testing y producción, con soporte para variables de entorno.

Uso:
  from app.config import settings
  print(settings.DATABASE_URL)
"""

import os
from enum import Enum
from typing import Optional


class Environment(str, Enum):
    """Entornos de ejecución."""
    DEVELOPMENT = "development"
    TESTING = "testing"
    PRODUCTION = "production"


class Settings:
    """Configuración de la aplicación."""

    # Entorno
    ENVIRONMENT: Environment = Environment(
        os.getenv("ENVIRONMENT", "development")
    )

    # Base de Datos
    DATABASE_URL: str = os.getenv(
        "DATABASE_URL",
        "sqlite:///./gestion_tareas.db"
    )
    DATABASE_NAME: str = os.getenv(
        "DATABASE_NAME",
        "gestion_tareas.db"
    )

    # API
    API_TITLE: str = "Sistema de Gestión de Tareas"
    API_VERSION: str = "1.0.0"
    API_PREFIX: str = "/api/v1"
    API_DESCRIPTION: str = (
        "API REST para gestión de empleados y asignación de tareas. "
        "Implementa arquitectura MVC con principios SOLID."
    )

    # CORS
    CORS_ORIGINS: list = [
        "http://localhost:3000",
        "http://127.0.0.1:3000",
        "http://localhost:8080",
        "http://127.0.0.1:8080",
    ]
    if ENVIRONMENT == Environment.DEVELOPMENT:
        CORS_ORIGINS.append("*")

    CORS_CREDENTIALS: bool = True
    CORS_METHODS: list = ["*"]
    CORS_HEADERS: list = ["*"]

    # Seguridad
    DEBUG: bool = os.getenv("DEBUG", "True").lower() == "true"
    SECRET_KEY: str = os.getenv(
        "SECRET_KEY",
        "dev-secret-key-change-in-production"
    )

    # Logging
    LOG_LEVEL: str = os.getenv("LOG_LEVEL", "INFO")
    LOG_FORMAT: str = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"

    # Paginación (para futuras consultas)
    PAGE_SIZE: int = 20
    MAX_PAGE_SIZE: int = 100

    @classmethod
    def is_development(cls) -> bool:
        """Verifica si está en entorno de desarrollo."""
        return cls.ENVIRONMENT == Environment.DEVELOPMENT

    @classmethod
    def is_production(cls) -> bool:
        """Verifica si está en entorno de producción."""
        return cls.ENVIRONMENT == Environment.PRODUCTION

    @classmethod
    def is_testing(cls) -> bool:
        """Verifica si está en entorno de testing."""
        return cls.ENVIRONMENT == Environment.TESTING


# Instancia global de configuración
settings = Settings()
