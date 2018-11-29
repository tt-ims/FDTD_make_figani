import numpy                as np
import matplotlib.pyplot    as pl
import matplotlib.ticker    as pt
import matplotlib.animation as an
import time                 as ti
import sys                  as sy
#set default plot
pl.rcParams['xtick.direction']   = 'in'
pl.rcParams['ytick.direction']   = 'in'
pl.rcParams['xtick.major.width'] = 2.0
pl.rcParams['ytick.major.width'] = 2.0
pl.rcParams['axes.linewidth']    = 2.0
#initialize calculation time
print('Now, making files...')
start_time=ti.time()
###############################################################################
#define function###############################################################
###############################################################################
def init_1d_list(num):
    var=[]
    for i in range(num):
        var.append(0)
    return var
def set_figenv1(var1,var2,var3,var4,var5,var6):
    pl.grid(which='major',color='gray',linestyle='--')
    pl.grid(which='minor',color='gray',linestyle='--')
    pl.xlim(var2); pl.ylim(var3);
    pl.xlabel(var5, fontsize=20); pl.ylabel(var6, fontsize=20);
    pl.title(var4, fontsize=20);  pl.tick_params(labelsize=20);
    pl.legend(fontsize=20,shadow=True,fancybox=True)
    var1.yaxis.set_major_formatter(pt.ScalarFormatter(useMathText=True)) 
    var1.yaxis.offsetText.set_fontsize(20)
    var1.ticklabel_format(style='sci',axis='y',scilimits=(0,0))
    var1.xaxis.set_major_formatter(pt.ScalarFormatter(useMathText=True)) 
    var1.xaxis.offsetText.set_fontsize(20)
    var1.ticklabel_format(style='sci',axis='x',scilimits=(0,0))
    return var1
def set_figenv2(var1,var2,var3,var4,var5,var6):
    pl.axis('scaled')
    pl.xlim(var2); pl.ylim(var3);
    pl.xlabel(var5, fontsize=20); pl.ylabel(var6, fontsize=20);
    pl.title(var4, fontsize=20);  pl.tick_params(labelsize=20);
    var1.yaxis.set_major_formatter(pt.ScalarFormatter(useMathText=True)) 
    var1.yaxis.offsetText.set_fontsize(20)
    var1.ticklabel_format(style='sci',axis='y',scilimits=(0,0))
    var1.xaxis.set_major_formatter(pt.ScalarFormatter(useMathText=True)) 
    var1.xaxis.offsetText.set_fontsize(20)
    var1.ticklabel_format(style='sci',axis='x',scilimits=(0,0))
    return var1
###############################################################################
#load input file and observation information###################################
###############################################################################
#initialize variables
dir_name='./'; make_ani='n'; 
obs_ani='none'; var_ani='none'; com_ani='none'; pla_ani='none';
frame_speed_ani=5e1;
e_min_fig='none'; e_max_fig='none'; h_min_fig='none'; h_max_fig='none'; 
e_min_ani='none'; e_max_ani='none'; h_min_ani='none'; h_max_ani='none';
x_min_ani='none'; x_max_ani='none';
y_min_ani='none'; y_max_ani='none';
z_min_ani='none'; z_max_ani='none';
unit_system  = 'none'; iperiodic=0; dt_em=0; nt_em=0;
al_em=0, 0, 0; dl_em=0, 0, 0; lg_sta=0, 0, 0; lg_end=0, 0, 0;
iobs_num_em=0; iobs_samp_em=0; e_max=0; h_max=0;
#load input file
f = open('figani.inp')
tmp_inp = f.readlines()
f.close()
for i in range(len(tmp_inp)):
    if tmp_inp[i].count('dir_name')==0: tmp_inp[i]=tmp_inp[i].replace('d', 'e')
tmp_inp = [s.replace('frame_speee_ani', 'frame_speed_ani') for s in tmp_inp]
for i in range(len(tmp_inp)):
    exec(tmp_inp[i])
