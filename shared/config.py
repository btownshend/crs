#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Co-related space shared config file """


# modeling configuration
#
max_legs = 4
default_radius = 75
default_orient = 0
radius_padding = 1.5      # increased radius of circle around bodies
group_distance = 100
ungroup_distance = 150

# graphics configuration
#
graphic_modes = 1 | 2   # 1=screen; 2=osc; 3=etherdream
draw_bodies = True

inverse=True
if inverse:
    default_bkgdcolor = (0, 0, 0, 1)    # black
    default_guidecolor = (1,1,1)  # white
    default_linecolor = (1,1,1)     # white
    default_bodycolor = (.2,.2,.2)  # dk gray
else:
    default_bkgdcolor = (1, 1, 1, 1)    # white
    default_guidecolor = (.1,.1,.1)  # dark dark gray
    default_linecolor = (0,0,0)     # black
    default_bodycolor = (.1,.1,.1)  # gray

curve_segments = 12     # number of line segs in a curve
fuzzy_area_for_cells = 1

minimum_connection_distance = 12000   # this is cm sq

xmin_field = -1600
ymin_field = 0
xmax_field = 1600 # 40ft = 12.19m = 1219cm
ymax_field = 1600

# etherdream
#xmin_vector = -32768 #
#ymin_vector = -32768
#xmax_vector = 32768
#ymax_vector = 32768
# Brent's graphic system
xmin_vector = -32768
ymin_vector = -32768
xmax_vector = 32768
ymax_vector = 32768
xmin_screen = 0
ymin_screen = 0
xmax_screen = 640
ymax_screen = 480
#xmax_screen = 1440
#ymax_screen = 795

default_margin=.03

#path_unit = 20   # 20cm = about 8in
#path_unit = 40   # 20cm = about 8in
path_unit = 30   # 20cm = about 8in

# Internal config
#

osc_framerate = 25

logfile="crs-visual.log"
freq_regular_reports = 100
debug_level = 22

max_lost_patience = 10

# OSC configuration

osc_default_host = "localhost"
osc_default_port = 7011
osc_server_host = ""
osc_server_port = 7010
osc_tracking_host = ""
osc_tracking_port = ""
osc_sound_host = ""
osc_sound_port = ""
osc_conductor_host = ""
osc_conductor_port = ""
osc_graphic_host = ""
osc_graphic_port = ""
osctimeout = 0

oscpath = {
    # Incoming OSC: field state
    'ping': "/ping",
    'ack': "/ack",
    'start': "/pf/started",
    'entry': "/pf/entry",
    'exit': "/pf/exit",
    'frame': "/pf/frame",
    'stop': "/pf/stopped",
    # Incoming OSC: set params
    'set': "/pf/set/",
    'minx': "/pf/set/minx",
    'maxx': "/pf/set/maxx",
    'miny': "/pf/set/miny",
    'maxy': "/pf/set/maxy",
    'npeople': "/pf/set/npeople",
    'groupdist': "/pf/set/groupdist",
    'ungroupdist': "/pf/set/ungroupdist",
    'fps': "/pf/set/fps",
    # Incoming OSC: updates
    'update': "/pf/update",
    'leg': "/pf/leg",
    'body': "/pf/body",
    # Requests to tracker
    'dump': "/pf/dump",
    'adddest': "/pf/adddest",
    'rmdest': "/pf/rmdest",
    'body': "/pf/body",
    # Outgoing to the graphic engine
    'graph_start': "/laser/start",
    'graph_stop': "/laser/stop",
    'graph_line': "/laser/line",
    'graph_cubic': "/laser/bezier/cubic",
    'graph_arc': "/laser/arc",
    'graph_color': "/laser/set/color",
    'graph_density': "/laser/set/density",
    'graph_attr': "/laser/set/attribute",
    'graph_pps': "/laser/set/pps",
    'graph_update': "/laser/update",
    # Outgoing OSC updates from the conductor
    'attribute': "/conducter/attribute",
    'rollcall': "/conducter/rollcall",
    'event': "/conducter/event",
    'conx': "/conducter/conx",
}
