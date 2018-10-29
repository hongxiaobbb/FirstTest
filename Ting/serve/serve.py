# -*- coding: utf-8 -*-

import numpy as np
import pandas as pd
import folium
import socket
from math import pi
from bokeh.io import output_file, show
from bokeh.layouts import widgetbox, row, column, gridplot
from bokeh.models.widgets import TextInput, Button, Select, Div, Paragraph, DataTable, TableColumn
from bokeh.plotting import figure, curdoc
from bokeh.models import ColumnDataSource, GMapOptions, CategoricalColorMapper, LabelSet
from bokeh.palettes import Viridis256, Category20c
from bokeh.transform import factor_cmap, cumsum
from bokeh.models.ranges import Range, FactorRange

S_JOBNO = 'JOBNO'
S_LAT = 'LATITUDE (deg)'
S_LNG = 'LONGITUDE (deg)'
S_WELLNAME = 'WELLNAME'
S_SDETAIL = 'SERVICE_DETAILS'
S_GEO = 'GEO'
S_MONTH = 'MONTH'
S_FIRST_BRS_DATE =  'FIRST_BRS_DATE'
S_DATEIN =  'DATE_IN'
S_DATEOUT =  'DATE_OUT'
S_ACCOUNTS = 'CORPORATE_ALIAS'
S_TOOLNAME = 'TOOLNAME'
S_LOC = 'LOC'
S_ALL = '--all--'
S_DRL_DIST = 'DRL_DIST_FT'
S_REAM_DIST = 'REAM_DIST_FT'
S_RUNNO = 'RUNNO'
S_HOLESIZE = 'HOLE_SIZE_IN'
S_AVGROP = 'AVG_ON_BOTTOM_ROP'
DOMAIN = '.dir.slb.com'
S_REASON_POOH = 'REASON_FOR_POOH'

def bTitle(D):
    hname = "http://"+socket.gethostname()+DOMAIN+":8888\map.html"
    T = "<center><font size=\"8\">"+D['GEO'].unique()[0]+ " LWD activity from "+D['DATE_OUT'].min().date().strftime('%d/%m/%y')+" to "+D['DATE_OUT'].max().date().strftime('%d/%m/%y')+"</font></center>"
    T = T+"<br><a href=\""+hname+"\">Well locations</a><br>"
    D = Div(text=T, width = 1200)
    return D

def bitSizeL(D):
    hs = D[S_HOLESIZE].unique()
    L = []   
    for i in hs:
        L.append(np.str(i))
    return Select(title="Average on bottom ROP (m/hr) of this bit size", value=np.str(L[0]), options=L)

def locationL(D):
    loca = D[S_LOC].unique()
    L = []
    L.append(S_ALL)
    for i in loca:
        L.append(np.str(i))
    return Select(title="Locations", value=np.str(L[0]), options=L)

def LWDByAccounts(D):
    acct = D[S_ACCOUNTS].unique()  
    L = []
    L.append(S_ALL)
    for i in acct:
        L.append(np.str(i))
    return Select(title="Accounts", value=np.str(L[0]), options=L)
    
def LWDTableL(D):
    tools = D[S_TOOLNAME].unique()
    L = []
    for i in tools:
        L.append(np.str(i))
    return Select(title="Find wells using this tool", value=np.str(L[0]), options=L)
    
def createMap(D):
    D_ = D.drop_duplicates(subset=[S_JOBNO],keep='first', inplace=False)
    initlat = np.float(D_[:1][S_LAT])
    initlon = np.float(D_[:1][S_LNG])
    m = folium.Map(location=[initlat,initlon], zoom_start=4)
    for index, r in D_.iterrows():
        wname = np.str(r[S_WELLNAME])
        rsum = np.str(r[S_SDETAIL])
        try:
            folium.Marker([np.float(r[S_LAT]), np.float(r[S_LNG])], popup='<i>'+wname+':'+rsum+'</i>').add_to(m)
        except:
            continue
     
    m.save('templates/map.html')
    return D_ 

