# Price Tracker 


# PricePulse - Smart Price Tracking Application 🏷️

A comprehensive full-stack web application that monitors product prices across multiple e-commerce platforms, sends automated alerts on price drops, and provides detailed price analytics through an intuitive dashboard.





## ✨ Features

- 🕷️ **Real-time Web Scraping** - Automated price extraction from Amazon, eBay, and other platforms
- 📧 **Smart Alerts** - Email notifications when prices drop below target thresholds
- 📊 **Price Analytics** - Interactive charts showing price history and trends
- 🔄 **Background Monitoring** - Scheduled price checks using APScheduler
- 👤 **User Management** - Secure user authentication and product management
- 📱 **Responsive Design** - Modern React frontend with Tailwind CSS
- 🛡️ **Anti-Bot Protection** - Advanced scraping techniques to avoid detection

## 🛠️ Tech Stack

### Backend
- **Framework**: FastAPI (Python)
- **Web Scraping**: Scrapy with custom middlewares
- **Database**: PostgreSQL with SQLAlchemy ORM
- **Email Service**: SendGrid / SMTP
- **Scheduling**: APScheduler for background tasks
- **Authentication**: JWT tokens

### Frontend
- **Framework**: React.js 18+
- **Styling**: Tailwind CSS 3.x
- **HTTP Client**: Axios
- **Notifications**: React Toastify
- **State Management**: React Hooks

### Infrastructure
- **Server**: Uvicorn ASGI server
- **Database**: PostgreSQL 15+
- **Environment**: Python 3.10+, Node.js 18+

## 📁 Project Structure

```
price-tracker/
├── backend/
│   ├── app/
│   │   ├── main.py                 # FastAPI application entry point
│   │   ├── config.py               # Configuration settings
│   │   ├── routes/
│   │   │   └── tracker.py          # API endpoints for products/users
│   │   ├── models/
│   │   │   └── product.py          # SQLAlchemy database models
│   │   ├── schemas/
│   │   │   └── product.py          # Pydantic request/response schemas
│   │   ├── services/
│   │   │   ├── scraper_runner.py   # Scrapy integration service
│   │   │   ├── email_alert.py      # Email notification service
│   │   │   └── scheduler.py        # Background task scheduler
│   │   └── db/
│   │       └── database.py         # Database connection setup
│   ├── scrapy_spiders/
│   │   ├── __init__.py
│   │   ├── product_spider.py       # Main scraping spider
│   │   └── settings.py             # Scrapy configuration
│   ├── requirements.txt            # Python dependencies
│   └── .env                        # Environment variables
├── frontend/
│   ├── src/
│   │   ├── components/
│   │   │   ├── UploadForm.jsx      # Product URL input form
│   │   │   └── ProductCard.jsx     # Product display component
│   │   ├── App.jsx                 # Main React application
│   │   ├── main.jsx                # React DOM entry point
│   │   └── index.css               # Tailwind CSS imports
│   ├── public/
│   │   └── index.html
│   ├── package.json                # Node.js dependencies
│   ├── tailwind.config.js          # Tailwind configuration
│   └── postcss.config.js           # PostCSS configuration
├── README.md
├── .gitignore
└── docker-compose.yml              # Docker deployment configuration
```

## 📦 Dependencies

### Backend Dependencies (`requirements.txt`)
```
fastapi==0.104.1
uvicorn[standard]==0.24.0
sqlalchemy==2.0.21
psycopg2-binary==2.9.7
pydantic==2.4.2
scrapy==2.12.0
requests==2.31.0
python-dotenv==1.0.0
apscheduler==3.10.4
sendgrid==6.10.0
python-multipart==0.0.6
alembic==1.12.0
bcrypt==4.0.1
python-jose[cryptography]==3.3.0
```

### Frontend Dependencies (`package.json`)
```
{
  "dependencies": {
    "react": "^18.2.0",
    "react-dom": "^18.2.0",
    "axios": "^1.5.0",
    "react-toastify": "^9.1.3",
    "@headlessui/react": "^1.7.17",
    "@heroicons/react": "^2.0.18"
  },
  "devDependencies": {
    "@types/react": "^18.2.15",
    "@types/react-dom": "^18.2.7",
    "@vitejs/plugin-react": "^4.0.3",
    "tailwindcss": "^3.3.0",
    "postcss": "^8.4.24",
    "autoprefixer": "^10.4.14",
    "vite": "^4.4.5"
  }
}
```

## 🚀 Installation & Setup

### Prerequisites
- Python 3.10 or higher
- Node.js 18+ and npm
- PostgreSQL 15+
- Git

### 1. Clone Repository
```
git clone https://github.com/yourusername/pricepulse.git
cd pricepulse
```

### 2. Backend Setup
```
cd backend

# Create virtual environment
python -m venv venv

# Activate virtual environment
# Windows:
venv\Scripts\activate
# macOS/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Setup environment variables
cp .env.example .env
# Edit .env with your credentials
```

### 3. Database Configuration
```
# Create PostgreSQL database
createdb price_tracker

# Run migrations (if using Alembic)
alembic upgrade head
```

