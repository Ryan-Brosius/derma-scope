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

    if (!response.ok) {
        throw new Error("Failed to send the request.");
    }

    const data = await response.json();
    console.log("Diagnosis Report:", data);
    
    // Store the result in localStorage for access in results.html
    localStorage.setItem("diagnosisData", JSON.stringify(data));
    
    // Redirect to the results page
    window.location.href = "results.html";
  } catch (error) {
    console.error("Error:", error);
    alert("An error occurred while generating the report.");
  }
}
