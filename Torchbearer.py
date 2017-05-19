import MalmoPython
import os
import random
import sys
import time
import json
import random
import math
import errno
from timeit import default_timer as timer

trial6x6 = 	'''	
	<DrawingDecorator>
		<DrawCuboid x1="0" y1="39" z1="0" x2="5" y2="39" z2="5" type="obsidian"/>
		<DrawCuboid x1="0" y1="40" z1="0" x2="15" y2="40" z2="15" type="air"/>
	</DrawingDecorator>
	'''

trial8x8 = 	'''	
	<DrawingDecorator>
		<DrawCuboid x1="0" y1="39" z1="0" x2="7" y2="39" z2="7" type="obsidian"/>
		<DrawCuboid x1="0" y1="40" z1="0" x2="15" y2="40" z2="15" type="air"/>
	</DrawingDecorator>
	'''

trial10x10 = 	'''	
	<DrawingDecorator>
		<DrawCuboid x1="0" y1="39" z1="0" x2="9" y2="39" z2="9" type="obsidian"/>
		<DrawCuboid x1="0" y1="40" z1="0" x2="15" y2="40" z2="15" type="air"/>
	</DrawingDecorator>
	'''

def GetMissionXML( trial ):
	# generatorString = 2;0;127; for MC v1.7 and below
	return '''<?xml version="1.0" encoding="UTF-8" ?>
	<Mission xmlns="http://ProjectMalmo.microsoft.com" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance">
		<About>
			<Summary>Light the way!</Summary>
		</About>

		<ServerSection>
			<ServerInitialConditions>
				<AllowSpawning>false</AllowSpawning>
				<Time>
					<StartTime>14000</StartTime>
					<AllowPassageOfTime>false</AllowPassageOfTime>
				</Time>
				<Weather>clear</Weather>
			</ServerInitialConditions>
			<ServerHandlers>
				<FlatWorldGenerator generatorString="3;0;127;"/>
				''' + trial + '''
				<ServerQuitFromTimeUp timeLimitMs="45000"/>
				<ServerQuitWhenAnyAgentFinishes />
			</ServerHandlers>
		</ServerSection>

		<AgentSection mode="Creative">
			<Name>Lightbringer</Name>
			<AgentStart>
				<Placement x="0" y="40" z="0"/>
				<Inventory>
					<InventoryItem slot="0" type="torch"/>
				</Inventory>
			</AgentStart>
			<AgentHandlers>
			<ContinuousMovementCommands turnSpeedDegs="180"/>
			<MissionQuitCommands quitDescription="quit"/>
			</AgentHandlers>
		</AgentSection>

	</Mission>'''


class Torchbearer(object):
	def __init__(self, trialsize):
		"""
		Create Torchbearer AI, with empty lists of coordinates.
		
		Args:
			trialsize:	<int>	The size of the square that the AI will iterate over, as an nXn square.
		"""
		self.currentList = []
		for i in range(trialsize):
			self.currentList.append([0]*trialsize)
		
		self.triedList = []
		
		self.bestList = []
		
		self.position = (0,0)
		
		self.trial = trialsize
		
		self.currentTorches = []
		
		self.worst = []
		
		#currentList = list of light levels of the CURRENT mission
		#triedList = list of coordinates we have TRIED already, as a list of combinations/final (x,z) coordinates 
			#(or: [ [(tuple), (tuple), (tuple)], [(tuple), (tuple), (tuple)] ])
		#bestList = list of BEST coordinates to place torches, as a list of (x,z) coordinates 
			#(or: [(tuple), (tuple), (tuple)]) 
			#(chosen compared to bList, based on number of torches placed/len of the combination)
			
		#currentTorches = list of tuples in the current run.
		
		#worst = the longest list of tuples in triedList so far.

	def updateLists(self):
		# Updates the set of lists by placing a torch at the CURRENT POSITION.
		initialNum = 14 # Torch light level = 0
		for i,j in enumerate(self.currentList): # i = index of y; j = list at y
			disY = abs(self.position[1] - i)
			for a,b in enumerate(j): # a = index of x; b = number at x
				disX = abs(self.position[0] - a)
				tryNum = initialNum - (disX + disY) # Taxi Cab distance
				if(b < tryNum):
					j[a] = tryNum
		return

	def placeTorch(self, agent_host):
		# Places torch down in game world; does not affect algorithm.
		agent_host.sendCommand("use 1")
		time.sleep(0.1)
		agent_host.sendCommand("use 0")
		self.updateLists()
		

	def findCenter(self, x, z):
		# Finds center of trial
		retX = math.floor(x/2)
		retZ = math.floor(z/2)
		return (int(retX), int(retZ))

	def teleport(self, agent_host, teleport_x, teleport_z):
		"""Directly teleport to a specific position."""
		print ("Attempting teleport to",str(teleport_x),str(teleport_z))
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
		self.position = (teleport_x, teleport_z)
		
	def clearSelf(self):
		self.currentList = []
		for i in range(self.trial):
			self.currentList.append([0]*self.trial)
		self.currentTorches = []

