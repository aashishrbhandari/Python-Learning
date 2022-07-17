# Python Day-To-Day Usefull Snippets

<p> Note: here command or snippets are for python3, most the command might work in python2 and you might have to change few things to make it work in python2
</p>

---

### Quickly find the python version
> A very basic one but important part here to know is most of the command will have the same syntax to get the version details

```python3
python3 --version
```
---

### Simplest Hello (without world)
> Again a basic once, but this tells us that we can run a small python snippet just via the cli, without writing/creating a python file. a lot of other programming languages (basically their executables) also gives the same functionality

```python3
python -c "print('Hello')"
```
---

### Get MD5 Hash
> A quick way to get MD5 hash of a string
```python3
python3 -c "import hashlib; print(hashlib.md5(b'Ashish').hexdigest())"
```
> same goes for sha512
```python3
python3 -c "import hashlib; print(hashlib.sha512(b'Ashish').hexdigest())"
```
---


### A Simple Python3 HTTP Server (@ Port 80)
> If you have a requirement of to transfer files (over http), this small cli based approach of python can help you quickly expose all the files (hierarchy with subfolder and files) of your CWD over http port (you can customize the port as per your requirement)

```python3
python3 -m http.server 80
```

---
<!--
## File Handling

### Read a Compressed File (Zip)
> The Efficient & Effective way of reading a ZIP file in python, you will require this if you are trying to process a ZIP file line by line, in situation like gathering a string count or extracting data.
<br>
Reference: 
https://stackoverflow.com/questions/11482342/read-a-large-zipped-text-file-line-by-line-in-python/11482347

```python3
import zipfile

zip_file = "syslog.zip"

with zipfile.ZipFile(zip_file) as z:
    with z.open(zip_file) as f:
        for line in f:
            print(line)
            
```

### Read a Compressed File (Zip)

```python3
import tarfile

tar_file = "syslog.zip"

with tarfile.TarFile(tar_file) as t:
    with t.open(tar_file) as f:
        for line in f:
            print(line)
            
```

-->