from classifiers.cnn import *
from solver import *
from data_utils import *
if __name__ == '__main__':
	dataset = get_CIFAR10_data()
	model = ThreeLayerConvNet(hidden_dim=500,reg=1e-3)
	solver = Solver(model, dataset, update_rule='adam', optim_config={'learning_rate':1e-3,},
		lr_decay=0.95, num_epochs=50, print_every=100)
	solver.train()