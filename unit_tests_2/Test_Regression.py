from HW2_calculations.Regression import regress,residual_bootstrap,pair_bootstrap
import numpy as np
# Generate some sample data
test_X = np.linspace(-3,1, 50)
test_V = np.linspace(2, 3, 50)
test_sigma = np.linspace(3, 4, 50)
test_eta=2
test_beta=1
test_h = test_eta*test_sigma*pow(test_X/((6/6.5)*test_V),test_beta) + 0.2 * np.random.normal(size=50)

test_params = regress(test_sigma,test_X,test_V,test_h)
#this should print something around [2,1]
print(test_params)

#testing residual bootstrap
print("residual bootstrap:")
#this print out the original beta, original eta, list of new beta, new eta and beta and eta's t_stat and the p-value
p_value_eta, p_value_beta= residual_bootstrap(test_sigma, test_X, test_V, test_h, test_beta, test_eta)
print("p_value_eta: ", p_value_eta)
print("p_value_beta: ", p_value_beta)

#testing pair bootstrap
print("pair bootstrap:")
#this print out the original beta, original eta, list of new beta, new eta and beta and eta's t_stat and the p-value
p_value_eta, p_value_beta= pair_bootstrap(test_sigma, test_X, test_V, test_h, test_beta, test_eta)
print("p_value_eta: ", p_value_eta)
print("p_value_beta: ", p_value_beta)
