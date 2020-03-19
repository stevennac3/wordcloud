'''Steven Nacinovich
   Geocomputation Project
   12/19/19
   Generating Wordclouds in Python'''
from wordcloud import WordCloud, STOPWORDS
from PIL import Image
import matplotlib .pyplot as plt
import pandas as pd
import geopandas as gpd
from shapely.geometry import Point, Polygon
from fiona.crs import from_epsg
import numpy as np

# reading the files into the script
airbnb_shp = gpd.read_file(r"E:\GeoComp I\Final\airbnb.shp", index_col=0)
# airbnb_rpj= from_epsg(2263) #setting the airbnb crs
zipcodes = gpd.read_file((r"E:\GeoComp I\Final\zip\ZIP_CODE_040114.shp"))
nbhood = gpd.read_file((r"E:\GeoComp I\Final\nbhood\nynta.shp"))
print(airbnb[["name", "host_id"]].head())
# nbhood_rpj = from_epsg(2263)
# ensuring the values can be read through object names
'''
print(airbnb.head())
print(zipcodes.head())
# print coordinate systems
print(airbnb_rpj)
print(type(airbnb))
print(zipcodes.crs)
# They are different, will need to be re-projected
# Point = object that describes lat/longs, :7 refers to list of fields in csv
geometry = [Point(xy) for xy in zip( airbnb['longitude'],
                                     airbnb['latitude'])]
geometry[:7]
# creating new object into a GeoDataFrame
geo_airbnb = gpd.GeoDataFrame(airbnb,
                              crs=airbnb_rpj, geometry=geometry)
geo_nbhood = gpd.GeoDataFrame(nbhood,
                              crs = nbhood_rpj)
print(geo_airbnb.head())
print(type(geo_airbnb))
print(type(nbhood))
print(geo_airbnb.crs)
print(nbhood.crs)
# Here, using a spatial join for airbnb's in neighborhoods
airbnb_by_zip = gpd.sjoin(geo_airbnb, geo_nbhood, op = 'within', how = 'inner')
print (airbnb_by_zip.head())
#saving a csv of the join to examine
airbnb_by_zip.to_csv("E:\GeoComp I\Final\Airbnb_zip.csv")
'''
'''Reading in the airbnb data, creating csv of result'''
airbnb = pd.read_csv(r"E:\GeoComp I\Final\AB_NYC_2019.csv", index_col=0)

# creating object borough, grouping by specific column
borough = airbnb.groupby("neighbourhood_group")

# Summary of all boroughs
print(borough.describe().head())
# Finding the median price for each borough airbnb
avg_boro_price = borough.median().sort_values(by="price", ascending=True)
print(avg_boro_price)
avg_boro_price.to_csv(r"E:\GeoComp I\Final\boro_price.csv")
# exported as a csv

# Wordcloud: opening csv file, making text a list of all description(airbnb names)
'''
text = []
with open("E:\GeoComp I\Final\AB_NYC_2019.csv", encoding="utf8") as f:
    reader = csv.reader(f)
    text = ' '.join([name[1] for name in reader])'''
# referencing the position[1] in the csv file.

# opening the file with pandas
text_desc = pd.read_csv("E:\GeoComp I\Final\AB_NYC_2019.csv", encoding="utf8")

# creating stopword list:
stopwords = set(STOPWORDS)
stopwords.update(("room", "bedroom", "br", "apt", "apartment",
                  "br", "2br", 'bdrm', '1br', "brooklyn","bronx", "queens", "staten island", "manhattan"))
# removing un-helpful descriptor words

# read in all borough masks
bk_mask = np.array(Image.open(r"E:\GeoComp I\Final\boroughs\Brooklyn.PNG"))
bx_mask = np.array(Image.open(r"E:\GeoComp I\Final\boroughs\Bronx.PNG"))
mn_mask = np.array(Image.open(r"E:\GeoComp I\Final\boroughs\Manhattan.PNG"))
qn_mask = np.array(Image.open(r"E:\GeoComp I\Final\boroughs\Queens.PNG"))
si_mask = np.array(Image.open(r"E:\GeoComp I\Final\boroughs\StatenIsland.PNG"))

#airbnb logo mask

logo_mask = np.array(Image.open(r"E:\GeoComp I\Final\airbnb_logo.png"))
print(logo_mask)


# creating the mask, defining the border based off pixel value swap 255 to 0
def transform_format(val):
    if np.any(val == 0):
        return 0
    elif np.any(val != 0):
        return 255
# airbnb logo had white logo with colored background (inverse the function)
def logo_format(val):
    if np.any(val != 0):
        return 0
    elif np.any(val == 0):
        return 255
