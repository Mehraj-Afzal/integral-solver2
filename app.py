from flask import Flask, render_template, request, jsonify
import sympy as sp
from sympy import symbols, integrate, sympify, exp
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
            logger.info(f"Attempting to solve integral: {expression_str}")
            expression_str = self._preprocess_expression(expression_str)
            expression = sp.sympify(expression_str)
            result = sp.integrate(expression, self.x)
            
            return {
                "success": True,
                "input": f"∫ {expression} dx",
                "result": f"{result} + C",
                "method": self._determine_integration_method(expression_str)
            }
        except Exception as e:
            logger.error(f"Error solving integral: {str(e)}")
            return {
                "success": False,
                "error": f"Error: {str(e)}"
            }

    def _preprocess_expression(self, expr):
        expr = expr.replace('^', '**')
        expr = expr.replace('e**x', 'exp(x)')
        expr = expr.replace('e^x', 'exp(x)')
        expr = expr.replace('ln(', 'log(')
        return expr

    def _determine_integration_method(self, expr):
        expr = expr.lower()
        if '*' in expr and ('sin' in expr or 'cos' in expr or 'exp' in expr or 'log' in expr):
            return "Integration by Parts"
        elif any(trig in expr for trig in ['sin', 'cos', 'tan', 'sec', 'csc', 'cot']):
            return "Trigonometric Integration"
        elif 'exp' in expr or 'e**' in expr:
            return "Exponential Integration"
        elif '/' in expr:
            return "Division Rule"
        elif '*' in expr:
            return "Product Rule"
        else:
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