del tmp_inp, i
#load obs0_info.data
f = open(dir_name+'/obs0_info.data')
tmp_inp = f.readlines()
f.close()
tmp_inp = [s.replace('au', '\'au\'') for s in tmp_inp]
tmp_inp = [s.replace('a.u.', '\'a.u.\'') for s in tmp_inp]
tmp_inp = [s.replace('A_eV_fs', '\'A_eV_fs\'') for s in tmp_inp]
for i in range(len(tmp_inp)):
    exec(tmp_inp[i])
del tmp_inp, i
al_em=list(al_em); dl_em=list(dl_em); lg_sta=list(lg_sta); lg_end=list(lg_end);
#set data number
nt=int(nt_em/iobs_samp_em)
###############################################################################
#prepare making files##########################################################
###############################################################################
#set adjust lg
lg_adj=init_1d_list(3)
for i in range(3):
    if lg_sta[i]<=0:
        lg_adj[i]=-lg_sta[i]
        lg_end[i]=lg_end[i]+lg_adj[i]+1;
    elif iperiodic==3: lg_adj[i]=-1;
del i
#prepare figure
t_axis=np.zeros(nt)
ex=np.zeros((iobs_num_em,nt))
ey=np.zeros((iobs_num_em,nt))
ez=np.zeros((iobs_num_em,nt))
hx=np.zeros((iobs_num_em,nt))
hy=np.zeros((iobs_num_em,nt))
hz=np.zeros((iobs_num_em,nt))
#prepare axis name
if unit_system=='au' or unit_system=='a.u.':
    name_l='a.u.'; name_e='a.u.'; name_h='a.u.'; name_t='a.u.';
elif unit_system=='A_eV_fs':
    name_l='Ang.'; name_e='V/Ang.'; name_h='A/Ang.'; name_t='fs';
#set spatial range
r_min=init_1d_list(3);
for i in range(3):
    if iperiodic==0:
        r_min[i]=-lg_end[i]*dl_em[i]/2;
    elif iperiodic==3:
        r_min[i]=0;
del i
#set spatial axis(+1 is introduced for pcolorfast)
x1d=np.zeros(lg_end[0]+1)
y1d=np.zeros(lg_end[1]+1);
z1d=np.zeros(lg_end[2]+1);
for i in range(lg_end[0]+1):
    x1d[i]=r_min[0]+i*dl_em[0]
for i in range(lg_end[1]+1):
    y1d[i]=r_min[1]+i*dl_em[1]
for i in range(lg_end[2]+1):
    z1d[i]=r_min[2]+i*dl_em[2]
del i
x_xy, y_xy=np.meshgrid(x1d,y1d);
y_yz, z_yz=np.meshgrid(y1d,z1d);
x_xz, z_xz=np.meshgrid(x1d,z1d);
#modify axis range
if e_min_fig=='none': e_min_fig=-e_max
if e_max_fig=='none': e_max_fig= e_max
if h_min_fig=='none': h_min_fig=-h_max
if h_max_fig=='none': h_max_fig= h_max
if e_min_ani=='none': e_min_ani=-e_max
if e_max_ani=='none': e_max_ani= e_max
if h_min_ani=='none': h_min_ani=-h_max
if h_max_ani=='none': h_max_ani= h_max
if x_min_ani=='none': x_min_ani= min(x1d)
if x_max_ani=='none': x_max_ani= max(x1d)
if y_min_ani=='none': y_min_ani= min(y1d)
if y_max_ani=='none': y_max_ani= max(y1d)
if z_min_ani=='none': z_min_ani= min(z1d)
if z_max_ani=='none': z_max_ani= max(z1d)
###############################################################################
#make figure files#############################################################
###############################################################################
#load and make figure data
for i in range(iobs_num_em): 
    #load
    f = open(dir_name+'/obs'+str(i+1)+'_at_point.data') #+1 for consistency.
    tmp_inp = f.readlines()
    f.close()
    tmp_inp = [s.replace('\n','') for s in tmp_inp]
    for j in range(nt): 
        tmp_inp2=tmp_inp[j+1] #+1 for consistency.
        tmp_inp2=tmp_inp2.split()
        if i==0:
            t_axis[j]=tmp_inp2[0]
        ex[i,j]=tmp_inp2[1]; ey[i,j]=tmp_inp2[2]; ez[i,j]=tmp_inp2[3];
        hx[i,j]=tmp_inp2[4]; hy[i,j]=tmp_inp2[5]; hz[i,j]=tmp_inp2[6];
    #make e
    pl.close(2*i+1) 
    fig, ax=pl.subplots(num=(2*i+1),figsize=(12,8))
    ax.plot(t_axis,ex[i,:],label='Ex',linestyle='solid' ,linewidth=3,color='b')
    ax.plot(t_axis,ey[i,:],label='Ey',linestyle='dashed',linewidth=3,color='r')
    ax.plot(t_axis,ez[i,:],label='Ez',linestyle='dotted',linewidth=3,color='g')
    set_figenv1(ax,[0,max(t_axis)],[e_min_fig,e_max_fig],\
                'obs'+str(i+1)+' E at point',name_t,name_e)
    pl.savefig('obs'+str(i+1)+'_E_at_point.jpg')
    #make h
    pl.close(2*(i+1)) 
    fig, ax=pl.subplots(num=(2*(i+1)),figsize=(12,8))
    ax.plot(t_axis,hx[i,:],label='Hx',linestyle='solid' ,linewidth=3,color='b')
    ax.plot(t_axis,hy[i,:],label='Hy',linestyle='dashed',linewidth=3,color='r')
    ax.plot(t_axis,hz[i,:],label='Hz',linestyle='dotted',linewidth=3,color='g')
    set_figenv1(ax,[0,max(t_axis)],[h_min_fig,h_max_fig],\
                'obs'+str(i+1)+' H at point',name_t,name_h)
    pl.savefig('obs'+str(i+1)+'_H_at_point.jpg')
