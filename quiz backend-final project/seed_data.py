"""
seed_data.py
------------
Populates the database with 50+ sample quiz questions across 6 categories.

Usage:
    python seed_data.py

Categories:
    - General Knowledge  (10 questions)
    - Programming        (10 questions)
    - Mathematics        (10 questions)
    - Data Science       (10 questions)
    - Business Studies   (10 questions)
    - Aptitude           (10 questions)

Each question has 4 answer choices (exactly 1 is correct).
Script is idempotent: skips seeding if questions already exist.
"""

import sys
import os

# Allow running from the project root
sys.path.insert(0, os.path.dirname(__file__))

from app.database import SessionLocal, engine, Base
from app import models

# ──────────────────────────────────────────────
# Sample data
# ──────────────────────────────────────────────

QUIZ_DATA = [

    # ── General Knowledge ──────────────────────
    {
        "question_text": "What is the capital of France?",
        "category": "General Knowledge",
        "choices": [
            ("Paris", True),
            ("London", False),
            ("Berlin", False),
            ("Madrid", False),
        ],
    },
    {
        "question_text": "Which planet is known as the Red Planet?",
        "category": "General Knowledge",
        "choices": [
            ("Mars", True),
            ("Venus", False),
            ("Jupiter", False),
            ("Saturn", False),
        ],
    },
    {
        "question_text": "How many continents are there on Earth?",
        "category": "General Knowledge",
        "choices": [
            ("7", True),
            ("5", False),
            ("6", False),
            ("8", False),
        ],
    },
    {
        "question_text": "Which is the largest ocean on Earth?",
        "category": "General Knowledge",
        "choices": [
            ("Pacific Ocean", True),
            ("Atlantic Ocean", False),
            ("Indian Ocean", False),
            ("Arctic Ocean", False),
        ],
    },
    {
        "question_text": "Who wrote 'Romeo and Juliet'?",
        "category": "General Knowledge",
        "choices": [
            ("William Shakespeare", True),
            ("Charles Dickens", False),
            ("Leo Tolstoy", False),
            ("Mark Twain", False),
        ],
    },
    {
        "question_text": "What is the chemical symbol for Gold?",
        "category": "General Knowledge",
        "choices": [
            ("Au", True),
            ("Ag", False),
            ("Go", False),
            ("Gd", False),
        ],
    },
    {
        "question_text": "Which country is the largest by area?",
        "category": "General Knowledge",
        "choices": [
            ("Russia", True),
            ("Canada", False),
            ("China", False),
            ("United States", False),
        ],
    },
    {
        "question_text": "How many bones are there in the adult human body?",
        "category": "General Knowledge",
        "choices": [
            ("206", True),
            ("186", False),
            ("256", False),
            ("300", False),
        ],
    },
    {
        "question_text": "Which element has the atomic number 1?",
        "category": "General Knowledge",
        "choices": [
            ("Hydrogen", True),
            ("Helium", False),
            ("Oxygen", False),
            ("Carbon", False),
        ],
    },
    {
        "question_text": "In which year did World War II end?",
        "category": "General Knowledge",
        "choices": [
            ("1945", True),
            ("1939", False),
            ("1950", False),
            ("1941", False),
        ],
    },

    # ── Programming ────────────────────────────
    {
        "question_text": "What does HTML stand for?",
        "category": "Programming",
        "choices": [
            ("HyperText Markup Language", True),
            ("HyperText Modeling Language", False),
            ("HighText Machine Language", False),
            ("Hyperlink and Text Markup Language", False),
        ],
    },
    {
        "question_text": "Which keyword is used to define a function in Python?",
        "category": "Programming",
        "choices": [
            ("def", True),
            ("func", False),
            ("function", False),
            ("define", False),
        ],
    },
    {
        "question_text": "What is the time complexity of binary search?",
        "category": "Programming",
        "choices": [
            ("O(log n)", True),
            ("O(n)", False),
            ("O(n^2)", False),
            ("O(1)", False),
        ],
    },
    {
        "question_text": "Which data structure uses LIFO order?",
        "category": "Programming",
        "choices": [
            ("Stack", True),
            ("Queue", False),
            ("Array", False),
            ("Linked List", False),
        ],
    },
    {
        "question_text": "What does SQL stand for?",
        "category": "Programming",
        "choices": [
            ("Structured Query Language", True),
            ("Simple Query Language", False),
            ("Standard Query Logic", False),
            ("Sequential Query Language", False),
        ],
    },
    {
        "question_text": "Which HTTP method is used to update a resource?",
        "category": "Programming",
        "choices": [
            ("PUT", True),
            ("GET", False),
            ("POST", False),
            ("DELETE", False),
        ],
    },
    {
        "question_text": "What is a primary key in a relational database?",
        "category": "Programming",
        "choices": [
            ("A unique identifier for each record in a table", True),
            ("The first column of any table", False),
            ("A key used to encrypt data", False),
            ("A foreign key reference to another table", False),
        ],
    },
    {
        "question_text": "Which of the following is NOT an OOP principle?",
        "category": "Programming",
        "choices": [
            ("Compilation", True),
            ("Encapsulation", False),
            ("Inheritance", False),
            ("Polymorphism", False),
        ],
    },
    {
        "question_text": "What is the output of `print(type([]))` in Python?",
        "category": "Programming",
        "choices": [
            ("<class 'list'>", True),
            ("<class 'array'>", False),
            ("<class 'tuple'>", False),
            ("<class 'dict'>", False),
        ],
    },
    {
        "question_text": "Which protocol is used for secure communication over the web?",
        "category": "Programming",
        "choices": [
            ("HTTPS", True),
            ("HTTP", False),
            ("FTP", False),
            ("SMTP", False),
        ],
    },

    # ── Mathematics ────────────────────────────
    {
        "question_text": "What is the value of π (pi) rounded to 2 decimal places?",
        "category": "Mathematics",
        "choices": [
            ("3.14", True),
            ("3.41", False),
            ("3.12", False),
            ("3.16", False),
        ],
    },
    {
        "question_text": "What is the square root of 144?",
        "category": "Mathematics",
        "choices": [
            ("12", True),
            ("14", False),
            ("11", False),
            ("13", False),
        ],
    },
    {
        "question_text": "How many degrees are in a right angle?",
        "category": "Mathematics",
        "choices": [
            ("90", True),
            ("45", False),
            ("180", False),
            ("360", False),
        ],
    },
    {
        "question_text": "What is the next prime number after 7?",
        "category": "Mathematics",
        "choices": [
            ("11", True),
            ("8", False),
            ("9", False),
            ("10", False),
        ],
    },
    {
        "question_text": "What is the formula for the area of a circle?",
        "category": "Mathematics",
        "choices": [
            ("π r²", True),
            ("2 π r", False),
            ("π d", False),
            ("r²", False),
        ],
    },
    {
        "question_text": "What is 15% of 200?",
        "category": "Mathematics",
        "choices": [
            ("30", True),
            ("20", False),
            ("25", False),
            ("35", False),
        ],
    },
    {
        "question_text": "What is the sum of angles in a triangle?",
        "category": "Mathematics",
        "choices": [
            ("180 degrees", True),
            ("90 degrees", False),
            ("360 degrees", False),
            ("270 degrees", False),
        ],
    },
    {
        "question_text": "If f(x) = 2x + 3, what is f(4)?",
        "category": "Mathematics",
        "choices": [
            ("11", True),
            ("8", False),
            ("10", False),
            ("14", False),
        ],
    },
    {
        "question_text": "What is the value of 2^10?",
        "category": "Mathematics",
        "choices": [
            ("1024", True),
            ("512", False),
            ("2048", False),
            ("100", False),
        ],
    },
    {
        "question_text": "What is the Fibonacci sequence?",
        "category": "Mathematics",
        "choices": [
            ("Each number is the sum of the two preceding ones", True),
            ("Each number is double the previous one", False),
            ("Each number is the square of its position", False),
            ("Each number is the product of the two preceding ones", False),
        ],
    },

    # ── Data Science ───────────────────────────
    {
        "question_text": "What does EDA stand for in Data Science?",
        "category": "Data Science",
        "choices": [
            ("Exploratory Data Analysis", True),
            ("Experimental Data Application", False),
            ("Extracted Data Algorithm", False),
            ("Enhanced Data Analytics", False),
        ],
    },
    {
        "question_text": "Which Python library is primarily used for data manipulation?",
        "category": "Data Science",
        "choices": [
            ("Pandas", True),
            ("NumPy", False),
            ("Matplotlib", False),
            ("Scikit-learn", False),
        ],
    },
    {
        "question_text": "What is overfitting in machine learning?",
        "category": "Data Science",
        "choices": [
            ("When a model learns noise in training data and performs poorly on new data", True),
            ("When a model is too simple to capture patterns", False),
            ("When training accuracy is lower than test accuracy", False),
            ("When the dataset has too many features", False),
        ],
    },
    {
        "question_text": "Which algorithm is used for classification and regression using decision boundaries?",
        "category": "Data Science",
        "choices": [
            ("Support Vector Machine (SVM)", True),
            ("K-Means Clustering", False),
            ("Apriori Algorithm", False),
            ("Principal Component Analysis", False),
        ],
    },
    {
        "question_text": "What does 'null hypothesis' mean in statistics?",
        "category": "Data Science",
        "choices": [
            ("A statement assuming no effect or relationship exists", True),
            ("A hypothesis that is always rejected", False),
            ("A hypothesis with no data", False),
            ("The final accepted conclusion", False),
        ],
    },
    {
        "question_text": "What is the purpose of the train-test split in machine learning?",
        "category": "Data Science",
        "choices": [
            ("To evaluate model performance on unseen data", True),
            ("To increase training data size", False),
            ("To remove outliers from the dataset", False),
            ("To balance class labels", False),
        ],
    },
    {
        "question_text": "Which metric is best for imbalanced classification datasets?",
        "category": "Data Science",
        "choices": [
            ("F1 Score", True),
            ("Accuracy", False),
            ("Mean Squared Error", False),
            ("R-squared", False),
        ],
    },
    {
        "question_text": "What is a confusion matrix used for?",
        "category": "Data Science",
        "choices": [
            ("Evaluating the performance of a classification model", True),
            ("Visualizing data distributions", False),
            ("Selecting features for a model", False),
            ("Normalizing data values", False),
        ],
    },
    {
        "question_text": "Which technique reduces the number of features in a dataset?",
        "category": "Data Science",
        "choices": [
            ("Principal Component Analysis (PCA)", True),
            ("Random Forest", False),
            ("Gradient Boosting", False),
            ("Cross-validation", False),
        ],
    },
    {
        "question_text": "What does 'K' represent in K-Means Clustering?",
        "category": "Data Science",
        "choices": [
            ("The number of clusters", True),
            ("The number of data points", False),
            ("The number of features", False),
            ("The number of iterations", False),
        ],
    },

    # ── Business Studies ───────────────────────
    {
        "question_text": "What does GDP stand for?",
        "category": "Business Studies",
        "choices": [
            ("Gross Domestic Product", True),
            ("General Domestic Production", False),
            ("Gross Demand Price", False),
            ("General Development Plan", False),
        ],
    },
    {
        "question_text": "What is the primary goal of marketing?",
        "category": "Business Studies",
        "choices": [
            ("To identify and satisfy customer needs profitably", True),
            ("To maximize production output", False),
            ("To reduce company expenses", False),
            ("To hire skilled employees", False),
        ],
    },
    {
        "question_text": "What does SWOT stand for in business analysis?",
        "category": "Business Studies",
        "choices": [
            ("Strengths, Weaknesses, Opportunities, Threats", True),
            ("Sales, Workforce, Operations, Trends", False),
            ("Strategy, Work, Output, Target", False),
            ("Supply, Workforce, Opportunity, Time", False),
        ],
    },
    {
        "question_text": "What is the breakeven point for a business?",
        "category": "Business Studies",
        "choices": [
            ("The point at which total revenue equals total costs", True),
            ("The point of maximum profit", False),
            ("The point of zero revenue", False),
            ("When fixed costs equal variable costs", False),
        ],
    },
    {
        "question_text": "Which financial statement shows a company's assets, liabilities, and equity?",
        "category": "Business Studies",
        "choices": [
            ("Balance Sheet", True),
            ("Income Statement", False),
            ("Cash Flow Statement", False),
            ("Statement of Retained Earnings", False),
        ],
    },
    {
        "question_text": "What is inflation?",
        "category": "Business Studies",
        "choices": [
            ("A general rise in the price level of goods and services over time", True),
            ("A decrease in interest rates", False),
            ("An increase in a company's stock price", False),
            ("A reduction in government spending", False),
        ],
    },
    {
        "question_text": "What is the role of a central bank?",
        "category": "Business Studies",
        "choices": [
            ("To manage monetary policy and regulate the banking system", True),
            ("To provide loans to individual customers", False),
            ("To collect income taxes", False),
            ("To manage stock market operations", False),
        ],
    },
    {
        "question_text": "Which pricing strategy sets prices lower than competitors to gain market share?",
        "category": "Business Studies",
        "choices": [
            ("Penetration Pricing", True),
            ("Skimming Pricing", False),
            ("Premium Pricing", False),
            ("Bundle Pricing", False),
        ],
    },
    {
        "question_text": "What does ROI stand for?",
        "category": "Business Studies",
        "choices": [
            ("Return on Investment", True),
            ("Rate of Income", False),
            ("Revenue over Interest", False),
            ("Return on Infrastructure", False),
        ],
    },
    {
        "question_text": "In economics, what is the law of supply?",
        "category": "Business Studies",
        "choices": [
            ("As price increases, quantity supplied increases, all else equal", True),
            ("As price increases, quantity demanded increases", False),
            ("Supply always equals demand", False),
            ("Higher wages lead to lower supply", False),
        ],
    },

    # ── Aptitude ───────────────────────────────
    {
        "question_text": "If a train travels 300 km in 3 hours, what is its average speed?",
        "category": "Aptitude",
        "choices": [
            ("100 km/h", True),
            ("90 km/h", False),
            ("150 km/h", False),
            ("120 km/h", False),
        ],
    },
    {
        "question_text": "A is twice as old as B. If B is 15, how old is A?",
        "category": "Aptitude",
        "choices": [
            ("30", True),
            ("25", False),
            ("20", False),
            ("35", False),
        ],
    },
    {
        "question_text": "What comes next in the series: 2, 4, 8, 16, ___?",
        "category": "Aptitude",
        "choices": [
            ("32", True),
            ("20", False),
            ("24", False),
            ("18", False),
        ],
    },
    {
        "question_text": "If 5 workers complete a job in 10 days, how many days will 10 workers take?",
        "category": "Aptitude",
        "choices": [
            ("5", True),
            ("8", False),
            ("20", False),
            ("2", False),
        ],
    },
    {
        "question_text": "A shopkeeper sells an item for Rs. 150 that cost Rs. 100. What is the profit percentage?",
        "category": "Aptitude",
        "choices": [
            ("50%", True),
            ("25%", False),
            ("33%", False),
            ("40%", False),
        ],
    },
    {
        "question_text": "Which number is missing: 3, 6, 9, ___, 15?",
        "category": "Aptitude",
        "choices": [
            ("12", True),
            ("10", False),
            ("11", False),
            ("13", False),
        ],
    },
    {
        "question_text": "If the ratio of boys to girls in a class is 3:2 and there are 30 students, how many are boys?",
        "category": "Aptitude",
        "choices": [
            ("18", True),
            ("12", False),
            ("15", False),
            ("20", False),
        ],
    },
    {
        "question_text": "What is the simple interest on Rs. 1000 at 5% per annum for 2 years?",
        "category": "Aptitude",
        "choices": [
            ("Rs. 100", True),
            ("Rs. 50", False),
            ("Rs. 200", False),
            ("Rs. 150", False),
        ],
    },
    {
        "question_text": "A clock shows 3:00. What is the angle between the hour and minute hands?",
        "category": "Aptitude",
        "choices": [
            ("90 degrees", True),
            ("45 degrees", False),
            ("180 degrees", False),
            ("120 degrees", False),
        ],
    },
    {
        "question_text": "If APPLE is coded as BQQMF, what is the code for CAT?",
        "category": "Aptitude",
        "choices": [
            ("DBU", True),
            ("CBT", False),
            ("DAT", False),
            ("EBU", False),
        ],
    },
]


