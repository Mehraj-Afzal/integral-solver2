import sympy as sp
from sympy import symbols, integrate, sympify, exp, sin, cos, tan, log, pi

class AdvancedIntegralSolver:
    def __init__(self):
        self.x = sp.Symbol('x')
        self.rules_kashmiri = {
            "1. Basic Rules": {
                "Constant Rule": "∫ k dx = kx + C",
                "Power Rule": "∫ xⁿ dx = (xⁿ⁺¹)/(n+1) + C (n ≠ -1)",
                "Sum Rule": "∫(f(x) + g(x))dx = ∫f(x)dx + ∫g(x)dx",
                "Difference Rule": "∫(f(x) - g(x))dx = ∫f(x)dx - ∫g(x)dx"
            },
            "2. Integration by Parts": {
                "Formula": "∫u dv = uv - ∫v du",
                "Common Forms": [
                    "∫x·eˣ dx",
                    "∫x·sin(x) dx",
                    "∫x·ln(x) dx"
                ]
            },
            "3. Trigonometric Rules": {
                "Sin": "∫ sin(x) dx = -cos(x) + C",
                "Cos": "∫ cos(x) dx = sin(x) + C",
                "Tan": "∫ tan(x) dx = -ln|cos(x)| + C",
                "Sec²": "∫ sec²(x) dx = tan(x) + C",
                "Sec·Tan": "∫ sec(x)tan(x) dx = sec(x) + C"
            },
            "4. Exponential Rules": {
                "Natural": "∫ eˣ dx = eˣ + C",
                "General": "∫ aˣ dx = aˣ/ln(a) + C"
            },
            "5. Logarithmic Rules": {
                "Natural": "∫ (1/x) dx = ln|x| + C",
                "General": "∫ ln(x) dx = x·ln(x) - x + C"
            },
            "6. Product Rule Related": {
                "Formula": "∫u·v dx requires Integration by Parts",
                "Example": "∫x·sin(x) dx = -x·cos(x) + ∫cos(x) dx"
            }
        }

    def print_rules(self):
        print("🌟 Advanced Integration Rules:")
        print("=" * 60)
        for category, rules in self.rules_kashmiri.items():
            print(f"\n{category}:")
            print("-" * 40)
            if isinstance(rules, dict):
                for rule_name, rule_desc in rules.items():
                    if isinstance(rule_desc, list):
                        print(f"{rule_name}:")
                        for example in rule_desc:
                            print(f"  - {example}")
                    else:
                        print(f"{rule_name}: {rule_desc}")
            else:
                print(rules)

    def solve_integral(self, expression_str):
        try:
            # Clean up the input expression
            expression_str = self._preprocess_expression(expression_str)
            
            # Convert string expression to sympy expression
            expression = sp.sympify(expression_str)
            
            # Calculate indefinite integral
            result = sp.integrate(expression, self.x)
            
            # Get the method used (if possible)
            method = self._determine_integration_method(expression_str)
            
            return {
                "Input": f"∫ {expression} dx",
                "Result": f"{result} + C",
                "Method": method
            }
        except Exception as e:
            return {
                "Error": f"Error in expression. Details: {str(e)}",
                "Details": str(e)
            }

    def _preprocess_expression(self, expr):
        """Preprocess the input expression for better handling"""
        expr = expr.replace('^', '**')
        expr = expr.replace('e**x', 'exp(x)')
        expr = expr.replace('e^x', 'exp(x)')
        expr = expr.replace('ln(', 'log(')
        return expr

    def _determine_integration_method(self, expr):
        """Determine the likely integration method used"""
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

    def example_problems(self):
        examples = [
            ("x**2", "Power Rule"),
            ("sin(x)", "Trigonometric"),
            ("exp(x)", "Exponential"),
            ("x*exp(x)", "Integration by Parts"),
            ("x*sin(x)", "Integration by Parts"),
            ("1/x", "Logarithmic"),
            ("2*x + 3", "Basic Linear"),
            ("sin(x)*cos(x)", "Product Rule"),
            ("tan(x)", "Trigonometric")
        ]
        
        print("\n📚 Example Problems:")
        print("=" * 50)
        for ex, method in examples:
            result = self.solve_integral(ex)
            if "Error" not in result:
                print(f"\nMethod: {method}")
                print(f"Input: {result['Input']}")
                print(f"Result: {result['Result']}")
                print("-" * 30)

def main():
    solver = AdvancedIntegralSolver()
    
    while True:
        print("\n🔢 Choose an option:")
        print("1. View Integration Rules")
        print("2. See Example Problems")
        print("3. Solve an Integral")
        print("4. Exit")
        
        choice = input("Enter your choice (1-4): ").strip()
        
        if choice == '1':
            solver.print_rules()
        elif choice == '2':
            solver.example_problems()
        elif choice == '3':
            print("\nEnter an expression to integrate:")
            print("Examples: x**2, sin(x), exp(x), x*exp(x), x*sin(x)")
            user_input = input("Expression: ").strip()
            result = solver.solve_integral(user_input)
            if "Error" in result:
                print(f"❌ Error: {result['Error']}")
            else:
                print(f"\n✅ Solution:")
                print(f"Input: {result['Input']}")
                print(f"Method: {result['Method']}")
                print(f"Result: {result['Result']}")
        elif choice == '4':
            print("Goodbye! (خُدا حافِظ)")
            break
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main() 