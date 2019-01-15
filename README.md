# yaxb_calc
Polar wall plotter calculation and analysis tools.

These tools allow users to simulate the result of changing polar wall plotter workspace and machine parameters.

## yaxb_simulate
Detemrine the optimal canvas location in a workspace.
![yaxb_simulate](images/yaxb_simulate.png?raw=true "yaxb_simulate")
* Green -> valid belt tension locations
* Red -> belt tension above maximum (motors will overtorque in this region)
* Blue -> horizontal component of belt tension below minimum (gondola will oscillate in this region due to poor horizontal constraint)
* Black border -> tallest valid tension region that is of the specified canvas width

## yaxb_movement
Determine the cartesian path through the field of polar positions.
![yaxb_movement](images/yaxb_movement.png?raw=true "yaxb_movement")
* Green -> valid belt tension locations
* Red -> belt tension above maximum (motors will overtorque in this region)
* Blue -> horizontal component of belt tension below minimum (gondola will oscillate in this region due to poor horizontal constraint)
* Teal -> positions considered when making the movement
* Purple -> positions considered and chosen when making the movement