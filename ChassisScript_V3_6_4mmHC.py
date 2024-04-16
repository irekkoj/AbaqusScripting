#NOTES
#1. RUN IT FIRST, ABORT, DELETE EVERYTHING BUT JOB 1, OPEN ASSEMBLY IN ABAQUS AND RUN AGAIN. OTHERWISE IT WILL NOT FIND MASS FOR SOME REASON??????????
#2. Set the working directory and save location with each run.



# Save by u24jl20 on 2024_01_30-19.15.26; build 2023 2022_09_28-19.11.55 183150
from part import *
from material import *
from section import *
from assembly import *
from step import *
from interaction import *
from load import *
from mesh import *
from optimization import *
from job import *
from sketch import *
from visualization import *
from connectorBehavior import *
from abaqus import *
from abaqusConstants import *
import regionToolset
import time
import timeit
import os
from odbAccess import *


#variables

RollCageProfiles = [
    ('Tube31_75x2_03mm', 0.015875, 0.00203),
    ('Tube31_75x2_64mm', 0.015875, 0.00264),
    ('Tube38_10x2_03mm', 0.01905, 0.00203),
    ('Tube25_40x2_64mm', 0.01270, 0.00264)
]

RollCageProfilesNamesList = ['Tube38_10x2_03mm','Tube31_75x2_03mm','Tube25_40x2_64mm']

OtherProfiles = [
    ('Tube25_40x1_62mm', 0.0127, 0.00162),
    ('Tube25_40x2_03mm', 0.0127, 0.00203),
    ('Tube31_75x1_62mm', 0.015875, 0.00162),
    ('Tube38_10x1_62mm', 0.01905, 0.00162)
]

OtherProfilesNamesList = ['Tube25_40x1_62mm', 'Tube31_75x1_62mm']

TBThicknessList = [0.0005, 0.0007, 0.001, 0.0015, 0.002]
HCThicknessList = [0.01, 0.015, 0.02]

#Monocoques

MonocoquesNamesList = ['Monocoque6mm']


ModelBaseName = "Model"
JobBaseName = "Job"
NameNumber = 0


def check_file(filename):
    # Check if the file exists
    if os.path.exists(filename):
        # Get the size of the file in kilobytes
        file_size_kb = os.path.getsize(filename) / 1024
        if file_size_kb < 3000:
            # If file size is less than 3000KB, wait and check again
            print("File exists but is too small ({file_size_kb} KB). Waiting...")
            time.sleep(2)
            check_file(filename)  # Recursive call
        else:
            # If file size is equal or greater than 3000KB
            print("File exists and is of sufficient size ({file_size_kb} KB).")
    else:
        # If file does not exist, wait and check again
        print("File does not exist. Waiting...")
        time.sleep(2)
        check_file(filename)  # Recursive call


    
#######################################################Iteration start######################################################

#Iteration START

