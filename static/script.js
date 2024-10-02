document.addEventListener('DOMContentLoaded', () => {
    const form = document.querySelector('form');
    const dropdown = document.getElementById('dropdown');
    const textInput = document.getElementById('text-input');
    const submitButton = document.getElementById('submit-btn');
    const selectedOptionText = document.getElementById('selected-option');
    const messageBox = document.getElementById('message-box');
    const loadingIndicator = document.getElementById('loading');

    form.addEventListener('submit', event => event.preventDefault());
    selectedOptionText.textContent = 'Select a company';

    dropdown.addEventListener('change', () => {
        selectedOptionText.textContent = dropdown.options[dropdown.selectedIndex].text;
        validateForm();
    });

    submitButton.addEventListener('click', async (event) => {
        event.preventDefault();

        const textInputValue = textInput.value.trim();
        const selectedCompany = dropdown.value;

        if (!validateForm()) {
            alert("Please select a company and enter some ingredients.");
            return;
        }

        const dataToSend = { company: selectedCompany, ingredients: textInputValue };

        try {
            loadingIndicator.style.display = 'block';
            submitButton.disabled = true;
            messageBox.style.display = 'none';
            messageBox.textContent = '';

            const response = await fetch('/submit', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(dataToSend),
            });

            if (!response.ok) {
                throw new Error('Failed to fetch response from the server');
            }

            const data = await response.json(); // Directly parse the JSON response

            loadingIndicator.style.display = 'none';
            submitButton.disabled = false;

            if (data.error) {
                messageBox.textContent = `Error: ${data.error}`;
            } else {
                const recipeHTML = `
                    <h2>${data.name}</h2>
                    <h4>${data.tagline}</h4>
                    <h3>Ingredients:</h3>
                    <ul>
                        ${data.ingredients.map(item => `<li>${item}</li>`).join('')}
                    </ul>
                    <h3>Instructions:</h3>
                    <ol>
                        ${data.instructions.map(instruction => `<li>${instruction}</li>`).join('')}
                    </ol>
                `;
                messageBox.innerHTML = recipeHTML;
            }

            messageBox.style.display = 'block'; 
            resetForm();

        } catch (error) {
            console.error('Error:', error);
            loadingIndicator.style.display = 'none';
            submitButton.disabled = false; 
            messageBox.textContent = 'There was an error sending your data to the server.';
            messageBox.style.display = 'block';
        }
    });

    textInput.addEventListener('input', validateForm);

    function validateForm() {
        const textInputValue = textInput.value.trim();
        const selectedCompany = dropdown.value;
        const isFormValid = textInputValue !== "" && selectedCompany !== "" && selectedCompany !== "none";
        submitButton.disabled = !isFormValid;
        return isFormValid;
    }

    function resetForm() {
        textInput.value = '';
        dropdown.selectedIndex = 0;
        selectedOptionText.textContent = 'Select a company';
        validateForm();
    }
});
