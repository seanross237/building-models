Ok, so at the highest level, there are 3 systems.


One is Eywa, the machine that when given a task, will attempt to solve it, benefitting from the learnings of past runs, while recording all its data of this run.


The next is Bonsai, the system around Eywa, that attempts to optimize it. Bonsai and Eywa are maybe not rly two distinct things, but for the moment in my mental model they are.


Last is the Potter. This is the system that takes a look at Bonsai, and the code of Bonsai and Eywa, and tries to optimize it. Not on the typical performance metrics. When it comes up with new versiions of Bonsai / Eywa, they should have identical outputs in every way. The potter merely tries to make the code more efficient, simple, modular, flexible, intuitive, robust etc. So for any run of eywa / bonzai, we will have a dry run machine (another important component), that for any situation will generate the possible proper outputs of the system. This dry run machine will be what keeps the Potter correct. Anything it creates must produce identical results.

The potter will be probably creating worktrees for its different systems, run them, and if it passes the dry runs then there will be other agents who'se job it is to evaluate those metrics of intuitiveness, flexibility, vizualizability etc.

So in terms of Eywa, here's the goal: to make a system that is maximally capable of being optimized in its effectiveness and growing in this over time, all autonomously.

My vision so far is this. We have some things that are 'locked in'.

Basically, it is a node based system that starts a root node. This takes a problem / task / question, then decides what to do next. Solve it, make a plan and solve it, make a plan and pass it to another agent to solve it, make a plan and divide it to multiple agents etc.

Every node though, should have the same DNA. We should hypothetically be able to take any node from the middle of a tree, and it should be at its core the same as any other.

The only things that should differ between nodes should be these 2 (or maybe 3) things:

The instructions it was given (which is comprehensive of its goal, and any supplementary information the system decided to provide it).

The parameter variables passed into it.
These parameter variables are the key: They are the variables that were either set at the tree level, or this nodes level, that determine certain attributes of how it will perform, and what it will have in its prompt.

These variables are the things the system will optimize. We will need to have an extremely clear set of them, and they are crucial to record thoroughly. Ideally, They are the only thing that should change between runs, and much of this problem is setting up an environment where all the the flexibility and crucial joints of the system that will need to be adapted from run to run for optimal performance is captured in the variables. Basically we want a system that is some extremely strong bones, then the rest is captured neatly in the variables. and the hope is we chose the right bones to allow maximam adaptation of the variables in a very organized yet flexible way. The idea is that the system, with the right variables, will perform optimally on a task, and we are building the system to be able to collect data from our runs of how different variables performed in different environments, learn from this, and then in the future the system when given a task can choose the optimal variables for that task. And i am hopeful that that is more of a node level thing, than tree level. maybe we wont be there to start, but i dream of a system where when it looks at a node, the rest of the tree is almost not important in that moment, that each node is likely an independent thing and the system is a simple chaining of them.

So, we also need to have an extremely strong benchmarking suite. I want a good name for this but haven't thought of one yet. Because it needs to be mentally seperate from the dry run kinda testing suite stuff that makes sure its functioning properly, though i guess they live in the same building.

Anyway, this benchmarking suite would be at least for now, a database of of tasks where the ideal output is somewhat verifiable in some way. To start this will be things we collect ourselves. The best of which are ones that have an easy way to "score" them beyond just right or wrong, but binary is ok too. and eventually we'll have some that get their validation by agents rating the output, such as similarity between outputted text, and goal text or something like that. but for now we'll start with the more clear cut stuff.

This benchmarking database would also be growing over time, as we encounter verifiable tasks out in the world, we can add them here.

We would want to categorize, and otherwise codify these tasks in whatever ways we can. We want ideally to have a system that given a task, we could turn it into numbers in some way, then look up past similar tasks to help figure out the ideal parameter variables to use on the current task.

So ideally a task lets say has 5 meta columns or something tagging it in different ways that ideally maximally encode its meaning.

So we'd have a benchmark database, and we would run eywa against it tons of times with different variables on the questions. This would produce a new scored dataset, with the metrics like score, time taken, tokens used, agents used, cost etc. We would use this to start building our knowledge mapping of what the right variables are for a given task. At the node level, and the tree level. So a row in this database might look like some id columns, some columns capturing the question (its raw text and the meta columns, im not sure what to call those yet), then the variables for that node, and then the metrics.

Later we will turn this into a machine learning problem probably: Given a task, what are the ideal variables to produce the highest score output? (A later version may also take in as input the root task). So to train this model, is another reason to have extremely clean data on all that happens. Primarily the question / task, the variables of the tree / node, and the score.

Obviously a huge component of this is being able to turn that question into something an ML model can take. I was thinking maybe we vectorize it or turn it into an embedding? But since questions can be rambly and what not, I was thinking there may be a way to massively reduce noise by first sending the question to a LLM layer that reduces the noise. For instance it could take the original task / question, and be told to output it again in the simplest formal / logic terms or something like that. Then those results get turned into embeddings. That's something we should experiment with down the line.

We'd also have a growing runs_history database, of all the instances eywa ran on a task. Some of these runs would make there way into the benchmark database if they are verifiable, and we decide to promote them there.

So we'd want to figure out the best performing variables 1) across the board on average, then 2) on certain types of tasks using something simple like heuristics perhaps, then 3) via an ML model that takes in the question / task, and outputs optimal variables.

Ok, good. the second thing, which we will be doing later, is establish the potter, which will be the system to test out different code that is hopefully better, but produces identical dry run results of eywa (where models arent actually ran), (and except that execution time could be a tiny bit different), and it should also hypothetically produce the same wet run results (except there will be some randomness of the models thats unavoidable).

So hopefully, we get to a point where the structure of any run of eywa, is simply: the task, and the variables that were chosen. more or less

We'll need to setup a system down the line for this to automatically learn, explore, identify its own blindspots etc. i think this is bonsai. though i think of bonsai as kindof the verb of trimming the tree (eywa). so the eywa / bonsai split isnt 100% clear. I suppose eywa is the bones and variables, bonsai is everything around it, to store, learn, and optimize variable selection.
