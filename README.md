# N_Body_Simulation
Pythonic brute force N body and CPP Barnes Hut algorithm

How to Use? <br>

1)  You can initialize a class object in 2 ways. <br> One in which all particles' initial velocities are zero. It comes together and goes away oscillating.<br>
And second in which all particles inital velocities are such that they spiral around the sun(yellow dot in centre). I tried to make it so that it orbits the Sun but eventually they deviate. You can set this setting by passing Revolve=True to Sun().

2) How to plot? You have two options, colors are uniform all white and sun yellow, or colors decided by mass normalization, to create a diminishing and coming together effect. First one looks better for revolving case. And colors by mass looks better in not revolving case.

3) Other option you get in plotting is converge. I vectorized converge function after a lot of thought. It merges particles if they are closer than a certain threshold in both coordinates. I added their masses, <b> took their velocity as their COM velocity and accelerations as their COM acceleration. </b> And later deleted the extra particle.



a) <b>You can initialize the number of particles by passing n in Sun(). </b>

b) Initialize G, softening, dt (time interval, smaller it is, accurate is the representation but slower) and sun's mass. <i>(By default it is done.)</i>

c) <b>You have to put the number of iterations in sun.plot(iterations)</b> It runs for this specified number of iterations.

I could have changed the sun's size too but it made the plot look like particles were entering and getting out of sun. So I didn't increase it much. 




