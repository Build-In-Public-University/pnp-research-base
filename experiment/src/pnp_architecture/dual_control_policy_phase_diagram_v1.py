from fractions import Fraction

def costs(p):
 return {'immediate':1+100*min(p,1-p),'touch':2+10*p,'inspect':6}
def best(p):return min(costs(p),key=lambda k:(costs(p)[k],k))
def intervals(grid):
 out=[];start=grid[0];prev=grid[0];last=best(start)
 for p in grid[1:]:
  cur=best(p)
  if cur!=last:out.append((last,start,prev));start=p;last=cur
  prev=p
 out.append((last,start,grid[-1]));return out
def experiment(step=0.001):
 grid=[round(i*step,10) for i in range(round(1/step)+1)];return {'grid_step':step,'intervals':intervals(grid),'thresholds':{'immediate_touch':1/90,'touch_inspect':.4,'inspect_immediate':.95},'checks':{p:{'best':best(p),'costs':costs(p)} for p in (.0,.01,.012,.1,.399,.4,.401,.949,.95,.951,1.0)},'units':'synthetic modeled cost'}
