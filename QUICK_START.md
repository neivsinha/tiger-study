# Quick Start Guide

## 🚀 Get Started in 3 Steps

### Step 1: Setup (First Time Only)
```bash
./setup.sh
```
This will:
- Create virtual environment
- Install all dependencies
- Create and seed the database with sample data

### Step 2: Run the Application
```bash
./run.sh
```

### Step 3: Open in Browser
Navigate to: **http://127.0.0.1:5000**

That's it! 🎉

---

## Alternative Manual Setup

If you prefer manual setup:

```bash
# 1. Create virtual environment
python3 -m venv venv

# 2. Activate it
source venv/bin/activate  # On Windows: venv\Scripts\activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Seed database
python seed_data.py

# 5. Run application
python app.py
```

---

## Resetting the Database

To reset with fresh sample data:
```bash
./venv/bin/python seed_data.py
```

---

## Stopping the Application

Press `Ctrl+C` in the terminal where the app is running.

---

## Troubleshooting

### "Permission denied" when running setup.sh
```bash
chmod +x setup.sh run.sh
```

### "Port already in use"
Edit `app.py` and change:
```python
app.run(debug=True, port=5001)  # Use different port
```

### Can't find Python 3
Try:
```bash
python3 --version
```
Make sure Python 3.7+ is installed.

---

## What's Included?

After setup, you'll have:
- ✅ 15 Princeton courses
- ✅ 37 sample study groups
- ✅ Realistic participant data
- ✅ Mix of upcoming and past meetings
- ✅ Various locations and capacities

---

## Need Help?

Check the full documentation:
- [README.md](README.md) - Complete documentation
- [DEMO_GUIDE.md](DEMO_GUIDE.md) - How to demo the app
- [PROJECT_SUMMARY.md](PROJECT_SUMMARY.md) - Technical overview
- [FEATURES.md](FEATURES.md) - Feature list

---

**Happy studying! 🐅**
