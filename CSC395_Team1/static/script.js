document.addEventListener('DOMContentLoaded', () => {
    const dropdown = document.getElementById('dropdown');
    const textInput = document.getElementById('text-input');
    const submitButton = document.getElementById('submit-btn');
    const selectedOptionText = document.getElementById('selected-option');
    const messageBox = document.getElementById('message-box');
    const loadingIndicator = document.getElementById('loading'); // Ensure you have this element in your HTML

    // Dropdown selection handler
    dropdown.addEventListener('change', function() {
        selectedOptionText.textContent = this.options[this.selectedIndex].text;
        validateForm();
    });

    // Submit button click handler
    submitButton.addEventListener('click', async function() {
        const textInputValue = textInput.value.trim();
        const selectedCompany = selectedOptionText.textContent;

        if (!validateForm()) {
            alert("Please select a company and enter some ingredients.");
            return;
        }

        const dataToSend = { company: selectedCompany, ingredients: textInputValue };

        try {
            loadingIndicator.style.display = 'block';

            const response = await fetch('/submit', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(dataToSend)
            });

            const data = await response.json();
            loadingIndicator.style.display = 'none';

            if (response.ok) {
                const recipeHTML = `
                    <h2>${data.name}</h2>
                    <h4>${data.tagline}</h4>
                    <ul>
                        ${data.recipe.map(item => `<li>${item}</li>`).join('')}
                    </ul>
                `;
                messageBox.innerHTML = recipeHTML;
            } else {
                messageBox.textContent = `Error: ${data.error || 'An error occurred. Please try again.'}`;
            }
            messageBox.style.display = 'block';

            // Reset form after submission
            resetForm();

        } catch (error) {
            console.error('Error:', error);
            loadingIndicator.style.display = 'none';
            messageBox.textContent = 'There was an error sending your data to the server.';
            messageBox.style.display = 'block';
        }
    });

    // Input change handler
    textInput.addEventListener('input', validateForm);

    // Form validation function
    function validateForm() {
        const textInputValue = textInput.value.trim();
        const selectedOption = selectedOptionText.textContent;

        submitButton.disabled = textInputValue === "" || selectedOption === "Select a company";
        return !submitButton.disabled; // Return true if the button is enabled
    }

    // Function to reset the form fields
    function resetForm() {
        textInput.value = '';
        dropdown.selectedIndex = 0; // Resets the dropdown to the first option
        selectedOptionText.textContent = 'Select a company';
        validateForm(); // Re-evaluate button state
    }
});
