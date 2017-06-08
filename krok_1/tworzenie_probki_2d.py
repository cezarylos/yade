########################  
#######################
##	 BETON 
##	 pierwsza probka 
##	 material sypki

from yade import ymport
from yade.pack import *
from yade import pack
from yade import qt
from yade import plot
from yade import utils
import export
import random
import math

######################
young = 30e10
local_poisson = 0.2
frictionAngle = 0
radius_expansion = False
density_sand = 2600
################


#wymiary probki
szerokosc = 0.10
wysokosc = 0.10
glebokosc = 0.1
zageszczenie_1 = 0.46			# ile kruszywa
porowatosc_2 = 0.95			# ile cementu
################################
################################
plik_wyjsciowy = './cement_2D.txt'
plik_tymczasowy = 'plik1'

##parametry numeryczne

O.trackEnergy=True
plot_interval		= 1
damping			= 0.95
time_step	 	= 1e-6
USE_MOMENTS = False
USE_INCR_FORM = False
bending_ratio = 0.5
moment_limit = 0.2

#####################################################################################
###################  PARAMETY  DO  ZMIENIANIA #######################################
#####################################################################################
##
plik = ''

radius			= 0.000625 	#2/2000
std_dev			= 0.333


r_cement = 0.000625	# cement  !!!! promien  !!!!
c_std = 0.6
#
r_3  = 0.0015		# kruszywa
r_6  = 0.0030
r_12 = 0.0060



global Energia_Ostateczna
Enegria_Ostateczna = 1e-7


##


######################
def set_materials(moment_limit_param,use_moments):
	O.materials.append(CohFrictMat  (young=young,
					poisson=local_poisson,
					frictionAngle=radians(0),
					density=density_sand,
					isCohesive=False,
					alphaKr=bending_ratio,
					alphaKtw=bending_ratio,
					momentRotationLaw=use_moments,
					etaRoll=moment_limit,
					label='cement'))

	O.materials.append(CohFrictMat  (young=young*1,
					poisson=local_poisson,
					frictionAngle=radians(0),
					density=density_sand,
					isCohesive=False,
					alphaKr=bending_ratio,
					alphaKtw=bending_ratio,
					momentRotationLaw=use_moments,
					etaRoll=moment_limit,
					label='kruszywo'))

	O.materials.append(CohFrictMat  (young=young*100000000,
					poisson=local_poisson,
					frictionAngle=radians(0),
					density=density_sand*10000000,
					isCohesive=False,
					alphaKr=bending_ratio,
					alphaKtw=bending_ratio,
					momentRotationLaw=use_moments,
					etaRoll=moment_limit,
					label='sciana'))
#-----------------------------------------------------
# geometry
#-----------------------------------------------------
global xxx
def set_geometry():

	from yade import pack
	import itertools
	import random
	from numpy import arange
	from yade import utils


	strzal()
	walls=yade.utils.aabbWalls(
					#extrema=((0,0,0),size), # auto
					thickness=.01,
					oversizeFactor=2.0,
					material='sciana')
	wallIds_local=O.bodies.append(walls)

	return wallIds_local




