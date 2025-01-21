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
            # Remove the integral symbol and clean up input
            expression_str = expression_str.replace('∫', '').strip()
            expression_str = self._preprocess_expression(expression_str)
            
            # Convert to sympy expression
            expression = sp.sympify(expression_str)
            
            # Calculate integral
            result = sp.integrate(expression, self.x)
            
            # Generate solution steps
            steps = self._generate_steps(expression, result)
            
            return {
                "success": True,
                "input": f"∫ {expression} dx",
                "steps": steps,
                "result": f"{result} + C",
                "latex_result": f"{latex(result)} + C",
                "method": self._determine_integration_method(expression_str)
            }
        except Exception as e:
            logger.error(f"Error solving integral: {str(e)}")
            return {
                "success": False,
                "error": f"Error: Please enter a valid expression (e.g., x^2 or sin(x))"
            }

    def _generate_steps(self, expression, result):
        steps = []
        
        # For sum of terms
        if isinstance(expression, sp.Add):
            steps.append("Using sum rule: ∫(f(x) + g(x))dx = ∫f(x)dx + ∫g(x)dx")
            for term in expression.args:
                term_result = sp.integrate(term, self.x)
                if term.is_number:
                    steps.append(f"∫{term}dx = {term}x (Constant rule)")
                elif term.is_Pow and self.x in term.free_symbols:
                    base, exp = term.args
                    if base == self.x:
                        steps.append(f"∫x^{exp}dx = x^{exp+1}/{exp+1} (Power rule)")
                
        # For single term
        else:
            if expression.is_number:
                steps.append(f"Using constant rule: ∫kdx = kx")
            elif expression.is_Pow and self.x in expression.free_symbols:
                base, exp = expression.args
                if base == self.x:
                    steps.append(f"Using power rule: ∫x^ndx = x^(n+1)/(n+1)")
        
        steps.append(f"Final result: {result} + C")
        return steps

    def _preprocess_expression(self, expr):
        # Clean up the input expression
        expr = expr.replace('^', '**')
        expr = expr.replace('e**x', 'exp(x)')
        expr = expr.replace('e^x', 'exp(x)')
        expr = expr.replace('dx', '')  # Remove dx if present
        return expr.strip()

    def _determine_integration_method(self, expr):
        expr = expr.lower()
        methods = {
            'power_rule': 'x**' in expr or 'x^' in expr,
            'constant': expr.replace(' ', '').isnumeric(),
            'sum_rule': '+' in expr or '-' in expr,
            'trig': any(t in expr for t in ['sin', 'cos', 'tan']),
            'exp': 'exp' in expr or 'e**' in expr
        }
        
        if methods['sum_rule']:
            return "Sum Rule"
        elif methods['power_rule']:
            return "Power Rule"
        elif methods['constant']:
            return "Constant Rule"
        elif methods['trig']:
            return "Trigonometric Integration"
        elif methods['exp']:
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