# ──────────────────────────────────────────────
# Seeding logic
# ──────────────────────────────────────────────

def seed():
    """Seed the database with sample quiz data."""
    # Ensure tables exist
    Base.metadata.create_all(bind=engine)

    db = SessionLocal()
    try:
        existing = db.query(models.Question).count()
        if existing > 0:
            print(f"[OK] Database already has {existing} questions. Skipping seed.")
            return

        print("[SEED] Seeding database with quiz data...")
        total_questions = 0
        total_choices = 0

        for item in QUIZ_DATA:
            # Create question
            question = models.Question(
                question_text=item["question_text"],
                category=item["category"],
            )
            db.add(question)
            db.flush()  # Get the question ID before adding choices

            # Create choices
            for choice_text, is_correct in item["choices"]:
                choice = models.Choice(
                    choice_text=choice_text,
                    is_correct=is_correct,
                    question_id=question.id,
                )
                db.add(choice)
                total_choices += 1

            total_questions += 1

        db.commit()
        print(f"[OK] Successfully seeded {total_questions} questions and {total_choices} choices.")
        print()
        print("Categories:")
        categories = db.query(models.Question.category).distinct().all()
        for (cat,) in categories:
            count = db.query(models.Question).filter(models.Question.category == cat).count()
            print(f"   {cat:25s} -> {count} questions")

    except Exception as e:
        db.rollback()
        print(f"[ERROR] Error seeding data: {e}")
        raise
    finally:
        db.close()


if __name__ == "__main__":
    seed()
