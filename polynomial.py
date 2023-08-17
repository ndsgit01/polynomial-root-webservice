class Polynomial:
    
    def __init__(self, coefficient_list):
        self.coefficients = coefficient_list
        self.degree = len(self.coefficients) - 1
        
    def __call__(self, x):
        value = 0
        x_pow_i = 1
        for coefficient in self.coefficients:
            value += coefficient * x_pow_i
            x_pow_i *= x
        return value
    
    def derivative(self):
        grad_coefficients = [self.coefficients[i] * i for i in 
                             range(1, self.degree + 1)]
        return Polynomial(grad_coefficients)
    
    def newtons_method(self, x, max_iter=1000):
        for _ in range(max_iter):
            if self(x) == 0:
                break
            x -= (self(x) / self.derivative()(x))
        return x
    
    def __str__(self):
        return ' + '.join([f'({str(coefficient)})x^{i}' for i, coefficient in
                        enumerate(self.coefficients)])
    
import numpy as np
p = Polynomial([1,2,1])
print(str(p))
print(p(np.array([0,1,2,3])))
