"""
Perimeter/Area Ratio Spatial Dissimilarity based Segregation Metrics
"""

__author__ = "Renan X. Cortes <renanc@ucr.edu> and Sergio J. Rey <sergio.rey@ucr.edu>"

import numpy as np
import pandas as pd
#import libpysal
from util import _return_length_weighted_w
from dissimilarity import _dissim
from sklearn.metrics.pairwise import manhattan_distances

__all__ = ['Perimeter_Area_Ratio_Spatial_Dissim']


def _perimeter_area_ratio_spatial_dissim(data, group_pop_var, total_pop_var, standardize = True):
    """
    Calculation of Perimeter/Area Ratio Spatial Dissimilarity index

    Parameters
    ----------

    data          : a geopandas DataFrame with a 'geometry' column.
    
    group_pop_var : string
                    The name of variable in data that contains the population size of the group of interest
                    
    total_pop_var : string
                    The name of variable in data that contains the total population of the unit
                    
    standardize   : boolean
                    A condition for standardisation of the weights matrices. 
                    If True, the values of cij in the formulas gets standardized and the overall sum is 1.

    Attributes
    ----------

    statistic : float
                Perimeter/Area Ratio Spatial Dissimilarity Index

    Notes
    -----
    Based on Wong, David WS. "Spatial indices of segregation." Urban studies 30.3 (1993): 559-572.

    """
    if (type(standardize) is not bool):
        raise TypeError('std is not a boolean object')
    
    D = _dissim(data, group_pop_var, total_pop_var)
    
    data = data.rename(columns={group_pop_var: 'group_pop_var', 
                                total_pop_var: 'total_pop_var'})
    
    # If a unit has zero population, the group of interest frequency is zero
    data = data.assign(pi = np.where(data.total_pop_var == 0, 0, data.group_pop_var/data.total_pop_var))

    if not standardize:
        cij = _return_length_weighted_w(data).full()[0]
    else:
        cij = _return_length_weighted_w(data).full()[0]
        cij = cij / cij.sum()
   
    peri = data.length
    ai   = data.area
    
    aux_sum = np.add(np.array(list((peri / ai))), np.array(list((peri / ai))).reshape((len(list((peri / ai))),1)))
    
    max_pa = max(peri / ai)
    
    num = np.multiply(np.multiply(manhattan_distances(data[['pi']]), cij), aux_sum).sum()
    den = 4 * max_pa
    
    PARD = D - (num / den)
    PARD
    
    return PARD


class Perimeter_Area_Ratio_Spatial_Dissim:
    """
    Calculation of Perimeter/Area Ratio Spatial Dissimilarity index

    Parameters
    ----------

    data          : a geopandas DataFrame with a 'geometry' column.
    
    group_pop_var : string
                    The name of variable in data that contains the population size of the group of interest
                    
    total_pop_var : string
                    The name of variable in data that contains the total population of the unit
                    
    standardize   : boolean
                    A condition for standardisation of the weights matrices. 
                    If True, the values of cij in the formulas gets standardized and the overall sum is 1.
        
    Attributes
    ----------

    statistic : float
                Perimeter/Area Ratio Spatial Dissimilarity Index
        
    Examples
    --------
    In this example, we will calculate the degree of perimeter/area ratio spatial dissimilarity (PARD) for the Riverside County using the census tract data of 2010.
    The group of interest is non-hispanic black people which is the variable nhblk10 in the dataset.
    
    Firstly, we need to read the data:
    
    >>> This example uses all census data that the user must provide your own copy of the external database.
    >>> A step-by-step procedure for downloading the data can be found here: https://github.com/spatialucr/osnap/tree/master/osnap/data.
    >>> After the user download the LTDB_Std_All_fullcount.zip and extract the files, the filepath might be something like presented below.
    >>> filepath = '~/data/std_2010_fullcount.csv'
    >>> census_2010 = pd.read_csv(filepath, encoding = "ISO-8859-1", sep = ",")
    
    Then, we filter only for the desired county (in this case, Riverside County):
    
    >>> df = census_2010.loc[census_2010.county == "Riverside County"][['trtid10', 'pop10','nhblk10']]
    
    Then, we read the Riverside map data using geopandas (the county id is 06065):
    
    >>> map_url = 'https://raw.githubusercontent.com/renanxcortes/inequality-segregation-supplementary-files/master/Tracts_grouped_by_County/06065.json'
    >>> map_gpd = gpd.read_file(map_url)
    
    It is necessary to harmonize the data type of the dataset and the geopandas in order to work the merging procedure.
    Later, we extract only the columns that will be used.
    
    >>> map_gpd['INTGEOID10'] = pd.to_numeric(map_gpd["GEOID10"])
    >>> gdf_pre = map_gpd.merge(df, left_on = 'INTGEOID10', right_on = 'trtid10')
    >>> gdf = gdf_pre[['geometry', 'pop10', 'nhblk10']]
    
    The value is estimated below.
    
    >>> perimeter_area_ratio_spatial_dissim_index = Perimeter_Area_Ratio_Spatial_Dissim(gdf, 'nhblk10', 'pop10')
    >>> perimeter_area_ratio_spatial_dissim_index.statistic
    0.31260876347432687
            
    Notes
    -----
    Based on Wong, David WS. "Spatial indices of segregation." Urban studies 30.3 (1993): 559-572.
    
    """

    def __init__(self, data, group_pop_var, total_pop_var, standardize = True):

        self.statistic = _perimeter_area_ratio_spatial_dissim(data, group_pop_var, total_pop_var, standardize)