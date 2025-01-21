function insertSymbol(symbol) {
    const input = document.getElementById('expression');
    const cursorPos = input.selectionStart;
    const textBefore = input.value.substring(0, cursorPos);
    const textAfter = input.value.substring(cursorPos);
    input.value = textBefore + symbol + textAfter;
    input.focus();
}

async function solveIntegral() {
    const expression = document.getElementById('expression').value;
    const resultDiv = document.getElementById('result');
    const solutionSteps = document.querySelector('.solution-steps');

    if (!expression) {
        resultDiv.innerHTML = `
            <div class="alert alert-warning">
                Please enter an expression
            </div>`;
        return;
    }

    try {
        const response = await fetch('/solve', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ expression: expression })
        });

        const data = await response.json();

        if (data.success) {
            solutionSteps.classList.remove('d-none');
            
            // Display steps
            document.querySelector('.step-1 .step-content').innerHTML = 
                `This is a ${data.method.toLowerCase()} integration problem`;
            
            document.querySelector('.step-2 .step-content').innerHTML = 
                data.steps.join('<br>');
            
            document.querySelector('.step-3 .step-content').innerHTML = 
                `Integrate: ${data.input}`;
            
            document.querySelector('.answer-content').innerHTML = 
                `${data.result}`;
        } else {
            resultDiv.innerHTML = `
                <div class="alert alert-danger">
                    ${data.error}
                </div>`;
        }
    } catch (error) {
        resultDiv.innerHTML = `
            <div class="alert alert-danger">
                An error occurred while processing your request
            </div>`;
    }
}

function toggleExamples() {
    const examples = document.getElementById('examples');
    examples.classList.toggle('d-none');
}

// Add Enter key support
document.getElementById('expression').addEventListener('keypress', function(e) {
    if (e.key === 'Enter') {
        solveIntegral();
    }
}); 