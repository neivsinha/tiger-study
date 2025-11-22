#!/bin/bash
# Setup script for Princeton Study Group Finder

echo "============================================================"
echo "Princeton Study Group Finder - Setup"
echo "============================================================"
echo ""

# Check if venv exists
if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv venv
    echo "✓ Virtual environment created"
else
    echo "✓ Virtual environment already exists"
fi

echo ""
echo "Installing dependencies..."
./venv/bin/pip install -r requirements.txt

echo ""
echo "Seeding database..."
./venv/bin/python seed_data.py

echo ""
echo "============================================================"
echo "Setup completed successfully!"
echo "============================================================"
echo ""
echo "To start the application, run:"
echo "  ./run.sh"
echo ""
echo "Or manually:"
echo "  source venv/bin/activate"
echo "  python app.py"
echo ""