del i, j, tmp_inp, tmp_inp2, fig, ax
###############################################################################
#make animation files##########################################################
###############################################################################
if make_ani=='y': #chosed animation-------------------------------------------#
    #check condition
    if obs_ani=='none' or var_ani=='none' or com_ani=='none' or pla_ani=='none':
        sy.exit('When make_ani=\'y\', you have to set obs_ani, var_ani, com_ani, and pla_ani.')
    #initialize animation
    if pla_ani=='xy':
        pla_ani='_xy_'; iord1=0; iord2=1; paxis1=x_xy; paxis2=y_xy;
        min1=x_min_ani; max1=x_max_ani; min2=y_min_ani; max2=y_max_ani;
    elif pla_ani=='yz':
        pla_ani='_yz_'; iord1=1; iord2=2; paxis1=y_yz; paxis2=z_yz;
        min1=y_min_ani; max1=y_max_ani; min2=z_min_ani; max2=z_max_ani;
    elif pla_ani=='xz':
        pla_ani='_xz_'; iord1=0; iord2=2; paxis1=x_xz; paxis2=z_xz;
        min1=x_min_ani; max1=x_max_ani; min2=z_min_ani; max2=z_max_ani;
    if   var_ani=='e': minc=e_min_ani; maxc=e_max_ani;
    elif var_ani=='h': minc=h_min_ani; maxc=h_max_ani;
    fig_num=2*iobs_num_em+1
    pl.close(fig_num)
    fig, ax=pl.subplots(num=fig_num,figsize=(12,8))
    mappable=0; ims=[]; iflag_clear=0;
    #make animation
    for itime in range(nt): #time loop
        fani=np.zeros((lg_end[iord1],lg_end[iord2]))
        #load data
        if com_ani!='abs':
            f=open(dir_name+'obs'+str(obs_ani)+'_'+var_ani+com_ani+pla_ani+str((itime+1)*iobs_samp_em)+'.data')
            tmp_inp = f.readlines()
            f.close()
            tmp_inp = [s.replace('\n','') for s in tmp_inp]
            for i in range(len(tmp_inp)):
                tmp_inp2=tmp_inp[i]
                tmp_inp2=tmp_inp2.split()
                fani[int(tmp_inp2[0])+lg_adj[iord1],int(tmp_inp2[1])+lg_adj[iord2]]=tmp_inp2[2]
            del tmp_inp, tmp_inp2, i
        elif com_ani=='abs':
            minc=0;
            fx=np.zeros((lg_end[iord1],lg_end[iord2]));
            fy=np.zeros((lg_end[iord1],lg_end[iord2]));
            fz=np.zeros((lg_end[iord1],lg_end[iord2]));
            for icom2 in range(3):
                if icom2==0:   ncom2='x'
                elif icom2==1: ncom2='y'
                elif icom2==2: ncom2='z'
                f=open(dir_name+'obs'+str(obs_ani)+'_'+var_ani+ncom2+pla_ani+str((itime+1)*iobs_samp_em)+'.data')
                tmp_inp = f.readlines()
                f.close()
                tmp_inp = [s.replace('\n','') for s in tmp_inp]
                for i in range(len(tmp_inp)):
                    tmp_inp2=tmp_inp[i]
                    tmp_inp2=tmp_inp2.split()
                    exec('f'+ncom2+'[int(tmp_inp2[0])+lg_adj[iord1],int(tmp_inp2[1])+lg_adj[iord2]]=tmp_inp2[2]')
            fani=np.sqrt( np.power(fx,2)+np.power(fy,2)+np.power(fz,2) )
            del tmp_inp, tmp_inp2, i, fx, fy, fz, icom2, ncom2
        #draw animation
        mappable=ax.pcolorfast(paxis1,paxis2,fani.transpose(),cmap="jet",animated=True)
        if iflag_clear==0:
            pl.colorbar(mappable)
            iflag_clear=1
        mappable.set_clim(minc,maxc)
        set_figenv2(ax,[min1,max1],[min2,max2], \
                    'obs'+str(obs_ani)+' '+var_ani.upper()+com_ani+' '+pla_ani[1:3]+'-plane', \
                    name_l,name_l)
        ims.append([mappable])
    #save animation
    ani = an.ArtistAnimation(fig, ims, interval=frame_speed_ani, blit=True, repeat_delay=1000);
    ani.save('obs'+str(obs_ani)+'_'+var_ani.upper()+com_ani+'_'+pla_ani[1:3]+'-plane'+'.mp4', writer="ffmpeg");
    del ani, itime, fig_num, iord1, iord2, \
        minc, maxc, min1, max1, min2, max2, \
        paxis1, paxis2, ims, iflag_clear, fani, fig, ax, mappable