# Create default Malmo objects:
if __name__ == '__main__':
	# For consistent results -- UNCOMMENT
	# random.seed(0)
	sys.stdout = os.fdopen(sys.stdout.fileno(), 'w', 0)  # flush print output immediately

	my_client_pool = MalmoPython.ClientPool()
	my_client_pool.add(MalmoPython.ClientInfo("127.0.0.1", 10000))

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

	#
	#Allowed trials: trial6x6, trial8x8, trial10x10
	trial = trial10x10
	#
	#

	num_reps = 10

	num = 0
	if(trial == trial6x6):
		num = 6
	elif(trial == trial8x8):
		num = 8
	elif(trial == trial10x10):
		num = 10

	# Initialize torchbearer with trial size (num)
	torchbearer = Torchbearer(num)
	# Initialize breaking point, where there's "too many torches"
	breaker = 5

	for iRepeat in range(num_reps):

		my_mission = MalmoPython.MissionSpec(GetMissionXML(trial), True)
		my_mission_record = MalmoPython.MissionRecordSpec()
		my_mission.allowAllAbsoluteMovementCommands()
		my_mission.requestVideo(800, 500)
		my_mission.setViewpoint(0)
		

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
		print "Mission running # ",iRepeat+1
		
		world_state = agent_host.getWorldState()
		for error in world_state.errors:
			print "Error:",error.text
		
		center = torchbearer.findCenter(num, num)
		# print("Are we running?",world_state.is_mission_running)

		agent_host.sendCommand("pitch 1")
		print("Trying to look down")
		time.sleep(1.0)
		
		# Control center torch
		# torchbearer.teleport(agent_host, center[0], center[1])
		# torchbearer.placeTorch(agent_host)

		# Check Torchbearer for list of light levels; quit if all are 8 or lower.
		
		# The current run's torchbearing.
		# IF WE HAVE A LIST WITH ONLY 1 TORCH, IT ISN'T GETTING MUCH BETTER IS IT?
		# SO NEVER TRY.
		
		while True:
			dark = False;
			for i in torchbearer.currentList:
				for j in i:
					if(j < 8): # 8 is light level that will respawn
						dark = True
			if(not dark):
				print("The area is alight!")
				endList = []
				for i,j in enumerate(torchbearer.currentList): # i is index, j is list
					for a,b in enumerate(j): # a is index, b is number
						if(b == 14):
							endList.append((a, i))
				#
				# TODO: check if the list is already tried.
				# If it isn't, we should add it.
				if(sorted(endList) not in torchbearer.triedList):
					torchbearer.triedList.append(sorted(endList))
				# print(torchbearer.currentList)
				#
				# Check if this tried but valid list is the longest so far
				# Really only works on the initial run.
				if(len(endList) > len(torchbearer.worst)):
					torchbearer.worst = endList
				torchbearer.clearSelf()
				break
			else:
				# Iterate twice: once to check for the amount of lowest light levels, the other time to add them.
				darkList = []
				lowest = 14
				for i in torchbearer.currentList:
					for j in i:
						if(j < lowest):
							lowest = j
				for i,j in enumerate(torchbearer.currentList): # i is index, j is list
					for a,b in enumerate(j): # a is index, b is number
						if(b == lowest):
							darkList.append((a,i))
			# print(darkList)
			
			# COMPLETELY RANDOM DISTRIBUTION
			# NO SMART CHECKS
			# NEED ALGORITHM
			# NEED TO IGNORE ALREADY TRIED SOLUTIONS
			
			tempDarkList = []
			tempDarkList.extend(darkList)
			for i in tempDarkList:
				tryTheseTorches = []
				tryTheseTorches.extend(torchbearer.currentTorches)
				tryTheseTorches.append(i)
				if(sorted(tryTheseTorches) in torchbearer.triedList):
					darkList.remove(i)
					
			if(len(darkList) == 0):
				print("Already tried this solution.")
				torchbearer.clearSelf()
				break
			
			rando = random.randint(0, len(darkList) - 1)
			
			torchbearer.teleport(agent_host, darkList[rando][0], darkList[rando][1])
			torchbearer.placeTorch(agent_host)
			torchbearer.currentTorches.append(torchbearer.position)
			
			# Check if the placed torches are either above our suspected control break, or more torches than our worst solution thus far.
			if(len(torchbearer.currentTorches) > breaker or (len(torchbearer.worst) > 0 and len(torchbearer.currentTorches) > len(torchbearer.worst))):
				print("Inefficient choices.")
				torchbearer.clearSelf()
				break
			
		#DEBUG BREAK
		#break
		# print(torchbearer.triedList)
		
		agent_host.sendCommand("quit")
		time.sleep(1)
		
	# Iterate twice: once to check for the lowest length amongst solutions, the other to add them.
	# print(torchbearer.worst)
	if(len(torchbearer.worst) > 0):
		bestLength = len(torchbearer.worst)
	else:
		bestLength = 1
	# print(bestLength)
	for i in torchbearer.triedList:
		if(len(i) < bestLength):
			bestLength = len(i)
	# print(bestLength)
	for i in torchbearer.triedList:
		# print(i)
		# print(len(i))
		if(len(i) == bestLength):
			torchbearer.bestList.append(i)
			
	print("Best locations: ")
	for i in torchbearer.bestList:
		print(i)