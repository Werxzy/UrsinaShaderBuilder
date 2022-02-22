from ursina import Vec3
# mode = 'ngon'
x_vert = [Vec3(0,1,0), Vec3(-1,2,0), Vec3(-2,1,0), Vec3(-1,0,0), Vec3(-2,-1,0), Vec3(-1,-2,0), Vec3(0,-1,0), Vec3(1,-2,0), Vec3(2,-1,0), Vec3(1,0,0), Vec3(2,1,0), Vec3(1,2,0)]
check_vert = [Vec3(-0.5,0,0), Vec3(-1.5,1,0), Vec3(-2.5,0,0), Vec3(-0.5,-2,0), Vec3(2.5,1,0), Vec3(1.5,2,0)]
down_arrow_vert = [Vec3(0,0,0), Vec3(-1,1,0), Vec3(-2,0,0), Vec3(0,-2,0), Vec3(2,0,0), Vec3(1,1,0)]
right_arrow_vert = [Vec3(0,0,0), Vec3(-1,-1,0), Vec3(0,-2,0), Vec3(2,0,0), Vec3(0,2,0), Vec3(-1,1,0)]
up_arrow_vert = [Vec3(0,0,0), Vec3(1,-1,0), Vec3(2,0,0), Vec3(0,2,0), Vec3(-2,0,0), Vec3(-1,-1,0)]
left_arrow_vert = [Vec3(0,0,0), Vec3(1,1,0), Vec3(0,2,0), Vec3(-2,0,0), Vec3(0,-2,0), Vec3(1,-1,0)]

# mode = 'triangle'
scale_arrow_vert = [Vec3(-2,2,0), Vec3(-2,-1,0), Vec3(1,2,0), 
					Vec3(1,0,0), Vec3(0,1,0), Vec3(-1,0,0), 
					Vec3(1,0,0), Vec3(-1,0,0), Vec3(0,-1,0), 
					Vec3(2,-2,0), Vec3(2,1,0), Vec3(-1,-2,0)]