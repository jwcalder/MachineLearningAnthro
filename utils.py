import numpy as np
import amaazetools.trimesh as tm
import pickle
import matplotlib.pyplot as plt
from scipy import spatial
import os,sys
import pandas as pd


#Put all possible directory locations here
data_dirs = ['/drive/GoogleDrive/AMAAZE/Dissertation_YezziWoodley/Paper3_MoclanReplicationPaper/',
             '/Users/jeff/Moclan/Paper3_MoclanReplicationPaper/',
             '/data/ML_data/']

#Find the directory that exists on a particular machine
try:
    data_dir_enum = enumerate(data_dirs)
    _,data_dir = next(data_dir_enum)
    while not os.path.isdir(data_dir):
        _,data_dir = next(data_dir_enum)
except:
    print('Warning: Could not find data directory.')

def sample_inventory(fields):

    #Load inventory file
    df = pd.read_csv(data_dir + 'finaldata_inventoryall.csv', encoding = 'cp1252')
    df = df[fields]

    #Load angle data dictionary
    with open('break_curve_data.pkl', 'rb') as f:
        angledata = pickle.load(f)

    specimen_list = []
    for specimen in angledata:
        specimen_list += [specimen]

    keep = np.zeros(len(df),dtype=bool)
    for i in range(len(df)):
        keep[i] = df['Specimen'][i] in specimen_list
    df = df[keep].reset_index().drop(['index'],axis=1)

    num_breaks = np.zeros(len(df))
    for i in range(len(df)):
        num_breaks[i] = len(angledata[df['Specimen'][i]])
    df['NumBreaks'] = num_breaks.astype(int)

    return df

def arc_length(x,y,z):
    v = np.vstack((x,y,z))
    length = 0
    for i in range(len(x)-1):
        length += np.linalg.norm(v[:,i+1] - v[:,i])
    return length

def arc_angle(x,y,z,principle_dir):
    v = np.vstack((x,y,z)).T
    _, vecs = tm.pca(v)
    break_dir = vecs[:,0]
    angle = np.arccos(np.abs(np.dot(principle_dir,break_dir)))*180/np.pi
    return angle
        
def save_curve(x,y,z,idx,break_num,fname):

    fig = plt.figure(figsize=(10,10))
    fig.suptitle('Break %d'%break_num)
    ax = fig.add_subplot(2,2,1,projection='3d')
    ax.scatter(x[idx[1:-1]],y[idx[1:-1]],z[idx[1:-1]],c='b')
    ax.scatter(x[idx[0]],y[idx[0]],z[idx[0]],c='r',s=100)
    ax.scatter(x[idx[-1]],y[idx[-1]],z[idx[-1]],c='g',s=100)
    ax.plot(x[idx],y[idx],z[idx])
    ax.set_title('(0,0)')
    ax.view_init(elev=0., azim=0)

    ax = fig.add_subplot(2,2,2,projection='3d')
    ax.scatter(x[idx[1:-1]],y[idx[1:-1]],z[idx[1:-1]],c='b')
    ax.scatter(x[idx[0]],y[idx[0]],z[idx[0]],c='r',s=100)
    ax.scatter(x[idx[-1]],y[idx[-1]],z[idx[-1]],c='g',s=100)
    ax.plot(x[idx],y[idx],z[idx])
    ax.set_title('(0,90)')
    ax.view_init(elev=0., azim=90)

    ax = fig.add_subplot(2,2,3,projection='3d')
    ax.scatter(x[idx[1:-1]],y[idx[1:-1]],z[idx[1:-1]],c='b')
    ax.scatter(x[idx[0]],y[idx[0]],z[idx[0]],c='r',s=100)
    ax.scatter(x[idx[-1]],y[idx[-1]],z[idx[-1]],c='g',s=100)
    ax.plot(x[idx],y[idx],z[idx])
    ax.set_title('(45,0)')
    ax.view_init(elev=45., azim=0)

    ax = fig.add_subplot(2,2,4,projection='3d')
    ax.scatter(x[idx[1:-1]],y[idx[1:-1]],z[idx[1:-1]],c='b')
    ax.scatter(x[idx[0]],y[idx[0]],z[idx[0]],c='r',s=100)
    ax.scatter(x[idx[-1]],y[idx[-1]],z[idx[-1]],c='g',s=100)
    ax.plot(x[idx],y[idx],z[idx])
    ax.set_title('(90,0)')
    ax.view_init(elev=90., azim=0)

    plt.savefig(fname)
    plt.close()

def plot_curve(x,y,z,idx,break_num):

    fig = plt.figure()
    ax = fig.add_subplot(projection='3d')
    ax.scatter(x[idx[1:-1]],y[idx[1:-1]],z[idx[1:-1]],c='b')
    ax.scatter(x[idx[0]],y[idx[0]],z[idx[0]],c='r',s=100)
    ax.scatter(x[idx[-1]],y[idx[-1]],z[idx[-1]],c='g',s=100)
    ax.plot(x[idx],y[idx],z[idx])
    ax.set_title('Break %d'%break_num)

def tsp_path(D,i):
    n = D.shape[0]
    path = [i]
    length = []
    for j in range(n-1):
        path += [np.argmin(D[path[j],:])]
        length += [D[path[j],path[j+1]]]
        D[:,path[j]] = np.inf
    
    return path,np.array(length)

def tsp_order(x,y,z):
    n = len(x)
    X = np.stack((x,y,z)).T
    D = spatial.distance_matrix(X,X)
    D[range(n),range(n)] = np.inf

    #Try starting from each point
    min_length = np.ones((n-1,))*np.inf
    min_path = list(range(n))
    for i in range(n):
        path,length = tsp_path(D.copy(),i)
        if np.sum(length) < np.sum(min_length):
            min_length = length
            min_path = path
    return min_path