for item1 in MonocoquesNamesList:
    for item2 in OtherProfilesNamesList:
        for item3 in RollCageProfilesNamesList:
        	for item4 in TBThicknessList:
        		for item5 in HCThicknessList:
            				start = timeit.default_timer()

					ModelName = ModelBaseName + str(NameNumber)
					JobName = JobBaseName + str(NameNumber)


					HC_Thickness = item5
					HC_Material = item1
					TB_Thickness = item4

					RollCageSection = item3
					MainTrussSection = item2
					SupportTrussSection = item2
					#######################################################Part creation start#################################################################################

					#Creating model
					mdb.Model(modelType=STANDARD_EXPLICIT, name=ModelName)

					mdb.models[ModelName].Part(dimensionality=THREE_D, name='Chassis', type=
						DEFORMABLE_BODY)
					mdb.models[ModelName].parts['Chassis'].ReferencePoint(point=(0.0, 0.0, 0.0))


					#Coordinates & Loactions of points in meters for the rear spaceframe (get these from solidworks)

					CoordinatesLeft = [[-0.225,0,0],[-0.3, 0.2,0.12],[-0.15,1.0,0.12],[-0.26,0.13,0.51],[-0.21,0.02,0.48],[-0.21,-0.03,0.71],[-0.26,0.11,0.75],[-0.19,-0.1,0.87]]
					CoordinatesRight = [[0.225,0,0],[0.3, 0.2,0.12],[0.15,1.0,0.12],[0.26,0.13,0.51],[0.21,0.02,0.48],[0.21,-0.03,0.71],[0.26,0.11,0.75],[0.19,-0.1,0.87]]


					#Coordinates into Abaqus

					for i in range(len(CoordinatesLeft)):
						mdb.models[ModelName].parts['Chassis'].DatumPointByCoordinate(coords=(CoordinatesLeft[i][0], CoordinatesLeft[i][1], CoordinatesLeft[i][2]))
						mdb.models[ModelName].parts['Chassis'].DatumPointByCoordinate(coords=(CoordinatesRight[i][0], CoordinatesRight[i][1], CoordinatesRight[i][2]))

					#Creating wires for spaceframe

					mdb.models[ModelName].parts['Chassis'].WirePolyLine(mergeType=IMPRINT, meshable=
						ON, points=((mdb.models[ModelName].parts['Chassis'].datums[6],
						mdb.models[ModelName].parts['Chassis'].datums[4]), (
						mdb.models[ModelName].parts['Chassis'].datums[2],
						mdb.models[ModelName].parts['Chassis'].datums[4]), (
						mdb.models[ModelName].parts['Chassis'].datums[4],
						mdb.models[ModelName].parts['Chassis'].datums[8]), (
						mdb.models[ModelName].parts['Chassis'].datums[8],
						mdb.models[ModelName].parts['Chassis'].datums[10]), (
						mdb.models[ModelName].parts['Chassis'].datums[10],
						mdb.models[ModelName].parts['Chassis'].datums[2]), (
						mdb.models[ModelName].parts['Chassis'].datums[2],
						mdb.models[ModelName].parts['Chassis'].datums[8]), (
						mdb.models[ModelName].parts['Chassis'].datums[8],
						mdb.models[ModelName].parts['Chassis'].datums[14]), (
						mdb.models[ModelName].parts['Chassis'].datums[14],
						mdb.models[ModelName].parts['Chassis'].datums[12]), (
						mdb.models[ModelName].parts['Chassis'].datums[12],
						mdb.models[ModelName].parts['Chassis'].datums[10]), (
						mdb.models[ModelName].parts['Chassis'].datums[8],
						mdb.models[ModelName].parts['Chassis'].datums[12]), (
						mdb.models[ModelName].parts['Chassis'].datums[16],
						mdb.models[ModelName].parts['Chassis'].datums[12]), (
						mdb.models[ModelName].parts['Chassis'].datums[8],
						mdb.models[ModelName].parts['Chassis'].datums[6])))
					mdb.models[ModelName].parts['Chassis'].Set(edges=
						mdb.models[ModelName].parts['Chassis'].edges.getSequenceFromMask(('[#fff ]',
						), ), name='Wire-1-Set-2')
					mdb.models[ModelName].parts['Chassis'].WirePolyLine(mergeType=IMPRINT, meshable=
						ON, points=((mdb.models[ModelName].parts['Chassis'].datums[7],
						mdb.models[ModelName].parts['Chassis'].datums[5]), (
						mdb.models[ModelName].parts['Chassis'].datums[5],
						mdb.models[ModelName].parts['Chassis'].datums[3]), (
						mdb.models[ModelName].parts['Chassis'].datums[3],
						mdb.models[ModelName].parts['Chassis'].datums[11]), (
						mdb.models[ModelName].parts['Chassis'].datums[11],
						mdb.models[ModelName].parts['Chassis'].datums[9]), (
						mdb.models[ModelName].parts['Chassis'].datums[9],
						mdb.models[ModelName].parts['Chassis'].datums[5]), (
						mdb.models[ModelName].parts['Chassis'].datums[3],
						mdb.models[ModelName].parts['Chassis'].datums[9]), (
						mdb.models[ModelName].parts['Chassis'].datums[9],
						mdb.models[ModelName].parts['Chassis'].datums[7]), (
						mdb.models[ModelName].parts['Chassis'].datums[11],
						mdb.models[ModelName].parts['Chassis'].datums[13]), (
						mdb.models[ModelName].parts['Chassis'].datums[13],
						mdb.models[ModelName].parts['Chassis'].datums[15]), (
						mdb.models[ModelName].parts['Chassis'].datums[15],
						mdb.models[ModelName].parts['Chassis'].datums[9]), (
						mdb.models[ModelName].parts['Chassis'].datums[9],
						mdb.models[ModelName].parts['Chassis'].datums[13]), (
						mdb.models[ModelName].parts['Chassis'].datums[13],
						mdb.models[ModelName].parts['Chassis'].datums[17])))
					mdb.models[ModelName].parts['Chassis'].Set(edges=
						mdb.models[ModelName].parts['Chassis'].edges.getSequenceFromMask((
						'[#fff000 ]', ), ), name='Wire-2-Set-1')
					mdb.models[ModelName].parts['Chassis'].WirePolyLine(mergeType=IMPRINT, meshable=
						ON, points=((mdb.models[ModelName].parts['Chassis'].datums[7],
						mdb.models[ModelName].parts['Chassis'].datums[6]), (
						mdb.models[ModelName].parts['Chassis'].datums[5],
						mdb.models[ModelName].parts['Chassis'].datums[4]), (
						mdb.models[ModelName].parts['Chassis'].datums[3],
						mdb.models[ModelName].parts['Chassis'].datums[2]), (
						mdb.models[ModelName].parts['Chassis'].datums[13],
						mdb.models[ModelName].parts['Chassis'].datums[12])))
					mdb.models[ModelName].parts['Chassis'].Set(edges=
						mdb.models[ModelName].parts['Chassis'].edges.getSequenceFromMask((
						'[#8800011 ]', ), ), name='Wire-3-Set-1')

					#Creating construction geometry

					mdb.models[ModelName].parts['Chassis'].DatumPlaneByThreePoints(point1=
						mdb.models[ModelName].parts['Chassis'].datums[4], point2=
						mdb.models[ModelName].parts['Chassis'].datums[2], point3=
						mdb.models[ModelName].parts['Chassis'].datums[3])

					mdb.models[ModelName].parts['Chassis'].DatumAxisByPrincipalAxis(principalAxis=
						YAXIS)

					mdb.models[ModelName].parts['Chassis'].DatumPlaneByPrincipalPlane(offset=-0.5,
						principalPlane=XYPLANE)
					mdb.models[ModelName].parts['Chassis'].DatumPlaneByPrincipalPlane(offset=-1.3,
						principalPlane=XYPLANE)

					#Creating rear roll hoop

					mdb.models[ModelName].ConstrainedSketch(gridSpacing=0.07, name='__profile__',
						sheetSize=3.18, transform=
						mdb.models[ModelName].parts['Chassis'].MakeSketchTransform(
						sketchPlane=mdb.models[ModelName].parts['Chassis'].datums[24],
						sketchPlaneSide=SIDE1,
						sketchUpEdge=mdb.models[ModelName].parts['Chassis'].datums[25],
						sketchOrientation=RIGHT, origin=(0.0, 0.513235, 0.307941)))
					mdb.models[ModelName].parts['Chassis'].projectReferencesOntoSketch(filter=
						COPLANAR_EDGES, sketch=mdb.models[ModelName].sketches['__profile__'])
					mdb.models[ModelName].sketches['__profile__'].Line(point1=(-0.3,
						-0.365291643356374), point2=(-0.225, -0.598529719150186))
					mdb.models[ModelName].sketches['__profile__'].Line(point1=(-0.225,
						-0.598529719150186), point2=(0.225, -0.598529719150186))
					mdb.models[ModelName].sketches['__profile__'].HorizontalConstraint(
						addUndoState=False, entity=
						mdb.models[ModelName].sketches['__profile__'].geometry[6])
					mdb.models[ModelName].sketches['__profile__'].Line(point1=(0.225,
						-0.598529719150186), point2=(0.3, -0.365291643356374))
					mdb.models[ModelName].parts['Chassis'].Wire(sketch=
						mdb.models[ModelName].sketches['__profile__'], sketchOrientation=RIGHT,
						sketchPlane=mdb.models[ModelName].parts['Chassis'].datums[24],
						sketchPlaneSide=SIDE1, sketchUpEdge=
						mdb.models[ModelName].parts['Chassis'].datums[25])
					del mdb.models[ModelName].sketches['__profile__']

					#Creating front roll hoop

					mdb.models[ModelName].ConstrainedSketch(gridSpacing=0.13, name='__profile__',
						sheetSize=5.31, transform=
						mdb.models[ModelName].parts['Chassis'].MakeSketchTransform(
						sketchPlane=mdb.models[ModelName].parts['Chassis'].datums[26],
						sketchPlaneSide=SIDE1,
						sketchUpEdge=mdb.models[ModelName].parts['Chassis'].datums[25],
						sketchOrientation=RIGHT, origin=(0.0, 0.45, -0.5)))
					mdb.models[ModelName].parts['Chassis'].projectReferencesOntoSketch(filter=
						COPLANAR_EDGES, sketch=mdb.models[ModelName].sketches['__profile__'])
					mdb.models[ModelName].sketches['__profile__'].Line(point1=(-0.225, -0.45),
						point2=(0.225, -0.45))
					mdb.models[ModelName].sketches['__profile__'].HorizontalConstraint(
						addUndoState=False, entity=
						mdb.models[ModelName].sketches['__profile__'].geometry[3])
					mdb.models[ModelName].sketches['__profile__'].Line(point1=(-0.225, -0.45),
						point2=(0.2275, -0.2925))
					mdb.models[ModelName].sketches['__profile__'].Line(point1=(0.2275, -0.2925),
						point2=(-0.162500000093132, -0.2925))
					mdb.models[ModelName].sketches['__profile__'].HorizontalConstraint(
						addUndoState=False, entity=
						mdb.models[ModelName].sketches['__profile__'].geometry[5])
					mdb.models[ModelName].sketches['__profile__'].Line(point1=(-0.162500000093132,
						-0.2925), point2=(0.225, -0.45))
					mdb.models[ModelName].sketches['__profile__'].EqualLengthConstraint(entity1=
						mdb.models[ModelName].sketches['__profile__'].geometry[4], entity2=
						mdb.models[ModelName].sketches['__profile__'].geometry[6])
					mdb.models[ModelName].sketches['__profile__'].DistanceDimension(entity1=
						mdb.models[ModelName].sketches['__profile__'].geometry[5], entity2=
						mdb.models[ModelName].sketches['__profile__'].geometry[3], textPoint=(
						0.530370116233826, -0.397730362415314), value=0.06)
					mdb.models[ModelName].sketches['__profile__'].ObliqueDimension(textPoint=(
						0.064136728644371, -0.323367160558701), value=0.34, vertex1=
						mdb.models[ModelName].sketches['__profile__'].vertices[19], vertex2=
						mdb.models[ModelName].sketches['__profile__'].vertices[20])
					mdb.models[ModelName].sketches['__profile__'].Line(point1=(-0.17, -0.39),
						point2=(-0.4225, -0.13))
					mdb.models[ModelName].sketches['__profile__'].Line(point1=(-0.4225, -0.13),
						point2=(-0.0975, 0.065))
					mdb.models[ModelName].sketches['__profile__'].Line(point1=(-0.0975, 0.065),
						point2=(0.13, 0.065))
					mdb.models[ModelName].sketches['__profile__'].HorizontalConstraint(
						addUndoState=False, entity=
						mdb.models[ModelName].sketches['__profile__'].geometry[9])
					mdb.models[ModelName].sketches['__profile__'].Line(point1=(0.13, 0.065),
						point2=(0.4875, -0.195))
					mdb.models[ModelName].sketches['__profile__'].Line(point1=(0.4875, -0.195),
						point2=(0.17, -0.39))
					mdb.models[ModelName].sketches['__profile__'].Line(point1=(-0.4225, -0.13),
						point2=(0.4875, -0.195))
					mdb.models[ModelName].sketches['__profile__'].Line(point1=(0.4875, -0.195),
						point2=(-0.0975, 0.065))
					mdb.models[ModelName].sketches['__profile__'].Line(point1=(-0.4225, -0.13),
						point2=(0.13, 0.065))
					mdb.models[ModelName].sketches['__profile__'].HorizontalConstraint(entity=
						mdb.models[ModelName].sketches['__profile__'].geometry[12])
					mdb.models[ModelName].sketches['__profile__'].EqualLengthConstraint(entity1=
						mdb.models[ModelName].sketches['__profile__'].geometry[13], entity2=
						mdb.models[ModelName].sketches['__profile__'].geometry[14])
					mdb.models[ModelName].sketches['__profile__'].EqualLengthConstraint(entity1=
						mdb.models[ModelName].sketches['__profile__'].geometry[10], entity2=
						mdb.models[ModelName].sketches['__profile__'].geometry[8])
					mdb.models[ModelName].sketches['__profile__'].EqualLengthConstraint(entity1=
						mdb.models[ModelName].sketches['__profile__'].geometry[7], entity2=
						mdb.models[ModelName].sketches['__profile__'].geometry[11])
					mdb.models[ModelName].sketches['__profile__'].DistanceDimension(entity1=
						mdb.models[ModelName].sketches['__profile__'].geometry[9], entity2=
						mdb.models[ModelName].sketches['__profile__'].geometry[5], textPoint=(
						0.752559781074524, -0.247190189361572), value=0.5)
					mdb.models[ModelName].sketches['__profile__'].ObliqueDimension(textPoint=(
						-0.061527743935585, 0.213499116897583), value=0.44, vertex1=
						mdb.models[ModelName].sketches['__profile__'].vertices[23], vertex2=
						mdb.models[ModelName].sketches['__profile__'].vertices[24])
					mdb.models[ModelName].sketches['__profile__'].AngularDimension(line1=
						mdb.models[ModelName].sketches['__profile__'].geometry[8], line2=
						mdb.models[ModelName].sketches['__profile__'].geometry[9], textPoint=(
						-0.0542428642511368, -0.0893950581550598), value=94.0)
					mdb.models[ModelName].sketches['__profile__'].undo()
					mdb.models[ModelName].sketches['__profile__'].ObliqueDimension(textPoint=(
						0.495766997337341, -0.312484723329544), value=0.225, vertex1=
						mdb.models[ModelName].sketches['__profile__'].vertices[25], vertex2=
						mdb.models[ModelName].sketches['__profile__'].vertices[19])
					mdb.models[ModelName].sketches['__profile__'].AngularDimension(line1=
						mdb.models[ModelName].sketches['__profile__'].geometry[8], line2=
						mdb.models[ModelName].sketches['__profile__'].geometry[9], textPoint=(
						-0.123449459671974, -0.0168455362319946), value=94.0)


					mdb.models[ModelName].parts['Chassis'].Wire(sketch=
						mdb.models[ModelName].sketches['__profile__'], sketchOrientation=RIGHT,
						sketchPlane=mdb.models[ModelName].parts['Chassis'].datums[26],
						sketchPlaneSide=SIDE1, sketchUpEdge=
						mdb.models[ModelName].parts['Chassis'].datums[25])
					del mdb.models[ModelName].sketches['__profile__']
					mdb.models[ModelName].ConstrainedSketch(name='__edit__', objectToCopy=
						mdb.models[ModelName].parts['Chassis'].features['Wire-5'].sketch)
					mdb.models[ModelName].parts['Chassis'].projectReferencesOntoSketch(filter=
						COPLANAR_EDGES, sketch=mdb.models[ModelName].sketches['__edit__'],
						upToFeature=mdb.models[ModelName].parts['Chassis'].features['Wire-5'])
					mdb.models[ModelName].sketches['__edit__'].setAsConstruction(objectList=(
						mdb.models[ModelName].sketches['__edit__'].geometry[13],
						mdb.models[ModelName].sketches['__edit__'].geometry[14],
						mdb.models[ModelName].sketches['__edit__'].geometry[12],
						mdb.models[ModelName].sketches['__edit__'].geometry[6],
						mdb.models[ModelName].sketches['__edit__'].geometry[4],
						mdb.models[ModelName].sketches['__edit__'].geometry[3]))
					mdb.models[ModelName].parts['Chassis'].features['Wire-5'].setValues(sketch=
						mdb.models[ModelName].sketches['__edit__'])
					del mdb.models[ModelName].sketches['__edit__']
					mdb.models[ModelName].parts['Chassis'].regenerate()
					#Creating front roll hoop END

					#Creating Front BEGINNING
					mdb.models[ModelName].ConstrainedSketch(gridSpacing=0.13, name='__profile__',
						sheetSize=5.49, transform=
						mdb.models[ModelName].parts['Chassis'].MakeSketchTransform(
						sketchPlane=mdb.models[ModelName].parts['Chassis'].datums[27],
						sketchPlaneSide=SIDE1,
						sketchUpEdge=mdb.models[ModelName].parts['Chassis'].datums[25],
						sketchOrientation=RIGHT, origin=(0.0, 0.45, -1.3)))
					mdb.models[ModelName].parts['Chassis'].projectReferencesOntoSketch(filter=
						COPLANAR_EDGES, sketch=mdb.models[ModelName].sketches['__profile__'])
					mdb.models[ModelName].sketches['__profile__'].Line(point1=(-0.21, -0.48),
						point2=(0.21, -0.48))
					mdb.models[ModelName].sketches['__profile__'].HorizontalConstraint(
						addUndoState=False, entity=
						mdb.models[ModelName].sketches['__profile__'].geometry[3])
					mdb.models[ModelName].sketches['__profile__'].Line(point1=(0.0, -0.48), point2=
						(0.0, -0.31674064398976))
					mdb.models[ModelName].sketches['__profile__'].VerticalConstraint(addUndoState=
						False, entity=mdb.models[ModelName].sketches['__profile__'].geometry[4])
					mdb.models[ModelName].sketches['__profile__'].PerpendicularConstraint(
						addUndoState=False, entity1=
						mdb.models[ModelName].sketches['__profile__'].geometry[3], entity2=
						mdb.models[ModelName].sketches['__profile__'].geometry[4])
					mdb.models[ModelName].sketches['__profile__'].CoincidentConstraint(
						addUndoState=False, entity1=
						mdb.models[ModelName].sketches['__profile__'].vertices[18], entity2=
						mdb.models[ModelName].sketches['__profile__'].geometry[3])
					mdb.models[ModelName].sketches['__profile__'].EqualDistanceConstraint(
						addUndoState=False, entity1=
						mdb.models[ModelName].sketches['__profile__'].vertices[16], entity2=
						mdb.models[ModelName].sketches['__profile__'].vertices[17], midpoint=
						mdb.models[ModelName].sketches['__profile__'].vertices[18])
					mdb.models[ModelName].sketches['__profile__'].CoincidentConstraint(
						addUndoState=False, entity1=
						mdb.models[ModelName].sketches['__profile__'].vertices[19], entity2=
						mdb.models[ModelName].sketches['__profile__'].geometry[2])
					mdb.models[ModelName].sketches['__profile__'].delete(objectList=(
						mdb.models[ModelName].sketches['__profile__'].geometry[2], ))
					mdb.models[ModelName].sketches['__profile__'].delete(objectList=(
						mdb.models[ModelName].sketches['__profile__'].geometry[4], ))
					mdb.models[ModelName].sketches['__profile__'].Line(point1=(-0.21, -0.48),
						point2=(0.1625, -0.325))
					mdb.models[ModelName].sketches['__profile__'].Line(point1=(0.1625, -0.325),
						point2=(-0.13, -0.325))
					mdb.models[ModelName].sketches['__profile__'].HorizontalConstraint(
						addUndoState=False, entity=
						mdb.models[ModelName].sketches['__profile__'].geometry[6])
					mdb.models[ModelName].sketches['__profile__'].Line(point1=(-0.13, -0.325),
						point2=(0.21, -0.48))
					mdb.models[ModelName].sketches['__profile__'].EqualLengthConstraint(entity1=
						mdb.models[ModelName].sketches['__profile__'].geometry[7], entity2=
						mdb.models[ModelName].sketches['__profile__'].geometry[5])
					mdb.models[ModelName].sketches['__profile__'].DistanceDimension(entity1=
						mdb.models[ModelName].sketches['__profile__'].geometry[6], entity2=
						mdb.models[ModelName].sketches['__profile__'].geometry[3], textPoint=(
						0.51225346326828, -0.446516585350037), value=0.12)
					mdb.models[ModelName].sketches['__profile__'].ObliqueDimension(textPoint=(
						0.669393837451935, -0.286205124855042), value=0.26, vertex1=
						mdb.models[ModelName].sketches['__profile__'].vertices[21], vertex2=
						mdb.models[ModelName].sketches['__profile__'].vertices[22])
					mdb.models[ModelName].sketches['__profile__'].setAsConstruction(objectList=(
						mdb.models[ModelName].sketches['__profile__'].geometry[5],
						mdb.models[ModelName].sketches['__profile__'].geometry[7]))
					mdb.models[ModelName].sketches['__profile__'].Line(point1=(-0.13, -0.36),
						point2=(0.13, -0.195))
					mdb.models[ModelName].sketches['__profile__'].Line(point1=(0.13, -0.195),
						point2=(-0.162500000093132, -0.195))
					mdb.models[ModelName].sketches['__profile__'].HorizontalConstraint(
						addUndoState=False, entity=
						mdb.models[ModelName].sketches['__profile__'].geometry[9])
					mdb.models[ModelName].sketches['__profile__'].Line(point1=(-0.162500000093132,
						-0.195), point2=(0.13, -0.36))
					mdb.models[ModelName].sketches['__profile__'].EqualLengthConstraint(entity1=
						mdb.models[ModelName].sketches['__profile__'].geometry[8], entity2=
						mdb.models[ModelName].sketches['__profile__'].geometry[10])
					mdb.models[ModelName].sketches['__profile__'].ObliqueDimension(textPoint=(
						0.0446645766496658, -0.0610057234764099), value=0.33, vertex1=
						mdb.models[ModelName].sketches['__profile__'].vertices[24], vertex2=
						mdb.models[ModelName].sketches['__profile__'].vertices[25])
					mdb.models[ModelName].sketches['__profile__'].DistanceDimension(entity1=
						mdb.models[ModelName].sketches['__profile__'].geometry[9], entity2=
						mdb.models[ModelName].sketches['__profile__'].geometry[6], textPoint=(
						0.456679284572601, -0.253761154413223), value=0.26)
					mdb.models[ModelName].sketches['__profile__'].Line(point1=(-0.165, -0.1),
						point2=(-0.13, -0.36))
					mdb.models[ModelName].sketches['__profile__'].Line(point1=(0.165, -0.1),
						point2=(0.13, -0.36))
					mdb.models[ModelName].sketches['__profile__'].setAsConstruction(objectList=(
						mdb.models[ModelName].sketches['__profile__'].geometry[10],
						mdb.models[ModelName].sketches['__profile__'].geometry[8]))
					mdb.models[ModelName].sketches['__profile__'].setAsConstruction(objectList=(
						mdb.models[ModelName].sketches['__profile__'].geometry[3], ))
					mdb.models[ModelName].parts['Chassis'].Wire(sketch=
						mdb.models[ModelName].sketches['__profile__'], sketchOrientation=RIGHT,
						sketchPlane=mdb.models[ModelName].parts['Chassis'].datums[27],
						sketchPlaneSide=SIDE1, sketchUpEdge=
						mdb.models[ModelName].parts['Chassis'].datums[25])
					del mdb.models[ModelName].sketches['__profile__']
					#Creating Front END

					#Creating Lofts START
					mdb.models[ModelName].parts['Chassis'].ShellLoft(endCondition=NONE,
						loftsections=((mdb.models[ModelName].parts['Chassis'].edges[6],
						mdb.models[ModelName].parts['Chassis'].edges[22],
						mdb.models[ModelName].parts['Chassis'].edges[28]), (
						mdb.models[ModelName].parts['Chassis'].edges[0],
						mdb.models[ModelName].parts['Chassis'].edges[1],
						mdb.models[ModelName].parts['Chassis'].edges[3],
						mdb.models[ModelName].parts['Chassis'].edges[4],
						mdb.models[ModelName].parts['Chassis'].edges[5])), startCondition=NONE)
					mdb.models[ModelName].parts['Chassis'].ShellLoft(endCondition=NONE,
						loftsections=((mdb.models[ModelName].parts['Chassis'].edges[4],
						mdb.models[ModelName].parts['Chassis'].edges[32],
						mdb.models[ModelName].parts['Chassis'].edges[36],
						mdb.models[ModelName].parts['Chassis'].edges[39],
						mdb.models[ModelName].parts['Chassis'].edges[42],
						mdb.models[ModelName].parts['Chassis'].edges[45],
						mdb.models[ModelName].parts['Chassis'].edges[48],
						mdb.models[ModelName].parts['Chassis'].edges[51]), (
						mdb.models[ModelName].parts['Chassis'].edges[0],
						mdb.models[ModelName].parts['Chassis'].edges[1],
						mdb.models[ModelName].parts['Chassis'].edges[2],
						mdb.models[ModelName].parts['Chassis'].edges[3])), startCondition=NONE)

					#Creating end caps to monocoque
					mdb.models[ModelName].parts['Chassis'].ShellLoft(endCondition=NONE,
						loftsections=((mdb.models[ModelName].parts['Chassis'].edges[38], ), (
						mdb.models[ModelName].parts['Chassis'].edges[52], )), startCondition=NONE)
					mdb.models[ModelName].parts['Chassis'].ShellLoft(globalSmoothing=ON,
						loftsections=((mdb.models[ModelName].parts['Chassis'].edges[58],
						mdb.models[ModelName].parts['Chassis'].edges[60],
						mdb.models[ModelName].parts['Chassis'].edges[62]), (
						mdb.models[ModelName].parts['Chassis'].edges[24], )), paths=((
						mdb.models[ModelName].parts['Chassis'].edges[64],
						mdb.models[ModelName].parts['Chassis'].edges[66]), (
						mdb.models[ModelName].parts['Chassis'].edges[53],
						mdb.models[ModelName].parts['Chassis'].edges[56])))

					#Creating Lofts END
					################################################################## Part creation ends ##################################################################

					#creating materials

					mdb.models[ModelName].Material(name='Steel')
					mdb.models[ModelName].materials['Steel'].Density(table=((7800.0, ), ))
					mdb.models[ModelName].materials['Steel'].Elastic(table=((200000000000.0, 0.33), ))


                                        mdb.models[ModelName].Material(name='Monocoque6mm') #Done checked
                                        mdb.models[ModelName].materials['Monocoque6mm'].Density(table=((42.34, ), ))
                                        mdb.models[ModelName].materials['Monocoque6mm'].Elastic(table=((276893.8, 
                                                281239.5, 1056885442.6, 0.991, 8.6e-05, 8.78e-05, 159993.9, 223954376.8, 
                                                150817486.6), ), type=ENGINEERING_CONSTANTS)


					#Al3003
					mdb.models[ModelName].Material(name='Al3003')
					mdb.models[ModelName].materials['Al3003'].Elastic(table=((68500000000.0, 0.33),
						))
					mdb.models[ModelName].materials['Al3003'].Plastic(scaleStress=None, table=((
						37000000.0, 0.0), (41000000.0, 0.001242), (46000000.0, 0.002169), (54000000.0, 0.004652), (60000000.0,
						0.007064), (68000000.0, 0.010347), (76000000.0, 0.014731), (82000000.0, 0.019343), (89000000.0,
						0.025241), (95000000.0, 0.031053), (100000000.0, 0.03778), (105000000.0, 0.044907), (110000000.0,
						0.052534), (113000000.0, 0.061191), (116000000.0, 0.069947), (119000000.0, 0.078303), (122000000.0,
						0.088959), (125000000.0, 0.101715), (129000000.0, 0.115657), (131000000.0, 0.124528)))
					mdb.models[ModelName].materials['Al3003'].Density(table=((2730.0, ), ))

					#Al5052
					mdb.models[ModelName].Material(name='Al5052')
					mdb.models[ModelName].materials['Al5052'].Density(table=((2680.0, ), ))
					mdb.models[ModelName].materials['Al5052'].Elastic(table=((70000000000.0, 0.33),
						))
					mdb.models[ModelName].materials['Al5052'].Plastic(scaleStress=None, table=((
						66000000.0, 0.0), (80000000.0, 0.0003), (87000000.0, 0.0007), (91000000.0, 0.0011429), (95000000.0,
						0.0015857), (97000000.0, 0.0019571), (98000000.0, 0.0021429), (99000000.0, 0.0024286), (
						100000000.0, 0.0027143), (101000000.0, 0.003), (102000000.0, 0.0032857), (103000000.0, 0.0035714),
						(104000000.0, 0.0038571), (105000000.0, 0.0041429), (106000000.0, 0.0044286), (107000000.0,
						0.0047143), (107000000.0, 0.0050143), (108000000.0, 0.0053), (109000000.0, 0.0055857), (
						109000000.0, 0.0058857), (110000000.0, 0.0061714), (110000000.0, 0.0064714), (111000000.0,
						0.0067571), (111000000.0, 0.0070571)))

					#Al1050
					mdb.models[ModelName].Material(name='AL1050')
					mdb.models[ModelName].materials['AL1050'].Density(table=((2705.0, ), ))
					mdb.models[ModelName].materials['AL1050'].Elastic(table=((71000000000.0, 0.33),
						))
					mdb.models[ModelName].materials['AL1050'].Plastic(scaleStress=None, table=((
						16000000, 0.0), (22550000, 0.0012083), (21390000, 0.0018246), (26740000, 0.0043493), (
						32000000.0, 0.0081752), (37000000.0, 0.0132048), (42000000.0, 0.0194344), (44000000.0, 0.0265062),
						(48000000.0, 0.0338499), (49000000.0, 0.0424358), (51000000.0, 0.0519076), (53000000.0, 0.0620794),
						(55000000.0, 0.0741513), (56000000.0, 0.0895372), (57000000.0, 0.1062231), (57000000.0, 0.1175231),
						(58000000.0, 0.132509)))

					#Creating Sets

					mdb.models[ModelName].parts['Chassis'].Set(faces=
						mdb.models[ModelName].parts['Chassis'].faces.getSequenceFromMask((
						'[#7ffff ]', ), ), name='Monocoque', referencePoints=(
						mdb.models[ModelName].parts['Chassis'].referencePoints[1], ))


					#creating Profiles


					#Roll cage

					for profile_name, radius, thickness in RollCageProfiles:
						mdb.models[ModelName].PipeProfile(name=profile_name, r=radius, t=thickness)

					#Rest

					for profile_name, radius, thickness in OtherProfiles:
						mdb.models[ModelName].PipeProfile(name=profile_name, r=radius, t=thickness)

					#creating Sections

						mdb.models[ModelName].BeamSection(consistentMassMatrix=False, integration=
						DURING_ANALYSIS, material='Steel', name=profile_name, poissonRatio=
						0.0, profile=profile_name, temperatureVar=LINEAR)

					for profile_name, radius, thickness in RollCageProfiles:
						mdb.models[ModelName].PipeProfile(name=profile_name, r=radius, t=thickness)

						mdb.models[ModelName].BeamSection(consistentMassMatrix=False, integration=
						DURING_ANALYSIS, material='Steel', name=profile_name, poissonRatio=
						0.0, profile=profile_name, temperatureVar=LINEAR)



					#Assigning Sections to spaceframe START

					mdb.models[ModelName].parts['Chassis'].Set(edges=
						mdb.models[ModelName].parts['Chassis'].edges.getSequenceFromMask((
						'[#860000 ]', ), ), name='RollCage')
					mdb.models[ModelName].parts['Chassis'].SectionAssignment(offset=0.0,
						offsetField='', offsetType=MIDDLE_SURFACE, region=
						mdb.models[ModelName].parts['Chassis'].sets['RollCage'], sectionName=
						RollCageSection, thicknessAssignment=FROM_SECTION)

					mdb.models[ModelName].parts['Chassis'].Set(edges=
						mdb.models[ModelName].parts['Chassis'].edges.getSequenceFromMask((
						'[#31ed7e ]', ), ), name='MainTrusses')
					mdb.models[ModelName].parts['Chassis'].SectionAssignment(offset=0.0,
						offsetField='', offsetType=MIDDLE_SURFACE, region=
						mdb.models[ModelName].parts['Chassis'].sets['MainTrusses'], sectionName=
						MainTrussSection, thicknessAssignment=FROM_SECTION)

					mdb.models[ModelName].parts['Chassis'].Set(edges=
						mdb.models[ModelName].parts['Chassis'].edges.getSequenceFromMask((
						'[#481281 ]', ), ), name='SupportingTrusses')
					mdb.models[ModelName].parts['Chassis'].SectionAssignment(offset=0.0,
						offsetField='', offsetType=MIDDLE_SURFACE, region=
						mdb.models[ModelName].parts['Chassis'].sets['SupportingTrusses'],
						sectionName=SupportTrussSection, thicknessAssignment=FROM_SECTION)

					#beam orientations
					mdb.models[ModelName].parts['Chassis'].assignBeamSectionOrientation(method=
						N1_COSINES, n1=(0.0, 0.0, -1.0), region=
						mdb.models[ModelName].parts['Chassis'].sets['Wire-1-Set-2'])
					mdb.models[ModelName].parts['Chassis'].assignBeamSectionOrientation(method=
						N1_COSINES, n1=(0.0, 0.0, -1.0), region=
						mdb.models[ModelName].parts['Chassis'].sets['Wire-2-Set-1'])
					mdb.models[ModelName].parts['Chassis'].assignBeamSectionOrientation(method=
						N1_COSINES, n1=(0.0, 0.0, -1.0), region=
						mdb.models[ModelName].parts['Chassis'].sets['Wire-3-Set-1'])

					#Assigning Sections to spaceframe END



					#Creating composite layup and assigning section to monocoque

					mdb.models[ModelName].parts['Chassis'].CompositeLayup(description='', 
						elementType=SHELL, name='CompositeLayup-1', offsetType=MIDDLE_SURFACE, 
						symmetric=False, thicknessAssignment=FROM_SECTION)
					mdb.models[ModelName].parts['Chassis'].compositeLayups['CompositeLayup-1'].Section(
						integrationRule=SIMPSON, poissonDefinition=DEFAULT, preIntegrate=OFF, 
						temperature=GRADIENT, thicknessType=UNIFORM, useDensity=OFF)
					mdb.models[ModelName].parts['Chassis'].compositeLayups['CompositeLayup-1'].ReferenceOrientation(
						additionalRotationType=ROTATION_NONE, angle=0.0, axis=AXIS_3, fieldName='', 
						localCsys=None, orientationType=GLOBAL)

					mdb.models[ModelName].parts['Chassis'].compositeLayups['CompositeLayup-1'].CompositePly(
						additionalRotationField='', additionalRotationType=ROTATION_NONE, angle=0.0
						, axis=AXIS_3, material='AL1050', numIntPoints=3, orientationType=
						SPECIFY_ORIENT, orientationValue=0.0, plyName='Ply-1', region=
						mdb.models[ModelName].parts['Chassis'].sets['Monocoque'], suppressed=False, 
						thickness=TB_Thickness, thicknessType=SPECIFY_THICKNESS)

					mdb.models[ModelName].parts['Chassis'].compositeLayups['CompositeLayup-1'].CompositePly(
						additionalRotationField='', additionalRotationType=ROTATION_NONE, angle=0.0
						, axis=AXIS_3, material=HC_Material, numIntPoints=3, orientationType=
						SPECIFY_ORIENT, orientationValue=0.0, plyName='Ply-2', region=
						mdb.models[ModelName].parts['Chassis'].sets['Monocoque'], suppressed=False, 
						thickness=HC_Thickness, thicknessType=SPECIFY_THICKNESS)

					mdb.models[ModelName].parts['Chassis'].compositeLayups['CompositeLayup-1'].CompositePly(
						additionalRotationField='', additionalRotationType=ROTATION_NONE, angle=0.0
						, axis=AXIS_3, material='AL1050', numIntPoints=3, orientationType=
						SPECIFY_ORIENT, orientationValue=0.0, plyName='Ply-3', region=
						mdb.models[ModelName].parts['Chassis'].sets['Monocoque'], suppressed=False, 
						thickness=TB_Thickness, thicknessType=SPECIFY_THICKNESS)



					#Moving Part to assembly

					mdb.models[ModelName].rootAssembly.DatumCsysByDefault(CARTESIAN)
					mdb.models[ModelName].rootAssembly.Instance(dependent=ON, name='Chassis-1',
						part=mdb.models[ModelName].parts['Chassis'])


					#getting mass properties
					
					mass = mdb.models[ModelName].parts['Chassis'].getMassProperties()['mass']
					print(mass)

					#Creating Steps
					mdb.models[ModelName].StaticStep(initialInc=0.1, name='Step-1', previous=
						'Initial')

					mdb.models[ModelName].fieldOutputRequests['F-Output-1'].setValues(variables=(
						'S', 'PE', 'PEEQ', 'PEMAG', 'U', 'UR'))


					#Fixing edges before meshing
					mdb.models[ModelName].parts['Chassis'].ignoreEntity(entities=(
						mdb.models[ModelName].parts['Chassis'].vertices.getSequenceFromMask((
						'[#40000000 ]', ), ), ))
					mdb.models[ModelName].parts['Chassis'].ignoreEntity(entities=(
						mdb.models[ModelName].parts['Chassis'].vertices.getSequenceFromMask((
						'[#0 #80 ]', ), ), ))


					#Meshing part

					mdb.models[ModelName].parts['Chassis'].seedEdgeBySize(constraint=FINER,
						deviationFactor=0.1, edges=
						mdb.models[ModelName].parts['Chassis'].edges.getSequenceFromMask((
						'[#0 #280 ]', ), ), minSizeFactor=0.1, size=0.025)

					mdb.models[ModelName].parts['Chassis'].seedPart(deviationFactor=0.1,
						minSizeFactor=0.1, size=0.048)
					mdb.models[ModelName].parts['Chassis'].generateMesh()

					mdb.models[ModelName].parts['Chassis'].setElementType(elemTypes=(ElemType(
						elemCode=S8R, elemLibrary=STANDARD), ElemType(elemCode=STRI65, 
						elemLibrary=STANDARD)), regions=(
						mdb.models[ModelName].parts['Chassis'].faces.getSequenceFromMask((
						'[#7ffff ]', ), ), ))


					#Creating Sets for Wheel constraints

					mdb.models[ModelName].parts['Chassis'].Set(elements=
						mdb.models[ModelName].parts['Chassis'].elements.getSequenceFromMask(mask=(
						'[#0:6 #2 #0 #8000000 #1 ]', ), ), name='LeftFrontWheelPart')
					mdb.models[ModelName].parts['Chassis'].Set(elements=
						mdb.models[ModelName].parts['Chassis'].elements.getSequenceFromMask(mask=(
						'[#0:15 #1080 #0 #80 ]', ), ), name='RightFrontWheel')


					mdb.models[ModelName].parts['Chassis'].Set(name='FrontRightWheelNodes', nodes=
						mdb.models[ModelName].parts['Chassis'].nodes.getSequenceFromMask(mask=(
						'[#0:7 #8 #0:18 #44000 ]', ), ))

					mdb.models[ModelName].parts['Chassis'].Set(name='FrontLeftWheelNodes', nodes=
						mdb.models[ModelName].parts['Chassis'].nodes.getSequenceFromMask(mask=(
						'[#0:4 #800 #0:17 #40000000 #4 ]', ), ))


					#Creating Loads and Constraints

					#Constraints
					mdb.models[ModelName].EncastreBC(createStepName='Initial', localCsys=None, 
						name='FrontLeftEncastre', region=
						mdb.models[ModelName].rootAssembly.instances['Chassis-1'].sets['FrontLeftWheelNodes'])
					mdb.models[ModelName].EncastreBC(createStepName='Initial', localCsys=None, 
						name='FrontRightEncastre', region=
						mdb.models[ModelName].rootAssembly.instances['Chassis-1'].sets['FrontRightWheelNodes'])


					#Loads
					mdb.models[ModelName].ConcentratedForce(cf2=-500.0, createStepName='Step-1', 
						distributionType=UNIFORM, field='', localCsys=None, name='RearRightDOW', 
						region=Region(
						vertices=mdb.models[ModelName].rootAssembly.instances['Chassis-1'].vertices.getSequenceFromMask(
						mask=('[#2010 ]', ), )))
					mdb.models[ModelName].ConcentratedForce(cf2=500.0, createStepName='Step-1', 
						distributionType=UNIFORM, field='', localCsys=None, name='RearLeftUP', 
						region=Region(
						vertices=mdb.models[ModelName].rootAssembly.instances['Chassis-1'].vertices.getSequenceFromMask(
						mask=('[#808 ]', ), )))


					#Running Study
					mdb.models[ModelName].rootAssembly.regenerate()
					mdb.Job(atTime=None, contactPrint=OFF, description='', echoPrint=OFF, 
						explicitPrecision=SINGLE, getMemoryFromAnalysis=True, historyPrint=OFF, 
						memory=90, memoryUnits=PERCENTAGE, model=ModelName, modelPrint=OFF, 
						multiprocessingMode=DEFAULT, name=JobName, nodalOutputPrecision=SINGLE, 
						numCpus=1, numGPUs=0, numThreadsPerMpiProcess=1, queue=None, resultsFormat=
						ODB, scratch='', type=ANALYSIS, userSubroutine='', waitHours=0, 
						waitMinutes=0)
					mdb.jobs[JobName].submit(consistencyChecking=OFF)


					odb_path = 'H:\Dump6\\'+str(JobName)+'.odb' #CHANGE TO WORKING DIRECTORY
                                        #odb_path = 'S:\\temp\\' + str(JobName)+'.odb'
                                        print(odb_path)
					check_file(odb_path)

					

		#######################################################Saving Data#########################################

					# Path to the data file
					output_file = 'H:\Thesis\Final Results\ChassisScriptOutput\TorsionalStiffnessResults6.txt'

					# Open the ODB file
					odb = openOdb(odb_path)

					# Variables to hold the maximum deflection and corresponding details
					max_deflection = 0
					max_deflection_details = None

					try:
						# Assuming you want to check the last frame of the last step
						last_step = odb.steps.keys()[-1]
						last_frame = odb.steps[last_step].frames[-1]

						# Accessing displacement data
						displacement = last_frame.fieldOutputs['UR']

						# Loop through each displacement value to find the maximum deflection
						for value in displacement.values:
							# Calculate the magnitude of the displacement vector
							deflection_magnitude = (value.data[0]**2 + value.data[1]**2 + value.data[2]**2)**0.5

							# Update maximum deflection if a larger value is found
							if deflection_magnitude > max_deflection:
								max_deflection = deflection_magnitude
								max_deflection_details = (value.nodeLabel, value.data)



					finally:
						odb.close()



					# Append the maximum deflection details to the output file
					with open(output_file, 'a') as file:  # Open in append mode
						if max_deflection_details:
							#file.write("Node Label, U1, U2, U3, Max Deflection\n")
							file.write("{},{},{},{},{},{},{},{},{},{},{}\n".format(max_deflection_details[0], 
                                                                                                            max_deflection_details[1][0],
                                                                                                            max_deflection_details[1][1],
                                                                                                            max_deflection_details[1][2],
                                                                                                            max_deflection,
                                                                                                            item1,
                                                                                                            item2,
                                                                                                            item3,
                                                                                                            item4,
                                                                                                            item5,
                                                                                                            mass))
					   
					print(timeit.default_timer() - start)
					NameNumber = NameNumber+1

