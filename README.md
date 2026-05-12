## Configuración de pre-commit

Este proyecto utiliza `pre-commit` para garantizar el estilo de código (PEP 8) y análisis estático antes de cada commit.

### Instalación
1. Crear y activar el entorno virtual.
2. Instalar dependencias:

pip install pre-commit black flake8
3. guarda dependencias
pip install pre-commit black flake8
4. crear  .pre-commit-config.yaml
repos:
  - repo: https://github.com/psf/black
    rev: 24.10.0
    hooks:
      - id: black
        exclude: |
          (^migrations/)|(^venv/)|(^.venv/)|(^__pycache__/)

  - repo: https://github.com/pycqa/flake8
    rev: 7.1.1
    hooks:
      - id: flake8
        exclude: |
          (^migrations/)|(^venv/)|(^.venv/)|(^__pycache__/)
    
5. crear .flake8
[flake8]
max-line-length = 88
exclude =
    migrations,
    venv,
    .venv,
    __pycache__,
    manage.py

6. crear pyproject.toml
[tool.black]
line-length = 88
exclude = '''
/(
    migrations
  | venv
  | \.venv
  | __pycache__
)/
'''

7. isntalar el hooks en git
pre-commit install

8. probar que bloquea commits
9. hacer git add. y despues el commit, git commit -m "prueba hooks"