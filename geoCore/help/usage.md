# geoCore - QGIS plugin for creating graphical representations of geoscientific drillings.

*Authors Gerrit Bette (1); Moritz Mennenga (2)*

1. T-Systems on site services GmbH
2. Lower Saxony Institute for Historical Coastal Research, Viktoriastr. 26/28, 26386 Wilhelmshaven

The QGIS Plugin geoCore is under development by [T-Systems on site services GmbH](https://www.t-systems-onsite.de/) based on the idea of the [Lower Saxony Institute for Historical Coastal Research Wilhelmshaven (NIhK)](www.nihk.de).

## Update Warning
**Please backup your geoCore.yml, config.yml and the additional .svg files before you update the plugin. If not, the files will be deleted due to the QGIS updating process!**

## Aim

The aim of the plugin is to create a flexible and easy way to display and export drilling profiles according to your own layout in QGIS. It allows the user to account for the different types of representation and across different sciences. This means that the uniformly processed data can be used by different users according to their specifications.

An example data set is available in the [github-Repository](https://github.com/t-systems-on-site-services-gmbh/geoCore).


## Preconditions

In the following, the necessary basics and specifications are presented to ensure that the plugin can be used.

### Data

**[Download example data](https://github.com/t-systems-on-site-services-gmbh/geoCore/tree/master/example_data)**

As a basis for displaying coring data, the plugin requires a specific format. Two sets are required. The former is a vector-layer whose attribute table must be organized as follows:

ID |	xcoord |	ycoord |	zcoord |	name | 
| --- |-------------|-------------|-------------|-------------|
1 |	32485574.7100 |	5949969,4730 |	1.459 |	core 1
2 |	32485583.1799 |	5950059.7089 |	1.308 |	core 2
3 |	32485604.7038 |	5950117.1169 |	1.400 |	core 3


The coordinates must be in a geographic coordinate system with a metric scale.

A text file is also required in which the data on the individual layers of the boreholes are available (layer data). To define the name of the text file, that will be used with the shapefile you have to define it in the config.yml in the plugin folder. The content of the columns petrography, description and color are used to define the display of the profiles and are linked to geoCore.yml, the adaptation of which is defined in the following section, Layout-Table. The layer data must be structured as follows. The ID corresponds to the ID in the master data table:

ID |	layerno |	petrography |	facies |	comment |	colour |	depth_from |	depth_to |	group
| --- |-------------|-------------|-------------|-------------|-------------|-------------|-------------|-------------|
1 |	1 |	S(u4, h, lam, as) |	st ||		gr |	0 |	10 |	1
1 |	2 |	T(u1, wood) |	it ||		br |      	10 	| 30 |	2
1 |	3 |	U(fs) ||		|	ge |              	30 |	35 |	3
1 |	4 |	G 		|||	gru |	                  35 |	36.5 |	4
2 |	1 |	S(u2) |||			gr |              	0 |	20 |	1
2 |	2 |	T 		|||	br |	                  20 |	43 |	2
2 |	3 |	U(t1) |||			ge |              	43 |	58 |	3
2 |	4 |	H 		|||	gru |	                  58 |	90 |	4
3 |	1 |	S(u2) |||			gr |              	0 |	20 |	1
3 |	2 |	T 		|||	br |	                  20 |	43 |	2
3 |	3 |	U(t1) |||			ge |              	43 |	58 |	3
3 |	4 |	H 		|||	gru |	                  58 |	90 |	4



*    ID -> Key value that is also available in the drilling table
*    layerno -> layernumber (unique per hole)
*   petrography -> description of the shift. The definition is determined by the **geoCore.yml** (see below)
*    facies -> only for the description text
*    comment -> is used in addition to the description of the layer on the drilling profile
*    colour -> Description of the color of the layer. The definition is determined by the **geoCore.yml** (see below)
*    depth_from -> Top of the layer in centimeters below the terrain surface
*    depth_to -> Lower edge of the layer in centimeters below the terrain surface
*    group -> Value for grouping layers of different profiles (acre in profile 1 corresponds to acre in profile 2)


### Layout-Table

The layout is defined by **geoCore.yml** in the plugin directory. This is divided into three areas.

#### boxes
In  `boxes`, the width of the boxes that represent a layer is defined based on the entry in *petrography*. In this step the value that is not in brackets is used. `longname` is used for the entry in the description field next to the layer of the profile.


ID |	layerno |	petrography
| --- |-------------|-------------
1 |	1 |	**S**(u4, h, lam, as)

In the yml file, the abbreviation is used to define the real name, which can be found in the description, and the width of the box.


```{yaml}

boxes:
    S: #shortname
        longname: Sand
        width: 1.5
    T: #shortname
        longname: Ton
        width: 1.0
        
```

### description

The `description` field is also defined by the *petrography* column, but the values in the brackets are used here. Their definition can also be found in geoCore.yml. `longname` defines the text module that is displayed next to the profile in the description field. `texture` contains the link to .svg vector graphics, which are stored in the symbols subdirectory. If available, these are inserted in the respective boxes of the layers (this function is still under construction).

ID |	layerno |	petrography
| --- |-------------|-------------
1 |	1 |	S**(u4, h, lam, as)**

```{yaml}

descriptions:
    u4: #shortname
        longname: stark schluffig
    h: #shortname
        longname: humos
    fs: #shortname
        longname: feinsandig
    lam: #shortname
        longname: laminiert
        texture: symbols/lam.svg
    as: #shortname
        longname: articulated shell
        
```

### colors
Also defined by the geoCore.yml is the *color* in which the respective box is displayed. Not shown, but `longname` is available for better traceability. In the field `code` the RGB value of the respective color is given. Predefined colors from color charts can also be used.

ID |	layerno |	color
| --- |-------------|-------------
1 |	1 |	**gr**

```{yaml}

colors:
    gr: #shortname
        longname: grau
        code: "#c9c8c8"
    br: #shortname
        longname: braun
        code: "#b6afa1"
        
```

## Usage

*The plugin is still under development - see [issues](https://github.com/t-systems-on-site-services-gmbh/geoCore/issues)*

If all files are available as described and the definitions are entered as required, the plug-in can be used. First, the shape file and the corresponding text file with the layer data must be imported. It is now possible to display a single or multiple profiles. To do this, select all the desired boreholes with the QGIS Selection Tool and click on the geoCore icon (or choose the menu entry Plugins -> geoCore -> Show drilling profile). A dialog opens showing the drilling profile(s). geoCore’s user interface is kept very simple and should be self-explanatory. A right click on the dialog opens the context menu which allows to export the profile as SVG. Furthermore you can rearrange the drilling profiles if you are showing multiple at once. If the *group* parameter contains an entry for several profiles, the layers are automatically connected. Using the mouse wheel you can zoom in and out. The middle mouse button allows for panning. This is just like navigating the QGIS map.

### Context menu
A right click on the dialog opens the context menu. You have the following options:

*    Scale: Changing the scales of x- and y-axis
*    Export as: Export the representation as
*    North -> South ...: Change the order of the corings
*    Manual: Open the manual
*    About: Informations about the license and the citation

