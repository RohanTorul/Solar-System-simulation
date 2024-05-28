class vector:
    def __init__(self, x=0, y=0, z = 0) -> None:
        self.x = x
        self.y = y
        self.z = z
    def add(self,a,b):
        return vector(a.x+b.x,a.y+b.y, a.z + b.z)
    def scale(self,a, s):
        return vector(a.x*s,a.y*s, a.z*s)
    def magnitude(self,a):
        return (a.x**2 + a.y**2 + a.z**2)**0.5
    def makeUnit(s,a):
        return(s.scale(a,1/s.magnitude(a)))
    def unitDirection(s,a,b):
        vec = s.add(a,s.scale(b,-1))
        return s.makeUnit(vec)
    def direction(s,a,b):
        vec = s.add(a,s.scale(b,-1))
        return vec
    def distance(s,a,b):
        return s.magnitude(s.add(a,s.scale(b,-1)))
    def dotProduct(s,a,b):
        return (a.x*b.x+a.y*b.y + a.z*b.z)
    def crossproduct(s,a,b):
        return vector((a.y*b.z - b.y*a.z), (a.x*b.z - b.x*a.z),(a.x*b.y-b.x*a.y))
    

    def centre(self, target, anchor):
        return vector(target.x + anchor.x, target.y + anchor.y, target.z + anchor.z)
    
class body:
    def __init__(self,name = 'untitled',radius = 63.78,mass = 5.97*(10**16),velocity = vector(0,0), position = vector(0,0)) -> None:
        self.name = name
        self.radius = radius
        self.mass = mass
        self.velocity = velocity
        self.position = position
    def Iscollide(s,other):
        return vector.magnitude(vector.Direction(s.position,other.position)) <= s.radius + other.radius
    
class Solsystem:
    def __init__(self, bodies:list[body] = [body()]) -> None:
        self.bodies = bodies
        self.dt = 1/(10**3)
        self.G = 6.67430e-11
    
    def getGravForce(s,a:body, b:body) -> vector:
        return (s.G * a.mass * b. mass)/vector.distance(vector(0,0),a.position,b.position)

    def getAcceleration(s, a:body, b:body):
        mag= (s.G * b. mass)/vector().distance(a.position,b.position)
        direction = vector.unitDirection(vector(0,0),a.position,b.position)
        return(vector().scale(direction,-1*mag))


    def update(self, ):

        for i in self.bodies:
            for x in self.bodies:
                if x != i:
                    i.velocity = vector().add(i.velocity,self.getAcceleration(i,x))
                    test = vector().add(i.position,i.velocity)
                    if not( vector().distance(test,x.position) < (i.radius + x.radius)):i.position = vector().add(i.position,i.velocity)

                    
                    