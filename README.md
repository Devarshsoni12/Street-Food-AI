# 🍛 Street Food AI — Indian Food Classifier

A deep learning-powered web application that identifies Indian street food from images, provides detailed nutritional information, tracks daily intake, and offers personalized health insights.

---

## 🚀 Features

- 📸 **Food Recognition** — Upload a food image and get instant AI-powered identification
- 🧠 **Deep Learning Model** — MobileNetV2 / EfficientNetB0 trained on 17 Indian street food categories
- 🥗 **Nutrition Tracking** — Calories, protein, carbs, fats, fiber, sodium per serving
- 📊 **Dashboard** — Visual charts of daily/weekly nutrition intake using Plotly
- 👤 **User Profiles** — BMI calculator, health goals, dietary preferences (vegan, jain, etc.)
- 🔐 **Authentication** — Secure login & registration with bcrypt password hashing
- ⚙️ **Admin Panel** — Manage users, view predictions, monitor app usage
- 🏆 **Achievements** — Gamified badges for healthy eating streaks and milestones
- 🗄️ **Dual Database** — Supports both SQLite (local) and PostgreSQL (production)

---

## 🍽️ Supported Food Classes

| # | Food | Region |
|---|------|--------|
| 1 | Aloo Paratha | Punjab |
| 2 | Burger | Pan India |
| 3 | Chole Bhature | Delhi |
| 4 | Dhokla | Gujarat |
| 5 | Dosa | South India |
| 6 | Grilled Sandwich | Mumbai |
| 7 | Idli | South India |
| 8 | Medu Vada | Karnataka |
| 9 | Misal Pav | Maharashtra |
| 10 | Momos | Delhi / Northeast |
| 11 | Pakoda | Pan India |
| 12 | Pani Puri | Pan India |
| 13 | Pav Bhaji | Mumbai |
| 14 | Poha | Madhya Pradesh |
| 15 | Samosa | North India |
| 16 | Sev Puri | Mumbai |
| 17 | Vada Pav | Mumbai |

---

## 🛠️ Tech Stack

| Layer | Technology |
|-------|-----------|
| Frontend / UI | Streamlit |
| Deep Learning | TensorFlow 2.x, Keras |
| Model Architecture | MobileNetV2, EfficientNetB0 |
| Image Processing | OpenCV, Pillow |
| Data Processing | NumPy, Pandas |
| Visualization | Plotly, Matplotlib |
| Database | SQLite (dev) / PostgreSQL (prod) |
| Authentication | bcrypt |
| Environment Config | python-dotenv |


---

## 📁 Project Structure

```
Street-Food-AI/
├── app/
│   ├── streamlit_app.py        # Main Streamlit entry point
│   ├── auth.py                 # Authentication helpers
│   ├── utils.py                # Shared utilities
│   └── pages/
│       ├── home.py             # Home page
│       ├── prediction.py       # Food scan & prediction page
│       ├── dashboard.py        # Nutrition dashboard
│       ├── profile.py          # User profile & BMI
│       └── admin.py            # Admin panel
├── src/
│   ├── model.py                # FoodClassifier & MealTypeClassifier
│   ├── prediction.py           # Inference pipeline
│   ├── nutrition.py            # Nutrition analysis & calorie recommendations
│   ├── preprocessing.py        # Image preprocessing
│   └── database.py             # Database layer (SQLite / PostgreSQL)
├── models/
│   ├── food_classifier.h5      # Trained model weights (not in repo)
│   └── class_indices.json      # Class label mappings
├── database/
│   ├── schema.sql              # PostgreSQL schema
│   ├── schema_sqlite.sql       # SQLite schema
│   └── seed_data.py            # Seed script
├── notebooks/
│   ├── train_model.py          # Model training script
│   └── TRAINING_GUIDE.md       # Training instructions
├── data/
│   └── raw/                    # Training images (not in repo)
├── .env.example                # Environment variable template
├── requirements.txt            # Python dependencies
└── train_model.py              # Root-level training entry point
```

---

## ⚙️ Setup & Installation

### 1. Clone the repository

```bash
git clone https://github.com/Devarshsoni12/Street-Food-AI.git
cd Street-Food-AI
```

### 2. Create a virtual environment

```bash
python -m venv venv
source venv/bin/activate        # Linux / macOS
venv\Scripts\activate           # Windows
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure environment variables

```bash
cp .env.example .env
# Edit .env with your settings
```

Key variables in `.env`:

```env
DATABASE_URL=sqlite:///./streetfood.db
SECRET_KEY=your-secret-key-here
MODEL_PATH=models/food_classifier.h5
CONFIDENCE_THRESHOLD=0.70
ADMIN_EMAIL=admin@streetfood.ai
ADMIN_PASSWORD=admin123
```

### 5. Initialize the database

```bash
python src/database.py --init
```

### 6. Run the app

```bash
streamlit run app/streamlit_app.py
```

---

## 🧠 Model Training

If you want to train the model from scratch:

```bash
# Place your dataset in data/raw/<ClassName>/ folders
python train_model.py
```

The training script uses **MobileNetV2** with transfer learning (ImageNet weights), fine-tuned on 17 Indian food categories. See `notebooks/TRAINING_GUIDE.md` for full details.

---

## 🗄️ Database

The app supports two backends controlled by `DATABASE_URL` in `.env`:

- **SQLite** (default for local dev): `sqlite:///./streetfood.db`
- **PostgreSQL** (for production): `postgresql://user:password@host/dbname`

Schema files are in `database/schema_sqlite.sql` and `database/schema.sql`.

---

## 🌐 Deployment

### Streamlit Community Cloud (Free)

1. Push your code to GitHub
2. Go to [share.streamlit.io](https://share.streamlit.io) and sign in
3. Click **New app** → select your repo
4. Set **Main file path** to `app/streamlit_app.py`
5. Add your `.env` variables under **Advanced settings → Secrets**
6. Click **Deploy**

> Note: Upload your trained model (`food_classifier.h5`) separately or use a cloud storage URL since large files cannot be committed to GitHub.

---

## 📊 Nutrition Data

Each food item includes:
- Calories, Protein, Carbohydrates, Fats, Fiber, Sugar, Sodium
- Serving size (grams)
- Allergen information
- Dietary flags: Vegetarian, Vegan, Jain-friendly
- Spice level (1–5)
- Regional origin

Calorie recommendations use the **Mifflin-St Jeor equation** adjusted for activity level and health goal (weight loss / maintenance / weight gain).

---

## 🔐 Security

- Passwords hashed with **bcrypt**
- Environment secrets managed via **python-dotenv**
- `.env` file excluded from version control via `.gitignore`
- Admin routes protected by role-based access check

---

## 📦 Requirements

```
streamlit>=1.28.0
tensorflow>=2.13.0
numpy>=1.24.0
pandas>=2.0.0
Pillow>=10.0.0
opencv-python>=4.8.0
plotly>=5.17.0
matplotlib>=3.7.0
bcrypt>=4.0.0
python-dotenv>=1.0.0
psycopg2-binary>=2.9.0
```

---

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch: `git checkout -b feature/your-feature`
3. Commit your changes: `git commit -m "Add your feature"`
4. Push to the branch: `git push origin feature/your-feature`
5. Open a Pull Request

---

## 📄 License

This project is licensed under the terms of the [LICENSE](LICENSE) file.

---

> Built with ❤️ using Streamlit and TensorFlow
