#!/usr/bin/env python

import sys
import os
import getpass
import pandas as pd
import astropy.units as u
import astropy.constants as c
import uncertainties as unc
import itertools
import numpy as np
from nexsci import utils

def parse_nexsci_html():
    #parse tables
    link= 'https://exoplanetarchive.ipac.caltech.edu/docs/API_exoplanet_columns.html'
    try:
        html=pd.read_html(link,header=0)
        return html
    except Exception as e:
        print(e)
        sys.exit()
        
def decode_name_id(keyword):
    ids = [0,1,2,3,4,5]
    table_names = 'default,planet,stellar,photometry,color'.split(',')
    
    name_id = {1: 'default',
               2: 'planet',
               3: 'stellar',
               4: 'photometry',
               5: 'color'}
    if type(keyword)==str:
        if keyword in table_names:
            return keyword.lower()
        elif keyword=='all':
            return 'all'
        else:
            print('Name not one of the ff:\n{}'.format(table_names))
            sys.exit()
    elif type(keyword)==int:
        if keyword in ids:
            print('keyword: {}'.format(name_id[keyword]))
            return name_id[keyword]
        else:
            print('ID not one of the ff:\n{}'.format(ids))
            sys.exit()
    else:
        print('Passed input ({}) not understood.'.format(table_name_id))

def parse_data_columns(keyword,remove_special_char=True):
    '''
    parse the column names defined in NExSci:
    https://exoplanetarchive.ipac.caltech.edu/docs/API_exoplanet_columns.html
    
    Parameters
    ----------
    keyword, str or int: corresponding to table name
    remove_special_char, bool: remove special characters in table
    
    1: default
    2: planet
    3: stellar
    4: photometry
    5: color
    all: (returns all tables as dict)
    
    Returns
    -------
    df : dataframe
    '''
    
    #dict of df or tables
    DF = {}
    
    #parse NExSci html page
    html = parse_nexsci_html()
    
    table_names = 'default,planet,stellar,photometry,color'.split(',')
    for tab,name in zip(html,table_names):
        if remove_special_char:
            tab[tab.columns[0]] = tab[tab.columns[0]].apply(lambda x: x.strip('†'))
            DF[name] = tab
    
    keyword=decode_name_id(keyword)
    if keyword=='all':
        return DF
    else:
        return DF[keyword]

def parse_data_columns_unc(keyword):
    DF_unc = {}
    html = parse_nexsci_html()
    
    table_names = 'default,planet,stellar'.split(',')
    for tab,name in zip(html,table_names):
        #uncertainty is 3rd col
        words = tab[tab.columns[3]].dropna().apply(lambda x:x.split('(-) '))
        plus = []
        minus = []
        for word in words:
            if len(word)==2:
                minus.append(word[0].strip('(+)').strip(' '))
                plus.append(word[1].strip(' '))
            #bug: replace pl_ratdorperr1 with pl_ratdorerr1
            minus = ['pl_ratdorerr1' if i=='pl_ratdorperr1' else i for i in minus]
            DF_unc[name] = np.concatenate(([minus,plus]),axis=0)
    
    keyword = decode_name_id(keyword)
    if keyword=='all':
        return DF_unc
    else:
        return DF_unc[keyword]
    
def get_param_names(DF,keyword):
    '''
    return list(s) of parameter names to be downloaded
    using 
    '''
    keyword=decode_name_id(keyword)
    
    if keyword=='all':
        #dict of several df
        cols_list = []
        for key in DF:
            df = DF[key]
            param_col = df[df.columns[0]].values
            cols_list.append(param_col)
            all_params = list(itertools.chain.from_iterable(cols_list))
            #remove duplicates
            all_params=list(set(all_params))
            #convert list into one str
            all_params= ','.join(all_params)
        return all_params
    
    else:
        #just one dataframe
        df = DF.copy()
        param_col = df.values
        #convert list into one str
        param_col = ','.join(param_col)
        return param_col
    
