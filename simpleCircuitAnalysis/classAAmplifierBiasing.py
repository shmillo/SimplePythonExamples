import numpy as np
import matplotlib.pyplot as mplt

sampleRate = 44100.0; dt = 1.0/sampleRate; m = 0.5; minv = 1.0/m; numTimeSteps = 5000
Is = 1.0e-14; Vt = 0.02585; bf = 200.0; br = 4.0; ar = (br/(1.0 + br)); af = (bf/(1.0 + bf))

gc1 = 1.0e-6 * minv * sampleRate; ic1 = 0.0
gce = 0.010e-6 * minv * sampleRate; ice = 0.0

grccp = 1.0/50000.0; grccn = 1.0/50000.0; grccc = 1.0/500000.0; gre = 1.0/100.0

viArr = []; vcArr = []; vbArr = []; veArr = []
ve = 0.0; vb = 0.0; vc = 0.0; vcc = 9.0; t = 0.0
for i in range(numTimeSteps):
    
    vi = 0.5 * np.sin(2.0 * 120.0 * np.pi * t); t += dt

    for k in range(9):

        vbe = vb - ve; vbc = vb - vc
    
        if(vbe > 0.657620385289472):
            p1 = ((Is * (np.exp(0.657620385289472/Vt) - np.exp(0.0/Vt))/(0.657620385289472 - 0.0)) * (vbe - 0.0)) + ((Is*np.exp(0.0/Vt)) - Is)
            vbe = Vt * np.log(1.0 + ((p1*vbe)/Is))
    
        if(vbc > 0.850955253299884):
            p1 = ((Is * (np.exp(0.850955253299884/Vt) - np.exp(0.0/Vt))/(0.850955253299884 - 0.0)) * (vbc - 0.0)) + ((Is*np.exp(0.0/Vt)) - Is)
            vbc = Vt * np.log(1.0 + ((p1*vbc)/Is))
    
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

    veArr.append(ve); vcArr.append(vc); viArr.append(vi); vbArr.append(vb)

mplt.plot(vcArr, label='vc'); mplt.plot(vbArr, label='vb'); mplt.plot(veArr, label='ve'); mplt.plot(viArr, label='vi')
mplt.legend()
mplt.show()

