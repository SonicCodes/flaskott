# Flaskott 🔥
## [Hotpress](https://github.com/SonicCodes/hotpress) for Flask, it's really hot.

Basically [Hotpress](https://github.com/SonicCodes/hotpress) remade for flask, it's really developmental at this stage, you are free to make contributions and prs, and don't forget to issue if you got something wrong.

All the features in Hotpress are included, and it does live code swapping, using killable threads.

The steps are pretty easy compared to Hotpress.

### #1 - your main app.py
```python
from reloader import init
from flask import Flask

app = Flask(__name__)

init(app, "./server.py")

# Or

if __name__ == '__main__':
    init(app, "./server.py")
```


### #2 - create a reloadable file (server.py)
```python
from reloader import pre_setup, post_setup

app = pre_setup(locals()) # correctly typed, IDE support is still there


@app.route("/hie")
def executing():
    return "Hie you too! I am your fairy mother, change something here to be surprised!"


post_setup(locals()) # this is used to hold the process from exiting.
```


### Result
![Screen Shot 2021-05-09 at 4 10 53 AM](https://user-images.githubusercontent.com/48802163/117557576-e9cea780-b07c-11eb-98fa-b2a28747d8f4.png)


### Requirements
- [watchgod](https://pypi.org/project/watchgod/)
- [flask](https://pypi.org/project/Flask/)
- [asyncio](https://pypi.org/project/asyncio/)

Flask is hard requirement, the others could be eliminated from the codebase with proper care.


### Note!
I’ll repeat, this is highly experimental, it was a proof of concept that python could do the same thing as Nodejs when it comes too hot-reloading, I highly advise you to not using it for anything other-than experimenting & research stuff. I hope you understand my message well.


### Licesnce
```
Do what ever you want with this, but keep in-mind, I am not liable to any damage the software, it's usage/mis-use might cause at any point of time and without any regards.
```



