# in cmd, run: py build.py build

import cx_Freeze

executables = [cx_Freeze.Executable("chengyu-maze.pyw", icon="icon.ico", base=None, target_name='chengyu-maze.exe')]

cx_Freeze.setup(
    name="Chengyu Maze",
    options={"build_exe": {"packages":["pygame","os","csv","random"],
                           "include_files":["assets/"], "excludes":["anyio","argon2-cffi","argon2-cffi-bindings","asttokens","attrs","Babel","backcall","beautifulsoup4","bleach","certifi","cffi","charset-normalizer","click","colorama","cx-Freeze","cx-Logging","debugpy","decorator","defusedxml","entrypoints","et-xmlfile","executing","ftfy","idna","ipykernel","ipython","ipython-genutils","jedi","Jinja2","joblib","json5","jsonschema","jupyter-client","jupyter-core","jupyter-server","jupyterlab","jupyterlab-pygments","jupyterlab-server","langcodes","lief","MarkupSafe","matplotlib-inline","mistune","msgpack","nbclassic","nbclient","nbconvert","nbformat","nest-asyncio","nltk","notebook","notebook-shim","openpyxl","packaging","pandocfilters","parso","pickleshare","pip","prometheus-client","prompt-toolkit","psutil","pure-eval","pycparser","pydub","Pygments","pyparsing","pypinyin","pyrsistent","python-dateutil","pytz","pywin32","pywinpty","pyzmq","regex","requests","Send2Trash","setuptools","six","sniffio","soupsieve","stack-data","terminado","testpath","tornado","tqdm","traitlets","urllib3","wcwidth","webencodings","websocket-client","wget","wordfreq","you-get"]}},
    executables = executables)