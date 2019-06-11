# Minesweeper

## Screenshots

![alt text](screenshots/home.png)

![alt text](screenshots/game.png)

![alt text](screenshots/game2.png)

## Prerequisites
Make sure your computer has the following software installed:
1. Python
2. MongoDB

## How to run this project on your computer

#### 1. Clone the source code
```
$git clone https://github.com/giangvu/Minesweeper.git
```

#### 2. Create and activate virtual environment
On Windows:
```
$virtualenv venv
$venv\Scripts\activate.bat
```

On Linux:
```
$virtualenv venv
$source venv/bin/activate
```

#### 3. Install libraries
```
$pip install -r requirements.txt
```

#### 4. Run the web application
```
$ python app.py
```

### Notes:
* Make sure your MongoDB listens on the same port as the value of `app.config['MONGO_PORT']` in the `app.py`. By default this value is `27017`