def toolSpecific(vala, vall, toolName):
    S = D
    if vala != S_ALL:
        S = D[D[S_ACCOUNTS]== vala]   
    
    if vall != S_ALL:
        S = S[S[S_LOC]==vall]
    
    thistool = S[S[S_TOOLNAME]==toolName]
    J = thistool[S_JOBNO].unique()
    
    jobno = []
    summary = []
    wellname = []
    for t in J:
        jobno.append(t)
        K = thistool[thistool[S_JOBNO]==t][S_SDETAIL][:1].tolist()[0]
        G = thistool[thistool[S_JOBNO]==t][S_WELLNAME][:1].tolist()[0]
        summary.append(K)
        wellname.append(G)
     
    return (jobno, summary, wellname)

def plotLWDUsage(vala, vall):
    T = D[S_TOOLNAME].unique()
    S = D
    if vala != S_ALL:
        S = D[D[S_ACCOUNTS]== vala]   
    
    if vall != S_ALL:
        S = S[S[S_LOC]==vall]
    
    Y = []
    X = []
    DIST_TOT = []
    DIST_DRL = []
    DIST_REAM = []
    TXT_HT_DRL = []
    TXT_HT_REAM = []
    DISP_DRL = []
    DISP_REAM = []
    dist_fact = 1000
    for t in T:
        s = (S[S_TOOLNAME]==np.str(t)).sum()
        drl = (S[S[S_TOOLNAME]==np.str(t)][S_DRL_DIST]).sum()
        ream = (S[S[S_TOOLNAME]==np.str(t)][S_REAM_DIST]).sum()
        X.append(np.str(t))
        Y.append(s)
        DIST_TOT.append(drl/dist_fact+ream/dist_fact)
        DIST_DRL.append(drl/dist_fact)
        DIST_REAM.append(ream/dist_fact)
        TXT_HT_DRL.append(drl/dist_fact/2.0)
        TXT_HT_REAM.append(drl/dist_fact+ream/dist_fact/2.0)
        DISP_DRL.append("%.1f" % (drl/dist_fact))
        DISP_REAM.append("%.1f" % (ream/dist_fact))
        
    
    return (X,Y, DIST_TOT, DIST_DRL, DIST_REAM, TXT_HT_DRL, TXT_HT_REAM, DISP_DRL, DISP_REAM)

def update_ToolSpecific(attrname, old, new):
    vala = p_sel_acct.value
    vall = p_sel_loc.value
    toolName = p_sel_tools.value
    (J,S,W) = toolSpecific(vala, vall, toolName)

    source2.data = dict(jobno=J, summary=S, wellname=W)   
    
def update_LWDUsage(attrname, old, new):
    vala = p_sel_acct.value
    vall = p_sel_loc.value
    toolName = p_sel_tools.value
    bs = p_sel_bs.value
    (Hist,Left,Right) = avgROP(vala, vall, bs)

    (REASON, ANGLE, COLOR, SUM) = piePOOH(vala, vall)
    (H,L,R) = avgROP(vala, vall, bs)
    (J,S,W) = toolSpecific(vala, vall, toolName)
    (X,Y,DIST_TOT, DIST_DRL, DIST_REAM, TXT_HT_DRL, TXT_HT_REAM, DISP_DRL, DISP_REAM) = plotLWDUsage(vala, vall)
    source4.data = dict(REASON=REASON, ANGLE=ANGLE, COLOR=COLOR, SUM = SUM)
    source3.data = dict(Hist=Hist, Left=Left, Right = Right)
    source2.data = dict(jobno=J, summary=S, wellname=W)  
    source.data = dict(tools=X, counts=Y,colors = Viridis256[:len(X)], 
                    dist_tot = DIST_TOT, dist_drl = DIST_DRL, dist_ream = DIST_REAM, 
                    txt_ht_drl = TXT_HT_DRL, txt_ht_ream = TXT_HT_REAM,
                    disp_drl = DISP_DRL, disp_ream = DISP_REAM)
    
    
