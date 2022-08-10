// testing OpenSCAD scripting

color("gray") {
  linear_extrude(height = 40, twist = 360, slices = 100) {
    square(20, center = true);
  }
}

color("blue") {
  translate([0, 40, 20]) {
    cylinder(d = 20 * sqrt(2), h = 40, center = true);
  }
}
