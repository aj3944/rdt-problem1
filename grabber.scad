
module washer(r= 20,b = 6){
        difference(){
        circle(r);
        circle(b);
    }

}

module pin(x = 150,j = 15){
    rotate([0,-90,0])
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
//pin(200);

//link(100,50);

//translate([0,100,12])
//link(100,50);
module suckerplate(){
        color("white")
        rotate([0,90,0])
        {
            for(i = [-1:1]){
                for(j = [-1:1]){
                    translate([30*j,30*i,3])
                    cylinder(h=10,r1=1,r2=12);
                }
            }
    }
}
module suckercup(r){
    rotate([0,0,90])
    {
        translate([-10,0,0])
        cylinder(h = 60,r=10,center=true);
        cube([10,80,80],center=true);
        suckerplate();
    }    
}





module gripper_base(){
    //translate([-150,0,-130])
    translate([-10,-100,-0])
    {


        // translate([-20,20,30])
        // rotate([0,-60,0])
        // cylinder(h = 100,r=6);
        // translate([-100,20,90])
        // rotate([0,60,0])
        // cylinder(h = 100,r=6);
        cx = 0;
        cy = 0;
        cz = 0;

        r = 0;

        l100 = 100;
        l150 = 100;
        l200 = 100;

        ltheta = 28;

        r1 = ltheta;
        cx1 = 0;
        cy1 = cy + l200*cos(r1);
        cz1 = cz + l200*sin(r1);

        translate([cx,cy,cz])
        rotate([90 + r1,0,0])
        // cylinder(h = l200,r=10);
        {
        pin(l200);
        translate([20,0,0])
        pin(l200);
        color("red"){
            translate([30,0,0])
            rotate([-0,-90,0])
            cylinder(h=60,r=6);
        }
        }


        r2 = r1  + ltheta  ;
        cx2 = 0;
        cy2 = cy1 + l150*cos(r2);
        cz2 = cz1 + l150*sin(r2);


        translate([0,-cy1,-cz1])
        rotate([90 + r2,00,0])
        {
        pin(l150);
        translate([20,0,0])
        pin(l150);
        color("red"){
            translate([30,0,0])
            rotate([-0,-90,0])
            cylinder(h=60,r=6);
        }        }


        r3 = r2 + ltheta;
        cy3 = cy2 + l150*cos(r3);
        cz3 = cz2 + l150*sin(r3);

        translate([0,-cy2,-cz2])
        rotate([90 + r3,00,0])
        {
        pin(l150);
        translate([20,0,0])
        pin(l150);
        color("red"){
            translate([30,0,0])
            rotate([-0,-90,0])
            cylinder(h=60,r=6);
        }        }


        r4 = r3 + ltheta;
        cy4 = cy3 + l100*cos(r4);
        cz4 = cz3 + l100*sin(r4);

        translate([0,-cy3,-cz3])
        rotate([90 + r4,00,0])
        {
        pin(l100);
        translate([20,0,0])
        pin(l100);
        color("red"){
            translate([30,0,0])
            rotate([-0,-90,0])
            cylinder(h=60,r=6);
        }        }


        translate([0,-cy4,-cz4])
{
        color("red"){
            translate([30,0,0])
            rotate([-0,-90,0])
         
            cylinder(h=60,r=6);
        }
        translate([0,15,0])
            suckercup(r4);
    }
    }
}


module muiltigrip(){

    // gripper_base();
    for( i = [45:90:360]){
        rotate([0,0,i])
        gripper_base();
    }
    
}

module lift_plate(){
    
    cylinder(h=40,r=20);

    difference(){

    intersection(){

    cube([300,300,10],center=true);
    rotate([0,0,45])
    cube([300,300,10],center=true);
    }
    
    muiltigrip();
    }
    
}

// gripper_base();
// lift_plate();
// muiltigrip();

