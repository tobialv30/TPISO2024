

# Init

Clonar el repositorio por https o ssh

En la raiz del repositorio ejecuta

```sh
python -m venv venv
```

Luego activamos el entorno virtual, en linux es de esta manera:

```sh
source venv/bin/activate
```

> **Nota:*** En windows no tengo idea como se activa pero es mas o menos similar.


Luego instalamos las dependencias del proyecto

```sh
pip install -r requirements.txt
```

Por ultimo lo ejecutamos

```sh
python src/main.py
```