# Simple pygame program
from bodyObject import *
# Import and initialize the pygame library
import pygame
from solarsystemData import PlanetData as PD
from MoonData import MoonData as MD
import json
from matplotlib import pyplot as plt
import numpy as np
from scipy.spatial.transform import Rotation as rot
G = 6.6743e-11

def ImportPlanetData():

    jsonToPlanetData = lambda dict:  PD(dict["Planet"],
                                        dict["Mass(10e24kg)"],
                                        dict["Radius(km)"],
                                        dict["Diameter(km)"],
                                        dict["Density(kg/m3)"],
                                        dict["Gravity(m/s2)"],
                                        dict["Escape Velocity(km/s)"],
                                        dict["Rotation Period(hours)"],
                                        dict[ "Length of Day(hours)"],
                                        dict["Distance from Sun(10e6km)"],
                                        dict["Perihelion(10e6km)"],
                                        dict["Aphelion(10e6km)"],
                                        dict["Orbital Period(days)"],
                                        dict["Orbital Velocity(km/s)"],
                                        dict["Orbital Inclination(degrees)"],
                                        dict["Orbital Eccentricity"],
                                        dict[ "Obliquity to Orbit(degrees)"],
                                        dict[ "Mean Temperature(C)"],
                                        dict["Number of Moons"],
                                        dict["Ring System?"],
                                        dict["Global Magnetic Field?"])
    #get data from Json file
    with open('planetsData.json','r') as fileread:
        filestring = fileread.read()[3::]
        PlanetsRawData: list[PD] = json.loads(filestring, object_hook=jsonToPlanetData)

    astres : list[body] = []
    astres.append(body('SUN',6.9634e5,1.989e30,vector(0,0),vector(0,0)))
    for i in PlanetsRawData:
        astres.append(body(i.planet, i.radius_km, i.mass_10_e24_kg, vector(0,i.orbital_velocity_km_s,0),  vector(i.perihelion_10_e6_km, 0, 0)))
    return astres, PlanetsRawData
    

def SolveKepler(M, e):
    Kepler_Equation = lambda M, E, e: E-(e*np.sin(E))-M
    kepler_Equation_Differentiated = lambda E,e : 1-e*np.cos(E)
    accuracy : float = 1e-10
    Maxiteration : int = 100
    E : float = e if e <= 0.8 else np.pi
    for i in range(0, Maxiteration):
        nextvalue = E-(Kepler_Equation(M,E,e)/kepler_Equation_Differentiated(E,e))
        difference = np.abs(E - nextvalue)
        E = nextvalue
        if(difference < accuracy): break

    return E

def ImportMoonData():

    jsonToMoonData = lambda dict:  MD(dict["Moon"],
                                    dict["Planet"],
                                    dict["Mass (1024kg)"], 
                                    dict["Eccentricity"], 
                                    dict["periapsis(10e6Km)"], 
                                    dict["Apoapsis(10e6Km)"], 
                                    dict["Orbital Period(days)"], 
                                    dict["Orbital Inclination deg"])
    #get data from Json file
    with open('Moons.json','r') as fileread:
        filestring = fileread.read()[3::]
        MoonsRawData: list[MD] = json.loads(filestring, object_hook=jsonToMoonData)
    return MoonsRawData
def ComputePointOrbit(Apoapsis, Periapsis, theta, inclination):
    semiMajor = (Apoapsis + Periapsis)/2.0
    semiMinor = (Apoapsis*Periapsis)**0.5
    meanAnomaly = theta % 2*np.pi
    linearEccentricity = semiMajor - Periapsis
    eccentricity = linearEccentricity/semiMajor
    eccentricAnomaly = SolveKepler(meanAnomaly, eccentricity)
    x = semiMajor * (np.cos(eccentricAnomaly) - eccentricity)
    y = semiMinor * np.sin(eccentricAnomaly)
    inclinedPlane  = rot.from_euler('y',inclination, True)
    result = inclinedPlane.apply([x,y,0])
    return vector(result[0], result[1], result[2])

