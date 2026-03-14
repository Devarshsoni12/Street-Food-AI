#!/usr/bin/env python3
"""
Quick Start Script for Indian Street Food AI
This script automates the initial setup process
"""

import os
import sys
import subprocess
import shutil

def print_header(text):
    """Print formatted header"""
    print("\n" + "=" * 60)
    print(f"  {text}")
    print("=" * 60 + "\n")

def run_command(command, description):
    """Run shell command with description"""
    print(f"⏳ {description}...")
    try:
        result = subprocess.run(command, shell=True, check=True, capture_output=True, text=True)
        print(f"✅ {description} - Success!")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ {description} - Failed!")
        print(f"Error: {e.stderr}")
        return False

def check_python_version():
    """Check if Python version is compatible"""
    print_header("Checking Python Version")
    version = sys.version_info
    print(f"Python version: {version.major}.{version.minor}.{version.micro}")
    
    if version.major < 3 or (version.major == 3 and version.minor < 8):
        print("❌ Python 3.8 or higher is required!")
        return False
    
    print("✅ Python version is compatible!")
    return True

def create_virtual_environment():
    """Create virtual environment"""
    print_header("Creating Virtual Environment")
    
    if os.path.exists('venv'):
        print("⚠️  Virtual environment already exists. Skipping...")
        return True
    
    return run_command(
        f"{sys.executable} -m venv venv",
        "Creating virtual environment"
    )

def install_dependencies():
    """Install required packages"""
    print_header("Installing Dependencies")
    
    # Determine pip path based on OS
    if sys.platform == "win32":
        pip_path = "venv\\Scripts\\pip"
    else:
        pip_path = "venv/bin/pip"
    
    return run_command(
        f"{pip_path} install -r requirements.txt",
        "Installing Python packages"
    )

def setup_environment():
    """Setup environment variables"""
    print_header("Setting Up Environment")
    
    if os.path.exists('.env'):
        print("⚠️  .env file already exists. Skipping...")
        return True
    
    try:
        shutil.copy('.env.example', '.env')
        print("✅ Created .env file from template")
        print("⚠️  Please update .env with your settings!")
        return True
    except Exception as e:
        print(f"❌ Failed to create .env file: {e}")
        return False

def create_directories():
    """Create necessary directories"""
    print_header("Creating Directories")
    
    directories = [
        'data/raw',
        'data/processed',
        'data/uploads',
        'models',
        'logs'
    ]
    
    for directory in directories:
        os.makedirs(directory, exist_ok=True)
        print(f"✅ Created directory: {directory}")
    
    return True

def initialize_database():
    """Initialize database"""
    print_header("Initializing Database")
    
    if os.path.exists('streetfood.db'):
        response = input("⚠️  Database already exists. Reinitialize? (y/N): ")
        if response.lower() != 'y':
            print("Skipping database initialization...")
            return True
        os.remove('streetfood.db')
    
    return run_command(
        f"{sys.executable} src/database.py --init",
        "Initializing database"
    )

def seed_database():
    """Seed database with initial data"""
    print_header("Seeding Database")
    
    return run_command(
        f"{sys.executable} database/seed_data.py",
        "Seeding database with initial data"
    )

def print_next_steps():
    """Print next steps for user"""
    print_header("Setup Complete! 🎉")
    
    print("Next steps:")
    print("\n1. Activate virtual environment:")
    if sys.platform == "win32":
        print("   venv\\Scripts\\activate")
    else:
        print("   source venv/bin/activate")
    
    print("\n2. Update .env file with your settings")
    
    print("\n3. (Optional) Add training images to data/raw/")
    
    print("\n4. Run the application:")
    print("   streamlit run app/streamlit_app.py")
    
    print("\n5. Open browser and navigate to:")
    print("   http://localhost:8501")
    
    print("\n6. Login with default admin credentials:")
    print("   Email: admin@streetfood.ai")
    print("   Password: admin123")
    print("   ⚠️  Change these credentials immediately!")
    
    print("\n📚 Documentation:")
    print("   - SETUP.md - Detailed setup guide")
    print("   - FEATURES.md - Feature documentation")
    print("   - API_DOCUMENTATION.md - API reference")
    print("   - DEPLOYMENT.md - Deployment guide")
    
    print("\n💡 Tips:")
    print("   - Check logs/ directory for application logs")
    print("   - Use 'streamlit run app/streamlit_app.py --server.port 8502' for different port")
    print("   - Read CONTRIBUTING.md if you want to contribute")
    
    print("\n🐛 Issues?")
    print("   - Check troubleshooting section in SETUP.md")
    print("   - Open an issue on GitHub")
    
    print("\n" + "=" * 60 + "\n")

def main():
    """Main setup function"""
    print_header("Indian Street Food AI - Quick Start")
    print("This script will set up your development environment")
    
    # Check Python version
    if not check_python_version():
        sys.exit(1)
    
    # Create virtual environment
    if not create_virtual_environment():
        print("\n❌ Setup failed at virtual environment creation")
        sys.exit(1)
    
    # Install dependencies
    if not install_dependencies():
        print("\n❌ Setup failed at dependency installation")
        sys.exit(1)
    
    # Setup environment
    if not setup_environment():
        print("\n❌ Setup failed at environment configuration")
        sys.exit(1)
    
    # Create directories
    if not create_directories():
        print("\n❌ Setup failed at directory creation")
        sys.exit(1)
    
    # Initialize database
    if not initialize_database():
        print("\n❌ Setup failed at database initialization")
        sys.exit(1)
    
    # Seed database
    if not seed_database():
        print("\n⚠️  Database seeding failed, but you can continue")
    
    # Print next steps
    print_next_steps()

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n⚠️  Setup interrupted by user")
        sys.exit(1)
    except Exception as e:
        print(f"\n\n❌ Unexpected error: {e}")
        sys.exit(1)
