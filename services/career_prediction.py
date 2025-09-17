import numpy as np
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense
from tensorflow.keras.utils import to_categorical

class CareerPredictionDL:
    def __init__(self):
        # Define skills and careers
        self.skills_list = [
            "python", "machine learning", "statistics", "data analysis",
            "html", "css", "javascript", "react",
            "java", "c++", "algorithms",
            "excel", "presentation", "communication",
            "deep learning", "tensorflow", "pytorch"
        ]
        self.careers = [
            "Data Scientist", "Web Developer", "Software Engineer", "Business Analyst", "AI Engineer"
        ]
        # Dummy training data (skills encoded as binary vectors)
        self.X_train = np.array([
            [1,1,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0],  # Data Scientist
            [0,0,0,0,1,1,1,1,0,0,0,0,0,0,0,0,0,0],  # Web Developer
            [1,0,0,0,0,0,0,0,1,1,1,0,0,0,0,0,0,0],  # Software Engineer
            [0,0,1,1,0,0,0,0,0,0,0,1,1,1,0,0,0,0],  # Business Analyst
            [1,1,0,0,0,0,0,0,0,0,0,0,0,0,1,1,1],    # AI Engineer
        ])
        self.y_train = np.array([0, 1, 2, 3, 4])  # Indices of careers
        self.y_train_cat = to_categorical(self.y_train, num_classes=len(self.careers))

        # Build and train the model
        self.model = Sequential([
            Dense(32, activation='relu', input_shape=(len(self.skills_list),)),
            Dense(16, activation='relu'),
            Dense(len(self.careers), activation='softmax')
        ])
        self.model.compile(optimizer='adam', loss='categorical_crossentropy', metrics=['accuracy'])
        self.model.fit(self.X_train, self.y_train_cat, epochs=100, verbose=0)

    def predict(self, skills):
        # Encode input skills as binary vector
        skill_vector = np.array([1 if skill.lower() in [s.lower() for s in skills] else 0 for s in self.skills_list])
        skill_vector = skill_vector.reshape(1, -1)
        pred_probs = self.model.predict(skill_vector)
        pred_idx = np.argmax(pred_probs)
        return self.careers[pred_idx]

# Example usage:
if __name__ == "__main__":
    user_skills = ["Python", "Machine Learning", "Statistics"]
    predictor = CareerPredictionDL