# this function is making sure if the array value is 0, making sure outline is the whitespace border.
# transforming queens mask into a new one that will work properly...

#transformed formats, allowing for proper shape
# brooklyn
transformed_brooklyn_mask = np.ndarray((bk_mask.shape[0], bk_mask.shape[1]), np.int32)
for i in range(len(bk_mask)):
    transformed_brooklyn_mask[i] = list(map(transform_format, bk_mask[i]))
# bronx
transformed_bronx_mask = np.ndarray((bx_mask.shape[0], bx_mask.shape[1]), np.int32)
for i in range(len(bx_mask)):
    transformed_bronx_mask[i] = list(map(transform_format, bx_mask[i]))
# manhattan
transformed_manhattan_mask = np.ndarray((mn_mask.shape[0], mn_mask.shape[1]), np.int32)
for i in range(len(mn_mask)):
    transformed_manhattan_mask[i] = list(map(transform_format, mn_mask[i]))
# queens
transformed_queens_mask = np.ndarray((qn_mask.shape[0], qn_mask.shape[1]), np.int32)
for i in range(len(qn_mask)):
    transformed_queens_mask[i] = list(map(transform_format, qn_mask[i]))
# staten island
transformed_staten_mask = np.ndarray((si_mask.shape[0], si_mask.shape[1]), np.int32)
for i in range(len(si_mask)):
    transformed_staten_mask[i] = list(map(transform_format, si_mask[i]))
# logo mask
transformed_logo_mask = np.ndarray((logo_mask.shape[0], logo_mask.shape[1]), np.int32)
for i in range(len(logo_mask)):
    transformed_logo_mask[i] = list(map(logo_format, logo_mask[i]))
# Join all reviews of each borough, separating the reviews
brooklyn = " ".join([str(borough) for borough in text_desc[text_desc['neighbourhood_group'] == 'Brooklyn'].name])
bronx = " ".join([str(borough) for borough in text_desc[text_desc['neighbourhood_group'] == 'Bronx'].name])
manhattan = " ".join([str(borough) for borough in text_desc[text_desc['neighbourhood_group'] == 'Manhattan'].name])
queens = " ".join([str(borough) for borough in text_desc[text_desc['neighbourhood_group'] == 'Queens'].name])
staten_island = " ".join([str(borough) for borough in text_desc[text_desc['neighbourhood_group'] == 'Staten Island'].name])
logo = " ".join([str(borough) for borough in text_desc.name])

wordcloud_bk = WordCloud(stopwords=stopwords, max_words=200, background_color='black', contour_width=0.25, contour_color='white',
                         min_font_size=6, max_font_size=24, colormap='Reds', mask=transformed_brooklyn_mask).generate(brooklyn.lower())

wordcloud_bx = WordCloud(stopwords=stopwords, max_words=150, background_color='black', contour_width=0.25, contour_color='white',
                         min_font_size=8, max_font_size=24, colormap='Reds', mask=transformed_bronx_mask).generate(bronx.lower())

wordcloud_mn = WordCloud(stopwords=stopwords, max_words=250, background_color='black', contour_width=0.25, contour_color='white',
                         min_font_size=6, max_font_size=24, colormap='Reds', mask=transformed_manhattan_mask).generate(manhattan.lower())

wordcloud_qn = WordCloud(stopwords=stopwords, max_words=250, background_color='black', contour_width=0.25, contour_color='white',
                         min_font_size=6, max_font_size=24, colormap='Reds', mask=transformed_queens_mask).generate(queens.lower())

wordcloud_si = WordCloud(stopwords=stopwords, max_words=150, background_color='black', contour_width=0.25, contour_color='white',
                         min_font_size=8, max_font_size=24, colormap='Reds', mask=transformed_staten_mask).generate(staten_island.lower())

wordcloud_logo = WordCloud(stopwords=stopwords, max_words=3000, background_color='black',
                           contour_width=1.25, relative_scaling=0.5, min_font_size=8, max_font_size=20,
                           colormap='Reds', contour_color='white', mask=transformed_logo_mask).generate(logo.lower())
# show the wordcloud
# image_colors = ImageColorGenerator('Reds') #object image_colors for the mask
plt.figure(figsize=[30, 30])
plt.imshow(wordcloud_bx, interpolation='bilinear')
plt.axis = ('off')
plt.xticks([]), plt.yticks([])
plt.title('Bronx', color='black', size='xx-large', family='sans-serif')
plt.savefig(r"E:\GeoComp I\Final\boroughs\bronx_bnb.PNG")
plt.show()
