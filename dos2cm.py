import math

# Take input from the user
# enter the below values from SP 6.1 pg-8-11
p = float(input("enter the max. load: "))      
fcd = float(input("enter the fcd from that table of IS 800 Pg-42: "))   
i = float(input("enter the moment of inertia: "))  
c = float(input("enter the c: "))  
area = float(input("enter the area: "))
lm = float(input("enter the length of the member: "))   # find this from truss

areareq = (p*1000)/fcd
izz = i*2*10000             
izzstar = izz/area
iyy = 2*((i*10000)+(area+(5+c)))
iyystar = iyy/area
rzz = math.sqrt(izzstar)
ryy = math.sqrt(iyystar)
klrzzstar = (0.85*lm)/rzz                               #should be less than 180/250

lamb = (250*klrzzstar**2)/((math.pi**2)*2*100000)       #no need to print this 
lambf = math.sqrt(lamb)
phi = 0.5*(1+0.49*(lambf-0.2)+lambf**2)
fcdd = 250/(1.1*(phi+(math.sqrt(phi**2-lambf**2))))
pd = (fcdd*area)/500

if p>pd :
    print("Choose a larger section")
elif p<pd :
    print("Section is suitable")
else :
    print("both are equal, so choose a larger section")
    
# Display the result
print("Area required is ", areareq)
print("moi zz is ", izz)
print("moi yy is ", iyy)
print("radius zz is ", rzz)
print("radius yy is ", ryy)
print("kl/r is ", klrzzstar)
print("lambda is ", lambf)
print("phi is ", phi)
print("fcd is ", fcdd)
print("Pd is ", pd)
