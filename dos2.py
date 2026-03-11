import math

# Take input from the user
# enter the below values from SP 6.1 pg-8-11
area = float(input("enter the area: "))
r = float(input("enter the radius: "))
rvv = float(input("enter the rvv: "))
l = float(input("enter the length: "))
t = float(input("enter the thickness: "))
lm = float(input("enter the length of the member: "))   # find this from truss
p = float(input("enter the max. load: "))               # finf this from load table

# these formulae are from IS 800:2007 pg-48
lvv = (lm/rvv)/88.86
lp = (l/t)/88.86
lamb = 0.7+(0.6*lvv**2)+(5*lp)
# Calculate square root
le = math.sqrt(lamb)
phi = 0.5*(1+0.49*(le-0.2)+le**2)
fcdd = phi+(phi**2-le**2)
fcd = 250/(1.1*fcdd)
pd = (fcd*area)/1000

# load assessment
if p>pd :
    print("Choose a larger section")
elif p<pd :
    print("Section is suitable")
else :
    print("both are equal, so choose a larger section")
    
# Display the result
print("lambda vv is ", lvv)
print("lambda phi is ", lp)
print("lambda e is ", le)
print("phi is ", phi)
print("fcd is ", fcd)
print("Pd is ", pd)
