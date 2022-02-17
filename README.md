# LearningToSimulateMaterialFlow
In this project a Machine Learning model is trained for learning a simulator for Material-Flow systems, where the Machine Learning model is based on Graph Neural Networks. The data for training the model is generated using an accurate physicbased simulator.

<img src="https://user-images.githubusercontent.com/63397065/154328745-03cefaf7-da0b-4547-a6eb-723be35ff510.PNG" width="450" /> 

<p float="left">
  <img src="https://user-images.githubusercontent.com/63397065/154323954-2132a131-3dad-4685-b478-ae35638c99bf.gif" width="200" />
  <img src="https://user-images.githubusercontent.com/63397065/154323543-fd61447a-6090-4ab4-80df-0e62b98c8bb3.gif" width="200" /> 
  <img src="https://user-images.githubusercontent.com/63397065/154446452-ef8398f6-7d25-4b6d-8787-f83e6b807375.gif" width="264" /> 
  
Based on DeepMind's Graph Nets (Library for building graph networks in Tensorflow and Sonnet https://github.com/deepmind/graph_nets) and their project Learning to Simulate Complex Physics with Graph Networks (https://github.com/deepmind/deepmind-research/tree/master/learning_to_simulate)

## Abstract
  
The commissioning of modern production plants is an important phase in the development process, as it becomes visible whether the developed plant with its software
and control technology meets all requirements. In order to reduce time-consuming
and cost-intensive iterative adjustments during planning and commissioning, virtual
commissioning with its simulation models has become established. The simulation
of virtual commissioning has high requirements in terms of computing time, so that
communication with the control system is possible in real time.
Modern production plants often consist of multiple sub-stations between which goods
are transported by Material-Flow systems. It is important to ensure reliable Material-Flow
between the stations so that the plant can run efficiently. In order to be able to detect
error cases during the Material-Flow within the simulation, such as jamming or tipping
over of goods, high-resolution process models that take physical effects into account are
required.
These physics-based Simulators are not solvable within the required real-time, especially for material flow scenes with many goods. An alternative is to use Deep Learning
to train the Simulator based on recorded training data. In recent years, Deep Learning
has successfully solved many Machine Learning tasks such as image classification and
speech recognition.
In many Deep Learning tasks, the data can be represented as a graph with complex
relationships and dependencies between objects. Scientific work of recent years shows
that the complex and computationally intensive relationships of graph data can be
modelled and learned using Graph Neural Networks.
  
## Structure of the learned simulator

In the simulation of physical systems, it is assumed that <img src="https://latex.codecogs.com/svg.image?X^t&space;\in&space;\mathcal{X}" title="X^t \in \mathcal{X}" /> describes the state of the system at time <img src="https://latex.codecogs.com/svg.image?t" title="t" />. By calculating the dynamics of the system over <img src="https://latex.codecogs.com/svg.image?K" title="K" /> time steps, a trajectory of system states 
  
<img src="https://latex.codecogs.com/svg.image?\mathbf{X^{t_{0:K}}}&space;=&space;(X^{t_0},...,X^{t_K})" title="\mathbf{X^{t_{0:K}}} = (X^{t_0},...,X^{t_K})" /> 
  
is obtained. A simulator <img src="https://latex.codecogs.com/svg.image?s:\mathcal{X}&space;\rightarrow&space;\mathcal{X}" title="s:\mathcal{X} \rightarrow \mathcal{X}" /> models the dynamics of the system by iterating each state <img src="https://latex.codecogs.com/svg.image?\tilde{X}^{t_i}" title="\tilde{X}^{t_i}" /> is iteratively mapped to a subsequent state <img src="https://latex.codecogs.com/svg.image?\tilde{X}^{t_{i&plus;1}}&space;=&space;s(\tilde{X}^{t_i})" title="\tilde{X}^{t_{i+1}} = s(\tilde{X}^{t_i})" />. Thus, a simulated trajectory is given by 
  
<img src="https://latex.codecogs.com/svg.image?\mathbf{\tilde{X}^{t_{0:K}}}&space;=&space;(X^{t_0},\tilde{X}^{t_1},...,\tilde{X}^{t_K})" title="\mathbf{\tilde{X}^{t_{0:K}}} = (X^{t_0},\tilde{X}^{t_1},...,\tilde{X}^{t_K})" />. 
  
