import numpy
from pyspark import SparkContext

def Diffusion(ncells):
    sc = SparkContext('spark://ip-172-31-38-169.eu-central-1.compute.internal:7077',f'Diffusion for {ncells} cells')
    leftX=-1000.
    rightX=+1000.
    sigma=300.
    ao=1.
    coeff=.375
    dx = (rightX-leftX)/(ncells-1)
    def tempFromIdx(i):
        x = leftX + dx*i + dx/2
        return (i, ao*numpy.exp(-x*x/(2.*sigma*sigma)))

    def interior(ix):                       
        return (ix[0] > 0) and (ix[0] < ncells-1)

    def stencil(item):
        i,t = item
        vals = [ (i,t) ]
        cvals = [ (i, -2*coeff*t), (i-1, coeff*t), (i+1, coeff*t) ]
        return vals + list(filter(interior, cvals))
    
    temp = map(tempFromIdx,range(ncells))
    data= sc.parallelize(temp)
    for i in range(50):
        stencilParts = data.flatMap(stencil)
        data = stencilParts.reduceByKey(lambda x,y:x+y)
    result = data.collect()
    sc.stop()
    
    return result
