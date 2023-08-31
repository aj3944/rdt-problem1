//nyu tandon - VIP - RDT
//created by aj3944 
//Task Description
//design a bot to pick up a box and place it higher than it initially was


// Bot Design
//wheels
module wheel(x,y,z,theta=0){
    translate([x,y,z])
    rotate([90,0,theta])
    cylinder(h=30,r=50,center=true);
}



//chassis
module chassis(){
    translate([-10,0,0])
    rotate([90,0,0])
    cylinder(h=600,r=10,center=true);
    translate([5,310,0])
    rotate([0,0,60])
    rotate([90,0,0])
    cylinder(h=600,r=10,center=false);
    translate([5,-310,0])
    rotate([0,0,120])
    rotate([90,0,0])
    cylinder(h=600,r=10,center=false);
}

module bodyframe(){
    translate([0,0,15])
    rotate([30,10,0])
    cylinder(h=400,r=10,center=false);
    translate([0,0,15])
    rotate([-30,10,0])
    cylinder(h=400,r=10,center=false);
    
    
    translate([0,-300,15])
    rotate([0,20,60])
    cylinder(h=1000,r=10,center=false);    


}
module bodyplate(){
    translate([170,0,180])
    cylinder(h=20,r=200,center=true);
    translate([170,0,350])
    cylinder(h=20,r=250,center=true);
    
    
    translate([173,0,900])
    sphere(70);
}


module electronics(){
    //battery
    color("blue")  
    translate([90,0,220])
    cube([60,140,40],center=true);

    color("green")  
    translate([220,0,220])
    cube([110,110,40],center=true);

}



module lift_bot(){
wheel(-20,330,0,30);
wheel(-20,-330,0,-30);
wheel(550,0,0,90);



electronics();



bodyplate();

chassis();

translate([260,160,0])
rotate([0,0,-120])
bodyframe();

translate([260,-160,0])
rotate([0,0,120])
bodyframe();
bodyframe();

}




//powertrain
module hydraulic_tank(){
    translate([380,0,80])
    hull(){  
        translate([0,-100,0])
        sphere(80);
        translate([0,100,0])
        sphere(80);
    }
}
module lift_arm(){
    
    translate([0,30,1000])
    rotate([0,0,90])
    rotate([90,0,0])
    cylinder(h = 1000, r = 12, center = true);
    translate([0,-30,1000])
    rotate([0,0,90])
    rotate([90,0,0])
    cylinder(h = 1000, r = 12, center = true);
    translate([0,30,1060])
    rotate([0,0,90])
    rotate([90,0,0])
    cylinder(h = 1000, r = 12, center = true);
    translate([0,-30,1060])
    rotate([0,0,90])
    rotate([90,0,0])
    cylinder(h = 1000, r = 12, center = true);
}
module lift_pin(x,z){
    translate([x,0,z])
    rotate([90,0,90])
    cube([110,110,20],center=true);
}   


module hydro_arm( r = 0){
        color("green")
        {
            
        cylinder(h = 300,r=40,center=true);
         translate([0,0,-120*r/100])
        cylinder(h = 300,r=20);
        }
}




module powertrain(){
    hydraulic_tank();
    lift_arm();


    translate([0,0,1120])
    rotate([0,-90,0])
    hydro_arm(10);

    lift_pin(100,1030);
    lift_pin(250,1030);
    lift_pin(490,1030);
    lift_pin(-490,1030);
    lift_pin(-390,1030);
    lift_pin(-250,1030);
    lift_pin(-90,1030);
}



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
    cube([300,300,10],center=true);
    
    
    gripper_base();
    
    
    
}


lift_plate();

// World
//box
module box(){
    color("red")
    translate([-600,-150,0])
    cube([300,300,300]);
}

box();