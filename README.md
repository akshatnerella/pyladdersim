# PyLadderSim

**PyLadderSim** is an educational Python library for simulating ladder logic in a programmable logic controller (PLC) environment. It includes an interactive visualization and a deterministic scan API for test and automation workflows.

## Features

- **Create Ladder Logic Circuits**: Add contacts, outputs, timers, counters, and edge-detection components.
- **Interactive Toggling**: Click contacts in the visualizer to toggle their states.
- **Real-Time Visualization**: Live, color-coded status updates for each rung and component.
- **Deterministic Scan API**: Execute one PLC scan at a time with `scan_once()`.
- **Educational Focus**: Designed to help students and developers learn PLC logic in an accessible way.

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

1. **Set up a basic rung**

```python
from pyladdersim import Contact, InvertedContact, Output, Ladder, Rung

start = Contact("Start")
stop = InvertedContact("Stop")
lamp = Output("Lamp")

rung = Rung([start, stop, lamp])
ladder = Ladder()
ladder.add_rung(rung)

print(ladder.scan_once())  # False
start.activate()
print(ladder.scan_once())  # True
```

2. **Use PLC primitives**

```python
from pyladdersim import CounterUp, RisingEdgeContact, RetentiveOutput

ons = RisingEdgeContact("ONS")
counter = CounterUp("CTU", preset=3)
latch = RetentiveOutput("LatchedLamp")

ons.activate()
if ons.evaluate():
    counter.evaluate(IN=True)

if counter.Q:
    latch.evaluate(True)
```

3. **Run continuously**

- `ladder.run(visualize=True)` starts the visual loop.
- `ladder.run(cycle_time=0.2)` changes scan period.
- Press `Q` to stop.

## Components

- **Contact**: Normally open contact.
- **InvertedContact**: Normally closed contact.
- **RisingEdgeContact / FallingEdgeContact**: One-shot edge detectors.
- **Output / RetentiveOutput**: Standard and latched output behavior.
- **Timers**: `OnDelayTimer`, `OffDelayTimer`, and `PulseTimer`.
- **Counters**: `CounterUp` and `CounterDown` with `PV`, `CV`, and `Q` fields.

## Visualization

The live visualization interface is built with `Tkinter`:
- **Transparent, Clickable Components**: Contacts are interactive.
- **Dynamic Color Coding**: Green for ON and red for OFF.
- **Simulation Control**: UI refreshes with each ladder scan.

## Example

Timer-driven output with two rungs:

```python
from pyladdersim import Contact, InvertedContact, OnDelayTimer, Output, Ladder, Rung

start_button = Contact(name="Start")
stop_button = InvertedContact(name="Stop")
timer = OnDelayTimer(name="Delay Timer", PT=3)
timer_done = Output("TimerDone")
lamp = Output(name="Lamp")

rung1 = Rung([start_button, stop_button, timer, timer_done])
rung2 = Rung([timer_done, lamp])

ladder = Ladder()
ladder.add_rung(rung1)
ladder.add_rung(rung2)

ladder.run(visualize=True)
```

## Contributing

Contributions are welcome to add features, fix bugs, and improve documentation.

## CI/CD (Auto Publish to PyPI)

This repository is configured with GitHub Actions:
- `CI`: runs tests on pull requests and pushes to `main`.
- `PR Version Bump`: when a pull request is opened/updated, it checks release labels and commits a version bump to `setup.py` directly in the PR branch.
- `Publish to PyPI`: builds and uploads the package when code is merged/pushed to `main`.

One-time setup required:
1. Create a PyPI API token (`__token__`) for your PyPI project.
2. In GitHub: `Settings -> Secrets and variables -> Actions`, add a repository secret named `PYPI_API_TOKEN`.
3. Use one release label on PRs:
   - `release:major`
   - `release:minor`
   - `release:patch`
4. If no release label is present, the workflow automatically adds `release:patch` and bumps patch version.
5. Automatic version bump commits run for same-repository PR branches; fork PRs require a maintainer to apply/version-bump after merge.

If the version already exists on PyPI, publish is skipped safely.

## License

This project is licensed under the MIT License.