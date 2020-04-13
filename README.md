# kis-admission

#### server

```
$ pip install -r requirements.txt
$ py.test server/tests.py
$ python -m server 127.0.0.1 1337
```

По задумке, умеет:
- отправить help в начале игры
- не снимать попытки, когда букву уже пробовали
- отправить состояние игры по команде ``?''
- 
