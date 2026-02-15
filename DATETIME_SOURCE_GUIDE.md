# 📅 Understanding Python's `datetime` Module

## Your Question:
```python
from datetime import datetime
start_time = datetime.now()
```
**Where is `datetime` imported from? How to see its source code?**

---

## 🎯 The Import Hierarchy Explained

### What This Import Means:
```python
from datetime import datetime
#    ^^^^^^^^         ^^^^^^^^
#    module name      class name
```

This is a **nested import**:
1. `datetime` (first) = The **module** (a Python file)
2. `datetime` (second) = A **class** inside that module

### Full Structure:
```
datetime module (datetime.py)
├── date class
├── time class
├── datetime class  ← This is what you import
├── timedelta class
├── timezone class
└── tzinfo class
```

---

## 📍 Where is `datetime` Located?

On your Mac (Python 3.9.6):
```
/Library/Developer/CommandLineTools/Library/Frameworks/Python3.framework/Versions/3.9/lib/python3.9/datetime.py
```

### General locations by OS:
- **macOS**: `/Library/.../python3.9/datetime.py`
- **Linux**: `/usr/lib/python3.x/datetime.py`
- **Windows**: `C:\Python3x\Lib\datetime.py`

---

## 🔍 How to Find the Source Code Location

### Method 1: Using Python interactively
```python
import datetime
print(datetime.__file__)
# Output: /path/to/python3.9/datetime.py
```

### Method 2: Using inspect module
```python
import inspect
from datetime import datetime

# Get the file location
print(inspect.getfile(datetime))

# Try to get source code (for Python-implemented methods)
try:
    print(inspect.getsource(datetime))
except TypeError:
    print("This is implemented in C, no Python source")
```

### Method 3: Terminal command
```bash
# Find where datetime module is
python3 -c "import datetime; print(datetime.__file__)"

# View the source file
python3 -c "import datetime; print(datetime.__file__)" | xargs cat
```

---

## 📖 How to View the Source Code

### Option 1: View in Terminal
```bash
# View entire file
cat /Library/Developer/CommandLineTools/Library/Frameworks/Python3.framework/Versions/3.9/lib/python3.9/datetime.py

# View first 100 lines
head -100 /path/to/datetime.py

# Search for specific function
grep -A 20 "def now" /path/to/datetime.py
```

### Option 2: Open in VS Code
```bash
code /Library/Developer/CommandLineTools/Library/Frameworks/Python3.framework/Versions/3.9/lib/python3.9/datetime.py
```

### Option 3: Use Python's inspect module
```python
import inspect
from datetime import datetime

# View source of methods
print(inspect.getsource(datetime.strptime))  # Works for pure Python methods
```

### Option 4: Online
View Python's official source code:
- GitHub: https://github.com/python/cpython/blob/3.9/Lib/datetime.py
- Python Docs: https://docs.python.org/3/library/datetime.html

---

## ⚠️ Important: C vs Python Implementation

### The `datetime.now()` Method
```python
from datetime import datetime
datetime.now()  # <built-in method now of type object>
```

**Key point**: `datetime.now()` is a **built-in method** (implemented in C for performance).

### What This Means:
1. **Python wrapper** exists in `datetime.py`:
   ```python
   class datetime(date):
       def now(cls, tz=None):
           # This delegates to C implementation
           ...
   ```

2. **Actual implementation** is in C code:
   - Located in: `Modules/_datetimemodule.c` (in CPython source)
   - Compiled into Python's binary
   - Much faster than pure Python

### How to Find C Source:
```bash
# Clone CPython repository
git clone https://github.com/python/cpython.git
cd cpython

# Find C implementation
cat Modules/_datetimemodule.c | grep -A 50 "datetime_now"
```

---

## 🧪 Practical Examples

### Example 1: Inspect datetime in Python
```python
#!/usr/bin/env python3
import inspect
from datetime import datetime

print("Module:", datetime.__module__)
print("File:", inspect.getfile(datetime))
print("Is built-in now():", inspect.isbuiltin(datetime.now))
print("\nDocstring:")
print(datetime.now.__doc__)
```

### Example 2: View Available Methods
```python
from datetime import datetime

# All methods and attributes
print(dir(datetime))

# Filter to show only public methods
methods = [m for m in dir(datetime) if not m.startswith('_')]
print("Public methods:", methods)
```

### Example 3: Interactive Source Exploration
```python
import inspect
from datetime import datetime, timedelta

# These work (pure Python):
print(inspect.getsource(timedelta.__add__))
print(inspect.getsource(datetime.strptime))

# These don't work (C implementation):
try:
    print(inspect.getsource(datetime.now))
except TypeError as e:
    print(f"Cannot view: {e}")
```

---

## 📚 Understanding the Import Statement

### Different Ways to Import:

```python
# 1. Import entire module
import datetime
start_time = datetime.datetime.now()
#             ^^^^^^^^ ^^^^^^^^ ^^^
#             module   class    method

# 2. Import specific class (what you're using)
from datetime import datetime
start_time = datetime.now()
#            ^^^^^^^^ ^^^
#            class    method

# 3. Import with alias
from datetime import datetime as dt
start_time = dt.now()

# 4. Import multiple items
from datetime import datetime, timedelta, timezone

# 5. Import everything (not recommended)
from datetime import *
```

---

## 🔧 How to Explore Any Python Module

### Universal Method:
```python
import <module>

# 1. Find location
print(<module>.__file__)

# 2. View documentation
print(<module>.__doc__)
help(<module>)

# 3. List contents
print(dir(<module>))

# 4. View source (if available)
import inspect
print(inspect.getsource(<module>))
```

### Example with FastAPI:
```python
import fastapi
import inspect

print("Location:", fastapi.__file__)
print("\nFastAPI class source:")
print(inspect.getsource(fastapi.FastAPI))
```

---

## 🎓 Summary

### Your Code:
```python
from datetime import datetime
start_time = datetime.now()
```

### What Happens:
1. Python looks for `datetime.py` in standard library paths
2. Finds it at: `/path/to/python3.9/datetime.py`
3. Imports the `datetime` class from that module
4. Calls `now()` method (implemented in C for speed)
5. Returns current timestamp

### The Hierarchy:
```
Standard Library (built-in to Python)
    └── datetime.py (module)
            └── datetime (class)
                    ├── now() [C implementation]
                    ├── strptime() [Python implementation]
                    ├── strftime() [C implementation]
                    └── ... other methods
```

---

## 🚀 Quick Reference Commands

```bash
# Find module location
python3 -c "import datetime; print(datetime.__file__)"

# View source file
python3 -c "import datetime; print(datetime.__file__)" | xargs less

# Open in VS Code
python3 -c "import datetime; print(datetime.__file__)" | xargs code

# Check if method is built-in (C)
python3 -c "from datetime import datetime; import inspect; print(inspect.isbuiltin(datetime.now))"

# View online
open https://github.com/python/cpython/blob/3.9/Lib/datetime.py
```

---

**Created:** December 16, 2025  
**Python Version:** 3.9.6  
**Platform:** macOS
