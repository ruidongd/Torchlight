import MalmoPython
import os
import sys
import time
import json
import math

sys.stdout = os.fdopen(sys.stdout.fileno(), 'w', 0)  # flush print output immediately

trial6x6 = 	'''	
				<DrawingDecorator>
					<DrawCuboid x1="0" y1="39" z1="0" x2="5" y2="39" z2="5" type="obsidian"/>
				</DrawingDecorator>
			'''
			
trial8x8 = 	'''	
				<DrawingDecorator>
					<DrawCuboid x1="0" y1="39" z1="0" x2="7" y2="39" z2="7" type="obsidian"/>
				</DrawingDecorator>
			'''
			
trial10x10 = 	'''	
				<DrawingDecorator>
					<DrawCuboid x1="0" y1="39" z1="0" x2="9" y2="39" z2="9" type="obsidian"/>
				</DrawingDecorator>
			'''

def GetMissionXML( trial ):
	# generatorString = 2;0;127; for MC v1.7 and below
	
	return 
	'''
		<?xml version="1.0" encoding="UTF-8" ?>
		<Mission xmlns="http://ProjectMalmo.microsoft.com" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance">
		<About>
			<Summary>Light the way!</Summary>
		</About>
		<ServerSection>
				<ServerInitialConditions>
					<Time>
						<StartTime>14000</StartTime>
						<AllowPassageOfTime>false</AllowPassageOfTime>
					</Time>
					<Weather>clear</Weather>
				 </ServerInitialConditions>
				 <ServerHandlers>
					  <FlatWorldGenerator generatorString="3;minecraft:air;127;"/>
					  ''' + trial + '''
					  <ServerQuitFromTimeUp timeLimitMs="30000"/>
					  <ServerQuitWhenAnyAgentFinishes/>
					</ServerHandlers>
				 </ServerSection>
				  
				 <AgentSection mode="Creative">
					<Name>Torchbearer</Name>
					<AgentStart>
						<Placement x="0" y="40" z="0"/>
						<Inventory>
							<InventoryItem slot="0" type="torch"/>
						</Inventory>
					</AgentStart>
					<AgentHandlers>
					  <ObservationFromFullStats/>
					  <ObservationFromGrid>
						  <Grid name="floor11x11">
							<min x="-5" y="-1" z="-5"/>
							<max x="5" y="-1" z="5"/>
						  </Grid>
					  </ObservationFromGrid>
					  <ContinuousMovementCommands turnSpeedDegs="180"/>
					  <InventoryCommands/>
					</AgentHandlers>
				  </AgentSection>
				</Mission>'''
				
def placeTorch():
	agent_host.sendCommand("use 1")
	time.sleep(0.1)
	agent_host.sendCommand("use 0")
	
def findCenter(x, z):
	retX = math.floor(x/2)
	retZ = math.floor(z/2)
	return (retX, retZ)

def teleport(self, agent_host, teleport_x, teleport_z):
	"""Directly teleport to a specific position."""
	tp_command = "tp " + str(teleport_x)+ " 40 " + str(teleport_z)
	agent_host.sendCommand(tp_command)
	good_frame = False
	start = timer()
	while not good_frame:
	world_state = agent_host.getWorldState()
	if not world_state.is_mission_running:
		print ("Mission ended prematurely - error.")
		exit(1)
	if not good_frame and world_state.number_of_video_frames_since_last_state > 0:
		frame_x = world_state.video_frames[-1].xPos
		frame_z = world_state.video_frames[-1].zPos
		if math.fabs(frame_x - teleport_x) < 0.001 and math.fabs(frame_z - teleport_z) < 0.001:
			good_frame = True
			end_frame = timer()

# Create default Malmo objects:

agent_host = MalmoPython.AgentHost()
try:
    agent_host.parse( sys.argv )
except RuntimeError as e:
    print 'ERROR:',e
    print agent_host.getUsage()
    exit(1)
if agent_host.receivedArgument("help"):
    print agent_host.getUsage()
    exit(0)

num_reps = 1000

# aList = set of light levels of the CURRENT mission
# bList = set of coordinates we have TRIED already, as a list of combinations/final (x,z) coordinates (or: [ [(tuple), (tuple), (tuple)], [(tuple), (tuple), (tuple)] ])
# cList = set of BEST coordinates to place torches, as a list of (x,z) coordinates (or: [(tuple), (tuple), (tuple)]) (chosen randomly compared to bList, based on number of torches placed/len of the combination)

for iRepeat in range(num_reps):
	#Allowed trials: trial6x6, trial8x8, trial10x10
	trial = trial6x6;

	my_mission = MalmoPython.MissionSpec(GetMissionXML(trial), True)
	my_mission_record = MalmoPython.MissionRecordSpec()

	num = 0

	if trial == trial6x6:
		num = 6
	elif trial == trial8x8:
		num = 8
	elif trial == trial10x10
		num = 10

	aList = []
	for i in range(num):
		aList.append([0]*num)

	# Attempt to start a mission:
	max_retries = 3
	for retry in range(max_retries):
		try:
			agent_host.startMission( my_mission, my_mission_record )
			break
		except RuntimeError as e:
			if retry == max_retries - 1:
				print "Error starting mission:",e
				exit(1)
			else:
				time.sleep(2)

	# Loop until mission starts:
	print "Waiting for the mission to start ",
	world_state = agent_host.getWorldState()
	while not world_state.has_mission_begun:
		sys.stdout.write(".")
		time.sleep(0.1)
		world_state = agent_host.getWorldState()
		for error in world_state.errors:
			print "Error:",error.text

	print
	print "Mission running ",


	while world_state.is_mission_running:
		sys.stdout.write(".")
		#time.sleep(0.1)
		agent_host.sendCommand("pitch 1")
		time.sleep(1.0)
		world_state = agent_host.getWorldState()
		for error in world_state.errors:
			print "Error:",error.text
		if world_state.number_of_observations_since_last_state > 0: 	# Have any observations come in?
			msg = world_state.observations[-1].text                 	# Yes, so get the text
			observations = json.loads(msg)                          	# and parse the JSON
			grid = observations.get(u'floor11x11', 0)               	# and get the grid we asked for
			
			