from typing import TypedDict

import numpy as np
from astropy.table import Table
import pandas as pd

from sklearn.ensemble import GradientBoostingRegressor


TimingData = TypedDict(
    "TimingData",
    {
        "band": str,
        "maximum_jd": float,
        "maximum_mag": float,
        "t2_mag": float,
        "t2_jd": float,
    },
)

MagData = TypedDict(
    "MagData",
    {
        "band": str,
        "predicted_mag": float,
        "eruption_time": float,
        "time_from_eruption": float,
        "tN_jd": float,
    },
)

def measure_time(dataset: Table) -> TimingData:
    
    mask = dataset.groups.keys["Band"] == "V"
    singlebanddata = dataset.groups[mask]
    magnitudes = singlebanddata["Magnitude"]
    jds = singlebanddata["JD"]
    
    alldata = dataset
    
    maximum_mag = min(magnitudes)
    maximum_indx = np.argmin(magnitudes)
    maximum_jd = jds[maximum_indx]
    
    X = np.array(jds)
    y = np.array(magnitudes)
    #print(len(X), len(y))
    
    X = X[~np.isnan(y)]
    y = y[~np.isnan(y)]
    #print(len(X), len(y))
    
    X = X[np.argmin(y):]
    y = y[np.argmin(y):]
    X =  X.reshape(-1, 1)
    
    #X_all = np.array(alldata['MET'])
    X_all = np.array(alldata['JD'][alldata['JD']<max(singlebanddata['JD'])])
    X_all = np.asarray(sorted(X_all[np.argmin(y):]))
    X_all = X_all.reshape(-1, 1)
    
    #have now included a data quality flag, if the LC is particualry data poor (or you are using binned means) the max_depth is increased
    if len(singlebanddata) < 100: 
        gbm = GradientBoostingRegressor(n_estimators=100, learning_rate=0.1, max_depth=5)
    else:
        gbm = GradientBoostingRegressor(n_estimators=100, learning_rate=0.1, max_depth=3)
        
    gbm.fit(X, y)
    
    fit = gbm.predict(X_all)
    
    t2_indx = np.argmin(np.abs(fit - (y.min()+2)))
    #print(t2_indx)
    #tN_mag = y[tN_indx]
    t2_mag = fit[t2_indx]
    
    t2_jd = X_all[t2_indx]
    
    #print(maximum_jd,maximum_mag,t2_mag,t2_jd[0])
    #print(type(maximum_jd), type(maximum_mag), type(t2_mag), type(t2_jd[0]))
    
    results = TimingData(
        band="V",
        maximum_jd=maximum_jd,
        maximum_mag=maximum_mag,
        t2_mag=t2_mag,
        t2_jd=t2_jd[0],
    )
    
    return(results)

def measure_tN(dataset: Table) -> TimingData:
    
    window = input('What is your window size (measure in days from eruption peak):')
    window = float(window)*86400
    
    mask = dataset.groups.keys["Band"] == "V"
    singlebanddata = dataset.groups[mask]
    magnitudes = singlebanddata["Magnitude"]
    jds = singlebanddata["JD"]
    
    alldata = dataset
    
    maximum_mag = min(magnitudes)
    maximum_indx = np.argmin(magnitudes)
    maximum_jd = jds[maximum_indx]
    
    X = np.array(jds)
    y = np.array(magnitudes)
    
    X = X[~np.isnan(y)]
    y = y[~np.isnan(y)]
    #X = np.array(data['MET']) #parsing the dataframe
    #y = np.array(data['Magnitude'])
    
    X =  X.reshape(-1, 1) #columnating the vector
    
    gbm = GradientBoostingRegressor(n_estimators=100, learning_rate=0.1, max_depth=1) #standard GBM
    gbm.fit(X, y)
    
    #fit = gbm.predict(X) #just passing X data right back will reproduce original data exactly 

    preds = np.array([X[np.argmin(y)]+window]) #predict magnitude according to fit a window away from the LC maximum
    preds = preds.reshape(-1, 1)
    predictions = gbm.predict(preds)
    #print(type(predictions))
    tN = (predictions[0] - y.min()) #tN is defined as the amount of time it takes the LC magnitude to reduce by N, this is the amount the LC has diminished
    #print(tN)
    
    #print(predictions[0],X[np.argmin(y)],window,tN)
    #print(type(predictions[0]), type(X[np.argmin(y)]), type(window), type(tN))
    
    results = MagData(
        band="V",
        predicted_mag=predictions[0],
        eruption_time=X[np.argmin(y)][0],
        time_from_eruption=window,
        tN_jd=tN,
    )
    
    return(results)
