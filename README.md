# GigaChat_api
![Static Badge](https://img.shields.io/badge/3.11-blue?label=Python)
![Static Badge](https://img.shields.io/badge/aiohttp-orange)
![Static Badge](https://img.shields.io/badge/asyncio-orange)

__________________________________________________

![logo](https://spark.ru/upload/other/b_64f789cc472b4.jpg)

### To use this script, please first read the documentation provided by the developers of the [GigaChat](https://developers.sber.ru/docs/ru/gigachat/individuals-quickstart) model

### Installation:
```
pip install -r requirements.txt
pip install https://github.com/Zloy-tarakaniscshe/GigaChat_api/tree/master.zip
```

The configuration file with the directory name config contains a .env.template - replace it with exactly the same file 
named .env and specify the correct settings for making requests to the gigachat model

### Usage example:
* ***generation of text responses***
```python
from gigachat_src.GigaChat import GigaChat


example_class = GigaChat(version="GigaChat-Pro", temperature=1.5)
answer = example_class.start_request("some text")
# type(answer) == dict or list[dict]
```

* ***image generation***
```python
from gigachat_src.GigaChat import GenerationImage


example_class = GenerationImage(image_name="some name", save_image_flag=True)
example_class.start_gen_image(request="some request")
```

### Script features:
1) ___Automate the analysis of text data in a conversational format or process multiple text data at once___
2) ___Generating images on request___
3) ___In case of long-term multiple requests to the model, it sends an email notification about the completion of work___ 


### This script is still in the process of being finalized, and will be updated and supplemented as it improves
