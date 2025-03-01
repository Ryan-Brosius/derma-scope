


async function sendDiagnosisData(image, age, gender, history, symptoms, lesion_location) {

  const formData = new FormData();

  formData.append("image", image);
  formData.append("age", age);
  formData.append("gender", gender);
  formData.append("history", history);
  formData.append("symptoms", symptoms);
  formData.append("lesion_location", lesion_location);
  
  try {
    const response = await fetch("http://localhost:8000/diagnose", {
        method: "POST",
        body: formData,
    });

    console.log(response)

    if (!response.ok) {
        throw new Error("Failed to send the request.");
    }

    const data = await response.json();
    console.log("Diagnosis Report:", data);
    alert("Report generated successfully!");
  } catch (error) {
      console.error("Error:", error);
      alert("An error occurred while generating the report.");
  }
}


