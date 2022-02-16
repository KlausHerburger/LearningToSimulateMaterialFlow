# LearningToSimulateMaterialFlow
In this project a Machine Learning model is trained for learning a simulator for Material-Flow systems, where the Machine Learning model is based on Graph Neural Networks. The data for training the model is generated using an accurate physicbased simulator.

<p float="left">
  <img src="https://user-images.githubusercontent.com/63397065/154323543-fd61447a-6090-4ab4-80df-0e62b98c8bb3.gif" width="200" /> 
  <img src="https://user-images.githubusercontent.com/63397065/154323954-2132a131-3dad-4685-b478-ae35638c99bf.gif" width="200" />
  <img src="https://user-images.githubusercontent.com/63397065/154325993-e522f519-fc84-4b99-bca6-d48bb037c122.gif" width="200" /> 
/>

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
