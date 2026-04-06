import os
import random
import pandas as pd
import joblib
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier, VotingClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score

MODEL_DIR = os.path.join(os.path.dirname(__file__), 'saved_models')

def generate_mock_dataset(num_samples=1000):
    """
    Generates a synthetic dataset for demonstration purposes.
    In a real scenario, this would load from a CSV of analyzed legitimate and phishing URLs.
    """
    data = []
    
    for _ in range(num_samples):
        # 1 = Phishing, 0 = Legitimate
        is_phishing = random.choice([0, 1])
        if random.random() < 0.1:
           is_phishing = 1 - is_phishing
        
        if is_phishing:
            sample = {
                'url_length': random.randint(20, 120),
                'is_long_url': random.choice([0, 1]),
                'domain_length': random.randint(5, 40),
                'has_ip_in_url': random.choices([0, 1], weights=[0.8, 0.2])[0],
                'is_shortened': random.choices([0, 1], weights=[0.8, 0.2])[0],
                'has_at_symbol': random.choices([0, 1], weights=[0.9, 0.1])[0],
                'has_double_slash_redirect': random.choices([0, 1], weights=[0.8, 0.2])[0],
                'has_dash_in_domain': random.choice([0, 1]),
                'subdomain_count': random.randint(1, 4),
                'https_token_in_domain': random.choices([0, 1], weights=[0.9, 0.1])[0],
                'num_dots': random.randint(1, 6),
                'num_hyphens': random.randint(0, 5),
                'num_underscores': random.randint(0, 3),
                'num_slash': random.randint(3, 8),
                'num_question_marks': random.choices([0, 1, 2], weights=[0.7, 0.2, 0.1])[0],
                'num_equals': random.choices([0, 1, 2], weights=[0.7, 0.2, 0.1])[0],
                
                'has_form': random.choice([0, 1]),
                'has_password_field': random.choices([0, 1], weights=[0.5, 0.5])[0],
                'has_hidden_inputs': random.choices([0, 1], weights=[0.6, 0.4])[0],
                'has_external_action_form': random.choices([0, 1], weights=[0.7, 0.3])[0],
                'num_iframes': random.randint(0, 5),
                'num_script_tags': random.randint(5, 30),
                'ratio_external_links': random.uniform(0.0, 0.9),
                'has_suspicious_title': random.choices([0, 1], weights=[0.6, 0.4])[0],
                'page_size_kb': random.uniform(10.0, 200.0),
                
                
                'label': 1
            }
        else:
            sample = {
                'url_length': random.randint(20, 120),
                'is_long_url': 0,
                'domain_length': random.randint(5, 40),
                'has_ip_in_url': 0,
                'is_shortened': random.choices([0, 1], weights=[0.95, 0.05])[0],
                'has_at_symbol': 0,
                'has_double_slash_redirect': 0,
                'has_dash_in_domain': random.choices([0, 1], weights=[0.8, 0.2])[0],
                'subdomain_count': random.randint(0, 2),
                'https_token_in_domain': 0,
                'num_dots': random.randint(1, 6),
                'num_hyphens': random.randint(0, 5),
                'num_underscores': random.randint(0, 1),
                'num_slash': random.randint(2, 5),
                'num_question_marks': random.choices([0, 1], weights=[0.9, 0.1])[0],
                'num_equals': random.choices([0, 1], weights=[0.9, 0.1])[0],
                
                'has_form': random.choice([0, 1]),
                'has_password_field': random.choices([0, 1], weights=[0.9, 0.1])[0],
                'has_hidden_inputs': random.choices([0, 1], weights=[0.9, 0.1])[0],
                'has_external_action_form': 0,
                'num_iframes': random.randint(0, 2),
                'num_script_tags': random.randint(5, 20),
                'ratio_external_links': random.uniform(0.0, 0.9),
                'has_suspicious_title': 0,
                'page_size_kb': random.uniform(10.0, 200.0),
                
            
                'label': 0
            }
        data.append(sample)
        
    return pd.DataFrame(data)

def train_ensemble_model():
    print("Loading real dataset...")
    df = pd.read_csv('data/phishing_dataset.csv').sample(10000, random_state=42)

    print(df['label'].value_counts())

    print(df.columns)

    from sklearn.feature_extraction.text import TfidfVectorizer

    # ✅ Convert URL text → numeric features
    vectorizer = TfidfVectorizer(max_features=2000)

    X = vectorizer.fit_transform(df['url'])
    y = df['label']
    
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    
    print("Training models...")

    rf_clf = RandomForestClassifier(
       n_estimators=20,
       random_state=42,
       class_weight='balanced' 
    )

    gb_clf = GradientBoostingClassifier(n_estimators=20, random_state=42)
    
    # Voting Classifier (Ensemble Approach as specified)
    ensemble_clf = VotingClassifier(
        estimators=[('rf', rf_clf), ('gb', gb_clf)],
        voting='soft' # We want probabilities for the frontend
    )
    
    ensemble_clf.fit(X_train, y_train)
    
    y_pred = ensemble_clf.predict(X_test)

    from sklearn.metrics import classification_report
    print(classification_report(y_test, y_pred))

    acc = accuracy_score(y_test, y_pred)
    print(f"Ensemble Model Accuracy on Test Set: {acc:.4f}")
    
    # Save the model and feature columns
    os.makedirs(MODEL_DIR, exist_ok=True)
    
    joblib.dump(ensemble_clf, os.path.join(MODEL_DIR, 'ensemble_model.pkl'))
    joblib.dump(vectorizer, os.path.join(MODEL_DIR, 'vectorizer.pkl'))
    
    print(f"Model saved to {MODEL_DIR}")

if __name__ == '__main__':
    train_ensemble_model()