### 4. Frontend Setup
```
cd ../frontend

# Install dependencies
npm install

# Install Tailwind CSS
npm install -D tailwindcss postcss autoprefixer
npx tailwindcss init -p
```

### 5. Environment Variables (`.env`)
```
# Database Configuration
DB_HOST=localhost
DB_NAME=price_tracker
DB_USER=postgres
DB_PASSWORD=your_password
DB_PORT=5432

# Email Configuration (SMTP/SendGrid)
SMTP_SERVER=smtp.gmail.com
SMTP_PORT=587
SMTP_USER=your_email@gmail.com
SMTP_PASSWORD=your_app_password

# SendGrid (Alternative)
SENDGRID_API_KEY=your_sendgrid_api_key

# Application Settings
SECRET_KEY=your_secret_key_here
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
```

## 🏃‍♂️ Running the Application

### Development Mode

**Backend:**
```
cd backend
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

**Frontend:**
```
cd frontend
npm run dev
```

### Production Mode
```
# Backend
uvicorn app.main:app --host 0.0.0.0 --port 8000

# Frontend
npm run build
npm run preview
```

## 🔌 API Endpoints

### Products
| Method | Endpoint | Description |
|--------|----------|-------------|
| `POST` | `/api/v1/products/` | Create new product |
| `GET` | `/api/v1/products/` | List all products |
| `GET` | `/api/v1/products/{id}` | Get product details |
| `PUT` | `/api/v1/products/{id}` | Update product |
| `DELETE` | `/api/v1/products/{id}` | Delete product |
| `GET` | `/api/v1/products/{id}/price-history` | Get price history |
| `POST` | `/api/v1/products/{id}/check-price` | Manual price check |

### Users
| Method | Endpoint | Description |
|--------|----------|-------------|
| `POST` | `/api/v1/users/` | Create user |
| `GET` | `/api/v1/users/` | List users |

### Example API Usage
```
# Add new product
curl -X POST "http://localhost:8000/api/v1/products/" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Example Product",
    "url": "https://www.amazon.in/dp/B09V4MXBSN",
    "target_price": 299.99,
    "platform": "amazon"
  }'

# Get all products
curl -X GET "http://localhost:8000/api/v1/products/"

# Check price manually
curl -X POST "http://localhost:8000/api/v1/products/1/check-price"
```

## 🕷️ Web Scraping Implementation

### Spider Configuration
The application uses Scrapy with custom settings for reliable scraping:

```
# scrapy_spiders/settings.py
USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
DOWNLOAD_DELAY = 3
RANDOMIZE_DOWNLOAD_DELAY = True
ROBOTSTXT_OBEY = False
COOKIES_ENABLED = True
HTTPERROR_ALLOW_ALL = True
```

### Supported Platforms
- **Amazon** (amazon.in, amazon.com)
- **eBay** (ebay.com, ebay.in)
- **Generic** e-commerce sites

### Anti-Detection Features
- Rotating User-Agents
- Random download delays
- Cookie handling
- Proxy support (configurable)

## 📧 Email Alert System

### Configuration
```
# Email via SMTP
SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587

# Email via SendGrid
SENDGRID_API_KEY = "your_api_key"
```

### Alert Triggers
- Price drops below target price
- Price increases above threshold
- Product availability changes
- Daily/weekly price summaries

## 🕒 Background Scheduling

The application uses APScheduler for automated price checking:

```
# Default schedule: Every 6 hours
scheduler.add_job(
    func=check_all_products,
    trigger="interval",
    hours=6,
    id='price_check_job'
)
```


## 🔧 Troubleshooting

### Common Issues

**1. Scrapy Signal Handler Error**
```
# Solution: Use multiprocessing in scraper_runner.py
process = multiprocessing.Process(target=_run_spider, args=(url, queue))
```

**2. PostgreSQL Connection Error**
```
# Check database credentials in .env
# Ensure PostgreSQL service is running
sudo service postgresql start
```

**3. Tailwind CSS Not Working**
```
# Reinstall Tailwind dependencies
npm uninstall tailwindcss
npm install -D tailwindcss@3.4.4 postcss autoprefixer
```

**4. Amazon Blocking Requests**
```
# Update user agent and add delays in scrapy settings
DOWNLOAD_DELAY = 5
RANDOMIZE_DOWNLOAD_DELAY = True
```

## 🤝 Contributing

1. Fork the repository
2. Create feature branch (`git checkout -b feature/amazing-feature`)
3. Commit changes (`git commit -m 'Add amazing feature'`)
4. Push to branch (`git push origin feature/amazing-feature`)
5. Open Pull Request

### Development Guidelines
- Follow PEP 8 for Python code
- Use ESLint for JavaScript code
- Write unit tests for new features
- Update documentation for API changes

## 🙏 Acknowledgments

- FastAPI team for the excellent web framework
- Scrapy developers for robust scraping capabilities
- React and Tailwind CSS communities
- PostgreSQL for reliable data storage

---

**Built with ❤️ by Mohammed Adiyaan R**  
*Powered by FastAPI ⚡ React ⚛️ and Scrapy 🕷️*

For support or questions, please open an issue on GitHub or contact [adiyaan126@gmail.com](mailto:adiyaan126@gmail.com)
```