The learned simulator predicts future states of the piece goods starting from an initial configuration <img src="https://latex.codecogs.com/svg.image?X^{t_0}" title="X^{t_0}" /> using the learned function <img src="https://latex.codecogs.com/svg.image?d_{\theta}" title="d_{\theta}" /> and a specified updating procedure. Therefore the learnable simulator <img src="https://latex.codecogs.com/svg.image?s_\theta" title="s_\theta" /> uses the computed dynamics of the current state to predict the subsequent state. For this purpose, the dynamics of the system are computed as accelerations of the particles <img src="https://latex.codecogs.com/svg.image?Y&space;\in&space;\mathcal{Y}" title="Y \in \mathcal{Y}" /> using the parameterized function <img src="https://latex.codecogs.com/svg.image?d_{\theta}:\mathcal{X}&space;\rightarrow&space;\mathcal{Y}" title="d_{\theta}:\mathcal{X} \rightarrow \mathcal{Y}" />, where the parameters <img src="https://latex.codecogs.com/svg.image?\theta" title="\theta" /> are optimized during the training phase. Finally, a numerical integration method is used to predict the subsequent state <img src="https://latex.codecogs.com/svg.image?\tilde{X}^{t_{i&plus;1}}" title="\tilde{X}^{t_{i+1}}" /> from the current state <img src="https://latex.codecogs.com/svg.image?\tilde{X}^{t_i}" title="\tilde{X}^{t_i}" /> and the accelerations calculated by <img src="https://latex.codecogs.com/svg.image?d_{\theta}" title="d_{\theta}" />. The learning function <img src="https://latex.codecogs.com/svg.image?d_{\theta}:\mathcal{X}&space;\rightarrow&space;\mathcal{Y}" title="d_{\theta}:\mathcal{X} \rightarrow \mathcal{Y}" /> of the simulator, whose parameters <img src="https://latex.codecogs.com/svg.image?\theta" title="\theta" /> are optimized during the training phase, consists of encoder, processor and decoder.
  
![Capture](https://user-images.githubusercontent.com/63397065/154433542-bb3c075c-fcb7-443b-aed7-b0afa2f3ccac.PNG)
  
The encoder constructs an initial graph <img src="https://latex.codecogs.com/svg.image?G^0" title="G^0" /> by assigning a node to each object and adding edges between the node and all other objects within a constant radius of connectivity <img src="https://latex.codecogs.com/svg.image?R" title="R" />. The edges reflect the local connectivity of the object. The edges reflect the local interactions of the objects. The embeddings of the nodes are learned based on the states of the objects <img src="https://latex.codecogs.com/svg.image?x_i" title="x_i" />, that represent the positions and the velocities of the past <img src="https://latex.codecogs.com/svg.image?n" title="n" /> time steps of the objects.
The processor forwards messages between nodes via the edges. It computes the interactions between nodes over <img src="https://latex.codecogs.com/svg.image?M" title="M" /> steps, where <img src="https://latex.codecogs.com/svg.image?G^{m&plus;1}&space;=&space;GN^{m&plus;1}(G^m)" title="G^{m+1} = GN^{m+1}(G^m)" />. Here <img src="https://latex.codecogs.com/svg.image?GN" title="GN" /> is a Graph Net Block and uses Artificial Neural Networks as internal edge and node update functions. The processor returns the final graph <img src="https://latex.codecogs.com/svg.image?G^M&space;=&space;Processor(G^0)" title="G^M = Processor(G^0)" />. In physics, these interactions correspond to the exchange of energy and momentum between particles.
The decoder extracts dynamics information from the nodes of the final graph with <img src="https://latex.codecogs.com/svg.image?y_i&space;=&space;\delta_v(G^M)" title="y_i = \delta_v(G^M)" />. Learning <img src="https://latex.codecogs.com/svg.image?\delta_v" title="\delta_v" /> should result in <img src="https://latex.codecogs.com/svg.image?y_i" title="y_i" /> being the velocity to the next time step as relevant dynamics information reflects, so that <img src="https://latex.codecogs.com/svg.image?y_i" title="y_i" /> is semantically meaningful for the update procedure.

## Evaluation
  
<img src="https://user-images.githubusercontent.com/63397065/154442211-96543bc7-4a4c-42cd-a378-fc57eefdf29e.PNG" width="600" /> 
  
The dynamics of the Material-Flow scene can be learned by the Machine Learning model, because the average MSE between the estimated trajectory <img src="https://latex.codecogs.com/svg.image?\mathbf{\tilde{X}^{t_{0:K}}}" title="\mathbf{\tilde{X}^{t_{0:K}}}" /> and the test data trajectory <img src="https://latex.codecogs.com/svg.image?\mathbf{X^{t_{0:K}}}" title="\mathbf{X^{t_{0:K}}}" /> is small with <img src="https://latex.codecogs.com/svg.image?0.0296&space;m" title="0.0296 m" />. It can be seen that especially the dynamics of the test data sets with a stopper angle α between 40° and 50° can be predicted very well. For stopper angles <img src="https://latex.codecogs.com/svg.image?\alpha" title="\alpha" /> that deviate further from the mean value of the stopper angles of all training data sets <img src="https://latex.codecogs.com/svg.image?\alpha&space;=&space;45^\circ" title="\alpha = 45^\circ" />, the simulated trajectories of the learned simulator become less accurate. This is especially true for test data sets with small stopper angle <img src="https://latex.codecogs.com/svg.image?\alpha" title="\alpha" />, since the unit loads collide more frequently in these data sets and are thus more difficult to simulate. The evaluation of the computation time for simulating a trajectory shows that the learned simulator with an average computation time of <img src="https://latex.codecogs.com/svg.image?3.16&space;s" title="3.16 s" /> simulates significantly faster than the physics-based simulator with <img src="https://latex.codecogs.com/svg.image?10.02&space;s" title="10.02 s" />.

