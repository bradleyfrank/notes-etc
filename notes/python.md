# Python

## Variables

- **`_var`:** Naming convention indicating name is meant for internal use. A hint for programmers and not enforced by programmers.
- **`__var`:** Triggers name mangling when used in class context. Enforced by the Python interpreter.
- **`var_`:** Used by convention to avoid naming conflicts with Python keywords.
- **`__var__`:** Indicates special methods defined by Python language.
- **`_`:** Used as a name for temporary variables.

## Strings

```python
# f-strings with dictionary
>>> values = {'first': 'Bill', 'last': 'Bailey'}
>>> "Won't you come home {first} {last}?".format(**values)
"Won't you come home Bill Bailey?"

# text padding
>>> count = 43
>>> f"|{count:5d}"
'|   43'
>>> padding = 10
>>> f"|{count:{padding}d}"
'|        43'
```

## Matching / Switch Case

```python
text = "18:32:50"
#text = "18:32"
#text = "tea time"

match text.split(":"):
    case [h, m]:
        print(f"{h} hours and {m} minutes")
    case [h, m, s]:
        print(f"{h} hours, {m} minutes and {s} seconds")
    case _:
        print("oops")
```

```python
data = response.json()

#  Python 3.9
for item in data["items"]:
    sha = item["sha"]
    message = item["commit"]["message"]
    name = item["commit"]["author"]["name"]

#  Python 3.10
for item in data["items"]:
    match item:
        case {"sha": sha, "commit": {"message": message, "author": {"name": name}}}:
            print(sha, "by", name)
            print(message)
            print(80*"-")
```

```python
# Python 3.9
if isinstance(message, SnakeChangeDirectionMessage):
    if message.direction != opposite_direction:
        self.direction = message.direction
elif isinstance(message, EntityCollisionMessage) and message.entity is self:
    if isinstance(message.other, (Snake, Wall)):
        new_messages.append(GameOverMessage("Snake collision"))
    elif isinstance(message.other, Food):
        self.max_length += 1
        new_messages.append(RemoveEntityMessage(message.other))
        new_messages.append(SpawnFoodMessage())

# Python 3.10
match message:
    case SnakeChangeDirectionMessage(direction):
        if direction != opposite_direction:
            self.direction = direction
    case EntityCollisionMessage(entity, other) if entity is self:
        match other:
            case Wall() | Snake():
                new_messages.append(GameOverMessage("Snake collision"))
            case Food():
                self.max_length += 1
                new_messages.append(RemoveEntityMessage(other))
                new_messages.append(SpawnFoodMessage())
```

## Arrays

```python
# transpose a 2D array
array = [['a', 'b'], ['c', 'd'], ['e', 'f']]
transposed = zip(*array)
print(transposed) # [('a', 'c', 'e'), ('b', 'd', 'f')]
```

## Loops

```python
# track the index value and element together with a tuple
for i, name in enumerate(names):
   print(i, name)
```

```python
# Before:
for x in listA:
    for y in listB:
        r.append((x, y))
# After:
for x, y in itertools.product(listA, listB):     
    r.append((x, y))
```

```python
names = ["A","B","C"]
[x.lower() for x in names] # wrong
list(map(str.lower, names)) # right
```

## Regex

```python
# versions_tf_content: required_version = ">= 0.13"
# terraform_bin_path = "13"
required_version = r'required_version\s=\s"[>=]+\s[0-9]+\.([0-9]+)"'
if match := re.search(required_version, versions_tf_content):
    terraform_bin_path = match.group(1)
```

## Debugging

```python
import requests

def make_request():
    result = requests.get("https://google.com")
    import ipdb; ipdb.set_trace()

make_request()
```

```text
python3 test.py
--Return--
None
> /home/bork/work/homepage/test.py(5)make_request()
      4     result = requests.get("https://google.com")
----> 5     import ipdb; ipdb.set_trace()
      6 

ipdb> result.headers
{...}
```

## Anaconda

```sh
conda create --name snakes python=3.5 # create environment
conda env list # list environments

# activate/deactivate
. /usr/local/anaconda3/bin/activate
conda deactivate

# updating
conda update -n base conda -y
conda update --prefix /usr/local/anaconda3 anaconda -y
conda clean --all -y
```