##################### pierwszy strzal
def strzal():
	global dlugosc, wysokosc,glebokosc

	il = 1.11
	num = int((zageszczenie_1/(3.1415*r_3*r_3)*0.1*wysokosc*szerokosc)*il)
	print '3: '+str(num)
	sphere_cloud=pack.SpherePack()
	sphere_cloud.makeCloud(	minCorner=(-0.5*szerokosc,-0.5*wysokosc,-0.5*glebokosc),
				maxCorner=(0.5*szerokosc,0.5*wysokosc,0.5*glebokosc),
				rMean=r_3,
				rRelFuzz=std_dev,
				num=num,
				periodic=False,
				porosity=1
				)
	O.bodies.append([utils.sphere(	center,
				rad,
				material='kruszywo')
				for center,rad in sphere_cloud])

	num = int((zageszczenie_1/(3.1415*r_6*r_6)*0.2*wysokosc*szerokosc)*il)
	print '6: '+str(num)
	sphere_cloud=pack.SpherePack()
	sphere_cloud.makeCloud(	minCorner=(-0.5*szerokosc,-0.5*wysokosc,-0.5*glebokosc),
				maxCorner=(0.5*szerokosc,0.5*wysokosc,0.5*glebokosc),
				rMean=r_6,
				rRelFuzz=std_dev,
				num=num,
				periodic=False,
				porosity=1
				)
	O.bodies.append([utils.sphere(	center,
				rad,
				material='kruszywo')
				for center,rad in sphere_cloud])

	num = int((zageszczenie_1/(3.1415*r_12*r_12)*0.3*wysokosc*szerokosc)*il)
	print '12: '+str(num)
	sphere_cloud=pack.SpherePack()
	sphere_cloud.makeCloud(	minCorner=(-0.5*szerokosc,-0.5*wysokosc,-0.5*glebokosc),
				maxCorner=(0.5*szerokosc,0.5*wysokosc,0.5*glebokosc),
				rMean=r_12,
				rRelFuzz=std_dev,
				num=num,
				periodic=False,
				porosity=1
				)
	O.bodies.append([utils.sphere(	center,
				rad,
				material='kruszywo')
				for center,rad in sphere_cloud])


	for a in O.bodies:
		pos=a.state.pos
		pos[2]=0.0
		a.state.pos = pos
		if (a.material.label == 'sciana' ):
			a.state.blockedDOFs='XYZxyz'
			a.shape.color = Vector3( 0.0 ,  0.0 ,  255.0)/255.0
		else:
			a.state.blockedDOFs='XYz'
			a.shape.color = Vector3( 0.0 ,  255.0 ,  255.0)/255.0

	pole = 0
	for a in O.bodies:
		if (a.material.label == 'sciana'):
			tmp = 0
		else:
			pole = pole + 3.1415*a.shape.radius**2
	probka = wysokosc*szerokosc
	zag = pole/probka
	print "!!!!!!!!!!!!!!!!!   "+str(zageszczenie_1)+'  :  '+str(zag)



def strzal_2():
	global dlugosc, wysokosc,glebokosc
	print 'STRZAL'
	num = 100
	sphere_cloud=pack.SpherePack()
	sphere_cloud.makeCloud(	minCorner=(-0.5*szerokosc,-0.5*wysokosc,-0.5*glebokosc),
				maxCorner=(0.5*szerokosc,0.5*wysokosc,0.5*glebokosc),
				rMean=r_cement,
				rRelFuzz=c_std,
				num=num,
				periodic=False,
				porosity=1
				)
	O.bodies.append([utils.sphere(	center,
				rad,
				material='cement')
				for center,rad in sphere_cloud])


	for a in O.bodies:
		pos=a.state.pos
		pos[2]=0.0
		a.state.pos = pos
		if (a.material.label == 'sciana' ):
			a.state.blockedDOFs='XYZxyz'
			a.shape.color = Vector3( 0.0 ,  0.0 ,  255.0)/255.0
		else:
			a.state.blockedDOFs='XYz'
			if (a.material.label == 'cement' ):
				a.shape.color = Vector3( 0.0 ,  255.0 ,  0.0)/255.0




#######################  moving back spheres to the box

def rnd1(): # random value between 0 ... 1
	return random.random()

def cofaj_kulki_do_pudelka():
	global wysokosc, dlugosc
	ile_ich_ucieklo=0
	for a in O.bodies:
		if(	(a.state.pos[1] < -0.8*wysokosc) or
			(a.state.pos[0] < -0.8*szerokosc) or
			(a.state.pos[1] > 0.8*wysokosc) or
			(a.state.pos[0] > 0.8*szerokosc) ):
			# back to the box
			center2 = Vector3(szerokosc*rnd1(),wysokosc*rnd1(), 0)
			a.state.pos = center2
			ile_ich_ucieklo = ile_ich_ucieklo + 1
	return ile_ich_ucieklo


def voxelPorosityChyba(a,b,c):
	rr=Vector3(a,a,250)
	return yade.utils.voxelPorosity(rr,b,c)