def get_param_names_unc(DF_unc,keyword):
    '''
    return list(s) of parameter names to be downloaded
    using 
    '''
    keyword=decode_name_id(keyword)
    
    if keyword=='all':
        #dict of several df
        cols_list = []
        for key in DF_unc:
            df = DF_unc[key]
            cols_list.append(df)
        all_params = list(itertools.chain.from_iterable(cols_list))
        #remove duplicates
        all_params=list(set(all_params))
        #convert list into one str
        all_params= ','.join(all_params)
        return all_params
    
    else:
        #just one dataframe
        df = DF_unc.copy()
        #convert list into one str
        param_col = ','.join(df)
        return param_col
    
def get_nexsci_download_url(keyword):
    '''
    create download url specific for given the 'keyword'
    
    Parameters
    ----------
    keyword, str or int: corresponding to table name
    remove_special_char, bool: remove special characters in table
    
    1: default
    2: planet
    3: stellar
    4: photometry
    5: color
    all: (returns all tables as dict)
    
    Returns
    -------
    download_url, str: download url
    '''
    
    base_url = 'http://exoplanetarchive.ipac.caltech.edu/cgi-bin/nstedAPI/nph-nstedAPI?table=exoplanets'    
    
    DF = parse_data_columns(keyword)
    DF_unc = parse_data_columns_unc(keyword)
    param_names     = get_param_names(DF,keyword)
    param_names_unc = get_param_names_unc(DF_unc,keyword)
    download_url= base_url+'&select='+param_names+','+param_names_unc
    return download_url

def fetch_csv(download_url):
    '''
    '''
    base_url = 'http://exoplanetarchive.ipac.caltech.edu/cgi-bin/nstedAPI/nph-nstedAPI?table=exoplanets'
    print("Downloading data from URL:\n{}\n".format(base_url))
    df = pd.read_csv(download_url)
    return df

uname = getpass.getuser()
loc = os.path.join('/home',uname,'data/')

def download_nexsci(keyword,filename='confirmed_planets.csv',
                    loc=loc,replace=True):
    '''
    helper function to download data from NExSci:
    http://exoplanetarchive.ipac.caltech.edu/

    See meaning of columns here:
    https://exoplanetarchive.ipac.caltech.edu/docs/API_exoplanet_columns.html
    '''
    full_path= os.path.join(loc,filename)

    try:
        if not os.path.isfile(full_path):
            #download from database
            download_url = get_nexsci_download_url(keyword)
            df  = fetch_csv(download_url)
            #save
            df.to_csv(full_path)
            print('Saved: {}\nin {}\n'.format(filename,loc))
        else:
            #read previously downloaded file
            if replace:
                #download from database
                download_url = get_nexsci_download_url(keyword)
                df  = fetch_csv(download_url)
                #save
                df.to_csv(full_path)
                print('Saved: {}\nin {}\n'.format(filename,loc))
            else:
                df  = pd.read_csv(full_path)

    except Exception as e:
        print('Download attempt unsuccessful.\n{}'.format(e))
        sys.exit()

    return df

def query_nexsci(hostname,keyword='all',letter='b',replace=False):
    '''
    query exoplanet system parameters from NExSci database
    '''

    if replace:
        df=download_nexsci(keyword=keyword,replace=True)
    else:
        df=download_nexsci(keyword=keyword,replace=False)

    q = df.query("pl_hostname == @hostname and pl_letter== @letter")
    

    if len(q)==0:
        print('Query unsuccessful. Check hostname.\nExiting!\n')
        sys.exit()

    return q

def get_error(df,param):
    try:
        err1=df[param+'err1'].values[0]
    except:
        err1=np.nan
    try:
        err2=df[param+'err2'].values[0]
    except:
        err2=np.nan

    return np.array([float(err1),float(err2)])


