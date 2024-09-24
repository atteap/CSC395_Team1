// JavaScript to handle showing selected option text
document.getElementById('dropdown').addEventListener('change', function() {
    const selectedOptionText = document.getElementById('selected-option');
    selectedOptionText.textContent = this.options[this.selectedIndex].text; // Update the selected option text
});

// Handling the submit button
document.getElementById('submit-btn').addEventListener('click', function() {
    const textInput = document.getElementById('text-input').value;
    const selectedOption = document.getElementById('selected-option').textContent;
    
    // Validate if a company is selected and input text is entered
    if (selectedOption === "" || textInput.trim() === "") {
        alert("Please select a company and enter some text.");
        return;
    }

    // Select the message box
    const messageBox = document.getElementById('message-box');

    // Prepare data to send to the Flask server
    const dataToSend = {
        company: selectedOption,
        ingredients: textInput
    };

    // Send the data to the Flask server using the Fetch API
    fetch('/submit', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify(dataToSend)  // Convert the data to JSON
    })
    .then(response => response.json())  // Parse the response as JSON
    .then(data => {
        // Display the server response in the message box
        messageBox.textContent = `Response from server: ${data.message}`;
        messageBox.style.display = 'block';
    })
    .catch(error => {
        console.error('Error:', error);
        messageBox.textContent = 'There was an error sending your data to the server.';
        messageBox.style.display = 'block';
    });
});