def main(tmax = 7.82438e9/3, dt = 1e5):
    def GetTotalPotentialEnergy(t,x,y,z):
        E = 0
        for i in range(0,len(RawPlanetData)):
           E+= -(G*RawPlanetData[i].mass_10_e24_kg*1e24)/vector().magnitude(vector().direction(vector(x,y,z),vector(PlanetPositionsX[i][t],PlanetPositionsY[i][t],PlanetPositionsZ[i][t])))
        return E

    def GetResultantGravitationalForce(t,x,y,z):
        F = vector()
        for i in range(0,len(RawPlanetData)):
            F.x+= -(G*RawPlanetData[i].mass_10_e24_kg*1e24)/vector().magnitude(vector().direction(vector(x=x),vector(x = PlanetPositionsX[i][t])))**2
            F.y+= -(G*RawPlanetData[i].mass_10_e24_kg*1e24)/vector().magnitude(vector().direction(vector(y=y),vector(y = PlanetPositionsY[i][t])))**2
            F.z+= -(G*RawPlanetData[i].mass_10_e24_kg*1e24)/vector().magnitude(vector().direction(vector(z=z),vector(z = PlanetPositionsZ[i][t])))**2
        return F

    def GetVolumeGravitationalResultant(t=0,step = 5e8):
        Spacial_Limit_Upper = (int(max([PlanetPositionsX[-1][t],PlanetPositionsY[-1][t],PlanetPositionsZ[-1][t]])))
        Spacial_Limit_Lower = (int(min([PlanetPositionsX[-1][t],PlanetPositionsY[-1][t],PlanetPositionsZ[-1][t]])))
        #print(Spacial_Limit_Upper)
        #print(Spacial_Limit_Lower)
        counter = 0
        diff = (int((Spacial_Limit_Upper-Spacial_Limit_Lower)))
       # print(diff // step)
       # print(diff / step)
       # print(diff)
       # print(step)
        Forces = np.zeros(shape = (3,diff//int(step)))
        Points = np.zeros(shape =  (3,diff//int(step) ))
        #print(F)
        for x in range(Spacial_Limit_Lower,Spacial_Limit_Upper, int(step)):
            for y in range(Spacial_Limit_Lower,Spacial_Limit_Upper, int(step)):
                for z in range(Spacial_Limit_Lower,Spacial_Limit_Upper, int(step)):
                    F_temp = (GetResultantGravitationalForce(t,x,y,z))
                    #print(counter)
                    if counter >= len(Forces[0]): break
                    Forces[0][counter] = F_temp.x
                    Forces[1][counter] = F_temp.y
                    Forces[2][counter] = F_temp.z 
                    
                    Points[0][counter] = x
                    Points[1][counter] = y
                    Points[2][counter] = z 
                    counter += 1                 
        print(Forces)
        print("------------------------")
        print(Points)               
        return Forces[0],Forces[1],Forces[2],Points[0],Points[1],Points[2]

    N = round(tmax/dt)
    Astres, RawPlanetData = ImportPlanetData()
    RawMoonData = ImportMoonData()
    PlanetPositionsX = np.zeros(shape =(len(RawPlanetData), int(N)))
    PlanetPositionsY = np.zeros(shape =(len(RawPlanetData), int(N)))
    PlanetPositionsZ = np.zeros(shape =(len(RawPlanetData), int(N)))

    MoonPositionsX = np.zeros(shape =(len(RawMoonData), int(N)))
    MoonPositionsY = np.zeros(shape =(len(RawMoonData), int(N)))
    MoonPositionsZ = np.zeros(shape =(len(RawMoonData), int(N)))
    #RawPlanetData = RawPlanetData[2:4]
    #RawMoonData = RawMoonData[0:3]
    t = np.zeros(N)
    for j in range(0 , len(RawPlanetData)):
        print("Found Planet " + RawPlanetData[j].planet)
        CurrentEarthPos = ComputePointOrbit(RawPlanetData[j].aphelion_10_e6_km*1.0e6,RawPlanetData[j].perihelion_10_e6_km*1.0e6,0,RawPlanetData[j].orbital_inclination_degrees)
        PlanetPositionsX[j][0] = CurrentEarthPos.x
        PlanetPositionsY[j][0] = CurrentEarthPos.y
        PlanetPositionsZ[j][0] = CurrentEarthPos.z

        if (RawPlanetData[j].number_of_moons > 0 and (RawPlanetData[j].planet.upper() in [moon.planet.upper() for moon in RawMoonData])):
            for m in range(0, len(RawMoonData)):
                if(RawMoonData[m].planet.upper() == RawPlanetData[j].planet.upper()):
                    print("Moon: " + RawMoonData[m].moon)
                    CurrentMoonPosition = (ComputePointOrbit(RawMoonData[m].apoapsis_10_e6_km*1.0e6,RawMoonData[m].periapsis_10_e6_km*1.0e6,0,RawMoonData[m].orbital_inclination_deg))
                    MoonPositionsX[m][0] = CurrentMoonPosition.x 
                    MoonPositionsY[m][0] = CurrentMoonPosition.y
                    MoonPositionsZ[m][0] = CurrentMoonPosition.z
                    #print(RawMoonData[m].moon + "done for time t = " + str(t[i+1]))
        for i in range(0, N-1):
            t[i+1] = t[i] + dt 
            CurrentEarthPos = ComputePointOrbit(RawPlanetData[j].aphelion_10_e6_km*10e6,RawPlanetData[j].perihelion_10_e6_km*1.0e6,(t[i+1]/(float(RawPlanetData[j].orbital_period_days)*24*3600))*2*np.pi,RawPlanetData[j].orbital_inclination_degrees)
            PlanetPositionsY[j][i+1] = CurrentEarthPos.y
            PlanetPositionsZ[j][i+1] = CurrentEarthPos.z
            PlanetPositionsX[j][i+1] = CurrentEarthPos.x

            if (RawPlanetData[j].number_of_moons > 0 and (RawPlanetData[j].planet.upper() in [moon.planet.upper() for moon in RawMoonData])):
                for m in range(0, len(RawMoonData)):
                    if(RawMoonData[m].planet.upper() == RawPlanetData[j].planet.upper()):
                        CurrentMoonPosition = (ComputePointOrbit(RawMoonData[m].apoapsis_10_e6_km*1.0e6 ,RawMoonData[m].periapsis_10_e6_km*1.0e6 ,(t[i+1]/(float(RawMoonData[m].orbital_period_days)*24*3600))*2*np.pi,RawMoonData[m].orbital_inclination_deg))
                        MoonPositionsX[m][i+1] = CurrentMoonPosition.x
                        MoonPositionsY[m][i+1] = CurrentMoonPosition.y
                        MoonPositionsZ[m][i+1] = CurrentMoonPosition.z

                    #print(RawMoonData[m].moon + "done for time t = " + str(t[i+1]))


        

        print(RawPlanetData[j].planet + " done!" )

    np.savez("SSSave.dat",RawPlanetData,RawMoonData,PlanetPositionsX,PlanetPositionsY,PlanetPositionsZ,MoonPositionsX,MoonPositionsY,MoonPositionsZ)

                  
    fig = plt.figure()
    ax = plt.axes(111,projection = '3d')
    for i in range(0, len(RawPlanetData)):
        ax.plot(t,PlanetPositionsX[i], PlanetPositionsY[i])
    ax.set_xlabel("time/s")
    ax.set_ylabel("X")
    #ax.set_zlabel("Y")
    ax.legend([p.planet for p in RawPlanetData], loc = 'upper right')
    plt.title(" Solar system Orbit Path(X-Y VS Time) ")

    fig = plt.figure()
    ax = plt.axes()
    for i in range(0, len(RawPlanetData)):
       ax.plot(PlanetPositionsX[i],PlanetPositionsY[i])
    ax.set_ylabel("X")
    #ax.set_zlabel("Y")
    ax.legend([p.planet for p in RawPlanetData], loc = 'upper right')
    plt.title(" Solar system Orbit Path(X VS Y) ")

    fig = plt.figure()
    ax = plt.axes(111,projection = '3d')
    for i in range(0, len(RawPlanetData)):
       ax.plot(PlanetPositionsX[i],PlanetPositionsY[i],PlanetPositionsZ[i])
    ax.legend([p.planet for p in RawPlanetData], loc = 'upper left')
    ax.set_xlabel("X")
    ax.set_ylabel("Y")
    #ax.set_zlabel("Z")
    plt.title(" Solar system Orbit Path(X-Y-Z) ")

   
    for i in range(0, len(RawMoonData)):
        fig = plt.figure()
        ax = plt.axes(projection = '3d')
        ax.plot(MoonPositionsX[i],MoonPositionsY[i],MoonPositionsZ[i])
        plt.title(RawMoonData[i].moon + " Orbit Path ")
        ax.set_xlabel("X")
        ax.set_ylabel("Y")
        #ax.set_zlabel("Z")
        #ax.plot(PlanetPositionsX[i],PlanetPositionsY[i],PlanetPositionsZ[i])
    


    ax = plt.figure().add_subplot(111,projection='3d')
    # Make the direction data for the arrows
    Spacial_Limit_Upper = (int(max([PlanetPositionsX[-1][1],PlanetPositionsY[-1][1],PlanetPositionsZ[-1][1]])))
    Spacial_Limit_Lower = (int(min([PlanetPositionsX[-1][1],PlanetPositionsY[-1][1],PlanetPositionsZ[-1][1]])))
    x = []
    y = []
    z = []
    u = []
    v = []
    w = []
    print("reached here!")
    for i in np.linspace(Spacial_Limit_Lower,Spacial_Limit_Upper,10):
        for j in np.linspace(Spacial_Limit_Lower,Spacial_Limit_Upper,10):
            for k in np.linspace(Spacial_Limit_Lower,Spacial_Limit_Upper,10):
                x.append(i)
                y.append(j)
                z.append(k)
                p = vector().scale(vector().makeUnit(GetResultantGravitationalForce(1,i,j,k)),1e8)
                u.append(p.x)
                v.append(p.y)
                w.append(p.z)

    ax.quiver(x, y, z, u,v,w,length = 1)
    plt.title("Gravitational Force Vector Field(X-Y-Z) ")

    #ax.quiver(Points[0],Points[1],Points[2],u, v, w, length = 1e9 ,normalize=True)
    



    plt.show()
    print("Done!")


if __name__=="__main__":
    main()
