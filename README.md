# Hospital-Inventory-and-Resource-Integration-System-HIRIS-
## Inspiration
- Inadequate inventory management practises lead to supply chain issues in healthcare [link](https://www.ghx.com/the-healthcare-hub/supply-chain-issues/)
- Medical resources not available where needed - most significant in times of crisis such as pandemics or mass casualty events
- Weighing system inspired by weights in neural networks and coefficients in PID (Proportional-Derivative-Integral) controllers, both of which can be customized to fit different needs

## What it does
HIRIS allows hospitals to use resources from other hospitals in times of need, by identifying and recommending nearby hospitals with a potential surplus of resources, based on the amount and type of resource needed.

## How we built it
First, we identified the goals that the system of HIRIS needs to fulfill. From these goals, we determined a data structure that contains necessary data categories and is organized to streamline input, manipulation and retrieval. Then, we separated the system into multiple programs that interface with one another and the data structure, and established milestones for their completion. Before coding each program, we also agreed upon the interfaces between the programs.
While we worked on separate parts of the system, we performed frequent progress check-ups to test programs, , as well as identify unexpected new goals or changes to the interface.

## Challenges we ran into
- Lack of real data - created randomized mock data that has the same structure and purpose
- Assumptions made for data categories - a program designed to be adaptable for new data categories before release

## Accomplishments that we're proud of
- Completing our first hackathon
- Researching and setting goals within the first two hours of the project
- Distributing jobs according to the strengths of team members

## What we learned
- Integrating various programs by reading and writing to files, to create a program that is more organized and capable
- Use of pandas Python module for data manipulation and retrieval

## What's next for HIRIS
- Improving performance of data retrieval algorithms, for scalability to larger datasets
- Adding remote access capabilities
- Integrating the weighing system with findings from system modelling studies, to provide more practical optimizations
- Allow hospitals to specify base demand to retain a supply of resources if needed
- Adding new/replacing current data categories to better suit medical industry needs
- Improving the accuracy of Estimated Time to Arrival predictions
- Improving security

Devpost link: https://devpost.com/software/hospital-inventory-and-resource-integration-system-hiris?ref_content=my-projects-tab&ref_feature=my_projects
