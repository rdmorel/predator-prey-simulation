# predator-prey-simulation
python simulation of the relationship between wolf and rabbit populations

See wiki tab for graph of results

Assignment:

Predator-prey simulations are used to understand how populations of animals interact. In this lab’s agentbased simulation, there will be two types of animals: Rabbits (prey) and Wolves (predators). Your task is to program the individual animal behaviors. Both types of animals run around randomly and reproduce with some probability. The wolves eat nearby rabbits, removing rabbits from the population. The wolves gain energy from eating the rabbits, but will die if their energy drops to zero. The animals are born with some energy units and expend energy each timestep. Wolves are less likely to reproduce if their energy is low. The Animal parent class and the World class are provided. Your first task is to implement the Rabbit and Wolf child classes. You should not modify the World or Animal classes. Next, you should run experiments with your simulation. Gather data about how the populations change as you vary one of the parameters: initial population size, speed, movement strategy, reproduction rate. Use Window() to plot the data and include the graph along with a brief reflection in your lab report. The display attribute can be used to
disable drawing each animal, resulting in faster simulations.
