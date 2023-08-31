
module washer(r= 20,b = 6){
        difference(){
        circle(r);
        circle(b);
    }

}

module pin(x = 150,j = 15){
    linear_extrude(10){    
    washer(j);
    translate([x,0,0])
    washer(j);
    y = 10;
    translate([j/2,-y/2,0])
    square([x - j ,y]);
    }
}

module link(b = 50, l = 100){
    
    // AABB

    // A 
pin(l);
translate([0,b,0])
pin(l);

// B
translate([0,0,13])
{
rotate([0,0,90])
pin(b);
translate([l,0,0])
rotate([0,0,90])
pin(b);
}





}

link(100,50);

translate([0,100,12])
link(100,50);


module gripper_base(){
    translate([-150,0,-130])
    color("green"){


        // translate([-20,20,30])
        // rotate([0,-60,0])
        // cylinder(h = 100,r=6);
        // translate([-100,20,90])
        // rotate([0,60,0])
        // cylinder(h = 100,r=6);
        translate([-0,0,50])
        rotate([0,-60,0])
        cylinder(h = 100,r=6);
        translate([-100,-10,110])
        rotate([0,60,0])
        cylinder(h = 100,r=6);
        translate([-0,-0,30])
        rotate([0,-60,0])
        cylinder(h = 100,r=6);
        translate([-100,-10,90])
        rotate([0,60,0])
        cylinder(h = 100,r=6);

            
        translate([10,0,50]){
            translate([-10,0,0])
            cylinder(h = 60,r=10,center=true);
            cube([10,80,80],center=true);
        }
    }
}




module lift_plate(){
    
    cylinder(h=40,r=20);

    intersection(){

    cube([300,300,10],center=true);
    rotate([0,0,45])
    cube([300,300,10],center=true);
    }
    
    
    gripper_base();
    
    
    
}


// lift_plate();

