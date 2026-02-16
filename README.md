
# PyLadderSim

**PyLadderSim** is an educational Python library for simulating ladder logic in a programmable logic controller (PLC) environment. This project provides an interactive, visual ladder logic simulation that allows users to build and visualize ladder circuits, toggle component states, and observe the impact of changes in real time.

## Features

- **Create Ladder Logic Circuits**: Add various components like contacts, coils, timers (ON-delay, OFF-delay, pulse timers), and more.
- **Interactive Toggling**: Components are now clickable in the visualization, allowing users to toggle their states directly by clicking on them.
- **Real-Time Visualization**: The simulation includes a live visualization of ladder logic, including color-coded status updates for each component.
- **Educational Focus**: Designed to help students and enthusiasts learn ladder logic programming and PLC simulation in an intuitive and accessible way.

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/akshatnerella/pyladdersim.git
   cd pyladdersim
   ```

2. Install required dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Usage

1. **Setting up a Ladder Logic Simulation:**

   Import `pyladdersim` components and set up a simple ladder circuit:

   ```python
   from pyladdersim.components import Contact, InvertedContact, Output, OnDelayTimer
   from pyladdersim.ladder import Rung, Ladder
   from pyladdersim.visualizer import LadderVisualizer

   # Define components
   input1 = Contact(name="Start")
   input2 = InvertedContact(name="Stop")
   output = Output(name="Lamp")

   # Create a rung and add components
   rung1 = Rung([input1, input2, output])

   # Initialize the ladder and add rungs
   ladder = Ladder()
   ladder.add_rung(rung1)

   # Run the ladder with visualization
   ladder.run(visualize=True)
   ```

2. **Interacting with the Simulation:**

   - Click directly on components in the visualization to toggle their states.
   - Observe color changes: Green indicates active (ON), and red indicates inactive (OFF).
   - Press **Q** to stop the simulation.

## Components

- **Contact**: Represents a standard normally open contact.
- **Inverted Contact**: Represents a normally closed contact.
- **Output Coil**: Represents an output device.
- **Timers**: Includes ON-delay, OFF-delay, and pulse timers, each with unique timing and control logic.

## Visualization

The live visualization interface is built with `Tkinter` for an interactive, seamless UI:
- **Transparent, Clickable Components**: Each contact and coil is interactive, allowing users to click and toggle their states.
- **Dynamic Color Coding**: Components show real-time ON/OFF status, with green for active and red for inactive.
- **Simulation Control**: The interface updates continuously, showing the current state of each rung and overall circuit.

## Example

Here’s an example of a simple ladder logic with a start/stop control and a timer-based output:

```python
from pyladdersim.components import Contact, InvertedContact, Output, OnDelayTimer
from pyladdersim.ladder import Rung, Ladder
from pyladdersim.visualizer import LadderVisualizer

# Define components
start_button = Contact(name="Start")
stop_button = InvertedContact(name="Stop")
timer = OnDelayTimer(name="Delay Timer", PT=3)  # Timer with preset time
lamp = Output(name="Lamp")

# Create rungs
rung1 = Rung([start_button, stop_button, timer])
rung2 = Rung([timer, lamp])

# Initialize ladder
ladder = Ladder()
ladder.add_rung(rung1)
ladder.add_rung(rung2)

# Run the ladder with visualization
ladder.run(visualize=True)
```

## Contributing

We welcome contributions to add new features, fix bugs, and improve documentation. To contribute, fork the repository, make your changes, and open a pull request.

## CI/CD (Auto Publish to PyPI)

This repository is configured with GitHub Actions:
- `CI`: runs tests on pull requests and pushes to `main`.
- `Auto Version Release`: on each merge/push to `main`, it auto-bumps version in `setup.py`, creates a git tag (for example `v0.1.1`), and pushes it.
- `Publish to PyPI`: builds and uploads the package when a release tag is pushed.

One-time setup required:
1. Create a PyPI API token (`__token__`) for your PyPI project.
2. In GitHub: `Settings -> Secrets and variables -> Actions`, add a repository secret named `PYPI_API_TOKEN`.
3. Use conventional commit messages in merged commits/PR titles for semantic bumps:
   - `feat:` -> minor bump
   - `fix:` (or anything else) -> patch bump
   - `BREAKING CHANGE` or `feat!:` / `fix!:` -> major bump

If the version already exists on PyPI, publish is skipped safely.

## License

This project is licensed under the MIT License.

---

Enjoy exploring ladder logic with PyLadderSim! For any questions, feel free to reach out or open an issue.

