import datetime  # Import datetime module for recording timestamps

class KnowledgeBase:
    def __init__(self):
        # containing diseases, their symptoms, treatments, and severity
        self.diseases = {
            "Common Cold": {
                "symptoms": ["sneezing", "runny_nose"],
                "treatment": "rest and fluids",
                "severity": "Mild"
            },
            "Flu": {
                "symptoms": ["fever", "cough", "body_aches"],
                "treatment": "rest and fluids",
                "severity": "Moderate"
            },
            "Pneumonia": {
                "symptoms": ["fever", "cough", "shortness_of_breath"],
                "treatment": "antibiotics",
                "severity": "Severe"
            },
            "Tuberculosis": {
                "symptoms": ["cough", "weight_loss", "night_sweats"],
                "treatment": "antibiotics",
                "severity": "Severe"
            },
            "Malaria": {
                "symptoms": ["fever", "chills", "sweating", "body_aches"],
                "treatment": "antimalarial drugs",
                "severity": "Severe"
            },
            "COVID-19": {
                "symptoms": ["fever", "cough", "shortness_of_breath", "loss_of_taste"],
                "treatment": "isolation, hydration, antivirals",
                "severity": "Moderate"
            },
            "Asthma": {
                "symptoms": ["shortness_of_breath", "wheezing", "cough"],
                "treatment": "inhalers, bronchodilators",
                "severity": "Chronic"
            }
        }
        
        # store which diseases are linked to each symptom
        self.relationships = {}
        for disease, details in self.diseases.items():
            for symptom in details["symptoms"]:
                if symptom not in self.relationships:
                    self.relationships[symptom] = []
                self.relationships[symptom].append(disease)

        # List to store patient history
        self.patient_history = []

    def get_disease(self, symptoms, duration):
        possible = {}  # Dictionary to store disease match counts

        # Count occurrences of each disease based on user-input symptoms
        for symptom in symptoms:
            for disease in self.relationships.get(symptom, []):
                possible[disease] = possible.get(disease, 0) + 1
        
        total_symptoms = len(symptoms)  # Number of symptoms provided by the user
        
        # Calculate probability for each disease
        probabilities = {
            disease: (count / max(len(self.diseases[disease]["symptoms"]), total_symptoms)) * 100
            for disease, count in possible.items()
        }
        
        # Sort diseases by highest probability
        sorted_diseases = sorted(probabilities.items(), key=lambda x: x[1], reverse=True)

        # Store patient history with timestamp if a diagnosis is found
        if sorted_diseases:
            self.patient_history.append({
                "date": datetime.datetime.now(),
                "symptoms": symptoms,
                "diagnosis": sorted_diseases[0][0],  # Most probable disease
                "probability": sorted_diseases[0][1],
                "duration": duration
            })

        return sorted_diseases  # Return the sorted list of possible diagnoses

    def display_patient_history(self):
        if not self.patient_history:
            print("\nNo past diagnoses recorded.")
            return
        
        print("\n--- Patient History ---")
        for record in self.patient_history:
            print(f"Date: {record['date'].strftime('%Y-%m-%d %H:%M:%S')}")
            print(f"Symptoms: {', '.join(record['symptoms'])}")
            print(f"Diagnosis: {record['diagnosis']} (Probability: {record['probability']:.2f}%)")
            print(f"Duration of Symptoms: {record['duration']} days\n")

# Create an instance of the KnowledgeBase class
kb = KnowledgeBase()

# Display available symptoms
print("Medical Diagnosis System")
print("Available symptoms:", ", ".join(kb.relationships.keys()))

# Get user input for symptoms
print("\nEnter the symptoms you have (comma-separated):")
user_input = input("> ").lower().replace(" ", "_").split(',')
symptoms = [s.strip() for s in user_input]  # Clean user input

# Get user input for duration of symptoms
print("\nHow many days have you had these symptoms?")
duration = int(input("> "))

# Get possible diagnoses based on symptoms
diagnoses = kb.get_disease(symptoms, duration)

# Display the diagnosis results
if diagnoses:
    print("\nPossible diagnoses:")
    for disease, probability in diagnoses:
        severity = kb.diseases[disease]["severity"]
        print(f"- {disease} (Probability: {probability:.2f}%) - Severity: {severity}")
        print(f"  Recommended Treatment: {kb.diseases[disease]['treatment']}\n")
else:
    print("\nNo matching diagnoses found.")

# Display patient history
kb.display_patient_history()



