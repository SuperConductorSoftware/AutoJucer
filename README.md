# AutoJucer
Python script for converting figma produced SVG files into C++ JUCE framework source code

[Watch the tutorial here!](https://www.youtube.com/watch?v=jJwLIg3-0Sw)

## Getting Started

- Make some stuff in a new Figma project
- Export to SVG with "include id attribute" turned on
- Run the script from the OpenProject.py entry point to create a .json file that points to your SVG file folder and your C++ source folder
- Run the script on the .json to process the svg into C++ code

## Layer Tag System

Double colon (::) indicates a tag for the Figma group of graphical elements, the script will interpret these tags and change behaviour accordingly:

::component #[ComponentName] - Used with a rectangle drawn, this indicates a space for a child component in the code composition

::scales #[linear/centre/bounds] - Sets a scale type for the graphical elements. By default elements will draw to exact pixel locations, the scale tags change this to draw elements in relation to the bounds of the parent component

::state #[graphical state] - adds object as a drawable graphic state and function within the cpp file, useful for buttons or elements with multiple graphical states

::blendmode #[blendmode]:[blendcolourhash] - modifies colours of all objects in the  group by the blendmode / blendcolourhash interaction given

## Missing Features / Features currently in progress

- Gradients currently not implemented
- Paint code unoptimised
- Plans to expand export to other frameworks like iPlug2

## Dependencies

Python 3.8
NumPy
svg.path
xml.dom
tkinter
PIL
blend_modes

