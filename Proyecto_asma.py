"""
Proyecto: Modelado y control del sistema respiratorio

Departamento de Ingeniería Eléctrica y Electrónica, Ingeniería Biomédica
Tecnológico Nacional de México [TecNM - Tijuana]
Blvd. Alberto Limón Padilla s/n, C.P. 22454, Tijuana, B.C., México

Nombre del alumno: Emiliano Villalobos García
Número de control: 23212243
Correo institucional: l23212243@tectijuana.edu.mx

Asignatura: Modelado de Sistemas Fisiológicos
Docente: Dr. Paul Antonio Valle Trujillo; paul.valle@tectijuana.edu.mx
"""
# Instalar librerias en consola
# pip install numpy control matplotlib

#Librerias
import numpy as np
import control as ctrl 
import matplotlib.pyplot as plt

#Datos generales de la simulacion
x0,t0,tend,dt,w,h = 0,0,20,1e-3,10,5
N = round(tend/dt)+1
t = np.linspace (t0,tend,N)
u = np.zeros(N); u[:round(0.5/dt)] = 1
u[round(10/dt):round(10.5/dt)] = 1

def respiratorio(L,R1,C1,R3,R2,C2):
    num = [R2*C2,1]
    den = [L*R2*C1*C2,R1*R2*C1*C2+L*(C1+(1+R2/R3)*C2),R1*C1+(R1*R2/R3+R1+R2)*C2+L/R3,1+R1/R3]
    sys = ctrl.tf(num,den)
    L = np.roots(den)
    return sys,L

#Función de transferencia: Control
L,R1,C1,R3,R2,C2 = 10e-6,10,1e-6,1000,100,1e-6
sysctrl, L = respiratorio(L,R1,C1,R3,R2,C2)
print(f'Función de transferencia del control: {sysctrl}')
print(f"Polos del sistema: {L}\n")

#Función de transferencia: Caso
L,R1,C1,R3,R2,C2 = 10e-6,30,1e-6,100,100,0.1e-6
syscaso, L = respiratorio(L,R1,C1,R3,R2,C2)
print(f'Función de transferencia del caso: {syscaso}')
print(f"Polos del sistema: {L}\n")

# Respuestas en lazo abierto
_,Fsx = ctrl.forced_response(sysctrl,t,u,x0)
_,Fsy = ctrl.forced_response(syscaso,t,u,x0)

def controlador(kP,kI,kD,sys):
    Nf = 23788.0653667222
    numPID = [kP+kD*Nf,kP*Nf+kI,kI*Nf]
    denPID = [1,Nf,0]
    PID = ctrl.tf(numPID,denPID)
    sysPID = ctrl.feedback(ctrl.series(PID,sys),1,sign=-1)
    return sysPID

casoPID = controlador(0.703106505048227,25112.1670097634,-4.39908221517028e-6,syscaso)
print(f'Función de transferencia del caso en lazo cerrado: {casoPID}')

# Respuesta del sistema de control en lazo cerrado
_,PIDy = ctrl.forced_response(casoPID,t,Fsx,x0)

clr1 = np.array([46, 41, 16])/255
clr2 = np.array([44, 87, 69])/255
clr3 = np.array([235, 227, 167])/255
clr4 = np.array([166, 77, 55])/255

fg = plt.figure()
fg.set_size_inches(w,h)
plt.rcParams['font.size'] = 11
plt.rcParams['font.family'] = 'serif'
plt.rcParams['font.serif'] = ['Times New Roman']
plt.plot(t,u,'-',color=clr4,label='Ve(t)')
plt.plot(t,Fsx,'--',linewidth=2,color=clr1,label='Vs(t): Control')
plt.plot(t,PIDy,'-',linewidth=1,color=clr3,label='Vs(t): Caso PID')
plt.plot(t,Fsy,'--',color=clr2,label='Vs(t): Caso')
plt.xlim(0,tend); plt.xticks(np.arange(0,21,2))
plt.ylim(-0.1,1.1); plt.yticks(np.arange(-0.1,1.2,0.1))
plt.xlabel('t [s]')
plt.ylabel('Vs(t) [V]')
plt.grid(True,alpha=0.4)
plt.legend(bbox_to_anchor=(0.5,-0.20),loc='center',ncol=2,frameon=False)
fg.tight_layout()
fg.savefig('caso_python.pdf',bbox_inches='tight')
plt.show()
