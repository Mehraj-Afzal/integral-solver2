async function solveIntegral() {
    const expression = document.getElementById('expression').value;
    const resultDiv = document.getElementById('result');

    if (!expression) {
        resultDiv.innerHTML = `
            <div class="alert alert-warning" role="alert">
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
            resultDiv.innerHTML = `
                <div class="alert alert-success" role="alert">
                    <h5>Input:</h5>
                    <div class="mb-2">${data.input}</div>
                    <h5>Result:</h5>
                    <div class="mb-2">${data.result}</div>
                    <h5>Method:</h5>
                    <div>${data.method}</div>
                </div>`;
        } else {
            resultDiv.innerHTML = `
                <div class="alert alert-danger" role="alert">
                    ${data.error}
                </div>`;
        }
    } catch (error) {
        resultDiv.innerHTML = `
            <div class="alert alert-danger" role="alert">
                An error occurred while processing your request
            </div>`;
    }
}

function showExamples() {
    const resultDiv = document.getElementById('result');
    resultDiv.innerHTML = `
        <div class="example-box">
            <h5>Example Inputs:</h5>
            <ul>
                <li>Basic: x^2, 2*x + 3</li>
                <li>Trigonometric: sin(x), cos(x), tan(x)</li>
                <li>Exponential: exp(x), e^x</li>
                <li>Integration by Parts: x*sin(x), x*exp(x)</li>
                <li>Logarithmic: log(x), 1/x</li>
            </ul>
            <p><strong>Note:</strong> Use ^ for powers, * for multiplication</p>
        </div>`;
}

// Add Enter key support
document.getElementById('expression').addEventListener('keypress', function(e) {
    if (e.key === 'Enter') {
        solveIntegral();
    }
}); 