from flask import Flask, render_template, request, jsonify
import sympy as sp
from sympy import symbols, integrate, sympify, exp, latex
import os
import logging
import sys

# Configure logging
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s %(levelname)s: %(message)s',
    stream=sys.stdout
)
logger = logging.getLogger(__name__)

app = Flask(__name__, 
    static_url_path='/static',
    static_folder='static')

app.config['SECRET_KEY'] = os.urandom(24)

class IntegralSolver:
    def __init__(self):
        self.x = sp.Symbol('x')

    def solve_integral(self, expression_str):
        try:
            # Clean up input
            expression_str = self._preprocess_expression(expression_str)
            expression = sp.sympify(expression_str)
            
            # Calculate integral
            result = sp.integrate(expression, self.x)
            
            # Generate formatted steps
            steps = self._generate_formatted_steps(expression, result)
            
            return {
                "success": True,
                "input": f"∫ {latex(expression)} dx",
                "steps": steps,
                "result": latex(result) + " + C",
                "method": self._determine_integration_method(expression_str)
            }
        except Exception as e:
            logger.error(f"Error solving integral: {str(e)}")
            return {
                "success": False,
                "error": "Please enter a valid expression (e.g., x^2 or sin(x))"
            }

    def _generate_formatted_steps(self, expression, result):
        steps = []
        
        if isinstance(expression, sp.Pow) and expression.base == self.x:
            power = expression.exp
            steps.append(f"For ∫x^{latex(power)}dx:")
            steps.append(f"Using power rule: ∫x^n dx = \\frac{{x^{{n+1}}}}{{n+1}}")
            steps.append(f"Here, n = {latex(power)}")
            steps.append(f"Therefore, ∫x^{latex(power)}dx = \\frac{{x^{latex(power+1)}}}{{{latex(power+1)}}} + C")
        
        elif isinstance(expression, sp.Add):
            steps.append("Using sum rule: ∫(f(x) + g(x))dx = ∫f(x)dx + ∫g(x)dx")
            for term in expression.args:
                term_result = sp.integrate(term, self.x)
                steps.append(f"∫{latex(term)}dx = {latex(term_result)}")
        
        return steps

    def _preprocess_expression(self, expr):
        expr = expr.replace('∫', '').strip()
        expr = expr.replace('^', '**')
        expr = expr.replace('dx', '')
        return expr.strip()

    def _determine_integration_method(self, expr):
        expr = expr.lower()
        if '**' in expr or '^' in expr:
            return "Power Rule"
        elif '+' in expr or '-' in expr:
            return "Sum Rule"
        elif any(t in expr for t in ['sin', 'cos', 'tan']):
            return "Trigonometric Integration"
        elif 'exp' in expr or 'e**' in expr:
            return "Exponential Integration"
        return "Basic Integration"

solver = IntegralSolver()

@app.route('/')
def index():
    logger.info("Accessing index page")
    try:
        return render_template('index.html')
    except Exception as e:
        logger.error(f"Error rendering index: {str(e)}")
        return f"Error loading page: {str(e)}", 500

@app.route('/health')
def health():
    return jsonify({"status": "healthy"}), 200

@app.route('/solve', methods=['POST'])
def solve():
    try:
        data = request.get_json()
        expression = data.get('expression', '')
        logger.info(f'Solving expression: {expression}')
        result = solver.solve_integral(expression)
        return jsonify(result)
    except Exception as e:
        logger.error(f'Error in /solve endpoint: {str(e)}')
        return jsonify({
            "success": False,
            "error": f"Server error: {str(e)}"
        }), 500

@app.errorhandler(Exception)
def handle_exception(e):
    logger.error(f'Unhandled exception: {str(e)}')
    return jsonify({
        "success": False,
        "error": "An unexpected error occurred"
    }), 500

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 10000))
    logger.info(f'Starting server on port {port}')
    app.run(host='0.0.0.0', port=port) 