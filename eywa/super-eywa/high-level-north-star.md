# Super-Eywa — High-Level North Star

Super-Eywa is being built as a system that can improve itself over time in two different ways:

1. by learning to choose better variables for a task
2. by improving the bones of the system without changing validated behavior

The long-term goal is a machine where, as much as possible, a run is simply:

- the task
- the chosen variables

The system should be designed so that the bones stay strong and stable, while the variables capture the main behavioral flexibility of the machine.

## The Three Systems

### Eywa

Eywa is the task-solving machine.

Given a task, it starts a root node and works through a graph of same-DNA nodes to try to solve the task. Each node should be fundamentally the same kind of thing. The main things that should differ from node to node are:

- the input it was given
- the variables it was given

### Bonsai

Bonsai is the system around Eywa that stores, learns, evaluates, and improves variable selection.

Its job is to study past runs, understand what kinds of variables worked well in what kinds of situations, and gradually get better at choosing the right variables for new tasks.

A likely shorter-term subcomponent of Bonsai is Gardener: a model-guided learning layer that reviews runs and proposes better variable ideas and experiments before more mature ML-based selection is in place.

### Potter

Potter is the later system that improves the bones of Eywa and Bonsai.

Its job is not to change the intended behavior of the machine. Its job is to make the code more efficient, simple, modular, flexible, intuitive, and robust while preserving validated behavior. It should be constrained by dry-run equivalence and other correctness checks.

## The Main Design Bet

The main design bet is that the system should be built so that most of the important adaptation happens through explicit variables rather than through hidden behavior spread across the codebase.

That means:

- the bones of the machine should be strong and stable
- the important run-to-run flexibility should be captured in variables
- those variables should be recorded clearly
- the system should later be able to learn which variables work best for which tasks

The hope is that this becomes true not only at the whole-run level, but increasingly at the node level as well.

## The Node-First Vision

The node is the core unit of the system.

The dream is that any node taken from the middle of a run is still, at its core, the same machine as any other node. Over time, the system should become more and more able to treat a node as an independent unit of decision, execution, and learning rather than relying on brittle special-case tree logic.

The system should be graph-capable, but still highly readable to a human.

## The Learning Vision

The system should record enough truth from every run that it can later learn from it.

At a high level, the learning path is:

1. identify variable choices that work best on average
2. identify stronger variable choices for certain kinds of tasks
3. later move toward more learned or model-based variable selection

The point of Bonsai is to make Eywa better at the variables layer over time.

## The Benchmarking Vision

The system should have a strong benchmarking layer that is separate from the dry-run correctness layer.

The benchmarking layer exists to measure effectiveness. It should contain tasks where outputs are meaningfully verifiable and scoreable. Over time, this should grow into a strong dataset for comparing variable choices and learning what works.

The dry-run layer exists for a different reason. It protects correctness and later protects Potter.

These two systems should stay clearly distinct:

- benchmarking measures how well the machine performs
- dry runs protect whether the machine is still behaving as intended

## The Potter Vision

Later, Potter should be able to try new versions of the code and compare them against a dry-run machine that can determine the proper outputs for known situations without relying on live model randomness.

Anything Potter creates should preserve validated behavior. It may improve the implementation, but it should not silently change what the machine is supposed to do.

This is the second self-improvement path of Super-Eywa:

- Bonsai improves variable choice
- Potter improves the bones

## What Success Looks Like

Success looks like a system where:

- Eywa can take a task and solve it through a graph of same-DNA nodes
- the important behavioral flexibility is explicit in variables
- runs are recorded cleanly enough that they can be reorganized, scored, and learned from later
- Bonsai can improve variable selection over time
- Potter can later improve the bones without changing validated behavior

The guiding direction is simple:

build a machine whose behavior is increasingly learnable through variables, and whose structure is increasingly improvable through behavior-preserving changes to the bones.
