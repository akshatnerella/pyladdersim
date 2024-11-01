# PyLadderSim

**PyLadderSim** is an open-source Python package designed for simulating ladder logic in an interactive and educational environment. Ideal for learning about programmable logic controllers (PLCs), ladder diagrams, and control systems, this tool offers a visual representation of ladder logic with real-time updates.

## Features
- **Ladder Logic Visualization**: Live graphical simulation of ladder diagrams with contacts, coils, and customizable rungs.
- **Real-Time State Updates**: Components change color based on state (`ON`/`OFF`) using a bright green (`ON`) and red (`OFF`) color scheme.
- **Interactive GUI**: Developed using Tkinter, offering a user-friendly visualization that can be closed by pressing "Q."
- **Extensible**: Add custom components or modify existing functionality to suit your project needs.

## Getting Started

### Prerequisites
- **Python 3.7+**
- **Tkinter** (usually included with Python)
- **Clone the Repository**:
  ```bash
  git clone https://github.com/YourUsername/PyLadderSim.git
  cd PyLadderSim
  ```

### Installation
To install the dependencies:
```bash
pip install -r requirements.txt
```
(*Note*: If additional libraries are added in the future, they should be added to `requirements.txt`.)

## Usage

### Setup and Run the Simulation

1. **Define Components**: `Contact`, `InvertedContact`, and `Output` components can be defined in your script.
2. **Create Rungs and Add to Ladder**:
   - Components are assembled into `Rung` objects.
   - Each `Rung` is then added to a `Ladder` object.

3. **Visualize the Ladder**:
   ```python
   from pyladdersim.components import Contact, InvertedContact, Output
   from pyladdersim.ladder import Ladder, Rung
   from pyladdersim.visualize_ladder import LadderVisualizer

   def setup_ladder():
       ladder = Ladder()

       # Example components for the first rung
       input1 = Contact("StartSwitch")
       input2 = InvertedContact("StopSwitch")
       output1 = Output("OutputLight")

       # Assemble the rung and add it to the ladder
       rung1 = Rung([input1, input2, output1])
       ladder.add_rung(rung1)

       return ladder

   if __name__ == "__main__":
       ladder = setup_ladder()
       visualizer = LadderVisualizer(ladder)
       visualizer.run()
   ```

### Controls
- **Press "Q"** to close the simulation window.

### Visualization Details
- **Contact**: A horizontal line symbol with labels that turns green when active.
- **Inverted Contact**: Similar to Contact, with a slash indicating its "normally closed" state.
- **Coil (Output)**: Circle representing an output device; fills green when active.

## Project Structure

```plaintext
PyLadderSim/
├── pyladdersim/
│   ├── components.py         # Contains Contact, InvertedContact, and Output component classes
│   ├── ladder.py             # Core ladder logic with Rung and Ladder classes
│   ├── visualize_shapes.py   # Shape drawing utilities for each ladder component
│   ├── visualize_ladder.py   # Main visualization setup and management
├── tests/
│   ├── test_ladder.py        # Basic tests for ladder logic functionality
├── README.md                 # Project README file
├── requirements.txt          # Python dependencies
```

## Contributing
Contributions are welcome! Here’s how you can help:

1. **Fork the Repository**: Click on `Fork` at the top right of the repository page.
2. **Clone Your Forked Repo**:
   ```bash
   git clone https://github.com/YourUsername/PyLadderSim.git
   ```
3. **Create a Feature Branch**:
   ```bash
   git checkout -b feature-name
   ```
4. **Commit Your Changes**: Write clear commit messages.
5. **Push to GitHub**:
   ```bash
   git push origin feature-name
   ```
6. **Submit a Pull Request**: Go to the original repository and create a pull request.

## Roadmap
- **Additional Components**: Adding specialized contacts, timers, and counters.
- **Advanced Visualization**: Support for live data feeds and interactive input toggling.
- **Export Functionality**: Export ladder diagrams to image files or PDFs.

## License
This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.