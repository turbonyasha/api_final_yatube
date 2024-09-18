# Финальный проект спринта: API для Yatube

### Как запустить проект:

Клонируйте репозиторий и перейдите в него в терминале:

```
git clone git@github.com:turbonyasha/api_final_yatube.git
```

```
cd api_final_yatube
```

Cоздайте и активируйте виртуальное окружение:

```
python -m venv env
```
```
source env/scripts/activate
```

Установите зависимости из файла requirements.txt:

```
pip install -r requirements.txt
```

Не забудьте выполнить миграции:

```
python3 manage.py migrate
```

Запустите проект с помощью команды в терминале:

```
python manage.py runserver
```