def query_transit_params(hostname,letter='b',precision=4):
    '''
    Query transit parameters of the system:
    Rp/Rs, t0, p, a/Rs, b, i, e, w;
    including Teff, logg, [Fe/H]
    from NExSci database
    '''
    pd.set_option('precision', precision)
    
    data=query_nexsci(hostname,letter=letter)
    
    param_names = 'pl_radj,pl_trandur,pl_tranmid,pl_orbper,pl_orbsmax,pl_imppar,pl_orbincl,pl_orbeccen,st_logg,st_metfe,st_rad,st_teff'.split(',')
    param_names = sorted(param_names)
    #select certain params and invert into column
    value = data[param_names]
    #add uncertainties
    
    err1_names = []
    err2_names = []
    for n in param_names:
        err1_names.append(n+'err1')
        err2_names.append(n+'err2')
    
    err1 = data[err1_names]
    err2 = data[err2_names]
    err1.columns = param_names
    err2.columns = param_names
    
    df = value.append([err1,err2]).T 
    df.columns = ['value','err1','err2']
    
    ## Rp/Rs
    Rp = df.loc['pl_radj']*u.Rjup
    #Rp = unc.ufloat(Rp['value'],utils.quad_err(Rp['err1'],Rp['err2']))
    Rs = df.loc['st_rad']*u.Rsun.to(u.Rjup)
    #Rs = unc.ufloat(Rs['value'],utils.quad_err(Rs['err1'],Rs['err2']))
    #k = (Rp/Rs).n
    #kerr = (Rp/Rs).s
    #0.1343 +/- 0.0179
    
    Rperr1 = unc.ufloat(Rp['value'],Rp['err1'])
    Rperr2 = unc.ufloat(Rp['value'],abs(Rp['err2']))
    Rserr1 = unc.ufloat(Rs['value'],Rs['err1'])
    Rserr2 = unc.ufloat(Rs['value'],abs(Rs['err2']))
    k = (Rperr1/Rserr1).n #== kerr2.n
    kerr1 = (Rperr1/Rserr1).s
    kerr2 = (Rperr2/Rserr2).s
    kerr = utils.quad_err(kerr1,kerr2) #== (Rp/Rs).s
    #0.1343-0.0161+0.0079 (quad: 0.0179)
    
    ## a/Rs
    a = df.loc['pl_orbsmax']*u.au
    Rs_au = df.loc['st_rad']*u.Rsun.to(u.au)
    
    a_err1 = unc.ufloat(a['value'],a['err1'])
    a_err2 = unc.ufloat(a['value'],abs(a['err2']))
    Rs_au_err1 = unc.ufloat(Rs_au['value'],Rs_au['err1'])
    Rs_au_err2 = unc.ufloat(Rs_au['value'],abs(Rs_au['err2']))
    
    a_s = (a_err1/Rs_au_err1).n 
    a_s_err1 = (a_err1/Rs_au_err1).s
    a_s_err2 = (a_err2/Rs_au_err2).s
    a_s_err = utils.quad_err(a_s_err1,a_s_err2)
    
    
    t0 = df.loc['pl_tranmid']
    p  = df.loc['pl_orbper']
    b  = df.loc['pl_imppar']
    i  = df.loc['pl_orbincl']
    e  = df.loc['pl_orbeccen']
    #stellar params for limb darkening model
    g = df.loc['st_logg']
    fe_h = df.loc['st_metfe']
    teff = df.loc['st_teff']
    #k ={'value':k, 'err1':kerr1, 'err2':kerr2}
    #a_s ={'value':a_s, 'err1':a_s_err1, 'err2':a_s_err2}
    
    k   = pd.Series({'value':k, 'err1':kerr1, 'err2':-kerr2},name='Rp/Rs')
    a_s = pd.Series({'value':a_s, 'err1':a_s_err1, 'err2':-a_s_err2},name='a/Rs')
    
    #df['value'] = df['value'].map('{:,.2f}'.format)
    
    df = df.append(k)
    df = df.append(a_s)
    idx_names = 'b,ecc,inc[deg],P[d],a[au],Rp[Rj],t14[d],t0[d],logg,[Fe/H],Rs[Rsun],Teff,Rp/Rs,a/Rs'.split(',')
    df.index = idx_names
    #import pdb; pdb.set_trace()
    return df