def piePOOH(vala, vall):
    S = D
    if vala != S_ALL:
        S = D[D[S_ACCOUNTS]== vala]   
    
    if vall != S_ALL:
        S = S[S[S_LOC]==vall]
    
    REASON = []
    SUM = []
    Reasons = S[S_REASON_POOH].unique()
    total = 0
    for i in Reasons:
        REASON.append(i)
        total = total + (S[S_REASON_POOH]==i).sum()
    
    
    ANGLE = []
    COLOR = []
    index = 0
    for i in Reasons:
        coun = (S[S_REASON_POOH]==i).sum()
        SUM.append(coun)
        ANGLE.append(coun/total*2*pi) 
        if index > 19:
            COLOR.append(Category20c[20][19])
        else:
            COLOR.append(Category20c[20][index])
        index = index + 1
    

    return (REASON, ANGLE, COLOR, SUM)
def avgROP(vala, vall, bs) :
    S = D
    if vala != S_ALL:
        S = D[D[S_ACCOUNTS]== vala]   
    
    if vall != S_ALL:
        S = S[S[S_LOC]==vall]
    
    ROP = S[S[S_HOLESIZE]==np.float(bs)][S_AVGROP].tolist()
    ROP = np.array(ROP)
    ROP = ROP[np.isfinite(ROP)]
    H, E = np.histogram(ROP, density=True, bins=10)
    #H = np.append(H,[0])
    L = E[:-1]
    R = E[1:]
    return (H,L,R)

global D
params = curdoc().session_context.request.arguments
p_fname = np.str(params['filename'][0].decode("ascii"))
DIR = "uploads/"

#fname = 'NAO-FEA-LWD-2018.csv'
fname = DIR+p_fname
na_values=['-', '#N/A']

D = pd.read_csv(fname, sep=',', encoding='latin1',  na_values=na_values, parse_dates=[S_FIRST_BRS_DATE, S_DATEIN, S_DATEOUT], dayfirst=True)

#params = curdoc().session_context.request.arguments  
#geomarket_code = np.str(params['geomarket'][0].decode("ascii"))
#print(geomarket_code)
#D = D[D[S_GEO]==geomarket_code]
#print(len(D))
createMap(D)

#output_file('page.html')

#########################################################################################
# LWD job counts by accounts and location
#########################################################################################
p_sel_acct = LWDByAccounts(D)
p_sel_loc = locationL(D)
p_sel_tools = LWDTableL(D)
p_sel_bs = bitSizeL(D)
p_title = bTitle(D)

ToolTips = [
        ("tool",'@tools'),
        ("count",'@counts')
        ]
ToolTips2 = [
        ("tool",'@tools'),
        ("drilling(1000 ft)",'@disp_drl'),
        ("reaming(1000 ft)",'@disp_ream')
        ]
(X,Y, DIST_TOT, DIST_DRL, DIST_REAM, TXT_HT_DRL, TXT_HT_REAM, DISP_DRL, DISP_REAM) = plotLWDUsage(p_sel_acct.value, p_sel_loc.value)
mapper = CategoricalColorMapper(palette=Viridis256[::10],factors=X)
source = ColumnDataSource(data=dict(tools = X, counts = Y, colors=Viridis256[:len(X)], 
                            dist_tot = DIST_TOT, dist_drl = DIST_DRL, dist_ream = DIST_REAM, 
                            txt_ht_drl = TXT_HT_DRL, txt_ht_ream = TXT_HT_REAM, 
                            disp_drl = DISP_DRL, disp_ream = DISP_REAM))
p = figure(  x_range=X, plot_height=500,  plot_width=1400, title="LWD run counts", tooltips = ToolTips)
p.vbar(x='tools', top='counts', width=0.9,
       source = source,  fill_color={'field':'tools','transform':mapper},line_color=None)
labels = LabelSet(x='tools', y='counts', text='counts', level='glyph',
        x_offset=-13.5, y_offset=0, source=source, render_mode='canvas')

p.add_layout(labels)
p.xaxis.major_label_orientation = np.pi/4
   
