import pandas as pd 
import numpy as np 
import matplotlib.pyplot as plt
from matplotlib import cm
from matplotlib.patches import Circle, Wedge, Rectangle
from pylab import *

class dataviz:

    def __init__(self, background  = '#1B1B2F', auxiliary_background ='#22223D', colors = ['#F54291','#2AD5F5','#F5E55B','#A81D59','#2594A8'], color_labels = '#FFFFFF', palette = 'RdPu'):
        self.background = background
        self.auxiliary_background = auxiliary_background
        self.colors = colors
        self.color_labels = color_labels
        self.palette = palette

    def generates_figure(self, axes = ['bottom', 'left', 'right', 'bottom'], axes_labels = ['x', 'y'], grid = True):
        """Generates the figure, axes and grids.
        
        Parameters
        ----------
        axes : list
            Axes list
        axes_labels : list
            Axes labels list
        grid : flag
            Grid flag
        Returns
        -------
        matplotlib.figure.Figure
        matplotlib.axes._subplots.AxesSubplot
        """

        # generates the figure and axes
        fig, ax = plt.subplots(facecolor = self.background)
        # set background color
        ax = plt.gca()
        ax.set_facecolor(self.background)

        all_axes = ['bottom', 'left', 'right', 'top']
        delete_axes = set(all_axes) - set(axes)
        all_axes_labels = ['x', 'y']
        delete_axes_labels = set(all_axes_labels) - set(axes_labels)

        # axes configuration
        # removes the bottom and left axes
        for param in delete_axes:
            ax.spines[param].set_visible(False)
        # changes the color of the active axes
        for param in axes:
            ax.spines[param].set_color(self.color_labels)
        # changes the color of the labels 
        for i in axes_labels:
            ax.tick_params(axis = i, colors = self.color_labels)
        # changes the color of the labels
        for i in delete_axes_labels:
            ax.tick_params(axis = i, colors = self.background)
        
        # grid configuration
        if grid:
            # add the grids
            plt.grid(color = self.color_labels, linestyle = ':', linewidth = 2, alpha = 0.1)

        return fig, ax

    def line_chart(self, x, y, legend = None, axes = ['bottom', 'left'], axes_labels = ['x','y'], grid = True, fname = None):
        """Plots line graph with n lines.
        
        Parameters
        ----------
        x : list
            List with x values
        y : list
            List with y values
        legend : list
            List with the legends 
        axes : list
            Axes list
        axes_labels : list
            Axes labels list
        grid : boolean
            Grid flag
        """

        fig, ax = self.generates_figure(axes = axes, grid = grid, axes_labels= axes_labels)

        # plots the lines
        for i in range(0, len(y)):
            plt.plot(x[i],y[i], color = self.colors[i])
        
        # definition of shadow resources
        n_shades = 10
        diff_linewidth = 1.0
        alpha_value = 0.4 / n_shades

        # generates the neon effect
        for i in range(0, len(x)):
            for n in range(1, n_shades+1):
                plt.plot(x[i],y[i], linewidth = 2+(diff_linewidth*n), alpha = alpha_value, color = self.colors[i])

        # generates the shadow below the lines
        for i in range(0, len(x)):
            ax.fill_between(x = x[i], y1 = y[i],y2 = np.array(y[i]).min(), color = self.colors[i], alpha = 0.08)

        # generates the legend
        if legend == None:
            aux_legend = []
            for i in range(0, len(x)):
                aux_legend.append(f'line {i+1}')
            leg = ax.legend(aux_legend, frameon = False)
        else:
            leg = ax.legend(legend, frameon = False)

        # change de color legend   
        for text in leg.get_texts():
            plt.setp(text, color = self.color_labels)

        # set x and y limits
        minn = np.array(x).min() - 0.2*np.array(x).min()
        maxx = np.array(x).max() + 0.2*np.array(x).max()
        plt.xlim(minn,maxx)

        minn = np.array(y).min() - 0.2*np.array(y).min()
        maxx = np.array(y).max() + 0.2*np.array(y).max()
        plt.ylim(minn,maxx)

        if(fname != None):
            plt.savefig(fname, transparent = True)
        return fig 

    def bar_chart(self, labels, values, legend = None, axes = [], axes_labels = ['x'], grid = False, fname = None):
        """Plots bar chart with n groups.
        
        Parameters
        ----------
        labels : list
            Lista(s) com os grupos.
        values : list
            Lista(s) com as quantidades por rupo.
        legend : list
            Lista com as legendas
        axes : list
            Axes list
        axes_labels : list
            Axes labels list
        grid : boolean
            Grid flag
        """

        ax = self.generates_figure(axes = axes, grid = grid, axes_labels= axes_labels)

        # set the width of the bars
        width = 0.8/len(values)
        x = np.arange(len(labels))

        # checks the position of the bars
        if len(values)%2 != 0:
            aux_x = np.arange(-len(values)+len(values)/2,len(values)-len(values)/2, dtype = float) * width
        else:
            aux_x = np.arange(-len(values)/2,(len(values))/2, dtype = float)* width

        # plots the bars
        for i in range(0, len(values)):
            bar = ax.bar(x+aux_x[i], values[i], width, color = self.colors[i], linewidth = 0.5)
        
        # Set the labels
        ax.set_xticks(x-width/2)
        ax.set_xticklabels(labels)

        # generates the legend
        if legend == None:
            aux_legend = []
            for i in range(0, len(x)):
                aux_legend.append(f'label {i+1}')
            leg = ax.legend(aux_legend, frameon = False)
        else:
            leg = ax.legend(legend, frameon = False)
        
        # changes the legends color
        for text in leg.get_texts():
            plt.setp(text, color = self.color_labels)
        
        # set y limits
        minn = np.array(values).min()
        if minn > 0:
            minn = 0
        else:
            minn = np.array(values).min() - 0.2*np.array(values).min() 

        maxx = np.array(values).max() + 0.2*np.array(values).max() 
        plt.ylim(minn,maxx)

        if(fname != None):
            plt.savefig(fname, transparent = True)
        return fig 

    def progress_chart(self, value, circles = 4, fname = None):
        """Plots gauge chart.
        
        Parameters
        ----------
        value : float
            Gauge value
        circles : int
            Number of circles
        """

        # generates the figure
        fig, ax = plt.subplots(facecolor = self.background)
        ax = plt.gca()
        ax.set_facecolor(self.background)
        size = 0.1

        # circles configuration
        startingRadius = 0.7 + (0.2 * circles)
        percentage = value
        remainingPie = 100-value
        donut_sizes = [percentage, remainingPie]

        # plots the pies
        for i in range(1,circles + 1):
            plt.pie(donut_sizes, radius = startingRadius, startangle = 90, colors = [self.colors[i%2],self.auxiliary_background], wedgeprops ={'edgecolor': self.background, 'linewidth': 4})
            startingRadius -= 0.12
            percentage *= 0.5
            remainingPie *= 1
            donut_sizes = [percentage, remainingPie]

        # plots the cicle in the center
        circle = plt.Circle((0,0), startingRadius, color = self.background)
        p = plt.gcf()
        p.gca().add_artist(circle)
        ax.annotate(f'{value} %', (0,0), fontsize = 36, color = self.color_labels, va = 'center', ha = 'center', family = 'monospace')

        if(fname != None):
            plt.savefig(fname, transparent = True)
        return fig 
      
    def horizontal_bar_chart(self, labels, values, fname = None):
        """Plots horizontal bar with n groups.
        
        Parameters
        ----------
        labels : list
            Groups list
        values : list
            Values list
        """

        # generates the figure
        fig, ax = plt.subplots(facecolor = self.background, figsize =(7, len(labels)))
        ax = plt.gca()
        ax.set_facecolor(self.background)

        # remove the axes
        for param in ['top', 'right', 'bottom', 'left']:
            ax.spines[param].set_visible(False)
        # change the color of the axes label
        for i in ['x','y']:
            ax.tick_params(axis = i, colors = self.color_labels)
        
        # remove labels of x axis
        ax.set_xticks([])
        
        # define the max value in the list
        maxx = 0
        for i in values:
            if i > maxx:
                maxx = i
        category = []

        # generates the labels of y axix
        for x in range(0,len(labels)):
            category.append(f'{labels[x]} - {values[x]}')

        # plot the background bar
        ax.barh(category, maxx + maxx/2, color = self.auxiliary_background , height = 0.2)
        # plot the bars
        ax.barh(category, values, color = self.colors, height = 0.2)

        if(fname != None):
            plt.savefig(fname, transparent = True)
        return fig 

    def gauge(self, value,  title = '', fname = None):
        """Plots gauge chart.
        
        Parameters
        ----------
        value : float
            float value
        title : str
            gauge title
        """

        # generates the figure
        fig, ax = plt.subplots(facecolor = self.background)
        ax = plt.gca()
        ax.set_facecolor(self.background)

        # generates color list from the palette
        cmap = cm.get_cmap(self.palette, 540)
        # get hex format colors
        colors = []
        for i in range(cmap.N):
            rgb = cmap(i)[:3]
            colors.append(matplotlib.colors.rgb2hex(rgb))
        
        # cuts the palette collor from the middle
        colors[1000:]
        colors = colors[::-1]
        value_ = str(value) + ' %'
        value = 225 -2.7*value

        # create the unit arches
        start = np.linspace(-45,225,270, endpoint = True)[0:-1]
        end = np.linspace(-45,225,270, endpoint = True)[1::]
        ang_range = np.c_[start,end]

        # create the arches
        patches = []
        for ang, c in zip(ang_range, colors):
            patches.append(Wedge((0.,0.), .4, *ang, facecolor = self.background, lw = 2))
            if ang.max() < value:
                patches.append(Wedge((0.,0.), .4, *ang, width = 0.07, facecolor = self.auxiliary_background, lw = 2))
            else:
                patches.append(Wedge((0.,0.), .4, *ang, width = 0.07, facecolor = c, lw = 2))

        # plots the archers
        [ax.add_patch(p) for p in patches]

        # add the minimum value
        ax.text(0.42 * np.cos(np.radians(225)), 0.42* np.sin(np.radians(225)), 0, horizontalalignment = 'center', verticalalignment = 'center', fontsize = 11, fontweight = 'ultralight', color = self.color_labels, rotation = np.degrees(np.radians(225) * np.pi / np.pi - np.radians(90)))

        # add the maximum value
        ax.text(0.42 * np.cos(np.radians(315)), 0.42* np.sin(np.radians(315)), 100, horizontalalignment = 'center', verticalalignment = 'center', fontsize = 11, fontweight = 'ultralight', color = self.color_labels, rotation = np.degrees(np.radians(315) * np.pi / np.pi - np.radians(90)))
        
        # writes the title
        ax.text(0, -0.38, title, horizontalalignment = 'center', verticalalignment = 'center', fontsize = 12, fontweight = 'bold', color = self.color_labels, fontfamily = 'sans-serif')

        # writes the value
        ax.text(0, -.3, value_, horizontalalignment = 'center', verticalalignment = 'center', fontsize = 32, fontweight = 'book', color = self.color_labels, fontfamily = 'sans-serif')

        # draw the arrow
        ax.arrow(0, 0, 0.32 * np.cos(np.radians(value)), 0.32 * np.sin(np.radians(value)),width=0.01, head_width=0.01, head_length=0.1, fc=self.color_labels, ec=self.color_labels, fill = True)
        
        # draw the circle inside the arrow
        ax.add_patch(Circle((0, 0), radius = 0.02, facecolor = self.color_labels))
        ax.add_patch(Circle((0, 0), radius = 0.01, facecolor = self.auxiliary_background, zorder = 12))

        # configure the display area
        ax.set_frame_on(False)
        ax.axes.set_xticks([])
        ax.axes.set_yticks([])
        ax.axis('equal')
        plt.tight_layout()

        if(fname != None):
            plt.savefig(fname, transparent = True)
        return fig 