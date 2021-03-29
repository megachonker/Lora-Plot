# This Python file uses the following encoding: utf-8
import sys
import geopandas as gpd
import matplotlib.pyplot as plt
import tilemapbase
import numpy

#on import le  cvs

fname=str(sys.argv[1])

df = gpd.read_file(fname)

#on convertie les coordonnée  en point
gdf = gpd.GeoDataFrame(df, geometry=gpd.points_from_xy(df.lon,df.lat))
gdf = gdf.set_crs("EPSG:4326")
gdf = gdf.to_crs("EPSG:3857")


#on se log  au  serveur de  carte
tilemapbase.start_logging()
#idk
tilemapbase.init(create=True)
#on download  une map pour la size de   gdf
#buffer  la taille des icone  annotation
extent = tilemapbase.extent_from_frame(gdf, buffer = 25)


#espace de point
fig, ax = plt.subplots(figsize=(25,25))
#on veux charger le backgroud
plotter = tilemapbase.Plotter(extent, tilemapbase.tiles.build_OSM(), width=1000)
#on veux dessiner le fond de cart openstreatmap
plotter.plot(ax)
#on défini les limite de la carte
bounding_box = [gdf["geometry"].x.min(), gdf["geometry"].x.max(), gdf["geometry"].y.min(), gdf["geometry"].y.max()]
ax.set_xlim(bounding_box[0]/1.00003, bounding_box[1]*1.00003)
ax.set_ylim(bounding_box[2]/1.00003, bounding_box[3]*1.00003)

#force un ratio 16/9
#ax.set_aspect(16/9)

#gdf.plot(ax=ax,color="red",color=(numpy.exp(-1/gdf["signal"].astype(float)*150)+100))
ax.scatter(
                    gdf["geometry"].x,
                    gdf["geometry"].y,
                    c=(gdf["rssi"].astype(float)),
                    )
#.-1/int(gdf["signal"])
#print(gdf)
#plt.savefig('world.jpg')
ax.axis('off')
fig.savefig(fname+".png", bbox_inches='tight',pad_inches = 0)