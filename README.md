# Face-Recognition-DjangoApp

This is a Django App which autheticates using Facial recognition

**Steps to run:**
1. Clone this Repo
```
git clone https://github.com/NP-compete/Face-Recognition-DjangoApp
```
2. cd into the directory
```
cd Face-Recognition-DjangoApp
```
3. Download the shape Predictor file from [here](https://drive.google.com/file/d/12yzYGzXu8LZz0Zi4-89Qu90WPMuyoQBX/view?usp=sharing)
4. Put the file in [DL Models](https://github.com/NP-compete/Face-Recognition-DjangoApp/tree/master/DLModels) folder
5. Make migrations
```
python manage.py makemigrations
```
6. Migrate
```
python manage.py migrate
```
7. Runserver
```
python manage.py runserver
```
8. Open web browser at [http://localhost:8000](http://localhost:8000)
