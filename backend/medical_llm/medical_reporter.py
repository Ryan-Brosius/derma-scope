from openai import OpenAI
from dotenv import load_dotenv
import os

class MedicalReportGenerator:
    def __init__(self):
        pass

    def generate_report(self, age, gender, history, symptoms, lesion_type, lesion_location):    
        return {"Likely Diagnosis" : "Death",
                "Diagnosis Explanation" : "Idk",
                "Patient Medical Report" : "Idk",
                "Diagnosis Explanation For Patient" : "Bruh",
                "Treatment Plan" : "Go outside"}


if __name__ == "__main__":
    generator = MedicalReportGenerator()
    
    print(generator.generate_report("", "", "", "", "", ""))