###################################################
##### MAIN  PROGRAM
###################################################
global nie_koncz, czas,Energia_ostateczna
nie_koncz = False
czas = 0
def stabilizacja():
	global Enegria_Ostateczna
	global zageszczenie,czas
	czas = czas+1

	cofaj_kulki_do_pudelka()

	if (O.iter%1000 == 1):
		p=voxelPorosityChyba(250,Vector3(-0.5*szerokosc,-0.5*wysokosc,-0.0002),Vector3(0.5*szerokosc,0.5*wysokosc,0.0002))
		print 'zageszczenie:  ' +str(1-p)
	if (O.iter%100==1 and O.iter > 10000):
		p=voxelPorosityChyba(600,Vector3(-0.5*szerokosc,-0.5*wysokosc,-0.0002),Vector3(0.5*szerokosc,0.5*wysokosc,0.0002))
		if (czas > 100):
			if ((1-p) < porowatosc_2):
				strzal_2()
				czas = 0
			else:
				E_tracker	  = dict(O.energy.items())
				E_kin_translation = E_tracker['kinTrans']
				if (E_kin_translation < Enegria_Ostateczna):
					print 'zageszczenie_ostateczne:  ' + str(1-p)
					yade.export.text(plik_wyjsciowy)
					zapis_ost()
					O.pause()




def zapis_ost():
	logfile3 = open('ziarna_2D','a')
	logfile4 = open('cement_2D','a')
	logfile3.write('#format x_y_z_r')
	logfile3.write('\n')
	logfile4.write('#format x_y_z_r')
	logfile4.write('\n')
	for a in O.bodies:
		if (a.material.label != 'sciana'):
			diameter = 2*a.shape.radius
			pos_x = a.state.pos[0]
			pos_y = a.state.pos[1]
			pos_z = a.state.pos[2]
			rad = a.shape.radius
			if(a.material.label=='kruszywo'):
				logfile3.write(str(pos_x))
				logfile3.write('        ')
				logfile3.write(str(pos_y))
				logfile3.write('        ')
				logfile3.write(str(pos_z))
				logfile3.write('        ')
				logfile3.write(str(rad))
				logfile3.write('\n')
			if (a.material.label == 'cement'):
				logfile4.write(str(pos_x))
				logfile4.write('        ')
				logfile4.write(str(pos_y))
				logfile4.write('        ')
				logfile4.write(str(pos_z))
				logfile4.write('        ')
				logfile4.write(str(rad))
				logfile4.write('\n')
	logfile3.close()
	logfile4.close()

	O.pause()
######################################################################################
set_materials(moment_limit,USE_MOMENTS)

walls=set_geometry()
O.dt=time_step

### engines
global newtonIntegrator, law_local
newtonIntegrator=NewtonIntegrator(damping=damping,kinSplit=True)
law_local=Law2_ScGeom6D_CohFrictPhys_CohesionMoment(always_use_moment_law= USE_MOMENTS ,useIncrementalForm=USE_INCR_FORM)

O.engines=[
		ForceResetter(),
		InsertionSortCollider([Bo1_Sphere_Aabb(),Bo1_Box_Aabb(),Bo1_Facet_Aabb(),Bo1_Wall_Aabb()]),
		InsertionSortCollider(nBins=5,verletDist=radius*0.05),
		InteractionLoop(
			[Ig2_Sphere_Sphere_ScGeom6D(),Ig2_Box_Sphere_ScGeom6D()],
			[Ip2_CohFrictMat_CohFrictMat_CohFrictPhys()],
			[law_local]
		),
		GlobalStiffnessTimeStepper(active=1,timeStepUpdateInterval=50),
		GravityEngine(gravity=(0,0,0)),
		newtonIntegrator,
		PyRunner(iterPeriod=1,command='stabilizacja()'),
	]
####
### plot
from yade import plot





#-----------------------------------------------------
# set gui
#-----------------------------------------------------
from yade import qt
#qt.View()
qt.Controller()
O.dt=.5*utils.PWaveTimeStep()
yade.qt.controller.setWindowTitle('proba_gravitacji')
plot.liveInterval=plot_interval
#plot.plot(subPlots=False)

