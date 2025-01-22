function insertSymbol(symbol) {
    const input = document.getElementById('expression');
    const cursorPos = input.selectionStart;
    const textBefore = input.value.substring(0, cursorPos);
    const textAfter = input.value.substring(cursorPos);
    input.value = textBefore + symbol + textAfter;
    input.focus();
}

function renderLatex(elementId, latex) {
    const element = document.getElementById(elementId);
    katex.render(latex, element, {
        displayMode: true,
        throwOnError: false
    });
}

async function solveIntegral() {
    const expression = document.getElementById('expression').value;
    const resultDiv = document.getElementById('result');

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
            // Render each step with LaTeX
            renderLatex('step1', `\\text{This is a ${data.method.toLowerCase()} integration problem}`);
            
            // Render the rule application
            let ruleText = data.steps.join(' \\\\ ');
            renderLatex('step2', ruleText);
            
            // Render the integration step with single integral
            renderLatex('step3', `\\int ${data.input.replace('∫', '')}`);
            
            // Render the final answer
            renderLatex('final', data.result);
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