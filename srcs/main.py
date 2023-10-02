import pymesh
import vtk
import os
from sas import sas
#
# read in part
#
print('...reading in part...')
reader = vtk.vtkSTLReader()
reader.SetFileName("/srcs/prt.stl")
reader.Update()
prt = reader.GetOutput()
#
# get center of `mass'
#
print('...get COM...')
com = vtk.vtkCenterOfMass()
com.SetInputData(prt)
com.SetUseScalarsAsWeights(False)
com.Update()
G = com.GetCenter()
#
# transform COM to 0,0,0 (used for rotations)
#
tfm = vtk.vtkTransform()
tfm.Translate(-G[0],-G[1],-G[2])
tfm.Update()
tfm_flt =  vtk.vtkTransformPolyDataFilter()
tfm_flt.SetInputData(prt)
tfm_flt.SetTransform(tfm)
tfm_flt.Update()
prt = tfm_flt.GetOutput()
#
# write it out
#
print('...write out part transformed COM -> 0,0,0')
writer = vtk.vtkSTLWriter()
writer.SetFileName("/srcs/prt_000.stl")
writer.SetInputData(prt)
writer.Update()
#
# translate part so that bottom is at z = 10
#
bnds=prt.GetBounds()
tfm = vtk.vtkTransform()
tfm.Translate(0,0,-bnds[4]+10.)
tfm.Update()
tfm_flt =  vtk.vtkTransformPolyDataFilter()
tfm_flt.SetInputData(prt)
tfm_flt.SetTransform(tfm)
tfm_flt.Update()
non = tfm_flt.GetOutput()
#
# write it out (non design domain for supopt)
#
print('...write out non design domain...')
writer = vtk.vtkSTLWriter()
writer.SetFileName("/srcs/non.stl")
writer.SetInputData(non)
writer.Update()
#
# make the sources and sinks
#
sas()
#
# read in sink and append it to non
#
print('...write out overhang sinks...')
reader = vtk.vtkSTLReader()
reader.SetFileName("/srcs/snk.stl")
reader.Update()
snk = reader.GetOutput()
app_flt = vtk.vtkAppendPolyData()
app_flt.AddInputData(snk)
app_flt.AddInputData(non)
app_flt.Update()
app = app_flt.GetOutput()
#
# write out non and sink (for convex hull)
#
print('...write out union of overhang sinks and non design domain...')
writer = vtk.vtkSTLWriter()
writer.SetFileName("/srcs/non_snk.stl")
writer.SetInputData(app)
writer.Update()
#
# read in for pymesh and make convex hull
#
print('...make convex hull of sinks and non design domain...')
mesh=pymesh.load_mesh("/srcs/non_snk.stl")
con=pymesh.convex_hull(mesh,engine='auto')
#
# write out convex hull
#
pymesh.save_mesh("/srcs/con.stl",con)
#
# make convex hull (design domain) 10% bigger
#
reader = vtk.vtkSTLReader()
reader.SetFileName("/srcs/con.stl")
reader.Update()
con = reader.GetOutput()
#
print('...make convex hull 10% bigger in all directions (0 stays at 0)...')
tfm = vtk.vtkTransform()
tfm.Scale(1.1,1.1,1.1)
tfm.Update()
tfm_flt =  vtk.vtkTransformPolyDataFilter()
tfm_flt.SetInputData(con)
tfm_flt.SetTransform(tfm)
tfm_flt.Update()
con_scl = tfm_flt.GetOutput()
writer = vtk.vtkSTLWriter()
writer.SetFileName("/srcs/con_111.stl")
writer.SetInputData(con_scl)
writer.Update()
#
print('...subtract part from scaled convex hull')
#
mesh_a=pymesh.load_mesh("/srcs/con_111.stl")
mesh_b=pymesh.load_mesh("/srcs/non.stl")
output_mesh = pymesh.boolean(mesh_a, mesh_b, operation="difference",engine="cork")
pymesh.save_mesh("/srcs/dom.stl", output_mesh)
#
print('...for supopt use dom.stl (domain), src.stl (load), and snk.stl (boundary condition).')
#
os._exit(1)
#
print('read sink')

reader = vtk.vtkSTLReader()
reader.SetFileName("/srcs/snk.stl")
reader.Update()
snk = reader.GetOutput()

print('appending')
app_flt = vtk.vtkAppendPolyData()
app_flt.AddInputData(snk)
app_flt.AddInputData(prt_scl)
app_flt.Update()
app = app_flt.GetOutput()

print('writing')
writer = vtk.vtkSTLWriter()
writer.SetFileName("/srcs/prt_snk.stl")
writer.SetInputData(app)
writer.Update()

#mesh_a=pymesh.load_mesh("/srcs/prt_tfm_scl.stl")
#mesh_b=pymesh.load_mesh("/srcs/snk.stl")
#
print("doing union now")


#output_mesh = pymesh.boolean(mesh_a, mesh_b, operation="union",engine="igl")

#print("writing now")

#pymesh.save_mesh("/srcs/union.stl",output_mesh)






