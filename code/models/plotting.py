# graphing imports
import bokeh.io
import bokeh.application
import bokeh.application.handlers
import bokeh.models

import holoviews as hv

bokeh.io.output_notebook()
hv.extension('bokeh')

# ==============================================================================
# General Plotting

def scatter_df(df, x_key, y_key, plot_title='no title', x_label='X', y_label='Y'):
    x_points = df[x_key]
    y_points = df[y_key]

    p = bokeh.plotting.figure(plot_width=600,
                                  plot_height=400,
                                 title =plot_title,
                                 x_axis_label = x_label,
                                 y_axis_label = y_label)

    p.circle(x_points, y_points, color ='black')
    bokeh.io.show(p)
