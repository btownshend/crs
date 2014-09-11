#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Module that handles OSC messages.

Co-related Space is an interactive multimedia installation that engages the
themes of presence, interaction, and place. Using motion tracking, laser light
and a generative soundscape, it encourages interactions between participants,
visually and sonically transforming a regularly trafficked space. Co-related
Space highlights participants' active engagement and experimentation with sound
and light, including complex direct and indirect behavior and relationships.

"""

__appname__ = "myoschandler.py"
__author__ = "Wes Modes (modes.io)"
__version__ = "0.1pre0"
__license__ = "GNU GPL 3.0 or later"

# core modules

# installed modules
# noinspection PyUnresolvedReferences
from OSC import OSCServer, OSCClient, OSCMessage
from time import time

# local modules
from shared.oschandler import OSCHandler
from shared import config
from shared import debug

# local Classes

# configure servers & clients properly
import socket
<<<<<<< HEAD
hostname=socket.gethostname()
print "hostname=",hostname
hostname="localhost"
ip = socket.gethostbyname(hostname)
print "ip=",ip
=======
ip = socket.gethostbyname(socket.gethostname())
>>>>>>> parent of 8d011cf... Force to production
IAM = 'conductor'
if ip == config.osc_ips_prod['localhost']:
    OSC_IPS = config.osc_ips_prod
    OSC_PORTS = config.osc_ports_prod
else:
    OSC_IPS = config.osc_ips_local
    OSC_PORTS = config.osc_ports_prod

# Constants

OSCTIMEOUT = config.osctimeout
OSCPATH = config.oscpath
REPORT_FREQ = config.report_frequency
PERSIST = 'persistent'
HAPPEN = 'happening'
HAPPENING_TYPES = ['fusion', 'transfer']
EVENT_TYPES = ['touch', 'tag']


# init debugging
dbug = debug.Debug()


class MyOSCHandler(OSCHandler):

    """Set up OSC server and other handlers."""

    def __init__(self, field=None, conductor=None):
        self.m_conductor = conductor
        osc_server = []
        osc_clients = []

        # build up connection array
        for host in OSC_IPS:
            if host == IAM:
                print "System:Config server:",(host,OSC_IPS[host],
                        OSC_PORTS[host])
                osc_server = [('server', OSC_IPS[host], OSC_PORTS[host])]
            elif host == 'localhost' or host == 'default':
                continue
            else:
                print "System:Config client:",(host,OSC_IPS[host],
                        OSC_PORTS[host])
                osc_clients.append((host, OSC_IPS[host], OSC_PORTS[host]))

        self.eventfunc = {
            # to conductor
            'conduct_dump': self.event_conduct_dump,
            'ui_condglobal': self.event_ui_condglobal,
        }

        super(MyOSCHandler, self).__init__(osc_server,
                osc_clients, field)

    def update(self, field=None, conductor=None):
        self.m_field = field
        self.m_conductor = conductor

    #
    # INCOMING to Conductor
    #

    def event_conduct_dump(self, path, tags, args, source):
        source_ip = source[0]
        if dbug.LEV & dbug.MSGS:
            print "OSC:dump req:from", source_ip
        for clientkey, client in self.m_osc_clients.iteritems():
            target_ip = client.address()[0]
            if target_ip == source_ip:
                try:
                    #TODO: Decide what we dump and dump it
                    #self.sendto(clientkey, OSCPATH('ping'), ping_code)
                    print "OSC:dump_req:from", clientkey
                except:
                    if dbug.LEV & dbug.MSGS:
                        print "OSC:dump_req:unable to reach", clientkey

    def event_ui_condglobal(self, path, tags, args, source):
        """Receive condglobal from UI.

        Sent from UI.
        args:
            frame - frame number
            cg - conductor global
        """
        #print "OSC:event_track_entry:",path,args,source
        #print "args:",args,args[0],args[1],args[2]
        #frame = args[0]
        condglobal = args[0]
        if dbug.LEV & dbug.MSGS: print "OSC:event_ui_condglobal:condglobal =",condglobal
        self.m_conductor.update(condglobal=condglobal)


    #
    # OUTGOING from Conductor
    #

    # Startup

    def honey_im_home(self):
        """Broadcast a hello message to the network."""
        self.send_to_all_clients(OSCPATH['conduct_start'],[])


    # Regular Reports

    def send_regular_reports(self):
        """Send all the reports that are send every cycle."""
        frame = self.m_field.m_frame
        if frame%REPORT_FREQ['rollcall'] == 0:
            self.send_rollcall()
        if frame%REPORT_FREQ['attrs'] == 0:
            self.send_cell_attrs()
        if frame%REPORT_FREQ['conxs'] == 0:
            self.send_conx_attr()
        if frame%REPORT_FREQ['gattrs'] == 0:
            self.send_group_attrs()
        if frame%REPORT_FREQ['events'] == 0:
            self.send_events()

    def send_rollcall(self):
        """Sends the currently highlighted cells via OSC.
        
        /conductor/rollcall [uid,action,numconx]
        """
        for id,cell in self.m_field.m_cell_dict.iteritems():
            if cell.m_visible:
                action = "visible"
            else:
                action = "hidden"
            #TODO: Should the connector count only show visble connectors?
            self.m_field.m_osc.send_downstream(OSCPATH['conduct_rollcall'],
                    [id, action, len(cell.m_conx_dict)])

    def send_cell_attrs(self):
        """Sends the current attributes of visible cells.
        
        /conductor/attr ["type",uid,value,time]
        """
        for uid, cell in self.m_field.m_cell_dict.iteritems():
            if cell.m_visible:
                for type, attr in cell.m_attr_dict.iteritems():
                    duration = time() - attr.m_createtime
                    self.m_field.m_osc.send_downstream(OSCPATH['conduct_attr'],
                            [type, uid, attr.m_value, duration])

    def send_conx_attr(self):
        """Sends the current descriptions of connectors.
        
        /conductor/conx [cid,"type",uid0,uid1,value,time]
        """
        for cid,conx in self.m_field.m_conx_dict.iteritems():
            if conx.m_cell0.m_visible and conx.m_cell1.m_visible:
                for type, attr in conx.m_attr_dict.iteritems():
                    duration = time() - attr.m_createtime
                    self.send_conx_downstream(cid, type, conx.m_cell0.m_id,
                            conx.m_cell1.m_id, attr.m_value, duration)

    def send_group_attrs(self):
        """Sends the current attributes of visible groups.
        
        /conductor/gattr ["type",gid,value,time]
        """
        for gid,group in self.m_field.m_group_dict.iteritems():
            if group.m_visible:
                for type,attr in group.m_attr_dict.iteritems():
                    duration = time() - attr.m_createtime
                    self.m_field.m_osc.send_downstream(OSCPATH['conduct_gattr'],
                            [type, gid, attr.m_value, duration])

    def send_events(self):
        """Sends notification of ongoing events.
        
        /conductor/event ["type",uid0,uid1,value,time]
        """
        for id,event in self.m_field.m_event_dict.iteritems():
            duration = time() - event.createtime
            self.m_field.m_osc.send_downstream(OSCPATH['conduct_event'],
                    [event.m_type, event.m_uid0, event.m_uid1, event.m_value, duration])

    # On-Call Messages

    def send_conx_downstream(self, cid, type, uid0, uid1, value, duration):
        if type in HAPPENING_TYPES:
            self.m_field.m_osc.send_downstream(OSCPATH['conduct_conx'],
                    [HAPPEN, type, cid, uid0, uid1, value, duration])
        elif type in EVENT_TYPES:
            self.m_field.m_osc.send_downstream(OSCPATH['conduct_event'],
                    [type, cid, uid0, uid1, value])
        else:
            self.m_field.m_osc.send_downstream(OSCPATH['conduct_conx'],
                    [PERSIST, type, cid, uid0, uid1, value, duration])

    def nix_cell_attr(self, uid, type):
        """Sends OSC messages to announce the removal of cell attr.
        
        /conductor/attr ["type",uid,0.0,time]"""
        if uid in self.m_field.m_cell_dict:
            cell = self.m_field.m_cell_dict[uid]
            if type in cell.m_attr_dict:
                attr = cell.m_attr_dict[type]
                duration = time() - attr.m_createtime
                self.m_field.m_osc.send_downstream(OSCPATH['conduct_attr'],
                        [type, uid, 0.0, duration])

    def nix_conx_attr(self, cid, type):
        """Sends OSC messages to announce the removal of connection attr.
        
        /conductor/conx ["type","subtype",cid,uid0,uid1,0.0,time]"""
        if cid in self.m_field.m_conx_dict:
            conx = self.m_field.m_conx_dict[cid]
            if type in conx.m_attr_dict:
                attr = conx.m_attr_dict[type]
                duration = time() - attr.m_createtime
                self.send_conx_downstream(cid, type, conx.m_cell0.m_id,
                        conx.m_cell1.m_id, 0.0, duration)

    def nix_conxs(self, cid):                
        """Sends OSC messages to announce the removal of a connection.
        
        /conductor/conxbreak [cid,uid0,uid1]
        """
        if cid in self.m_field.m_conx_dict:
            conx = self.m_field.m_conx_dict[cid]
            for type,attr in conx.m_attr_dict.iteritems():
                duration = time() - attr.m_createtime
                self.send_conx_downstream(cid, type, conx.m_cell0.m_id,
                        conx.m_cell1.m_id, 0.0, duration)
            self.m_field.m_osc.send_downstream(OSCPATH['conduct_conxbreak'],
                    [cid, conx.m_cell0.m_id, conx.m_cell1.m_id])