elif make_ani=='all': #all animation#-----------------------------------------#
    #start
    for iobs in range(iobs_num_em): #observation point loop
        for ivar in range(2): #variable loop
            if   ivar==0: nvar='e'
            elif ivar==1: nvar='h'
            for ipla in range(3): #plane loop
                if ipla==0:
                    npla='_xy_'; iord1=0; iord2=1; paxis1=x_xy; paxis2=y_xy;
                    min1=x_min_ani; max1=x_max_ani; min2=y_min_ani; max2=y_max_ani;
                elif ipla==1:
                    npla='_yz_'; iord1=1; iord2=2; paxis1=y_yz; paxis2=z_yz;
                    min1=y_min_ani; max1=y_max_ani; min2=z_min_ani; max2=z_max_ani;
                elif ipla==2:
                    npla='_xz_'; iord1=0; iord2=2; paxis1=x_xz; paxis2=z_xz;
                    min1=x_min_ani; max1=x_max_ani; min2=z_min_ani; max2=z_max_ani;
                if   nvar=='e': minc=e_min_ani; maxc=e_max_ani;
                elif nvar=='h': minc=h_min_ani; maxc=h_max_ani;
                for icom in range(4): #component loop
                    if icom==0:   ncom='x'
                    elif icom==1: ncom='y'
                    elif icom==2: ncom='z'
                    elif icom==3: ncom='abs';
                    #initialize animation
                    fig_num=2*iobs_num_em+2*3*4*iobs+3*4*ivar+4*ipla+(icom+1)
                    pl.close(fig_num)
                    fig, ax=pl.subplots(num=fig_num,figsize=(12,8))
                    mappable=0; ims=[]; iflag_clear=0;
                    #make animation
                    for itime in range(nt): #time loop
                        fani=np.zeros((lg_end[iord1],lg_end[iord2]))
                        #load data
                        if icom<3:
                            f=open(dir_name+'obs'+str(iobs+1)+'_'+nvar+ncom+npla+str((itime+1)*iobs_samp_em)+'.data')
                            tmp_inp = f.readlines()
                            f.close()
                            tmp_inp = [s.replace('\n','') for s in tmp_inp]
                            for i in range(len(tmp_inp)):
                                tmp_inp2=tmp_inp[i]
                                tmp_inp2=tmp_inp2.split()
                                fani[int(tmp_inp2[0])+lg_adj[iord1],int(tmp_inp2[1])+lg_adj[iord2]]=tmp_inp2[2]
                            del tmp_inp, tmp_inp2, i
                        elif icom==3:
                            minc=0;
                            fx=np.zeros((lg_end[iord1],lg_end[iord2]));
                            fy=np.zeros((lg_end[iord1],lg_end[iord2]));
                            fz=np.zeros((lg_end[iord1],lg_end[iord2]));
                            for icom2 in range(3):
                                if icom2==0:   ncom2='x'
                                elif icom2==1: ncom2='y'
                                elif icom2==2: ncom2='z'
                                f=open(dir_name+'obs'+str(iobs+1)+'_'+nvar+ncom2+npla+str((itime+1)*iobs_samp_em)+'.data')
                                tmp_inp = f.readlines()
                                f.close()
                                tmp_inp = [s.replace('\n','') for s in tmp_inp]
                                for i in range(len(tmp_inp)):
                                    tmp_inp2=tmp_inp[i]
                                    tmp_inp2=tmp_inp2.split()
                                    exec('f'+ncom2+'[int(tmp_inp2[0])+lg_adj[iord1],int(tmp_inp2[1])+lg_adj[iord2]]=tmp_inp2[2]')
                            fani=np.sqrt( np.power(fx,2)+np.power(fy,2)+np.power(fz,2) )
                            del tmp_inp, tmp_inp2, i, fx, fy, fz, icom2, ncom2
                        #draw animation
                        mappable=ax.pcolorfast(paxis1,paxis2,fani.transpose(),cmap="jet",animated=True)
                        if iflag_clear==0:
                            pl.colorbar(mappable)
                            iflag_clear=1
                        mappable.set_clim(minc,maxc)
                        set_figenv2(ax,[min1,max1],[min2,max2], \
                                    'obs'+str(iobs+1)+' '+nvar.upper()+ncom+' '+npla[1:3]+'-plane', \
                                    name_l,name_l)
                        ims.append([mappable])
                    #save animation
                    ani = an.ArtistAnimation(fig, ims, interval=frame_speed_ani, blit=True, repeat_delay=1000);
                    ani.save('obs'+str(iobs+1)+'_'+nvar.upper()+ncom+'_'+npla[1:3]+'-plane'+'.mp4', writer="ffmpeg");
                    del ani
    del iobs, ivar, ipla, icom, itime, fig_num, iord1, iord2, \
        minc, maxc, min1, max1, min2, max2, \
        ncom, nvar, npla, paxis1, paxis2, \
        iflag_clear, ims, fani, fig, ax, mappable
###############################################################################
#fin###########################################################################
###############################################################################
#output calculation time
elapsed_time = ti.time() - start_time
print ("elapsed time:{0}".format(elapsed_time) + "[sec]")
#delete all variables
del dir_name, make_ani, obs_ani, var_ani, com_ani, pla_ani, frame_speed_ani, \
    e_min_fig, e_max_fig, h_min_fig, h_max_fig, \
    e_min_ani, e_max_ani, h_min_ani, h_max_ani, \
    x_min_ani, x_max_ani, y_min_ani, y_max_ani, z_min_ani, z_max_ani, \
    unit_system, iperiodic, dt_em, nt_em, al_em, dl_em, lg_sta, lg_end, \
    iobs_num_em, iobs_samp_em, e_max, h_max, \
    nt, lg_adj, r_min, x1d, y1d, z1d, x_xy, y_xy, y_yz, z_yz, x_xz, z_xz, \
    start_time, elapsed_time
del ex, ey, ez, hx, hy, hz, name_e, name_h, name_l, name_t, t_axis
del f, init_1d_list, set_figenv1, set_figenv2
print('Finish!')

















