from openai import OpenAI
from dotenv import load_dotenv
import os

class MedicalReportGenerator:
    def __init__(self, model="gpt-4o-mini"):
        load_dotenv()

        self.model = model

        API_KEY = os.getenv("GPT_API_KEY")
        self.client = OpenAI(
            api_key=API_KEY,
        )

    def generate_report(self, age, gender, history, symptoms, lesion_type, lesion_location, max_tokens=800):    
        reports = []

        context = (
            f"Patient Report:\n"
            f"- Age: {age}\n"
            f"- Gender: {gender}\n"
            f"- Medical History: {history}\n"
            f"- Symptoms: {symptoms}\n"
            f"\n"
            f"- Skin Lesion Analysis: {lesion_type}\n"
            f"- Skin Lesion Location: {lesion_location}\n"
        )
        task = (
            f'\n'
            f"Task:\n"
            f"Based on the patient details provided, give a primary diagnosis and a secondary diegnosis (if necessary). "
            f"Include a brief rationale for each possibility. "
            f"Only include the diagnosis(es) with short descriptions in plain text without any extra formatting.\n"
        )

        messages = [
            {"role": "system", "content": "You are an expert medical consultant who provides diagnostic reports."},
            {"role": "user", "content": context + task}
        ]
        response = self.client.chat.completions.create(
            model=self.model,
            messages=messages,
            max_tokens=max_tokens,
            temperature=0.7,
        )
        reports.append(response.choices[0].message.content)
        task = (
            f"\nLikely Diagnosis: {reports[0]}"
            f'\n\n'
            f'Task:\n'
            f"Analyze the listed diagnosis(es) in detail, taking into account the patient's age, gender, medical history, symptoms, and lesion characteristics. "
            f"Provide a structured and professional explanation that clearly outlines why the diagnosis fits the patient’s condition. "
            f"Keep the response in plain text and limit the content to the explanation without any additional formatting.\n"
        )

        messages = [
            {"role": "system", "content": "You are an expert medical consultant who provides detailed diagnostic reports."},
            {"role": "user", "content": context + task}
        ]
        response = self.client.chat.completions.create(
            model=self.model,
            messages=messages,
            max_tokens=max_tokens,
            temperature=0.7,
        )
        reports.append(response.choices[0].message.content)
        task = (
            f"\nLikely Diagnosis: {reports[0]}"
            f'\n\n'
            f"Diagnosis Explanation: {reports[1]}"
            f'\n\n'
            f'Task:\n'
            f"Integrate the information into a formal medical record entry that a doctor would use. "
            f"Include only the following details: Name, Gender, Age, Medical History, Current Symptoms, Primary Diagnosis, Secondary Diagnosis (if applicable), and Recommended Treatment. "
            f"Ensure the report is written in plain text without any extra formatting.\n"
        )

        messages = [
            {"role": "system", "content": "You are an expert medical consultant who provides detailed diagnostic reports."},
            {"role": "user", "content": context + task}
        ]

        response = self.client.chat.completions.create(
            model=self.model,
            messages=messages,
            max_tokens=max_tokens,
            temperature=0.7,
        )
        reports.append(response.choices[0].message.content)
        task = (
            f"\nLikely Diagnosis: {reports[0]}"
            f'\n\n'
            f"Diagnosis Explanation: {reports[1]}"
            f'\n\n'
            f'Task:\n'
            f"Explain the diagnosis in simple, clear language tailored for the patient. "
            f"Focus on conveying the key points of the diagnosis and its implications in a brief and understandable manner. "
            f"Keep the response plain and free of fancy formatting.\n"
        )

        messages = [
            {"role": "system", "content": "You are an expert medical consultant who provides detailed diagnostic reports."},
            {"role": "user", "content": context + task}
        ]
        response = self.client.chat.completions.create(
            model=self.model,
            messages=messages,
            max_tokens=max_tokens,
            temperature=0.7,
        )
        reports.append(response.choices[0].message.content)
        task = (
            f"\nLikely Diagnosis: {reports[0]}"
            f'\n\n'
            f"Diagnosis Explanation: {reports[1]}"
            f'\n\n'
            f'Task:\n'
            f"Develop a concise treatment plan and provide recommendations for diagnosis that will be presented to the patient. "
            f"Make it simple and easy to understand for the patient. "
            f"Outline clear steps and suggestions about the best treatments. "
            f"Ensure the explanation is in plain text without any fancy formatting.\n"
        )

        messages = [
            {"role": "system", "content": "You are an expert medical consultant who provides detailed diagnostic reports."},
            {"role": "user", "content": context + task}
        ]
        response = self.client.chat.completions.create(
            model=self.model,
            messages=messages,
            max_tokens=max_tokens,
            temperature=0.7,
        )
        reports.append(response.choices[0].message.content)

        return [r.replace("*", "") for r in reports]


if __name__ == "__main__":
    generator = MedicalReportGenerator()
    
    report = generator.generate_report(
        age=45,
        gender="Female",
        history="None",
        symptoms="None",
        lesion_type="actinic keratoses and intraepithelial carcinoma",
        lesion_location="Forearm"
    )
    print("=== Generated Diagnostic Report ===\n")
    reports = ["Likely Diagnosis", "Diagnosis Explanation", "Patient Medical Report", "Diagnosis Explanation For Patient", "Treatment Plan"]

    for i, r in enumerate(reports):
        print(f"=== {r} ===\n")
        print(report[i])
        print()
