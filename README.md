# Web Automation System

Comprehensive web automation system built with Python, Selenium, and MySQL for automated data extraction, form filling, and interaction testing.

## 🚀 Features

### Implemented Modules:

1. **Form Automation**
   - Complete form filling with file upload
   - Modal validation
   - Data verification

2. **Web Table Scraping**
   - Selective data extraction
   - MySQL persistence with duplicate prevention
   - Parameterized SQL queries

3. **Advanced Interactions**
   - Double click, right click, dynamic click
   - Action validation
   - Screenshot on errors

4. **Drag & Drop**
   - Element manipulation
   - State validation

## 🛠️ Tech Stack

- **Python 3.9+**
- **Selenium 4+** - Browser automation
- **PyMySQL** - MySQL database connector
- **webdriver-manager** - Automatic driver management
- **python-dotenv** - Environment configuration

## 📋 Prerequisites

- Python 3.9 or higher
- MySQL Server 8.0+
- Firefox browser (or modify for Chrome)
- Git

## 🔧 Installation

### 1. Clone repository
```bash
git clone https://github.com/picrack/RPA_Test.git
cd RPA_Test
```

### 2. Create virtual environment
```bash
python -m venv env

# Windows
env\Scripts\activate

# macOS/Linux
source env/bin/activate
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

### 4. Database setup

Create database:
```sql
CREATE DATABASE automation_data;
```

Create tables:
```bash
mysql -u root -p automation_data < scripts/schema.sql
```

### 5. Environment configuration

Copy `.env.example` to `.env` and update with your credentials:
```bash
cp .env.example .env
```

Edit `.env`:
```
DB_HOST=localhost
DB_PORT=3306
DB_USER=root
DB_PASSWORD=your_password
DB_NAME=automation_data
```

### 6. Verify installation
```bash
python check.py
```

## 🎯 Usage

### Run all tasks:
```bash
python main.py --task all
```

### Run individual tasks:
```bash
# Form automation
python main.py --task form

# Web table scraping
python main.py --task webtables

# Button interactions
python main.py --task buttons

# Drag & Drop
python main.py --task droppable

# Headless mode
python main.py --task all --headless
```

## 📁 Project Structure
```
RPA_Test/
├── app/
│   └── db.py                    # Database connection and queries
├── functions/
│   ├── form_task.py             # Form automation
│   ├── webtables_task.py        # Web scraping and persistence
│   ├── buttons_task.py          # Click interactions
│   └── droppable_task.py        # Drag & Drop
├── scripts/
│   ├── schema.sql               # Database schema
│   └── seed.sql                 # Sample data (optional)
├── utils/
│   ├── utils.py                 # Helper functions
│   └── selectors.py             # Centralized selectors
├── check.py                     # Environment validation
├── main.py                      # Main orchestrator
├── requirements.txt             # Dependencies
├── README.md                    # This file
└── .env.example                 # Configuration template
```

## 🌟 Key Features

### Architecture
- **Modular design:** Each task is independent
- **Separation of concerns:** Business logic, data layer, and utilities are separate
- **Centralized selectors:** Easy maintenance when web structure changes
- **Explicit waits:** Reliable element detection
- **Error handling:** Comprehensive logging with automatic screenshots

### Database
- **Parameterized queries:** SQL injection prevention
- **Duplicate prevention:** `ON DUPLICATE KEY UPDATE` strategy
- **Transaction control:** Data integrity guaranteed

### Code Quality
- **PEP8 compliant**
- **Modular functions**
- **Comprehensive logging**
- **Environment-based configuration**
- **Full documentation**

## 🔍 Technical Highlights

### Web Scraping
- Selective row extraction (rows 1 and 3)
- CSS selectors for precise targeting
- Empty row handling

### Database Integration
- Direct SQL without ORM
- Efficient duplicate handling
- Connection pooling ready

### Browser Automation
- Explicit waits (WebDriverWait)
- ActionChains for complex interactions
- JavaScript execution for edge cases
- Screenshot capture on errors

## 📝 Future Enhancements

- [ ] Page Object Model implementation
- [ ] Unit tests with pytest
- [ ] Retry logic for robustness
- [ ] Docker containerization
- [ ] CI/CD with GitHub Actions
- [ ] Chrome/Edge support
- [ ] Reporting dashboard

## 🐛 Troubleshooting

### Connection errors
Ensure MySQL is running:
```bash
# Windows
net start MySQL80

# macOS
brew services start mysql

# Linux
sudo service mysql start
```

### Driver issues
The project uses webdriver-manager which downloads drivers automatically. 
If issues persist, update:
```bash
pip install --upgrade webdriver-manager
```

## 📄 License

MIT License - feel free to use this project for learning and development.

## 👤 Author

**Bastián González**
- LinkedIn: [linkedin.com/in/bastiángonzálezpicart](https://linkedin.com/in/bastiángonzálezpicart)
- GitHub: [@picrack](https://github.com/picrack)

## 🙏 Acknowledgments

Built with best practices in web automation, database integration, and software architecture.

---

⭐ If you find this project useful, please consider giving it a star on GitHub!