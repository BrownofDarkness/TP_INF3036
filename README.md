# TP_INF3036

une application web permettant la gestion des annonces de vente de voitures en ligne.

Comment executer l'application :
- Vous devez avoir python
  
- Cree un environment virtuelle
  
  ```bash
  python -m venv env
  ```
  
- activer l'environment virtuelle
  
  Sur linux

  ```
  source ./env/bin/activate
  ```

  Sur windows

  ```
  .\env\Scripts\activate
  ```

- Vous devez installer les dependance avec
  
  ```bash
  cd src/AnnoncesApp/
  ```

  ```
  pip install -r requirements.txt
  ```

- executer l'application
  
  ## Pour la premier fois
  
  - Vous devez executer tous ces commande
  
    ```bash
    python manage.py makemigrations
    ```

    ```bash
    python manage.py migrate
    ```

    ```bash
    python manage.py createsuperuser
    ```

    ```bash
    python manage.py runserver
    ```

  - Le cas echeant
  
    ```bash
    python manage.py runserver
    ```