p_sel_acct.on_change('value', update_LWDUsage)
p_sel_loc.on_change('value', update_LWDUsage)
p_sel_tools.on_change('value', update_LWDUsage)
p_sel_bs.on_change('value', update_LWDUsage)
#p.vbar(x='tools', top='counts', width=0.9, source=source, legend='tools')
#p.y_range.start = 0
#p.y_range.end=100

#show(p_title)
#show(column(p_title, p_sel_acct, p))
R = row(p_sel_acct, p_sel_loc)

#########################################################################################
# LWD footage 
#########################################################################################
p1 = figure(  x_range=X, plot_height=500,  plot_width=1400, title="LWD footage (1000's of feet) ", tooltips = ToolTips2)
p1.vbar(x='tools', top = 'dist_drl', width = 0.9, source=source, legend="drilling")
p1.vbar(x='tools', top = 'dist_tot', bottom = 'dist_drl', width = 0.9, source=source, color='orange', legend="reaming")
lbl_drl = p1.text(x='tools', y='txt_ht_drl', source=source, text='disp_drl', text_font_size='8pt')
lbl_ream = p1.text(x='tools', y='txt_ht_ream', source=source, text='disp_ream', text_font_size='8pt')
p1.xaxis.major_label_orientation = np.pi/4

#########################################################################################
# LWD usage table
#########################################################################################

(J,S,W) = toolSpecific(p_sel_acct.value, p_sel_loc.value, p_sel_tools.value)
source2 = ColumnDataSource(data=dict(jobno=J, summary=S, wellname=W))
columns = [
        TableColumn(field='wellname', title = 'Well Name', width=100),
        TableColumn(field='jobno', title = 'Job Number', width = 100),
        TableColumn(field='summary', title = 'Service Summary', width = 900),
        ]
data_table = DataTable(source=source2, columns = columns, width = 1400, height = 300, editable=True)

#########################################################################################
# AVG ROP histogram
#########################################################################################
#(hist,edges) = avgROP(p_sel_acct.value, p_sel_loc.value, p_sel_bs.value)

(Hist,Left, Right) = avgROP(p_sel_acct.value, p_sel_loc.value, p_sel_bs.value)
source3 = ColumnDataSource(data=dict(Hist=Hist, Left=Left, Right=Right))
#S=D[D[S_LOC]==loc_code]
#ROP = S[S[S_HOLESIZE]==np.float(bs)][S_AVGROP].tolist()
#ROP = np.array(ROP)
#ROP = ROP[np.isfinite(ROP)]
#hist, edges = np.histogram(ROP, density=True, bins=20)

p2 = figure(title='Average ROP (m/hr)',tools="save",
            background_fill_color="#E8DDCB", plot_height=200,  plot_width=200)
           
p2.quad(source = source3, top='Hist', bottom=0, left='Left', right='Right',
        fill_color="#036564", line_color="#033649")
        
#########################################################################################
# Reason for POOH pie chart
########################################################################################
(REASON, ANGLE, COLOR, SUM) = piePOOH(p_sel_acct.value, p_sel_loc.value)
source4 = ColumnDataSource(data=dict(REASON=REASON, ANGLE=ANGLE, COLOR=COLOR, SUM = SUM))   
p3tips = [
        ("Reason", "@REASON"),
        ("Count", "@SUM")
        ]     
p3 = figure(plot_height=700, plot_width = 700, title="POOH reason", 
            x_range=(-1, 2.4),  tooltips="@REASON:@SUM") 
p3.wedge(x=0,y=1,radius = 1, source=source4, start_angle=cumsum('ANGLE', include_zero=True), end_angle=cumsum('ANGLE'), 
        fill_color='COLOR', legend='REASON')
p3.legend.label_text_font_size='7pt'


curdoc().add_root(column(p_title,R,p,p1, p_sel_tools, data_table, p_sel_bs, p2, p3))
#curdoc().add_root(column(p_title,p_sel_acct, p_lwd_usage))
#show(column(edDateRange, btnApplyDate, showMap(), width = 300))

#createMap(D)