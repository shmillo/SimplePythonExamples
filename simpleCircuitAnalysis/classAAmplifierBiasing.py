import numpy as np
import matplotlib.pyplot as mplt

sampleRate = 44100.0; dt = 1.0/sampleRate; m = 0.85; minv = 1.0/m; numTimeSteps = 5000
Is = 1.0e-14; Vt = 0.02585; bf = 200.0; br = 3.0; ar = (br/(1.0 + br)); af = (bf/(1.0 + bf))

gc1 = 4.7e-7 * minv * sampleRate; ic1 = 0.12882646511953683
gce = 1.0e-6 * minv * sampleRate; ice = 0.15440781646147314

grccp = 1.0/15000.0; grccn = 1.0/50000.0; grccc = 1.0/680.0; gre = 1.0/680.0

viArr = []; vcArr = []; vbArr = []; veArr = []; vbeArr = []; vbcArr = []
ve = 4.452095660161452; vb = 5.289522393528046; vc = 4.644175153446648; vcc = 9.0; t = 0.0
for i in range(numTimeSteps):
    
    vi = 0.65 * np.sin(2.0 * 1000.0 * np.pi * t); t += dt

    for k in range(9):

        vbe = vb - ve; vbc = vb - vc
    
        vbep = 0.652; vben = -1000.650
        if(vbe > vbep):
            p1 = ((Is * (np.exp(vbep/Vt) - np.exp(vben/Vt))/(vbep - vben)) * (vbe - vben)) + ((Is*np.exp(vben/Vt)) - Is)
            vbe = Vt * np.log(1.0 + (p1/Is))
    
        vbcp = 0.611; vbcn = -10.0
        if(vbc > vbcp):
            p1 = ((Is * (np.exp(vbcp/Vt) - np.exp(vbcn/Vt))/(vbcp - vbcn)) * (vbc - vbcn)) + ((Is*np.exp(vbcn/Vt)) - Is)
            vbc = Vt * np.log(1.0 + (p1/Is))

        evbe = np.exp(vbe/Vt); evbc = np.exp(vbc/Vt)
    
        gcc = -(-(Is/Vt)*evbc); gec = ar*(Is/Vt)*evbc
        gee = -(-(Is/Vt)*evbe); gce = af*(Is/Vt)*evbe

        ie = -Is*evbe + Is + ar*Is*evbc - ar*Is
        ic = af*Is*evbe - af*Is - Is*evbc + Is
    
        Ie = ie + gee*vbe - gec*vbc
        Ic = ic - gce*vbe + gcc*vbc
 
        vb = (Ic + Ie + ic1 + gc1*vi + grccp*vcc + (gce*(Ie - ice + (gec*(Ic - grccc*vcc))/(gcc + grccc)))/(gce + gee + gre - (gce*gec)/(gcc + grccc)) - (gee*(Ie - ice + (gec*(Ic - grccc*vcc))/(gcc + grccc)))/(gce + gee + gre - (gce*gec)/(gcc + grccc)) - (gcc*(Ic - grccc*vcc + (gce*(Ie - ice))/(gce + gee + gre)))/(gcc + grccc - (gce*gec)/(gce + gee + gre)) + (gec*(Ic - grccc*vcc + (gce*(Ie - ice))/(gce + gee + gre)))/(gcc + grccc - (gce*gec)/(gce + gee + gre)))/(gc1 + grccn + grccp - gcc*((gcc - gce*((gec - gee)/(gce + gee + gre) + 1))/(gcc + grccc - (gce*gec)/(gce + gee + gre)) - 1) + gec*((gcc - gce*((gec - gee)/(gce + gee + gre) + 1))/(gcc + grccc - (gce*gec)/(gce + gee + gre)) - 1) + gce*((gee + gec*((gcc - gce)/(gcc + grccc) - 1))/(gce + gee + gre - (gce*gec)/(gcc + grccc)) - 1) - gee*((gee + gec*((gcc - gce)/(gcc + grccc) - 1))/(gce + gee + gre - (gce*gec)/(gcc + grccc)) - 1))
        ve = -(Ie - ice - gee*vb + gec*(vb + (Ic - gcc*vb + gce*vb - grccc*vcc)/(gcc + grccc)))/(gce + gee + gre - (gce*gec)/(gcc + grccc))
        vc = -(Ic - gcc*vb - grccc*vcc + gce*(vb - ve))/(gcc + grccc)

    ic1 = ic1 + (minv * ((gc1*(vb - vi)) - ic1))
    ice = ice + (minv * ((gce*(ve - 0.0)) - ice))

    vbeArr.append(vbe); vbcArr.append(vbc); veArr.append(ve); vcArr.append(vc); viArr.append(vi); vbArr.append(vb)

print(vb, vc, ve, ic1, ice)

mplt.plot(vbArr, label='vb'); mplt.plot(veArr, label='ve'); mplt.plot(viArr, label='vi'); 
mplt.ylim([-1.0, 9.0]); mplt.legend()

mplt.figure()
mplt.plot(vcArr, label='vc'); mplt.plot(vbcArr, label='vbc'); mplt.plot(vbeArr, label='vbe')
mplt.ylim([-1.0, 9.0]); mplt.legend()

mplt.show()

