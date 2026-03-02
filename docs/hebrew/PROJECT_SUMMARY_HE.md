📄 סיכום פרויקט – גרסת Kaggle Hybrid (תקציר בעברית)
🎯 מטרת המערכת

מערכת AI מקצה־לקצה שמקבלת קריאת שירות IT ומבצעת:

סיווג קטגוריה (8 קטגוריות אמיתיות)

קביעת דחיפות (כרגע placeholder)

שליפת Runbook רלוונטי (RAG)

יצירת תשובה מובנית

📊 Dataset

מקור: Kaggle IT Support

47,837 טיקטים אמיתיים

חלוקה 80/10/10 (Train/Val/Test)

הרחבת Train בלבד עם EDA

שיפור איזון מחלקות

🤖 מודל

TF-IDF (20K features)

Logistic Regression

class_weight="balanced"

📈 ביצועים (Test אמיתי)

Accuracy: 0.86

Macro F1: 0.86

אין Overfitting

שדה urgency כרגע מוחזר כ-"Medium" וניתן להרחבה בעתיד.

📚 RAG

מסמכי Runbooks ב-Markdown

אחסון ב-Chroma

שליפה Top-K

יצירת תשובה מבוססת תבנית

ללא LLM חיצוני

🧪 בדיקות

19 טסטים עוברים

Docker תקין

Endpoints נבדקו

המערכת עובדת מקצה לקצה

⚙️ מה זה מדגים

✔ ML יישומי אמיתי
✔ עבודה עם דאטה אמיתי
✔ איזון מחלקות ללא leakage
✔ ארכיטקטורת Backend מודולרית
✔ שילוב ML + RAG
✔ Containerization מלא

⚠️ מגבלות

אין מודל דחיפות אמיתי

אין LLM חיצוני

מיועד לדמו ולא לפרודקשן

🚀 מצב נוכחי

✔ עובד מקצה לקצה
✔ ניתן להרצה בפקודה אחת
✔ מוכן להצגה